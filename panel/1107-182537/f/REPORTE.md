# REPORTE — hr02ds

**Video:** "What the Final 48 Hours of Life Actually Look Like (A Hospice Chaplain of 34 Years)"
**Personaje:** Rosa, capellana de hospice (34 años). Nunca se presenta como enfermera ni médica.
**Estado:** ENTREGADO. `final.mp4` listo, validador `--etapa final` en **OK**.

---

## 1. Números finales

| Dato | Valor |
|---|---|
| Duración de `final.mp4` | 1878.30 s (31:18) |
| Duración de la voz (`voz/master.wav`) | 1878.30 s (dif 0.00 s) |
| Imagen | 1920x1080, 30 fps, H.264 CRF 20 |
| Audio | AAC 192 kbps, estéreo |
| Peso del archivo | 845 MB |
| Guion | 5217 palabras (~167 ppm) |
| Fotos en `fotos/` | 200 archivos (161 PNG + 39 JPG) |
| Fotos únicas usadas | 191 |
| Planos del montaje (`shots_timed.json`) | 217 (corte cada 3-5 s, sin huecos) |
| Ventanas de avatar | 141 clips (`avatar/A0…A140.mp4`) |
| Tiempo total de avatar | 545.6 s = **29 %** del video (estilo Bertha) |
| Ventana de avatar más larga | 6 s (ninguna >20 s sin avatar) |
| Clips de video (Veo/i2v) | 0 — todo b-roll con fotos y Ken Burns |
| SFX | 5 cues puntuales (`cues.json`), sin música |

## 2. Qué se hizo

1. **Guion** en inglés, en la voz de Rosa, con la estructura pedida: gancho con
   número y objeto, credencial de 34 años, la "prueba de la puerta" (~min 4),
   problema → anécdota con fecha/nombre/lugar → por qué → cambio concreto con
   precio → chequeo de "esta noche", like/subscribe antes del último punto,
   pregunta para comentarios y enganche al próximo video. Sin las palabras
   prohibidas (nurse, doctor, clinic, cure, heal, as an ai, artificial
   intelligence) y sin consejos médicos: siempre "llamá a tu equipo de hospice".
   Validado con `validar.py --etapa guion`.
2. **Voz** con Fish (`rosa_mx`), bloque por bloque, master único de 31:18.
3. **Transcripción** con Groq: `captions.json` con tiempos por palabra (~50 ms),
   que es lo que fija el `startMs` de cada plano.
4. **Fotos**: 200 imágenes de b-roll por la cola de avatarity (Nano Banana /
   gpt-image-2 según prioridad), cada una con su JSON narrativo (`moment`,
   `action`, `props` de 6-10 objetos, `camera` variada, ≥30 % primeros planos,
   ≥60 % con personas o manos). Se revisaron por hojas de contacto y se
   repidieron las que salían "de estudio", con texto inventado o aburridas.
   También se hicieron las imágenes creativas de GPT (cuaderno a cámara,
   lista escrita a mano, collage de rutina) con la cláusula de realismo y su
   capa de detalle narrativo.
5. **Avatar**: InfiniteTalk, **una sola llamada** (`avatar_it.py`), 141 ventanas
   concatenadas en un reel de 587.9 s y cortadas de nuevo, con el desfase del
   reel medido y corregido (máximo 395 ms). La foto de referencia es el frame
   de la primera ventana (`avatar/frames/a1.jpg`), así todas las ventanas
   salen del mismo set (su cocina).
6. **Render y armado**: en GitHub (`render.py` sube el paquete, 24 máquinas
   renderizan en paralelo, se unen los fundidos y se mezcla voz + SFX).
   `assemble.py` también corrió en GitHub. No se renderizó en la PC.
7. **QC**: 63 cuadros cada 30 s (`qc/f_001…f_063.jpg`) en 6 hojas de contacto,
   revisados uno por uno. Arranca con Rosa hablando a cámara desde el segundo 0,
   sin huecos negros, sin texto quemado, sin caras ni manos rotas.

## 3. Costos

| Servicio | Costo |
|---|---|
| InfiniteTalk (RunPod) — avatar | **US$0.25** |
| Fish (voz) | gratis |
| Groq (transcripción) | gratis |
| Nano Banana / gpt-image-2 (fotos) | gratis por cola compartida |
| Render en GitHub | gratis (cola de 24 máquinas) |
| DeepSeek (texto: guion y planificación) | centavos, no medido aparte |
| **Total estimado** | **~US$0.25** |

## 4. Problemas y cómo se resolvieron

- **Guion más largo que el rango del validador**: 5217 palabras contra el rango
  esperado de 2762-4312 para 25 min. El video quedó en 31:18 (la voz se generó
  completa), así que la densidad es normal; se dejó como aviso, no como error.
- **Render/armado local se quedaba sin memoria**: la PC no daba abasto con 20
  videos en paralelo (libx264 abría demasiados hilos). Se probó y se localizó
  el problema con `test_chunk2.py` (limitando `-threads 2` ya no fallaba), pero
  el creador movió el render a GitHub y se abandonó esa vía: `render.py` y
  `assemble.py` corren en la nube. Los scripts locales (`assemble_light.py`,
  `test_chunk*.py`) quedan como residuo, sin uso.
- **Disco casi lleno (D: con 1.6 GB libres)** al armar el paquete de subida:
  se borraron artefactos viejos del render local (`xf_l1`, `xf_tmp`,
  `segments`, mp4 de prueba) y quedaron ~5.8 GB libres.
- **Varias instancias de `render.py` peleándose por la misma descarga**
  (`final.mp4.bajando` bloqueado, `WinError 32`): se mataron los procesos
  sobrantes y se dejó terminar la descarga de `gh`. El archivo bajó completo
  y se renombró a `final.mp4` (verificado con `ffprobe` antes de renombrar).
- **Faltaban 8 fotos** (e25-e32) cuando la cola ya marcaba 0 pendientes: se
  volvieron a pedir en un lote aparte (`pedidos_e2.json`) y llegaron todas.
  Al final: 191 ids reales, 0 sustituidas en `shots_timed.json`.
- **Aviso de pantalla**: una foto de cama (persona tapada con una colcha vista
  desde el pasillo) y un hombre mayor dormido en un sillón quedaron justo en
  el límite de la regla "nunca una cara de moribundo". Se aceptaron porque no
  muestran caras de agonía ni cuerpos: son escenas domésticas de descanso.

## 5. Qué se puede mejorar

- El guion podría recortarse a ~25 min (4300 palabras) para que entre en el
  rango que pide el validador; hoy dura 31:18 y es un video largo.
- Hay 200 fotos en disco y 191 se usan: las 9 restantes quedaron sin montar
  (variantes descartadas).
- Un cuadro aislado (~min 12:30) agarra a mitad de un fundido entre una foto
  de Rosa y su clip de avatar en la misma cocina y se ve la cara duplicada por
  un instante. Se puede acortar ese fundido a 0.3 s si molesta.
- Se podría sumar música muy baja en los tramos de anécdota; se dejó sin
  música a propósito (sólo voz y SFX puntuales).

## 6. Archivos

`guion.txt` · `voz/master.wav` · `captions.json` · `avatar/` (141 clips) +
`avatar/frames/` · `fotos/` (200) · `sfx/` (17 archivos, 5 usados) ·
`shots_timed.json` · `shots_planned.json` · `avatar_ranges.json` ·
`cues.json` · `plan.json` · `segments/` · `qc/` (63 cuadros + hojas) ·
`final.mp4` · `meta.json` · `gates/` (guion, fotos, render, final).
