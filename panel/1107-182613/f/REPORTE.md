# The Last Thing Dying Parents Do With Their Hands — Hospice Chaplain Rosa

## Lo que es

Video de **33 min 22 s** (2002,11 s de voz), **1920x1080**, **30 fps**, **H.264 CRF 20**,
**AAC 192k estéreo** (48 kHz). 998 MB.
Presentadora: Rosa, capellán de hospicio de 34 años, San Antonio (West Side), esposa de Ernie Navarro.
En ninguna parte del video se dice que sea IA. Sin música (la biblioteca de audio de YouTube no
está disponible desde este entorno). Sin consejos médicos: Rosa es capellana, nunca enfermera.

## Lo que se hizo

| Etapa | Herramienta | Detalle |
|---|---|---|
| Guion | DeepSeek | 5.695 palabras, gancho con número (34 años / 3.000 familias) y objeto, prueba interactiva, 5 puntos, like/subscribe antes del último punto, pregunta al cierre + gancho al siguiente video |
| Voz | Fish `rosa_mx` | 12 bloques, 3 tags de emoción con `--keep-tags`, `voz/master.wav` |
| Transcripción | Groq | tiempos por palabra (`captions.json`), precisión ~50 ms |
| Avatar | InfiniteTalk (`avatar_it.py`) | 121 ventanas, 527,9 s = **26 %** del video, 1 sola llamada — US$0,25 |
| Fotos | cola avatarity (Nano Banana) | **146 fotos** usadas en 150 planos cortados a tiempos de palabra |
| Creativas | cola (gpt-image-2) | 4 imágenes creativas con `detalle_narrativo`, revisadas una por una |
| SFX | Mixkit (`sfx_doc.mjs`) | 7 cues bajos, anclados a palabras del guion |
| Armado | `render.py` + `assemble.py` | 336 segmentos, fundidos 0,6 s avatar↔foto y 0,3 s foto↔foto |

## Costo

- Avatar InfiniteTalk: **US$0,25** (una sola llamada).
- DeepSeek (guion): **US$0,00** (modelo del panel).
- Fotos, voz, transcripción, SFX, render: gratis (colas compartidas / APIs gratuitas / GitHub Actions).

## Reemplazos y fotos rechazadas

- **o11** y **w02**: retiradas antes del render por mostrar la cara de una persona muriendo;
  movidas a `fotos_no/` y reemplazadas en el plan.
- **d01**: mostraba a un hombre mayor en la cama con la cara visible y el brazo levantado
  (144,5-156,1 s). Viola la regla dura del brief. Reemplazada por **d01c**: sólo las manos y
  antebrazos de un mecánico de 82 años en su banco de trabajo (caja de herramientas roja con
  cinta, lata de tornillos, reloj de servicio, anillo de casamiento), sin cara. Se re-renderizó
  sólo ese segmento y se rearmó el video completo. Verificado en `qc/chk_0150s.jpg`.
- Fotos repedidas antes del render: 6 de prueba + 2 más en la revisión de hojas de contacto
  (fecha impresa / look de estudio).

## Problemas

1. **La cola desvió la foto de reemplazo a gpt-image y falló** con `400 INVALID_PAYLOAD`
   ("prompt: Expected string, received object"): el desvío no acepta el prompt JSON como objeto.
   Se repitió el pedido con el prompt serializado como texto y salió bien (es la única foto del
   video que no salió de Nano Banana; queda como aviso del validador).
2. **El proceso de armado murió dos veces sin error** después de "render en GitHub listo"
   (posible presión de memoria del `gh` al bajar el asset de 998 MB). Se relanzó `assemble.py`,
   se enganchó a la corrida ya hecha y terminó: release `est-hr06ds`,
   asset `final_8ae7c8712c43.mp4`, 22/22 máquinas en 8,6 min. El asset se bajó a `final.mp4`
   con `gh release download`.
3. **`fotos/t06.png` está corrupto** (ffmpeg sale con 4294967268); queda sin usar y excluido
   de las hojas de contacto.
4. **Avisos del validador que no frenan:** guion de 5.695 palabras (rango largo del brief);
   2 huecos de 0,4 s en 766,9-767,3 s que quedan debajo de una ventana de avatar (no se ve
   negro); 86 fotos duran más de 8 s en el plan, pero `render.py` parte cada foto en los tramos
   de avatar, así que el corte visible es cada ~4-5 s (mediana 5,00 s, 67 % ≤6 s).
5. **Sin música** (biblioteca de YouTube no disponible) y **sin clips de Veo**: todo el b-roll es
   foto con Ken Burns aleatorio (zoom/paneo sorteado, sin patrón, supersample 3840x2160).

## Estado

- `final.mp4` completo y validado: `validar.py --etapa final` → **RESULTADO: OK**, sin ✗.
- Duración del video = duración de la voz (2002,108146 vs 2002,108141 s).
- `meta.json` con título y descripción listos para subir (sin links, sin hashtags de IA).
- Puntos de control en `gates/`: guion, fotos, render y final (auto + pedido). No había
  `gates/correcciones.txt` del creador.
