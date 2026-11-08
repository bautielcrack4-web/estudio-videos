# REPORTE · Las 7 cosas que la funeraria no te dice antes de firmar el contrato

Canal: Don Ernesto, el Funerario · Funeraria Navarro (Analco, Guadalajara)
**Duración: 25:02 (1502,40 s)** · 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192k estéreo

## Qué se hizo
- **Guion**: 3979 palabras, español mexicano de Guadalajara. Gancho 0-45 s con número y objeto, credencial del presentador, prueba interactiva al min 4, los 7 puntos con problema → anécdota con fecha/nombre/lugar → por qué pasa → cambio concreto con precio → "chequeo de esta noche", like/suscribe antes del último punto, cierre con pregunta y gancho al siguiente video (el traslado). Historia madre de Don Refugio respetada tal cual la BIBLIA. Precios con fuente (Profeco / FTC Funeral Rule). Sin palabras prohibidas ni consejos médicos, y sin marcar el contenido como IA.
- **Voz**: Fish, voz `ernesto_es`, con tags de emoción. Master en `voz/master.wav` (1502,378 s).
- **Transcripción**: Groq por palabra → `captions.json`; todos los cortes y las ventanas de avatar están clavados al `startMs` de la palabra.
- **Avatar**: 101 ventanas (398 s = 26 % del video), estilo Bertha: ventanas cortas cada ~11-13 s, nunca más de 20 s sin avatar, la primera desde el segundo 0 y con el primer cuadro real de `funerario/refs/ernesto_av.png`. Una sola llamada por `avatar_it.py`, desfase del reel medido y corregido (máx 305 ms). US$ 0,25.
  - **Cuadro de referencia (cambio del creador, 8-nov)**: el primer cuadro NO se generó con Nano Banana; es la foto de ChatGPT web tal cual. La ventana 1 usa `"frame": "D:/rtmp/funerario/refs/ernesto_av.png"` (ruta absoluta al original, sin copia intermedia). Verificado: `avatar/frames/a1.jpg`, que es lo que se le pasó a InfiniteTalk, tiene exactamente las mismas medidas que el PNG (1672x941) y un SSIM de 0,9927 contra el original — es la misma foto recomprimida a JPEG, no una generación. El primer cuadro del `final.mp4` (t = 0,05 s) muestra esa misma escena y al mismo presentador, ya hablando.
- **Fotos**: 572 imágenes en `fotos/` (b-roll por la cola de avatarity, con la cláusula de realismo de celular). 321 ids distintos en el plan, 0 faltantes. 3 variantes del gancho (gancho_a / b / c), alternadas cada 2-3 s en los primeros 30 s. Hojas de contacto revisadas con Read en `qc/` (lote por lote, la de fotos, la de render y las 4 del final).
- **Clips de video**: 0. Todo el b-roll va en fotos con Ken Burns; no hizo falta gastar los 15 clips de Veo.
- **Sonido**: 8 efectos puntuales (papel, puerta, teléfono, reloj, viento de panteón, motor, cuaderno) con `cues.json` a gain 0,033-0,05. **No hay música**: la biblioteca de audio de YouTube Studio no se puede descargar desde la herramienta del panel.
- **Armado**: `render.py` (411 planos, Ken Burns al azar con semilla fija, escala 3840x2160 antes del zoompan, fundidos 0,6 s avatar / 0,3 s foto) + `assemble.py`, todo local (RENDER_LOCAL=1): el render en GitHub Actions se quedaba trabado subiendo archivos.

