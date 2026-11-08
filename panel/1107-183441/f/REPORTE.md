# REPORTE — "The 7 Things the Funeral Home Never Tells You Before You Sign"

Canal: Ernie Navarro, Funeral Director · 8-nov-2026 · carpeta `D:/rtmp/fn09ds`

## Lo que quedó

- **Duración:** 26 min 32 s (final 1591,83 s vs voz master 1591,79 s; ±0,3 s).
- **Formato:** 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192k estéreo.
- **Guion:** 4176 palabras, sin "honest"/"genuinely"/relleno; 2 tags de emoción de Fish; sin palabras médicas.
- **Voz:** Fish (`ernie_en`), 1 master + bloques, `--keep-tags`.
- **Fotos:** **309 archivos** en `fotos/` — **cero repetidas**: cada plano tiene su propia foto (regla del creador "un video nunca repite imagen"). Las 165 fotos del primer armado que se repetían se reemplazaron por 165 fotos nuevas únicas (3 lotes `r001…r165`, por la cola avatarity → desvío gpt-image-2; las de prio 0 siguen por Nano Banana). Incluye 6 creativas de GPT con su `detalle_narrativo`.
- **Avatar:** InfiniteTalk, **1 sola llamada**; 117 ventanas de 478,5 s = **30 % del video**, 3-6 s cada ~11-13 s, nunca más de 20 s sin avatar; primer cuadro = `D:/rtmp/funerario/refs/ernesto_av.png` (foto de ChatGPT web, máxima calidad, sin regenerar) y todas las ventanas con ese mismo `frame`.
- **Plan:** 407 planos (290 de foto + 117 de avatar), cortes cada 3-4 s, 0→1591,8 s sin huecos, 0 huecos negros.
- **SFX:** 9 cues (`cues.json` en la raíz + copia en `sfx/`): papel, puerta, vaso, teléfono, llaves, cajón. Sin música (a propósito para este canal).
- **Archivos:** `final.url` (+ `final.nube.json`) apuntando al final publicado en GitHub, `meta.json` (título + descripción en 3 párrafos con la voz de Ernie, sin links ni hashtags de IA), `qc/` con hojas de control (`hoja_final_0..4.jpg`, `hoja_repes.jpg`, `hoja_fotos.jpg`, `hoja_render.jpg`) y 53 cuadros cada 30 s.
- **Entrega:** `final.mp4` local (737.451.194 bytes) bajado del release `est-fn09ds` del repo de la herramienta de nube (se bajó antes del aviso de "final sólo en GitHub"; el aviso dice que un final.mp4 bueno ya hecho sigue valiendo), más `final.url` / `final.nube.json` con la fuente: `https://github.com/bagasy-search/claudeyoutubevideos/releases/download/est-fn09ds/final_58c0f673fdb4.mp4`. `render.py`/`assemble.py` nuevos trabajan en la nube por defecto; el asset se descargó y se verificó con `ffprobe` (1591,829 s, 1920x1080, 30/1, h264 + aac 48k estéreo, 737 MB = tamaño del asset).

## Costos

- Avatar InfiniteTalk (RunPod): **US$0,25** (1 ejecución, reel 513,23 s, cuenta RUNPOD_API_KEY_10).
- Fotos b-roll: por la cola compartida (gpt-image-2 batch low 1088x608 y Nano Banana para prio 0) — sin costo directo medible desde esta carpeta.
- Voz Fish, transcripción Groq, cola de fotos, render cloud (GitHub Actions): gratis.
- DeepSeek: sin gasto propio registrado en esta carpeta.

## Problemas y cómo se resolvieron

