# REPORTE — One Collar Press Makes a Plain Shirt Look Tailored · Kyoto Grace

## Estado
En producción. Se actualiza al final con los números definitivos.

## Qué se hizo
- **Guion**: 19.176 caracteres (3.740 palabras), inglés, voz de Michiko. Pasa el validador de guion (18.000–23.000 para 20 min).
  Estructura: gancho con objeto concreto (el cuello de la camisa), credencial (32 años en la tienda de Teramachi, 1976–2008),
  memoria de 1968 con Mrs. Kondo, prueba interactiva (tres comprobaciones frente al espejo), y puntos con anécdota + fecha/lugar
  + por qué + cambio concreto + algo para hacer hoy. Pedido de like antes del último punto y pregunta final con gancho al
  próximo video (el suéter fino). Sin consejos médicos, sin marcas, sin menciones de IA.
- **Voz**: clon de Fish a partir de `refs/voz.wav`. La narración natural salió de 23,5 min; se ajustó un 10 % con `atempo`
  (sin cambiar el tono) para acercarla a los ~20 min pedidos. Duración final de la voz: 21,4 min (1.281,9 s).
- **Tiempos**: `captions.json` por palabra (3.736 palabras), sobre el audio ajustado.
- **Planos**: `planos.py` generó 139 planos de b-roll (~4–7 s) + 17 fotos de pantalla partida, cortados en pausas del habla.
- **Avatar**: `avatar_ranges.json` con 89 ventanas, 544,4 s (42,5 % del video; tope 560 s), reel 571,1 s (tope 590 s).
  Primera ventana desde 0; ventanas a pantalla completa ≤ 6 s y 17 ventanas en pantalla partida de ~9 s; ningún hueco > 14,4 s
  sin avatar. Una sola llamada a InfiniteTalk.
- **Fotos**: 3 variantes del gancho, elegida p001_c; 6 de prueba variadas; lote completo de 149 fotos en 2 batches
  (136 sin referencia + 13 con la cara del presentador). Total 156 fotos para 156 planos, cero repetidas. 6 imágenes creativas
  con `detalle_narrativo` (p005 antes/después, p007 foto antigua en la mano, p021 flat lay histórico, p106 etiquetas de papel,
  p123 grilla del plegado de viaje, p131 grilla de rutina con horas).
- **Sonido**: 5 efectos puntuales y bajos (`cues.json`): papel en el recuerdo de 1976, vapor en el siseo de la plancha,
  tela al enrollar el cuello sobre la toalla, pájaros y té al cierre.

## Gasto
- Fotos gpt-image low + Batch: pendiente de total (≈ US$0,003 por foto).
- Avatar InfiniteTalk: US$0,25 aprox. (1 llamada).
- Tiempos/ASR: ~US$0,006/min.
- Revisor final: < US$0,01.

## Problemas / avisos
- La voz natural superaba el largo objetivo (23,5 min); se compensó con un 10 % de velocidad.
- En la tanda de prueba, tres escenas de técnica mostraron una cara distinta a la presentadora (p002, p050, p105). Se rehacen
  en una única ronda con encuadre desde el mentón hacia abajo. El resto del lote ya lleva esa instrucción.
- La cara del reflejo en p079 no coincide del todo con la presentadora; la figura principal es la espalda, queda como aviso menor.

## Qué mejorar
- Para próximos videos, pedir desde el inicio "framed from the chin down" en todas las escenas de manos para no gastar rehechas.
- El ritmo de voz del clon es más lento que la referencia; conviene ajustar el guion al largo real antes de generar.
