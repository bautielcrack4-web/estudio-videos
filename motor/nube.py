# -*- coding: utf-8 -*-
"""Corre UN video entero dentro de GitHub Actions (en la cuenta del usuario, con SUS claves de los secretos del repo).
Lo lanza .github/workflows/video.yml. Mismo motor que el Estudio de PC (server.py: sesión de Claude Code con DeepSeek,
proxy que mide el gasto, guardián). Cada ~2 min publica el avance en la rama `estado` (videos/<vid>.json), que es lo
que lee el panel. Lee los mensajes del panel (mensajes/<vid>.json). Al terminar sube final.mp4 a un Release.
Si se acerca al límite de 6 h de GitHub, frena, guarda todo en la caché y se relanza solo en otra máquina."""
import base64, json, os, shutil, subprocess, sys, time, urllib.error, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(BASE)
sys.path.insert(0, BASE + "/tools")
import _cfg

E = os.environ
VID = E["VID"]
REPO = E["GITHUB_REPOSITORY"]
TOK = E["GH_TOKEN"]
LIMITE = float(E.get("LIMITE_MIN", "320")) * 60     # GitHub corta a las 6 h: a las 5 h 20 min frenamos y seguimos en otra máquina
T0 = time.time()
RUN_URL = f"https://github.com/{REPO}/actions/runs/{E.get('GITHUB_RUN_ID', '')}"


def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)   # los logs del repo son PÚBLICOS: nunca imprimir claves ni el guion


def gh(method, path, body=None, ok404=True):
    rq = urllib.request.Request(E.get("GITHUB_API_URL", "https://api.github.com") + path, method=method,
                                data=json.dumps(body).encode() if body is not None else None,
                                headers={"Authorization": "Bearer " + TOK, "Accept": "application/vnd.github+json",
                                         "User-Agent": "estudio-videos", "X-GitHub-Api-Version": "2022-11-28"})
    for k in range(5):
        try:
            r = urllib.request.urlopen(rq, timeout=60).read()
            return json.loads(r) if r else {}
        except urllib.error.HTTPError as e:
            if e.code == 404 and ok404: return None
            if e.code in (409, 422) and method == "PUT": return {"_conflicto": True}
            log("GitHub", e.code, path)
        except Exception as e: log("GitHub", e)
        time.sleep(5 * (k + 1))
    return None


def rama_estado():
    if gh("GET", f"/repos/{REPO}/branches/estado"): return
    main = gh("GET", f"/repos/{REPO}")["default_branch"]
    sha = gh("GET", f"/repos/{REPO}/git/ref/heads/{main}")["object"]["sha"]
    gh("POST", f"/repos/{REPO}/git/refs", {"ref": "refs/heads/estado", "sha": sha})


def leer_estado(ruta):
    r = gh("GET", f"/repos/{REPO}/contents/{ruta}?ref=estado")
    if not r: return None, None
    return json.loads(base64.b64decode(r["content"]).decode("utf8")), r["sha"]


def escribir_estado(ruta, obj):
    for _ in range(3):
        _, sha = leer_estado(ruta)
        body = {"message": f"estado {VID}", "branch": "estado",
                "content": base64.b64encode(json.dumps(obj, ensure_ascii=False, indent=1).encode("utf8")).decode()}
        if sha: body["sha"] = sha
        r = gh("PUT", f"/repos/{REPO}/contents/{ruta}", body)
        if r and not r.get("_conflicto"): return True
        time.sleep(3)
    return False


try: os.remove(os.path.join(_cfg.DATOS, "relanzar_" + VID))   # vino en la caché de la máquina anterior
except OSError: pass

# ── 1) claves (secretos del repo) → config.json local de esta máquina (nunca se imprime)
c = _cfg.leer()
for k in ("deepseek", "openai", "fish", "runpod", "groq"):
    v = (E.get(k.upper() + "_API_KEY") or "").strip()
    if v: c[k] = v
c["github"] = TOK                                  # token del propio workflow: sube cara+audio un rato a ESTE repo (público) para RunPod
c["avatar_repo"] = REPO.split("/")[1]
c["fotos_motor"] = "openai"
_cfg.guardar(c)

