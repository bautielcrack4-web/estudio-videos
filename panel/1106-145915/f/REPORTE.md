# Michiko's Kyoto Closet — "I'm 68 in Kyoto: The 8 Daiso Skincare Finds I Actually Use"

## Estado
- Voz: Fish `moda_michiko_ca` con `--keep-tags`, master `voz/master.wav` = 1012,1 s (16 min 52 s).
- Guion: 63 párrafos, sin "old", sin claims médicos, precios en US$, °F. Gancho 0-96 s (ver desvíos).
- Tiempos: Groq ASR palabra por palabra (`captions.json`, 2537 palabras) y `paras_timed.json` 63/63. Cada plano anclado al `startMs` de la palabra que lo motiva.
- Fotos: 172 archivos de b-roll, todas por Nano Banana en la cola de avatarity (0 por otra vía), prompts JSON con `moment/action/props/setting/light/camera/color/avoid`, linter OK en cada lote.
- Clips: 0 (ver abajo).
- Montaje: 163 segmentos, fundido foto-foto 0,3 s / avatar-foto 0,6 s, Ken Burns al azar con semilla fija, 3840x2160 antes de zoompan.
- SFX: 5 cues (agua, papel x2, monedas, tela), gain 0,045-0,05, mezclados bajos.
- Salida: `final.mp4` 1920x1080 30 fps H.264 CRF 20, AAC 192k estéreo, 1012,108 s
  (= voz, desvío 0,000 s), 399.595.888 bytes (381 MB), ~3,16 Mbps.
- Validador etapa final: OK. Única advertencia: 18 fotos >8 s (máx. 14,4 s, `s06`),
  todas sobre párrafos largos de narración y con Ken Burns; se dejaron así para no
  invalidar la numeración de 163 segmentos ya verificados.

## Avatar
- Plan de 6 tramos (A1, A1b, A2, A3, A4, A5) = 46 s en pantalla, todos ≤6 s en los primeros 30 s y con escena distinta.
- La cola de agnes no entregó **ningún** clip en ~2,5 h (cupo diario agotado en todas las claves Starter; el pool devolvía `EPERM` al escribir el estado compartido por la cantidad de videos en paralelo). El trabajo quedó lanzado hasta el final y el proceso en segundo plano (`avatar.mjs`, última tanda) fue detenido al alcanzar el límite de tiempo del entorno: 0 clips entregados.
- Reemplazo aplicado (regla del kit): cada tramo de avatar va con **su primer cuadro como foto fija**, fundido de 0,6 s, así el corte no se siente y el video no frena. Si los clips llegan, se corre `render.py` + `assemble.py` y se reemplazan solos.

## Fotos rehechas
- `h08` → `h08b`, `r15` → `r15b`, `r18` → `r18b`: la cola devolvió falsos positivos CONTENT_POLICY (CSAM_MINOR_SAFETY) con prompts de edad + cuerpo; se reescribieron como manos + objetos concretos.
- `k11` → `k11b`, `l02` → `l02b`, `l08` → `l08b`, `m02` → `m02b`, `h15` → `h15b`, `g10` → `g10b`, `y01` → `y01b`: mismos falsos positivos; versiones nuevas con manos o persona + ropa concreta.
- `k05b` (rojez en la mejilla) volvió a caer por el mismo filtro → se usó la foto original `k05` y `k05c` (solo manos con el paño) quedó sin usar.
- `a3` (primer cuadro del avatar) no llegó → se encoló `a3b`; el plan apunta a `frames/a3b.jpg`.

## Desvíos del plan
- El gancho dura ~96 s antes de la credencial (el guion pedía 45-50 s). El texto ya estaba aprobado y grabado, así que se respetó y se cubrió con 19 fotos de gancho para que los cortes queden en 4-6 s.
- `mk17ds` llegó al tope de 150 imágenes por slug; los lotes siguientes fueron con el slug `mk17ds_b` (misma cola).
- El tramo A1 se extendió de 4,18 s a 4,64 s para tapar un hueco de plan entre la foto `h01` y `h10`.

## Costos
- agnes: sólo cupo gratuito (0 s entregados de avatar).
- OpenAI / gpt-image: US$ 0. `D:/rtmp/SIN_OPENAI` intacto.
- DeepSeek: US$ 0 (guion y prompts se escribieron en esta sesión).

## Puntos de control
- `guion`, `fotos`, `render` y `final`: validador corrido, revisión visual propia con
  hojas de contacto (`qc/hoja_fotos.jpg`, `qc/hoja_render.jpg`, `qc/hoja_final_0/1/2.jpg`)
  y `gates/<etapa>_auto.txt` + `gates/<etapa>_pedido.txt` escritos.
- `gates/correcciones.txt` no existió en ningún punto de control (nada que aplicar).

## Problemas técnicos
- Render en paralelo con otros ~10 videos: dos segmentos (`0087`, `0111`) salieron con un bloque NAL corrupto (misma firma de bytes); se detectaron con un decode-check de los 163 segmentos y se re-renderizaron. El primer ensamblado se cayó por eso; el segundo pasó.
- `0084` salió sin duración (moov incompleto) y también se re-renderizó.
- Un PNG (`a3b.png`) no lo pudo decodificar ffmpeg por memoria; se convirtió a JPG q95 con PIL.
- Estado compartido de agnes con carreras `EPERM` entre procesos; la herramienta reintenta sola.
