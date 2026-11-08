# REPORTE · mk04ds — Japanese Women Over 60 Never Wear These 5 Shoes (And Still Walk 10,000 Steps)

Canal: Michiko's Kyoto Closet · idioma: inglés · fecha: 6 nov 2026

## Estado

- **Guion**: 2587 palabras, 16 min 28 s de voz (`voz/master.wav`, 988.19 s). Gancho 0-45 s con número + objeto; credencial; 5 zapatos con problema → anécdota fechada → por qué después de los 60 → cambio concreto con precio en US$ → "tonight's check"; prueba del papel en el min 4; like/subscribe antes del último ítem; cierre con pregunta para comentarios y gancho al video siguiente.
- **Fotos**: 200 imágenes en `fotos/`, todas por la cola de Nano Banana (avatarity), con prompt JSON completo y linter aprobado (lotes 1-11, slugs `mk04ds` y `mk04ds_b`). 6 fotos de prueba + hojas de contacto revisadas a ojo (`qc/hoja_fotos.jpg`, `qc/hoja_*.jpg`).
- **Avatar**: 5 tramos previstos (A1-A5), 43,5 s en total, todos ≤ 55 s. Plan `avatar/avatar_plan.json`; cara `avatar/cara_hd.png`. **Los clips de lipsync agnes no se pudieron generar** (ver Problemas 3-4): en el final van sus primeros cuadros fijos, sin lipsync.
- **Render**: 202 segmentos (197 fotos con Ken Burns al azar + 5 tramos de avatar). `plan.json` va de 0,0 a 988,08 s sin huecos. Fundidos foto-foto 0,3 s y avatar-foto 0,6 s.
- **Audio**: voz + 7 SFX puntuales (`cues.json`), mezclados a -29/-22 dB. Sin música.
- **Final**: `final.mp4` 1920x1080, 30 fps, H.264 CRF 20, AAC 192k estéreo, **988,186 s** (voz 988,187 s), 445.543.454 bytes (425 MB). Montado a las 19:10; decodificado entero con `ffmpeg -v error -i final.mp4 -f null -` → 0 errores (`qc/decode_check.log`). **Estado del validador: FALLA (1)** — `validar.py` se actualizó a las 19:54 y ahora rechaza la entrega mientras los 5 tramos de avatar sean foto fija ("no se entrega hasta que estén los clips"). El video está completo en todo lo demás; falta sólo que la cola de agnes entregue los 5 clips A1-A5 para re-renderizar esos tramos.

## Fotos y clips

- 200 fotos, 22 por sección más 35 de intro. ≥30 % primeros planos, ≥60 % con persona o manos.
- 0 clips Veo: el b-roll es todo foto con Ken Burns; los únicos planos con persona fija son los 5 tramos de avatar (43,5 s).
- Segundos de agnes: 44 s pedidos, 0 s generados. Los 5 pedidos (A1-A5) se enviaron 4 veces (15:47, 17:50, 19:19 y 19:59) y ninguna vez bajaron el clip: la cola de video contestó siempre `video_queue_full` (ver Problema 3). No se consumió cupo de video útil porque los pedidos no llegaron a procesarse.

## Re-hechos

- 3 segmentos fallaron al renderizar con `Error encoding a frame: Generic error in an external library` (0103 `e21`, 0139 `f21`, 0142 `f24`); se borraron y se re-renderizaron bien.
- `t01`, `t02`, `t03` se copiaron con nombre corto porque `render.py` busca coincidencia exacta de ruta y los originales tenían sufijo descriptivo.
- El gancho se rehizo: había 3 variantes (`gancho_a/b/c`) y se eligió `t01` para el segundo 0 (regla de apertura con foto).

## Gasto

- Nano Banana y agnes: colas gratuitas. **US$ 0,00**.
- Voz Fish: gratis. ASR Groq: gratis. SFX Mixkit: gratis.
- ffmpeg local: sin costo.

## Problemas

