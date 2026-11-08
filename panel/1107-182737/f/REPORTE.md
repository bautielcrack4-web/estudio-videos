# REPORTE — fn02ds

**Titulo:** What Happens at a Mexican Wake That American Funeral Homes Never Allow — A Funeral Director of 40 Years
**Canal:** Ernie Navarro, director de funeraria (version en ingles de Ernesto Navarro)
**Idioma:** ingles · **Duracion final:** 27:57.6 (1677.6 s) · **Voz:** 1677.6 s

## Que se hizo

| Etapa | Estado |
|---|---|
| Guion | `guion.txt`, 174 lineas, 4419 palabras (aviso del validador, no error). Sin palabras medicas ni de IA. |
| Voz | Fish, voz `ernie_en`, `voz/master.wav`, 1677.6 s. |
| Captions | Groq ASR por palabra, `captions.json`, 4327 palabras, ultima en 1677591 ms. |
| Plan de avatar | `plan_avatar.py` -> 105 ventanas, 479.1 s = 28.6%, todas de 3-6 s, maximo 13.4 s sin avatar, primera ventana 0-6.24 s. Plan CERRADO antes de la unica llamada. |
| Avatar | `avatar_it.py` (InfiniteTalk), 1 llamada, US$0,25, reel de 510.6 s, desfase medido y corregido (max 395 ms). 105 clips `avatar/A0..A104.mp4`. |
| Fotos | 222 fotos en `fotos/` (194 del lote revisado + pruebas y creativas; 2 rechazadas por la regla de pantalla en `qc/rechazadas/`). Pedidas por la cola compartida (slugs fn02ds / fn02ds_b), prompt JSON completo, linter `lint_fotos.py` pasado. 6 creativas GPT con detalle narrativo. |
| Referencia del avatar | Pedido del creador (7-nov): el frame de la primera ventana es `D:/rtmp/funerario/refs/ernesto_av.png` (foto de ChatGPT web). Se aplico en `avatar_ranges.json`; copia en `avatar/frames/a1_ref.png`. La llamada unica ya estaba hecha con `a1.jpg` (misma escena y personaje), asi que A0.mp4 coincide con la referencia nueva pero no se puede regenerar (regla de 1 llamada por video). |
| Gancho | 3 variantes (gancho_a/b/c); elegida **gancho_b** (familia descargando bandejas de la camioneta de noche) — ver `gates/fotos_auto.txt`. |
| SFX | 6 sonidos de Mixkit elegidos a mano por nombre y duracion; `cues.json` con ganancia 0.035-0.07. Sin musica. |
| Armado | `render.py` en GITHUB (nube del creador, 22 maquinas): 321 segmentos, 21 tandas, render en 4.7 min, fundidos + voz + SFX + descarga de `final.mp4` entero. `assemble.py` ya no se usa localmente (va a GitHub). |

## Final

- `final.mp4`: 1920x1080, H.264 CRF 20, 30 fps, AAC 192k **estereo**, 645 MB, 27:57.6.
- 321 segmentos: 105 de avatar (479 s, 29 % del video) y 216 de foto con Ken Burns al azar
  (semilla fija, 3840x2160 -> 1920x1080), fundidos avatar 0.6 s / foto 0.3 s.
- Apertura: avatar hablando desde el segundo 0, ventana 0-6.24 s, despues gancho_b y cortes
  cada 2-3 s alternando avatar y fotos en los primeros 30 s.
- `validar.py --etapa final --min 25`: **RESULTADO OK**, 0 errores.
- Revision visual: `qc/final_sheet1..5.jpg` (56 cuadros cada 30 s) y `qc/hoja_t0.jpg`.
- Gates: `gates/final_auto.txt` y `gates/final_pedido.txt`. No habia `gates/correcciones.txt`.

## Costos

- InfiniteTalk / RunPod: **US$0,25** (1 llamada).
- Fotos: cola compartida, sin costo por pieza.
- Render: GitHub Actions de la nube del creador, sin costo por video.
- Voz (Fish), captions (Groq), SFX: gratis.
- DeepSeek (redaccion de guion, prompts y este armado): costo de la sesion, sin cargo aparte.

## Problemas y recambios

- Cola de fotos compartida saturada al principio (~2 fotos cada 9 min); se resolvio con el
  desvio automatico de la cola y el video se armo con 222 fotos propias. Las que faltaron se
  repiten espaciadas (nunca dos veces seguidas): 0 ids consecutivos repetidos en 216 planos.
- `t01_sala` (ataud abierto con tela blanca) descartada por la regla de pantalla; reemplazo
  `t01_sala2` (ataud cerrado).
- `c5_06` (mujeres tocando a una persona acostada con la cara visible) descartada por la regla
  de pantalla -> `qc/rechazadas/`.
- `c4_07` fallida en la cola (falso positivo de CONTENT_POLICY con "young"); el capitulo 4
  tiene 11 fotos y alcanza.
- RunPod tardo en asignar el job de InfiniteTalk (IN_QUEUE); no se relanzo la llamada.
- Los primeros intentos de armado local (`assemble.py` con xfade) fallaron por memoria
  ("Cannot allocate memory") con la maquina al 100 %; se abandono el armado local y se paso
  al render en GitHub que indico el creador.
- Aviso del validador: 4419 palabras de guion (por encima del rango para 25 min). El video
  dura 27:57 y el presentador no se va por las ramas; se deja como aviso.
- Dudas anotadas en `gates/final_pedido.txt`: c5_01 (ataud abierto + mano con rosario, sin
  cuerpo ni cara) y el cuaderno con lista legible en ingles.

## Pendiente

- Nada. Video cerrado: `final.mp4`, `meta.json` y `REPORTE.md` listos.