# ── 2) el canal (lo sube el panel a canales/<id>/ del repo)
cid = E["CANAL"]
src = os.path.join(RAIZ, "canales", cid)
if not os.path.exists(os.path.join(src, "canal.json")): sys.exit(f"⛔ no existe el canal {cid} en el repo")
dst = os.path.join(_cfg.CANALES, cid)
os.makedirs(dst, exist_ok=True)
for f in os.listdir(src): shutil.copy2(os.path.join(src, f), os.path.join(dst, f))

import server                                      # noqa: E402  (crea las carpetas de datos)
import threading                                   # noqa: E402
server.preparar_brain()
threading.Thread(target=server.TS(("127.0.0.1", server.PROXY_PORT), server.Proxy).serve_forever, daemon=True).start()

ST = os.path.join(_cfg.DATOS, f"nube_{VID}.json")
st = server.jload(ST, {}) or {}
rama_estado()


import re                                          # noqa: E402
TAPAR = re.compile(r"(api[ _-]?key[^\n]{0,20}?)\S*\*+\S*|sk-[A-Za-z0-9_\-]{8,}|gh[ps]_[A-Za-z0-9]{8,}|rpa_[A-Za-z0-9]{8,}|gsk_[A-Za-z0-9]{8,}", re.I)
SECRETOS = [v for v in (str(c.get(k) or "") for k in ("deepseek", "openai", "fish", "runpod", "groq", "github")) if len(v) >= 8] + [TOK]
def tapar(t):                                      # el repo es público: nada que se parezca a una clave
    for v in SECRETOS: t = t.replace(v, "[oculto]")
    return TAPAR.sub(lambda m: (m.group(1) or "") + "[oculto]", t)
def limpio(o):
    if isinstance(o, str): return tapar(o)
    if isinstance(o, list): return [limpio(x) for x in o]
    if isinstance(o, dict): return {k: limpio(x) for k, x in o.items()}
    return o


# ── lo que muestra el panel: se publica entero en la rama `estado` (panel/<vid>/…) con git, que no gasta la cuota de la API
GIT_DIR = os.path.join(os.path.dirname(_cfg.DATOS.rstrip("/\\")), "estado_git")
GIT_URL = f"https://x-access-token:{TOK}@" + E.get("GITHUB_SERVER_URL", "https://github.com").split("://")[-1] + f"/{REPO}.git"


def git(*a):
    return subprocess.run(["git", "-C", GIT_DIR, *a], capture_output=True, text=True, timeout=300)


def preparar_git():
    if os.path.isdir(os.path.join(GIT_DIR, ".git")): return
    os.makedirs(GIT_DIR, exist_ok=True)
    git("init", "-q"); git("remote", "add", "origin", GIT_URL)
    git("config", "user.name", "estudio"); git("config", "user.email", "estudio@users.noreply.github.com")


def traer():
    r = git("fetch", "-q", "--depth", "1", "origin", "estado")
    return r.returncode == 0 and git("checkout", "-q", "-f", "--detach", "FETCH_HEAD").returncode == 0


