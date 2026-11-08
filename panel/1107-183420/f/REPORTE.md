# REPORTE · fe11ds

**Video:** fe11 · "Después de enterrar a 6.000 personas, esto es lo que quiero en mi propio funeral"
**Canal:** Don Ernesto, el Funerario (ES)
**Duración:** 1619,94 s (27:00) — audio maestro `voz/master.wav`
**Salida:** `final.mp4` 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192k estéreo · **753,6 MB · 1619,944 s**
(ffprobe: video 1619,933 s / audio 1619,944 s → desfase 0,011 s; bitrate 3,72 Mbps)

## Qué se hizo

1. **Guion** (`guion.txt`, 4.298 palabras): gancho con el número 6.000 + el sobre amarillo como objeto +
   credencial de funerario; 12 líneas con problema → anécdota fechada y situada (Guadalajara, marzo 2019)
   → porqué → cambio concreto con precio → chequeo de esta noche; like/suscribirse después de la línea 10;
   cierre con pregunta para comentarios y gancho a fe12 ("Abrí una tumba después de 10 años").
2. **Voz**: Fish, voz `ernesto_es`, 3 bloques en paralelo → `voz/master.wav` (1619,94 s).
3. **Transcripción**: Groq ASR por palabra (`captions.json`, última palabra 1.619.118 ms) → todos los cortes
   clavados en la palabra que los motiva.
4. **Fotos**: 230 archivos en `fotos/` (189 PNG de Nano Banana por la cola de avatarity + 41 JPG del desvío
   automático gpt-image-2 en quality low). Todas con prompt JSON completo y linter `lint_fotos.py` OK.
   6 fotos de prueba primero, hoja de contacto, y después el lote. Revisión visual con Read en 9 hojas de
   contacto (H, K/L, M/N, N×2, P×2, S, T×2): 0 rechazos.
5. **Avatar**: InfiniteTalk, **1 sola llamada** (`tools/avatar_it.py`), 125 ventanas (A0–A124),
   reel de 499,92 s, **US$ 0,25**, 61 min de ejecución, 0 descuadres (corrección de lag medida por correlación
   de audio). Estilo Bertha: 463 s con avatar = 29 % del video, ventanas de 3–6 s, nunca >20 s sin avatar.
6. **Render**: 474 segmentos (`render.py`, Ken Burns al azar con semilla fija, 3840x2160 antes de zoompan,
   xfade 0,6 s avatar / 0,3 s foto, saturación 0,92). `plan.json` escrito por la herramienta.
7. **Armado**: `assemble.py` (tramos de 25 con xfade → video sin audio → mezcla de voz + SFX → mux final).
   La herramienta compartida falló 3 veces seguidas en esta máquina (memoria con 25 decodificadores y luego
   disco lleno por las otras pestañas), así que se usó el reemplazo local `ensamblar.py`: **misma matemática de
   xfades y mismos ajustes de calidad** (tramos CRF 14 veryfast → unión CRF 20 medium → mux `-c copy` con voz
   + SFX), con `-threads 2` por entrada, reanudable (los 19 tramos quedan en `xf2/`) y escritura en `C:` para
   no depender del disco `D:` que quedó al 100 % libre. El `final.mp4` se entrega en `D:/rtmp/fe11ds/`.
   La unión de los 19 tramos salió en una sola pasada (2346 s → `video_noaudio.mp4`, 714,2 MB, 1619,933 s).
   El proceso murió justo al arrancar la mezcla de audio (dejó `audio_mix.m4a` truncado en 1,57 MB); se rehízo
   sólo esa parte con `audio_mux.py`: voz + 8 SFX a 48 kHz estéreo (169 s), mux `-c copy` con `+faststart`
   y copia a `D:/rtmp/fe11ds/final.mp4` (753,6 MB · 1619,944 s).
8. **SFX**: 8 cues (`cues.json`), ganancias 0,04–0,055 (bajos, sólo en momentos puntuales).
   **Sin música**: no se usó música de fondo en ningún tramo (decisión del brief).
9. **Meta**: `meta.json` con título y descripción de YouTube en 3 párrafos, voz del presentador,
   sin enlaces y sin hashtags de IA.

## Costos

- Avatar InfiniteTalk: **US$ 0,25** (1 llamada /run).
- Fotos Nano Banana / gpt-image-2: por la cola compartida, sin costo directo.
- Fish, Groq, Mixkit: gratis.
- DeepSeek (redacción/planificación): sin facturación medible desde esta sesión.

## Cambio del creador aplicado (avatar)

