# REPORTE — "Lo que las familias nunca ven después de que se cierra el ataúd"

Canal: Don Ernesto, el Funerario · slug `fe05ds` · 2026-11-08

## Entrega
- **`final.mp4`** — 802 MB · 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192k 48 kHz estéreo · **31:16,7 (1876,70 s)**, igual que la voz (0,0 s de diferencia).
- `meta.json` con el título exacto y la descripción de 3 párrafos en primera persona.
- `REPORTE.md` (este archivo), `gates/` con los 4 puntos de control, `qc/` con los cuadros de revisión.

## Guion y voz
- Guion en español de Guadalajara, 9 puntos (sala, caja de traslado, cómo cargan, aparato de descenso, liner/bóveda, bolsa de pertenencias, papelerío, flores, tierra) + precios con referencia a Profeco/FTC + prueba interactiva + like/suscribirse + pregunta al comentario y gancho al próximo video. 5.001 palabras, ~160 ppm.
- Voz: Fish `ernesto_es`, 9 bloques + master (`voz/master.wav`, 1876,70 s). 2-4 tags de emoción en el guion, borrados del audio. Sin música.
- Transcripción: Groq ASR por palabra (`captions.json`, precisión ~50 ms) — de ahí salieron los cortes.

## Fotos (b-roll)
- **254 archivos** en `fotos/` que cubren **328 tomas** (s1-s13, creativas, ganchos a/b/c, apertura).
- Todas pedidas por la cola de avatarity (Nano Banana / gpt-image-2 en paralelo, 355 archivos subidos al render). Linter de fotos activo, sin LINT_FOTOS=0.
- Revisión con hojas de contacto (Read) en todas las tandas. Repetidas las que salieron con fecha impresa, texto inventado, manos raras o look de publicidad.
- `s3_05` (familia cargando el ataúd) la moderación la rechazó 2 veces por menores; se resolvió con un plano sólo de manos adultas en las agarraderas (sin caras, sin parentescos) y "children, minors" en `avoid`.
- Creativas: ficha/orden de pañuelo, grilla de rutina con fechas 1/10/30 OCT, flat lay de pertenencias con nombre bordado, antes/después de la sala, cuaderno con correcciones a mano.

## Avatar
- InfiniteTalk, **1 sola llamada**: reel de 557,9 s desde la foto `D:/rtmp/funerario/refs/ernesto_av.png` (primera ventana con esa foto, como pidió el creador) → **111 ventanas** cortadas (`avatar/A0.mp4`…`A110.mp4`), US$0,25.
- **525 s de avatar = 28 % del video**, ventanas de 3-6 s cada ~11-13 s, nunca más de 20 s sin avatar; apertura en 0 s (A0, 9,8 s). Todos los tramos son clips reales (ninguno congelado).
- Desfase del reel medido y corregido por `avatar_it.py` (máx 395 ms), registrado en `avatar/it_sync.json` (111 cortes, 0 perdidas).
- Reintentos: el corte de clips se cayó 2 veces por falta de RAM de la máquina (x264 no podía reservar memoria con 20 videos en paralelo); se relanzó y terminó los 111.

## Render y armado
- **Hecho entero en GitHub** (como pidió el creador el 8-nov): paquete de 355 fotos/avatares (321 MB, 94 s) + audio (74 MB, 23 s) → 28 tandas en 29 máquinas → **4,4 min** → descarga de `final.mp4` (802 MB). Sin RENDER_LOCAL ni ffmpeg propio.
- Corrida: https://github.com/bagasy-search/claudeyoutubevideos/actions/runs/42449520935
- Primer intento del paquete falló con `No space left on device` (disco D: al 100 %, ~4 GB libres entre todos los chats). Se borraron sólo artefactos regenerables de esta carpeta (segments/, temporales del paquete, bloques de voz) y se relanzó: subió a la primera.
- Fundidos: avatar↔foto 0,6 s y foto↔foto 0,3 s. Fotos con Ken Burns aleatorio (tipo/intensidad/foco sorteados, semilla fija), escaladas a 3840x2160 antes del zoompan.

## SFX
- 8 cues muy bajos (gain 0,035-0,08): papel, madera, cinta, llaves, reloj, papel, agua, tierra. Momentos tomados de `captions.json`. `sfx/` + `cues.json`.

## QC
- `validar.py --etapa final --min 25` → **RESULTADO: OK** (todo ✓: apertura con avatar, estilo Bertha 28 %, sin huecos, specs, duración, meta).
- Revisión visual: primeros 12 s cuadro por cuadro (`qc/hoja_ini.jpg`), uno cada 30 s (`qc/f_001..063.jpg`, 6 hojas) y últimos 4 s (`qc/hoja_end.jpg`). Sin fecha impresa, sin texto inventado, sin manos rotas, sin negro.
- Aviso del validador: 5.001 palabras (el rango esperado es para 25 min; este video dura 31,3 min).

## Costos
- InfiniteTalk (avatar): **US$0,25** (1 llamada, el reel se reutilizó de la bóveda al reintentar el corte: no se cobró dos veces).
- Fotos, voz Fish, Groq, agnes: gratis (colas compartidas).
- DeepSeek (texto del guion/prompts): consumo de la sesión, no se mide desde esta carpeta.

## Problemas y cómo se resolvieron
1. **Disco D: al 100 %** (~4 GB libres de 932 GB por los 20 videos en paralelo): el paquete del render no cabía. Se liberaron segments/, temporales y bloques de voz; quedó espacio para subir y bajar el final.
2. **Falta de RAM**: los clips de avatar se cortaron 2 veces con "malloc failed" de x264. Se relanzó y terminó.
3. **Moderación de Nano Banana** con `s3_05`: 2 rechazos por menores; se resolvió con manos adultas sin caras.
4. **Cambio del creador a mitad de camino**: el render local quedó obsoleto (se borraron sus segmentos para liberar disco) y se rehizo entero en GitHub.

## Actualización del creador (8-nov, flujo sin disco)
- El render nuevo deja el final **hecho en GitHub** (`final.url`, `final.nube.json`, cuadros en `qc/f_*.jpg`, `qc/final_info.json`) y no baja nada a la PC.
- Este video ya tenía su **`final.mp4` bajado, validado y bueno** (802 MB, `validar.py --etapa final` = OK), así que por indicación del creador **no se rehízo nada**: sigue valiendo. Los cuadros de QC de `qc/` ya estaban extraídos de ese mismo archivo.
- Para la próxima: el render corre igual y el panel lo reproduce/entrega desde GitHub; conviene no bajar el archivo (disco D: al 100 %).

## Qué falta
- Nada del video. El archivo está listo para que lo suba el creador desde el panel.
- Sugerencia para la próxima: mantener el disco con ≥20 GB libres antes de armar; con el disco al 100 % el paquete del render falla y hay que repetir la subida.
