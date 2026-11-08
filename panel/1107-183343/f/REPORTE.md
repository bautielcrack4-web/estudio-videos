# hr08ds · Hospice Chaplain Rosa — "Why Dying Parents Wait Until You Leave the Room"

## Entrega
- `final.mp4` — 1801,42 s (30:01), 1920x1080, 30 fps, H.264 CRF 20, AAC 192k estéreo, 772,6 MB.
- `meta.json` — título + descripción de 3 párrafos (1.723 caracteres) en la voz de Rosa.
- `guion.txt` — 5.145 palabras en inglés: gancho (número + objeto), credencial, la prueba del umbral (minuto 4), 7 puntos con problema → anécdota con fecha/nombre/lugar → por qué → cambio concreto con precio → chequeo de esta noche, like/subscribe antes del último punto y cierre con pregunta + gancho a hr09 (Walt Pruitt).
- Validación final: `validar.py --etapa final --min 25` → **OK**, sin ✗.

## Cómo se hizo
- **Voz:** Fish `rosa_mx` con `--keep-tags` (2-4 tags de emoción dentro del guion). `voz/master.wav`, 1801,27 s a 44,1 kHz.
- **Captions:** Groq ASR por palabra → `captions.json` (5.123 palabras). De ahí salieron los cortes cada 3-5 s de `shots_timed.json` (419 planos, sin huecos, 0 s a 1801,65 s).
- **Fotos:** 118 imágenes pedidas por la cola de avatarity (Nano Banana / gpt-image-2 de la cola, nunca llamados directo), 0 rechazadas por el linter. Todas con prompt JSON completo (`fotos/<id>.json` cuando no pasó por la cola). Hojas de contacto en `qc/fotos/hoja_01..10.jpg`, revisadas a ojo: sin fecha impresa, sin manos rotas, sin texto inventado. No hubo que repedir ninguna por calidad.
- **Imágenes creativas de GPT:** `cre_cuaderno_camara`, `cre_foto_vieja_mano`, `cre_grilla_rutina`, `cre_nota_mano`, `cre_estante_tarjetas`, `cre_antes_despues`, cada una con su capa de detalle narrativo inventada para este video (la hora escrita a mano en la grilla, la taza vacía en el después, la mancha de té sobre el paso 2).
- **Avatar:** InfiniteTalk, **una sola llamada paga** (`avatar/it_llamada.json`), US$ 0,25, 589 s de reel, **115 ventanas** estilo Bertha (31 % del video = 550 s, primera ventana 0-6,1 s, cortes de 3-6 s).
- **Sonido:** 6 cues de SFX puntuales (`sfx/`, `cues.json`, gain 0,04-0,06): puerta, teléfono, páginas, campana. **Sin música**, por decisión del brief.
- **Armado:** `render.py` + `assemble.py` (herramientas compartidas), corridos en la nube del estudio (GitHub Actions) para no pelear por memoria con los otros videos de la PC.

## El problema grande de este video: el desfase del reel del avatar
`avatar_it.py` no detectó que el reel de InfiniteTalk **perdió ~3,4 s de audio alrededor del segundo 115** y siguió perdiendo ~0,1 s cada 2 minutos (hasta -3,71 s al final). Su búsqueda por ventana es de ±1 s y descarta cualquier desfase mayor a 0,8 s, así que cortó **todas las ventanas desde el segundo 115 con la cara corrida ~3,4 s** respecto de la voz.

Qué hice, sin pagar una segunda llamada:
1. Decodifiqué reel y `avatar/it/voz.wav` a 2 kHz y armé un mapa de desfase por correlación de envolventes. Resultado: 0 s hasta ~110 s, escalón a -3,41 s desde ~120 s y -3,71 s al final.
2. `recut_all.py` volvió a cortar las 116 ventanas en `nom + lag(nom)` y verificó cada clip contra la voz: **113 cortadas, residuo medio 7 ms**.
3. Tres cortes fallaron por memoria de la PC y una ventana (`A23`) quedó sin audio en el reel: la busqué en todo el reel y **ese tramo no existe**. La descarté (no se puede sincronizar; clip archivado en `qc/A23_descartado.mp4`) y esa franja va con el b-roll de abajo. Las otras tres se recuperaron con `fix_faltan.py` (residuos 95 ms, 95 ms y 1 ms).

## Avisos que quedan (no rompen el video)
- **Hueco sin avatar de 28,5 s** entre 359,6 s y 388,1 s: es la consecuencia de haber descartado A23. En ese tramo hay 7 planos de b-roll de 4-5 s (manta, teléfono de noche, vecina, hija en la silla, monitor, uñas, loción). Rehacerlo implicaría otra llamada paga a InfiniteTalk, así que se dejó documentado.
- **Conteo de palabras:** el validador estima 2.762-4.312 palabras para 25 min y el guion tiene 5.145; con la voz de Rosa ese texto dura 30:01, que es lo que quedó en el video. No se recortó.
- **Duración:** el plan terminaba en 1801,65 s y la voz en 1801,27 s. Se recortó el final sin re-encodear a 1801,42 s (audio 1801,31 s, video 1801,40 s) para entrar en la tolerancia de ±0,3 s.

## Cambio del creador (8-nov): el primer cuadro del avatar es la foto de ChatGPT web
- `avatar_ranges.json` → la **primera ventana** (A0, 0-6,14 s) ahora tiene `"frame": "D:/rtmp/hospice/refs/rosa_av.png"` (1672x941, 16:9 exacto, copia intacta en `avatar/frames/a1_av.png`).
- El cuadro que había generado Nano Banana quedó archivado en `avatar/frames/a1_nb_generado.jpg`; `avatar/frames/a1.jpg` ahora es la foto del creador (JPG q2 desde el PNG, sin recorte).
- `plan.json` **no cambió** (md5 3a9504ea…): el campo `frame` sólo se usa como respaldo cuando el clip de avatar todavía no existe, y los 115 clips están completos. Por eso el video final no se re-renderizó: `final.mp4` sigue siendo el validado.
- **Lo que este cambio no puede arreglar en este video:** la llamada paga a InfiniteTalk ya se hizo y usó el cuadro anterior como referencia de cara, así que la cara que habla en pantalla viene de esa generación (misma persona, mismo cardigan, misma cocina). Volver a generarla requiere una segunda llamada paga, que la regla del video prohíbe. Para el próximo video la referencia real ya está puesta de entrada.
- Los otros 114 tramos siguen apuntando a `avatar/frames/a1_crop.jpg` (sólo respaldo; no se ven en el final). Si el creador quiere, se cambian todos a la foto real sin re-renderizar.

## Costos
- InfiniteTalk / RunPod: **US$ 0,25** (una llamada, sin reintentos pagos).
- Fotos (cola avatarity), Nano Banana, gpt-image de la cola, Groq, Fish, SFX: **US$ 0** (cuotas gratuitas del estudio).
- Render y armado: corridos en la nube del estudio (GitHub Actions), sin costo directo.
- DeepSeek (guion y prompts): costo de la sesión, no medido aparte por el panel.

## Problemas operativos
- El disco D: se llenó justo al recortar el final (0,7 GB libres): se borró una copia vieja de `qc/final_nube.mp4` (807 MB) y se reintentó el recorte.
- La bajada del `final.mp4` de la nube se cortó una vez y se relanzó sola: ~35 min en total.
- El render en la nube quedó ~40 min con la última máquina en cola; se verificó por `gh api` que los trabajos estaban completos y terminó sin acción.