El primer cuadro del avatar es **directo** `D:/rtmp/funerario/refs/ernesto_av.png` (foto de ChatGPT web),
no una generación de Nano Banana:

- `avatar_ranges.json` → primera ventana con `"frame": "D:/rtmp/funerario/refs/ernesto_av.png"`.
- `avatar/frames/a1.jpg` regenerado desde ese PNG (`-q:v 1`, 227 KB) para que la foto fija de respaldo sea la misma.
- La llamada de InfiniteTalk ya había usado ese PNG como `FRAME_AVATAR` (BRIEF.md), así que los 125 clips y
  la foto fija son coherentes. **No se hizo una segunda llamada al avatar.**

## Problemas y cómo se resolvieron

- **Cola de fotos quedó en 0 pendientes con 37 fotos faltantes** (K10–K15, L01–L10, M01–M13, N01–N09): el slug
  `fe11ds` había llegado al tope de 150 imágenes y los lotes nunca se encolaron. Se armó `pedidos_b6.json` con
  esos 37 ids y se encoló en `fe11ds` + `fe11ds_b`. Llegaron todas; ninguna sección quedó con relleno.
- **9 segmentos fallaron con libx264 (-22)** y otros 9 con "Cannot allocate memory" (-12) por la carga de los
  ~10 chats en paralelo: se borraron los mp4 de 0 bytes y se re-corrió `render.py`, que rehace sólo los que
  faltan. 474/474 segmentos válidos.
- **`assemble.py` falló 3 veces** (25 decodificadores 1080p en paralelo → `-1145393733` / `-12` memoria; después
  `-28` disco lleno por las otras pestañas): se reemplazó por `ensamblar.py` (misma matemática de xfades, misma
  calidad, `-threads 2` por entrada, reanudable). Sacó los 19 tramos y la unión completa (2346 s).
- **El proceso de armado murió al arrancar la mezcla de audio** (quedó `audio_mix.m4a` truncado en 1,57 MB y
  el `video_noaudio.mp4` intacto). Se rehízo sólo esa parte con `audio_mux.py`: voz + 8 SFX (169 s), mux
  `-c copy` con `+faststart` y copia a `D:/rtmp/fe11ds/final.mp4`.
- **Disco `D:` llegó a 0,03 GB libres** por las ~10 pestañas en paralelo: los intermedios se escribieron en `C:`
  y se liberaron los temporales antes de copiar el final.
- **`avatar/it_sync.json` se perdió** por un bloqueo de archivo de Windows al terminar la llamada; los 125 clips
  igual se cortaron con la corrección de lag medida (0 descuadres informados por la herramienta).
- Encuadre de apertura: se mantuvo el plano de oficina completa (set fijo estilo Bertha) porque da contexto y
  la boca arranca sincronizada desde el segundo 0.

## Cambio del creador aplicado (render en GitHub, 8-nov)

El creador movió el render a GitHub (14 máquinas en paralelo, final en la nube, sin bajar nada a la PC) y
cortó el armado local. Este video **no se rehizo**: ya tenía un `final.mp4` bueno y terminado (753,6 MB ·
1619,944 s · 1080p30) validado con `validar.py --etapa final` → OK, y la regla del creador es que en ese caso
sigue valiendo. De acá en adelante `ensamblar.py` y `audio_mux.py` quedan sin uso: no se renderiza ni se une
video en la PC.

## Revisión visual del final

54 cuadros, uno cada 30 s (`qc/c30_*.jpg`, hojas `qc/hoja_f1..f5.jpg`), revisados con Read:
apertura con el clip real del avatar desde el 0; fundidos limpios; fotos con texto legible y bien escrito
(lista de precios $6.500–$24.000, lápida "MARIA INES ORTIZ 1912-1978", notepad, fachada 2643);
sin marcas de agua, fecha impresa, texto inventado roto, cuerpos, caras de moribundos, sangre, tubos ni agujas;
ninguna foto repetida seguida; sin huecos negros.

`validar.py --etapa final --min 25` → **RESULTADO: OK** (sin ✗). Dos avisos `!` documentados:
`avatar/it_sync.json` perdido (lag ya medido y corregido en los 125 clips) y la revisión visual (hecha arriba).

## Pendiente / mejoras

- Ninguna sección quedó con fotos repetidas por falta de material (todas al 100 %).
- Para próximos videos: encolar las fotos por lotes de ≤40 ids y verificar el conteo por sección antes de dar
  la cola por terminada (el estado global "0 pendientes" no garantiza que todos los ids se hayan pedido).
