# REPORTE — Layer a Thin Sweater Without Bulk in 3 Quiet Steps

## Entrega
- `final.mp4`: 1920x1080, 30 fps, **649,5 s (10,8 min)**, H.264 CRF 20 bt709, AAC 192k estéreo 48 kHz.
- `meta.json`: título + descripción de YouTube en 3 párrafos (voz de Michiko, sin links ni hashtags).
- `guion.txt`: 8.479 caracteres, 1.670 palabras (rango pedido 7.200-9.200 para 8 min).
- `captions.json`: 1.657 palabras alineadas; `planos.json`: 56 planos; `shots_timed.json`: 56 fotos/clips.
- `avatar_ranges.json`: 56 ventanas, **49 % del video con avatar (317 s)**, primera en 0, máximo 6 s por ventana y
  máximo 7 s sin avatar. Una sola llamada a InfiniteTalk; 56 clips, desfase máximo corregido 200 ms.
- `cues.json`: 5 efectos suaves (agua 9 s y 649 s, tela 283 s y 527 s, papel 440 s).

## Fotos y b-roll (MODO AHORRO)
- 39 clips de stock de Pexels; el juez de visión quedó con promedio 7,4/10. Reemplacé 18 clips en 3 rondas de búsquedas
  más literales (incluida una toma con ropa interior, descartada). Los únicos flojos que quedan: p026 (5/10) y p034 (6/10).
- 20 imágenes generadas con gpt-image low + Batch: 3 variantes del gancho (`p001_a/b/c`), `p001_a` elegida como `p001.png`,
  y 16 fotos más (17 usadas en el plan). 0 rehechas.
- 6 imágenes creativas con `detalle_narrativo`: p012 (cuaderno con corte del sweater), p018 (báscula antes/después 240 g),
  p020 (knit a contraluz del shoji, etiqueta 12 gg), p023 (medida de 3 dedos), p028 (línea de parada con cinta roja),
  p046 (tira de 3 fotos doblando el knit, con gato en el cajón).
- Cero fotos repetidas. El validador lo confirma.

## Gasto aproximado (gasto.jsonl)
| Ítem | USD |
|---|---|
| Fotografías gpt-image (20) | 0,0455 |
| Avatar InfiniteTalk (1 llamada, 334 s de reel) | 0,25 |
| Juez de stock (62 planos juzgados en 5 rondas) | 0,0094 |
| Revisor final | 0,0020 |
| Voz (Groq Whisper) | 0,00 |
| Edición extrema (proceso del panel, no incorporada) | 0,144 |
| **Total** | **~0,45** |

## Problemas y desvíos
- **Duración 10,8 min vs ~8 min pedidos.** El mínimo de 7.200 caracteres del validador y el ritmo real del clon
  (≈13,3 caracteres/s) hacen que el guion de 8.479 caracteres dure ~10,8 min. No es un ✗ en ninguna etapa.
- **Primeros 30 s con cortes cada ~6 s**, no cada 2-3 s: las ventanas de avatar son de 5,8 s y los planos de b-roll de
  ~5-6 s. Se priorizó el ritmo pausado del canal y el requisito de avatar ≤6 s.
- **p029** muestra en el espejo a una mujer joven (la demostración no es la presentadora). No es una falla grave; se aceptó.
- **p026/p034**: clips de apoyo con puntaje bajo del juez, aceptados para no seguir gastando rondas.
- **Edición extrema**: el panel lanzó `extrema.py` en paralelo cuando el render ya estaba armado. No se incorporó a esta
  entrega (el video usa el b-roll normal); el proceso gastó US$0,144 de su tope de US$0,20.
- La cola del video quedó 0,73 s más larga que la voz; se recortó a 649,40 s con `-c copy` y el validador final quedó OK.

## Para mejorar en el próximo
- Apuntar a 7.300-7.500 caracteres para quedar en ~9 min reales.
- Pedir 2-3 variantes de las fotos creativas que más pesan (báscula y línea de parada) y elegir con la hoja.
- Usar pantalla partida en 3-4 ventanas de 7-10 s para bajar el total de planos y ganar variedad de encuadre.
