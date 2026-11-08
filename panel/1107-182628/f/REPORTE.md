# REPORTE — fe03 · Don Ernesto, el Funerario

**Título:** "He enterrado a 6.000 personas: nunca pongas estas 9 cosas en el ataúd de tu madre"
**Duración:** 26:03 (voz: 1563,23 s · video: 1562,87 s de cuadro)
**Formato:** 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192k **estéreo**

## Qué se hizo

1. **Guion** (`guion.txt`, 4.321 palabras, en español de Guadalajara). Hook 0–45 s con número + objeto (la caja de zapatos con el sobre amarillo), credencial del presentador, prueba interactiva en el minuto 4, los 9 puntos con problema → anécdota fechada (Zarzamora, 22 frascos de medicina, US$3.200 en el bolsillo del saco) → por qué pasa → cambio concreto con precio y fuente (Profeco / FTC Funeral Rule) → chequeo para esta noche. Like/suscribe antes del último punto; cierre con pregunta al comentario y gancho a fe04 ("la urna"). Sin consejos médicos, sin "honest"/"genuinely", sin sermonear. La historia de la madre de Don Refugio quedó exactamente como está en la BIBLIA.
2. **Voz** con Fish (`ernesto_es`, `--keep-tags`, concurrencia 3) → `voz/master.wav`.
3. **Transcripción por palabra** con Groq (`captions.json`, 4.045 palabras, 0–1562,863 s) y todos los cortes clavados en el inicio de una palabra.
4. **Fotos** con Nano Banana por la cola de avatarity: 165 fotos aprobadas para el b-roll + 3 variantes del gancho (`gancho_a/b/c`) en la primera tanda. Todas con prompt JSON completo (`type, moment, subject, action, props 6-10, setting, light, camera, color, avoid`), linter en verde, ≥30 % primeros planos y ≥60 % con persona o manos. 0 clips de Veo.
5. **Avatar** con InfiniteTalk: **1 sola llamada** (US$0,25), 111 ventanas de 3–6 s cada ~11–13 s = 432 s efectivos (28 % del video), nunca más de 20 s sin avatar, y el primerísimo cuadro es el avatar hablando desde el segundo 0 (ráfaga de apertura de 9,36 s). El primer cuadro es la foto entregada `funerario/refs/ernesto_av.png` usada directo, sin pasar por Nano Banana, y `avatar_ranges.json` deja la primera ventana con `"frame": "D:/rtmp/funerario/refs/ernesto_av.png"` (la ruta absoluta al original, regla del creador 8-nov).
6. **Armado** con las herramientas compartidas: `render.py` (Ken Burns al azar por foto: tipo, intensidad y foco sorteados, nunca el mismo movimiento dos veces seguidas, 3840x2160 → 1080p) y `assemble.py` (fundidos de 0,6 s avatar↔foto y 0,3 s foto↔foto, voz + 14 SFX de Mixkit a −24/−29 dB). `plan.json` lo escribió `render.py`.

## Números

| Ítem | Cantidad |
|---|---|
| Fotos de b-roll | 165 (+3 gancho, 1 rechazada) |
| Clips de Veo | 0 |
| Ventanas de avatar | 111 (432 s, 28 %) |
| Segmentos de render | 445 |
| Cortes | 445 planos en 26:03 (3,6–5,2 s; 2–3 s en los primeros 30 s) |
| SFX | 14 cues |
| **Costo DeepSeek** | **US$0,2486** (299 llamadas, medido por el panel) |
| **Costo RunPod/InfiniteTalk** | **US$0,25** (1 llamada) |
| **Total** | **≈ US$0,50** |

## Reprocesos y ajustes

