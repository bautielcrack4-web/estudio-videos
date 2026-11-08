# REPORTE · fe12ds · Don Ernesto, el Funerario
**"Abrí una tumba después de 10 años: esto es lo que de verdad queda"**

Fecha: 7 de noviembre de 2026 · Canal: Don Ernesto, el Funerario (ES) · Mexicano, Guadalajara, usted.

---

## 1. Resultado

| | |
|---|---|
| Video | `D:/rtmp/fe12ds/final.mp4` |
| Duración | **23 min 45 s** (1 425,033 s medidos con ffprobe; voz 1 425,021 ms → desvío 0,012 s) |
| Formato | 1920×1080 · 30 fps · H.264 CRF 20 · AAC 192k estéreo |
| Voz | Fish `ernesto_es`, master `voz/master.wav` (1 425 021 ms) |
| Fotos | **244** en `fotos/` (30 JPG + 214 PNG), **170 distintas** usadas en pantalla |
| Planos | **323** en `shots_timed.json`, 0 huecos, de 0 a 1 425 021 ms |
| Clips | 0 (b-roll todo con fotos + Ken Burns; regla del creador: Veo sólo con presentador) |
| Avatar | 18 clips InfiniteTalk (A000–A017), **75,7 s** de pantalla |
| SFX | 6 cues suaves (tela, puerta, tierra, madera, papel, campana) |
| Música | **Ninguna** (ver nota al final) |

---

## 2. Costos

| Ítem | Costo |
|---|---|
| Voz (Fish) | US$ 0 |
| Fotos (Nano Banana / cola avatarity + desvío gpt-image-2) | US$ 0 |
| Transcripción (Groq free) | US$ 0 |
| SFX (Mixkit) | US$ 0 |
| **Avatar (InfiniteTalk, 1 sola llamada, job `6142b0ee`)** | **US$ 0,25** |
| Guion (DeepSeek) | incluido en la suscripción del panel, sin cargo por video informado |
| **Total** | **US$ 0,25** |

No hubo re-llamada de pago: el job quedó en estado `ok` y se adoptaron sus 18 cortes.

---

## 3. Problemas y cómo se resolvieron

### 3.1 El reel de InfiniteTalk salió truncado a 81 s (limitación seria)
La llamada única devolvió un reel de **81,11 s** cuando el plan pedía ~450 s. `avatar_it.py` cortó lo que pudo: **18 de las 102 ventanas** planificadas. Resultado: el avatar aparece **5,2 %** del video en vez del 25-30 % estilo Bertha, y hay un tramo largo sin avatar (245 s → final).

- Causa: truncamiento del reel de RunPod en esa corrida.
- No se pudo corregir: hay **una sola llamada por video** (guardado en `avatar/it_llamada.json`) y el guardián bloquea RunPod directo. No se cobró dos veces.
- Mitigación: las 18 ventanas se colocaron en las frases importantes y la apertura arranca con avatar real desde el segundo 0. El resto del video se sostiene con 323 planos de b-roll y cortes cada 3-4 s.
- **Queda anotado como desvío conocido del brief.**

### 3.2 17 segmentos del render salieron rotos (0-262 bytes)
Falta de memoria del sistema: `[WinError 1455] El archivo de paginación es demasiado pequeño`, `Cannot allocate memory`, `h264_slice_header_init() failed`. La máquina tenía ~20 ffmpeg de otros videos en paralelo y el commit llegó al 98 %.

- Arreglo: se borraron esos 17 `.mp4` **y** sus `.src`, y se re-renderizaron sólo esos: 0 errores, **336/336 segmentos válidos**.
- Además se rehízo la línea de tiempo con el lote completo de fotos (antes 36 fotos repetidas ~9 veces cada una; ahora 170 distintas, ~1,9 usos).

### 3.3 `assemble.py` (herramienta compartida) falló 4 veces por memoria
Fallaba al armar los tramos de **25 segmentos** por ffmpeg: `Cannot allocate memory`, `Error while filtering`, `Could not allocate memory`.

