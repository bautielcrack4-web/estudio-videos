# REPORTE — fn04ds

**Video:** "Why I Told My Own Mother Never to Buy a Prepaid Funeral — 40 Years in the Business"
**Idioma:** inglés · **Duración:** 1479,0 s (24 min 39 s) · 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192k estéreo
**Entregado:** `final.mp4` (728,7 MB, también en `final.url`) · `meta.json` · `gates/final_auto.txt` + `gates/final_pedido.txt`
**Voz:** Fish `ernie_en` (master 1478,997 s) · ASR Groq por palabra (3.779 palabras)

## Qué se hizo (punta a punta)

1. **Guion** con gancho de número + objeto, prueba interactiva al min 4, problema → anécdota con
   fecha/nombre/lugar → por qué pasa → cambio concreto con precio (FTC Funeral Rule, NFDA 2023,
   Texas Department of Banking) → chequeo de esta noche, like/suscribir antes del último punto, cierre
   con pregunta de una palabra ("folder") y enganche a fn02 (velorio de toda la noche). Sin palabras
   prohibidas, sin consejo médico, sin nada que marque el contenido como IA.
2. **Voz** con `fish_factory.py --keep-tags` → `voz/master.wav` (tags de emoción usados con mesura).
3. **Transcripción Groq** (`captions.json`, tiempo por palabra) y de ahí `shots_timed.json`:
   443 planos, cortes cada ~3,3 s, de 0 a 1.478.997 ms sin huecos. Cada cambio cae en el `startMs` de
   la palabra que lo motiva.
4. **Fotos** pedidas por la cola de avatarity con JSON completo (`type/moment/subject/action/props/
   setting/light/camera/color/avoid`), linter de `encolar.mjs` en OK, 6 de prueba primero y después el
   lote completo; todas revisadas en hojas de contacto con Read. Personas con el presentador con `refs`
   del avatar. **192 fotos en el corte final, todas de la cola.**
5. **Avatar InfiniteTalk**: **1 sola llamada** (`avatar/it_llamada.json`), US$ 0,25.
   112 ventanas (A0…A111), 433 s = 29 % del video, 3-6 s cada ~11-13 s, nunca más de 20 s sin avatar.
   Primer cuadro = **`D:/rtmp/funerario/refs/ernesto_av.png`** directo (foto de ChatGPT web, la que pidió
   el creador), puesto en `avatar_ranges.json` antes de correr `avatar_it.py`; el resto de las ventanas
   sale de `avatar/frames/a1.jpg`, la misma escena. Desfase del reel de RunPod medido y corregido clip
   por clip (`avatar/it_sync.json`, máximo 305 ms).
6. **SFX** Mixkit puntuales (`sfx/`, `cues.json`: 5 cues, gain 0,035-0,055), **sin música** (ver abajo).
7. **Armado** con `render.py` **en la nube** (el creador cortó el render local el 8-nov):
   28 tandas en GitHub, **7,8 min**, 444 segmentos, 0 huecos negros, fundidos 0,6 s avatar↔foto y
   0,3 s foto↔foto, Ken Burns al azar con semilla 20261106, recorte del 9,1 % que saca la estrellita.
   `plan.json` lo escribió render.py solo. `assemble.py` ya no hace falta (la nube une y pone voz+SFX).
   El `final.mp4` bajado es el mismo binario del release `est-fn04ds`.

## Validación

`validar.py --etapa final --min 25` → **RESULTADO: OK**, ningún ✗:
3.779 palabras · 192 fotos de la cola de avatarity · 0 huecos sin imagen · arranca con el avatar hablando
desde el segundo 0 · avatar 433 s (29 %) · nunca más de 20 s sin avatar · todos los segmentos de avatar
son clips reales · desfase máx 305 ms · 0 huecos negros ≥ 0,5 s · 1920x1080 · 30 fps · 1479,00 s =
voz 1479,00 s · `meta.json` con título y descripción larga · `REPORTE.md` presente.

