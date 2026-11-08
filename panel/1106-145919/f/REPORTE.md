# REPORTE · mk12ds

**Canal:** Michiko's Kyoto Closet
**Título:** Why Japanese Women Over 60 Never Wear Perfume (And Still Smell Clean)
**Idioma:** inglés · **Duración:** 1005,2 s (16:45) · **Formato:** 1920x1080 30 fps H.264 CRF 20,
AAC 192k estéreo (44,1 kHz) · **Tamaño:** 416 MB
**Música:** ninguna (la biblia la prohíbe) · **Archivo:** `final.mp4`

---

## Lo que se hizo

- **Guion** (`guion.txt`): 2580 palabras, gancho con número y objeto ("nine bottles of perfume"),
  credencial temprana (Fumiko, kitsuke-shi en Gion cuarenta años; Carol en Sacramento; diecinueve
  años en Sunnyvale), diez puntos con problema → anécdota fechada → por qué → cambio concreto con
  precio en dólares → comprobación para esa noche, prueba interactiva de la puerta de los dos
  minutos en el minuto ~4, like/subscribe antes del punto 9, cierre con pregunta a comentarios,
  el tansu de Fumiko y el gancho al mk06 (el bidón amarillo de la lavandería de Sunnyvale).
  Sin "old" para personas, sin consejo médico, sin marcar el contenido como IA.
- **Voz** (`voz/master.wav`, 1005,04 s): Fish, voz `moda_michiko_ca`, con tags de emoción
  (`--keep-tags`). Transcripción por palabra con Groq (`captions.json`) y de ahí se clavó cada
  corte en el `startMs` de la palabra que lo motiva.
- **Avatar** (`avatar/`): agnes-video-2.5-flash, modo reference, con `michiko_face_hd.png`.
  Cinco tramos en pantalla, 37,3 s en total: dos pedazos de la intro (2,52-7,0 s y 10,44-13,85 s,
  los dos del mismo clip A1 para que la cara y la luz no cambien), un regreso a los 118,2 s,
  otro a los 609 s y otro a los 936 s. Se generaron 44,8 s de clip (A1 12,3 s · A2 11,6 s ·
  A3 11,6 s · A4 9,4 s); lo que sobra queda fuera del corte. Cuatro escenas distintas, primeros
  cuadros de Nano Banana con la referencia del presentador.
- **Fotos de b-roll** (`fotos/`): 203 archivos de Nano Banana por la cola de avatarity
  (210 pedidos en total, contando los 3 ganchos, los 7 primeros cuadros del avatar y un b03 que
  no entró en el corte). 196 fotos se usan en el video; las otras 6 quedan debajo de los tramos
  del avatar. Todos los prompts son JSON con los diez campos (`moment`, `action`, `props`…),
  pasaron el linter y quedaron en `pedidos_01..10.json`.
- **Sonido** (`sfx/`): 7 efectos de Mixkit mezclados bajos (ganancia 0,04-0,06) en momentos
  puntuales (`cues.json`): cajón, agua, baño, tela, vapor, papel y el segundo cajón.
- **Armado**: `render.py` (Ken Burns sorteado por foto, 3840x2160 antes del zoompan, fundidos
  0,6 s avatar / 0,3 s foto) + `assemble.py` (9 tramos con xfade, voz, SFX). `plan.json` lo
  escribió render.py: 201 segmentos (196 foto + 5 avatar), 0 huecos, arranca con foto en t=0.

## Puntos de control

| etapa | validador | revisión propia | pedido |
|---|---|---|---|
| guion | OK | `gates/guion_auto.txt` | `gates/guion_pedido.txt` |
| fotos | OK (203 fotos, 0 fuera de Nano Banana) | `gates/fotos_auto.txt` (18 hojas, 202 fotos) | `gates/fotos_pedido.txt` |
| render | OK (10/10 ✓) | `gates/render_auto.txt` | `gates/render_pedido.txt` |
| final | OK (16/16 ✓) | `gates/final_auto.txt` | `gates/final_pedido.txt` |

`gates/correcciones.txt`: vacío. No hubo correcciones del revisor; `gates/correcciones_hechas.txt`
lo deja anotado.

## Costos

- OpenAI / gpt-image: **US$ 0** (`D:/rtmp/SIN_OPENAI` presente; no se tocó).
- agnes: sólo el avatar, 44,8 s generados dentro del cupo de las cuentas Starter; sin gasto en
  dólares.
- Nano Banana / veo: cola compartida de avatarity, sin gasto en dólares.
- DeepSeek: este chat no expone contador de gasto; no hay cifra medible desde acá.

## Problemas

1. **`clipStartMs` mal puesto** en `avatar_ranges.json`: con el valor 0, render.py le pasaba a
   ffmpeg un `-ss` de 118/609/936 s sobre clips de 9-12 s y salían mp4 de 262 bytes; además los
   dos tramos de A1 arrancaban 2,52 s tarde. Se corrigió a "segundo de la voz donde arranca cada
   clip" y se rehizo sólo esos cinco segmentos (`gates/render_auto.txt`, 16:05).
2. **`assemble.py` se murió una vez con el log en 0 bytes** (stdout buffereado). Se relanzó con
   `python -u` y terminó bien. Vale para cualquier corrida larga.
3. **Contención del `state.json` de agnes_pool** (EPERM/UNKNOWN al renombrar) por los ~10 videos
   en paralelo; la propia librería reintentó y los cuatro clips salieron. No afectó la entrega.
4. **La cola de imágenes** marcó ~40 pedidos pendientes durante varias horas (compartida con el
   resto de los videos). Se avanzó el guion, el avatar y el render parcial mientras tanto; no se
   salteó la cola ni se tocó nada ajeno.
5. El primer `final.mp4` de prueba duraba 1005 s pero el video sólo ~751 s: era el hueco de las
   fotos que todavía no habían llegado. Con las 202 fotos el render completo cerró sin huecos.

## Qué mejoraría

- Guardar el prompt de cada foto también como `fotos/<id>.json` además de los `pedidos_*.json`
  (el validador lo acepta igual, pero queda más cómodo para retocar una sola).
- Programar el render completo apenas entre la última foto: hoy la cola marca 0 pendientes y las
  fotos siguen bajando un rato, así que hubo que esperar a que el contador de archivos coincidiera
  con el plan.
- Para la próxima, poner el `clipStartMs` desde el minuto uno: es el único bug que costó un
  re-render de avatar.
