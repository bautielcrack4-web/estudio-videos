# REPORTE · fe06ds · "Por qué le dije a mi propia madre que nunca comprara un funeral a futuro"

Canal: **Don Ernesto, el Funerario** (ES) · voz `ernesto_es` · slug `fe06ds`
Duración final: **21 min 59,66 s** (1319,66 s) · 1920x1080 · 30 fps · H.264 · AAC 192 kbps estéreo
Archivo: `final.mp4` (553,6 MB) · guion 3364 palabras

## Qué se hizo

| Etapa | Detalle |
|---|---|
| Guion | `guion.txt`, 3364 palabras, español de Guadalajara. Siete preguntas para llevar impresas, letra del hambre, fideicomiso vs caja de la funeraria, Profeco y FTC Funeral Rule. Sin música, sin claims médicos. |
| Voz | Fish, voz `ernesto_es` → `voz/master.wav` (1319,66 s). Gratis. |
| Transcripción | Groq ASR palabra por palabra → `captions.json` (3150 palabras, precisión ~50 ms). Gratis. |
| Plan de planos | `shots_timed.json`: **204 planos** de 193 fotos distintas (1,06 de reutilización), media 4,86 s, máx 7,32 s. Cortes pegados a las palabras del ASR (`mk_shots2.py`). |
| Fotos b-roll | **198 fotos** por la cola de avatarity (Nano Banana / gpt-image-2 según desvío). Prompts JSON completos, linter pasado. Revisión visual en 13 hojas de contacto. |
| Imágenes creativas | Las escenas con el presentador y los detalles narrativos (grilla de rutina con horas 6:05/6:12/6:20, carta manuscrita, contrato con signos de pregunta a mano, fotos del antes/después) con `detalle_narrativo` y cláusula de realismo de celular. |
| Avatar | InfiniteTalk, **UNA sola llamada** → 71 ventanas `avatar/A0..A70.mp4`, 329 s = **25 % del video**, ventanas de 3-6 s cada 11-13 s, nunca más de 20 s sin avatar. A0 abre el video en t=0 con el frame del creador `ernesto_av.png`. |
| SFX | 5 cues muy bajos (gain 0,04-0,05): papel ×2, teléfono, cajón, puerta. Sin música (brief). |
| Render + armado | `render.py` → GitHub Actions (18 tandas / 19 máquinas), fundidos 0,6 s avatar y 0,3 s foto, audio mezclado en la nube. 4,1 min de render + unión. |

## Costos

| Ítem | US$ |
|---|---|
| InfiniteTalk (avatar, 1 llamada) | 0,25 |
| Fish, Groq, avatarity, GitHub Actions | 0,00 |
| **Total** | **0,25** |

## Problemas y cómo se resolvieron

1. **`avatar_it.py` murió por OOM al cortar el reel** → `cut_avatar.py`, cortador equivalente con `-threads 1 -preset veryfast -crf 18`, audio aparte y mux `-c copy`; mide el desfase del reel de RunPod y lo corrige (máx 200 ms, perdidas: ninguna).
2. **Cola de imágenes rechazaba el lote**: el despachador exige `prompt` string y le pasábamos el objeto JSON. Se manda el JSON serializado y el linter lo acepta.
3. **Disco D: al 100 % (0 bytes)** a mitad de las hojas de contacto → se liberaron copias propias redundantes (`avatar/it/_push_*`, `reel.mp4`, `voz.wav`) y quedaron ~9 GB.
4. **Primer render en la PC: `OSError [WinError 1455] El archivo de paginación es demasiado pequeño`** (10 chats en paralelo + disco saturado; ni `gh` podía arrancar). Se relanzó `render.py` cuando bajó la presión: mismo plan, subida a GitHub y render en 4,1 min sin tocar nada local.
5. **5 fotos repedidas** tras el QC visual, por `fotos_prohibidas.txt`:
   - `b191` fecha quemada 2006-11-14 · `b017` cama oscura con manos mayores (regla de pantalla)
   - `b043` slide en inglés "7 Time Management Tips" · `b078` overlay de cámara "REC 14:02:09"
   - `b149` infografía en inglés "PHOTOSYNTHESIS"
   El plan se recalculó (204 planos) sin esas fotos.
6. **El validador marcó `!`** en la carta manuscrita en inglés (~18:00, 4-5 s) y en el plano de la refinería de noche (~10:30, b-roll del relato del trabajador). Ninguno rompe reglas; quedan anotados.

## Cumplimiento de reglas

- ⛔ Pantalla: ningún cuerpo, ninguna cara de moribundo, sin sangre, tubos ni agujas. Cementerio sólo con tumba vacía y gente de pie; ataúdes siempre cerrados.
- Sin música. Precios citados con fuente (Profeco / FTC Funeral Rule). Sin claims médicos, el presentador no es médico.
- Nada de OpenAI directo, RunPod/ElevenLabs/Modal/git/YouTube/Bagasy/Telegram. El render en GitHub es el camino interno de la herramienta compartida `render.py`.
- No se tocaron carpetas de otros videos; no se imprimieron ni copiaron claves.
- Etiquetas de IA: ninguna. `SIN_OPENAI` intacta.

## Estado

Listo para entrega desde el panel. `final.mp4` validado con `validar.py --etapa final --min 25`: **RESULTADO OK, 0 ✗**.
Pendiente sólo de la revisión del creador (`gates/final_pedido.txt`).