Revisión visual: 49 cuadros cada 30 s (`qc/f_*.jpg`, hojas `qc/nf_a.jpg` … `nf_d.jpg`), las cuatro
miradas con Read, más dos muestras del archivo bajado (`qc/chk_b9.jpg`). Avatar coherente en todas las
ventanas, b-roll del tema en todo el recorrido, sin fechas impresas, sin texto inventado, sin manos
rotas, sin look de publicidad. Los cuadros "fantasma" (f_009, f_031, f_036…) son fundidos de 0,6 s
capturados a mitad de disolvencia, no un error.

## Costos

| cosa | US$ |
|---|---|
| Avatar InfiniteTalk (1 llamada) | 0,25 |
| Fotos por la cola de avatarity (incluye el desvío gpt-image-2 low) | cuota compartida, 0 |
| Fish, Groq, Mixkit | gratis |
| Render + armado | nube compartida (GitHub Actions), 0 |

## Problemas y cómo se resolvieron

- **Bloque b9 (18 fotos del tramo final): cuatro pedidos, tres fallidos.**
  1) El primer lote llegó con **infografías educativas ajenas** (fotosíntesis, ciclo del agua, machine
     learning…) pese a que el prompt guardado en la cola era correcto → apartadas a `qc/bad/`.
  2) Segundo pedido rechazado por la cola: `prompt Expected string`.
  3) Tercer pedido (Nano Banana, prio 0): **`503 MAINTENANCE`** en los 18 trabajos durante más de una
     hora. Con la regla del KIT ("si falla 3 veces, poné un reemplazo") los 43 planos b9 se cubrieron
     con 18 fotos existentes y **así se entregó la primera versión**.
  4) **Resuelto:** la cuarta copia (prio 1, desvío `fotos_gpt.mjs`) entregó las 18 fotos reales
     (`fotos/b9*5.jpg|png`, revisadas en `qc/cand_b9final.jpg` y `cand_b9final2.jpg`). Con el render
     ya en la nube (8 min) se repusieron los 43 planos (`shots_timed.json`, backup del estado anterior
     en `shots_timed_b9fallback.json`), se re-renderizó y **el `final.mp4` entregado ya trae las fotos
     nuevas**. Verificado en `qc/f_045.jpg`, `qc/f_047.jpg`, `qc/f_048.jpg` y `qc/chk_b9.jpg`.
- **Primer intento de render en la nube falló**: corrí `render.py .` con ruta relativa y `nube.py`
  arma el tag con el nombre de la carpeta → `est--` → `gh: release not found`. Se relanzó con la ruta
  absoluta (`render.py D:/rtmp/fn04ds`) y anduvo. Sin consecuencias.
- **Hueco de 0,28 s en 736,929→737,209**: la ventana de avatar A55 se montaba sobre el plano `b5g` y
  render.py descarta los fragmentos de foto menores a 500 ms. Se alinearon los bordes
  (`b5g` fin = `b5h` inicio = 736929). Verificado con `check_plan.py`: 444 segmentos, sin huecos,
  44.370 cuadros = 1479,00 s.
- **`fn04ds__t03`**: la API devolvió `400 CONTENT_POLICY_VIOLATION` en una foto de prueba; no se
  volvió a pedir (era sólo test, el plano se cubrió con otra foto).
- **`hoja.py`** se colgaba con presión de memoria (WinError 1455): las hojas de contacto se armaron con
  PIL (`sheet_pil.py`).
- **Sin música**: el KIT no trae música de fondo; sólo SFX puntuales. Queda anotado como pedido.
- **`gates/correcciones.txt`**: no existió en ningún punto de control; no hubo correcciones del revisor
  que aplicar.

## Estado

- `final.mp4` **entregado y validado (OK)**: 728,7 MB · 1478,9977 s · 1920x1080 · 30 fps · H.264 · AAC
  192k estéreo. Link permanente en `final.url` (release `est-fn04ds`).
- `plan.json` escrito por render.py: 444 segmentos, cero huecos.
- Puntos de control completos en `gates/`: `guion`, `fotos`, `render`, `final` — cada uno con `_auto`
  y `_pedido`, más `correcciones_hechas.txt`.
- Nada pendiente.
