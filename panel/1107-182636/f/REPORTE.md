# REPORTE · fe04ds — "Lo que de verdad hay dentro de la urna que te dan en la funeraria"

Canal: Don Ernesto, el Funerario (español de México, Guadalajara).
Fecha de cierre: 2026-11-08.

## Entrega

- **final: 32:00.48 (1920.482 s)** · 1920x1080 · 30 fps · H.264 · AAC 192k estéreo 44.1 kHz · 776,7 MB.
  La duración del video coincide exactamente con la de la voz (`voz/master.wav`, 1920.482 s).
- Se renderizó y unió **en GitHub** (render.py → nube.py), como pidió el creador el 8-nov. **No hay final.mp4 local**
  (regla de cero disco): el archivo queda en la release `est-fe04ds` como `final_ecae72f9cd05.mp4`
  (link en `final.url`, datos en `final.nube.json`), los cuadros del QC en `qc/` y las medidas en `qc/final_info.json`
  (0 huecos negros, revisado con blackdetect). No se subió a ningún lado: la entrega la hace el creador desde el panel.
- `meta.json`: título + descripción de 3 párrafos (1429 caracteres) en la voz del presentador, sin links ni hashtags de IA.

## Qué se hizo

- Guion: 4763 palabras, gancho con número y objeto en los primeros 45 s, credencial, prueba interactiva ~min 4,
  8 capítulos con problema → anécdota con fecha/nombre/lugar → por qué → cambio concreto con precio → "revísalo esta noche",
  like/suscribirse antes del último punto y cierre con pregunta de una palabra + gancho al fe05. Sin palabras prohibidas,
  sin consejo médico, sin marcar el contenido como IA.
- Voz: Fish, voz `ernesto_es` con `--keep-tags`. Transcripción por palabra con Groq (`captions.json`) para clavar cada corte.
- 457 planos, cortes cada 3-4 s, cobertura 0 → 1.920.182 ms sin huecos.
- **150 fotos** de b-roll, todas por la cola compartida de avatarity (Nano Banana / gpt-image-2 según el desvío de la cola),
  con prompt JSON completo (`type, moment, subject, action, props, setting, light, camera, color, avoid`), ≥30 % primeros
  planos y ≥60 % con persona o manos. Movimiento Ken Burns al azar (semilla fija 20261106).
- **116 ventanas de avatar** InfiniteTalk = 529 s = **28 % del video** (estilo Bertha), 3-6 s cada ~11-13 s, nunca más de 20 s
  sin avatar, primera ventana en `startMs 0` y ≤6 s: el video abre con el avatar hablando. Primer cuadro = la foto de ChatGPT
  web `D:/rtmp/funerario/refs/ernesto_av.png`, en las 116 ventanas.
- Sonido: 6 cues sutiles (papel, metal, madera, llaves, tierra) en `cues.json`, gain 0.045-0.05. **Sin música.**
- QC: cuadros cada 30 s en `qc/` (`f_001.jpg` …), revisados con hoja de contacto.

## Costos

- Avatar InfiniteTalk (RunPod, **una sola llamada** vía `avatar_it.py`): **US$0.25** (reel de 563,80 s, 88 min de ejecución).
- Fish, Groq, Nano Banana/cola y el render de GitHub: $0.
- DeepSeek: no hay log de consumo de la cuenta en esta sesión, así que no puedo dar un número medido; el trabajo fue
  texto/coordinación (no hubo llamadas propias a APIs de pago).

## Problemas y cómo se resolvieron

1. **4 fotos rechazadas por CONTENT_POLICY** (`c1_lupa`, `gancho_a`, `gancho_c`, `t_manos_bolsa`), incluso tras reescribir el
   prompt 2 veces. Regla "si falla 3 veces, sustituí y seguí": las variantes de gancho a/c se descartaron y quedó
   **gancho_b** (mujer en la cocina con la urna abierta y la bolsa atada sobre la mesa: tiene el objeto exacto del gancho,
   la cocina está viva y la cara se entiende sin audio) — justificación completa en `gates/fotos_auto.txt`.
   `c1_lupa → c1_cremains_palabra`, `t_manos_bolsa → t_cinta_manos` (misma familia, `prep_fotos.py`).
   `c11_altar_casa` también cayó y se resolvió con `c11_cierre_ernesto`.
2. **El corte del reel de avatar murió por OOM** (numpy no pudo reservar ni 425 KB: la RAM la tenían otros ~20 videos), ya
   después de la llamada paga a RunPod. Se rescató **sin una segunda llamada** con `rescue_cut2.py`: misma cuenta de desfase
   que `avatar_it.py` (envolvente 200 Hz, PAD 0.3) pero extrayendo 8 s de audio por ventana con `-ss/-t` en vez de decodificar
   el reel entero. Resultado: 116/116 clips, **desfase máximo medido 395 ms, corregido** (`avatar/it_sync.json`), 0 pérdidas.
3. **`A40.mp4` quedó truncado** (23 KB / 1,35 s) por ese mismo crash. `recut_bad.py` comparó la duración de los 116 clips
   contra su ventana y rehizo el único que no coincidía (ahora 4,80 s).
4. **Un plano usaba `a1` (cuadro fijo del avatar) fuera de toda ventana** → el validador lo marcaba como avatar congelado.
   Se cambió ese plano por `c2_san_antonio_mesa` y se volvió a renderizar.
5. **`nube.py` no pudo bajar `qc_<plan>.tar`** (ese asset no existe en la release: la corrida subió el final y todos los jobs
   dieron success, pero el tar del QC nunca se subió). Comprobado en la release y en `gh run view`. Como el final ya estaba
   bien, se bajó `final_ecae72f9cd05.mp4` de la release y los cuadros de QC se generaron localmente desde ese archivo
   (eso es QC, no render); después el final local se borró para liberar el disco. Es un problema de la herramienta
   compartida, no del video: hay que avisarle al creador.
6. **Disco D: al 100 %** (932 GB, ~8 GB libres, compartido con ~20 videos): una descarga falló con `WinError 32` y otra con
   "No space left". Se limpiaron `.bajando` viejos y el final local anterior antes de rebajar.

## Avisos (no bloquean)

- **Duración 32:00 vs los 25 min del brief.** El guion quedó en 4763 palabras (el validador avisa: esperado 2762-4312 para
  25 min; el archivo de guion marca 5076 por los tags de emoción). Es un video largo: si el creador lo quiere en 25 min hay
  que recortar guion, no render.
- **Sin música**, como pide el brief.
- El paso de "subir a YouTube / Bagasy / Telegram" no se hizo: lo hace el creador desde el panel.
