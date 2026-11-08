# REPORTE — mk13ds

**Video:** "Japanese Women Over 60 Wear Jeans Too — Only Differently (I'm 68 and Not Model-Thin)"
**Canal:** Michiko's Kyoto Closet · inglés · 16 min 32 s · 1920x1080 30 fps

## Estado (cerrado 6-nov 18:15)
- [x] Guion aprobado (compuerta guion OK, `gates/guion_ok.txt`)
- [x] Voz: Fish `moda_michiko_ca` → `voz/master.wav` 991,97 s
- [x] Timings por palabra: Groq → `captions.json` (2.493 palabras)
- [x] 163 fotos de b-roll + apertura (op1b) + 4 reemplazos, todas por Nano Banana (cola avatarity)
- [x] `render.py`: 173 planos, 29.748 cuadros (991,60 s), 0 `FALTA IMG`, Ken Burns al azar
- [x] `assemble.py`: fundidos + voz + 6 SFX → `final.mp4`
- [x] `validar.py --etapa final --min 15` → **RESULTADO: OK**
- [~] Clips de avatar con lipsync: la cola de agnes no entregó ninguno (ver Problema 7). Los 7 tramos
      de avatar van con su primer cuadro como still; no impide la entrega.

**Salida:** `D:/rtmp/mk13ds/final.mp4` — 414.971.765 bytes, 991,97 s, H.264 CRF 20 + AAC 192k estéreo.

## Gasto
US$ 0. Voz (Fish), transcripción (Groq), fotos (Nano Banana / avatarity) y clips (agnes) salen de las
colas gratuitas compartidas. No se usó gpt-image ni Veo.

## Problemas y decisiones
1. **Cara chica en el primer A1.** El primer clip se hizo con `michiko_face.png` (128x192) y salía blando.
   Corregido: la cara va siempre desde `michiko_face_hd.png` (460x613 nativo). agnes rechazaba el PNG
   por tamaño de entrada, así que se guardó la MISMA imagen sin agrandar ni recomprimir a
   `avatar/face_hd_q98.jpg` (460x613, JPEG q98). El A1 viejo quedó como `avatar/A1_v1_cara_chica.mp4`.
2. **Apertura.** El segundo 0 es una FOTO (op1b): Michiko de pie en el tatami abriéndose la pretina
   del jean, mirando a cámara. Se probaron 3 variantes y se eligió la que sobrevive el recorte
   obligatorio de 0,91 con el cuerpo entero.
3. **Intro partida.** Los primeros 30 s alternan foto / avatar en tramos de ≤ 6 s, con `clipStartMs`
   listo para que la boca siga a la voz en cada corte cuando haya clip.
4. **Job D colgado** 30 min sin salida: se mató y se relanzó el plan completo con la cara HD.
5. **Procesos en segundo plano.** `nohup` se muere en silencio en esta máquina; los lanzamientos van
   con PowerShell `Start-Process -WindowStyle Hidden` y log a `qc/avatar_run.out`.
6. **Duplicado de avatar.** Quedó una sola corrida viva (PID 3668); se mató la otra (PID 34088) para
   no gastar cupo dos veces. No se tocó ningún proceso de otros chats.
7. **agnes saturado (bloqueante de avatar).** Desde las 15:53 la API devuelve `video_queue_full` a
   todas las cuentas, para todos los chats. El log del pool (`D:/rtmp/agnes_pool/log.jsonl`) tiene
   353 respuestas de tipo `queue` y **0 `ok`** para las etiquetas `mk13ds_avatar_*`: no es el pedido ni
   las claves, es el cupo global de la cola compartida. El proceso `avatar.mjs` (PID 3668) sigue vivo
   reintentando. Decisión (regla del KIT: nada frena el video): se armó el final con el **primer cuadro
   de cada tramo de avatar como still**, que render.py admite sin huecos. Cuando agnes entregue, se
   corre `tools/map_shots.py` → `render.py` (sólo cambian 7 segmentos) → `assemble.py` y se revalida.
8. **Herramientas compartidas.** Se usaron `render.py`, `assemble.py`, `avatar.mjs`, `hoja.py` y
   `validar.py` sin copiarlas ni editarlas. `plan.json` lo escribió `render.py`.

## Control de calidad
- `validar.py --etapa fotos`: OK (6 fotos de prueba + primeros cuadros del avatar).
- `validar.py --etapa render`: OK tras rehacer los primeros 30 s con la apertura foto.
- `validar.py --etapa final --min 15`: **OK**, 0 fallas.
- Revisión visual: 34 cuadros cada 30 s (`qc/final_frames/`) en 3 hojas (`qc/hoja_final_1..3.jpg`).
  Sin fechas, sin texto legible inventado, sin manos rotas, sin look de estudio; todas las escenas
  muestran a alguien a mitad de un gesto.
- `ffprobe`: 991,97 s (= voz ±0,0 s), 1920x1080, 30/1 fps, AAC 44,1 kHz estéreo.

## Pendiente (no bloquea la entrega)
- Reemplazar los stills de avatar por los clips con lipsync cuando la cola de agnes los entregue
  (A1, A2, B, C, D, E) y volver a correr `map_shots.py` / `render.py` / `assemble.py` / `validar.py`.
