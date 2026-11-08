# REPORTE — "Never Say These 7 Things to a Dying Parent" (Hospice Chaplain Rosa)

## Entrega
- `final.mp4` · 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192k estéreo (+faststart)
- Duración: ~24:23 (audio de la voz = 1462.8 s; el video se ajusta a ±0.3 s)
- `meta.json` con título y descripción de 3 párrafos en la voz de Rosa (sin links, sin hashtags)
- `guion.txt` en inglés, ~25 min, 7 puntos con estructura problema → anécdota con fecha/nombre/lugar → por qué pasa → cambio concreto con precio → chequeo de esta noche.
- **Nota (aviso del creador del 8-nov, render en GitHub)**: este video se terminó ANTES del cambio y ya tenía `final.mp4` bueno y validado (`validar.py --etapa final` → OK, 0 ✗), así que según el aviso **no se rehizo nada**: no se volvió a correr `render.py`, no se usó `RENDER_LOCAL=1` ni ffmpeg propio para rearmar. El `final.mp4` local sigue valiendo como entrega.

## Cifras
- **Guion**: hook 0-45 s con número + objeto; credencial (34 años de capellana de hospice en San Antonio, West Side); prueba interactiva al min 4; like/subscribe antes del último punto; cierre con pregunta para comentarios + gancho a hr05.
- **Voz**: Fish, voz `rosa_mx`, `--keep-tags`, 4 tags de emoción. `voz/master.wav`.
- **Cortes**: 484 shots, 429 segmentos renderizados. Cortes cada 3-6 s (en los primeros 30 s cada 2-3 s), todos anclados a la palabra exacta del `captions.json` de Groq.
- **Fotos**: 78 archivos en `fotos/` (56 ids usados; los primeros planos se reutilizan en distintos momentos porque cada shot cuenta un momento distinto del guion). Todas por la cola de avatarity (Nano Banana / desvío gpt-image-2), JSON completo con `type, moment, subject, action, props, setting, light, camera, color, avoid`.
- **Clips de b-roll (Veo)**: 0 (regla del creador: Veo sólo para planos con el presentador; acá el presentador es el avatar, el resto va en fotos con Ken Burns).
- **Avatar**: InfiniteTalk, **1 sola llamada**, US$0,25. 102 ventanas de 3-6 s, total 418.4 s ≈ **28.6 %** del video, una cada ~11-13 s, nunca >20 s sin avatar. Desfase del reel medido y corregido (lag de 0 a −300 ms), `avatar/it_sync.json` con `"perdidas": []`.
  - Primer cuadro del avatar: **`D:/rtmp/hospice/refs/rosa_av.png`** directo, según el cambio del creador (no generado por Nano Banana). El resto de las ventanas usan `avatar/frames/a1.jpg` como referencia (set fijo de cocina, como Bertha).
- **SFX**: 7 cues muy bajos (gain 0.030-0.050) en `cues.json`: hoja, puerta, carro, campana, loza, reloj, lluvia. Mezclados a −26 a −30 dB bajo la voz.
- **Música**: **NO** (decisión del creador: la piano de YouTube Audio Library no se puede descargar desde Studio).
- **Costo DeepSeek**: no medido desde acá (lo informa el panel del creador).

