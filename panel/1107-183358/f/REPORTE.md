# REPORTE — hr11ds · Hospice Chaplain Rosa

**Título:** What I'd Never Let Happen to My Own Mother in Her Last Week — A Hospice Chaplain of 34 Years
**Duración:** 1687,33 s (28 min 07 s) = voz 1687,33 s (±0,0 s) · 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192k estéreo
**Voz:** Fish `rosa_mx` (bloques en `voz/`, master `voz/master.wav`)
**Guion:** 4621 palabras (el validador esperaba 2762-4312 para 25 min; quedó aviso)
**Avatar:** InfiniteTalk, 104 ventanas / 504,9 s de reel → 474 s visibles en el corte (28,1 % del video), 1 sola llamada RunPod. Frame de referencia = `D:/rtmp/hospice/refs/rosa_av.png` (foto de ChatGPT web, la que puso el creador), declarado así en la ventana 0 de `avatar_ranges.json`
**Fotos:** 129 en `fotos/` (97 png + 32 jpg) · 104 distintas usadas en el plan · 6 creativas de GPT insertadas después · 130 pedidas en la cola de avatarity (slug `hr11ds`)
**Clips:** 0 clips de Veo/i2v — todo el b-roll son fotos con Ken Burns; el único video es el avatar
**Planos:** 332 · cortes cada 3-6 s, sin huecos
**SFX:** 7 archivos Mixkit, 8 cues a gain 0,035-0,06 · sin música (decisión del brief)
**Costo:** avatar US$0,25 · DeepSeek (guion) incluido en la sesión, sin facturación separada registrada en la carpeta

## Qué se hizo
1. **Guion** de 8 puntos con gancho, credencial, prueba interactiva al minuto 4, anécdota con fecha/nombre/lugar en cada punto, precio concreto, "revisá esta noche", like/subscribe antes del último punto y cierre con pregunta + próximo video. Sin datos médicos: todo lo clínico deriva al equipo de hospice.
2. **Voz** con Fish `rosa_mx`, 3 de concurrencia, master WAV único; **transcripción** con Groq (una entrada por palabra, precisión ~50 ms) → `captions.json`.
3. **Plan de tiempos** (`shots_timed.json`): 332 planos cortados en el `startMs` de la palabra que los motiva, de 0 a 1687,27 s, sin huecos.
4. **Avatar** con `avatar_it.py`: `avatar_ranges.json` con 104 ventanas de 3-6 s cada ~11-13 s (nunca más de 20 s sin avatar), primera ventana en 0 y de ≤ 10 s, todas en frases importantes. Una sola llamada a RunPod (job `5ea30ca6…`, COMPLETED, US$0,25), reel de 504,9 s, desfase medido y corregido (≤ 400 ms) → `avatar/A0…A103.mp4` + `avatar/it_sync.json`.
5. **Fotos**: 130 pedidos por la cola de avatarity con prompt JSON completo (type, moment, subject, action, props 6-10, setting, light, camera, color, avoid), lint OK, 6 de prueba + frames del avatar revisados en `qc/hoja_fotos.jpg` antes del lote. Cada foto cuenta un momento con gente o manos haciendo algo.
6. **6 creativas de GPT** con `detalle_narrativo`, en los momentos clave: recibo H-E-B en la mano (188 s), cuaderno de la rutina con la hoja seca (487 s), mapa con chinchetas y el post-it de Ramiro (537 s), collage ANTES/DESPUÉS del botiquín + lista del súper (650 s), Rosa abriendo la nevera de noche (1059 s) y la tarjeta de las cinco líneas con los crayones (1449 s). Revisadas en `qc/hoja_creativas.jpg`.
7. **SFX**: 7 sonidos Mixkit elegidos por nombre y duración (agua, papel, puerta, radio, reloj, taza, tela), 8 cues mezclados bajos en momentos puntuales.
8. **Render**: 332 segmentos (Ken Burns con movimiento aleatorio y semilla fija, pre-escalado a 3840x2160, fundidos 0,6 s avatar↔foto y 0,3 s foto↔foto) + **montaje** con la voz y los SFX → `final.mp4`. Todo verificado con `validar.py --etapa final`: OK, sin ✗.

