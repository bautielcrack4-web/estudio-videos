# REPORTE — hr07ds · «The Quiet Goodbyes Aging Parents Start Saying in Their Last Year — A Hospice Chaplain Explains»

Canal: Hospice Chaplain Rosa · 2026-11-07 · carpeta `D:/rtmp/hr07ds`

## Qué se hizo

| Etapa | Estado |
|---|---|
| Guion | `guion.txt` · 5.155 palabras · 7 puntos + gancho + cierre · validado (OK) |
| Voz | Fish `rosa_mx` con `--keep-tags` · `voz/master.wav` · **31:14** (1.873,7 s) |
| Transcripción | Groq word-level · `captions.json` · 5.131 palabras con tiempos |
| Fotos | Nano Banana / GPT-image por la cola de avatarity · 290 archivos (267 planos únicos + variantes de gancho, creativas y 2 reposiciones) en 3 slugs de cupo |
| Avatar | InfiniteTalk · 127 ventanas · 544,7 s de avatar (29,1 %) · reel 582,4 s · 1 sola llamada |
| Render | 499 planos · promedio 3,75 s · plantilla compartida `render.py` en la nube (32 tandas) |
| Sonido | 8 cues de Mixkit, ganancia 0,035-0,06 (-29 a -24 dB) |
| Armado | `render.py` + `assemble.py` → GitHub · `final.url` + `final.nube.json` + `qc/f_*.jpg` · 1920x1080 30 fps H.264 CRF 20 · AAC 192k estéreo · 1.873,905 s · 1.018 MB (970 MiB) |

## Decisiones

- **Gancho:** `gancho_c` — dos pares de manos sobre el táper azul de botones (la de ella con anillo y manchas
  de la edad, la de la hija en cárdigan lila), cocina con crucifijo y Virgen de Guadalupe. Se ve a los 7,6 s,
  apenas termina el primer tramo de avatar. Por qué: es la tesis del video en una foto (lo que se regala pasa
  de mano en mano), el lila ata con el cárdigan de Rosa y no tiene texto legible. `gancho_b` quedó descartado
  por el «H-E-B» legible y `gancho_a` por no tener a la segunda persona.
- **Primeros 30 s:** avatar 0-7,6 s (hablando desde el cuadro 1), después cortes cada 2,5 s alternando el
  gancho con fotos de la cocina; las otras ventanas de avatar antes del segundo 30 duran 4,3 s.
- **Estilo Bertha:** 127 ventanas de 3,9 a 5,0 s, una cada ~13 s, máximo 14,3 s sin avatar, 29,1 % del video.
  Las ventanas caen en las frases importantes (la promesa de cada punto, los números, los «pero»).
- **Timeline:** 499 planos, ninguno pasa de 5,5 s ni baja de 1 s, sin huecos (0-1.873.748 ms), primera foto
  después del avatar = `gancho_c`.
- **Foto del avatar:** cambio del creador aplicado — las 127 ventanas de `avatar_ranges.json` apuntan a
  `D:/rtmp/hospice/refs/rosa_av.png` (1672×941, cara ~460 px), la foto canónica del canal. No se generó ningún
  cuadro del presentador con Nano Banana; `avatar/frames/av_a1.jpg` quedó sin uso.

## Imágenes creativas de GPT (4-6 por video)

Se encolaron **6**, con `detalle_narrativo` inventado para este video:

1. `cr_mapa` — el mapa del tour de despedida dibujado a lápiz en el reverso de un boletín de la iglesia
   (mancha de grasa de barbacoa, «14 oct 2021», crucecita junto al nombre de la iglesia).
2. `cr_libro` — Rosa sostiene su cuaderno a cámara con los siete puntos numerados (anillo de café sobre el
   punto 4, hoja de nogal prensada, el punto 3 tachado y reescrito).
3. `cr_receta` — la ficha de «frijoles de la olla» escrita por la madre en marzo 2015, con la lista del
   mandado transparentándose y «comino» subrayado dos veces.
4. `cr_caja` — la caja de fichas con las tarjetas en cuatro letras distintas, la que se saca dice «I KNOW»
   (liga de hule vencida, lista del mandado, esquina de una foto de boda de 1994).
5. `cr_carta` — las cinco frases de la señora Ybarra en una hoja rayada, con estampilla de 58¢ y un aro de
   agua de vaso en la esquina.
6. `cr_album` — la galería del teléfono con seis fotos de la casa, el nogal y ella mirando el nogal, con el
   pulgar de la hija en el borde del último cuadro.

## Sin música

El piano de la Biblioteca de Audio de YouTube no se puede bajar desde el Estudio del creador, así que el
video va **sin música**, sólo voz y los 8 SFX puntuales. Si el creador la quiere, se agrega en el Estudio.

## Problemas y qué se hizo

1. **`props` mal escrito en los generadores** (`{"props": [` en vez de lista) → SyntaxError en dos lotes;
   arreglado con reemplazo simple, sin tocar los prompts.
2. **Linter de fotos** rechazó tres lotes (moments de <70 caracteres, «empty wheelchair», «empty hospital
   bed», pocos primeros planos) → se reescribieron esas frases y se pasaron 8 cámaras a «close-up from…».
   Nunca se salteó el linter (`LINT_FOTOS=0` prohibido).
3. **Timeline con planos de 8 s** (el primer armado arrastraba el inicio de cada plano sobre la ventana de
   avatar) → reescrito `plan_shots2.py`: fronteras de sección + bordes de ventana, trozos <900 ms fundidos,
   y los planos que quedan enterrados bajo el avatar no gastan foto. Resultado: 0 huecos, 0 planos >5,5 s.
