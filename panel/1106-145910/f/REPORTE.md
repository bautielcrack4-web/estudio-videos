# REPORTE · Michiko's Kyoto Closet · "The 7 Pieces A Japanese Woman Over 60 Owns Forever"

**Estado:** final.mp4 entregado (830,0 s). Los 5 tramos de avatar salen con su primer cuadro
fijo hasta que agnes devuelva los clips; cuando lleguen, render.py rehace sólo esos tramos y
assemble.py vuelve a unir (ver "Pendiente").

## Entregables
- `final.mp4`: 1920x1080, H.264 CRF 20, 30 fps, AAC 192k estéreo, 830,004 s = 13 min 50 s,
  344,8 MB. Duración = voz (830,00 s).
- `meta.json`: título + descripción de 3 párrafos (1.453 caracteres), sin links ni hashtags de IA.
- `REPORTE.md`: este archivo.

## Qué hay hecho
- `guion.txt`: 2.101 palabras, 13 min 50 s de voz. Gancho con número + objeto (siete piezas, la
  bolsita de caqui), credencial de la presentadora a los ~50 s, prueba interactiva a los ~4 min,
  los 7 ítems con problema → anécdota (fecha, nombre, lugar) → por qué después de los 60 →
  cambio concreto con precio en dólares → prueba para esa noche. Like/suscribirse antes del
  séptimo; cierre con pregunta para comentarios y gancho del próximo video (Carol en abril).
- `voz/master.wav`: Fish `moda_michiko_ca` con `--keep-tags`, 830,0 s.
- `captions.json`: ASR de Groq por palabra (2.067 palabras con startMs/endMs). Todos los cortes
  están clavados al inicio de la palabra que los motiva.
- `shots_timed.json`: 171 planos contiguos de 0 a 829,7 s, cortes de 3,1 a 6,0 s. Los primeros
  30 s cortan cada 2-3 s (foto de apertura gancho_b en el segundo 0, avatar partido en A1a
  (2,5-7,5) y A1b (9,0-14,5) intercalado con fotos).
- `avatar_ranges.json`: 5 tramos, 42,5 s en total; ninguno pasa de 6 s en los primeros 30 s.
- Fotos: 233 archivos en `fotos/`, todos salidos de la cola compartida de avatarity (Nano
  Banana), prompts JSON completos aprobados por `lint_fotos.py`. 155 ids distintos en el plan;
  varias fotos se reutilizan dos veces con ≥ 2 min de distancia.
- `sfx/` + `cues.json`: 7 sonidos suaves (tela, tijera, llaves, papel, cajón, puerta), ganancia
  0,045-0,06 (≈ -26 dB), sólo en el séptimo ítem y el cierre. Sin música.
- `plan.json`, `segments/` (171 segmentos > 200 KB), `qc/` con 28 cuadros del final cada 30 s.

## Costos
- DeepSeek (guion): **US$ 0** (el guion se escribió en esta sesión, sin API paga).
- Nano Banana (cola avatarity): gratis.
- agnes (avatar): gratis, con cupo diario por cuenta.
- Fish / Groq / Mixkit: gratis.
- gpt-image-2: 73 fotos salieron por la vía de OpenAI de la cola aunque existe la bandera
  `D:/rtmp/SIN_OPENAI`; no lo decidió este chat: la cola compartida despachó esas imágenes por
  ese motor (los archivos llegaron como `.png`). No se hizo ninguna llamada directa a OpenAI ni
  se pagó nada desde acá.

## Problemas y cómo se resolvieron
- **Falsos positivos de CONTENT_POLICY (`CSAM_MINOR_SAFETY`)** con prompts domésticos que
  nombraban edad o partes del cuerpo ("mujer de sesenta y ocho", "el cuello", "el pecho"). Se
  reescribieron diez fotos en tono objeto-primero (`_r`, `_r2`) y se reencolaron: `p1e_luz_r`,
  `p1k_medir_r`, `p1b_vieja_r2`, `p6g_banda_r`, `p7a_seda_r`, `c_fumiko_r`, `q02_cuello_r`,
  `h02_cinta_r`, `h07_percha_r`, `i_tatami_dia_r`.
- **72 fotos "faltaban" aunque la cola las daba por hechas**: el motor de OpenAI las guardó como
  `.png` y render.py busca `<id>.jpg`. Se convirtieron todas con ffmpeg (`-q:v 2`), sin tocar la
  herramienta compartida.
- **8 segmentos del render salieron de 0-262 bytes** por contención de CPU con x264 (seis hojas
  de contacto en paralelo). Se volvió a correr render.py con un solo hilo para esos tramos: los
  171 quedaron > 200 KB. No se editó nada de `D:/rtmp/dspanel/tools/`.
- **El plan de avatar tenía un tramo de 14,6 s** (fuera del rango 4-12 s de agnes); se partió en
  A1a + A1b con `chain` y va en pedazos en la intro.
- **`avatar.mjs` murió dos veces por `EPERM` al renombrar `D:/rtmp/agnes_pool/state.json`**
  (el archivo de estado lo comparten los ~10 videos en paralelo). No es un bug del video: se
  relanzó y quedó un supervisor (`supervise_avatar.sh`) que lo vuelve a lanzar hasta que estén
  los cinco clips; la herramienta saltea lo que ya existe.
- **El primer `assemble.py` no llegó a terminar** porque el turno del panel se cortó a mitad de
  camino; se relanzó y terminó bien (los tramos ya hechos se reutilizan).

## Pendiente
- Clips de avatar A1a/A1b/A2/A3/A4: la cola global de agnes está saturada
  (`video_queue_full`): ~1.000 rechazos por hora y **cero** envíos aceptados entre todos los
  videos en paralelo, con 24 claves además marcadas `banned` por el límite diario. No es un
  problema de este video ni se saltea la cola: `avatar.mjs` reintentó 2 h seguidas (hasta las
  21:17, cuando el supervisor se detuvo por su límite de tiempo) sin un solo clip. Mientras
  tanto los 5 tramos van con su primer cuadro y movimiento Ken Burns (no son cuadros congelados).
  Al llegar: `python D:/rtmp/dspanel/tools/render.py D:/rtmp/mk09ds` (rehace sólo esos 5 tramos)
  y `python D:/rtmp/dspanel/tools/assemble.py D:/rtmp/mk09ds`. Revisar que la boca siga al audio.

## Mejoras para la próxima
- Escribir los prompts de foto sin ninguna referencia a edad, parentesco ni partes del cuerpo:
  ahorra los diez rebotes de CONTENT_POLICY y ~40 min de cola.
- Que la cola de avatarity convierta a `.jpg` en el destino: hoy el `.png` de OpenAI rompe el
  render sin avisar.
- Lanzar el render cuando no haya hojas de contacto corriendo, o con `--limit` por tandas: los
  segmentos de 262 bytes son todos del mismo minuto de contención.
- Pedir el avatar en el primer minuto (la voz y la cara ya están) y no al final: agnes es el
  cuello de botella real.