1. **165 fotos repetidas** (la primera tanda reutilizaba archivos en varios planos). Se detectaron con `slots_repes.py`, se generaron 165 prompts nuevos con la misma estructura JSON (moment/action/props de 6-10 objetos/camera variada), pasaron `lint_fotos.py` en 3 lotes (7 rechazos corregidos: "nobody", "catalog", "empty", props de 2 palabras) y `aplica_repes.py` reescribió `shots_timed.json`: **reemplazados 165 de 165**. El validador pasó de ✗ "fotos repetidas: 165" a ✓ "ninguna".
2. **La herramienta del avatar murió a mitad del renombrado.** InfiniteTalk terminó el reel (513,23 s) y el cortador dejó 117 `.tmp.mp4`, renombró 97 y murió antes de escribir `it_sync.json`. `finish_avatar.py` terminó el renombrado (97 → 117) y reconstruyó `it_sync.json` midiendo cada clip. El desfase ya venía corregido en cada corte (máximo medido 0 ms).
3. **La cola de fotos entregaba ~1 cada 4,7 min** (112 pendientes ≈ 8 h). Causa: el despachador había muerto por un error de archivo en `turnos.json`; `estado.mjs` lo levantó de nuevo. Además el desvío `fotos_gpt.mjs` no estaba corriendo: al arrancarlo volvieron a entrar los lotes y las fotos pasaron de 33 a 146 en ~40 min; con los 3 lotes de reposición se llegó a 309.
4. **Reparto en dos slugs** (`fn09ds` y `fn09ds_b`) para que la cola despachara dos imágenes por turno en vez de una.
5. **Las fotos del desvío GPT llegan como `.png`, no `.jpg`.** Un `esperar.py --cuenta "fotos/r*.jpg" 165` marcó 9/165 cuando en realidad estaban 156; con `r*.png` coincidió y `aplica_repes.py` (que prueba `.jpg/.png/.jpeg`) confirmó las 165.
6. **Render:** en la etapa local 7 segmentos fallaron por falta de memoria con 6 workers (`Cannot allocate memory` en PNG/libx264). Se re-corrió con `RENDER_WORKERS=2` y quedaron los 407. En la corrida final del arreglo de repetidas, `render.py` (default nuevo) hizo todo en la nube: 407 clips / 47.755 cuadros en **7,7 min**, y el armado completo en **26,5 min** (737 MB).
7. **Assemble local:** los intentos fallaron por OOM y por disco lleno al unir tramos de 25 segmentos (28 ffmpeg de otros videos en paralelo). Se resolvió con un armador propio (`asm_resume.py`): misma matemática de fundidos de `xf.json`, fusión en dos niveles (10 → 6), valida cada tramo por duración, reintenta y borra los insumos usados. Ya no hace falta: el armado final lo hizo la nube.
8. **`assemble.py` lee `cues.json` de la raíz del video**, no de `sfx/` (los archivos de sonido sí van en `sfx/`). Se copió `sfx/cues.json` → `cues.json`; sin eso el armado salía sin SFX.
9. **Sin campana de iglesia en Mixkit** para el cierre: se cerró con cajón/papel en vez de campana.
10. Los planos con id "avatar" del plan imprimen `FALTA IMG avatar` en el log: es ruido, el avatar lo ponen las ventanas de `avatar_ranges.json`.
11. **Muertes silenciosas de ffmpeg y de python (rc=1, sin stderr).** No era OOM: `D:/rtmp/dspanel/tools/guardia_render.py` (8-nov) mata cada 20 s todo `ffmpeg.exe` cuyo comando incluya `D:/rtmp|segments|xf_tmp` y esté codificando video, y hace `taskkill /T` al python que lo lanzó. Se creó `D:/rtmp/render_local_permitido.txt` (bandera de excepción documentada en el mismo guardián) para poder codificar en la PC durante la etapa local; **se borra al cerrar este video**. Con el render en la nube la bandera ya no se necesita.
12. **Las herramientas compartidas cambiaron su default a nube** (`render.py` líneas 178-208): sin `RENDER_LOCAL=1` + bandera + sin `--limit`, sube los assets a GitHub Actions y publica el `final.mp4` como asset de release. Un intento intermedio subió 242 archivos y arrancó la corrida 42442996718; se canceló y se borró para no dejar artefactos. La corrida final (42458931889) se dejó completa: es la que produjo el entregable.

## Mejoras para la próxima

- Encolar el b-roll **sin repetir ids** desde el principio (`un id = un plano`): evita el lote de reposición. Revisar con `slots_repes.py` antes del primer render.
- Arrancar `fotos_gpt.mjs` antes de encolar: sin el desvío la cola va de a una imagen y se hace inviable.
- Contar fotos con glob `*` (o `.png` incluido): el desvío GPT escribe `.png` y los conteos con `*.jpg` dan falsos negativos.
- Dejar el corte de las ventanas del avatar en un proceso aparte, o correr `finish_avatar.py` como paso fijo después de `avatar_it.py`.
- Revisar `estado.mjs` de la cola cada ~30 min: el despachador se cae solo y no avisa.
- Aceptar el render en la nube como camino normal cuando el guardián local esté activo: 407 clips en 7,7 min y final en 26,5 min, sin tocar el disco local. Ya no es necesario `asm_resume.py` ni la bandera `render_local_permitido.txt`.
- Si en algún momento vuelve a hacer falta el armado local: dejar ≥6 GB libres en D: (tramos + `video_noaudio.mp4` + `final.mp4` pesan ~3-4 GB) y usar `RENDER_WORKERS=2`.
