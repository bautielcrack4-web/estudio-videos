# REPORTE — fn06ds · Ernie Navarro, Funeral Director

**Título:** I Buried 7,000 People in San Antonio — The 9 Things Families Regret Paying For
**Archivo:** `D:/rtmp/fn06ds/final.mp4` · 1920x1080 · 30 fps · H.264 CRF 18 · AAC estéreo 192k
**Duración:** 1759,908 s (29 min 20 s) — idéntica a `voz/master.wav` (0,0 s de diferencia)
**Peso:** 757 MB

---

## Qué se hizo

| Etapa | Resultado |
|---|---|
| Guion | `guion.txt`, inglés, 4.546 palabras, 2-4 tags de emoción de Fish. Gancho con número + objeto, credencial, test interactivo al minuto 4, 9 puntos con problema → anécdota con fecha/nombre/lugar → por qué pasa → cambio concreto con precio → chequeo para esa noche, like/subscribe antes del 9.º, cierre con pregunta al comentario y gancho al video siguiente. Sin "honest", sin "genuinely", sin relleno, sin sermón. |
| Voz | Fish, voz `ernie_en`, `--keep-tags`, 235 frases → `voz/master.wav` (29,3 min). |
| Transcripción | Groq `asr_groq.py`, tiempos por palabra (~50 ms) → `captions.json` y `timeline.txt`. |
| Fotos | **311 fotos** (63 .jpg + 248 .png), todas por la cola de avatarity con prompt JSON completo y linter pasado. 5 de ellas creativas de GPT con `detalle_narrativo`. 0 clips de Veo. |
| Avatar | InfiniteTalk, **1 sola llamada**, US$ 0,25, reel de 485 s desde `D:/rtmp/funerario/refs/ernesto_av.png`. **104 ventanas** de 3-6 s = 453,8 s (26 % del video). |
| Plan de planos | 570 planos, 0 huecos, suma exacta 1.759.500 ms, mínimo 520 ms, promedio 3,1 s. |
| Sonido | 5 SFX de Mixkit, 6 cues en `cues.json`, gain 0,035-0,08. **Sin música, a propósito.** |
| Armado | **Render en GitHub** (`render.py` → `nube.py` → `estudio.yml`): 33/33 máquinas OK, 4,3 min de render, `final.mp4` bajado ya terminado. Nada renderizado en la PC. |

## Cuadro de apertura (regla del creador)

El primer cuadro es **el avatar real hablando**, desde el ms 0 (`plan.json` arranca `kind:"av"` en t0=0, validado). La primera ventana dura 6,98 s y corta en una pausa. Justo después entra **gancho_c**: una mano abanicando un mazo de formularios rosas y verdes delante de un archivador. Se eligió porque es la única de las tres variantes con una acción a mitad de gesto, se lee en chico y no repite la cara del avatar (el razonamiento completo está en `gates/fotos_auto.txt`). Los otros dos ganchos entran a los 15,0 s y a los 27,6 s.

## Costos

| Ítem | Costo |
|---|---|
| InfiniteTalk (avatar, 1 llamada, reel 485 s) | **US$ 0,25** |
| Fish (voz) | US$ 0 (gratis) |
| Groq (transcripción) | US$ 0 (claves free) |
| Fotos (cola avatarity, Nano Banana + desvío gpt-image-2) | US$ 0 |
| SFX (Mixkit) | US$ 0 |
| Render (GitHub Actions) | US$ 0 |
| **Total** | **US$ 0,25** |

## Problemas y cómo se resolvieron

1. **La herramienta del avatar se cortó al final.** RunPod ya había entregado el reel (pago, US$ 0,25) y `avatar_it.py` se cayó cortando las ventanas en `A090` (`x264 malloc failed`, memoria de la PC). Como los clips se promueven recién al final, quedaban 91 `.tmp.mp4` y **cero** clips buenos. Se escribió `cut_av.py`, que mide el desfase del reel con la misma correlación de envolvente, corta **solo las 14 ventanas que faltaban** en la PC y promueve las 104. No hizo falta una segunda llamada a RunPod ni se cobró de nuevo.
2. **Huecos en el plan.** Los cortes de `timeline.txt` dejaban 67 huecos de 200-1.300 ms (40,8 s) que en la nube habrían quedado en negro. Se cerraron estirando cada plano hasta el arranque del siguiente.
3. **El video quedaba 5,1 s más corto que la voz.** `render.py` parte las fotos alrededor de las ventanas de avatar y **descarta los pedazos de menos de 500 ms**. Se hizo que `mk_shots.py` "enganche" cada borde de ventana de avatar a un borde de plano: ahora el render simulado pierde 156 ms en total.
4. **Disco lleno.** `nube.subir_paquete()` falló con `No space left on device` al tarrear 381 fotos nuevas (D: 2,94 GB libres). Se borró el tar parcial y se relanzó cuando el disco se liberó.
5. **`spawnSync git ENOENT`.** El PATH no tenía Git; se agregó `/c/Program Files/Git/cmd` a todas las llamadas.
6. **`WinError 1455`** (page file) en tandas de fotos: se resolvió con reintentos a 90 s.
7. **`pkill` no existe** en este shell: los procesos se matan con `taskkill //F //PID`.

## Avisos del validador (no frenan)

- **Guion largo:** 4.546 palabras contra el rango esperado de 2.762-4.312 para 25 min. La voz ya estaba grabada cuando se detectó (29,3 min), así que no se recortó: el video dura 29 min 20 s en vez de 25. Queda anotado como lo primero a corregir en el próximo video (achicar el guion antes de grabar, no después).
- Algunos cuadros de las hojas de contacto caen justo sobre un fundido y se ven dobles. Verificado con `qc/hoja_check_fades.jpg`: 0,4 s después cada plano es limpio. Es el fundido fotografiado en el medio, no un defecto.

## Nota sobre la entrega (cambio del creador del 8-nov)

Este video se renderizó **antes** del cambio que deja el final sólo en GitHub. Ya tenía
`final.mp4` bueno y validado, así que según la regla del creador ("si tu video ya tiene un
final.mp4 bueno, no rehagas nada: sigue valiendo") no se volvió a renderizar. El archivo de
entrega de este video es `D:/rtmp/fn06ds/final.mp4` (757 MB, 1759,908 s, validado con
`--etapa final` en OK). Los videos nuevos ya no lo bajan a la PC: usan `final.url`,
`final.nube.json` y los cuadros `qc/f_*.jpg`.

## Qué falta / qué mejoraría

- Nada bloqueante: el video está cerrado, validado en `--etapa final` con **RESULTADO OK**.
- Mejoraría el ritmo del minuto 25 en adelante: con el guion más corto sobra tiempo para dejar respirar las anécdotas de los últimos dos puntos.
- Hay 311 fotos para 570 planos, así que muchas se repiten (2-4 apariciones). Funcionan porque cambia el movimiento y el punto de foco, pero con 100 fotos más se vería todavía más variado.
