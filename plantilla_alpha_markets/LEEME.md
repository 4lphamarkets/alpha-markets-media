# Plantilla ALPHA MARKETS v24 (vídeos verticales 9:16)

**Empieza aquí.** Esta página es el resumen; el detalle técnico completo (portadas, sonidos, insertos, motor de dinamismo, historial de versiones) está en `REFERENCIA_TECNICA.md` (el antiguo LEEME de la v22, con las contradicciones corregidas).

## 1. Montar un vídeo en 6 pasos
Requisitos: Python 3 + `numpy` + `pillow`, ffmpeg, Node + `npm i playwright-core` y Google Chrome (`CHROME=<ruta>` si no está en el sitio habitual).
```bash
python scripts/validar.py                                   # 0. comprueba el entorno (1 vez por sesión)
python scripts/transcribir.py tmp/voz.mp3                   # 1. audio de Jaime → frases con su tiempo (a/b) → tmp/transcripcion.json
#    2. escribir tmp/guion_analista.json (o guion_clasico.json) con esos tiempos y el texto BUENO del guion
python scripts/montar.py revisar analista tmp/guion_analista.json   # 3. prep + validar + build + HOJA DE CONTACTO (4 s) → out/hoja_contacto.jpg
#    4. ABRIR out/hoja_contacto.jpg: texto cortado, solapes, piezas fuera de y = 240…1680 → corregir el guion y repetir el paso 3
python scripts/montar.py video analista tmp/guion_analista.json    # 5. render + insertos + efectos + mezcla -16 LUFS + control de calidad → out/video_final.mp4
python scripts/entrega.py out/video_final.mp4               # 6. descripción + 2 portadas (antes: entrega.json, ver FLUJO_DE_TRABAJO.md)
```
- Modo clásico (`template.html`): igual con `clasico` y `scripts/prep_clasico.py` (guion JSON con escenas y frases; cabecera en `scripts/prep_clasico.py`). `template.html` es el vídeo de ejemplo ORO Y PLATA: para un vídeo nuevo se adaptan sus escenas a mano.
- `montar.py` para si un paso falla y dice cuál; con `--sin-prep` repite desde `build` sin regenerar el timeline. `--workers N` fuerza los workers del render.
- Los pasos sueltos siguen funcionando (`build.py`, `render.js stills|video|events`, `insertos.py`, `sfx.py`, `final.py`, `qa_video.py`).

## 2. Mapa de la plantilla
| Qué | Dónde |
|---|---|
| Cómo se trabaja de principio a fin (tema → guion → audio → vídeo → entrega → publicación) | `FLUJO_DE_TRABAJO.md` |
| Rutina diaria automática (08:30: historias + **2** vídeos) | `RUTINA_DIARIA.md` |
| Qué noticias merecen vídeo (puntuación 0-100) | `FILTRO_NOTICIAS.md` · `scripts/filtro_noticias.py` |
| Estilo y componentes del **modo analista** (el principal, 3 de cada 4 vídeos) | `ESTILO_ANALISTA.md` · `template_analista.html` |
| Modo clásico (1 de cada 4, control A/B) | `template.html` (ejemplo ORO Y PLATA) · `template_binance_ejemplo.html` |
| Ganchos, temas, formatos de prueba, medición | `PLAYBOOK_COMPETENCIA.md` |
| Portadas (estilo fijo `foto_epica` + 1 diseño nuevo por vídeo, historial anti-repetición) | `REFERENCIA_TECNICA.md` (v10/v11) · `portadas/` |
| Sonidos, presupuesto de efectos, insertos, momentos dibujados | `REFERENCIA_TECNICA.md` · `sonidos/` · `insertos/` |
| Recursos de edición externos | `recursos_visuales/` |
| Vídeos y scripts de vídeos ya hechos (Nvidia, Binance, Oro): solo consulta | `archivo/` |

## 3. Reglas fijas (resumen; mandan los detalles de los documentos anteriores)
- **Formato**: 1080×1920, 30 fps, H.264 High slow CRF 12 (PNG sin pérdida), AAC 320 kbps 48 kHz, −16 LUFS / pico −1 dBTP. No se cambia por ir más rápido.
- **Duración (v24)**: **máximo 40 s** (~90-100 palabras). Si Antonio pide otra, manda la suya. Sin música.
- **Marca**: en pantalla **4LPHA MARKETS** (perfil @4lphamarkets); en el texto del audio se escribe «Alfa Markets» para la pronunciación. Cierre cripto fijo: «Sígueme para no perderte nada de los mercados financieros, esto es... Alfa Markets!!». Cabecera con el logo de letras (`img/logo_alpha_wordmark.png`), nunca avatar + texto.
- **Voz**: ElevenLabs, «Jaime - Confident, Clear and Warm», `[en tono juguetón]` al principio, **una sola generación** (no reintentar). Créditos (v24): se genera **sin pedir OK si el audio cuesta ≤ 2.000 créditos**; solo se pregunta si supera 2.000 (estimar antes y respetar los límites de `RUTINA_DIARIA.md`).
- **Subtítulos**: mayúsculas, blancos, tamaño moderado, Montserrat Black (y/o Awesome Serif Italic Bold ExtraTall variando según lo que quede mejor).
- **Zona segura**: nada importante fuera de y = 240…1680.
- **Sonido**: ~14-19 efectos por cada 30 s, un sonido por golpe, la voz siempre por delante (`sfx.py` recorta el exceso).
- **Cada vídeo**: 1-2 momentos dibujados, personas y logos reales en la portada (si falta la foto de una persona, se pide; nunca se genera), datos con fuente, «esto no es consejo financiero» en la última línea de la descripción.
- **Entrega**: carpeta `<slug>` con vídeo, descripción y 2 portadas, **enviada suelta por el chat (sin zip) y dejada SIEMPRE en el Escritorio** (`~/Desktop/<slug>/`, con TODO: vídeo, descripción y 2 portadas) antes del mensaje final, **sin pedir permiso (v24)**. Publicar en Instagram/YouTube solo con el «OK» (o según `RUTINA_DIARIA.md`).

