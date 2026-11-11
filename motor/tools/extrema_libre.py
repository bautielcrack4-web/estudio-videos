# -*- coding: utf-8 -*-
"""EDICIÓN EXTREMA LIBRE: DeepSeek dirige. Mira al presentador y las fotos, inventa el sistema visual del canal (gen/canal.tsx),
planifica la edición del video ENTERO, programa cada pieza en Remotion viendo sus fotos, saca cuadros de lo que hizo, los mira y corrige.
Sin catálogo ni receta de diseño: sólo recibe el video, las fotos, los clips y los datos técnicos.
Dos tipos: "full" (escena completa, sólo fuera del avatar) y "overlay" (fondo transparente, encima de lo que ya está en pantalla).
SEGURIDAD: el código que escribe DeepSeek se compila, se prueba y se renderiza SIEMPRE como el usuario sin claves (ESTUDIO_USUARIO_SESION),
con entorno por lista blanca. Si ese usuario no existe, no se ejecuta nada.
Cualquier pieza que falle queda con el b-roll normal: nunca rompe el video."""
import base64, concurrent.futures as cf, glob, io, json, os, re, shutil, subprocess, threading, time

FPS = 30
MAX_ESCENAS = 18
RES_DIRECTOR = 0.06        # lo máximo que puede costar cada llamada: el tope de gasto es duro
RES_CODIGO = 0.045
RES_OJO = 0.02
PERMITIDOS = re.compile(r"^(\./canal|react(/.*)?|remotion|@remotion/[\w-]+(/.*)?|three(/.*)?|@react-three/[\w-]+(/.*)?)$")
TEC = """Technical facts of the project (the only fixed things):
- Remotion 4.0.472, React 19. 1920x1080, 30 fps. One single .tsx file with `export default function Scene()`, no props. It plays full screen over the narration.
- Installed packages you may import: remotion, @remotion/three, three, @react-three/fiber, @remotion/google-fonts/<FontName> (e.g. import {loadFont} from '@remotion/google-fonts/Fraunces'; const {fontFamily} = loadFont();). Nothing else is installed.
- Photos are 16:9 in public/: <Img src={staticFile('fotos/p001.jpg')} />, or as three.js textures (THREE.TextureLoader + delayRender/continueRender).
- Stock video clips are in public/ too: <OffthreadVideo muted src={staticFile('clips/s123.mp4')} /> from remotion (it is a video element you can layer, mask, transform and place in CSS 3D like an image).
- Write every photo and clip id literally in the code, never build ids by computing them.
- Everything is a pure function of useCurrentFrame(): no CSS animations or transitions, no Math.random (use random('seed') from remotion), no Date, no setTimeout.
- Any text on screen is in the language of the transcript."""


def usuario(): return os.environ.get("ESTUDIO_USUARIO_SESION") or ""


def aislado(cmd):
    """El comando corre como el usuario sin claves, con un entorno armado por lista blanca."""
    u = usuario()
    if not u: raise RuntimeError("sin usuario aislado")
    pasa = {x: os.environ[x] for x in ("PATH", "LANG", "LC_ALL", "TZ") if x in os.environ}
    pasa.update(HOME="/home/" + u, USER=u)
    return ["sudo", "-n", "-H", "-u", u, "--", "env", "-i", *["%s=%s" % kv for kv in pasa.items()], "sh", "-c", 'umask 000; exec "$0" "$@"', *cmd]


def parar_aislados():
    """Si se corta el render, no quedan Chrome ni node dando vueltas."""
    if not usuario(): return
    try: subprocess.run(["sudo", "-n", "pkill", "-9", "-u", usuario(), "-f", "/tmp/extrema_pkg"], capture_output=True, timeout=30)      # sólo el render: la sesión del video sigue viva
    except Exception: pass


def preparar(T, PKG, log):
    if not os.path.exists(T + "/node_modules/remotion"):
        shutil.rmtree(T, ignore_errors=True); shutil.copytree(PKG, T, ignore=shutil.ignore_patterns("node_modules", "gen"))
        r = subprocess.run(["npm", "i", "--no-audit", "--no-fund", "--loglevel=error"], cwd=T, capture_output=True, text=True, timeout=900)
        if r.returncode: log("npm falló, queda el b-roll normal:", r.stderr[-400:]); return False
    else:
        shutil.copytree(PKG + "/src", T + "/src", dirs_exist_ok=True, ignore=shutil.ignore_patterns("gen"), copy_function=shutil.copyfile)
        for f in ("render.mjs", "smoke.mjs", "still.mjs"): shutil.copyfile(PKG + "/" + f, T + "/" + f)
    shutil.rmtree(T + "/src/gen", ignore_errors=True); os.makedirs(T + "/src/gen"); shutil.rmtree(T + "/public", ignore_errors=True); os.makedirs(T + "/public/fotos"); os.makedirs(T + "/public/clips")
    subprocess.run(["chmod", "-R", "a+rwX", T], check=True)      # lo usa el usuario sin claves; el dueño nunca ejecuta lo que quede acá
    return True


def verifica(T, f, frames):
    r = subprocess.run(aislado(["node", T + "/smoke.mjs", f, str(frames)]), cwd=T, capture_output=True, text=True, encoding="utf8", errors="replace", timeout=240)
    out = (r.stdout or r.stderr or "").strip()
    return "" if out.startswith("OK") else (out[:1800] or "the file did not run")


