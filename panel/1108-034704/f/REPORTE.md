# REPORTE · mk01ds — "My Kyoto Closet At 68: The 10 Things I Gave Away And Never Bought Again"

Canal: Michiko's Kyoto Closet · 08-nov-2026

## Qué se hizo

| Etapa | Resultado |
|---|---|
| Guion | `guion.txt`, 2.932 palabras, 19,4 min de voz. Diez prendas, reglas de Fumiko Arai, cierre "Stand straight." Sin "honest", sin "genuinely", sin "old", sin consejos médicos, precios en US$, temperaturas en °F. |
| Voz | Fish, voz `moda_michiko_ca`, 7 bloques → `voz/master.wav` (19,4 min). |
| Tiempos | Groq por palabra → `captions.json` (2.910 palabras, 0 → 1.161.628 ms). |
| Planos | `planos.py` → 147 planos de b-roll (12,6 por minuto) + `avatar_ranges.json` automático con 89 ventanas (488 s). |
| Fotos | 150 fotos (147 planos + 3 variantes del gancho) por la cola de avatarity, todas en una tanda + reintentos. `planos.py --shots` → 147 planos con 147 fotos distintas, cero repetidas. |
| Avatar | InfiniteTalk, 1 sola llamada (`avatar_auto.py`), 89 clips A0-A88 (488 s). Después de la revisión del revisor externo se reparó el fondo de los 88 clips A1-A88 (ver Problema 6) y se re-renderizó. |
| SFX | 6 sonidos (tela ×2, pasos, cremallera, lluvia, taza) mezclados bajos según `cues.json`. |
| Render | `render.py` en GitHub, 4 pasadas: (1) b-roll solo, 148 segmentos / 10 tandas / 4,9 min; (2) con los 89 clips de avatar, 323 → 629 MB; (3) recorte de cola (`fix_tail.py`); (4) **final tras reparar el fondo del avatar: 236 segmentos, 15 tandas, 10 máquinas, 6,9 min**. Se rehace sólo lo que cambia. |
| Final | `final_cc0f58b6b05e.mp4` · 19,4 min (1161,20 s) · 1920x1080 · 30 fps · H.264 CRF 20 bt709 · AAC 192k estéreo 48 kHz · **568 MB** · 0 huecos negros. Duración = voz (1161,18 s, ±0,3 s). Entregado como `final.url` en GitHub (no se bajó a la PC). |

## Costos

- Avatar InfiniteTalk: **US$ 0,25** (1 sola llamada por video; el job huérfano se adoptó por hash de audio, **no** se pagó un segundo /run).
- Fotos, voz, transcripción, clips y render: US$ 0 (colas compartidas y GitHub).
- DeepSeek: US$ 0 (no se usó).
- Revisor externo (visión): US$ 0,0124 la pasada final de 39 cuadros (`gates/revisor_final.json`).
- **Total: ~US$ 0,26.**

## Problemas y cómo se resolvieron