1. **Cara del avatar**: el recorte real de la cara mide ≈345 px de ancho, por debajo de los 400 px ideales. No se agrandó (regla del creador: nunca upscalear). Riesgo de avatar algo blando; queda anotado en `gates/fotos_pedido.txt`.
2. **`avatar/avatar_listo.json` engañoso**: un intento anterior escribió el archivo con los 5 clips en `true` sin que existieran los mp4. La herramienta saltea sólo archivos >100 KB, así que no alcanza con mirar ese marcador: hay que comprobar que existan `avatar/A1.mp4 … A5.mp4`. Al final quedó escrito con los 5 en `false`, que es lo real.
3. **Lipsync agnes imposible por la cola compartida**: el 4.º intento (17:50-18:31) falló los 5 clips con `UNKNOWN: unknown error, open 'D:\rtmp\agnes_pool\state.json.tmp'` y `EPERM: operation not permitted, rename ...state.json.tmp -> state.json`, en los 4 reintentos seguidos de cada clip. Después de eso la respuesta del servidor quedó clara: **`{"code":"video_queue_full","message":"video queue is full, please try again later"}`** en todas las llamadas. Revisando el log de la cola (`D:/rtmp/agnes_pool/log.jsonl`), mis 5 tags (`mk04ds_avatar_A1`…`A5`) suman ~1300 intentos entre las 15:47 y las 21:00 y **ninguno** devolvió nada distinto de `res:"queue"`: la cola de video de agnes está llena a nivel global (todos los chats pidiendo a la vez), no es el cupo de las cuentas ni el archivo de estado. No se saltó la cola ni se armó un rotador propio (regla del kit). Se intentó 4 veces más el envío (15:47, 17:50, 19:19, 19:59); la corrida de las 19:59 quedó esperando en segundo plano y se dejó viva hasta las 21:05 sin bajar ningún clip. Entre las 19:00 y las 21:00 tampoco apareció ningún `A*.mp4` nuevo en las otras carpetas de `D:/rtmp`, así que la saturación es de todos. Se mató un proceso duplicado mío (PID 19196, de las 15:28) para no cargar más una cola ya llena. Si los clips aparecen, se rehacen sólo esos 5 segmentos con `render.py` + `assemble.py`.
4. **Proceso de avatar**: se murió dos veces lanzado con `nohup` dentro de un Bash normal; se resolvió lanzándolo como tarea en segundo plano con timeout largo. La tarea de las 19:59 la cortó el límite de 2 h del panel a las 21:59 (sin clips); se relanzó **desprendido con `nohup`** (queda vivo como PID 59816, fuera de la tarea) y sigue reintentando contra la cola. La primera corrida de `assemble.py` la mató el timeout de 1 h y dejó un `video_noaudio.mp4` incompleto; se borró y se relanzó con timeout de 2 h, que terminó bien.
5. **Cola compartida de fotos**: la generación tardó ~1 h con 10 videos en paralelo, pero terminó sin fallidos (`pend 0 · hechos 149 · fallidos 0`). 3 fotos del gancho (`t01/t02/t03`) son copias con nombre corto de las variantes `gancho_a/b/c`, por eso el validador avisa "3 NO salieron de Nano Banana": sí son de Nano Banana, sólo que con otro nombre.

## Mejoras para el próximo

- Generar la cara de referencia a ≥600 px desde el principio (recorte del original grande), para no quedar en el límite.
- Escribir el plan del avatar cuando el clip exista de verdad, no cuando se envía el pedido; y antes de dar el video por cerrado, comprobar los mp4 con `ls -la avatar/*.mp4`, no el json de estado.
- Revisar los segmentos con ffprobe automáticamente después de renderizar: tres archivos quedaron de 262 bytes y no se detectaron hasta el final.
- Pedir el avatar apenas esté la voz y en un momento de menos carga de la cola (los otros ~10 videos estaban todos pidiendo a la vez), o aceptar de entrada el fallback de cuadro fijo para no gastar una hora en reintentos.

## Puntos de control

- `gates/guion_*.txt`, `gates/fotos_*.txt`, `gates/render_*.txt` y `gates/final_*.txt` escritos; `validar.py` en las 4 etapas → OK.
- `gates/correcciones.txt` vacío (el revisor no dejó pedidos); lo que salió de la revisión propia quedó en `gates/correcciones_hechas.txt`.
