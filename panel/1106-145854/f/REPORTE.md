# REPORTE — Michiko's Kyoto Closet · mk07ds

**Título:** The 8 Color Pairs My Mother Put Next to Older Faces Instead of Black (Kyoto Kimono Dresser)
**Duración:** 1023,46 s (17:03) · 1920×1080 · 30 fps · H.264 CRF 20 · AAC 192 k estéreo
**Voz:** Fish `moda_michiko_ca`, master `voz/master.wav` (1023,45 s) · captions por palabra con Groq
**Avatar:** agnes-video-2.5-flash (lipsync por referencia), 7 clips · 53,3 s generados, 47,2 s en pantalla

## Qué se hizo

1. **Guion** (17 min, 8 pares de color). Gancho 0–45 s con número + objeto + "not because I'm thinner",
   credencial de Fumiko kitsuke-shi, cada ítem con problema → anécdota con fecha/nombre/lugar → por qué
   después de los 60 → cambio concreto con precio en US$ → chequeo frente al espejo esa noche. Test
   interactivo en el minuto 4, ✗/✓ en pantalla, like/subscribe antes del último par, cierre "don't buy,
   open your closet" + frase de Fumiko + pregunta para comentarios + gancho a la serie siguiente.
2. **Voz y tiempos.** Fish con `--keep-tags` (2 tags en todo el guion). Groq devolvió tiempos por palabra;
   cada plano arranca en el `startMs` de la palabra que lo motiva.
3. **Fotos.** 201 ids únicos en 223 archivos de `fotos/`, todas por la cola de avatarity con Nano Banana
   (prompt JSON con los campos obligatorios, pasado por `lint_fotos.py`). Movimiento Ken Burns al azar
   (7 tipos, zoom 5–13 %, foco descentrado, semilla fija) en la herramienta compartida `render.py`.
4. **Avatar.** `avatar.mjs` en modo reference (cara `michiko_face_hd.png`, recorte ≥ 400 px). La intro va
   en tramos de ≤ 6 s intercalados con fotos; después 4 regresos de ~9 s (A4–A7). El segundo 0 es una
   foto (gancho_a, Carol con el pañuelo mostaza), nunca el avatar.
5. **Sonido.** 5 SFX suaves y puntuales (tela, papel, taza, cajón, shoji), gain 0,045–0,060, sin música.
6. **Armado.** `render.py` (215 segmentos, 30 703 cuadros) + `assemble.py` (fundidos 0,6 s avatar /
   0,3 s foto, voz + cues) → `final.mp4`.

## Rehecho durante el trabajo

| Qué | Por qué |
|---|---|
| h28 → h28b | el cartel de la foto tenía texto inventado ilegible; prompt nuevo y revisión con Read |
| 8 segmentos del render | fallaron por presión de memoria (libx264); se relanzó render.py y rehízo sólo esos |
| A6 y A7 | se relanzó `avatar.mjs` cuando terminó el cupo; los cuadros fijos quedaron como respaldo |
| 37 fotos repetidas | el mismo id aparecía en dos secciones vecinas (2–30 s de diferencia). Se cambiaron las 37 apariciones posteriores: 6 se cubrieron con fotos ya existentes sin usar (n01, n03, n04, n07, n35, n36) y 31 se generaron nuevas por la cola (n02, n05, n06, n08–n34, n37). Hojeadas con Read en 4 hojas de contacto; 0 rechazos |

## Gasto

- **APIs pagas: US$ 0,00.** No se usó DeepSeek ni gpt-image en este video (existe `D:/rtmp/SIN_OPENAI`,
  y de todos modos el b-roll va por la cola gratuita de avatarity).
- agnes: 53,3 s de video de avatar generados (7 clips). Fotos: 137 en el slug `mk07ds` + 81 en
  `mk07ds_b` (incluye las 31 de esta corrección); sin costo.

## Problemas

1. **Fotos repetidas entre secciones vecinas.** Causa: el diccionario `SHOTS` de `build_shots.py`
   reutilizaba ids en secciones contiguas para "rellenar". Corregido en el origen (se cambió el id de la
   aparición posterior, nunca la primera) y se regeneró `shots_timed.json` con los mismos tiempos.
2. **`render.py` y extensiones.** El primer barrido de fotos faltantes miraba sólo `*.jpg` y daba 21 falsos
   faltantes que eran `.png`. Se audita con todas las extensiones.
3. **Cola de imágenes: `prompt` tiene que ir como string JSON**, no como objeto (`INVALID_PAYLOAD`).
4. **Refs inexistentes.** Los prompts de Hiroshi y la señora Kinoshita apuntaban a `ch_hiroshi.png` /
   `ch_kinoshita.png`, que no existen en `refs/`; la cola rechazaba el lote entero. Se sacaron las refs y
   esos dos personajes van descritos en texto (son secundarios y salen de espaldas o de perfil).
5. **Presión de memoria / forks en Windows** durante el render: falla esporádica de libx264, se resuelve
   relanzando (los segmentos sin `.src` se rehacen solos).

## Control final

- `validar.py --etapa final --min 15` → **RESULTADO OK** (15 ✓, 1 aviso: 6 de las 223 imágenes de
  `fotos/` no llevan la firma de la cola; son refs y copias internas, no b-roll del video).
- `final.mp4`: 1023,457 s · 1920×1080 · 30 fps · H.264 3,19 Mbps · AAC 190 kbps 44,1 kHz estéreo ·
  433,7 MB. Diferencia con la voz: 0,00 s.
- 34 cuadros cada 30 s en `qc/f_0001…f_0034` (f_0001 = 0 s), mirados en `qc/hoja_fin1/2/3.jpg`, y los
  tramos de avatar en `qc/hoja_avatar_final.jpg`. Sin fechas impresas, sin marcas de agua, sin texto
  inventado, sin manos rotas, sin look de estudio.
- `gates/final_auto.txt` y `gates/final_pedido.txt` escritos. `gates/correcciones.txt`: no existió en
  ningún momento del trabajo, así que no hubo correcciones externas que aplicar.

## Qué falta / notas

- Nada bloqueante. `final.mp4`, `meta.json` y este reporte están en `D:/rtmp/mk07ds`.
- Los ids `gancho_b`, `gancho_c`, `c20`, `t01`, `t02`, `t03` siguen en `fotos/` además de sus copias n*;
  no molestan (el render resuelve por id del plan).
