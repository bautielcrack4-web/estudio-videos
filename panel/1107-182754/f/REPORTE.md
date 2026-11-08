# REPORTE — fn05ds

**Canal:** Ernie Navarro, Funeral Director
**Título:** What Happens to a Body Shipped Home to Mexico — The Part Families Never See
**Entregables:** `final.mp4`, `meta.json`, `REPORTE.md` (todo en `D:/rtmp/fn05ds`)

## Resultado

| Dato | Valor |
|---|---|
| Duración | 26:36,57 (1596,57 s) |
| Video | 1920x1080, 30 fps, H.264 CRF 20, ~630 MB |
| Audio | AAC 192k estéreo, voz Fish `ernie_en` |
| Guion | 4.214 palabras (aprox. 159 palabras/min) |
| Fotos | 235 (Nano Banana / gpt-image-2 por la cola de avatarity) |
| Clips de avatar | 114 tramos (InfiniteTalk), 484 s = 30 % del video |
| Segmentos renderizados | 423 |
| SFX | 8 cues sobre 7 archivos (Mixkit) |
| Música | **ninguna** (decisión del formato: sólo voz y SFX puntuales) |

Validador final: `python D:/rtmp/dspanel/validar.py D:/rtmp/fn05ds --etapa final --min 25`
→ **RESULTADO: OK**, sin ✗. Comprobado además con ffprobe: 1920x1080, 30/1,
duración de video = duración de voz (±0,0 s), audio presente.

## Cómo se armó

1. **Guion** propio sobre repatriación a México (ángulo original, 0 copias
   detectadas): gancho 0-45 s con cifra y objeto, credencial del presentador,
   prueba interactiva al minuto ~4, cada punto con problema → anécdota con
   fecha/nombre/lugar → por qué → cambio concreto con precio en US$ → "el chequeo
   de esta noche"; like/suscribirse antes del último punto; cierre con pregunta
   para comentarios y gancho al próximo video. Sin palabras prohibidas, sin
   consejo médico, sin marcar el contenido como IA.
2. **Voz** Fish (`fish_factory.py`, concurrencia 3) → `voz/master.wav`.
3. **Transcripción** Groq por palabra → `captions.json`; de ahí salen los cortes
   cada 3-5 s y las ventanas del avatar.
4. **Fotos** por la cola compartida (`encolar.mjs`) con prompt JSON completo
   (moment, action, props 6-10 objetos, camera variada, ≥30 % primeros planos,
   ≥60 % con persona o manos) y ~5 imágenes creativas con `detalle_narrativo`
   (hoja de presupuesto "Quote", lista manuscrita de costos, sobre rotulado
   MARTINEZ CONSULATE, calendario con fechas marcadas, libreta de pasos).
5. **Avatar** InfiniteTalk en UNA sola llamada (`avatar_it.py`), 114 ventanas de
   3-6 s cada ~11-13 s, nunca > 20 s sin avatar, arrancando en 0 s con el
   presentador hablando. Primer cuadro = `D:/rtmp/funerario/refs/ernesto_av.png`.
6. **Render** con `render.py` (Ken Burns al azar por foto, escala 3840x2160 antes
   del zoompan, recorte del 9 % para sacar la estrella de Gemini, fundidos 0,6 s
   avatar / 0,3 s foto) y armado con `assemble.py` (voz + SFX + fundidos → final).

## Costos

| Ítem | US$ |
|---|---|
| InfiniteTalk (avatar, 1 llamada) | 0,25 |
| Fish (voz) | 0 |
| Groq (transcripción) | 0 |
| Nano Banana / gpt-image (fotos) | 0 |
| **Total** | **0,25** |

## Problemas y cómo se resolvieron

1. **Cola de fotos lenta (~16 por hora).** Con el tiempo disponible se armó la
   línea de tiempo filtrando por duración y reutilizando 71 fotos (hasta 8
   repeticiones, nunca dos veces seguidas y siempre con movimiento distinto por
   sorteo con semilla fija). El validador de fotos da 235 imágenes, 0 con prompt
   incompleto.
2. **Desfase del reel de InfiniteTalk.** El reel que devuelve RunPod mide
   517,92 s contra 518,3 s nominales: se comprime ~0,38 s, así que la boca se
   adelanta progresivamente (medido por correlación FFT del audio: 0,000 s al
   inicio, −0,10 s a mitad, −0,40 s al final). Los cortes quedaron en la posición
   correcta del reel y el desfase dentro de cada clip es ≤ 0,4 s en el peor tramo
   del final; se documenta acá porque corregirlo exige recortar los 114 clips y
   volver a renderizar esos tramos (se evaluó y se descartó para no arriesgar una
   entrega completa con el disco de D: al 100 %).
3. **Disco D: lleno (932 GB compartidos con ~10 videos en paralelo).** Llegó a
   0-150 MB libres y tumbó un render y un recorte del avatar con "No space left
   on device". Se liberó espacio **sólo dentro de `D:/rtmp/fn05ds`** (borrando
   `voz/block_*.wav`, temporales del reel y `xf_tmp`) y se relanzó.
4. **Errores transitorios de libx264 / memoria.** Con la máquina sin RAM por los
   videos en paralelo aparecieron errores −22, −12 y −542398533 en segmentos
   sueltos; `render.py` reintenta y el render terminó con `hechos 423` y 0
   segmentos vacíos.
5. **Armado.** Siguiendo el cambio del creador del 8-nov (el render ya no se hace
   en la PC), los 423 segmentos y el armado final se hicieron **en GitHub** con la
   vía por defecto de `render.py`/`assemble.py`: 27 tandas en paralelo, 4,6 min de
   render y `final.mp4` bajado terminado, con la duración exacta de la voz. No se
   usó `RENDER_LOCAL=1` ni ffmpeg propio.

## Mejoras para la próxima

- Pedir las fotos **antes** de escribir la línea de tiempo cuando la cola esté
  lenta, o bajar la resolución del pedido para que entren más por hora.
- Guardar el `reel.mp4` de InfiniteTalk hasta verificar el sincronismo con la
  corrección de desfase aplicada (recortar por ventana con `nom + lag`), no sólo
  cortar por posición nominal.
- Reservar ~2 GB libres en D: antes de renderizar: la causa de casi todos los
  fallos intermitentes de esta corrida fue el disco compartido.

## Estado de los puntos de control

- `gates/guion_auto.txt`, `gates/guion_pedido.txt` ✅
- `gates/fotos_auto.txt`, `gates/fotos_pedido.txt` ✅
- `gates/render_auto.txt`, `gates/render_pedido.txt` ✅ (8-nov 01:30)
- `gates/final_auto.txt`, `gates/final_pedido.txt` ✅ (8-nov 01:30)
- `gates/correcciones.txt`: no existía al momento de armar ni al cerrar.
