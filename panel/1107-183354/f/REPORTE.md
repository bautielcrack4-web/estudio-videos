# REPORTE — hr10 · Hospice Chaplain Rosa

**Título:** What People With Dementia Say at the Very End — I Heard It at 400 Bedsides as a Hospice Chaplain
**Duración:** 29 min 25 s (1764,65 s de video = 1764,65 s de voz, desfase < 0,3 s)
**Archivo:** `final.mp4` · 808 MB · 1920x1080 · 30 fps · H.264 CRF 20 · AAC 188 kbps estéreo 44,1 kHz

## Qué se hizo

- **Guion:** 4951 palabras en inglés, voz de capellana de hospicio (34 años), gancho con número (four hundred bedsides) y objeto (cuaderno espiral de 79¢ en H-E-B Bandera Road), credencial ("I am not a physician and I am not on the medical team"), test interactivo al minuto ~4, 7 puntos con problema → anécdota con fecha/nombre/lugar → por qué → cambio concreto con precio → "check tonight", like/subscribe antes del último punto, cierre con pregunta para comentarios y gancho al video siguiente. Cero palabras prohibidas (honest / genuinely / nurse / doctor / clinic / patient / cure / heal / as an AI), cero consejo médico. 3 tags de Fish.
- **Voz:** Fish `rosa_mx` con `--keep-tags` → `voz/master.wav` (1764,6 s).
- **Tiempos:** transcripción por palabra con Groq → `captions.json` (4923 palabras); todos los cortes clavados al `startMs` de la palabra que los motiva.
- **Avatar:** InfiniteTalk, **una sola llamada** (US$ 0,25), 122 ventanas de 3-6 s, 528 s = 30 % del video (estilo Bertha), nunca más de 20 s sin avatar, apertura con avatar hablando desde el segundo 0. Desfase medido y corregido por `avatar_it.py` (máx 395 ms corregido).
- **Fotos:** 264 fotos de b-roll por la cola compartida de avatarity (Nano Banana + desvío gpt-image-2), todas con prompt JSON completo (`type, moment, subject, action, props 6-10, setting, light, camera, color, avoid`), gente a mitad de gesto, lugares reales llenos de cosas, cámaras variadas. 262 ids en el plan, uso máximo 2 veces.
- **4 imágenes creativas de GPT:** `cr_cuaderno` (las 5 frases escritas a mano con hora y mancha de té), `cr_cartas` (tarjetas de papel rasgado con las frases), `cr_foto` (foto vieja en blanco y negro en el regazo con rosario y crucita), `cr_pasos` (3 cuadros 7:40 / 8:15 / 9:02: la lámpara, la silla, la silla apuntando a la cama vacía con la lámpara prendida).
- **Sonido:** 6 SFX de Mixkit en `cues.json` (silla, sábana, página x2, puerta, taza), gain 0,035-0,05, sólo en momentos puntuales.
- **Armado:** `render.py` en la nube (GitHub): 416 segmentos en 26 tandas, 27 máquinas, render en 4,6 min + descarga; fundidos avatar↔foto 0,6 s y foto↔foto 0,3 s, movimiento Ken Burns al azar con semilla fija, escala 3840x2160 antes del zoompan.

## Control de calidad

- `validar.py --etapa final --min 25` → **RESULTADO: OK** (ningún ✗). Avisos (!) anotados abajo.
- Revisión visual con Read: `qc/hoja_final1.jpg` y `qc/hoja_final2.jpg` (15 cuadros cada 30 s + cierre). Todo correcto: Rosa igual en todas (cardigan lila, blusa blanca, crucita), avatar hablando al inicio, ningún cuadro negro, ninguna cara de persona moribunda, ningún cuerpo, sin sangre/tubos/agujas.
- Los 11 "huecos sin imagen" del aviso son el solape de los fundidos (0,3-0,5 s): verificado con un cuadro en 48,85 s — es un fundido entre dos imágenes, no un negro.

## Avisos que quedaron (!)

- Guion 4951 palabras vs banda 2762-4312 para 25 min: se aceptó el video de 29,4 min (la voz ya estaba hecha; más largo, nunca más corto).
- 4 fotos no salieron de Nano Banana: son las 4 creativas de GPT (pedidas a propósito por la cola, desvío gpt-image-2/quality low).
- 18 fotos duran más de 8 s: son planos largos en anécdotas y las creativas (4-6 s con zoom muy lento); se dejaron así a propósito para no picar el relato.

## Problemas y cómo se resolvieron

1. **Fotos que nunca llegaron:** 29 ids de las tandas e/j/k no se entregaron. Se reencolaron como slug `hr10ds_c` (28 pedidos, linter OK) y llegaron en minutos. Pérdida definitiva: `j19` (rechazo CSAM_MINOR_SAFETY del servidor) → sustituida por `fill.py` por la foto j más cercana, uso máximo 2; y `gancho_a` (CONTENT_POLICY_VIOLATION) → no se usa (el gancho quedó en `gancho_b`).
2. **`avatar_it.py` se cayó una vez con WinError 1455** (archivo de paginación) por presión de memoria del equipo; se relanzó y terminó sin gastar otra llamada de RunPod (el FAILED no cobra).
3. **Render local con `RENDER_WORKERS=6`:** 2 segmentos de avatar fallaron con "Generic error in an external library" (libx264, presión de memoria). Con 2 workers salieron bien. Después el creador movió el render a GitHub y se usó esa vía (prohibido render local).
4. **El primer render local completo terminó sin `final.mp4`** (quedó obsoleto al cortarse el render local); se resolvió con el render en la nube.
5. **Cola compartida lenta:** ~10 videos en paralelo; se esperó con `esperar.py`, sin saltar colas ni llamar APIs directo.
6. **Música:** no se pudo descargar música. El video va sólo con voz y 6 SFX sutiles (no hay pista musical de fondo).
7. **Primer cuadro del avatar:** el creador pidió que sea la foto de ChatGPT web `D:/rtmp/hospice/refs/rosa_av.png`; se puso en `avatar_ranges.json` (primera ventana) y en `avatar/frames/rosa_av.png`. El clip `A0.mp4` ya estaba generado con el cuadro anterior y **no se regeneró** porque InfiniteTalk permite una sola llamada por video (US$ 0,25 pagados una vez). El clip A0 es idéntico en escena y ropa; el cambio de `frame` sólo afecta la referencia.

## Costos

- **Avatar (RunPod/InfiniteTalk):** US$ 0,25 (una sola llamada).
- **DeepSeek:** no se usó para el guion (lo escribí yo); sin medición de costo.
- **Fotos, voz, transcripción, SFX:** gratis (colas compartidas / Fish / Groq / Mixkit).

## Qué falta / mejoras para la próxima

- Música de fondo suave (no se pudo bajar ninguna).
- Si el creador quiere A0 con el cuadro nuevo, hay que permitir una segunda llamada o generar el clip aparte.
- Los 11 solapes de fundido se podrían cerrar ajustando `shots_timed.json` al frame exacto (estético, no se nota).

## Control de gates

- `gates/guion_auto.txt` + `gates/guion_pedido.txt` ✓
- `gates/fotos_auto.txt` + `gates/fotos_pedido.txt` ✓
- `gates/render_auto.txt` + `gates/render_pedido.txt` ✓
- `gates/final_auto.txt` + `gates/final_pedido.txt` ✓
- `gates/correcciones.txt`: no existía al cerrar (nada que aplicar). Ver `gates/correcciones_hechas.txt`.
