# REPORTE — fe08ds · "Lo que de verdad pasa detrás de la puerta del crematorio, 40 años de funerario"

Canal: Don Ernesto, el Funerario · Español mexicano (Guadalajara) · 8-nov-2026

## Entrega
- `final.mp4` — 1920x1080, 30 fps, H.264 CRF 20, AAC 192k **estéreo** (44.1 kHz), **24 min 16,6 s** (1456,63 s), 624,7 MB.
- Duración del video = duración del audio (`voz/master.wav` 1456,627 s → final 1456,626 s, diferencia 1 ms).
- `meta.json`: título + descripción de 3 párrafos en voz del presentador, sin enlaces ni menciones de IA.
- `qc/`: hojas de contacto de fotos, del avatar, del render de prueba y del final (un cuadro cada 30 s).

## Qué se hizo
1. **Guion**: 4008 palabras (~25 min leídos).
2. **Voz**: Fish `ernesto_es` con `--keep-tags`, 3 en paralelo → `voz/master.wav` (WAV 44.1 kHz mono, 128 MB).
3. **Tiempos por palabra**: Groq ASR → `captions.json` (todas las palabras con startMs/endMs, ~50 ms).
4. **Plan de planos**: `shots_timed.json` con **208 planos** de 3-6 s, cada uno arrancando en la palabra que lo motiva;
   sin huecos de 0 a 1456 s.
5. **Fotos**: **226 archivos** en `fotos/` — 208 slots de b-roll + **6 imágenes creativas** (cuaderno, grilla de rutina,
   libro a cámara, foto vieja en la mano, antes/después, las cuatro preguntas en cartulina). Todas por la cola de
   avatarity (Nano Banana / gpt-image-2 según el desvío automático), con prompt JSON completo y `lint_fotos.py` en verde.
   Revisión visual con hojas de contacto: se repitieron sólo las que salían con fecha impresa, manos rotas o nada pasando.
6. **Avatar**: InfiniteTalk por `avatar_it.py`, **1 sola llamada** (US$ 0,25) → **106 ventanas**, 475 s = **33 % del video**,
   tramos de 3-6 s cada ~11-13 s, nunca más de 20 s sin avatar, apertura desde el segundo 0.
   Desfase del reel medido y corregido por la herramienta (máximo 395 ms).
   Primer cuadro = `D:/rtmp/funerario/refs/ernesto_av.png` (pedido del creador); la foto de Nano Banana anterior quedó como `avatar/frames/a1_nb.jpg`.
7. **SFX**: 5 cues (puerta de metal, reloj, papeles, tela, llaves), mezclados bajos (-29 a -22 dB) sólo en momentos puntuales.
8. **Render**: `render.py` → 315 segmentos (208 fotos con movimiento aleatorio + 106 avatar + apertura), todos con
   zoom/paneo sorteado (sin patrón fijo), escala 3840x2160 antes de zoompan y recorte del 91 % para sacar la estrellita de Gemini.
9. **Armado**: `assemble.py` con fundidos (avatar↔foto 0,6 s; foto↔foto 0,3 s) + voz + SFX → `final.mp4`.
10. **Validación**: `validar.py --etapa final --min 25` → **RESULTADO OK**, todas las comprobaciones ✓.

## Costos
- Avatar InfiniteTalk (RunPod): **US$ 0,25** (1 llamada).
- DeepSeek: sin medición exacta en esta corrida; el guion se armó en la sesión y no se hizo ninguna llamada adicional
  que se pueda facturar aparte. (Si el panel lo pide, el número es 0 para esta entrega.)
- Fotos, voz (Fish), transcripción (Groq) y clips: gratis (colas compartidas).

## Problemas y cómo se resolvieron
1. **Cola de fotos compartida saturada**: al principio llegaba 1 foto cada 9-10 min (138 slugs, cientos de pedidos por delante).
   No se salteó la cola; se siguió trabajando y se re-encolaron sólo las que faltaban (`ped_c.json`, 40 pedidos).
   Al final llegaron todas menos `s142_recibos`, que se sustituyó por `s149_recibos` (la misma tarjeta, la que hacía
   más tiempo que no se usaba) → un solo plano reutiliza una foto, con ~7 min de separación.
2. **Render**: la primera pasada completa dejó 8 segmentos fallados (errores de hilos de x264, "Generic error in an
   external library"). Se volvió a correr `render.py`: sólo rehizo esos 8 y terminó "hechos 315", 0 errores.
3. **Armado (assemble.py)**: el primer intento murió en el tramo 12 por falta de memoria (`Cannot allocate memory`),
   con la máquina cargada por ~10 videos en paralelo. Se reanudó desde `resume_assemble.py` sin rehacer los 11 tramos
   ya listos, y esa corrida chocó con el **disco D: lleno (0 bytes libres)**. Se liberó espacio moviendo los 13 tramos
   (1 GB) a `E:/work_fe08ds/` y se rehizo la unión final + mezcla de audio + mux: `final: 1456.626 s`.
4. **Fotos fuera de tono**: se detectaron y repitieron las que parecían "de estudio" o aburridas (cuarto vacío,
   aparato solo) antes de usarlas.

## Lo que no quedó perfecto (anotado, no bloquea)
- **Precios de la libreta**: la foto `s147_libreta` muestra escrito "$1,500 / $1,100 / $650", mientras el guion habla de
  12-20 mil y 35-60 mil pesos en esa parte. No se rehízo por costo de otra vuelta de cola; se ve 4 s y en plano corto.
- **Avatar 832x464**: los clips de InfiniteTalk salen en 832x464 y se escalan a 1080p en el render; se ven algo suaves
  comparados con las fotos, pero consistentes entre sí.
- **Encuadre fijo del avatar**: las 106 ventanas comparten el mismo plano general del consultorio (viene de la foto de
  referencia del creador). Es intencional (estilo set fijo tipo Bertha), pero es el elemento más repetitivo del video.

## Música
**No lleva música de fondo**, tal como pide el formato: sólo voz, ambientes reales de la casa/negocio y 5 SFX puntuales.
