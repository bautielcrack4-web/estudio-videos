# FN10DS — "After Burying 7,000 People, This Is the Funeral I Want for Myself"

**Canal:** Ernie Navarro, Funeral Director (inglés) · **Voz:** Fish `ernie_en` · **Entrega:** `D:/rtmp/fn10ds/final.mp4`

## Entregado
| | |
|---|---|
| `final.mp4` | 1526.93 s = **25 min 27 s**, 1920x1080, 30 fps, H.264 CRF 20, AAC 192 kbps 48 kHz estéreo, 731,3 MB |
| `guion.txt` | 3.987 palabras (validado, sin palabras prohibidas, sin claims médicos) |
| `voz/master.wav` | 1526,93 s, Fish, conc. 3 (manifest en `voz/manifest.json`) |
| `captions.json` | 3.827 palabras con tiempos (Groq free, ~50 ms) — de ahí salen todos los cortes |
| `shots_timed.json` | 211 tomas, 0 → 1.526.681 ms, sin huecos ni solapes |
| `avatar_ranges.json` | 106 ventanas (A0…A105), 508,3 s de reel, **477 s en el video = 31 %** |
| `meta.json` | título + descripción (4 párrafos, con el papel de US$4.810, precios FTC y Ofelia de Laredo) |
| `cues.json` | 6 SFX (papel, café, campana, fósforo, puerta, tierra), gain 0,05–0,07 |
| `qc/` | 51 cuadros cada 30 s + 5 hojas de contacto + hojas de fotos y de render |
| `gates/` | guion, fotos, render y final: `_auto.txt` + `_pedido.txt` |

## Cómo se hizo
1. **Guion** de 25 min con la estructura pedida (gancho con número y objeto, credencial, test interactivo
   al minuto 4, problema → anécdota con fecha/nombre/lugar → por qué pasa → cambio con precio → chequeo
   para esa noche, CTA antes del último punto, cierre con pregunta y gancho a fn11). La historia de la madre
   (Don Refugio, Mezquitán, 3-nov-1999) quedó textual como está en la BIBLIA.
2. **Voz** Fish + **transcripción** Groq por palabra → cortes clavados en la palabra que los motiva.
3. **Fotos**: 211 fotos reales pedidas por la cola de avatarity con prompt JSON completo (Nano Banana para
   prioridad 0 y el desvío automático a gpt-image-2 para el resto; nunca agnes-imagen). Revisadas en hojas
   de contacto de 12; se repitieron las que tenían manos rotas, fecha impresa o look de estudio.
4. **Avatar**: una sola llamada de InfiniteTalk (`tools/avatar_it.py`), foto de referencia =
   `funerario/refs/ernesto_av.png`, desfase medido y corregido (`avatar/it_sync.json`, máx 395 ms).
5. **Render**: por la nube nueva (`render.py` → `nube.py` → GitHub Actions): un tar de 248 MB con fotos y
   avatar + otro de 60 MB con voz y SFX, 20 tandas en paralelo, final.mp4 bajado directo. No hizo falta
   `assemble.py`: la nube hace segmentos, fundidos (0,6 s avatar↔foto / 0,3 s foto↔foto), mezcla de audio y pegado.

## Gastos
| | |
|---|---|
| InfiniteTalk (RunPod, vía avatar_it.py) | **US$ 0,25** |
| Fotos (cola avatarity) | US$ 0 |
| Fish, Groq, SFX (Mixkit) | US$ 0 |
| Render (GitHub Actions) | US$ 0 |
| **Total** | **US$ 0,25** |

## Problemas y cómo los resolví
- **La cola de fotos iba lenta** (0,22 fotos/min con 161 faltando). Seguí trabajando con lo que llegaba;
  al final llegaron todas y el plan quedó con **211 fotos reales, 0 sustituciones**.
- **El primer render quedó colgado** subiendo archivo por archivo (40/312 en 20 min) porque estaba corriendo
  la versión vieja de `nube.py`. Lo maté (`taskkill`) y relancé con la versión nueva: 4 minutos.
- **Disco lleno** (`No space left on device`) por un `video_noaudio.mp4` de 641 MB que quedó de un armado
  viejo. Lo borré (5,7 GB libres) y pude extraer los cuadros de control.
- **Hueco de 1,1 s** antes del avatar A96 (138,3 → 138,5 s). Alargué `l04_mapa_pared` a 138,5 s: el validador
  pasó a "0 huecos sin imagen".
- **Plano prohibido**: `d09_velorio_tres_dias` mostraba un cuerpo en la caja. Lo cambié por `d11_rosario_casa`
  (velorio de casa lleno, con vela) en la misma ventana de 398,9–405,1 s.
- **Último cuadro con letras inventadas**: la foto del cierre (`m20_foto_1958_marco`) tenía un cartel con
  pseudo-texto de IA. La repedí por la cola con el cartel liso (`m20b_foto_1958_marco`) y re-rendericé sólo
  el tramo afectado: 3,8 min de nube + descarga. El cierre quedó sin una sola letra (ver `qc/ultimo2.jpg`).
- **Foto fuera de lugar en la historia del padre** (20:20): `j17_hermano_cara` mostraba a un hombre
  anglosajón de traje en un cementerio con césped y sillas plegables, mientras la voz dice "at the gate of
  the Mezquitán" y el padre le habla al oído. La repedí por la cola como `j17b_padre_porton` (señor mexicano
  mayor con guayabera, sombrero en las manos y rosario, en el portón de un panteón de Guadalajara, con cubeta
  de cempasúchil y perro en la esquina) y re-rendericé: 8 min de nube + descarga. El cuadro nuevo está en
  `qc/chk1220n.jpg`.
- **16 segmentos** se re-renderizaron en el camino por cambios de plan; sólo se rehízo lo que cambió.

## Avisos que dejo anotados (no frenan)
- 4 fotos duran más de 8 s (aviso del validador; no hay hueco negro ni desincronización).
- Dos fotos con texto legible: "CERTIFICATE OF DEATH" y un teléfono con una lista de correos. Se leen bien
  y no están mal escritas; quedan.
- `c08_upsell` se siente algo "de catálogo"; sale una sola vez.
- **No lleva música**: sólo voz + 6 SFX puntuales.

## Qué falta
Nada del video. El archivo está en `D:/rtmp/fn10ds/final.mp4` con `final.mp4.plan` (huella del plan) para que
la nube no lo vuelva a renderizar. La entrega/publicación la hace el creador desde el panel.