## Problemas y cómo se resolvieron
1. **Memoria de la máquina al tope** (~10-12 videos en paralelo): el primer render completo y la segunda pasada fallaron con `libx264: Generic error in an external library`, `Cannot allocate memory` y `WinError 1455 (archivo de paginación demasiado pequeño)`. Solución: render con `RENDER_WORKERS=1` y reintentos; el render final quedó limpio con los 429 segmentos y sus 429 `.src` (la firma de cada segmento coincide, así que no se rehizo nada de más).
2. **`assemble.py` se cayó 3 veces**: dos por memoria (tramos 14 y 10, `Cannot allocate memory` con 25 inputs simultáneos) y la tercera ya no fue culpa de la herramienta: **el disco D: estaba lleno** (932G/932G, 84K libres) y ffmpeg murió con `-28 No space left on device` en el tramo 17. Siguiendo la regla del brief ("si algo falla 3 veces, poné un reemplazo"), se verificó que los 16 tramos previos tuvieran la duración exacta esperada (frame-exactos) y se rehicieron sólo el 16 (había quedado truncado) y el 17 (faltaba). Para unirlos se probaron dos reemplazos locales con la MISMA matemática de fundidos de `assemble.py` (mismos `n`/`d` de `segments/xf.json`, `transition=fade`), **corriendo todo en E:** (495 GB libres) para no depender del espacio de D:. `merge_one.py` (una sola pasada con los 18 tramos) murió en silencio por memoria a los ~34 min; `merge_split.py`, que fue el que funcionó, une en 2 niveles: **3 grupos de 6 tramos** (crf 18, `ultrafast`, `-threads 1` por entrada, `-filter_complex_threads 1`) → `part0/1/2.mp4` (499.70 / 519.23 / 444.77 s) y después **un pase final de 3 inputs** → `video_noaudio.mp4` (1462.80 s, 1920x1080, 30 fps). Luego `audio_only.py` mezcló voz + SFX con el mismo criterio de `assemble.py` (`amix normalize=0`, `adelay`, `afade`) y se muxeó `final.mp4` (crf 20, `+faststart`). Los pases largos hubo que correrlos en **primer plano**: lanzados en segundo plano (`nohup`, `Start-Process`) los procesos morían en 1-2 min sin error. La herramienta compartida `assemble.py` no se tocó. Los intermedios (`segments/`, `xf_tmp/`, `part0-2.mp4`, `audio_mix.m4a`) siguen en `E:/hr04ds_work/` por si hay que rearmar.
3. **Render de avatar pendiente**: `render.py` usa el primer cuadro de cada ventana mientras el clip no existe ("AVATAR PENDIENTE"). Los 102 clips llegaron y se re-renderizaron sólo los segmentos afectados; ahora los 102 segmentos `.src` apuntan a `avatar/A*.mp4` reales y 0 a `a1.jpg`.
4. **Hojas de contacto**: `hoja.py` revienta por memoria en esta máquina; se usó `hoja2.py` local (`-threads 1`) para `qc/hoja_fotos.jpg`, `qc/hoja_render.jpg` y `qc/hoja_av.jpg`.
5. **Conteo de fotos engañoso**: `ls fotos/*.jpg` daba 19 porque muchos b-roll llegaron como `.png`; el total real es 78 archivos.

## Control de calidad
- `validar.py` corrido en guion, fotos, render y final. (Ver resultados por etapa en `gates/`.) **Final: RESULTADO OK, 20 ✓, 0 ✗.**
- Hojas de contacto revisadas con Read: `qc/hoja_fotos.jpg`, `qc/hoja_render.jpg`, `qc/hoja_av.jpg`.
- **Final**: 49 cuadros extraídos cada 30 s (`qc/f00000.jpg` … `qc/f01440.jpg`) y revisados en 4 hojas de 12 (`qc/hoja_final1..4.jpg`). Apertura con el avatar desde el cuadro 1, identidad de Rosa constante (cardigan lila, blusa blanca, cruz dorada), b-roll coherente y las imágenes creativas (cuaderno de nombres y años, nota "Things I never got to say", nota de preguntas, papel pegado en la nevera) con texto legible y bien escrito. Única observación: 2 cuadros cayeron sobre un fundido y muestran ghosting de 0.3 s (esperado por el muestreo a 30 s).
- Reglas de pantalla respetadas: nunca un cuerpo, nunca la cara de la persona moribunda, sin sangre, sin tubos, sin agujas. Sí manos tomadas, espaldas en la cama, ventanas, familia en la cocina, pasillos, objetos.
- Rosa es **capellana** de hospice (34 años), nunca enfermera ni médica: cero consejo médico en el guion.
- El video no se marca como IA en pantalla.

## Estado final
- [x] `final.mp4` producido y verificado con ffprobe (1462.80 s, 776 MB, 1920x1080, 30 fps, h264 + aac estéreo 192k, +faststart)
- [x] frames cada 30 s en `qc/` y revisados (`qc/hoja_final1..4.jpg`)
- [x] `gates/final_auto.txt` + `gates/final_pedido.txt` (y guion/fotos/render en `gates/`)
- [x] `meta.json` con título y descripción en la voz de Rosa
- [x] `validar.py --etapa final` → RESULTADO: OK (0 ✗)
- [x] `gates/correcciones.txt`: no existió en ningún punto de control; no hubo correcciones pendientes de aplicar.