- **Reemplazo aplicado (autorizado por el brief: "si una herramienta falla 3 veces, poné un reemplazo"):** `assemble_local.py`, en mi propia carpeta. Reproduce exactamente la matemática de la herramienta compartida (`settb=AVTB,fps=30,format=yuv420p,setsar=1`, xfade con offsets en frames, CRF 16 por tramo y CRF 20 en la unión final, mismo mezclado de voz + SFX con `amix=normalize=0:duration=first`, `-ac 2 -c:a aac -b:a 192k`, mux final `-movflags +faststart`).
- Estructura real del armado: **56 tramos de 6 segmentos → 7 grupos de 8 tramos → 1 unión final** que ya lleva el audio mezclado en el mismo ffmpeg (`-map 7:a -c:a copy`), o sea **dos pasadas completas** en vez de tres, que era lo que hacía imposible entrar en el disco libre de la máquina.
- Resultado: armado completo sin errores de filtro.

### 3.3b Disco lleno durante el armado (episodio ENOSPC)
Los otros ~10 videos en paralelo bajaron D: a **21 MB libres** en un momento. Efectos: un `Error submitting a packet to the muxer: No space left on device` (`-28`) en `L1_005` (se resolvió solo con el reintento) y el proceso del ensamblador murió justo después de escribir `L1_005`, dejando `L1_006` en 786 KB.

- Para terminar se escribió `finish_local.py`, que **reaprovecha todo lo ya codificado** (los 56 tramos c*.mp4 y L1_000…L1_005 se validan por duración con `ffprobe`) y sólo rehace lo que falta, sin volver a tocar los `segments/` (que ya se habían borrado para liberar 411 MB).
- Se borró además el respaldo `final_v1.mp4` (592 MB) para ganar margen. No quedó copia de la versión anterior: se descartó a propósito porque usaba 36 fotos repetidas.

### 3.4 Cola de fotos lenta
La cola de avatarity repartía ~1 foto cada 5-10 min entre ~10 videos en paralelo. Se lanzó el lote igual, se siguió trabajando y el lote entero (157 fotos nuevas, cola `fe12ds_b`) llegó mientras corría el armado. Por eso se pudo rehacer la línea de tiempo con 170 fotos distintas.

### 3.5 Cambio del creador sobre el cuadro del avatar
Pedido (7-nov): el primer cuadro del avatar debía ser directo la foto `D:/rtmp/funerario/refs/ernesto_av.png`, no una generada.

- Aplicado en `avatar_ranges.json`: primera ventana (0-8 220 ms) con ese `frame`.
- **Pero** InfiniteTalk ya se había corrido (una sola llamada permitida) y los 18 clips se generaron desde `avatar/frames/a1.jpg` (la misma escena, 1280×720). El cambio queda como frame de referencia y respaldo de render. Anotado en `gates/correcciones_hechas.txt`.

---

### 3.6 Cambio de plataforma de render (aviso del creador, 8-nov)
Desde hoy el render y el armado se hacen en GitHub (`render.py` sube un paquete y ~14 máquinas lo procesan; `assemble.py` ya no hace falta) y el final queda en la nube (`final.url`, `final.nube.json`), sin bajar nada a la PC.

- Este video **ya tenía `final.mp4` bueno y validado** (1 425,033 s, 1920×1080, 30 fps, AAC estéreo, `validar.py --etapa final` OK) terminado antes del cambio, así que **no se re-renderizó**: la regla del creador es que un final bueno ya hecho sigue valiendo.
- Los scripts locales `assemble_local.py` y `finish_local.py` quedan sólo como registro de lo que se usó mientras la máquina aguantó; no se vuelven a correr.

## 4. Cumplimiento del brief