4. **Cupo de imágenes:** `hr07ds_b` quedó casi lleno; se abrió un tercer slug de cupo (`hr07ds_c`) para las
   fotos que faltaban y para las reposiciones.
5. **InfiniteTalk cortó a mitad del empalme (A21):** x264 se quedó sin memoria (`malloc of size 1500068 failed`)
   cuando el reel de RunPod ya estaba completo (582,4 s). No se hizo una segunda llamada paga: se cortaron las
   127 ventanas en local desde `avatar/it/reel.mp4` con la misma corrección de desfase por envolvente
   (`rescue_cut.py` → `avatar/it_sync.json`), y se verificó con una hoja de contactos que la boca está abierta
   en posiciones distintas en cada ventana.
6. **Dos prompts bloqueados por política** (`p7_06`, `p3_07`, etiqueta `CSAM_MINOR_SAFETY`): mezclaban
   «drawing de una nena» / «naked lady» con menores. Se reescribieron sin esos elementos y se regeneraron.
7. **Fotos `p7_18` y `p7_17` repedidas:** la primera salía como un primer plano de la cara de un señor con
   los ojos cerrados en la cama, y la segunda como la frente de la hija pegada a esa misma cara; la regla de
   pantalla prohíbe la cara de una persona moribunda. Se rehízo `p7_18` con sólo las manos sobre la frazada y
   el rosario (sin caras) y `p7_17` con la hija apoyada de mejilla sobre la frazada, la cara del señor fuera
   de cuadro. Los originales quedaron como `fotos/_old_p7_18.png` y `fotos/_old_p7_17.png`. En la revisión
   final se miraron además `p4_14` (la señora sentada en su cama, mano en la boca) y `close_02` / `p5_12`
   (planos generales del cuarto con la cara lejos y chica): se dejaron porque no son caras de moribundo.
8. **El render en la nube se cortó una vez** justo después de subir el audio (el proceso murió a las 23:52 sin
   disparar el workflow). Se relanzó `render.py` y retomó todo lo ya subido: 32 tandas, 0 archivos nuevos que
   subir.
9. **Segundo armado cortado por el límite de la terminal:** el proceso local de `assemble.py` que esperaba al
   workflow se cortó a los 10 min, pero la corrida en GitHub siguió y terminó igual. `assemble.py` ahora deja
   el corte en el release (`final.url`) en vez de bajarlo; se bajó con `curl` a `D:/rtmp/hr07ds/final.mp4`
   (1.018 MB) y se verificó con `ffprobe` y cuadros del corte.
10. **Cambio del creador del mismo día:** el final ya no se baja a la PC — `render.py` lo deja hecho en GitHub
    (`final.url`, `final.nube.json`, `qc/f_*.jpg`, `qc/final_info.json`) y el panel lo entrega desde ahí. Este
    video ya tenía su `final.mp4` bueno y validado, así que no se rehizo nada; el archivo local es el mismo
    que está en el release. `qc/final_info.json`: 1.873,905 s, 1920x1080, 30 fps, 0 tramos negros.

## Revisión final (QC)

- 64 cuadros del corte final, uno cada 30 s (`qc/final_000.jpg` … `qc/final_063.jpg`), mirados en 6 hojas
  de contactos (`qc/hoja_final_1.jpg` … `qc/hoja_final_6.jpg`) más los 62 cuadros que saca el render de la
  nube (`qc/f_000.jpg` … `qc/f_061.jpg`).
- Arranque: cuadro 0 = avatar hablando en la cocina (0-7,6 s); a los 7,6 s entra `gancho_c`.
- Sin cuadros negros, sin huecos en el plan, avatar en ventanas cortas a lo largo de todo el video.
- Reposiciones comprobadas en el corte nuevo: 1591-1594 s y 1609-1612 s (manos + rosario, sin caras) y
  1588 s / 1607 s (la hija con la mejilla sobre la frazada, la cara del señor fuera de cuadro).
- Última ventana de avatar (1867,6-1871,7 s): tres cuadros seguidos muestran la boca cerrada, entreabierta y
  abierta → el clip no está congelado y el desfase corregido no deja la boca parada.
- `ffprobe`: 1.873,905 s · 1920x1080 · 30/1 · H.264 · AAC 2 canales.

## Costos

- InfiniteTalk: **US$ 0,25** (una sola llamada, 127 ventanas).
- Nano Banana / GPT-image: cola compartida de avatarity, sin costo directo.
- Fish, Groq, Mixkit: gratis.
- DeepSeek (guion): sin costo medible en esta corrida.

## Pendientes / a mejorar

- Desfase del avatar medido y corregido en `avatar/it_sync.json`: 0 ms al principio, hasta -395 ms al final
  del reel (el reel pierde ~0,1 s por minuto). Revisado a ojo en el corte final (cuadros de 1867,6-1871,7 s):
  la boca se mueve con el audio, sin quedar adelantada ni parada.
- El validador avisa «5155 palabras (esperado 2762-4312 para 25 min)» — el video dura 31:14, así que el aviso
  es por el rango fijo de 25 min, no por el guion.
- El otro aviso, «291 fotos · 2 NO salieron de Nano Banana (cola avatarity)», son las dos reposiciones que sí
  salieron de la cola pero se guardaron con otro nombre: `p7_18b.png` → `p7_18.png` y `p7_17b.jpg` →
  `p7_17.png`.
- Agregar los 7 pacientes nuevos a `D:/rtmp/hospice/BIBLIA.md` («Agregados»).
