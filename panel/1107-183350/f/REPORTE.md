# REPORTE — "The Rally Before Death: Why a Dying Parent Suddenly Gets Better for One Day"

Canal: Hospice Chaplain Rosa · carpeta `D:/rtmp/hr09ds` · 8-nov-2026

## Qué se hizo

- **Guion** (`guion.txt`): 5015 palabras, inglés, voz de Rosa (capellana de hospice, 34 años, West Side de San Antonio).
  Hook 0-45 s, credencial, test interactivo en el minuto ~4, cinco puntos con el molde problema → anécdota con fecha →
  por qué pasa → cambio concreto con precio → chequeo de esta noche; like/subscribe antes del último punto; pregunta final
  para comentarios + enganche al próximo video. Sin palabras prohibidas (honest, genuinely, filler, sermonizing,
  medical advice) ni indicaciones médicas: Rosa nunca diagnostica, nunca habla de dosis ni de pronóstico.
- **Voz** (`voz/master.wav`): Fish, voz `rosa_mx`, concurrencia 3. Duración final **29:16** (1756 s).
- **Tiempos** (`captions.json`): Groq word-level ASR, una entrada por palabra, ~50 ms de precisión. Última palabra
  termina en 1 756 479 ms; todos los cortes del video salen de ahí, no de estimaciones.
- **Fotos** (`fotos/`): pedidas por la cola compartida de avatarity (`encolar.mjs`, Nano Banana / gpt-image-2) con
  prompts JSON completos (moment, subject, action, props 6-10 con material y desgaste, setting, light, camera, color,
  avoid). Nada de agnes-imagen ni gpt-image directo. Cada foto es un momento con alguien a mitad de gesto en un lugar
  real lleno de cosas; ≥30 % primeros planos, ≥60 % con persona o manos, cámara distinta en cada una.
- **Avatar** (`avatar/A0.mp4` … `A116.mp4`): InfiniteTalk, **una sola llamada paga** (`avatar_it.py`), US$0,25,
  ejecución 84 min en RunPod. 117 ventanas, 503,4 s = **28,7 % del video**, ventanas de 3-6 s, ninguna pausa sin avatar
  mayor a 12,5 s. Primera ventana arranca en 0 ms con el cuadro `D:/rtmp/hospice/refs/rosa_av.png` (foto del canal).
  Desfase medido y corregido por ventana (máximo 395 ms antes de corregir), queda en `avatar/it_sync.json`.
- **Sonido** (`sfx/` + `cues.json`): 6 efectos puntuales de Mixkit (taza, teléfono, puerta de auto, puerta, papeles,
  lapicera), ganancia 0,035-0,06, sólo en el momento exacto de la palabra. **Sin música** (decisión: el canal no usa
  música de fondo; sólo voz y sfx puntuales).
- **Armado**: `render.py` con render en **GitHub** (352 segmentos subidos en 22 tandas, 23 máquinas en paralelo,
  7,6 min de render) + fundidos y audio; `assemble.py` ya no se usa. El video final **no se baja a la PC** (así lo
  hace ahora la herramienta): queda en
  `https://github.com/bagasy-search/claudeyoutubevideos/releases/download/est-hr09ds/final_5648983c59f6.mp4`
  y el enlace queda también en `final.url` y `qc/final_info.json`. 29,3 min, 932 MB, 1920x1080 30 fps, AAC estéreo,
  0 huecos negros, duración 1756,11 s = voz 1756,11 s.

## Puntos de control

| Puerta | Validador | Revisión visual | Archivos |
|---|---|---|---|
| guion | 1 corrida | — | `gates/guion_auto.txt`, `gates/guion_pedido.txt` |
| fotos | 1 corrida | 3 hojas de contacto | `gates/fotos_auto.txt`, `gates/fotos_pedido.txt` |
| render | 1 corrida, OK | `qc/hoja_final.jpg` | `gates/render_auto.txt`, `gates/render_pedido.txt` |
| final | 2 corridas, OK | `qc/hoja_final_2.jpg` (12 cuadros) | `gates/final_auto.txt`, `gates/final_pedido.txt` |

## Problemas y cómo se resolvieron

1. **Cola de fotos lenta** (compartida con ~10 videos): al armar el timeline sólo había 53 fotos `.jpg` en disco.
   Solución: `fill_shots.py` guarda el plan original en `shots_plan.json` y reemplaza cada foto faltante por la foto
   existente más cercana del mismo tramo del guion, sin dos iguales seguidas; `render.py` rehace sólo los segmentos
   que cambian cuando llega una foto nueva.
   **Corrección importante**: la cola ya había entregado las 236 fotos, pero 183 llegaron como `.png` y mi conteo
   sólo miraba `.jpg`, así que las dos primeras corridas repitieron esas 53. Arreglado el filtro (jpg/jpeg/png/webp),
   el timeline final usa **234 fotos distintas** sobre 236 ids del plan (sólo falta `x02`, que se cubre con su vecina).
2. **Poller de RunPod huérfano**: el proceso node del avatar quedó vivo sin su padre python y el rescate chocó con el
   candado (`otro proceso ya está lanzando el avatar`). No se lanzó una segunda llamada paga; el job original terminó
   bien a los 84 min y produjo los 117 clips.
3. **Texto legible inventado** en `t04` (número de "hospice after hours" en el refrigerador): repedida como `t04b`
   con garabatos sin letras y avoid reforzado.
4. **Render local** (prueba de 10 segmentos): dos segmentos fallaron de forma transitoria (error -22 y "Generic error
   in an external library"); se rehízo la misma corrida y salieron bien. El render local quedó descartado cuando el
   creador pasó todo a GitHub.
5. **Primer intento de subida a GitHub** murió con un volcado de memoria de Python en `tarfile`; se relanzó `render.py`
   y subió 170 archivos (130 MB) en 44 s.
6. **Hueco de 0,23 s** en 1240,2 s: un plano de 233 ms que el render redondeaba a cero cuadros. Arreglado en
   `fill_shots.py` (los planos de menos de 0,4 s se fusionan con el de atrás) y se volvió a renderizar.

## Qué falta / para mejorar

- **Duración**: el audio quedó en 29:16 en vez de ~25 min (5015 palabras a 171 ppm). El guion cumple el mínimo de 4600
  palabras del brief, así que no se recortó; el validador avisa por el rango esperado para 25 min.
- **Fotos**: entraron 234 fotos distintas; sólo `x02` no tiene foto propia y se cubre con su vecina. `t02` (señora en el
  porche, plano lejano) sigue siendo la más floja: se lee "persona sentada", no "momento".
- **Entrega**: el final queda en GitHub, no en `D:/rtmp/hr09ds/final.mp4` — así lo hace ahora `render.py` (borra el
  final local viejo a propósito). El enlace está en `final.url` y en `qc/final_info.json`.
- Costos: InfiniteTalk US$0,25 (única llamada). Fish, Groq, avatarity (fotos) y Mixkit: gratis. Render GitHub: sin costo
  por corrida.
