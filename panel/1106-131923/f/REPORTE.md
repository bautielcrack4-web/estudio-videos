# REPORTE — Why Japanese Women Bathe at Night After 50

## Video final
- Archivo: `D:/rtmp/exprb/final.mp4` — 1090.63 s (18:10.6), 1920x1080, 30 fps, H.264 CRF 20, AAC 192k, 258.1 MB.
- Diferencia con la voz: 0.01 s (voz 1090.643 s). Dentro de ±0.5 s.
- Cortes: 248 en total — 9 planos de avatar (Reiko a cámara: intro + 3 regresos, 72.8 s) + 13 clips de b-roll animados (67.4 s) + 226 fotos animadas con zoom/pan (resto). Sin texto en pantalla, sin música ni gráficos; 11 fundidos cortos a negro.

## Gasto
- OpenAI (gptimg): 239 imágenes generadas, 0 fallidas → ≈ US$0.48 (fórmula low + Batch + 1088x608).
- Fish Audio: gratis (voz `reiko_en`, 263 oraciones, −14 LUFS).
- agnes: Starter (ya pago). Video generado: 9 clips de avatar (72.8 s) + 13 clips de b-roll (67.4 s) = **140.2 s** de un máximo de 500 s/día.
- RunPod / ElevenLabs / Modal: US$0.

## Tiempos por etapa (6 nov)
- Voz Fish + unión + normalización −14 LUFS: cerrada 12:09 (`voz/voz.wav`).
- Timings por oración (ASR) y agrupado en 235 grupos: 12:12–12:15.
- Imágenes gptimg: 3 tandas (incluye 4 rellenos b235–b238); última terminada 12:38.
- Avatar agnes (4 partes en paralelo, 9 chunks): terminado 12:52.
- Clips b-roll agnes: 13/30 terminados; el resto se bloqueó por cuota a las 13:05 (ver abajo).
- Render de 248 segmentos (ffmpeg zoompan / setpts / tpad): 13:05–13:08.
- Encode final (concat + AAC): 13:08–13:10.

## Qué falló y cómo se resolvió
1. **Cuota de video de agnes agotada.** Al lanzar los 17 clips restantes con concurrencia 8, la API rechazó: *"You have used up today's video generation quota and are now limited to 1 request every 5 minutes. Try again after 16:03:00"*. No se podía esperar ~3 h ni generar 17 clips a 1 cada 5 min, así que los 17 planos sin clip se resolvieron con sus fotos ya generadas (zoom/pan), que es el formato previsto para el resto del video. Resultado: 13 clips animados en lugar de 30; el video sigue completo y sin huecos.
2. **Primer lanzamiento de clips b-roll falló entero ("NO IMG")** porque pasé los nombres sin el prefijo `b` (`003,…` en vez de `b003,…`). Relanzado con los nombres correctos.
3. **Job de avatar cortado por límite de tiempo del entorno** a mitad de camino. Relanzado en background con timeout largo; reanudó desde los chunks existentes y terminó los 9.
4. **Crash de `lastFrame` del avatar** por "Non full-range YUV is non-standard" al extraer el último frame como JPEG. Se cambió a PNG con `-update 1` y 3 reintentos; los 4 chains terminaron con `Promise.allSettled`.
5. **`build_plan.py` fallaba** si faltaba un clip de avatar (ffprobe non-zero). Ahora `dur()` devuelve 1.0 si el archivo no existe, y un clip solo se usa si el mp4 existe y pesa >100 KB (fallback automático a foto).
6. **4 huecos de cobertura** entre el final de un bloque de avatar y la primera oración (23.44–30.00 s, 345.15–348.50 s, 600.49–605.63 s) se rellenaron con fotos extra b235–b238 generadas con gptimg.

## QC
- 12 frames distribuidos (30…1020 s) revisados en hoja de contacto: sin texto quemado, sin marcas de agua, sin manos rotas, sin frames negros; agua/vapor/telas coherentes con lo narrado.
- 4 frames de los regresos de avatar (3, 334, 588, 1076 s): misma mujer de 55, blusa de lino gris-azul, baños de Osaka distintos, gestos naturales (mano alzada, paño sostenido), sin texto.
- Audio: −14 LUFS integrado, LRA 3.2; `silencedetect` a −35 dB / 0.9 s no reporta cortes.
- Duración video vs voz: 1090.633 vs 1090.643 s.

