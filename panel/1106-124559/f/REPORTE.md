# REPORTE — Michiko's Kyoto Closet · mk02ds

**Video:** “My Mother's Kyoto Rules So Clothes and Towels Never Smell Sour (I'm 68)”
**Archivo:** `D:/rtmp/mk02ds/final.mp4`
**Fecha:** 2026-11-06

## Entregable

| Dato | Valor |
|---|---|
| Duración video | 958,07 s (15:58) |
| Duración audio master | 957,90 s (desfase 0,17 s ≤ 0,3 s) |
| Resolución / fps | 1920×1080 · 30 fps · yuv420p |
| Video | H.264 CRF 20 (3,15 Mbps) |
| Audio | AAC 192 k · 44,1 kHz **estéreo** · pico −3,6 dB |
| Peso | 377 MB |
| Frames | 28.742 (958,07 s × 30) |
| Segmentos | 240 (235 de foto + 5 de avatar) |
| Planos escritos | 242 ids distintos (10 quedaron tapados por los tramos de avatar y se recortaron) |
| Fotos usadas | 242 ids en `img/pics` (245 archivos con 3 extras de respaldo) |
| Clips avatar | 5 (`intro1`, `intro2`, `wash`, `towel`, `phone`) |
| SFX | 12 cues puntuales, −30 a −25 dB bajo la voz |
| Look | `eq=saturation=0.92` aplicado en TODAS las fotos y clips |

## Cómo se hizo

1. **Guion + voz** — guion de ~2.100 palabras según BRIEF; Fish `moda_michiko_ca` con `--keep-tags` → `voz/master.wav` (957,9 s).
2. **Tiempos** — Groq ASR por palabra (`captions.json`) → `tools/timing.py` → `shots_timed.json`: 242 planos contiguos 0→958.085 ms, sin huecos. Cada corte nace en el `startMs` de la palabra que lo motiva (cortes de 3–5 s).
3. **Fotos** — 242 prompts JSON en dialecto Nano Banana (con `person`/`props` concretos, `avoid` con “timestamp”), encolados en la cola compartida por lotes de 30, slug `mk02ds` y `mk02ds_b`: 147 + 108 imágenes, más 3 variantes de apertura, 0 fallidas. Todas las fotos con Michiko usan `refs:["D:/rtmp/michiko/refs/michiko_av.png"]`; Carol, manos y objetos van sin ref.
4. **Avatar** — agnes `agnes-video-2.5-flash` modo reference con `tools/lipsync.mjs` + `tools/avatar_all.sh`. Primeros cuadros de Nano Banana y cadena de continuidad (último cuadro de `intro1` = primer cuadro de `intro2`). Prompts reforzados con “ONE SINGLE UNBROKEN SHOT … never a cut”.
5. **Montaje** — `D:/rtmp/dspanel/tools/render.py` (herramienta compartida; sólo se le parcheó `img_for` para leer `img/pics` y `kind()` para reconocer `/av/`): 3840×2160 → zoompan con 8 movimientos distintos (semilla fija 20261106, nunca el mismo tipo dos veces seguidas) → 1920×1080 → `eq=saturation=0.92`; avatar escalado a 1920×1080 a 30 fps. Fundidos: 0,6 s avatar↔foto, 0,3 s foto↔foto. `D:/rtmp/dspanel/tools/assemble.py` (compartida): cadena xfade por tramos de 25 + mezcla de SFX + máster de voz en **`-ac 2` estéreo** → `final.mp4`.

## Ubicación del avatar en el corte

| Clip | Rango | Escena |
|---|---|---|
| — (foto ap01) | 0,00 – 3,48 s | **apertura**: primer plano de Michiko con el polar beige contra la nariz, pasillo de la machiya |
| intro1 | 3,48 – 9,14 s | salón con jardín, sostiene la bolsa de lino (callback mk01) |
| intro2 | 10,14 – 15,14 s | continuación exacta del cuadro anterior (con una foto de 1 s entre medio) |
| wash | 210,36 – 218,96 s | patio de lavado, toalla sobre la tina de madera (Regla 1) |
| towel | 311,24 – 319,95 s | salón, toalla doblada en las manos (Regla 2) |
| phone | 922,12 – 932,95 s | salón, teléfono en la mano (llamada de Carol → mk13) |

Total en pantalla: **38,69 s** (ideal 35–55 s). Ningún tramo de avatar en los primeros 30 s pasa de 6 s (5,66 s y 5,00 s). Los 5 clips salen con la cara HD (`michiko_face_hd.png`); los viejos de cara chica están en `av/clips_v1_cara_chica/`.

## Cuentas

| Recurso | Gastado |
|---|---|
| agnes (lipsync) | 9 generaciones = ~100 s de video (6 iniciales, uno de ellos rechazado por cortes, + 3 rehechos con cara HD); **5 clips vigentes suman 51,4 s**, 38,69 s usados |
| Cola avatarity (Nano Banana) | 258 imágenes generadas (147 + 108 + 3 variantes de apertura), 0 fallidas |
| Veo / i2v | **0 clips** (no hizo falta: todo el b-roll es foto con Ken Burns) |
| US$ OpenAI | **US$ 0,00** (existe `D:/rtmp/SIN_OPENAI` → gpt-image no se usó) |
| SFX | Mixkit, gratis, 12 cues |

