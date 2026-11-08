# REPORTE · fe10ds

**Canal:** Don Ernesto, el Funerario
**Título:** Qué pasa con un mexicano que muere en Estados Unidos y lo regresan a su pueblo
**Voz:** `ernesto_es` (Fish, gratis)
**Entrega:** `D:/rtmp/fe10ds/final.mp4` + `meta.json` + este reporte

---

## 1. Qué se hizo

| Etapa | Detalle |
|---|---|
| Guion | `guion.txt`, 4317 palabras · 9 puntos (problema → anécdota con fecha/nombre/lugar → por qué pasa → cambio concreto con precio → chequeo de esta noche) · gancho con número y objeto · prueba de una palabra al minuto ~4-5 · like/suscribí antes del último punto · cierre con pregunta y guiño a fe11. Validador etapa guion: sin ✗. |
| Voz | Fish `ernesto_es`, 27,8 min (1667,5 s), 2 tags de emoción, `voz/master.wav` + `manifest.json`. |
| Tiempos | Groq ASR por palabra → `captions.json` (~50 ms). Todo el plan de cortes está anclado a esas marcas. |
| Avatar | InfiniteTalk, **1 sola llamada** (US$ 0,25): 129 ventanas A0…A128, reel 534,0 s, desfase medido y corregido (máx 395 ms) en `avatar/it_sync.json`. Primer cuadro = `D:/rtmp/funerario/refs/ernesto_av.png` (foto del creador), como pidió. Avatar total 495,7 s = **29,7 %** del video, ventanas de 3-6 s cada ~11-13 s, nunca más de 20 s sin avatar. |
| Fotos | Nano Banana por la cola de avatarity: **55 momentos** distintos (`gancho_a/b/c`, `t01…t03`, `d12…d30`, `e01…e05`, `f01…f17`), **206+ archivos** contando los encuadres recortados. Cada sección del guion tiene ≥9 candidatas y ningún archivo se usa más de 4 veces. |
| Imágenes creativas | Las de GPT quedaron pedidas con `detalle_narrativo`; la cola las devolvió igual por Nano Banana (ver problemas). Se conservan las que sí traen detalle propio (cotización tachada, calendario de enero, póliza sobre la cómoda con el rosario, urna envuelta en un suéter dentro de la maleta). |
| Sonido | 5 SFX de Mixkit (`campana`, `dinero`, `metal_2`, `papeles_2`, `telefono_3`) en `sfx/`, mezclados bajos (gain 0,035-0,08) en `cues.json`. Sin música. |
| Armado | **En GitHub** (regla nueva del creador): `render.py` armó el plan (521 segmentos, `plan.json`), subió UN paquete con fotos/avatar/voz/SFX y ~34 máquinas renderizaron en paralelo (Ken Burns aleatorio con semilla fija, fundidos 0,6 s avatar y 0,3 s entre fotos), unieron y pusieron la voz + SFX. 8,3 min la segunda corrida. El final quedó en GitHub Releases (`final.url`) y se bajó a `final.mp4` para la entrega. `assemble.py` ya no hizo falta. |

## 2. Estructura de la apertura (regla del creador)

`plan.json` verificado: **A0 de 0,00 a 7,98 s** (avatar hablando desde el primer cuadro) → `gancho_a` (caja de metal con papeles) → **A1 3,84 s** → `f10_carga_avion` → **A2 4,00 s** → `gancho_a_v3`. En los primeros 30 s alterna avatar y foto cada 3-4 s, sin superar los 6 s por ventana.

## 3. Problemas y cómo se resolvieron

1. **Sequía de fotos.** gpt-image-2 devolvió 429 desde las 19:01 y todo cayó a Nano Banana; llegaba ~1 foto cada 6-7 min. Se resolvió reconstruyendo el plan cada vez que entraban fotos y multiplicando cada foto en 5 encuadres (3 en las PNG chicas 1088x608, que quedaban fuera del mínimo de ancho).
2. **Fotos chicas sin recortes.** Los dos scripts de variantes las salteaban en silencio (0,72 x 1088 = 783 px < mínimo). Se agregó `make_variants3.py` con ancho 0,84 solo para las chicas: 40 variantes más.
3. **Render con poca memoria.** `RENDER_WORKERS=5` murió a los ~163 segmentos con `WinError 1455: el archivo de paginación es demasiado pequeño` (C: al 100 %, commit lleno con ~28 ffmpeg de otros videos). Se relanzó con **RENDER_WORKERS=2** y `TMP/TEMP` en `D:/rtmp/tmp_fe10ds`. La firma `.src` de render.py evitó repetir trabajo.
4. **Seis segmentos vacíos** (0190, 0259, 0327, 0365, 0367, 0368) quedaron en 0-262 bytes aunque el render decía "hechos 521". Se borraron y se re-renderizaron: 521/521 válidos, ninguno menor a 20 KB.
5. **Pedido viejo fallido en la cola** (`fe10ds__av_a1.json`, POST 400 INVALID_PAYLOAD por un prompt en objeto): era un pedido heredado, no afectó la entrega.
6. **`assemble.py` local murió por memoria** (`Cannot allocate memory`) con ~30 ffmpeg de los otros videos corriendo; se armó un `assemble_resume.py` para terminar ese intento. Quedó obsoleto cuando el creador pasó el render a GitHub: desde entonces `render.py` sube el paquete y allá se une todo, así que `assemble.py` no se volvió a usar.
7. **D: se llenó tres veces** (0 bytes libres; otros ~10 videos en paralelo). Se borraron sólo intermedios míos ya reemplazados (`voz_old_30min`, un `final.mp4` truncado a 64 MB) y todo lo pesado se dejó en C:.
8. **Desfase video/audio (el problema grande).** El final de GitHub medía 1663,50 s de video contra 1667,88 s de voz y las ventanas de avatar entraban adelantadas (0,5 s a los 298 s, ~2 s a los 1005 s, ~3,5 s a los 1600 s). **Causa raíz encontrada en `render.py` (herramienta compartida, no la toqué):** al recortar las fotos contra las ventanas de avatar quedan trocitos de <0,5 s, y `render.py` los descarta (`if y - x >= 500`). Eran **17 huecos de 0,04-0,48 s (3,94 s en total)**; al unir, la pista de imagen se comprimía esos 3,94 s mientras el audio quedaba completo → el desfase crecía de a poco. Primero se probó un retime sin pérdida (`-itsscale`, `-c:v copy`) sobre un armado local: sincronizaba pero dejaba **359/12 fps (29,9167)** y no arreglaba el origen. **Solución definitiva:** mover 33 bordes en `shots_timed.json` (sin tocar render.py) para que ningún trozo visible quede bajo 500 ms. Lo simulé con la misma lógica de `render.py` antes de renderizar: `521 segmentos, 0 huecos`, `50036 cuadros`. Segunda corrida a GitHub (sólo 33 tandas, 8,3 min): video **1667,864 s / 50036 cuadros**, audio **1667,879 s**, **fps 30/1 exacto** y `plan.json` con **0 huecos**. Sincronizado comprobado con cuadros exactos sacados por HTTP del release: A78 entra en 1005,60 s y A124 en 1600,63 s, cada una con su fundido de 0,6 s.
9. **Avisos `!` del validador final, aclarados:** `make_variants3.py` aparece como "herramienta prohibida para fotos" pero es un script propio de **recortes con PIL** sobre fotos que ya salieron de la cola (no llama a ninguna API); las "118 fotos que NO salieron de Nano Banana" son esos mismos recortes derivados. El guion quedó en 27,8 min (un poco más largo que los 25 pedidos). Los 17 huecos de `plan.json` que aparecían antes ya no existen.

