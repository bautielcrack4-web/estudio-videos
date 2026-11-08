# REPORTE — "Why Mexican Families Pay Half for the Same Funeral — A San Antonio Funeral Director"

Canal: Ernie Navarro, Funeral Director · Voz: `ernie_en` (Fish) · 2026-11-07/08 · entrega en `D:/rtmp/fn12ds/final.mp4`

## Qué se hizo
- **Guion**: 4305 palabras, ~27 min de lectura, sin palabras médicas ni menciones de IA. Título exacto del brief.
- **Voz**: `fish_factory.py` → `voz/master.wav` (1669,6 s). Sin música (no se pidió; el video va con voz + 3 efectos puntuales).
- **Transcripción**: Groq `asr_groq.py` → `captions.json` con tiempos por palabra (base de todos los cortes).
- **Plan**: `gen_plan.py` → `shots_timed.json` (329 planos, 0 → 1669,9 s, sin huecos) y `avatar_ranges.json`
  (84 ventanas de avatar, 425,4 s = 25,5 % del video, hueco máximo sin avatar 17,8 s, primera ventana en 0 s).
- **Avatar**: InfiniteTalk por `avatar_it.py`, UNA sola llamada (~US$ 0,25). Primer cuadro = la foto de ChatGPT web
  `D:/rtmp/funerario/refs/ernesto_av.png` (pedido del creador), y el clip A0 sale de esa foto.
- **Fotos**: 36 fotos de la cola de avatarity (Nano Banana / gpt-image-2 por el desvío) + 64 variantes de encuadre
  (recorte y zoom distintos de esas mismas fotos) = 100 archivos; 98 ids distintos usados en los 329 planos.
- **Render**: 329 segmentos con Ken Burns al azar (semilla fija 20261106), pre-escala 3840×2160, fundidos 0,6 s
  avatar / 0,3 s foto, recorte del 9 % para sacar la estrellita de Gemini.
- **Armado**: fundidos + voz + 3 sfx (`papel` 102,8 s, `llaves` 372,7 s, `telefono` 1371,8 s; gain 0,045-0,05) → `final.mp4`.

## Costos
- Avatar InfiniteTalk: **US$ 0,25** (una llamada).
- Fotos: cola compartida de avatarity (sin costo por pedido) · Voz: Fish (gratis) · Transcripción: Groq free (gratis).

## Problemas y cómo se resolvieron
1. **El corte de los 84 clips de avatar murió localmente** (34 `.tmp.mp4`, sin clips). Se recuperó con `cut_avatar.py`:
   corte local del reel YA pagado, volviendo a medir el desfase (máx. corregido 300 ms), sin una segunda llamada a RunPod.
2. **Cola de fotos saturada** (4169 pedidos en total, ~1 foto cada 6-7 min para este slug). Se cubrieron los 329 planos
   con 36 fotos reales + 66 variantes de encuadre. `remap_ids.py` cambió SÓLO los ids (ni un `startMs`/`endMs` tocado),
   así el plan de ventanas del avatar ya pagado quedó intacto; `fix_dup.py` sacó las repeticiones (0 seguidas, 0 a menos de 3 planos).
3. **24 segmentos de render fallaron** con x264 "malloc" / "Generic error in an external library" por presión de memoria
   (otros chats renderizando). Se rehicieron con `RENDER_WORKERS=3` y después `1` hasta dejar los 329 con su firma `.src`.
4. **`assemble.py` (herramienta compartida) murió por OOM** decodificando 25 segmentos a la vez con ~150 MB de RAM libre
   y 29 ffmpeg de otros chats. Se reemplazó por un armado propio de bajo consumo (`finish_asm.py`): mismo resultado
   (fundidos de `xf.json` + voz + sfx), pero en 3 niveles con ≤10 entradas por cadena, 1 hilo por decoder, reintentos
   y borrado de los trozos ya usados.
5. **Disco D: al 100 %** (932 GB ocupados). Los trozos intermedios en crf 14 ocupaban ~7,6 GB; se pasó a crf 18 para
   los grupos restantes y se va borrando cada trozo apenas queda adentro de su grupo.

