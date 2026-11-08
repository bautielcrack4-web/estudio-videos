# KIT DE HERRAMIENTAS — videos con avatar (leer ANTES de empezar)

Herramientas del Estudio: `{APP}/tools/`. Trabajá SOLO en tu carpeta de video (la del brief). No toques nada fuera de ella.
Las claves ya están configuradas: las herramientas las leen solas. **Nunca las busques, leas ni imprimas.**

## 🚀 CAMINO RECTO (hacelo de primera: cada vuelta extra atrasa la entrega)
1. **Guion** → `guion.txt` (largo del brief). Validá `--etapa guion` UNA vez.
2. **Voz** (§1) en segundo plano y, **en paralelo**, escribí todos los prompts de fotos (JSON completos, §4) y pedí la PRIMERA tanda (el Batch tarda: pedila temprano).
3. **Tiempos** (§2) → `captions.json`. Con eso escribí de UNA `shots_timed.json` (cortes cada 3-4 s, sin huecos) y `avatar_ranges.json` (§3).
4. **Fotos**: 6 de prueba → hoja → mirala → resto del lote en 1 o 2 pedidos grandes (§4). Mientras llegan, seguí.
5. **Avatar**: con el plan cerrado, `avatar_it.py` en segundo plano (1 sola llamada, §3).
6. **Render de prueba** (`render.py --limit 10`) → hoja → mirala. Después `render.py` completo + `assemble.py`.
7. **Final**: validá `--etapa final`, `meta.json`, `REPORTE.md`. Listo: el usuario lo descarga desde el panel.

Reglas anti-vueltas:
- **Esperar = SÓLO `python {APP}/tools/esperar.py`** (hasta 9 min de una: `--log render.log`, `--cuenta "fotos/*.png" 120`, `--existe final.mp4`; llamala con timeout 600000). **Prohibido `sleep` en bucle** y mirar con `ls`/`tail` cada minuto.
- Todo lo que tarde > 1 min (voz, fotos, avatar, render, assemble) va en segundo plano con log (`nohup … > x.log 2>&1 &`) y lo esperás con `esperar.py` mientras hacés otra cosa.
- Antes de escribir un script propio, fijate si ya hay herramienta (voz, tiempos, fotos, avatar_it, render, assemble, hoja, esperar, validar). No reinventes.
- Leé cada archivo UNA vez. El validador: arreglá sólo los **✗**; los **!** son avisos (mejoralos si es rápido o anotalos en REPORTE.md y SEGUÍ). Máximo 2 corridas por etapa.

## ⛔ Reglas duras
- **Nunca imprimas, copies ni leas claves** (el guardián lo bloquea).
- No usar: git push, YouTube, ni APIs directo. RunPod SÓLO por `tools/avatar_it.py`; imágenes SÓLO por `tools/fotos.py`.
- **gpt-image SIEMPRE quality low + Batch** (lo hace `fotos.py`; no hay otra forma).
- Nunca marcar el contenido como IA dentro del video ni en la descripción. Sin claims médicos ni legales.
- **Scripts y JSON largos: escribilos con Write a un archivo y después corré `python archivo.py`.** Nunca en heredoc ni `python -c '…'` (los apóstrofos rompen las comillas).
- **Matar un proceso:** `kill <pid>` o `taskkill //F //PID <pid>` (el pid sale de `echo $!` al lanzarlo).
- **Texto en ffmpeg prohibido** (`drawtext` puede no tener fuentes). Hojas de contacto: `python {APP}/tools/hoja.py <salida.jpg> <fotos o videos…>` (hasta 12).
- **Nada frena el video.** Si una herramienta falla 3 veces, poné un reemplazo (otra foto, el cuadro del presentador en vez de avatar), anotalo en REPORTE.md y seguí.

## 1. Voz — el clon de la voz del canal (Fish)
```
python {APP}/tools/voz.py <carpeta> > <carpeta>/voz/voz.log 2>&1 &
```
- Lee `guion.txt` + la muestra `refs/voz.wav`. Salida: `voz/master.wav`. Si falla, relanzala: rehace sólo los bloques que faltan.
- Tags de emoción que suman (2-4 en todo el guion): `[whispering]`, `[excited]`, `[emphatically]`, `(laughs)`. Nada de más.

