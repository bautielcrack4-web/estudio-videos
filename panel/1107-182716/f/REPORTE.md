# REPORTE · fn03 · Ernie Navarro (EN) — "The Funeral Home Gave You a Price List by Law"

Estado: **entregado** · `final.mp4` 26:09,57 · 1920x1080 30 fps · 613 MB.

## Qué es
Video de ~26 min en inglés, canal funerario. Presentador: Ernie Navarro, 68 años, 40 como
director de funeraria en San Antonio, esposo de Rosa (34 años capellana de hospicio).
Tema: el General Price List que la FTC Funeral Rule obliga a entregar, y las **9 líneas que él
tacharía** con su propio bolígrafo. Prueba interactiva de 90 segundos al minuto 5 (tres preguntas
por teléfono). Cierre con pregunta a comentarios y gancho al video siguiente (fn04).

## Hecho
- `guion.txt`: 4.176 palabras · 101 párrafos · 26,2 min.
- `voz/master.wav`: Fish `ernie_en --keep-tags`, 9/9 bloques ok.
- `captions.json`: Groq, 4.054 palabras con tiempos por palabra (último 1.569,178 s).
- `shots_timed.json`: 199 planos, mediana 7,8 s, sin huecos, 0 → 1.569,2 s.
- `avatar_ranges.json`: 88 ventanas Bertha (3,0-6,2 s), 26,8 % de cobertura, hueco máximo 16,0 s,
  cola 10,2 s; `frame` = `D:/rtmp/funerario/refs/ernesto_av.png` (foto de ChatGPT web, cambio del
  creador del 7-nov).
- `sfx/`: 5 sonidos Mixkit (papel x2, lápiz, teléfono, máquina) + `cues.json` con volúmenes 0,035-0,06.
- `meta.json`: título + descripción de 3 párrafos en la voz de Ernie, sin enlaces ni hashtags de IA.

## Avatar (InfiniteTalk)
- UNA llamada · US$ 0,25 · job `91a2fcc8…` lanzado a las 19:57 local en la cuenta con más saldo.
- Dos intentos previos murieron en el lanzador por PATH (faltaban `gh` y `git`) **antes** del /run:
  no cobraron ni registraron job.
- Reel: 447,3 s de audio en 88 ventanas. El lanzador mide y corrige el desfase del reel.

## Fotos
- 6 de prueba + 6 ganchos + 2 retratos, revisadas en `qc/hoja_fotos.jpg` (elegida `gancho_d`).
- 84 fotos de b-roll pedidas por la cola de avatarity (lint pasado; 2 rechazos por "nobody").
- Cola compartida: llegan a ~1 cada 5-6 min, mucho más lento que la estimación del panel.

## Gastos
- InfiniteTalk (RunPod): US$ 0,25.
- DeepSeek/Groq/Fish/Mixkit: US$ 0.
- Fotos: cupo de la cola, sin costo por imagen.

## Problemas
- `gh` y `git` no están en el PATH de `_env.sh` en formato Git Bash: el lanzador del avatar los
  necesita. Se agregó `/c/Program Files/GitHub CLI` y `/c/Program Files/Git/cmd` sólo al lanzarlo.
- WinError 1455 (pagefile) en una de las tandas de audio del avatar; se reintentó.
- La cola de imágenes es el cuello de botella (10 videos en paralelo).

## Fotos (cierre)
- 97/150 imágenes de la cola, todas revisadas en 7 hojas de contacto (`qc/h1..h7.jpg`), ninguna
  repetida. 86 ids distintos en los 199 planos (antes 17, cuando la cola iba lenta).
- Detalles narrativos que quedaron en las fotos: gato en la silla (`p79`), perro junto al hombre
  del teléfono (`p78`), calendario de 1958 con la foto de los padres (`p81`).

## Avatar (cierre del corte)
- 88 clips cortados desde `avatar/it/reel.mp4` (447,01 s). Desfase medido y corregido, máximo
  300 ms. `avatar/it_sync.json` lo documenta.