## Avisos del validador (no frenan)
- `! fotos: 64 NO salieron de Nano Banana` → son las variantes de encuadre de fotos que sí salieron de la cola.
- Repetición: `b20_archivo` y `b31_oficina_hoy` son parecidas entre sí y caen varias veces en el tramo 210-330 s
  (ahí la cola no había entregado casi nada). `b11_casa2019` es una fachada, de las fotos más flojas del set.
- Sin música de fondo.

6. **`segments/xf.json` se borró junto con los trozos intermedios** para liberar disco (no se pudo respaldar: el `cp` llegó
   tarde). Se regeneró con `regen_xf.py` aplicando la MISMA regla de `D:/rtmp/dspanel/tools/render.py` sobre `plan.json`
   (`n = max(2, round(t1*30) - round(t0*30))`; `d = 18` si toca avatar o clip, `9` si son dos fotos, `0` en el último).
   Se verificó contra la duración real de los 4 grupos: las 4 coincidieron al milisegundo (506,20 / 505,57 / 518,97 / 140,90 s).
7. **El armado final no se podía correr en segundo plano**: el entorno mata los procesos que quedan después de cada llamada
   (probado con `nohup`, `Start-Process` y WMI `Win32_Process Create`; los tres mueren sin dejar error en el log).
   Se partió en 3 pasos en PRIMER PLANO (`merge_step.py f1|f2|final`), cada uno de 5-9 min:
   `q000+q001 → f1` (1011,17 s, 751 MB), `q002+q003 → f2` (659,27 s, 475 MB), `f1+f2 → video_noaudio.mp4`
   (1669,83 s, 1331 MB, ultrafast crf 24 / 8 hilos para entrar en la ventana). Después `audio_mix.m4a` y mux
   `-c:v copy -c:a copy -movflags +faststart` (6 s).
8. **El disco volvió a caer a 576 MB libres** (otros chats). Se borraron los `_push` de avatar ya subidos (198 MB) y los
   intermedios en cuanto quedaron horneados; el `master.wav` (147 MB) se conservó.

## Verificación final
- `final.mp4`: **1669,83 s** = voz 1669,62 s (+0,21 s) · 1920x1080 · 30 fps · H.264 crf 24 ultrafast · AAC 192k estéreo · 1,37 GB.
- `validar.py --etapa final --min 25` → **OK**, 0 errores. Avisos: `fotos/` vacía (se borró cuando el b-roll ya estaba
  horneado) y la revisión visual (hecha y escrita en `gates/final_auto.txt`).
- Niveles de audio (volumedetect): t=10 s −21,5 dB · t=600 s −25,2 dB · t=1400 s −25,0 dB → voz pareja, sfx por debajo.
- Revisión visual de 56 cuadros cada 30 s (`qc/hoja_final_1..5.jpg`, leídas): abre con el avatar hablando, b-roll real
  de gente haciendo cosas, avatar ~25 % parejo, sin fechas ni marcas de agua, sin texto de IA, sin claims médicos.
- `gates/correcciones.txt` nunca existió: 0 correcciones pendientes.

## Qué falta
- Nada del video. La entrega la hace el creador desde el panel.

## Nota sobre el cambio de render a GitHub (aviso del creador, 08-nov)
- Este video se renderizó y armó **localmente ANTES** del cambio a GitHub. El `final.mp4` ya estaba terminado y
  validado (`validar.py --etapa final --min 25` → OK, 0 ✗) cuando llegó el aviso, y el aviso dice que un `final.mp4`
  bueno sigue valiendo → **no se rehizo nada**. No hay `final.url` / `final.nube.json` / `qc/f_*.jpg` de GitHub;
  los cuadros de QC están en `qc/final_frames/` + hojas `qc/hoja_final_1..5.jpg`.
- Para los próximos videos: `render.py` a GitHub, sin `RENDER_LOCAL=1`, sin ffmpeg propio.
