# REPORTE — mk14ds · Michiko's Kyoto Closet

**Título:** I'm 68 in Kyoto: The 7 Handbag Mistakes I Stopped Making After 60
**Duración:** 14:07 (voz: 847,2 s)
**Voz:** Fish, `moda_michiko_ca` · **Avatar:** agnes-video-2.5-flash (reference + lipsync)
**B-roll:** Nano Banana por la cola de avatarity (slug mk14ds + mk14ds_b) · **SFX:** Mixkit

## Estado
- [x] Guion (2184 palabras) y voz master (`voz/master.wav`)
- [x] Transcripción Groq por palabra (`captions.json`) y `timeline.txt`
- [x] Plan de planos (`shots_timed.json`, 178 planos, mediana 4,9 s)
- [x] Fotos de b-roll: 178 de 178 entregadas (todas por la cola de avatarity)
- [x] Avatar: 7 de 7 clips (A1, A2, A3, B1, B2, B3, B4; 49,7 s en pantalla)
- [x] Render de los 179 segmentos (0 huecos en plan.json, validar render OK)
- [x] Mezcla final (`final.mp4`, 847,4 s, 376 MB, AAC estéreo)
- [x] QC final: 1920x1080 · 30 fps · cuadros cada 30 s revisados · lipsync OK
- [x] `validar.py --etapa final`: RESULTADO OK · gates/final_auto.txt + final_pedido.txt

## Decisiones
- La foto del segundo 0 es `gancho_a` (mujer levantando un bolso de cuero enorme en la
  cocina): la más fuerte de las tres variantes; `gancho_b` y `gancho_c` van a 2,8 y 8,1 s.
- Intro partida en trozos ≤ 6 s (A1 15,7-21,8 s) alternando foto/avatar cada 2-3 s.
  Después del avatar entra `hk_espejo_pobre` (21,8 s) para no repetir la foto de la cama.
- 7 regresos de avatar (49,7 s en total, dentro de 35-55 s).
- Prueba de pararse: arranca en 169,8 s («So, before I go on, stand up, I will wait»),
  sobre el avatar B1. El audio ya estaba grabado así, no se cambió.
- `t_item5_window` no se usa: la prueba de la ventana la hace el avatar B2 (559,3 s).
- `t_item1_kinoshita` falló en la cola con CONTENT_POLICY_VIOLATION (no se reintenta).
- CTA: el guion dice «press like» (línea 93), sin línea explícita de «subscribe».
  No se regeneró la voz por eso; queda anotado.
- Yui (la nieta que filma) aparece en 710,8 s, justo cuando el guion la nombra.

## Problemas
- La cola de avatarity es lenta (~1 foto cada 40-60 s para todos los videos): el render
  se corrió por tandas a medida que llegaban las fotos (`render.py` rehace sólo lo que falta).
- `avatar.mjs` se murió dos veces al lanzarlo con `nohup` desde la herramienta de shell;
  ahora corre con el modo de segundo plano del harness.
- Con la máquina cargada (10 videos en paralelo) algún render tiró
  «WinError 1455 (archivo de paginación demasiado pequeño)»; se relanzó y terminó bien.
- La primera pasada de assemble.py se cortó a los 10 min de segundo plano; se relanzó con
  timeout largo y log a `assemble.log` (179 segmentos, 8 tramos de 25).

## Costos
- OpenAI: US$ 0 (prohibido). agnes/avatarity/Fish/Groq/Mixkit: gratis.
- Total: **US$ 0**.
