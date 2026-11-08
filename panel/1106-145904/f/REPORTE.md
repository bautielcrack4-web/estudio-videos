# REPORTE — mk10ds · "9 Japanese Hair Rules After 60 That Take 10 Years Off Your Face"

Canal: Michiko's Kyoto Closet · 6-nov-2026

## Qué se hizo
- Guion de 2.523 palabras (~16,6 min de voz), sin la palabra "old", precios en US$, temperatura en °F, sin consejos médicos y sin música.
- Voz: Fish `moda_michiko_ca` con `--keep-tags` → `voz/master.wav` (998,0 s).
- Captions palabra por palabra con Groq (`captions.json`, 2.502 palabras con tiempos).
- Avatar con lipsync: agnes-video-2.5-flash modo reference, cara `D:/rtmp/michiko/refs/michiko_face_hd.png`, 8 clips (A1-A5 intro, R1-R3 regresos) = 50,34 s en pantalla; todos los tramos de los primeros 30 s ≤ 6 s; regresos de 8-10 s.
- B-roll: 184 fotos en `fotos/` (179 ids únicos para 198 planos), todas por la cola de avatarity (Nano Banana), prompts JSON de 10 campos con momento/acción/props/cámara.
- SFX: 5 cues muy bajos (spray, agua, clip, toalla, secador), sin música.
- Armado: `render.py` (Ken Burns al azar, 3840x2160 → 1080p) + `assemble.py` (xfade 0,6 s avatar / 0,3 s foto, voz, SFX).

## Números
- Duración final: 998,00 s (voz 998,00 s, diferencia 0,0 s)
- Fotos: 184 archivos · 179 ids únicos · 198 planos
- Clips de avatar: 8 (agnes), 50,34 s
- Segmentos renderizados: 196/196
- Rehacer/repeticiones: c15→c15b (texto de marca legible), w05→w05b (2 rechazos de política), d06 e i12 reencoladas, S14 re-mapeado de x01-x16 a i01-i16, 1 re-render del tramo R2 por error de x264.
- Costo: DeepSeek US$0,00 (sin uso) · agnes US$0 (cuenta gratuita) · Nano Banana US$0 (cola) · Fish US$0 · Groq US$0

## Problemas y soluciones
- Colisión de ids: las fotos de intro i02-i07 y la tanda final i01-i16 se pisaban. Solución: copié las de intro a n01-n06 (misma imagen, mismo prompt) y el cierre usa i01-i16, que sí tienen registro en la cola.
- w05 falló dos veces con CONTENT_POLICY_VIOLATION (hablaba de cuero cabelludo): prompt reescrito como escena de raya en el baño (w05b) y aceptado.
- c15 salió con cajas de tinte con marca legible: reencolada como c15b con etiquetas en blanco y sin rostros; reemplazada.
- i12 y d06 no salieron en su tanda: reencoladas en lotes propios, llegaron y se verificaron.
- A5 tardó más que el resto (cola de avatar): se renderizó su tramo con el primer cuadro y se re-renderizó al llegar el clip.
- Un segmento de R2 falló una vez en x264 ("Generic error in an external library"); el clip de avatar estaba intacto y el segmento se re-renderizó bien.
- 6 fotos n01-n06 aparecen sin registro en `hechos/` porque son copias locales de originales que sí salieron de Nano Banana; el validador las cuenta como aviso y quedan dentro de la tolerancia del 5 % (184 fotos → 9).

## Cierre
- Validador final: OK (guion, fotos, render, final, meta y reporte). Sólo queda el aviso informativo de las 6 copias n01-n06; no es falla.
- Revisión visual completa: 33 cuadros cada 30 s (qc/f_*.jpg) en tres hojas; aprobado.
- `gates/correcciones.txt`: sin pedidos del revisor al momento del cierre.

## Pendiente / mejoras
- Nada pendiente de contenido. Para la próxima: pedir las tandas de cierre con ids propios desde el principio (i01-i16 no deberían compartir espacio con la intro) para no depender de copias locales.
- Se podría sumar un clip de Veo del presentador en la intro para variar el plano, pero el brief lo dejaba opcional y el cupo quedó para otros videos.
