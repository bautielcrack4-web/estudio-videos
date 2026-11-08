# REPORTE — simulacro 1 (Michiko · 7 handbag mistakes)

**Tipo:** simulacro de punta a punta EN MINIATURA (sólo el gancho). No es el video final de 15 min.

## Entregado
| | |
|---|---|
| `final.mp4` | **49,842 s** · 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192 k · 18,4 MB |
| `voz/master.wav` | 49,842 s · 44,1 kHz mono · 1 bloque Fish (gratis) |
| `captions.json` | 122 palabras con startMs/endMs (Groq) |
| `plan.json` | 10 segmentos, 0 huecos, con `file` absoluto por tramo |
| Fotos | **4** (3 b-roll + 1 primer cuadro de avatar), 0 repetidas, 0 descartadas |
| Clips de avatar | **0** (corrió sólo `SECO=1`: no se gastó agnes) |
| Avatar en pantalla | 6,26 s, como **foto fija** (el clip A1 no existe) |
| SFX | 1 cue de prueba a −20 dB (`sfx_tela.mp3`) + 2 tomas de reserva |
| Cuota de cola | 4/150 imágenes · 0/15 videos |

## Gasto
- **US$ 0,00.** Fish, Groq, la cola de avatarity y Mixkit son gratis; agnes no se tocó (SECO).
- OpenAI no se usó (además existe `D:/rtmp/SIN_OPENAI`).
- Lo de DeepSeek (la sesión del agente) no se mide desde acá.

## Qué salió bien
- La cola de avatarity devolvió las 4 imágenes en ~4 min, con prio 0/0/1/0, sin 429.
- `plan_motion()` al azar + semilla 20261106: misma foto repetida con movimiento distinto en cada aparición.
- Los fundidos (18 cuadros avatar / 9 cuadros foto) no corren los tiempos: final 49,841995 vs voz 49,842381 s.
- El branch de SFX de `assemble.py` (amix con voz) funciona y `duration=first` respeta la voz.

## Problemas y huecos (detalle en SIMULACRO.md)
1. `validar.py --etapa guion --min 15` **falla** con el guion del simulacro (125 palabras vs 1657-2587) — pero sólo porque el brief manda `--min 15`. Con `--min 0.8` (la duración real del recorte) da **OK**. El validador sí sabe medir un recorte corto: el error es del comando del brief.
2. El KIT pide tramos de avatar de **8-12 s**, pero `validar.py` rechaza tramos de avatar de **> 6,5 s** en los primeros 30 s (el mensaje dice «≤ 6 s»). Incompatible sin partir la intro.
3. `render.py`/`assemble.py` **no son drop-in**: tienen `AUDIO_MS = 957900` y `img/pics` a mano. Hay que editar 4 cosas además de las rutas.
4. `plan.json` (formato del brief, con `file`) **no lo lee** `render.py`: el render usa `shots_timed.json` + `avatar_ranges.json`. Hice que los tres salgan de una sola tabla para que no se desincronicen.
5. `sfx_doc.mjs` devuelve tomas con poca relación semántica con los tags: para `["handbag","hook","hang"]` dio «Dough hook drop» (un gancho de panadería) y para `["fabric","rustle"]` dio «Squishing a soggy cloth shirt». Hay que escuchar/elegir, no confiar en el nombre.
6. `sfx_doc.mjs` escribe en `video2/public/<slug>/sfx/`, no en la carpeta del video: hay que copiar a mano.
7. El audio del final queda **mono** (el master es mono y `assemble.py` no lo sube a estéreo).
8. El chequeo «cara ≥ 400 px» de `avatar.mjs` mide el **ancho del archivo** (460 px), no la cara: la cara real ronda 300-330 px y el avatar puede salir blando. No se puede detectar sin abrir la imagen.
9. Con 3 fotos para 50 s, b01 se repite 4 veces (0/20,7/30,9/44,6 s). En el video real, con 1 foto cada 3-5 s, no pasa.

## Qué falta para el video real
- Guion completo (~1.800 palabras, 15 min) → `guion.txt` y `validar.py --etapa guion` en verde.
- Intro de avatar 15-20 s partida en tramos ≤ 6 s con b-roll entre medio + 3 regresos de 8-10 s (total ≤ 55 s).
- ~200 fotos Nano Banana (1 cada 3-5 s) en tandas de 30 con hoja de 12.
- Clips de avatar reales (agnes, ~1-3 h de cola con 10 videos en paralelo) y re-render sólo de sus segmentos.
- SFX elegidos a oído, no por tag; `cues.json` con tiempos de `captions.json`.
- `assemble.py` a estéreo (−ac 2) y prueba de un tramo de 25 segmentos a escala real.

## Archivos de control
`gates/guion_auto.txt` · `gates/fotos_auto.txt` · `gates/fotos_pedido.txt` · `gates/render_auto.txt`
`gates/render_pedido.txt` · `gates/final_auto.txt` · `gates/final_pedido.txt` · `gates/correcciones_hechas.txt`
Hoja de fotos `qc/hoja_fotos.jpg` · hoja del render `qc/hoja_render.jpg` · hoja del final `qc/hoja_final.jpg`.