def armar_panel(extra):
    """Escribe en la copia de git lo que cambió de este video. Devuelve la lista de rutas tocadas."""
    rid = st["rid"]; v = server.video(rid); cwd = v["cwd"]
    base = os.path.join(GIT_DIR, "panel", VID); os.makedirs(base, exist_ok=True)
    pub = st.setdefault("pub", {})
    def js(nombre, o):
        with open(os.path.join(base, nombre), "w", encoding="utf8") as fh: json.dump(limpio(o), fh, ensure_ascii=False, separators=(",", ":"))
    vista = {k: x for k, x in v.items() if k != "cwd"}
    vista["nube"] = extra
    js("video.json", vista)
    js("timeline.json", server.timeline(rid))
    g = server.gallery(rid); js("gallery.json", g)
    ev = server.events(rid); ult = ev[-250:]
    cortos = [{k: (x[:1500] if isinstance(x, str) else x) for k, x in e.items()} for e in ult]
    js("chat.json", {"total": len(ev), "desde": len(ev) - len(ult), "ev": cortos})

    def nuevo(clave, ruta):
        try: firma = str(os.path.getmtime(ruta))
        except OSError: return False
        if pub.get(clave) == firma: return False
        pub[clave] = firma; return True

    n = 0                                          # miniaturas: las fotos van apareciendo en el panel a medida que llegan
    for it in g["fotos"] + g["clips"] + [{"p": q} for q in g.get("qc", [])]:
        rel = it["p"]; full = os.path.join(cwd, rel)
        if n >= 150 or not nuevo("t:" + rel, full): continue
        j = server.thumb(full, 420, "/tmp/estudio_t")
        if not j: pub.pop("t:" + rel, None); continue
        dst = os.path.join(base, "t", rel + ".jpg"); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(j, dst); n += 1

    F = v.get("files") or {}
    for rel in [F.get(k) for k in ("guion", "reporte", "captions")] + ["planos.json"]:     # textos que abre el panel
        if not rel: continue
        full = os.path.join(cwd, rel)
        if nuevo("f:" + rel, full) and os.path.getsize(full) < 3_000_000:
            dst = os.path.join(base, "f", rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(full, encoding="utf8", errors="replace") as a, open(dst, "w", encoding="utf8") as b: b.write(tapar(a.read()))
    rel = F.get("master")
    if rel and nuevo("m:" + rel, os.path.join(cwd, rel)):   # la voz, liviana, para escucharla en la línea de tiempo
        dst = os.path.join(base, "f", rel + ".mp3"); os.makedirs(os.path.dirname(dst), exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(cwd, rel), "-ac", "1", "-b:a", "48k", dst], capture_output=True, timeout=300)
        w = server.wave(rid)
        if w: shutil.copy2(w, os.path.join(base, "wave.png"))
    server.jsave(ST, st)


def publicar_panel(extra):
    """Un solo commit con todo lo del panel. Si otro video (o un mensaje) empujó justo antes, se reintenta sobre lo nuevo."""
    if not st.get("rid"): return
    try:
        preparar_git()
        for intento in range(4):
            if not traer(): log("git: no pude traer la rama estado"); return
            if intento: st["pub"] = {k: x for k, x in st.get("pub", {}).items() if k[:2] not in ("t:", "f:", "m:")}
            armar_panel(extra)
            git("add", "-A", "panel/" + VID)
            if git("diff", "--cached", "--quiet").returncode == 0: return
            git("commit", "-q", "-m", "panel " + VID)
            if git("push", "-q", "origin", "HEAD:refs/heads/estado").returncode == 0: return
            time.sleep(4 + 3 * intento)
        log("git: no pude publicar el panel")
    except Exception as e: log("no pude publicar el panel:", type(e).__name__)


def clave_mala():
    """Si DeepSeek rechaza la clave, no tiene sentido insistir: se avisa en el panel enseguida."""
    for x in server.events(st["rid"])[-6:]:
        t = x.get("t") if isinstance(x.get("t"), str) else ""
        if re.search(r"401|Authentication Fails|invalid x-api-key|api key.*invalid", t, re.I): return True
    return False


def publicar(estado, extra=None):
    try:
        v = server.video(st["rid"]) if st.get("rid") else {}
        ev = []
        if st.get("rid"):
            for x in server.events(st["rid"])[-30:]:
                t = x.get("t") if isinstance(x.get("t"), str) else json.dumps(x.get("t"), ensure_ascii=False)
                ev.append({"k": x.get("k"), "t": tapar(t or "")[:400]})
        o = {"vid": VID, "titulo": E.get("TITULO"), "canal": cid, "estado": estado, "actualizado": time.time(),
             "creado": st.get("creado"), "run": RUN_URL, "pasos": (v.get("pipeline") or {}).get("steps"),
             "costo": v.get("cost"), "eventos": ev, "maquinas": st.get("maquinas", 1)}
        o.update(st.get("final") or {})
        o.update(extra or {})
        escribir_estado(f"videos/{VID}.json", o)
        publicar_panel({k: o.get(k) for k in ("titulo", "canal", "run", "estado", "error", "final", "release", "actualizado", "maquinas")})
    except Exception as e: log("no pude publicar el estado:", type(e).__name__)


def mensajes_nuevos():
    m, _ = leer_estado(f"mensajes/{VID}.json")
    m = m if isinstance(m, list) else []
    n = st.get("msj", 0)
    st["msj"] = len(m); server.jsave(ST, st)
    return [str(x.get("texto") if isinstance(x, dict) else x) for x in m[n:]]