## 4. Costos

| Ítem | US$ |
|---|---|
| InfiniteTalk (1 llamada, 129 ventanas) | 0,25 |
| Fish, Groq, Mixkit, Nano Banana por cola | 0,00 |
| **Total** | **0,25** |

## 5. Control de calidad

- Validadores: guion, fotos, render y final (ver `gates/`).
- Hojas de contacto revisadas con Read: `qc/hoja_fotos.jpg`, `qc/hoja_render.jpg`, `qc/hoja_d1.jpg`, `qc/hoja_d2.jpg`, `qc/hoja_render2.jpg`, y sobre el final de GitHub los 56 cuadros `qc/f_001.jpg` … `qc/f_056.jpg` (uno cada ~30 s) en 5 hojas: avatar desde el primer cuadro y cada ~11-13 s, sin negros, sin cuerpos ni caras de agonía. Los "dobles" que aparecen en una hoja son cruces de fundido capturados por el muestreo.
- Sincronizado comprobado cuadro por cuadro con ffmpeg sobre el release por HTTP (sin bajarlo): duración de la pista de video 1667,864 s vs audio 1667,879 s, y A78/A124 entrando en su `startMs` (1005,60 s y 1600,63 s).
- Reglas de pantalla respetadas: ni cuerpos, ni caras de agonía, ni sangre, ni tubos. Sí manos tomadas, espaldas en la cama, ventanas, familia en la cocina, pasillos y objetos.

## 6. Pendiente / mejoras para el próximo

- La cola no entregó las 4-6 imágenes creativas de GPT con `detalle_narrativo` como tales: llegaron como fotos de Nano Banana. Para fe11 conviene pedirlas con más anticipación, antes de que arranque la sequía.
- Las fotos chicas (1088x608) obligan a recortar más y pierden algo de detalle al escalar a 1920x1080.
- Con ~10 videos en paralelo la máquina quedó sin RAM: conviene arrancar el render completo de noche o con `RENDER_WORKERS=2` desde el principio.

## 7. Entrega

```
D:/rtmp/fe10ds/final.mp4   (bajado del release que armó GitHub)
https://github.com/bagasy-search/claudeyoutubevideos/releases/download/est-fe10ds/final_efae0a2db55b.mp4
Contenedor: MP4 · 832.161.904 bytes
Video:  H.264 · 1920x1080 · 30/1 fps · 3,79 Mbps · 50036 cuadros
Audio:  AAC · 48 kHz · estéreo · 189 kbps
Duración: 1667,879 s (27:47,9) — idéntica a voz/master.wav (diferencia 0,00 s;
          pista de video 1667,864 s, 0,014 s de diferencia)
```

- Entrega en GitHub: `final.url` + `final.nube.json` + `qc/final_info.json` (1920x1080, 30/1 fps, 1667,879 s, **0 negros**) + 56 cuadros `qc/f_001..056.jpg`. El `final.mp4` local es una copia de ese mismo release (bajada antes del aviso de "cero disco"); el video ya vale por la entrega de GitHub.
- Validador etapa final: **RESULTADO OK**, sin ✗ — `plan.json` 0 huecos, fps 30/1, duración = voz, arranca con avatar (30 % del video con avatar). Avisos `!` explicados en §3.9.
- Primer cuadro: avatar hablando desde 0,00 s (ventana A0, 7,98 s), frame de arranque = `D:/rtmp/funerario/refs/ernesto_av.png`.
- Sin música. SFX sólo en 5 momentos puntuales, por debajo de la voz.
- `meta.json` con título y descripción (3 párrafos en la voz del presentador, sin enlaces).