## 2. Tiempos por palabra
```
python {APP}/tools/tiempos.py <carpeta> <es|en|pt>
```
- Salida `captions.json`: una entrada por PALABRA `{text,startMs,endMs}`. **Clavá cada imagen en el segundo exacto** en que se dice la palabra.

## 3. Avatar — InfiniteTalk, UNA sola llamada por video
```
python {APP}/tools/avatar_it.py <carpeta> > <carpeta>/avatar/it.log 2>&1 &
```
- Lee `avatar_ranges.json` (TODAS las ventanas), hace **1 solo /run** con la foto `refs/avatar.png` y corta cada ventana en su `file` (`avatar/A0.mp4`, `A1.mp4`…), midiendo y corrigiendo el desfase. Tarda 10-60 min: seguí con todo lo demás.
- ⛔ **El plan de ventanas tiene que estar CERRADO antes.** Hay UNA llamada por video; la herramienta se niega a una 2ª. Si después movés ventanas, las nuevas van con FOTO. Un FAILED no cobra: ahí sí podés repetirla.
- Total de ventanas ≤ 590 s. Cada ventana ≥ 3 s.
- **Ritmo:** el avatar cuesta lo MISMO (1 llamada) dure lo que dure, y cada foto cuesta: **~50 % del video con avatar** (máx. 560 s en total),
  en ventanas CORTAS de **3-6 s** que entran y salen, con 1-2 fotos entre ventana y ventana; **nunca más de 15 s seguidos sin avatar**.
  ⛔ Que siga siendo DINÁMICO: nunca más de 6 s de avatar a pantalla completa. Para tramos más largos (7-12 s) usá **pantalla
  partida**: en la ventana agregá `"foto":"<id>","lado":"izq"` (o `"der"`, alternando) → avatar de un lado y la foto de lo que
  dice del otro. Mezclá: avatar entero, foto, partida, foto, avatar entero… Las ventanas van en las FRASES IMPORTANTES (la promesa, un número, un "pero", la conclusión de cada parte).
- ⛔ **Lo PRIMERO que se ve es SIEMPRE el avatar hablando desde el segundo 0** (primera ventana `startMs: 0`, ≤ 10 s; en los primeros 30 s las demás ≤ 6 s). El validador lo controla.
- Cada ventana: `{"file":"avatar/A0.mp4","frame":"refs/avatar.png","startMs":0,"endMs":7400}` (el `frame` se usa como foto fija mientras el clip no llega).

## 4. Fotos del b-roll — gpt-image low + Batch, CADA FOTO CUENTA UN MOMENTO
```
python {APP}/tools/fotos.py <carpeta> <carpeta>/pedidos_01.json > <carpeta>/fotos/fotos_01.log 2>&1 &
```
- `pedidos = [{"id":"b01_gancho","cara":true,"prompt":{…JSON…}}]`. `cara: true` = sale el presentador (se le agrega su descripción física; NUNCA va una foto de referencia); `false` = escena sin él.
  El presentador ya aparece en el avatar la mitad del video: usá `cara: true` sólo en el gancho y en pocas fotos más (≤ 15 %).
  Lo demás: manos, objetos, lugares, otras personas.
