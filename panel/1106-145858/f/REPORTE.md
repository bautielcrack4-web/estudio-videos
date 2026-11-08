# REPORTE — mk15ds · "I Tried 5 Glasses at a Kyoto Optician at 68 — These Took Years Off My Face"

Actualizado: 2026-11-06 19:35 · video terminado

## Qué se hizo

- **Guion** (`guion.txt`, 2.561 palabras del validador, ~15,6 min): hook con el número + el objeto + el "no es por verme más flaca" + loop al último par; credencial de Fumiko (kitsuke-shi, 19 años en Sunnyvale) a los ~50 s; los cinco pares con problema → anécdota con nombre y lugar → por qué recién después de los 60 → cambio concreto con precio en US$ → chequeo en el espejo esa noche; test interactivo en el minuto 4 con ✗/✓ en pantalla; like/subscribe antes del último par; cierre con "no compren, abran el clóset" + frase de Fumiko + pregunta para comentarios + gancho a mk03 (blusa leopardo, poliéster). Sin la palabra "old", sin música, precios en dólares, temperatura en °F.
- **Voz** (`voz/master.wav`, 937,605 s): Fish TTS, voz `moda_michiko_ca`, por bloques con master único.
- **Tiempos** (`captions.json`, 2.507 palabras): transcripción por palabra con Groq; el último `endMs` cae en 937.464 ms, así que imagen y voz cierran a la par. Cada plano arranca en el `startMs` de la palabra que lo motiva.
- **Avatar** (agnes lipsync, modo reference, cara `michiko_face_hd.png`): A2, A3, A4 y A5 listos y en el corte final. La intro va partida en A1a + A1b por el tope de 12 s por clip de agnes; ver "Problemas".
- **Fotos de b-roll**: 162 fotos en `fotos/`, todas pedidas a la cola de avatarity (Nano Banana) con prompt JSON completo (`moment`, `action`, `props` de 6 a 10 objetos, cámara variada, `avoid` con fecha/sello/marca) y aprobadas por el linter `lint_fotos.py` en 8 tandas. Ninguna con fecha impresa, texto legible inventado, manos rotas ni look de publicidad: se revisaron a ojo con hojas de contacto de 12, las últimas 41 en `qc/hoja_rev1–4.jpg`.
- **Armado**: 180 planos (164 de b-roll + 16 tramos de avatar), 2,0–6,4 s por plano; movimiento Ken Burns aleatorio (tipo, intensidad y foco sorteados por foto, semilla fija 20261106); fundidos de 0,6 s avatar↔foto y 0,3 s foto↔foto; SFX de Mixkit bajos en cuatro momentos puntuales. Render y armado con las herramientas compartidas `render.py` / `assemble.py`.
- **Final** (`final.mp4`): 1920×1080, 30 fps, H.264 CRF 20, AAC 192k estéreo, 937,6 s; duración igual a la voz (±0,3 s). Segundo 0 = foto del ojo tras la montura (`gancho_c`), nunca el avatar.

## Costos

- **US$ 0.** Todo salió por las vías gratuitas: Fish, Groq free, agnes (cupo diario), cola de avatarity (Nano Banana) y Mixkit. No se usó gpt-image ni Veo.

## Problemas y cómo se resolvieron

1. **`t01_tienda` rechazada por la cola** con `CONTENT_POLICY_VIOLATION` (el prompt juntaba "niño/joven" con contenido sugerente). No se reintentó: el plano se cubre con `t01b_tienda`, la variante ya generada del mismo momento.
2. **agnes tiene tope de 12 s por clip.** La intro se partió en A1a + A1b encadenados (A1b arranca en el último cuadro de A1a). **A1a/A1b nunca llegaron**: pasaron más de 4 h en cola sin cupo (otros ~10 videos comparten las claves). Para no frenar el video, los dos tramos de la intro usan el primer cuadro del avatar (`avatar/frames/a1_cocina.jpg`) como foto fija. El lipsync de A2–A5 sí está. Si A1a/A1b aparecen, `render.py` + `assemble.py` rehacen sólo esos dos tramos.
3. **Fotos que todavía no llegaban.** `tools/fix_shots.py` sustituyó en su momento cada foto ausente por la más parecida (coseno IDF, con penalización por repetición y adyacencia) leyendo el plan semántico `qc/shots_full.json`. Al drenar la cola llegaron las 162 y quedan sólo 3 planos con la foto sustituta.
4. **Fotos repetidas cerca.** En la primera versión del final aparecían la misma foto del sastre a los 549 s y 644 s, `k02` en dos planos consecutivos (417/422 s) y `y03` cinco veces. Se escribió `tools/diversify.py`: reasigna la foto repetida por la más afín al texto del plano que no se haya visto en 180 s ni en el plano anterior. **15 cambios**, sin repeticiones dentro de 180 s; se re-renderizaron sólo esos 15 segmentos (3,5–6,4 s, todos validados con ffprobe) y se re-armó.
5. **Segmentos corruptos por presión de memoria.** Bajo la carga de ~10 videos en paralelo, libx264 dejó 5 segmentos con 0 o 262 bytes (`0002`, `0016`, `0150`, `0154`, `0171`). `tools/check_segs.py` los detectó, se borraron con su `.src` y `render.py` los rehízo; el final se armó con los 186 segmentos válidos.
6. **Dos instancias de `assemble.py` a la vez** corrompieron los tramos intermedios (`moov atom not found`, `Device or resource busy`). Se mataron los procesos, se borraron `xf_tmp/`, `video_noaudio.mp4`, `audio_mix.m4a` y `final.mp4`, y se relanzó una sola instancia limpia.
7. **Esperas de la cola de agnes.** Cada clip tardó entre 7 y 8 minutos y A1a quedó trabado en la espera de cupo. La herramienta espera sola y no pierde el pedido; mientras tanto se siguió con fotos, SFX y armado.

## Qué falta

- Nada para entregar: `final.mp4` (422.648.783 bytes), `meta.json` y este reporte están completos y `validar.py --etapa final --min 15` dio **RESULTADO: OK** (guion 2.561 palabras, 162 fotos limpias, plan sin huecos, apertura con foto, avatar 49 s, 1920x1080, 30 fps, 937,61 s vs voz 937,60 s, meta y reporte).
- Opcional si aparece el cupo: A1a/A1b → re-render de los dos tramos de la intro → re-armado (el resto no se toca). Los procesos de `avatar.mjs` quedan vivos esperando; la próxima clave de agnes se libera a las 21:07.
- Audio: media −24,3 dB, pico −3,8 dB, ningún silencio de más de 3 s.
- Gates: `gates/final_auto.txt` + `gates/final_pedido.txt` escritos; no había `gates/correcciones.txt`.