## Reparación del plano de las 3:35 (después del armado)
En la revisión visual del final encontré que el plano 59 (`q02_tres_preguntas.jpg`, 5 s a las 3:35) mostraba un papel con las tres preguntas **en inglés** ("Where is the key? / Why is he here? / When are they coming?"). En un video mexicano eso no va.
- Lo reemplacé por `p5_08_tres_preguntas.png`, las mismas tres preguntas en español (ya estaba en `fotos/`, sin usar).
- Para no re-renderizar los 25 min hice un **parche quirúrgico**: corte en keyframes (208,266667 s y 224,933333 s), re-encode de sólo 16,667 s (500 cuadros = original + foto nueva con Ken Burns + original) y unión con el demuxer concat en `-c copy`. El audio completo se re-encodeó aparte (AAC 192k estéreo) y se remuxeó, así que el sincronismo no se movió.
- Resultado verificado: 1502,400 s (idéntico al original), h264 1920x1080 30/1, AAC 44,1 kHz 2 ch, 522 MB. En 215,0-220,3 s ya no queda ni un cuadro con texto en inglés y las dos disolvencias (0,3 s) se ven como el resto. Hojas: `qc/hoja_patch2.jpg`, `qc/hoja_patch3.jpg`.
- Ojo: `plan.json` lo escribe `render.py` y sigue nombrando `q02_tres_preguntas.jpg` en ese tramo (no se toca a mano). El archivo se ve bien; el único desfasaje es esa línea de `plan.json`. Los scripts del parche quedaron en `qc/patch/` (`fix_patch1c.py`, `mux_fix3.py`) por si hay que repetirlo con otra foto.

## Costos
- Avatar InfiniteTalk: **US$ 0,25** (1 sola llamada).
- Fotos: US$ 0 (cola compartida de avatarity; el desvío del creador las hace con gpt-image-2 low).
- Voz Fish, transcripción Groq, efectos Mixkit, clips: US$ 0.
- Guion: el gasto de DeepSeek lo registra el panel; la carpeta no guarda recibo.

## Problemas y cosas a mejorar
- **Huecos en el plan (corregido)**: `render.py` descarta los trozos de plano de menos de 500 ms; había 20 huecos (5,38 s) porque los cortes de `shots_timed.json` no coincidían con los bordes de las ventanas de avatar. `ajustar.py` movió 57 bordes de planos a esos bordes (sin tocar las ventanas, lipsync intacto). Verificado: 411 tramos, 0 huecos.
- **Segmentos rotos al renderizar (corregido)**: los segmentos 0105 y 0116 fallaron con error de memoria de libx264 (la PC estaba cargada por otros renders). Se rehicieron y se verificó el cuadro exacto de cada uno.
- **El primer armado se cayó dos veces**: una por falta de memoria, y otra porque el disco se llenó a mitad de camino (un trozo de la concatenación quedó truncado). Se borraron los intermedios (`segments/`, `xf_tmp/`, los bloques de voz), se rehízo el armado en una sola pasada por trozos con `libx264 -preset veryfast -crf 20` y se rearmó sin `faststart` para no volver a necesitar el doble de espacio.
- **Fotos con texto en otro idioma o inventado**: el de las 3:35 ya está reparado (arriba). Queda **un solo texto en inglés de 1,9 s a las 6:34** (`p1_20.png`, una hoja de cálculo con "Home Solutions / Better Build"): dura menos que un parpadeo y está semitapado por el movimiento, así que no lo parcheé. También hay un cuadro con la bandera de Texas colgado en la pared del set de oficina (~208-210 s), que es decoración y no texto; y un cartel inventado "FUNERALES GONZÁLEZ" en `c05_zarzamora`. Si alguno molesta, se repite la foto y se parchea igual que el de las 3:35.
- El texto de `captions.json` que devuelve Groq viene en inglés (sólo se usaron los tiempos); los textos en español están en `captions_es.json`.

## Validación
`validar.py --etapa guion / fotos / render / final` → **OK en las cuatro**, con todos los chequeos en ✓ (abre con el avatar real desde 0 s, ventanas ≤6 s en los primeros 30 s, avatar 26 %, nunca >20 s sin avatar, 0 huecos, 1920x1080 30 fps, 1502,40 vs 1502,38 s, meta.json completo).
Avisos que quedan anotados: 250 fotos no salieron de Nano Banana sino del desvío de gpt-image-2 (regla del creador, no se repiten), y el de la revisión visual, que está en `gates/final_auto.txt`.

## Estado
`final.mp4` listo para entregar. `meta.json` con título y descripción de YouTube (268 palabras, voz del presentador, sin links ni hashtags de IA). Puntos de control en `gates/` (guion, fotos, render, final); no había `gates/correcciones.txt` que aplicar.