- Si el usuario eligió **"Las hago yo"** (Configuración), fotos.py NO gasta: escribe `fotos/PROMPTS.md` y espera a que él las suba desde el panel. Corrélo igual en segundo plano, seguí con lo demás y esperá con `esperar.py --cuenta "fotos/*.*" N`. No le pidas que use otro programa ni le expliques: el panel ya le muestra la lista.
- El Batch tarda (de minutos a un par de horas): **pedí temprano y en pocos pedidos grandes**, no de a una. Mientras tanto, seguí.
- La herramienta tiene una **COMPUERTA**: si falta algo, no manda nada y te dice qué arreglar. Reescribí, no la saltees.
- ⛔ **Prohibidas las fotos aburridas.** Un cuarto vacío, un objeto solo o un "plano general a 2 m" NO sirven. Cada foto: alguien haciendo algo a mitad del gesto (o el rastro fresco de lo que pasó), en un lugar real LLENO de cosas, con una emoción que se entiende sin audio.
- **Campos obligatorios:** `type, moment, subject, action, props, setting, light, camera, color, avoid` (+ `person`/`hands`, `clothing` si hay alguien).
  - `type` = `"amateur phone photo, mild JPEG compression, real skin texture with pores, uneven ordinary indoor light, slightly crooked framing, everyday clutter, nothing blurred out, everything in focus, 16:9"` (la frase **nothing blurred out** es obligatoria).
  - `moment`: QUÉ pasa en ese segundo y POR QUÉ importa (atado a la frase del guion que suena ahí), ≥ 70 caracteres.
  - `action`: el gesto a medias (la mano entrando al agua, la taza a mitad de camino a la boca).
  - `props`: **6 a 10 objetos concretos con detalle** (material, color, desgaste): "a dented aluminium kettle", no "kettle".
  - `camera`: **variá en cada foto**: manos a 40 cm, plano medio, cenital de la mesa, por encima del hombro, desde la puerta. ≥30 % primeros planos, ≥60 % con persona o manos.
  - `avoid` = `"cinematic lighting, dramatic shadows, studio look, perfect plastic skin, empty clean background, depth-of-field blur, date stamp, watermark, readable text"`.
  - Prohibido en el resto del prompt: cinematic, photorealistic, 35mm, bokeh, 8k, golden hour, stock photo (dan look de IA).
- **Imágenes creativas (4 a 6 por video, en los momentos clave):** el cuaderno abierto a cámara con pasos a mano, la grilla de rutina (collage de celular), el antes/después, el flat lay con tarjetitas escritas a mano, la foto vieja en la mano. `type` dice qué es + la cláusula de realismo; texto legible EXACTO entre comillas y corto. Sumá siempre un `"detalle_narrativo"` con 2-3 detalles que nadie te pidió (la hora en cada fotito, una mancha de té, el gato dormido en una sola foto).
- **Vos SÍ podés ver imágenes** (Read sobre un .png). Después de cada tanda armá una hoja de 12 con `hoja.py` y mirala. Repedí (con id nuevo) las que tengan texto inventado, manos rotas, la cara cambiada o look de publicidad.

## 5. Armado (herramientas del Estudio: no las copies ni las edites)
```
python {APP}/tools/render.py <carpeta> [--limit 10]
python {APP}/tools/assemble.py <carpeta>
```
- `shots_timed.json` = `[{"id":"b01_gancho","startMs":0,"endMs":3200}]` — `id` = nombre sin extensión de la foto en `fotos/`. Cubrí de 0 al final de la voz, sin huecos.
- `avatar_ranges.json` (§3) tapa las fotos que haya debajo.
- Fotos con movimiento al azar, fundidos (avatar 0,6 s / foto 0,3 s), escala 4K antes del zoom: ya está hecho. render.py escribe `plan.json` solo (el panel lo dibuja): no lo escribas a mano.
- Si un clip de avatar todavía no existe, NO esperes: render.py pone la foto del presentador. Cuando llegue el clip, corré render.py y assemble.py otra vez (sólo rehace lo que cambió).
- SFX opcionales: archivos en `<carpeta>/sfx/` + `cues.json` = `[{"file":"x.mp3","t":171100,"gain":0.05,"fade":0.4}]`. Pocos y bajos.
- Salida: `final.mp4` 1920x1080 30 fps, AAC estéreo. Duración = la de la voz.

## 6. Control de calidad (no frena)
- `python {APP}/tools/validar.py <carpeta> --etapa guion|fotos|render|final --min <minutos>`. Sólo frena con ✗ (video roto, sin audio, desincronizado, no arranca con el avatar, avatar congelado, hueco negro > 0,5 s, menciones de IA, sin título).
- En fotos/render/final mirá la hoja con Read y escribí en `gates/<etapa>_auto.txt` qué miraste y qué arreglaste. Después SEGUÍ.
- Si el usuario te escribe correcciones en el chat, aplicalas antes del armado final.
- `REPORTE.md`: qué se hizo, gasto, problemas y qué falta.

## 7. Carpetas (el panel las lee para dibujar el pipeline — respetalas)
`guion.txt` · `voz/master.wav` · `captions.json` · `avatar/` · `fotos/` (cada foto con su `.json`) · `sfx/` · `plan.json` · `segments/` · `qc/` · `final.mp4` · `meta.json` · `REPORTE.md` · `refs/` (avatar, cara, voz, canal: NO los toques).