def importa_raro(c):
    malos = [m for m in re.findall(r"""(?:\bfrom\s*|\bimport\s*\(?\s*|\brequire\s*\(\s*)['"]([^'"]+)['"]""", c) if not PERMITIDOS.match(m)]
    return "These imports do not exist in this project: %s. Use only the installed packages." % ", ".join(sorted(set(malos))) if malos else ""


def transcripcion(W):
    ren, act, t0 = [], [], 0
    for w in W:
        if not act: t0 = w["startMs"]
        act.append(w["text"].strip())
        if w["endMs"] - t0 > 8000 or (act[-1][-1:] in ".?!" and w["endMs"] - t0 > 3000): ren.append("[%d-%d] %s" % (t0, w["endMs"], " ".join(act))); act = []
    if act: ren.append("[%d-%d] %s" % (t0, W[-1]["endMs"], " ".join(act)))
    return "\n".join(ren)


def huecos(AV, total):
    B, t = [], 0
    for r in sorted(AV, key=lambda x: x["startMs"]):
        if r["startMs"] - t >= 2000: B.append((t, r["startMs"]))
        t = max(t, r["endMs"])
    if total - t >= 2000: B.append((t, total))
    return B


def duracion(f):
    try: return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True, timeout=60).stdout.strip())
    except Exception: return 0.0


def limpiar_escenas(E, AV, total, log):
    """Lo que el director pidió y el video permite: dentro del video, sin encimarse, sin tapar al avatar con una escena completa."""
    pisa = lambda a, b, rs: any(a < r["endMs"] and b > r["startMs"] for r in rs)
    out = []
    for e in sorted([x for x in E if isinstance(x, dict)], key=lambda x: int(x.get("startMs") or 0)):
        try: a, b = max(0, int(e["startMs"])), min(total, int(e["endMs"]))
        except Exception: continue
        tipo = "overlay" if e.get("tipo") == "overlay" else "full"
        if tipo == "overlay": b = min(b, a + 12000)        # las capas pesan (ProRes con transparencia): cortas
        if not (2000 <= b - a <= 35000) or not str(e.get("idea") or "").strip(): continue
        if tipo == "full" and (a < 3000 or pisa(a, b, AV)): log("escena completa sobre el avatar, se descarta:", a, b); continue
        if tipo == "overlay" and pisa(a, b, [r for r in AV if r.get("foto")]): log("capa sobre pantalla partida, se descarta:", a, b); continue
        if any(a < x["endMs"] and b > x["startMs"] for x in out): continue
        out.append({"tipo": tipo, "startMs": a, "endMs": b, "idea": str(e["idea"])})
    return out[:MAX_ESCENAS]


# ── EL DIRECTOR: mira las fotos, inventa el sistema visual del canal, planifica el video entero, programa, MIRA sus cuadros y corrige
def _jpg(im, q=80):
    b = io.BytesIO(); im.convert("RGB").save(b, "JPEG", quality=q); return b.getvalue()


def con_img(texto, jpgs):
    return [{"type": "text", "text": texto}] + [{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(j).decode()}} for j in jpgs if j]


def _letra(tam):
    from PIL import ImageFont
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", tam)
    except Exception:
        try: return ImageFont.load_default(tam)
        except Exception: return ImageFont.load_default()