1. **8 fotos rechazadas con `INVALID_PAYLOAD "prompt": Expected string, received object`** (gancho_a/b/c, p002, p083, p087, p095, p136). La cola de avatarity (Nano Banana) exige `prompt` como string; las otras 142 las hizo gpt-image-2, que acepta el objeto. Solución: reencolar esos 8 con `prompt = json.dumps(objeto)` — sigue siendo el mismo JSON rico para el linter y la API lo acepta.
2. **Validador de avatar adoptado**: el primer intento de rescate murió con `UnicodeDecodeError … 0xe0`, porque este Python arranca en modo UTF-8 y decodificaba como UTF-8 la salida en cp1252 de `tasklist`. Se relanzó con `PYTHONUTF8=0`. El job de RunPod sobrevivió y se adoptó (sin doble cobro).
3. **Fotos rehechas (1 ronda, 4)**: p095 traía fecha impresa "2023.11.15" en el borde (regla dura: sin fechas); p043, p081 y p144 mostraban mujeres europeas donde debía estar la presentadora japonesa. Rehechas con prompt que fija mujer japonesa de ~68 y `avoid: western european face, blonde hair, blue eyes`. Las viejas quedaron en `cuarentena/`.
4. **Duración**: el guion salió de 19,4 min contra un objetivo de ~15. Es el desvío más grande del video; queda anotado abajo.
5. **Plan de avatar al ~40 %** (461 s de 1.161 s en el final; 89 ventanas / 488 s planificadas) cuando el estilo Bertha pide 25-30 %. Viene así de `planos.py`; no se tocó `avatar_ranges.json` (regla del creador).
6. **Fondo del avatar degradado (mosaico) — el problema más grande del video.** El revisor externo marcó 9 cuadros ("fondo glitch/distorsionado" en ~10:30, ~13:00, ~14:00, ~14:30, ~15:00, ~15:30 y "cara/mano deforme" en ~18:30 y ~19:00). El diagnóstico propio: 6 de los 8 segundos caían dentro de ventanas de avatar y el defecto era real, pero estaba en el **fondo**, no en la cara: el reel de InfiniteTalk (488 s en un solo /run) fue degradando el jardín de la izquierda, de bloques de color cada vez más grandes (desfase medido contra A0: 11 → 30 de media |dif| en la franja izquierda; A88 era el peor). Cara, manos y ropa siempre estuvieron enteras.
   Solución sin romper ninguna regla (ni `avatar_ranges.json`, ni un 2º /run, ni herramientas compartidas): se parcharon los **88 clips A1-A88** con el jardín limpio compuesto desde el cuadro de A0 (la misma escena de `michiko_av.png`), sobre la franja izquierda 0-32 % del ancho con degradado hasta 38 %, corrección de color por clip medida en la zona estática del shoji y borde difuminado; A0 quedó intacto (abre limpio). Duración, fps y audio de cada clip idénticos (ffprobe). Originales en `cuarentena/avatar_original/`. Re-render en GitHub → `final_cc0f58b6b05e.mp4`. Ver `gates/correcciones_hechas.txt`.

## Gates

- `gates/guion_auto.txt`, `gates/guion_pedido.txt`
- `gates/fotos_auto.txt`, `gates/fotos_pedido.txt`
- `gates/render_auto.txt`, `gates/render_pedido.txt`
- `gates/final_auto.txt`, `gates/final_pedido.txt`
- Revisor externo: 1ª pasada sobre el final anterior, 9 marcas (`gates/correcciones.txt`) → todas aplicadas (`gates/correcciones_hechas.txt`). 2ª pasada sobre `final_cc0f58b6b05e.mp4`: **39 cuadros, 0 malos** (`gates/revisor_final.json`).
- `validar.py --etapa final`: **RESULTADO: OK** (0 ✗; quedan los 3 avisos `!` de abajo, todos anotados).

## Avisos del validador (no frenan)

- Guion de 2.931 palabras para 15 min (esperado 1.657-2.587). Es la duración real de esta historia; no se recortó para no romper el ritmo.
- La palabra "patient" aparece 1 vez ("be patient with the fabric"). No es consejo médico; se deja.

## Mejoras para la próxima

1. **Guion más corto**: 2.931 palabras dieron 19,4 min cuando el objetivo era ~15. Para la próxima, contar palabras del guion antes de generar la voz (2.100-2.300 palabras ≈ 15 min) y apuntar a 10 prendas en frases de 2-3 líneas.
2. **Cortar el reel de InfiniteTalk**: el mosaico del fondo crece con la duración del reel. Con ventanas de avatar más espaciadas o pidiendo clips más cortos por tanda (varios /run de ≤150 s en vez de uno de 488 s) el fondo no llegaría a degradarse. Acá no se pudo (1 llamada por video) y se parcheó después.
3. **Estilo Bertha dentro de rango**: revisar el plan de `planos.py` antes de correr el avatar; el 40 % sale del plan automático (cada ~11-13 s) y el ideal es 25-30 % con ventanas de 3-6 s en las frases importantes.
4. **Revisión del avatar antes del render**: medir el desfase del fondo contra A0 en cuanto llegan los clips (`medir_fondo.py`) y parchar antes del primer render, no después de tres pasadas.
5. **Cupo y errores de la cola**: los 8 prompts que fallaron con `INVALID_PAYLOAD` eran por mandar el JSON como objeto a Nano Banana; en la próxima, `prompt` siempre string (`json.dumps`) para las prio 0.
