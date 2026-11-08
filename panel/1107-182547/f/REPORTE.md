# REPORTE — hr03ds · Dying Patients All See the Same 3 Things (Hospice Chaplain Rosa)

## Entrega
- `final.mp4` — **renderizado en GitHub** (`render.py`, 462 segmentos en 29 tandas, 30/30 máquinas, 4,9 min). 1920x1080, 30 fps, H.264 ~3,36 Mbps, AAC 44,1 kHz 188k estéreo. 833,1 MB.
- Duración: **31:16,1** (1.876,096 s); voz 1.875,83 s → desvío 0,27 s (±0,3 s). Verificado con ffprobe.
- QC: 63 cuadros cada 30 s en `qc/f_*.jpg` + hojas `qc/hoja_qc1..6.jpg` y `qc/hoja_arranque.jpg` (arranque en el avatar). `validar.py --etapa final` → OK.
- Voz: Fish `rosa_mx` con `--keep-tags` (susurro en el cierre).
- `meta.json` con título y descripción de 3 párrafos en la voz de Rosa (sin links).
- `guion.txt`: 5.243 palabras, ~31 min.

## Estructura
- Gancho 0–45 s: la puerta + el número (34 años, 3.000 pacientes) + la promesa de las tres cosas.
- Cada punto: problema → anécdota con fecha/nombre/lugar (1993 el primer error; Delgado, 1951 las botas; Inés y la puerta de la calle) → por qué pasa → cambio concreto con precio ($3 el cuaderno de H-E-B) → "tonight's check".
- Pedido de like/suscribe antes del tercer punto; cierre con pregunta para comentarios y gancho al siguiente video (hr04: "the three words I almost said to my own mother").
- Rosa es **capellana de hospice, 34 años**; nunca enfermera ni médica; sin consejos médicos.

## Imágenes
- **121 fotos** por la cola compartida de avatarity (Nano Banana / gpt-image-2 según prioridad), slug `hr03ds`. 111 entran al corte.
- Todas con prompt JSON completo (`type, moment, subject, action, props, setting, light, camera, color, avoid`), aprobadas por `lint_fotos.py`; ~10 prompts re-hechos para pasar el linter.
- 6 fotos de prueba primero → `qc/hoja_fotos.jpg`; después lotes con hojas de control de 12 (`qc/hoja_loteA/B/C.jpg`) miradas una por una.
- 3 variantes del gancho (`gancho_a/b/c`): elegí **`gancho_a`** (la mano que apunta a la puerta abierta, la casa llena de cosas al fondo) porque muestra el gesto exacto del video en el primer segundo de b-roll.
- Descartadas: `p_cocina_rosa` (la cara no coincidía con el avatar) y `p_rosa_senala_cuaderno` (páginas en blanco) — la creativa del cuaderno a cámara cubre ese momento.
- 6 creativas de GPT con capa de detalle narrativo (tríptico de puertas, nota a mano, flat lay con ticket, cuaderno a cámara, espejo con post-its, foto vieja en la mano).
- Movimiento Ken Burns aleatorio por foto (semilla fija 20261106), sin patrón, con pre-escalado a 3840x2160.

## Avatar
- InfiniteTalk (RunPod) por `tools/avatar_it.py`: **1 sola llamada**, **125 ventanas**, 522 s = **27,8 %** del video, reel 558,7 s.
- Estilo Bertha: ventanas de 3–7 s cada ~11 s, hueco máximo 13,8 s, primera ventana en `startMs: 0` (0–6,3 s), el video cierra en la cara de Rosa.
- Primer cuadro = `D:/rtmp/hospice/refs/rosa_av.png` (foto real de ChatGPT web, sin generarla con Nano Banana), tal como pidió el creador.
- Desfase del reel medido y corregido por correlación de audio: `avatar/it_sync.json`.
- **Costo: US$0,25** (una ejecución de 63 min en A10G).

## Sonido
- 7 SFX de Mixkit en `sfx/` con `cues.json` (ganancia 0,035–0,07): puerta, café, papel, campanas de iglesia, reloj, pasos, timbre.
- **Sin música**: la pista de piano de YouTube Audio Library no se puede descargar en este entorno (queda anotado como pendiente para el creador).

