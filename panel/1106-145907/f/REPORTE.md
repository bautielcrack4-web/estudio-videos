# REPORTE — Michiko's Kyoto Closet · "Carol Flew to Kyoto at 70"

_Estado: **ENTREGADO**. `final.mp4` listo en `D:/rtmp/mk08ds/`._

## Qué es
Video de **13 min 32 s** (812,11 s) sobre Carol, una mujer de 70 años que vuela
a Kyoto y cambia 6 prendas de su valija en la casa/tienda de Michiko. Guion en
inglés, precios en US$, temperaturas en °F, sin marcas de IA dentro del video y
sin claims médicos.

## Entregables
| archivo | detalle |
|---|---|
| `final.mp4` | 1920x1080 · 30 fps · H.264 CRF 20 (~3,26 Mbps) · AAC 192k estéreo 44,1 kHz · 812,11 s · 335 MB (351.119.486 bytes) |
| `meta.json` | title + description en inglés |
| `gates/` | guion, fotos, render y final (auto + pedido) |
| `qc/` | hojas de fotos, render, avatar y cuadro cada 30 s |

## Pipeline usado
1. **Guion** — `guion.txt`, 170 bloques visuales sobre ~165 oraciones.
2. **Voz** — Fish Audio (`fish_factory.py`, voz del brief): un WAV por bloque +
   `voz/master.wav` de **812,11 s**. Gratis.
3. **Tiempos por palabra** — Groq ASR: `captions.json`, 2105 palabras con
   `startMs`/`endMs`; cada corte de imagen se pegó a la palabra más cercana.
4. **Avatar** — agnes-video-2.5-flash vía `avatar.mjs`, modo reference:
   5 clips (A1, A2, R1, R2, R3) = **44 s**. Intro en tramos de 6 s
   (2,08–8,08 s y 12,74–18,74 s) intercalados con fotos, más 3 regresos
   (46,3–54,3 s · 136,7–148,7 s · 786,5–798,5 s). Cupo agnes, US$ 0.
5. **Fotos** — Nano Banana por la cola compartida de avatarity: **158 fotos**
   de b-roll en 9 batches (170 pedidos con las variantes de gancho), prompts en
   JSON con `moment/action/props/setting/light/camera/avoid` y validación
   automática (`lint_fotos.py`, 0 incompletos). Gratis.
6. **SFX** — Mixkit: **10 cues** en `cues.json` (valija, té, cajón, puerta,
   papel ×2, tela ×2, pasos, tijeras, avión), ganancias 0,045–0,06. Gratis.
7. **Armado** — `render.py` (Ken Burns aleatorio por foto: tipo, intensidad
   5–13 %, foco y dirección sorteados con semilla fija; 3840x2160 antes de
   `zoompan` para que no tiemble) + `assemble.py` (xfade 0,6 s avatar↔foto y
   0,3 s foto↔foto, voz y SFX). 165 segmentos, 24.353 cuadros.

## Composición del corte
- **170 planos**, **152 fotos distintas**; 18 planos son callbacks a propósito
  (gancho_a/b/c, a01_petalos, a07_nota, h05, h12, c01_fumiko_foto, e07, e10,
  e12, i1_03, i5_01, i6_01, h11), siempre separados por más de 60 s.
- **Segundo 0** = gancho_a (Carol riéndose mientras Michiko le alcanza la
  bufanda mostaza). El video cierra con la misma foto a los 807 s.
- Avatar sólo en la intro y en 3 regresos; todo lo demás es b-roll de fotos con
  Ken Burns y fundidos.

## Puntos de control
- `gates/guion_auto.txt` + `gates/guion_pedido.txt`
- `gates/fotos_auto.txt` + `gates/fotos_pedido.txt` (+ cierre del lote)
- `gates/render_auto.txt` + `gates/render_pedido.txt` (+ render completo)
- `gates/final_auto.txt` + `gates/final_pedido.txt`
- No apareció `gates/correcciones.txt`: no hubo pedidos del revisor.

## Gasto
**US$ 0.** Fish, Groq, agnes, Nano Banana y Mixkit son gratuitos en este setup;
gpt-image no se usó.

## Problemas y notas (y cómo se resolvieron)
- **Cara de Michiko chica**: el recorte disponible da ~290–315 px de ancho de
  cabeza, por debajo del ideal de 400 px. Se usó el máximo sin re-comprimir; los
  clips salieron bien, pero es el techo de nitidez del avatar.
- **4 segmentos corruptos** (0129, 0130, 0161, 0163): carreras entre dos
  `render.py` que se pisaron y dejaron mp4 con `moov` roto o NAL inválidos.
  Síntoma: el ensamblado final quedaba 21 s corto y un tramo de 57 s en vez de
  78 s. Se borró cada `NNNN.mp4` + su `NNNN.mp4.src`, se re-corrió `render.py`
  y se verificó cuadro por cuadro (los 165 segmentos dan exacto contra `xf.json`).
- **Ensamblador zombie**: un `assemble.py` viejo siguió escribiendo mientras
  corría el nuevo y mezcló los chunks. Se mató por PID (pid de PowerShell) y se
  volvió a ensamblar limpio de punta a punta.
- **SFX reubicados**: dos cues caían dentro del tramo de avatar R2
  (136,7–148,7 s); se movieron a la foto que los justifica: puerta→103,3 s,
  té→55,2 s, cajón→69,3 s, papel→137,0 s.
- **Aviso del validador**: 4 fotos quedan 8–8,7 s en pantalla (a05, a01, i1_03,
  i1_05). Es aviso, no falla; no se re-renderizó porque el costo era rehacer
  esos segmentos y todo el ensamblado por 0,1–0,7 s de diferencia.
- Sin clips ni fotos de reemplazo: todo lo que se ve en el corte final es el
  material pedido (5 clips de avatar reales y fotos de Nano Banana).
