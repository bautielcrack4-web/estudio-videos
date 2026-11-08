# REPORTE — Lo que pasa en un velorio mexicano que en Estados Unidos no te dejan hacer

Canal: Don Ernesto, el Funerario (ES) · Carpeta: `D:/rtmp/fe07ds` · Entrega: `final.mp4` + `meta.json`

## Entregado
- **`final.mp4`** — 1920×1080 · 30 fps · H.264 CRF 20 · AAC 192 kbps estéreo 44,1 kHz · **1639,8 s (27:20)** · 649 MB.
  Duración del video = duración de la voz (Δ 4 ms). Sin música: sólo voz y SFX suaves.
- **`meta.json`** — título + descripción de 3 párrafos en la voz de Don Ernesto, sin links ni hashtags de IA.

## Estado
- Guion: `guion.txt`, 4203 palabras, hook con número y objeto, prueba interactiva, cierre con pregunta y gancho al video del crematorio.
- Voz: Fish `ernesto_es` con 2 tags de emoción, master en `voz/master.wav` (1639,83 s).
- Tiempos: Groq ASR palabra por palabra en `captions.json`; todos los cortes van clavados a esas palabras.
- Avatar: InfiniteTalk, **una sola llamada** (`avatar_it.py`, US$ 0,25). 135 ventanas, **491 s = 30 % del video**,
  de 3-6 s cada ~11-13 s, nunca más de 20 s sin avatar. Desfase del reel de RunPod medido y corregido (máx 395 ms).
  Arranca con Ernesto hablando a cámara desde el segundo 0.
- Fotos: 265 archivos en `fotos/` (275 pedidas por la cola de avatarity — 259 del plan + pruebas y variantes).
  Todas salieron de la cola (Nano Banana / desvío gpt-image-2), todas con prompt JSON completo.
  Revisadas por hojas de contacto de 12: se repidieron las que traían fecha impresa, texto inventado o manos raras.
  Quedaron dos flojas (g02: escritorio con café; p4_11) que aguantan los 4 s que duran en pantalla.
- Segmentos: 405 en `segments/` (Ken Burns 4K→1080 con movimiento sorteado sin patrón), 49.195 cuadros.
- SFX: 7 sonidos de Mixkit en `sfx/` + `cues.json` (0,035-0,08 de ganancia), mezclados bajos en
  los segundos 80,9 / 184,8 / 221,0 / 476,0 / 732,7 / 1061,2 / 1152,0.
- Gates: los 4 puntos de control escritos en `gates/` (guion, fotos, render, final). No apareció
  `gates/correcciones.txt` en ninguno.

## Costos
- Avatar InfiniteTalk (RunPod): **US$ 0,25** (1 llamada).
- DeepSeek (guion, prompts, revisión): sin medidor local de consumo; por tokens de la sesión, estimado **< US$ 0,20**.
- Fotos, voz, transcripción, SFX, render: **gratis** (colas compartidas, Mixkit, render en GitHub Actions).

## Música
Sin música. El piano de la Biblioteca de Audio de YouTube no se puede bajar desde el Estudio de YouTube,
así que el video va sólo con voz y SFX suaves.

## Problemas (y cómo se resolvieron)
1. **Disco D: al 100 %** (932 GB, unos 10 videos en paralelo). El armado local murió dos veces por
   `No space left on device` y otra por falta de RAM en `assemble.py` (tramo 12).
   → Liberé sólo mis intermedios (bloques de voz ya unidos, tramos truncados) y terminé el render por el
   camino en la nube de `render.py`/`assemble.py` (GitHub Actions): 405 segmentos en 26 tandas, 4,8 min,
   y el armado final completo. `finish_assemble.py` quedó escrito como reemplazo local por si la nube fallaba; no hizo falta.
2. **Una corrida de nube quedó colgada** ("1 trabajando" durante 27 min). La cancelé y relancé: la segunda
   terminó 27/27 sin problema. Los segmentos ya subidos se reutilizaron ("394 ya estaban en GitHub").
3. **Borré de más 55 segmentos** en una limpieza apurada por el disco lleno; se rehicieron todos.
4. **Groq ASR se corrió en `en`**: los tiempos por palabra son exactos (±50 ms) pero el texto de
   `captions.json` es fonético en varios tramos. No afecta al video (sólo se usaron los tiempos), pero
   si se quisiera hacer subtítulos habría que re-transcribir en `es`.
5. **Avatar**: los 135 clips tardaron en cola de RunPod; mientras tanto el render usaba el cuadro fijo a1.
   Cuando llegaron se re-renderizaron los segmentos de avatar; el ✗ del punto de control de render quedó resuelto
   y el validador final confirma que **todos** los tramos de avatar son clips reales.

## Qué mejorar
- Empezar con el disco revisado y todos los intermedios afuera de D: (los segmentos a 4K son lo que más pesa).
- No borrar `segments/` hasta tener `final.mp4` verificado: el render es lo que más tiempo cuesta.
- Correr Groq con `es` desde el principio para poder sacar subtítulos sin re-transcribir.
- Las fotos g02 y p4_11 se pueden repedir en una próxima pasada; son planos de apoyo, no cuentan nada nuevo.
- Probar el avatar antes de cerrar el plan de ventanas (si se corre `avatar_it.py` con el plan abierto, las
  ventanas nuevas ya no pueden ir con clip).

## Cambio del creador (8-nov): primer cuadro del avatar = foto de ChatGPT web
- Pedido: la primera ventana de `avatar_ranges.json` usa como `frame` directo `D:/rtmp/funerario/refs/ernesto_av.png`.
- Hecho: la ventana A0 (0–7,54 s) ya apunta a esa ruta. Copia de resguardo en `avatar/frames/ernesto_av.png`.
- Verificación: `avatar/frames/a1.jpg` (la que usó el generador de avatar) es esa misma foto re-encodeada —
  1672×941, diferencia media 0,36/255. El primer cuadro de `avatar/A0.mp4` es la misma escena, persona, ropa y pose.
  O sea: los 135 clips ya salieron de esa foto, no de una imagen de Nano Banana.
- Ojo: la llamada única del avatar ya se consumió (`avatar/it_llamada.json` = ok, reel 531 s), así que la foto
  de referencia no se puede reemplazar sin repetir la llamada. No hizo falta: el contenido coincide.
- `final.mp4` no se rehizo: el campo `frame` sólo se usa como relleno si falta un clip, y los 135 existen.
