# REPORTE — A 2-Minute Evening Hand Ritual for Warm, Soft Hands · Kyoto Grace

## Estado final
**Video terminado.** `final.mp4` de 604,00 s (10:04), 1920x1080, 30 fps, H.264 CRF 20, AAC 192k estéreo 48 kHz.
`validar.py --etapa final` = OK. Revisor final: 21 cuadros, sin fallas.

## Qué se hizo
- **Guion** (inglés, 1.641 palabras): gancho con el número "dos minutos" y el objeto concreto (palangana, paño de algodón);
  credencial de Michiko (68 años, Kyoto, tienda de ropa); prueba interactiva en el minuto ~2 (manos bajo la lámpara, presionar la piel,
  frotar las palmas); cuatro puntos con problema → anécdota con fecha y lugar (1979, 1968, 1985) → por qué pasa → cambio concreto
  (agua tibia, 30 s de secado, dos minutos de masaje, el paño junto a la palangana, uñas en una sola dirección); pedido de
  like/suscripción antes del último punto; pregunta para comentarios y gancho al próximo video (el cuello del abrigo).
  Sin consejos médicos, sin productos, sin menciones de IA.
- **Voz**: clon de la voz del canal, 4 bloques, `voz/master.wav` de 603,8 s.
- **Tiempos**: `captions.json`, 1.634 palabras.
- **Avatar**: 63 ventanas, 333,7 s (55 % del video), tramos de 3-5 s; 5 ventanas de pantalla partida (s01-s05, 11 s)
  alternando lado; primera ventana en 0 ms; reel de 352,6 s (bajo el tope de 590 s). 63 clips reales, desfase corregido
  a un máximo de 200 ms; sin carteles de espera en el corte final.
- **Planos**: 60 planos de b-roll + 5 fotos de pantalla partida (65 fotos distintas, cero repetidas).
- **Fotos**: 68 archivos generados (incluidas 3 variantes del gancho; se eligió p001_a por ser la más clara en chico y sin audio:
  manos en el agua tibia, vapor, ojos cerrados con alivio, reloj a las 7:10). 6 imágenes creativas con detalle narrativo:
  p019 (hilo en la seda + ticket de 1979 + botón suelto), p023 (muñeca junto a la taza + tarjeta "wrists, not tea"),
  p034 (tira de 5 fotos numeradas del secado), p045 (grilla semanal "My Evening Routine" con horas 7:01-7:05),
  p048 (cuaderno con los 5 pasos dibujados, fecha 7 Nov, mancha de té), p058 (nota manuscrita "Tell me about her hands.").
  Todas revisadas en hojas de contacto.
- **Sonidos**: 5 cues bajos — agua al entrar las manos (4,7 s), canilla en el lavado (147 s), paño al secar (301,5 s),
  reloj en "la velocidad del segundero" (399,4 s), papel en el cuaderno (482 s). No se encontraron tomas buenas de pava
  ni de taza: se siguió sin ellas.
- **Render**: 123 clips, 18.120 frames, 604,0 s; escala 4K antes del zoom; fundidos avatar 0,6 s / foto 0,3 s.
- **QC**: guion, fotos, render y final validados; revisor final sin correcciones.

## Gasto
- Fotos: US$0,142 (9 de prueba + 58 del lote + 1 rehecha).
- Avatar: ~US$0,25 (llamada única).
- Revisor: US$0,001.
- Total aproximado: **US$0,39**.

## Problemas y decisiones
- p011 (baño) salió con una persona joven en shorts vista de espaldas: se rehízo en una sola ronda y quedó correcta.
- La cola del servicio de avatar tardó cerca de 80 minutos; el render completo se hizo en paralelo con cuadros de espera
  y después se rehicieron sólo los 63 tramos del avatar (70 s), así que no frenó la entrega.
- Aviso del validador sobre tramos de avatar de 11 s: son las 5 pantallas partidas permitidas por el KIT §3; el control
  final ya da ✓ en "dinámico".

## Qué mejorar
- Las fotos con el presentador tienen pequeñas variaciones de edad entre tomas (p001/p006/p035/p050/p056); se nota poco
  en b-roll corto, pero se podría reforzar la consistencia con menos fotos con cara.
- p033 tiene texto japonés generado en las etiquetas: legible y coherente, pero no es texto real de una tienda.
- Para otro episodio, buscar pava y taza con otras etiquetas del banco de sonidos.
