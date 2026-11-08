# REPORTE — hr05ds · Hospice Chaplain Rosa
## "Medicare Pays for This When a Parent Is Dying — 9 Hospice Benefits Families Never Ask For"

**Estado:** TERMINADO (8-nov-2026). 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192k estéreo · **25:57,6** · 757 MB.

**Entrega (regla nueva del creador, 8-nov):** el final **no se baja a la PC**. Queda hecho en GitHub, ya en formato
de YouTube, y la carpeta entrega eso:
- `final.url` → https://github.com/bagasy-search/claudeyoutubevideos/releases/download/est-hr05ds/final_f0f74b59a410.mp4
- `final.nube.json` (plan `f0f74b59a410`, tag `est-hr05ds`, 1557,60 s, 793,05 MB)
- `qc/f_001..052.jpg` (cuadros cada 30 s) + `qc/final_info.json` (medidas, 0 huecos negros)
La copia local de `final.mp4` (757 MB) se usó para el QC y **se borró** al quedar validado desde GitHub (el disco
estaba al 100 %). No se re-renderizó nada: es el mismo final corregido.

## Qué se hizo
- **Guion:** `guion.txt`, 4.246 palabras en inglés (validador OK para 25 min). Orden: gancho → quién soy →
  los 9 beneficios (aide, equipo, capellán, trabajadora social, respiro, cuidado continuo, medicamentos,
  duelo, derecho a cambiar/revocar) → pedido de suscripción → recapitulación → cierre.
  Rosa es **capellana** de hospicio: cero indicaciones médicas, cero dosis/diagnósticos.
- **Voz:** Fish, voz `rosa_mx`, `--keep-tags`, 9 bloques → `voz/master.wav` de **1.557,59 s (25:57,6)**.
- **Transcripción:** Groq word-level → `captions.json` (4.213 palabras, precisión ~50 ms). Todos los cortes
  salen del `startMs` de la palabra que los motiva.
- **Fotos:** pedidas por la cola de avatarity (`encolar.mjs`) en 6 tandas: 160 prompts de b-roll
  (Nano Banana / desvío gpt-image-2 de la cola) + 6 imágenes creativas de GPT. Linter `lint_fotos.py`
  OK en todas las tandas (se corrigieron 4 escenas "vacías" y 12 cámaras sin close-up en la tanda 5).
  Total entregado: **166 fotos**. Usadas: 151 únicas.
- **Avatar:** InfiniteTalk, **1 sola llamada** (`avatar_it.py`, US$ 0,25), 95 ventanas / 448,9 s de reel,
  desfase medido y corregido (máx 300 ms). Primer cuadro = `D:/rtmp/hospice/refs/rosa_av.png` (foto de
  ChatGPT web, sin pasar por Nano Banana), igual para las 95 ventanas.
- **Efectos:** 8 SFX de Mixkit, 7 cues a gain 0,04–0,05.
- **Música:** **no se usó** música (la biblioteca disponible no daba el tono del canal; el video va sólo
  con voz + SFX puntuales).
- **Render y armado:** hechos **enteros en GitHub** con `render.py` (plan.json → 378 segmentos en 24
  tandas → 25 máquinas en paralelo → fundidos + voz + SFX → `final.mp4` en la release). La última pasada
  tardó 8,3 min. No se descargó a la PC: link en `final.url`.

## Números
- Duración final: **1.557,60 s (25:58)** · voz 1.557,59 s (desvío 0,005 s).
- 283 planos de b-roll · 95 ventanas de avatar = **27,0 %** del video (regla 20-35 %).
- Hueco máximo sin avatar: 12,7 s (regla: nunca más de 20 s).
- Primera ventana de avatar: 0–8,0 s (regla: arranca en 0 y ≤ 10 s).
- Cortes: cada 2,0–3,1 s en el gancho, cada 3–6 s en el resto; fundidos 0,6 s avatar↔foto, 0,3 s foto↔foto.
- US$: **avatar 0,25**. Fotos, clips, voz, ASR y SFX: 0 (colas e instancias gratuitas). DeepSeek: ~0.
- 0 huecos negros ≥ 0,5 s · 0 palabras médicas/IA en el guion.

## Problemas y qué se hizo
- **`gancho_b`** rechazado por la cola 2 veces con `CONTENT_POLICY_VIOLATION / CSAM_MINOR_SAFETY`
  (falso positivo, era una foto de una familia). No se reintentó (regla de 3 fallas). Se usan
  `gancho_a` + `gancho_c`; se eligió `gancho_a` (hija con la pila de papeles de Medicare) como primer
  plano después del avatar porque es la situación que duele y se entiende sin audio.
- **Primer render en GitHub:** la subida del paquete falló dentro de `nube.py` (tarfile, error de
  Python). Se volvió a correr `render.py` y subió completo (221 MB + 63 MB); el render terminó 25/25.
- **Disco de la PC al 100 %:** durante el QC el disco llegó a 0 libre y un comando falló al escribir.
  Se liberó borrando archivos intermedios propios; el render ya no se hace en la PC.
- **Dos descargas simultáneas de `final.mp4`** (`assemble.py` y `render.py`) chocaron por
  `final.mp4.bajando` (PermissionError). Se mató el proceso duplicado y se rehízo la descarga.
- **Id `e06_binder`** no existía (el archivo entregado era `e06_binder_beneficios`): se corrigió en
  `shots_timed.json` y en `build_plan.py`.
- **Duración vs voz:** el plan cerraba en 1.558,075 s (último `endMs` de `captions.json`) y el video
  quedaba 0,47 s más largo que la voz → ✗ del validador. Se ajustó `END` a 1.557.593 ms; sólo cambió
  el último plano y se re-renderizó.
- **Regla PANTAYA:** `b30_camion` (funeraria bajando una camilla cubierta) salía en 432,8 s y 524,0 s.
  Se reemplazó por `d04_silla_ruedas` y `d10_andador`. Verificado en el render final.

## Qué faltaba y quedó hecho
- Fotos de b-roll: cola drenada (`pend 0`), 166 archivos.
- Avatar: 95 clips reales, sincronizados.
- Render completo en GitHub; final validado con `ffprobe` y con `qc/final_info.json` (1557,60 s, 0 negros).
- `validar.py --etapa final --min 25` → **OK** (0 ✗). Cuadros cada 30 s en `qc/final_*.jpg`
  (hojas `qc/hoja_final_1..5.jpg`), revisados con Read.
- Gates `guion`, `fotos`, `render` y `final` escritos en `gates/`. No hubo `gates/correcciones.txt`.

## Lo que mejoraría
- Pedir las fotos con más anticipación para no depender de la cola compartida (la tanda final tardó
  horas con ~3.300 pedidos globales).
- Evitar motivos de funeraria con camilla en los prompts (PANTAYA los prohíbe y la IA los genera igual):
  pedir directamente "camioneta de agencia estacionada, sin camilla".
- Cerrar el último corte del plan con la duración real del WAV (`ffprobe` del master) y no con el último
  `endMs` del ASR, que agrega ~0,4 s.
- Sumar una tanda de fotos "antes/después" al estilo del menú de imágenes creativas (no entró por tiempo
  de cola en este video).