def hojas(fotos, tope=5):
    """Las fotos del video en hojas de contacto con su id escrito: el director elige MIRANDO, no leyendo descripciones."""
    from PIL import Image, ImageDraw
    ids = sorted(fotos); cols, fil, w, h, pie = 6, 5, 320, 180, 26
    por = cols * fil
    if len(ids) > por * tope: ids = [ids[round(k * (len(ids) - 1) / (por * tope - 1))] for k in range(por * tope)]
    out, letra = [], _letra(19)
    for k in range(0, len(ids), por):
        lote = ids[k:k + por]; H = Image.new("RGB", (cols * w, -(-len(lote) // cols) * (h + pie)), (18, 18, 18)); d = ImageDraw.Draw(H)
        for n, i in enumerate(lote):
            x, y = (n % cols) * w, (n // cols) * (h + pie)
            try: im = Image.open(fotos[i]).convert("RGB").resize((w - 4, h - 2)); H.paste(im, (x + 2, y))
            except Exception: pass
            d.text((x + 6, y + h + 1), "fotos/%s.jpg" % i, fill=(255, 255, 255), font=letra)
        out.append(_jpg(H, 78))
    return out


def foto_jpg(p, lado=768):
    from PIL import Image
    try: im = Image.open(p).convert("RGB"); im.thumbnail((lado, lado)); return _jpg(im, 82)
    except Exception: return None


def _bloque(c):
    bl = re.search(r"```(?:tsx|typescript|ts|jsx)?\s*\n(.*?)```", c or "", re.S)
    return bl.group(1) if bl else ""


def programar(T, i, frames, msgs, caja, ia, log, vueltas=2):
    """Pide el archivo, lo compila y lo prueba; si falla, le devuelve el error. Devuelve True si quedó un archivo que corre."""
    f = T + "/src/gen/%s.tsx" % i
    for n_ in range(vueltas):
        try: c = ia(caja, msgs, RES_CODIGO, 42000, True, False, 900, 1)
        except RuntimeError as x:
            if str(x) == "tope": log(i, "no alcanzó el tope de gasto"); return False
            log(i, "sin respuesta:", x); continue
        cod = _bloque(c)
        if not cod: msgs.append({"role": "user", "content": "Reply with the complete file in one ```tsx block."}); continue
        err = importa_raro(cod)
        if not err:
            open(f + ".nuevo", "w", encoding="utf8").write(cod); os.replace(f + ".nuevo", f); os.chmod(f, 0o666)
            try: err = verifica(T, f, frames)
            except subprocess.TimeoutExpired: err = "the scene takes too long to run"
        if not err: return True
        log(i, "intento", n_ + 1, "con error:", err[:160].replace("\n", " | "))
        msgs += [{"role": "assistant", "content": c}, {"role": "user", "content": err + "\nFix it and reply with the complete file in one ```tsx block."}]
    return False


def montar(B, T, G, fotos, clips):
    """Deja el paquete listo para sacar cuadros o renderizar: las fotos y clips que el código nombra, y el registro de piezas."""
    from PIL import Image
    pub = T + "/public"; codigo = ""
    for g in G:
        try: codigo += open(T + "/src/gen/%s.tsx" % g["id"], encoding="utf8").read() + "\n"
        except OSError: pass
    try: codigo += open(T + "/src/gen/canal.tsx", encoding="utf8").read()
    except OSError: pass
    usa = lambda i: re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(i), codigo)
    for i, p in fotos.items():
        if usa(i) and not os.path.exists(pub + "/fotos/" + i + ".jpg"):
            try: im = Image.open(p).convert("RGB"); im.thumbnail((1920, 1080)); im.save(pub + "/fotos/" + i + ".jpg", quality=86)
            except Exception: pass
    for i in clips:
        if usa(i) and not os.path.exists(pub + "/clips/" + i + ".mp4"): shutil.copyfile(B + "/clips/" + i + ".mp4", pub + "/clips/" + i + ".mp4")
    open(T + "/src/gen/manifest.ts", "w", encoding="utf8").write("".join("import c%d from './%s';\n" % (k, g["id"]) for k, g in enumerate(G)) +
        "export const comps = [%s];\n" % ",".join("{id:'%s',C:c%d,frames:%d}" % (g["id"], k, g["frames"]) for k, g in enumerate(G)))
    json.dump([g["id"] for g in G if g.get("tipo") == "overlay"], open(T + "/src/gen/capas.json", "w"))
    subprocess.run(["chmod", "-R", "a+rwX", T + "/src", T + "/public"], check=True)


PUNTOS = (.22, .55, .9)


def sacar_cuadros(T, X, G, log):
    """Renderiza 3 cuadros sueltos de cada pieza (a mitad de tamaño). Devuelve {id: {ok, n, error}}."""
    V = X + "/_ver"; os.makedirs(V, exist_ok=True); subprocess.run(["chmod", "a+rwx", X, V], check=False)
    ped = T + "/_cuadros.json"
    json.dump([{"id": g["id"], "cuadros": [round(g["frames"] * p) for p in PUNTOS]} for g in G], open(ped, "w")); os.chmod(ped, 0o666)
    try: os.remove(V + "/cuadros.json")
    except OSError: pass
    try:
        r = subprocess.run(aislado(["node", T + "/still.mjs", T + "/public", V, ped]), cwd=T, capture_output=True, text=True, timeout=240 + 75 * len(G))
        if r.returncode: log("cuadros:", (r.stderr or r.stdout)[-300:])
    except subprocess.TimeoutExpired: log("sacar los cuadros tardó demasiado: se mira lo que llegó")
    finally: parar_aislados()
    try: return json.load(open(V + "/cuadros.json", encoding="utf8"))
    except Exception: return {}


def _base(B, t, AV, SH, fotos):
    """Lo que hay en pantalla en ese momento, para ver una capa transparente como la va a ver el espectador."""
    from PIL import Image
    try:
        if any(r["startMs"] <= t < r["endMs"] for r in AV): im = Image.open(B + "/refs/avatar.png")
        else:
            i = next((s["id"] for s in SH if s["startMs"] <= t < s["endMs"]), None)
            im = Image.open(fotos[i]) if i in fotos else None
        if im is not None: return im.convert("RGB").resize((960, 540))
    except Exception: pass
    return Image.new("RGB", (960, 540), (70, 70, 70))


def tira(B, X, g, AV, SH, fotos):
    """Los 3 cuadros de la pieza, uno debajo del otro. Las capas van ya puestas sobre lo que tapan."""
    from PIL import Image
    T_ = Image.new("RGB", (960, 540 * len(PUNTOS) + 8 * (len(PUNTOS) - 1)), (0, 0, 0)); hay = 0
    for k, p in enumerate(PUNTOS):
        f = X + "/_ver/%s_%d.png" % (g["id"], k)
        if not os.path.exists(f): continue
        try:
            im = Image.open(f).convert("RGBA").resize((960, 540))
            if g.get("tipo") == "overlay":
                base = _base(B, g["startMs"] + (g["endMs"] - g["startMs"]) * p, AV, SH, fotos).convert("RGBA"); base.alpha_composite(im); im = base
            else:
                fondo = Image.new("RGBA", (960, 540), (0, 0, 0, 255)); fondo.alpha_composite(im); im = fondo
            T_.paste(im.convert("RGB"), (0, k * 548)); hay += 1
        except Exception: pass
    return _jpg(T_, 80) if hay else None


OJO = ("You are the art director of this channel, reviewing frames of a piece BEFORE it is rendered. The image shows 3 frames of it, top to bottom (early, middle, late), exactly as the viewer will see them%s.\n\n"
       "THE CHANNEL'S VISUAL SYSTEM:\n%s\n\nWHAT THIS PIECE WAS MEANT TO BE:\n%s\n\n"
       "First write what is ACTUALLY on the frames. Then be a hard reviewer and list every concrete defect you can see: text that is unreadable, tiny, cut off, overlapping or outside the frame; a photo that is small, dark, stretched, blank or missing; a frame that is empty, flat or mostly one colour; nothing changing between the three frames; the presenter's face covered; a generic template look (gradient background, glass or rounded UI card, neon glow) instead of the channel's own system; anything that looks broken. Do not be polite: a piece you would not be proud to publish is not an 8.\n"
       'Return JSON only: {"veo":"...","problemas":["..."],"nota":1-10 (8 = publish as it is),"arreglo":"precise instructions for the programmer: what to change, where, how big"}')


def mirar(caja, ia, jpg, S_txt, idea, capa, log, i):
    try:
        j = ia(caja, [{"role": "user", "content": con_img(OJO % (", already placed on top of the real video frame it covers" if capa else "", S_txt, idea), [jpg])}], RES_OJO, 2500, True, True, 240, 2)
        nota = max(1, min(10, int(float(j.get("nota") or 0))))
        return {"nota": nota, "veo": str(j.get("veo") or "")[:400], "problemas": [str(x)[:300] for x in (j.get("problemas") or [])][:8], "arreglo": str(j.get("arreglo") or "")[:1500]}
    except Exception as e:
        log(i, "no se pudo mirar:", str(e)[:80]); return None


def sistema(B, X, T, GUION, HOJAS, fotos, caja, ia, log, SH, AV):
    """El sistema visual del canal: lo inventa DeepSeek mirando al presentador y las fotos, y lo deja programado en gen/canal.tsx."""
    guard = [B + "/refs/sistema", X]          # el del canal (si ya se inventó en otro video) o el de este video
    for d in guard:
        js, tsx = d + "/sistema.json", (d + "/gen/canal.tsx" if d == X else d + "/canal.tsx")
        try: S = json.load(open(js, encoding="utf8"))
        except Exception: S = None
        if S and os.path.exists(tsx):
            shutil.copyfile(tsx, T + "/src/gen/canal.tsx"); os.chmod(T + "/src/gen/canal.tsx", 0o666)
            if not verifica(T, T + "/src/gen/canal.tsx", 240): log("sistema del canal: reuso «%s»" % S.get("nombre")); return S
    def leer(n):
        try: return json.dumps(json.load(open(B + "/" + n, encoding="utf8")), ensure_ascii=False)[:5000]
        except Exception: return "(not available)"
    cara = foto_jpg(B + "/refs/avatar.png", 1024)
    ped = ("You are the art director of this YouTube channel and you are about to edit this whole video. Before any scene exists, define the channel's VISUAL SYSTEM: the look that makes a frame from any minute of any video of this channel recognisable as THIS channel and impossible to confuse with another one.\n\n"
           "Look at the images: the first one is the presenter in their place; the others are contact sheets of the real photos of this video. The system is born from this person and this place - their objects, materials, paper, handwriting, fabrics, tools, light - not from 'the graphics a YouTube video usually carries'. Ask: if this person made the graphics by hand with what is in that room, what would they be? Generic motion-graphics looks are forbidden: gradient backgrounds, glass or rounded UI cards, neon glows, a default sans title on a dark box, stock infographic icons.\n\n"
           "THE CHANNEL:\n%s\n\nTHE WORLD OF THE CHANNEL:\n%s\n\nTRANSCRIPT OF THIS VIDEO:\n%s\n\n"
           'Return JSON only: {"nombre":"a short name for the system","concepto":"2-3 sentences: the one idea everything follows","paleta":[{"hex":"#...","uso":"..."}],'
           '"tipografia":{"titulos":"a Google Font name","texto":"a Google Font name","como":"sizes, case, how text sits on its material"},"materiales":"the physical surfaces and objects graphics are made of, and how photos are shown",'
           '"movimiento":"how things enter, move and leave; the pace","recurrentes":[{"nombre":"PascalCase","que_es":"what it shows and what it looks like","props":"its inputs"}],"nunca":["..."]}\n'
           "`recurrentes` are the 4 to 7 components that will come back through the whole video and hold it together: how the video announces what is coming, how each part opens, how the viewer knows where they are, how a name, a date or a number is labelled, how a photo is shown as an object. Decide your own from this content.") % (leer("refs/canal.json"), leer("mundo.json"), GUION[:14000])
    try: S = ia(caja, [{"role": "user", "content": con_img(ped, [cara] + HOJAS[:3])}], RES_DIRECTOR, 6000, True, True, 600, 2)
    except Exception as e: log("no pude definir el sistema del canal:", e); return None
    if not isinstance(S, dict) or not S.get("recurrentes"): log("el sistema del canal vino vacío"); return None
    log("sistema del canal: «%s» · %s" % (S.get("nombre"), ", ".join(str(r.get("nombre")) for r in S["recurrentes"] if isinstance(r, dict))))
    muestra = sorted(fotos)[:: max(1, len(fotos) // 6)][:6]
    msgs = [{"role": "user", "content": ("Program the shared module of this channel's visual system: src/gen/canal.tsx. Every scene of every video will import from it, so this file IS the look of the channel. Make it beautiful and unmistakable.\n\nTHE SYSTEM (your own design):\n%s\n\n"
            "It must export:\n- `K`: the tokens (colours, the loaded font families, sizes, and any easing/spring helpers you want to reuse).\n- each recurring component as a NAMED export with typed props. Each one animates from its own frame 0 using useCurrentFrame(), so a scene can place it with <Sequence from={...}>. Components that go on top of the video must have no background of their own. Text must be large: nothing under 40px, titles 80px or more.\n"
            "- `export default function Scene()`: a 240-frame specimen that shows every component in action, one after another, with these real photos: %s. The art director will look at frames of it.\n\n%s\n\nReply with the complete file in one ```tsx block.") % (json.dumps(S, ensure_ascii=False, indent=1), ", ".join("fotos/%s.jpg" % i for i in muestra), TEC)}]
    if not programar(T, "canal", 240, msgs, caja, ia, log, 3): log("no pude programar el sistema del canal"); return None
    g = {"id": "canal", "tipo": "full", "frames": 240, "startMs": 0, "endMs": 8000}
    for vuelta in range(2):                 # mira su propio sistema y lo corrige una vez
        montar(B, T, [g], fotos, {}); c = sacar_cuadros(T, X, [g], log); jpg = tira(B, X, g, AV, SH, fotos)
        if not jpg:
            if vuelta: break
            v = {"nota": 1, "problemas": ["it does not render: " + str((c.get("canal") or {}).get("error") or c.get("_error") or "no frames")[:500]], "arreglo": "fix the error"}
        else: v = mirar(caja, ia, jpg, json.dumps(S, ensure_ascii=False), "The specimen of the channel's system: every recurring component, one after another.", False, log, "canal")
        if not v: break
        log("sistema del canal: nota %d · %s" % (v["nota"], "; ".join(v["problemas"])[:220]))
        S["nota"] = v["nota"]
        if v["nota"] >= 8 or vuelta: break
        cod = open(T + "/src/gen/canal.tsx", encoding="utf8").read()
        m2 = msgs[:1] + [{"role": "assistant", "content": "```tsx\n%s\n```" % cod},
                         {"role": "user", "content": con_img("I rendered the specimen and looked at it (3 frames, top to bottom). Problems:\n- %s\n\nWhat to do: %s\n\nKeep every export name and every prop exactly as they are. Reply with the complete corrected file in one ```tsx block." % ("\n- ".join(v["problemas"]), v["arreglo"]), [jpg] if jpg else [])}]
        shutil.copyfile(T + "/src/gen/canal.tsx", T + "/src/gen/canal.tsx.bien")
        if not programar(T, "canal", 240, m2, caja, ia, log, 2): shutil.copyfile(T + "/src/gen/canal.tsx.bien", T + "/src/gen/canal.tsx"); break
    try: os.remove(T + "/src/gen/canal.tsx.bien")
    except OSError: pass
    os.makedirs(X + "/gen", exist_ok=True); shutil.copyfile(T + "/src/gen/canal.tsx", X + "/gen/canal.tsx")
    json.dump(S, open(X + "/sistema.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
    return S


def componer(B, X, T, W, AV, FT, fotos, clips, cara, caja, total, nmax, ia, log):
    GUION = transcripcion(W); pres = "the presenter is framed so the face is at x %d-%d%%, y 2-42%% of the frame, with the body below it; the rest of the frame is free" % (max(0, round((cara - .13) * 100)), min(100, round((cara + .13) * 100)))
    desc = lambda i: re.sub(r"\s+", " ", str(FT.get(i, {}).get("_d") or ""))[:150]
    FOTOS = "\n".join("fotos/%s.jpg - %s" % (i, desc(i)) for i in sorted(fotos))
    CLIPS = "\n".join("clips/%s.mp4 - %ds - %s" % (i, d, desc(i)) for i, d in sorted(clips.items())) or "(none in this video)"
    AVR = ", ".join("%d-%d" % (r["startMs"], r["endMs"]) for r in AV) or "(none)"
    LIBRE = ", ".join("%d-%d" % h for h in huecos(AV, total))
    try: SH = json.load(open(B + "/shots_timed.json", encoding="utf8")) or []
    except Exception: SH = []
    try: FIRMA = [m for m in (json.load(open(X + "/manifest.json", encoding="utf8")) or []) if str(m.get("mp4", "")).startswith("extrema/es")]
    except Exception: FIRMA = []
    OCUP = ", ".join("%d-%d" % (m["startMs"], m["endMs"]) for m in FIRMA) or "(none)"
    n = min(nmax, MAX_ESCENAS)
    HOJAS = hojas(fotos)

    # 1) el sistema del canal
    S = sistema(B, X, T, GUION, HOJAS, fotos, caja, ia, log, SH, AV)
    if S:
        S_txt = json.dumps({k: v for k, v in S.items() if k != "nota"}, ensure_ascii=False, indent=1)
        CANAL = "\n\nTHE CHANNEL'S VISUAL SYSTEM (your own design; every piece follows it):\n%s\n\nIt is already programmed in src/gen/canal.tsx. Import what you need with `import {K, ...} from './canal'` and build with it: its tokens, fonts and recurring components. This is the file:\n```tsx\n%s\n```" % (S_txt, open(T + "/src/gen/canal.tsx", encoding="utf8").read())
    else: S_txt, CANAL = "(none: make every piece belong to the same family)", ""

    # 2) el plan del video ENTERO, mirando las fotos
    ped = ("You are the director and editor of this YouTube video. Below is the whole video: transcript with times in ms, the time ranges where the presenter is on camera, the time ranges with b-roll, the real photos (you can SEE them in the contact sheets, each with its id) and the stock clips.\n\n"
           "THE CHANNEL'S VISUAL SYSTEM (your own design):\n%s\n\n"
           "Plan the edit of the WHOLE video, from the first minute to the last: up to %d pieces. A viewer who lands on any minute must see this channel's hand. Two layers of work:\n"
           "1. STRUCTURE, with the recurring components of the system: how the video announces what is coming, how each part opens, how the viewer knows where they are. If the video is a list, every item gets its opening and the viewer always knows which one they are on.\n"
           "2. SIGNATURE MOMENTS: where the narration says something that deserves a scene built WITH the real photos and clips - several layers, depth, photos moving at different distances, things happening on top of and inside the images, each thing landing on the exact word that names it. Each one different from the others and born from what is said there. Choose the photos by LOOKING at them: the right face, the right place, the right object.\n"
           "Do not leave any stretch longer than about 90 seconds without a piece.\n\n"
           "Two kinds: 'full' = a complete full-screen scene (only inside the b-roll ranges, 4 to 30 s); 'overlay' = graphics on a transparent background that appear ON TOP of what is already on screen, the presenter or the b-roll (3 to 12 s). Use both.\n\n"
           "TRANSCRIPT:\n%s\n\nPRESENTER ON CAMERA (ms): %s\nWhen on camera: %s.\n\nB-ROLL RANGES (ms): %s\n\nALREADY TAKEN by finished scenes, put nothing there (ms): %s\n\nPHOTOS:\n%s\n\nSTOCK VIDEO CLIPS:\n%s\n\n"
           'Return JSON only: {"escenas":[{"tipo":"full or overlay","startMs":0,"endMs":0,"fotos":["p001"],"idea":"what the piece is and how it moves, concretely, moment by moment, naming the recurring components it uses and what each photo does"}]}') % (S_txt, n, GUION, AVR, pres, LIBRE, OCUP, FOTOS, CLIPS)
    try: j = ia(caja, [{"role": "user", "content": con_img(ped, HOJAS)}], RES_DIRECTOR, 30000, True, True, 600, 2)
    except Exception as e: log("el director no respondió, queda el b-roll normal:", e); return []
    crudas = [x for x in (j.get("escenas") or []) if isinstance(x, dict)]
    E = limpiar_escenas([x for x in crudas if not any(int(x.get('startMs') or 0) < f['endMs'] and int(x.get('endMs') or 0) > f['startMs'] for f in FIRMA)], AV, total, log)
    for e in E:
        o = next((x for x in crudas if str(x.get("idea")) == e["idea"]), {})
        e["fotos"] = [re.sub(r"^fotos/|\.jpg$", "", str(i)) for i in (o.get("fotos") or []) if re.sub(r"^fotos/|\.jpg$", "", str(i)) in fotos][:6]
    log("director: %d piezas (%d encima) para %d min" % (len(E), sum(e["tipo"] == "overlay" for e in E), total // 60000))

    # 3) programa cada pieza viendo SUS fotos
    PED = {}
    def crea(k, e):
        i = "xm%02d" % (k + 1); a, b = e["startMs"], e["endMs"]; fr = round((b - a) * FPS / 1000)
        pal = " ".join("%s@%d" % (w["text"].strip(), max(0, round((w["startMs"] - a) * FPS / 1000))) for w in W if a - 50 <= w["startMs"] < b)
        sobre = next(("the presenter on camera: " + pres for r in AV if a < r["endMs"] and b > r["startMs"]), "a b-roll photo or clip of the video")
        extra = "" if e["tipo"] != "overlay" else "\n\nThis is an OVERLAY: the root must have NO background, everything outside your graphics stays fully transparent, because it plays on top of %s. Do not cover the presenter's face. Keep it to a part of the frame: it must leave most of the picture visible." % sobre
        vistas = [foto_jpg(fotos[x]) for x in e.get("fotos") or []]
        txt = ("Build this piece of my YouTube video. Make it look incredible.\n\nThe whole video, for context:\n%s\n\nTHE PIECE (your own idea):\n%s\n\nIt lasts %d frames (30 fps). Narration during the piece, word@frame (land each thing on its word):\n%s\n\n"
               "%sThe photos of the video:\n%s\n\nStock video clips of the video:\n%s\n\nBuild it with these real images and clips as the main material (layers, depth, parallax), not with drawn shapes that imitate them. The images stay large, bright and clearly visible. Text is large: nothing under 40px.%s\n\n%s\n\nReply with the complete file in one ```tsx block.") % (
               GUION, e["idea"], fr, pal, ("Attached, in this order, are the photos you chose for it: %s. Look at where the subject is in each one before placing or cropping it.\n\n" % ", ".join("fotos/%s.jpg" % x for x in e["fotos"])) if vistas else "", FOTOS, CLIPS, CANAL, TEC + extra)
        PED[i] = txt
        if not programar(T, i, fr, [{"role": "user", "content": con_img(txt, vistas)}], caja, ia, log): return None
        log(i, e["tipo"], "programada:", e["idea"][:90])
        return {"id": i, "tipo": e["tipo"], "startMs": a, "endMs": b, "frames": fr, "idea": e["idea"], "fotos": e.get("fotos") or []}

    with cf.ThreadPoolExecutor(6) as ex: G = [r for r in ex.map(lambda x: crea(*x), enumerate(E)) if r]
    if not G: return []

    # 4) MIRA lo que hizo y lo corrige: una vuelta de arreglo y un control final. Lo que no llega a 6 no entra al video.
    def ronda(lote):
        montar(B, T, G, fotos, clips); c = sacar_cuadros(T, X, lote, log); tiras = {}
        def una(g):
            jpg = tira(B, X, g, AV, SH, fotos); tiras[g["id"]] = jpg
            if not jpg: g["nota"] = 1; g["ojo"] = {"nota": 1, "problemas": ["it does not render: " + str((c.get(g["id"]) or {}).get("error") or c.get("_error") or "no frames")[:500]], "arreglo": "fix the error"}; return
            v = mirar(caja, ia, jpg, S_txt, g["idea"], g["tipo"] == "overlay", log, g["id"])
            if v: g["nota"] = v["nota"]; g["ojo"] = v
            else: g.setdefault("nota", 7)        # no se pudo mirar (tope o red): no se la castiga
        with cf.ThreadPoolExecutor(6) as ex: list(ex.map(una, lote))
        return tiras
    tiras = ronda(G)
    log("primera mirada: " + " ".join("%s=%d" % (g["id"], g["nota"]) for g in G))
    flojas = [g for g in G if g["nota"] < 8 and g.get("ojo")]
    def arregla(g):
        i = g["id"]; f = T + "/src/gen/%s.tsx" % i; cod = open(f, encoding="utf8").read(); v = g["ojo"]; jpg = tiras.get(i)
        m = [{"role": "user", "content": PED[i]}, {"role": "assistant", "content": "```tsx\n%s\n```" % cod},
             {"role": "user", "content": con_img("I rendered it and looked at it (3 frames, top to bottom%s). What is on screen: %s\nProblems:\n- %s\n\nWhat to do: %s\n\nReply with the complete corrected file in one ```tsx block." % (
                 ", already on top of the video frame it covers" if g["tipo"] == "overlay" else "", v.get("veo", ""), "\n- ".join(v["problemas"]) or "it is not good enough to publish", v["arreglo"]), [jpg] if jpg else [])}]
        shutil.copyfile(f, f + ".antes")
        if programar(T, i, g["frames"], m, caja, ia, log): g["antes"] = g["nota"]; return g
        shutil.copyfile(f + ".antes", f); return None
    if flojas:
        with cf.ThreadPoolExecutor(6) as ex: rehechas = [g for g in ex.map(arregla, flojas) if g]
        if rehechas:
            ronda(rehechas)
            for g in rehechas:
                f = T + "/src/gen/%s.tsx" % g["id"]
                if g["nota"] < g["antes"]: shutil.copyfile(f + ".antes", f); g["nota"] = g["antes"]      # el arreglo la empeoró: vuelve la anterior
            log("segunda mirada: " + " ".join("%s=%d(antes %d)" % (g["id"], g["nota"], g["antes"]) for g in rehechas))
    for f in glob.glob(T + "/src/gen/*.antes"): os.remove(f)
    fuera = [g for g in G if g["nota"] < 6]
    for g in fuera: log(g["id"], "queda afuera (nota %d): %s" % (g["nota"], "; ".join((g.get("ojo") or {}).get("problemas") or [])[:200]))
    G = [g for g in G if g["nota"] >= 6]
    res = [{k: v for k, v in g.items() if k not in ("ojo", "antes")} for g in G]
    os.makedirs(X + "/gen", exist_ok=True)
    for g in res: shutil.copyfile(T + "/src/gen/%s.tsx" % g["id"], X + "/gen/%s.tsx" % g["id"])
    json.dump(res, open(X + "/director.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)     # otra máquina las reusa: no se paga dos veces
    shutil.rmtree(X + "/_ver", ignore_errors=True)
    return res


def capa_ok(f, frames, caja_cara):
    """La capa tiene que ser transparente de verdad y no tapar la cara."""
    from PIL import Image
    Wd, Hd = 240, 135
    for p in (.15, .35, .55, .75, .95):
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.2f" % (frames / FPS * p), "-i", f, "-frames:v", "1", "-vf", "scale=%d:%d,format=rgba" % (Wd, Hd), "-f", "rawvideo", "-"], capture_output=True, timeout=120)
        if len(r.stdout) != Wd * Hd * 4: return "no se pudo leer"
        a = Image.frombytes("RGBA", (Wd, Hd), r.stdout).getchannel("A")
        tot = sum(1 for v in a.getdata() if v > 40) / (Wd * Hd)
        if tot > .6: return "tapa el %d%% del cuadro" % (tot * 100)
        if caja_cara:
            x0, y0, x1, y1 = caja_cara; cr = a.crop((int(x0 * Wd), int(y0 * Hd), int(x1 * Wd), int(y1 * Hd))); datos = list(cr.getdata())
            cara = sum(1 for v in datos if v > 80) / max(1, len(datos))
            if cara > .15: return "tapa la cara (%d%%)" % (cara * 100)
    return ""


def renderizar(B, X, T, G, fotos, clips, cara, AV, log):
    pub = T + "/public"; montar(B, T, G, fotos, clips)
    ext = lambda g: "mov" if g["tipo"] == "overlay" else "mp4"
    json.dump([{"id": g["id"], "startMs": g["startMs"], "endMs": g["endMs"], "texto": g["idea"][:120], "arch": "extrema/%s.%s" % (g["id"], ext(g))} for g in G], open(X + "/momentos.json", "w", encoding="utf8"), ensure_ascii=False)
    subprocess.run(["chmod", "a+rwx", X], check=False)
    t0 = time.time()
    def _local(ids):       # el camino de siempre: en esta máquina, una atrás de otra, como el usuario sin claves
        try:
            r = subprocess.run(aislado(["node", T + "/render.mjs", pub, X, ",".join(ids)]), cwd=T, capture_output=True, text=True, timeout=4200)
            print(r.stdout[-1500:], r.stderr[-800:], flush=True)
        except subprocess.TimeoutExpired: log("el render tardó demasiado: van las piezas que llegaron")
        finally: parar_aislados()
    import granja
    granja.render(T, pub, X, [g["id"] for g in G], log, _local)      # una máquina de GitHub por pieza; lo que no vuelva, acá
    try: res = json.load(open(X + "/render.json", encoding="utf8"))
    except Exception: res = {}
    man, capas = [], []
    caja_cara = (max(0, cara - .13), .02, min(1, cara + .13), .42)
    for g in G:
        i, f = g["id"], X + "/%s.%s" % (g["id"], ext(g))
        if not (res.get(i) or {}).get("ok") or not os.path.exists(f): log(i, "no se renderizó: queda el b-roll", str((res.get(i) or {}).get("error") or "")[:160]); continue
        if abs(duracion(f) * FPS - g["frames"]) > 6: log(i, "duración rara: queda el b-roll"); continue
        if g["tipo"] == "overlay":
            sobre = any(g["startMs"] < r["endMs"] and g["endMs"] > r["startMs"] for r in AV)
            mal = capa_ok(f, g["frames"], caja_cara if sobre else None)
            if mal: log(i, "capa descartada:", mal); continue
            capas.append({"mov": "extrema/%s.mov" % i, "startMs": g["startMs"], "endMs": g["endMs"]})
        else: man.append({"mp4": "extrema/%s.mp4" % i, "startMs": g["startMs"], "endMs": g["endMs"], "texto": g["idea"][:120]})
    try: firma = [m for m in (json.load(open(X + "/manifest.json", encoding="utf8")) or []) if str(m.get("mp4", "")).startswith("extrema/es")]      # las escenas firma (escenas.py) se conservan
    except Exception: firma = []
    libre = lambda m: not any(m["startMs"] < f["endMs"] and m["endMs"] > f["startMs"] for f in firma)
    man = sorted(firma + [m for m in man if libre(m)], key=lambda m: m["startMs"]); capas = [c for c in capas if libre(c)]
    for nom, dat in (("manifest.json", man), ("capas.json", capas)):
        json.dump(dat, open(X + "/" + nom + ".tmp", "w", encoding="utf8"), ensure_ascii=False, indent=1); os.replace(X + "/" + nom + ".tmp", X + "/" + nom)      # render.py puede estar leyéndolo
    shutil.rmtree(pub, ignore_errors=True)
    log("%d escenas y %d capas listas en %.0f s" % (len(man) - len(firma), len(capas), time.time() - t0))


def correr(B, X, W, AV, FT, fotos, PKG, caja, nmax, ia, log, gasto):
    if not os.environ.get("GITHUB_ACTIONS"): log("el código generado sólo corre en GitHub Actions"); return
    if not usuario(): log("sin usuario aislado no se ejecuta código generado: queda el b-roll normal"); return
    T = os.environ.get("EXTREMA_TRABAJO") or "/tmp/extrema_pkg"
    if not preparar(T, PKG, log): return
    total = W[-1]["endMs"]
    try: cara = float(json.load(open(B + "/refs/canal.json", encoding="utf8")).get("cara_cx") or .5)
    except Exception: cara = .5
    clips = {}
    d = B + "/clips"
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        i, e = os.path.splitext(f)
        if e.lower() == ".mp4" and not i.startswith("_") and len(clips) < 60:
            s = duracion(d + "/" + f)
            if s > 1: clips[i] = round(s)
    try: G = json.load(open(X + "/director.json", encoding="utf8"))
    except Exception: G = None
    if G and all(os.path.exists(X + "/gen/%s.tsx" % g["id"]) for g in G):
        for i in [g["id"] for g in G] + (["canal"] if os.path.exists(X + "/gen/canal.tsx") else []): shutil.copyfile(X + "/gen/%s.tsx" % i, T + "/src/gen/%s.tsx" % i)
        log("reuso las %d piezas ya programadas" % len(G))
    else:
        G = componer(B, X, T, W, AV, FT, fotos, clips, cara, caja, total, nmax, ia, log)
        if caja.gastado > 0: gasto(B, "edicion_extrema", caja.gastado, llamadas=caja.n)
        log("programadas %d piezas · US$%.4f" % (len(G), caja.gastado))
    if G: renderizar(B, X, T, G, fotos, clips, cara, AV, log)