# ── 3) arrancar o retomar la sesión
if not st.get("rid"):
    st["creado"] = time.time()
    try:
        st["rid"] = server.nuevo_video({"canal": cid, "titulo": E["TITULO"], "idea": E.get("IDEA", ""),
                                        "min": E.get("MINUTOS") or None, "cap": E.get("TOPE") or 2})
    except Exception as e:
        publicar("parado", {"error": "No arrancó: " + str(e)[:300]}); sys.exit(1)
    st["seguir"] = 0
    log("video lanzado")
else:
    st["maquinas"] = st.get("maquinas", 1) + 1
    server.launch(st["rid"], "La sesión siguió en otra máquina (GitHub corta cada 6 h). Todo lo tuyo está igual en tu carpeta: "
                             "mirá qué hay, NO rehagas nada y seguí el CAMINO RECTO del KIT hasta el final.")
    log("video retomado, máquina", st["maquinas"])
server.jsave(ST, st)
publicar("trabajando")

relanzar, ult = False, 0
while True:
    time.sleep(20)
    meta = server.jload(os.path.join(server.rdir(st["rid"]), "meta.json"), {})
    vivo = server.alive(meta.get("pid"))
    if time.time() - ult > 60:
        ult = time.time(); publicar("trabajando" if vivo else "pensando")
        nuevos = mensajes_nuevos()
        if nuevos:
            if vivo: meta.setdefault("cola", []).extend(nuevos); server.jsave(os.path.join(server.rdir(st["rid"]), "meta.json"), meta)
            else: server.launch(st["rid"], "\n\n".join(nuevos)); continue
    if time.time() - T0 > LIMITE:
        server.stop(st["rid"]); relanzar = True; log("límite de tiempo: sigue en otra máquina"); break
    if vivo: continue
    if meta.get("cola"):
        txt = "\n\n".join(meta["cola"]); meta["cola"] = []; server.jsave(os.path.join(server.rdir(st["rid"]), "meta.json"), meta)
        server.launch(st["rid"], txt); continue
    v = server.video(st["rid"])
    if v["pipeline"]["complete"]: break
    if v["estado"] == "tope": publicar("tope", {"error": "Se alcanzó el tope de gasto del video."}); sys.exit(0)
    if clave_mala(): publicar("parado", {"error": "DeepSeek rechazó la clave: revisala en la pestaña Claves y relanzá."}); sys.exit(1)
    if st.get("seguir", 0) >= 6: publicar("parado", {"error": "La sesión terminó sin completar el video (6 empujones)."}); sys.exit(1)
    st["seguir"] = st.get("seguir", 0) + 1; server.jsave(ST, st)
    server.launch(st["rid"], "Todavía falta terminar el video (final.mp4 + REPORTE.md). Seguí con el CAMINO RECTO del KIT desde donde "
                             "quedaste, sin rehacer lo que ya está y sin preguntar.")

if relanzar:
    open(os.path.join(_cfg.DATOS, "relanzar_" + VID), "w").write("1")
    publicar("trabajando", {"nota": "sigue en otra máquina"}); sys.exit(0)

# ── 4) entrega: Release con el final y el reporte
v = server.video(st["rid"]); cwd = v["cwd"]
fin = os.path.join(cwd, v["files"]["final"]) if v["files"].get("final") else None
tag = "video-" + VID
archivos = [x for x in (fin, os.path.join(cwd, "REPORTE.md")) if x and os.path.exists(x)]
r = subprocess.run(["gh", "release", "create", tag, *archivos, "--repo", REPO, "--title", (E.get("TITULO") or VID)[:120],
                    "--notes", f"Canal: {cid}. Hecho por el Estudio."], capture_output=True, text=True)
if r.returncode != 0:
    subprocess.run(["gh", "release", "upload", tag, *archivos, "--repo", REPO, "--clobber"], capture_output=True, text=True)
url = f"https://github.com/{REPO}/releases/download/{tag}/{os.path.basename(fin)}" if fin else None
st["final"] = {"final": url, "release": f"https://github.com/{REPO}/releases/tag/{tag}"}
server.jsave(ST, st)
publicar("listo")
log("listo")