## Control de calidad
- `validar.py --etapa final --min 25` → **OK** sobre el `final.mp4` de GitHub (sólo 1 aviso !: largo del guion).
- Audio del render de GitHub medido: media −22,1 dB / pico −4,7 dB a los 15 min (mismo nivel que la mezcla original), estéreo.
- 63 cuadros cada 30 s en `qc/f_001..f_063.jpg`, revisados en 6 hojas de contacto (`qc/hoja_qc1..6.jpg`).
- Arranque verificado a t=0,1 / 3 / 6,5 s (`qc/hoja_arranque.jpg`): el primer cuadro es Rosa hablando en su cocina; recién después entra el b-roll.
- Avatar idéntico en las 125 ventanas (misma cocina, tarjeta lila, cruz, Virgen de Guadalupe detrás); fundidos limpios; cierre en su cara.
- Sin fechas impresas, marcas de agua ni texto inventado legible. Pacientes siempre despiertos o descansando en su casa: sin cuerpos sin vida, sin caras de agonía, sin sangre, tubos ni agujas.
- El video no se marca como contenido de IA en ningún momento.

## Problemas y cómo se resolvieron
1. **El proceso de avatar se cortó dos veces** (límite de tiempo del harness). La herramienta retomó la misma ejecución de RunPod (`ADOPTO … NO se paga otro /run`) y cortó los 125 clips al terminar: **no hubo doble cobro**.
2. **Plan de cortes con segmentos de <2 s**: se agregó un mínimo de 2,1 s por plano y una segunda pasada de limpieza → 466 planos, media 4,03 s.
3. **Reel por encima del tope de 590 s**: se ajustó el plan a 522 s hablados (559,7 s con el padding por ventana).
4. **Faltaban fotos al armar el plan** (ids sin imagen): los bloques sin fotos ahora toman prestado el pool del bloque más cercano; al llegar las 121 fotos, 0 faltantes.
5. **Dos segmentos de la prueba fallaron por memoria** ("Cannot allocate memory" de ffmpeg): se re-corrió el render y salieron bien.
5b. **10 segmentos del render completo quedaron corruptos** (0 bytes o sin `moov atom`, por la misma falta de memoria bajo carga): se borraron con su `.src`, se re-renderizaron sólo esos 10 (20 s) y el armado siguió.
5c. **El primer `assemble.py` se cortó con "No space left on device"**: el disco D: estaba al 99 % (otros videos en paralelo). Se limpiaron los WAV temporales del reel y los tramos fallidos de `xf_tmp/`, y se re-armó con `RENDER_LOCAL=1` cuando hubo 12 GB libres.
5d. **El armado final pasó por tres intentos y terminó en GitHub.** El `assemble.py` local murió dos veces por disco lleno (D: llegó a 4 KB libres y el `final.mp4` quedaba sin `moov atom`); con eso hice un armado intermedio `assemble_lean.py` (misma matemática de fundidos de `xf.json` + misma mezcla) que dio un `final.mp4` válido. Cuando el creador cortó el render local, **se rehizo todo por el camino oficial**: `render.py` subió el plan + fotos/avatar/voz/SFX, GitHub renderizó los 462 segmentos en 30 tandas (4,9 min) y bajó `final.mp4` **terminado, con audio incluido** ("hecho entero en GitHub"). No hizo falta `assemble.py`. Se borraron los `segments/*.mp4` locales para liberar 600 MB en D: (el render los usa desde GitHub). El `final.mp4` intermedio quedó como respaldo en `C:/hr03ds_tmp/final_pc_backup.mp4`.
6. **Aviso del validador (no bloqueante)**: el guion tiene 5.236 palabras frente al rango sugerido 2.762–4.312. Se priorizó el largo pedido en el brief (~25 min mínimo, 4.600 palabras).
7. Palabras médicas detectadas por el validador: reescritas en el guion (sin nombres de medicamentos ni diagnósticos).

## Costos
- Avatar InfiniteTalk: **US$0,25**.
- DeepSeek (guion): **US$0** (guion escrito sin API de pago).
- Fotos, voz, transcripción y SFX: gratis (colas compartidas / Fish / Groq / Mixkit).

## Qué falta / qué se puede mejorar
- Música de fondo: falta una pista descargable (el creador puede agregarla en el panel).
- Repetición de algunas fotos: la más usada aparece 16 veces en 31 min (~1 cada 2 min); con más fotos del mismo bloque bajaría.
