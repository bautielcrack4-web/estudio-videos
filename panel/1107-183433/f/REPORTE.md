# REPORTE · fn07ds
**What Families Never See After the Casket Closes at a Mexican Funeral**
Ernie Navarro, funeral director (San Antonio). Inglés. 2026-11-07.

## Qué se hizo
- **Guion** de 4.900 palabras (~31,8 min de voz). Gancho 0–45 s con número y objeto,
  credencial del presentador, prueba interactiva al minuto 4, nueve puntos con problema →
  anécdota con fecha/nombre/lugar → por qué pasa → cambio concreto con precio → chequeo de
  esta noche, like/subscribe antes del último punto, cierre con pregunta y gancho al próximo
  video (crematorio, BIBLIA fn08). Sin "honest", "genuinely" ni relleno. Sin consejo médico.
- **Voz**: Fish, voz `ernie_en`, con tags de emoción (`--keep-tags`). Master en `voz/master.wav`;
  los tags se conservaron y el ASR los ignora.
- **Transcripción**: Groq, 4.806 palabras con tiempo por palabra → `captions.json`
  (última palabra 1905,986 s). Todos los cortes están anclados a esas marcas.
- **Avatar**: InfiniteTalk, **una sola llamada** (US$ 0,25). 115 ventanas de 3–7 s,
  27,6 % del video, cada ~11–13 s, hueco máximo 17,0 s, suma+0,3 = 560,4 s (tope 590).
  Primera ventana 0–6,43 s (el video abre con el presentador hablando desde el segundo 0) y
  última ventana cerrando sobre el presentador a los 1906 s. Desfase medido y corregido por
  `avatar_it.py` (queda en `avatar/it_sync.json`, deriva máxima 395 ms).
  El cuadro de referencia del avatar es **`D:/rtmp/funerario/refs/ernesto_av.png`** (la foto
  de ChatGPT web, máxima calidad; cambio del creador del 7-nov). No se usó ninguna foto de
  Nano Banana como cara: el `frame` de la primera ventana apunta a ese PNG y `BRIEF.md` lo
  fija con `FRAME_AVATAR`, que es lo que leyó `avatar_it.py`.
  La llamada de RunPod se **adoptó** (misma huella de audio) tras cortarse el sondeo: se pagó
  un solo /run.
- **B-roll**: 298 pedidos a la cola de avatarity (Nano Banana / gpt-image-2 en paralelo;
  269 de la primera tanda + 27 que quedaron sin bajar + 2 repedidas),
  prompts en JSON completo con `moment`, `action`, 6–10 `props` concretos, `camera` variada
  (≥30 % primeros planos, ≥60 % con persona o manos) y `avoid` con fecha, reloj y texto.
  5 imágenes creativas de GPT (cuaderno a cámara, flat lay de efectos, foto del padre,
  antes/después de la tumba, tira del refrendo) con capa de detalle narrativo.
  En disco: **270 archivos** que cubren los **255 ids** de `shots_timed.json` (0 faltantes).
  Repedidas por texto legible inventado: `n18_aviso_esquina` y `r12_fuentes_pan` (llegaron
  como `n18b` / `r12b`; se copiaron sobre el nombre original para no tocar los tiempos).
- **Tiempos**: `shots_timed.json` con 367 cortes (media 3,8 s de foto visible, máximo 6,9 s,
  sin huecos); el gancho (`gancho_a`) entra justo al terminar la primera ventana de avatar.
- **Sonido**: 5 SFX puntuales de Mixkit (tapa del cajón, papel, puerta, taza, pala), gain
  0,035–0,06. **No hay música**: el video va con voz y ambiente, como el resto del canal.
- **Armado**: `render.py` (Ken Burns con movimiento sorteado, fundidos de 0,6 s avatar↔foto y
  0,3 s foto↔foto). 474 segmentos. La corrida completa tomó la vía **en la nube** de
  `render.py` (GitHub Actions `estudio.yml`, 30 trabajos en paralelo + 1 de unión,
  corrida 42441797595): subió los segmentos como assets y bajó el `final.mp4` ya armado con
  voz y SFX. En paralelo quedó corriendo el render local como respaldo
  (`RENDER_LOCAL=1`, 295 segmentos en cola compartida). `assemble.py` no hizo falta.

## Entrega
- `final.mp4`: **1906,300567 s** (31 min 46 s), 826.301.088 bytes (826 MB),
  1920x1080, 30 fps, H.264 CRF 20, AAC 44,1 kHz estéreo. Duración = voz (1906,301 s).
- Validación final `validar.py --etapa final`: **RESULTADO OK**, todas en verde.
- Estado al cierre (8-nov, aviso del creador: el render ya no se hace en la PC): el
  `final.mp4` entregado **vino de la vía de nube** y pasó el QC, así que **no se re-renderizó**
  ni hace falta `assemble.py`. El respaldo local que se había lanzado en paralelo quedó como
  historia del proceso; desde el aviso `RENDER_LOCAL=1` está prohibido y no se volvió a usar.
- `gates/correcciones.txt`: no existe, no hubo correcciones del revisor que aplicar.
- Revisión visual: 63 cuadros cada 30 s en `qc/` (`hoja_final_1/13/25/37/49/61.jpg`), todas
  revisadas. Apertura correcta (avatar real desde t=0, `gancho_a` a los 8 s), avatar
  consistente, sin cuerpos ni caras de fallecidos, sin texto inventado ilegible.
  Detalle completo en `gates/final_auto.txt`.

## Costos
- InfiniteTalk: **US$ 0,25** (1 llamada).
- Fotos, voz, transcripción, SFX y render: **US$ 0** (colas, claves gratuitas y GitHub Actions).

## Problemas
- Cola de imágenes compartida con ~10 videos en paralelo: la espera fue de varias horas para
  las 269 fotos. Se avanzó con todo lo demás mientras llegaban.
- El guion quedó en ~31,8 min (el validador esperaba 25): es el largo aprobado, no se recortó.
- El render completo local murió a mitad de camino (205/474 segmentos) sin error en el log;
  se relanzó y tomó la vía de nube, y el render local se lanzó como respaldo.
- El trabajo "final" de GitHub Actions quedó ~40 min colgado con 30/31 trabajos en verde;
  terminó solo y el `final.mp4` bajó completo.
- 3 segmentos (0156, 0157, 0172) quedaron en 0 bytes por ffmpeg `-22 (Invalid argument)`;
  se reconstruyeron con el render local y quedaron válidos.
- `assemble.py` falló con `WinError 32` sobre `final.mp4.bajando` porque el descargador de la
  nube tenía tomado el archivo temporal. No hizo falta: el `final.mp4` de la nube ya estaba.
- Avisos del validador (no bloquean): 4.900 palabras vs rango de 25 min; 13 "huecos" de
  `plan.json` que son el solapamiento de los xfade (el video no tiene cuadros negros,
  verificado en las 63 muestras).
- Texto legible inventado pero plausible (cuaderno de servicios, hoja de precios FTC,
  contacto "javier olivares"): se revisó y se conservó.
- Disco D: quedó al 100 % (3,2 GB libres) por los ~10 videos en paralelo; no afectó la entrega.