## 4. Novedades v23 (revisión a fondo de la v22)
**Más fluidez**
- `scripts/montar.py`: todo el montaje con un comando (antes 8 comandos a mano), con **hoja de contacto** para revisar el vídeo de un vistazo antes de renderizar.
- `scripts/validar.py`: comprueba el entorno y el timeline **antes** del render (escenas con huecos, subtítulos fuera de su escena, componentes mal escritos, imágenes que no existen…). Un error de guion se ve en 1 s, no tras 15 min de render.
- `scripts/prep_clasico.py` y `scripts/transcribir.py` genéricos: sustituyen a `prep_oro/prep_nvidia/prep3/prep4/asr_run*`, que llevaban los tiempos de un vídeo concreto escritos a mano (movidos a `archivo/scripts_por_video/`).
- `render.js`: progreso por consola, detecta Chrome/Chromium en Windows, Mac y Linux, GPU con flags correctos por sistema, borra las partes temporales y espera a que fuentes **e imágenes** estén cargadas antes del primer fotograma.

**Más calidad**
- Modo analista: el *kicker* se cortaba («SEMANA DEL 23 ›») → ahora se ajusta solo; cabecera dentro de la zona segura (y ≥ 245); desaparece la banda negra que dejaba el desenfoque del fondo en el borde superior; la escala de las escenas se calcula con las fuentes ya cargadas (antes la escena 1 se medía con la fuente de reserva); subtítulos partidos en líneas **equilibradas** (antes salía «SEGUIDOS» suelto en una línea).
- Mezcla final con loudnorm en **dos pasadas** (antes una sola pasada dinámica: el volumen real quedaba entre −17 y −14 LUFS) y `qa_video.py` (resolución, fps, códec, audio, duración vs. timeline, volumen, pico, fotogramas negros).
- Errores claros en lugar de trazas: componente desconocido, escena que no existe, campos que faltan en `entrega.json`.

**v24 (22-11-2026)**
- Vídeos de **40 s como máximo** (guion de ~90-100 palabras; `qa_video.py` marca error por encima de 41 s y `validar.py` avisa).
- ElevenLabs: **sin pedir OK salvo que un audio cueste más de 2.000 créditos**.
- Carpeta en el Escritorio con todo (vídeo, descripción y 2 portadas): **se deja sin pedir permiso**.

**Más efectividad**
- Plantilla **limpia para el vídeo siguiente**: ya no viaja el `entrega.json` ni el `insertos.json` del vídeo de Nvidia (se usaban por defecto si no se reescribían), ni el `index.html`/`portada_index.html` de 2,3 MB generados, ni la caché de Python (`archivo/video_nvidia/`).
- `filtro_noticias.py`: 2 vídeos al día por defecto (decisión del 22-11-2026) y marca las de 60-69 como «relleno».
- Documentación sin contradicciones: duración 40 s–1:20 (el LEEME antiguo aún decía 30-45 s), «Alfa Markets» en el audio y 4LPHA MARKETS en pantalla, entrega sin zip, 8-15 hashtags (el script avisaba solo fuera de 5-15).

**Errores concretos corregidos**
- `insertos.py` salía con error (código 1) cuando `insertos.json` estaba vacío; y si `tmp/video_sin_insertos.mp4` venía de otro vídeo se montaban los insertos sobre el vídeo viejo (ahora `render.js` lo borra al renderizar uno nuevo).
- `timeline_ejemplo_analista.json` no era JSON válido (`.1` en vez de `0.1`).
- `prep_analista.py`: si la primera escena no empezaba en 0, los primeros fotogramas mostraban la última escena.
- En `template_analista.html`, `from` de la cifra del componente `num` chocaba con `from:"side"`: la entrada de lado se escribe ahora `"enter":"side"` (`from:"side"` sigue valiendo en el resto).
- `template.html`: la píldora roja «ORO Y PLATA» estaba fija (ahora `"tag"` en el timeline) y una escena sin función `upd` rompía el render.

**Pendiente de decidir por Antonio** (no se ha tocado): el A/B 3 de 4 analista / 1 de 4 clásico, y los pesos del filtro de noticias; se recalibran con las métricas del 27-11 y el 4-12.
