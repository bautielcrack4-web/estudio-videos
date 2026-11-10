# REPORTE — I've Fitted Shoes for 42 Years — These Are the Only 4 I'd Buy After 65

## Resultado
- **final.mp4**: 654,0 s (10,9 min), 1920x1080, 30 fps, H.264 CRF 20 bt709 + AAC 192k 48 kHz estéreo. 344 MB.
- **meta.json**: título exacto + descripción en la voz de Sal, 3 párrafos, sin links ni hashtags.
- **validar.py --etapa final: OK** (0 ✗). **revisor.py: 22 cuadros, 0 fallas.**

## mundo.json en una línea
El fondo de la zapatería familiar en South Philadelphia — el banco de madera gastada, el Brannock en el piso, las estanterías de cajas con etiqueta a mano, la campanilla de bronce, el almanaque de la farmacia y la libreta de tarjetas de clientes —, y lo que sostiene el video es **la fila de cuatro cajas con una tarjeta escrita a mano cada una** (el índice: 1 insole removible, 2 puntera ancha, 3 talón bajo y estable, 4 contrafuerte firme).

## Escenas firma
- **es01 · planos p019+p020** (la tarjeta de Mr. Rossi: "9D" arriba y "9E — wide, high instep" abajo, once años entre las dos líneas): **salió**. Cámara que viaja del file box abierto a la tarjeta y empuja a las dos líneas. Foto pedida antes del resto (ficha → fotos → construir) y armada por el motor.
- Solo el motor eligió 1 escena (no 3) para este guion; no agregué más a mano. Quedó fuerte y en el momento del dato clave.

## Fotos
- **115 fotos distintas** + 1 escena firma, un plano = una foto: **cero repetidas** (validador OK).
- **13 fotos con Sal (cara: true)** + el gancho: p001 (elegida entre 3 variantes), p005, p011, p015, p018, p022, p031, p072, p082, p099, p109, p115, p116. La descripción física del presentador coincide con el avatar (el validador no marca cara cambiada).
- **Fotos de DATO pedidas como imagen creativa, con el número/palabra escritos a mano en el objeto del mundo:**
  - p001 / p003: el índice de 4 cajas con sus tarjetas ("1. Removable insole", "2. Wide toe box", "3. Low stable heel", "4. Firm heel counter").
  - p019 / p020: la tarjeta de Mr. Rossi con "9D", "9E — wide, high instep" y el "2011" en lápiz.
  - p059: la caja con el talle impreso girada — "la caja sugiere, no manda".
  - p066 / p113: el papel y la regla con "10" y la tarjeta "10 1/2 D" — medir en pulgadas.
  - p069 / p113: el reloj de pared a las 4 en punto — "your feet are bigger at four o'clock".
  - los tres traps: la tarjeta de p025 ("no support"), p040 ("no support" en otra), p044 ("firm") y p112 ("Check heel counter — no collapse").
- **Repedidas** (una sola ronda, 3 fotos): p020 (rehiche con texto más nítido), p055 (rehiche: display de alturas de talón), p061 (salió con la cara equivocada → rehecha sin cara, manos de Sal poniendo el zapato con el shoehorn). Borradas además p089/p097/p108 por textos imprecisos en la ropa/cruz del cristal, y reescritas con más momento.

## Gasto aproximado
- gpt-image low + Batch: **~US$0,266** (21 fotos de prueba 0,048 + 85 fotos 0,178 + 11 con cara 0,030 + escena 0,003 + 1 ficha/2 rehechas 0,007).
- Escenas (ficha + construir): ~US$0,005. Revisor: ~US$0,001. Voz, tiempos, avatar, sonidos, render: herramientas del Estudio fijas (1 sola llamada InfiniteTalk, 20 ventanas, reel 109 s).

## Problemas y qué mejorar
- **Avatar 16 % del video** (103 s, 20 ventanas de 5 s): el validador lo marca como aviso (ideal ~50 %). El plan de tramos se eligió para abrir con Sal, cortar en cada frase importante y el resto en b-roll. Subir el avatar ahora implicaría otra llamada de InfiniteTalk; se dejó el plan cerrado que validó. **Próxima vez:** más ventanas de 3-6 s con pantalla partida en los tramos de 7-12 s (el KIT §3) en lugar de concentrar en 20 ventanas de 5 s.
- **3 imágenes creativas con `detalle_narrativo`** (lo pedido era 4-6, aviso, no frena). Las fichas del índice y los datos van como fotos de objeto real; la próxima vez conviene forzar 2-3 collages de celular o la grilla de rutina para llegar a 6.
- Marcas reales de zapato que el generador puso por su cuenta en cajas y carteles de la tienda (no las pedimos, el guion nunca las nombra ni las vende; se ven chicas en el fondo). Sin marcas en voz, sin venta, sin claim médico ("ask your doctor" incluido en el trap del talón).
- **Primer tramo de avatar de 7 s** (0-7 s) en pantalla completa: aviso de ≤ 6 s. Queda como está (es la apertura y el validador lo acepta).
- La p061 final: manos de Sal con el shoehorn sobre el talón de un cliente, encuadre bajo y cálido, sin cara del presentador equivocada.
