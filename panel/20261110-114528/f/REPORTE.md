# Reporte — My Grandmother Walked Every Day Until 98 (Yoko's Morning Legs, video 1)

## En una línea, el mundo (mundo.json)
El living chico y luminoso de un departamento japonés (silla de madera, radio plateada, colchoneta violeta junto a la puerta del balcón), donde todo lleva información escrita a mano —la pizarra con los 5 movimientos y círculos rojos, el cronómetro tomate, el almanaque, el cuaderno, la foto enmarcada de la abuela— sobre madera clara, cortina blanca y el rojo del lápiz.

## Qué se hizo
- `guion.txt`: 9.968 caracteres (~1.865 palabras), inglés, voz de Yoko: gancho con la edad de la abuela (98), credencial (32 años de maestra), prueba interactiva ("stand up once, slowly, without using your hands" ~min 2), los 5 movimientos con conteo en voz alta, qué notar a las 2 semanas, pedido de like/suscripción antes del cierre, pregunta final y gancho al próximo video. Sin palabras prohibidas, sin consejos médicos ("ask your doctor" donde corresponde).
- Voz clonada (Fish): 12,4 min de master. Tiempos por palabra en `captions.json`.
- Avatar InfiniteTalk: **una sola llamada**, 21 clips (A24 y A26 no llegaron en el reel; esos planos van con foto). 114 s de avatar (~15 %). Por qué no el 50 %: ver "Problemas".
- 135 fotos distintas, cero repetidas (validador ✓). Escenas firma construidas (4) y 2 metidas en la línea sin pisar el avatar.
- Sonido: 11 cues suaves de su lugar (radio, madera de la silla, pájaros, pasos, papel, cronómetro, puerta corredera).

## Los 10 puntos de la edición
1. **Índice** — la hoja escrita a mano "5 Movements" en la pizarra, una fila por movimiento con su dibujo, pedida en planta y cortada por filas en la escena es01 (cada fila entra con su palabra).
2. **Progreso** — la última línea que se cierra con círculo rojo al empezar cada movimiento; la pizarra completa antes del cierre (p119–p121).
3. **Apertura de movimiento** — cada movimiento abre con su foto (Yoko en la silla), no con tarjeta: M1 la hoja a planta cortada en paneles; M2/3/4/5 abren con foto de Yoko y conteo en voz alta; es02 (pie del círculo) es un empuje continuo de cámara.
4. **Avatar + encuadres** — pantalla partida (avatar + foto de lo que nombra) en la frase del gancho; 21 ventanas cortas de 3,5–6 s, en las frases clave.
5. **Transición de capítulo** — el sonido de la madera de la silla + la foto de la silla girada entre movimientos (p017/p018/p062...), nunca tarjetas.
6. **Sonido del lugar** — 11 cues por debajo de la voz.
7. **Lugares** — el pueblo al norte de Sendai, el pescadero (noren 魚屋), el patio del colegio con polvo, el jardín de piedras: en foto real, el nombre japonés visible en el noren.
8. **Recuerdos de la abuela** — foto vieja saliendo del sobre (p004), foto enmarcada en sus manos (p007), manos de abuela y nieta contando (p041), los dos pies lado a lado (p085). Nunca a pantalla completa fija.
9. **Números** — 10 repeticiones en el almanaque, "twenty steps" en el cuaderno con huellitas, 20 años en el abanico de almanaques atados, 2 semanas en la grilla de la pizarra, "one centimetre" en la regla. Todo escrito a mano en objetos suyos.
10. **Cierre** — repaso de los 5 sobre la hoja completa (es04, paneles) + CTA con el avatar. Sin pantalla final con link.

## Escenas firma (escenas/ficha.json)
- Tesis: cinco movimientos simples en una silla, hechos lento y juntos, traen equilibrio y soltura; el recurso: la pizarra con los 5 números y los círculos rojos.
- es01 (p027) · paneles por filas sobre "Number two... Number three..." — **en la línea**.
- es02 (p076) · empuje continuo al dedo del pie que dibuja el círculo — cae sobre avatar, va como b-roll.
- es03 (p106) · ventana sobre "the oldest was Mrs. Sato" — cae sobre avatar/escena, va como b-roll.
- es04 (p118) · paneles sobre el repaso final — **en la línea**.

## Piezas de la extrema
- Corre el motor (`extrema/`, renderizado) con 2 piezas de escenas firma. Las piezas animadas "libres" no se programaron a mano: el kit pide no pisotear las escenas firma y el motor trae las suyas.

## QC final
- Revisor: 25 cuadros cada 30 s, **0 fallas** (gates/revisor_final.json). Sin ronda de correcciones.
- `validar.py --etapa final`: **OK**. Avisos: avatar al 15 % (el reel salió corto) y huecos de más de 15 s sin avatar.
- Duración: 12,4 min (746,97 s) · 1920x1080 · 30 fps · H.264 CRF 20 · AAC 192k.
- Una toma de movimiento 4/5 (p074/p075) es de la pantalla de movimiento sin la cara del canal (tope de caras agotado); no se puede repedir sin re-render completo, queda anotada.

## Gasto (estimado con los logs de las herramientas)
- Fotos gpt-image low/Batch: ~US$0,60 (209 imágenes bajadas, incluidas repedidas y hojas).
- Escenas firma: US$0,0077 (DeepSeek) + render local.
- Avatar: 1 llamada fija por video (precio según panel; 126 s de reel).
- Sonidos: gratis. Voz: incluida en el plan del canal.

## Problemas y qué mejorar
- **Avatar:** el reel salió corto (21 de 23 ventanas) y el avatar quedó en ~15 % del video (ideal ~50 %). Las 17 fotos con "cara: true" quedaron por debajo del ideal porque la compuerta cuenta 15 por video y ya había una en el gancho: las tomas de movimiento 3, 4 y 5 se hicieron con modelos de otra cara (algunas con la presentadora en otro encuadre). Para el próximo video: la herramienta de avatar 1 llamada y **declarar las ventanas ANTES de pedir las fotos con cara**, y prever el reel corto dejando las últimas 2 ventanas fuera.
- **Escenas:** la primera versión de p027/p118 salió con una lista ajena ("Jumping Jacks…") y se repidió; la segunda está bien. `escenas construir` tardó 19 min y el render esperó 10 min por las piezas (máx. del motor); las tomó por el archivo existente.
- **Fotos:** el Batch tardó mucho (hasta 32 min por lote) y algunos lotes se encolaron en espera del anterior; el proceso esperador quedó colgado dos veces y hubo que matarlo para que avanzaran los que estaban detrás.
- **Qué mejorar:** cada movimiento debería tener su foto de Yoko con la cara del canal (mismo tope de 15), repartidas mejor; el cierre con el avatar (A26) no llegó por 1 s de reel.