- **Gancho:** 3 variantes pedidas en la primera tanda; elegí `gancho_c` (caja de zapatos abierta con el sobre amarillo arriba de la ropa) y entra apenas termina la ventana de apertura del avatar, a los 9,36 s.
- **1 foto rechazada:** `d1_ataud_patio` mostraba un cuerpo tapado con tela → fuera (regla de pantalla: nunca un cuerpo). Se repidió el momento con el ataúd vacío y flores.
- **1 foto repetida:** `c2_farmacia_recepcion` salió con look de catálogo de stock → repedida con mostrador lleno de cosas y manos a medio gesto.
- **Avisos del validador (no bloqueantes):** guion de 4.321 palabras (justo en el borde alto del rango) y 1 foto (`i01_campo_analco`) que no salió de la cola: era un PNG que rompía el render y se convirtió a JPG con PIL.
- **Textos en inglés en algunos props** (cupón de heladera, lista a mano): se dejaron porque la historia pasa 25 años en San Antonio; el video es en español y el contexto lo explica.
- **Huecos de timeline (arreglados):** las ventanas de avatar no coincidían con los cortes de plano y `render.py` descartaba pedazos <500 ms, lo que dejaba 16 huecos de 0,15–0,4 s. Se corrigió en el origen (`gen/shots.py` fuerza un corte exacto en cada inicio y fin de ventana) y se verificó con `gen/check_plan.py`: 445 segmentos, 0 huecos, 0 pedazos descartados.
- **Memoria/CPU:** la máquina tenía otros ~10 videos en paralelo. El render local con 8 workers reventó por memoria; se terminó con `RENDER_WORKERS=3`. El armado final se hizo por la vía de nube de las herramientas compartidas (GitHub Actions, corrida 42441809410, 28 tandas + job final). El visor local de `gh` se cayó con un panic de Go a mitad de la espera: se relanzó `assemble.py` y se reenganchó a la misma corrida (29/29 jobs) sin volver a renderizar ni gastar cuota.
- **Disco:** el disco D: llegó a 0 bytes libres a mitad del armado (falló el tramo 15 con "No space left on device"). Se borraron intermedios propios (`voz/block_*.wav`, `avatar/it/reel.mp4` y su carpeta de subida) y quedaron 9,5 GB libres; el armado se relanzó sin tocar nada de otros videos.
- **Cambio del creador (8-nov), posterior a la entrega:** la primera ventana de `avatar_ranges.json` ahora lleva `"frame": "D:/rtmp/funerario/refs/ernesto_av.png"` (la foto original de ChatGPT web, sin pasar por Nano Banana). El avatar ya se había generado con esa misma foto: comparé el PNG con el primer cuadro del clip y es la misma escena, el mismo saco y el mismo encuadre. Como `avatar/A0.mp4` existe, `render.py` no usa el `frame` (sólo es respaldo si falta el clip): el plan no cambió y `final.mp4` sigue siendo el mismo, sin segunda llamada a InfiniteTalk.
- **InfiniteTalk:** el reel de RunPod se cortó en local con `gen/cortar_reel.py` porque el lanzador murió después de que RunPod entregó el reel. El desfase medido (−305…0 ms) quedó corregido en el corte y en `avatar/it_sync.json`.

## Sin música

El video va **sin música**: el piano de la Biblioteca de Audio de YouTube no se puede bajar desde el Estudio, así que sólo hay voz y SFX puntuales de Mixkit (14 cues).

## Control final

- `validar.py --etapa final --min 25` → **OK** (todo ✓). Avisos que quedan: 4.321 palabras en el guion (borde alto) y 1 foto que no salió de la cola (PNG convertido a JPG).
- `ffprobe`: 1563,23 s (= voz, 0,00 s de diferencia), 1920x1080, 30/1 fps, H.264 ~3,11 Mbps, AAC estéreo 188 kbps, 616 MB.
- Revisión visual: 52 cuadros cada 30 s (`qc/final30/`) en 5 hojas (`qc/hoja_final_1…5.jpg`). Sin cuerpos, sin caras de moribundo, sin sangre ni agujas; ataúd siempre vacío o cerrado; sin marcas de IA; el video abre con el avatar hablando y se le ve la boca moverse en sincronía. Detalle menor: en un cuadro se ve el borde de un cartel callejero real que dice "CLAUDIA DELGADO" (no es marca de agua).
- Al cerrar volvió a llenarse el disco D: (0 bytes); se borraron los restos del armado local (`xf_tmp/`, 848 MB) y quedaron 5,8 GB libres. Sin entregables afectados.
- **Archivos entregados:** `final.mp4`, `REPORTE.md`, `meta.json`.

## Mejoras para la próxima

- Pedir el b-roll con más días de margen: con 10 videos en paralelo la cola de avatarity marca el ritmo.
- Evitar props con texto en inglés si la historia no lo justifica; el linter no lo detecta y se ve recién en la hoja de contacto.
- Dejar el disco con >15 GB libres antes de armar: el armado de un video de 26 min necesita ~4–5 GB de intermedios.
- Correr el render de noche con `RENDER_WORKERS=3` o directo por la nube; en la PC con 10 videos simultáneos los errores de memoria son la norma.