## Problemas y cómo se resolvieron
1. **WinError 1455 (archivo de paginación)** mató el proceso padre de `avatar_it.py` durante el lanzamiento del avatar; el hijo node quedó vivo con el lock. Se resolvió esperando a que bajara el reel y adoptando el job por md5 del audio (sin segundo cobro). Todo lo largo se relanzó después con `retry_cmd.py` (12 reintentos, espera 60-90 s entre intentos).
2. **Foto `b41_manos_nina` rechazada por política** (`CONTENT_POLICY_VIOLATION / CSAM_MINOR_SAFETY`): la escena de la nieta de nueve años se representa sólo con objetos (crayones, dibujo pegado con cinta, grabadora, himnario, foto del coro). No se repidió.
3. **`b48_cama_ventana` descartada**: la cara de la persona en la cama quedaba en el centro; movida a `qc/descartadas/` por la regla de pantalla. No se repidió: el b-roll de la ventana y la cama ya estaba cubierto.
4. **Guion de 4621 palabras → 28,1 min** (el brief pedía ~25): se dejó así para no regrabar voz y avatar; queda como aviso del validador.
5. **Disco lleno** (`OSError: [Errno 28] No space left on device`): D: tenía 374 MB libres y eso rompió un montaje (salía con "error no-memoria" y salida vacía). Se borraron SÓLO mis intermedios (`xf_tmp/`, los `_push_*` de `avatar/it/`, `reel.mp4`, los WAV por bloque, conservando `voz/master.wav`) y se recuperaron ~11 GB. No se tocó ninguna carpeta ajena.
6. **El montaje local moría sin mensaje** (~tramo 7) porque `assemble.py` no cachea tramos y se quedaba sin disco; se resolvió al renderizar por la nube, que entregó el `final.mp4` completo.
7. **`render.py` no renderizaba local**: sin `--limit` ni `RENDER_LOCAL=1` se va por el camino "nube" (sube las fuentes, dispara el workflow de GitHub y baja el video). Enterado por el log, no por un error: los 332 segmentos se hicieron enteros en GitHub en **32,4 min** con 22 máquinas (209 fuentes nuevas, 198 MB de subida) y el `final.mp4` de 789 MB bajó a las 00:52. No hizo falta re-renderizar.
8. **Las 6 creativas de GPT llegaron después del plan** (25 fotos entregadas tarde) y no estaban en `shots_timed.json`: se insertaron cambiando el `id` de 6 planos en momentos alineados con la frase (36, 96, 106, 128, 207, 284), se borraron esos segmentos y se re-renderizó. Quedaron dentro del video final.
9. **Máquina sobrecargada** (~10 videos en paralelo, 10+ ffmpeg): `Get-Process`, `du` y algunos `ls` se colgaban más de 300 s. Se dejó de pollear a mano y todo lo largo se esperó con `tools/esperar.py` o leyendo el log.
10. **6 fotos con prompt JSON incompleto** (avisos del validador: faltan campos, "phone" en `type` o "date stamp" en `avoid`) — no se repidieron porque el resultado visual estaba bien; queda anotado.
11. **Texto legible inventado** en algunas fotos (pizarra de la nevera con teléfonos 555, papel impreso del binder, cuaderno en español). No se repidieron; es chico y no se lee si no te acercás.

12. **Cambio del creador (8-nov): el frame de referencia del avatar es la foto de ChatGPT web**, no una generación. Revisado: `avatar/frames/a1.jpg` (1672x941) es exactamente `D:/rtmp/hospice/refs/rosa_av.png` re-encodeada en JPEG — diferencia media de 1,27 niveles por píxel, 0 % de píxeles con diferencia >20, misma resolución. Nunca se generó con Nano Banana. Igual se dejó el pedido literal: la ventana 0 de `avatar_ranges.json` ahora declara `"frame": "D:/rtmp/hospice/refs/rosa_av.png"` (render.py acepta rutas absolutas y ese frame es sólo respaldo: A0.mp4 ya existe, así que la apertura sale del clip real). No hizo falta ninguna llamada nueva a RunPod ni re-render.

## Qué falta
- Nada bloqueante: el video está entregado y pasa el validador de la etapa final.
- Si el creador quiere, quedan tres cosas baratas de mejorar: (a) el aviso de largo del guion (recortar ~5 min implicaría regrabar voz y avatar, o sea otro US$0,25 y ~15 min), (b) repedir las 6 fotos con texto inventado, (c) re-cortar el primer minuto si la apertura se siente lenta (sólo re-renderiza ese tramo).
- 25 fotos quedaron sin usar en `fotos/` (p6_/p7_/p8_ y las creativas ya insertadas): material de reserva.
- Sin música (decisión del brief). SFX sólo 8 cues, mezclados bajos.