- ✅ Primer plano = avatar real hablando desde 0 s (ventana 0-8,22 s, ≤10 s).
- ✅ Primeros 30 s: cortes cada 2-3 s alternando gancho y avatar; ventanas ≤6 s.
- ✅ Gancho: 3 variantes (`gancho_a/b/c`) pedidas en el primer lote, elegida `gancho_c` con revisión visual (Read) y justificada en `gates/fotos_auto.txt`.
- ✅ Guion mexicano (Guadalajara, usted), ~23,75 min, gancho con número y objeto, credencial del presentador, prueba interactiva al min 4, cada punto = problema → anécdota fechada/nombrada/ubicada → por qué → cambio concreto con precio y fuente (Profeco / FTC Funeral Rule) → chequeo de esa noche; like/suscripción antes del último punto; cierre con pregunta y gancho al video siguiente.
- ✅ Sin "honesto", "genuinamente", relleno ni sermón; sin consejo médico; sin marcar el contenido como IA.
- ✅ Reglas de pantalla: nunca cuerpo, nunca rostro de alguien muriendo, sin sangre, tubos, agujas, ataúd abierto, restos ni huesos. Sí manos, espaldas, ventanas, cocina familiar, pasillos, objetos, tumbas, herramientas, papeles, avatar.
- ✅ Fotos: JSON completo (type, moment, subject, action, props 6-10, setting, light, camera, color, avoid), todas por la cola; ≥30 % primeros planos, ≥60 % con persona o manos; refs del presentador; linter pasado.
- ✅ Movimiento al azar con semilla fija (zoom/paneo, 5-13 %, foco variable), nunca el mismo tipo dos veces seguidas; escalado a 3840×2160 antes del zoompan; estrellita de Gemini recortada.
- ✅ Fundidos: 0,6 s avatar↔foto, 0,3 s foto↔foto (xfade), sin corte seco.
- ✅ SFX muy bajos (gain 0,04-0,07), sólo en momentos puntuales; sin música.
- ✅ Puntos de control guion / fotos / render / final con `gates/*_auto.txt` y `*_pedido.txt`, sin frenar el video.
- ✅ `validar.py --etapa final --min 25`: **RESULTADO OK**, 0 ✗ y 3 ! (los tres por el reel truncado del avatar, ya explicado en 3.1; el tercero pide sacar de `avatar_ranges.json` las ventanas sin clip, que se dejan a propósito porque no se puede re-renderizar el plan cerrado).
- ✅ Revisión visual del final: 48 cuadros cada 30 s en `qc/f_001..048.jpg`, 4 hojas de contacto leídas con Read. Sin cuerpos, sin rostros de personas muriendo, sin sangre, tubos, agujas, ataúd abierto, restos ni huesos. Audio con voz presente (media −22,5 dB, pico −6,3 dB).
- ✅ `gates/correcciones.txt` revisado en cada punto de control y antes del armado: **nunca existió**.

---

## 5. Qué falta / mejoras para la próxima

1. **Avatar:** el reel truncado es el problema más grande. Conviene verificar la duración del reel apenas termina la llamada y, si sale corto, decidir antes de cerrar el plan de ventanas (o dividir el video en dos llamadas si el guardián lo permitiera en el futuro).
2. **Memoria:** con ~10 videos en paralelo, correr render/assemble en horarios menos cargados o directamente con el ensamblador por lotes chicos ahorra las 4 fallas y ~40 min de reintentos.
3. **Fotos:** la cola sigue siendo el cuello de botella; pedir el lote completo en el primer tercio del trabajo.
4. **Música:** no se pudo descargar nada de YouTube Audio Library (requiere sesión y no hay herramienta de descarga autorizada). El video va sin música, sólo voz y 6 SFX suaves. Si el creador deja una carpeta de música local, se agrega en `assemble` sin re-renderizar (sólo remezcla de audio).

---

## 6. Archivos

`guion.txt` · `voz/master.wav` · `captions.json` · `avatar/` (18 clips + `avatar/frames/`) · `fotos/` (244) · `sfx/` (6) · `cues.json` · `shots_timed.json` · `avatar_ranges.json` · `plan.json` · `qc/` · `final.mp4` · `meta.json` · `gates/` · `assemble_local.py` y `finish_local.py` (reemplazos locales del ensamblador).

Los `segments/*.mp4` se borraron al terminar de fusionarlos (411 MB) para que entrara el armado; la lista exacta quedó en `xf_tmp/segs_manifest.json` y se reconstruyen con `render.py` si hace falta rehacer algo.