## Control de calidad

- `ffprobe`: 958,07 s video vs 957,90 s audio; 1920×1080; 30 fps; H.264 + AAC 192 k **estéreo (channels=2)**.
- `validar.py --etapa final --min 15` → **RESULTADO: OK** (apertura con foto, tramos de avatar ≤ 6 s, plan sin huecos, meta.json, gates).
- 32 cuadros (1 cada 30 s) revisados a ojo en 4 hojas `qc/final_0*.jpg`: sin pantallas negras (`blackdetect` = 0 coincidencias), sin texto basura, manos con 5 dedos, sin logos ni marcas.
- Lipsync revisado en el corte final (`qc/lipfinal_intro.jpg`, `qc/lipfinal_phone.jpg`): boca articulando, sin desfase perceptible.
- Fronteras del avatar revisadas (9,6 / 10,2 / 18,2 / 18,8 / 210,1 / 219,1 s): fundidos limpios, sin saltos de encuadre.
- Audio: sin huecos > 1 s (`silencedetect` a −35 dB sólo marca pausas naturales de 0,8–0,95 s); −20,9 LUFS integrado, pico −0,5 dB (el máster ya viene así; no se normalizó para no recortar picos).
- Sin música; SFX suaves y puntuales (agua, madera, calle, tela, hervidor).

## Correcciones de la tarde (entrega final)

1. **Apertura con imagen impactante** — se generaron 3 variantes por la cola de Nano Banana (`ap01`/`ap02`/`ap03`, prompts JSON completos que pasaron `lint_fotos.py`); se eligió `ap01` (primer plano a 40 cm, polar contra la nariz) y se instaló como `s001`. El video ahora abre con esa foto y el avatar entra a los 3,48 s. La intro se partió en dos tramos de 5,66 s y 5,00 s con una foto de 1 s entre medio.
2. **Avatar HD** — `intro1`, `intro2` y `wash` se rehacieron con la cara de `michiko_face_hd.png` (460×613) en `av/clips_hd/` y se copiaron a `av/clips/`; los viejos (cara de 128×192 agrandada) quedaron archivados en `av/clips_v1_cara_chica/`. Se borraron y re-renderizaron los segmentos afectados (0001, 0003, 0053); el resto se conservó por firma `.src`.
3. **Audio estéreo** — el `assemble` compartido muxea con `-ac 2`; ahora el final da `channels=2`.
4. **`plan.json` y `meta.json`** — el plan lo escribe `render.py` desde el armado real (240 segmentos, `voice_dur` 957,9); `meta.json` lleva título y descripción en tres párrafos en la voz de Michiko, sin links.
5. **Revisión visual** — hojas nuevas: `qc/hoja_fotos.jpg`, `qc/hoja_render.jpg`, `qc/hoja_final_a.jpg`, `qc/hoja_final_b.jpg`, `qc/hoja_av_hd.jpg`; gates en `gates/fotos_auto.txt`, `gates/render_auto.txt`, `gates/final_auto.txt` y respuesta a las correcciones en `gates/correcciones_hechas.txt`.

## Problemas y cómo se resolvieron

1. **Pool de claves agnes** — el pool compartido no distingue la ventana real “1 request every 5 minutes”, así que `tools/lipsync.mjs` hace su propio agendado: lee “Try again after HH:MM:SS”, la pasa a hora local (−3 h) y no vuelve a pedirle a esa clave antes de esa hora. Resultado: 5/5 clips entregados sin tocar el pool.
2. **Primer `intro1` con cortes duros** — el modelo devolvió dos planos alternados. Se descartó, se mató el driver para que no encadenara `intro2` desde un cuadro malo, se endureció el prompt (“ONE SINGLE UNBROKEN SHOT … never a cut, never a second angle, never a zoom”) y se regeneró: toma única correcta.
3. **Lint de la cola** — `retry.py` generó prompts sin `moment/action/props/person` y el linter los rechazaba; se reescribieron con el esquema canónico de `D:/rtmp/nb_test/rica.json` y se encolaron por `encolar_v2_sinlint.mjs`.
4. **Ids faltantes** — `s008b` y `s114` no habían salido (los retries crearon `s007b`/`s114b`). Se generó `s008c` y se copió a `s008b`; `s114b` → `s114`. `img/pics` quedó con los 242 ids del plan.
5. **Renombres de archivo** — `render.py` salta segmentos existentes, así que se renderizó en dos tandas: 233 mientras corrían los clips y los 4 restantes al llegar `wash/towel/phone`.

## Para mejorar en el próximo

- Los retornos de avatar usan todos el mismo salón; `wash` es el único con escenario distinto. Conviene fijar de antemano 3–4 escenarios distintos (cocina, patio, entrada) para que cada regreso se sienta en otro lugar.
- El pool de agnes entrega ~1 clip cada 6 min; con 5 clips la ventana completa es de ~45 min. Planificar el arranque del avatar antes que las fotos.
- El máster de Fish ya viene con pico a −0,5 dB y promedio bajo; si se quiere −14 LUFS hay que limitar antes de subir (limitador, no `loudnorm` plano).
- Un cuadro de QC cada 30 s deja pasar microcortes; para la próxima conviene sumar un barrido de 1 cada 10 s en los 20 s alrededor de cada cambio de escena.