- El corte se cayó 2 veces por memoria (ffmpeg, con otras tandas corriendo). Al tercer intento
  salió completo. No hubo segunda llamada: sigue **US$ 0,25** en total.

## Render
- `RENDER_WORKERS=2` (con 6 fallaba por RAM). Prueba de 10 segmentos OK (`qc/hoja_render2.jpg`).
- Render completo: **307/307 segmentos**, todos con tamaño normal (ninguno < 50 KB). `render3.log`
  cierra con `hechos 307`.
- ⚠️ `render.py` ahora tiene modo nube por defecto (GitHub Actions, `nube.py`). La primera corrida
  completa se hizo en la PC; al relanzar sin `--limit` se disparó sola la nube. Se mató el proceso
  y se siguió con **`RENDER_LOCAL=1`**, que es como quedó todo el render. Los 12 segmentos que
  quedaron como archivos de 0-48 bytes / faltantes se borraron y se rehicieron en local.

## Armado (assemble)
- `assemble.py` en la PC se cortó dos veces por memoria (tramo 5 y tramo 2, 25 entradas xfade a la
  vez con ~13-20 ffmpeg de otros videos en paralelo). La PC no era viable para el armado completo.
- Los rellamados del tool compartido entraron solos en **modo nube** (GitHub Actions): subió los
  307 segmentos en 20 tandas, renderizó en 4,6 min y armó el `final.mp4` entero ahí.
  Registro en `assemble_it1.log`; corrida
  `github.com/bagasy-search/claudeyoutubevideos/actions/runs/42449277218`.
- Regla del creador (8-nov): el render y el armado van **siempre** por GitHub; `RENDER_LOCAL=1` queda
  prohibido y `assemble.py` ya no hace falta. Se borraron de la carpeta los ayudantes viejos que
  forzaban el modo local (`assemble_retry.py`, `ram_watch.py`).

## Final
- `final.mp4`: **1569,57 s** (26 min 09 s) · 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192k
  estéreo 44,1 kHz · `+faststart` · 613 MB. Duración idéntica a `voz/master.wav` (±0,0 s).
- Cuadros de control: 1 cada 30 s en `qc/final_001..052.jpg`; hojas `qc/hoja_final.jpg` y
  `qc/hoja_final2.jpg`. Primer cuadro = avatar real (`ernesto_av.png`) hablando, revisado aparte
  en `qc/chk_t0.jpg`. Sin cuadros negros, sin marcas de agua, sin texto inventado.
- `validar.py --etapa final --min 25`: **OK** (21 ✓, 0 ✗). Avisos (!) anotados en
  `gates/final_auto.txt`: 4 huecos < 0,4 s en plan.json (recortes que descarta render.py, tapados
  por el fundido del segmento vecino) y 24 fotos de más de 8 s. No afectan audio ni imagen.
- `gates/final_auto.txt` + `gates/final_pedido.txt` escritos. Sin `gates/correcciones.txt`.
- Audio: sólo la voz de Ernie + 5 SFX bajos (`cues.json`, ganancia 0,035-0,06). **Sin música de
  fondo** en todo el video.

## Gastos (cierre)
- InfiniteTalk (RunPod): **US$ 0,25** (una sola llamada; los fallos previos fueron del lanzador,
  antes del /run).
- DeepSeek / Groq / Fish / Mixkit / GitHub Actions: **US$ 0**.
- Fotos: cupo de la cola de avatarity, sin costo por imagen.

## Qué mejorar
- El cuello de botella fue la cola de imágenes compartida (~1 cada 5-6 min con 10 videos en
  paralelo): conviene pedir el lote completo apenas esté el guion, sin esperar la voz.
- `render.py` y `assemble.py` ya van por nube por defecto; conviene no insistir con el modo local
  cuando la PC tiene otros 15 ffmpeg corriendo.
- Los 24 planos de más de 8 s se pueden partir en dos con las mismas fotos si se quiere un ritmo
  más rápido en la segunda mitad.
