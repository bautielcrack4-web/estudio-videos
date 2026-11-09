# REPORTE — 10 Tops I Gave Away at 68 — What I Wear in Kyoto Instead

## Entregado
- `final.mp4`: 1920x1080, 30 fps, H.264 CRF 20, bt709 rango tv, keyframe cada 2 s, AAC 192 k estéreo 48 kHz.
- Duración: **20.8 min (1249,9 s)**, exactamente la de `voz/master.wav` (0,00 s de diferencia).
- `guion.txt`: 16.741 caracteres hablados (dentro del rango pedido de 13.500-17.250). Inglés, voz de Michiko.
- `meta.json` y este reporte.

## Estructura del guion
- Gancho 0-45 s: el cajón y las diez prendas nombradas una por una (número + objetos concretos).
- Credencial: la tienda del barrio, la memoria de 1987 con Mrs. Okada y la talla.
- Prueba interactiva (~min 4): cuello, hombro y dobladillo frente al espejo, en cuatro minutos.
- Los diez puntos: problema → anécdota con año/nombre/lugar → por qué pasa → cambio concreto con precio o medida → algo para hacer hoy.
- Like/suscripción antes del último punto; cierre con "Your clothes speak before you do", pregunta para comentar y gancho al próximo video (los pañuelos).
- Sin dietas, sin procedimientos, sin promesas de juventud, sin venta y sin mencionar IA.

## Avatar
- 101 ventanas, **511 s = 41 % del video**, en tramos de 3-6 s; la primera en 0 ms (4,58 s).
- Una sola llamada a InfiniteTalk (reel de 541,3 s), US$0,25. Desfase medido y corregido por `avatar_it.py` (máximo 395 ms).
- **Corrección de calidad:** el clip generado dejó un glitch de color en el jardín de fondo en varias ventanas. Recorté los 101 clips (624x351 desde x=208,y=56) y los escalé a 1920x1080 con lanczos; el glitch desapareció y el encuadre queda más cerrado. Los originales quedaron en `avatar/orig/`.
- Todos los tramos son clips reales: no hay carteles de espera ni fotos fijas en el avatar.

## Fotos (modo Ahorro, tope 20)
- **17 fotos** con gpt-image low + Batch: p001, p002, p013, p017, p022, p027, p040, p066, p097, p106, p119, p124, p126, p136, p143, p147, p152.
- 6 creativas con `detalle_narrativo`: p001 (las diez prendas en el tatami), p017 (la tienda de 1987), p027 (la prueba del espejo), p136 (los tres que se queda), p143 (el cuaderno de hombro/dobladillo/cuello) y p147 (la puerta de la tienda a la luz).
- 5 con el presentador (p001, p022, p027, p124, p147), cara consistente con el avatar.
- Gancho: se pidieron 3 variantes p001_a/b/c; elegí **p001_b** (Michiko levantando el cuello alto negro a mitad del gesto) y la copié como p001. Las otras dos se borraron.
- Una ronda de rehechas: p126 (el puño globo no se veía tragándose la mano) se repidió más cerrada.
- Sin fotos repetidas (el validador lo confirma).

## Clips de stock (Pexels, gratis)
- **139 clips** para el resto de los 156 planos. Cuatro rondas de reemplazo de los que no tenían nada que ver o rompían el tono (jeans en vez de tops, pies, acuario, cartel BLACK FRIDAY, ropa interior, primer plano de labios, lentejuelas de discoteca, suéter navideño, gato, etc.).
- Quedan algunos planos con modelos jóvenes en escenas de ropa y telas: son pertinentes al tema, no tienen marcas grandes y no hablan a cámara. La biblioteca tiene poco material de mujer mayor en interiores japoneses.

## Sonido
- 4 efectos puntuales en `cues.json`: cajón al abrir (16,2 s), tela (164,8 s), papel al escribir los tres puntos (275,1 s) y té servido en el cierre (1220,4 s). Ganancias 0,04-0,055. El resto va sólo con voz.

## Gasto
- Fotos gpt-image: US$0,052 (5 tandas; incluye las 3 variantes del gancho y la rehecha de p126).
- Avatar InfiniteTalk: US$0,25.
- Revisor: US$0,004.
- Whisper: US$0 (Groq).
- **Total aproximado: US$0,31.**

## Problemas y qué mejorar
- La voz clonada habló más lento de lo previsto: 16.741 caracteres dieron 20,8 min en vez de ~15. El guion está dentro del rango del validador y no se recortó para no perder contenido; si se quiere 15 min exactos, conviene apuntar a ~12.500 caracteres con esta voz.
- El primer render del avatar trajo un glitch de fondo; se resolvió con recorte. Para próximos videos conviene revisar una muestra de ventanas apenas llega el reel, antes de renderizar todo.
- El clip p121 salió negro y el revisor lo detectó; se repidió con satén claro. Es la única corrección del revisor.
- La calidad del stock es la limitación principal del modo Ahorro: exige varias rondas de búsqueda y aún así deja planos genéricos.

## Estado de controles
- `validar.py --etapa guion`: OK.
- `validar.py --etapa fotos`: OK.
- `validar.py --etapa render`: OK salvo la apertura, que fallaba sólo porque el avatar aún no había llegado; resuelto al re-renderizar.
- `validar.py --etapa final`: **OK**.
- Revisor final: primera corrida, 3 avisos de negro en 984-991 s (p121), corregidos; ver `gates/correcciones_hechas.txt`. Segunda corrida: 0 fallas en 42 cuadros.