## v2 — fotos gpt-image-2
- Archivo: `D:/rtmp/exprb/final.mp4`. Es de 1090.633 s, 1920x1080, 30 fps (32719 cuadros, igual que el plan), H.264 CRF 20 y AAC 192k. Pesa 395.8 MB.
- Voz: la misma master de v1 (`voz/voz.wav`, 1090.643 s). El video queda a 0.010 s de la voz y la pista AAC dura 1090.618 s.
- Respaldo de v1: `final_v1_agnes.mp4` (renombrado) y `broll_v1_agnes/` (copia de las 239 fotos agnes de 1312x736). No se borró nada; `segments/` (v1) quedó intacto.

### Qué cambió
- `broll/` ahora tiene las 239 fotos de `fotos_gpt/out_v2/` (b000–b238, 1088x608), que reemplazan a todas las de agnes.
- Se sacaron los 13 clips animados de agnes (b003, b013, b019, b022, b030, b037, b050, b051, b056, b070, b072, b085, b089) porque mostraban las fotos viejas. Esos planos ahora usan su foto nueva con Ken Burns, así que los 239 planos de b-roll son fotos gpt.
- Movimiento nuevo (`tools/render_v2.py`, adaptado de `mk02ds/tools/render.py`):
  - Cada foto tiene un movimiento al azar (`plan_motion` con semilla fija 20261106) entre in, out, izq, der, arriba, abajo, diag_in y diag_out, y nunca repite el mismo tipo dos veces seguidas.
  - Intensidad y punto de foco al azar, con arranque y frenada suaves (coseno).
  - Antes del zoompan la foto se escala a 3840x2160 (sin temblor) y se aplica eq saturation 0.92.
  - Se **quitó el crop de la marca de Gemini** (`crop=trunc(iw*0.91/2)*2…`), porque las fotos gpt no tienen marca.
- Fundidos (`tools/assemble_v2.py`, adaptado de `mk02ds/tools/assemble.py`, sin SFX porque v1 no tenía):
  - Fundido xfade de 0.6 s entre avatar y foto, y de 0.3 s entre foto y foto. Cada segmento lleva su cola de cuadros extra, así que los tiempos no se corren (`segments_v2/xf.json`).
  - Entre trozos de avatar contiguos el corte es seco.
  - Se sacaron los 11 fundidos a negro de v1, que quedan reemplazados por los xfade.
- Avatar: los mismos 9 `av_clips` y los mismos tiempos y tratamiento que v1 (escala, recorte y tpad, sin eq). Solo se agrega la cola de 0.6 s donde el avatar funde a foto.
- Arreglo en `assemble_v2.py`: el original de mk02 fallaba al mezclar `concat` (corte seco) con `xfade` por timebase distinto (AVTB vs 1/30). Ahora todas las entradas y salidas van con `settb=1/30`.

### Tiempos (6 nov)
- Render de 248 segmentos a `segments_v2/` (6 en paralelo): 13:53–13:56, unos 3 min, 0 errores.
- Ensamblado (10 tramos xfade + unión + voz): 13:57–14:14, unos 16 min.

### QC
- `qc_v2/hoja_final.jpg`: hoja de 12 cuadros, de 20 s a 1010 s cada 90 s.
  - Se ven el avatar (Reiko en el baño) y 11 fotos gpt: baños y cocinas japonesas, manos, agua y una mujer mayor.
  - Sin texto quemado, sin marca de agua, sin cuadros negros y sin manos rotas visibles.
- `blackdetect` (d 0.1 s, pix_th 0.10) sobre todo el video: no detectó ningún tramo negro.
- `silencedetect` (−35 dB, 0.9 s) sobre el audio final: no detectó ningún silencio.
- Video y voz: 1090.633 s contra 1090.643 s (diferencia de 0.010 s).
- Script de QC: `tools/qc_v2.sh`.
