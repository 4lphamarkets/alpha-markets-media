# Plantilla ALPHA MARKETS v22 (vídeos verticales 9:16)
## ⭐ NOVEDADES v22: MODO ANALISTA + FILTRO DE NOTICIAS (leer `ESTILO_ANALISTA.md` y `FILTRO_NOTICIAS.md`)
Tras analizar en profundidad @h.analistasoficial y @lacartabursatil (22-11-2026): (1) **`template_analista.html`**: segundo motor de edición, sobrio y de «un elemento cada vez» (píldora con hora → titular → widget → dato rojo; calendario, velas y líneas que se dibujan, cifra gigante, subtítulos discretos). Se usa con `python scripts/prep_analista.py tmp/guion_analista.json` y `python scripts/build.py analista`; ejemplo en `timeline_ejemplo_analista.json`. El modo clásico (`template.html`, v21) sigue intacto (render, sonidos, portadas, entrega, publicación iguales). (2) **Filtro de noticias** con puntuación 0-100 (`scripts/filtro_noticias.py`, ejemplo `filtro_ejemplo.json`). (3) A/B: 3 de 4 vídeos en modo analista y 1 de 4 en clásico durante 2 semanas; KPI = enviados/vistas.
# Plantilla ALPHA MARKETS v21 (vídeos verticales 9:16)

## 🆕 v21: MÁS WORKERS AUTOMÁTICOS + GPU OPCIONAL
`node scripts/render.js video` ahora elige solo los workers (mitad de los hilos, entre 4 y 12; Ryzen 9 → hasta 12). Para forzar: `node scripts/render.js video 8`. GPU opcional con la variable `GPU=1` (PowerShell: `$env:GPU=1; node scripts/render.js video`): sin probar todavía, comprobar que los fotogramas salen idénticos antes de dejarlo fijo. La calidad (PNG sin pérdida + H.264 slow CRF 12) no cambia.

## 🆕 v20: RENDER ~2x MÁS RÁPIDO (misma calidad)
`scripts/render.js` captura cada fotograma con `Page.captureScreenshot` (CDP) y `optimizeForSpeed`: sigue siendo PNG sin pérdida con píxeles idénticos (diferencia máx. 0 medida en 3 fotogramas); H.264 slow CRF 12 y el resto de ajustes NO cambian. Medido con 60 fotogramas y 2 workers en 2 CPU: 36,9 s → 17,5 s.

## 🆕 v19: RECURSOS VISUALES DE EDICIÓN (carpeta `recursos_visuales/`)
Se añadieron 11 repos de edición de vídeo (earshot, pixelfx, hyperframes, huashu-motion, claude-animated-shorts, lemo-opuscar, rea-video, react-three-rapier, blender-mcp, Wan2.2, LTX-Video). Leer `recursos_visuales/RECURSOS_VISUALES.md` (qué aporta cada uno y cuándo usarlo) y ejecutar `bash recursos_visuales/INSTALAR.sh` al empezar (reclona e instala todo; el sandbox es temporal). En **cada vídeo nuevo** usar 2-3 de estos recursos: SFX variados con earshot, insertos animados con pixelfx/hyperframes, apertura/cierre distintivos, sin romper el flujo v18 ni la legibilidad (la voz manda). Guías de cada repo en `recursos_visuales/guias/`.

## ⭐ NOVEDADES v18: PLAYBOOK DE COMPETENCIA (leer `PLAYBOOK_COMPETENCIA.md`)
Tras analizar cuentas de Instagram sin cara del nicho (noticias de bolsa EEUU y cripto en español), se añade un playbook de temas, ganchos, portadas y formatos de prueba. Cambios concretos: (1) orden de prioridad de temas (eventos con hora exacta primero); (2) fórmulas de gancho con número concreto en la primera frase; (3) dos conceptos nuevos de portada, `dos_cifras` y `cuenta_atras`, en `portadas/CATALOGO.md`; (4) dos formatos de prueba por semana (cuenta atrás de evento y meme de inversor con animación propia, sin clips ajenos); (5) medición semanal. No cambia nada del montaje técnico, la marca ni la entrega.
## (v17) NOVEDADES v17: CARPETA EN EL ESCRITORIO = PASO OBLIGATORIO (aviso del usuario)
En el vídeo ORO Y PLATA Claude entregó los archivos sueltos y NO dejó la carpeta en el Escritorio; el usuario lo reclamó. Desde v17 es obligatorio y se hace SIEMPRE antes del mensaje final (ver aviso al principio de `FLUJO_DE_TRABAJO.md`): `SendUserFile` ×4 → `device_request_folder_access ~/Desktop` (si hace falta) → `device_commit_files` ×4 a `~/Desktop/<slug>/`. Sin ese `written` confirmado, el vídeo no se da por entregado.
Incluidos como ejemplo del vídeo ORO Y PLATA: `template.html` (escenas de oro/plata/dólar/Fed; el de Binance está en `template_binance_ejemplo.html`), `scripts/prep_oro.py` (timeline con el audio SIN cortes, escenas y subtítulos por frases; útil cuando el audio de ElevenLabs sale limpio), `portadas/disenos/oro_plata_caida_b.html` (ejemplo `grafica_gigante`) y logos `img/logos/oro.png` y `img/logos/plata.png` (monedas Au/Ag para portadas de metales). Transcripción: Whisper small de sherpa-onnx (`pip install sherpa-onnx`; modelo en github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2) con segmentos por silencios (`ffmpeg silencedetect`).
Notas de montaje aprendidas: `.scene` empieza en top:390px (si no, choca con el logo); el render completo de ~59 s tarda ~15 min con 2 CPU (lanzar en segundo plano y esperar); si se repite `entrega.py` hay que quitar la entrada del slug de `portadas/historial.json` y de `~/.alpha_markets/historial_portadas.json`.
# (v16) Plantilla ALPHA MARKETS (vídeos verticales 9:16)
## ⭐ NOVEDADES v16: CARPETA EN EL ESCRITORIO AL TERMINAR
Cuando el vídeo está terminado y entregado, Claude **deja siempre una carpeta `<slug>` en el Escritorio del usuario** (vídeo, 2 miniaturas y descripción), sin que lo pida. Pasos en `FLUJO_DE_TRABAJO.md` → «5b» (`device_request_folder_access` ~/Desktop la primera vez + `device_commit_files` con los `file_uuid` de `SendUserFile`).
## (v15)
## ⭐ NOVEDADES v15: FLUJO DE TRABAJO INCLUIDO EN LA PLANTILLA (leer primero: `FLUJO_DE_TRABAJO.md`)
El flujo acordado con el usuario viaja ahora dentro de la plantilla. Resumen (detalle en `FLUJO_DE_TRABAJO.md`):
1. El usuario manda el **tema**: en **imagen** o pide un tema en **texto** (Claude propone uno y arranca).
2. Claude escribe el **guion de MÁXIMO 40 s (orden de Antonio, 23-11-2026; manda sobre cualquier otra duración de este documento)** (sustituye al antiguo límite de 30–45 s de este documento; si el usuario pide otra duración, manda la suya). Cierre cripto fijo: «Sígueme para no perderte nada de los mercados financieros, esto es... ALFA MARKETS!!».
3. Claude genera el **audio con Jaime** («Jaime - Confident, Clear and Warm») en **ElevenLabs** (texto a voz), con la etiqueta **[en tono juguetón]** al principio y **una sola generación**.
4. Claude **monta el vídeo** con esta plantilla (sección «Flujo» más abajo).
5. Claude **genera la carpeta de entrega** (sin comprimir): vídeo editado + descripción + 2 miniaturas, y la manda al usuario.
6. Con el **«OK»** del usuario, Claude lo publica en Instagram (Reel) y YouTube (Short) vía Metricool.
Todo sin pedir permiso entre pasos; solo se para para pedir la foto de una persona que falte, avisar de un bloqueo o esperar el OK de publicación.
Nota: donde más abajo se lea «máx. 30 s / 45 s», aplica ahora 40 s – 1:20 (los números de efectos, insertos y momentos dibujados se escalan en proporción para vídeos de más de 45 s).
## ⭐ NOVEDADES v14: LOGO DE LETRAS EN LA CABECERA (vídeo, portadas e historias)
El logo de arriba a la izquierda es SIEMPRE el logo de letras del canal: flecha + «ALPHA» (blanco cursiva) + «MARKETS» (menta pincel), **sin cara**: `img/logo_alpha_wordmark.png` (PNG transparente, sacado de la historia «MERCADOS HOY» del usuario). NUNCA avatar + texto 4LPHA MARKETS ni el logo cuadrado con la cara.
- Vídeo: `template.html` → `#brand` muestra solo ese logo (150 px de alto, brillo menta), sin texto al lado.
- Portadas e historias: `marca()` de `portadas/kit.js` devuelve ese logo (el parámetro `variante` se ignora; `tam` 44 ≈ 84 px de alto; en historias `marca('',82)` ≈ 155 px de alto ≈ 500 de ancho, con la fecha a la derecha). Estilo en `portadas/kit.css` (`.marca-logo`).
- `img/logo_alpha_markets.jpg` = logo cuadrado con la cara (solo referencia, no se usa en cabeceras). `img/avatar.jpg` sigue solo en la tarjeta de perfil de Instagram del final (botón Seguir).
## ⭐ HISTORIAS DE INSTAGRAM («hazme una historia con el tema X»)
Carpeta `historias/` (ejemplo: `nvidia_resultados.html`, 1080×1920 a sangre, sin franjas vacías arriba/abajo, oso y toro en `historias/assets/`). Estilo «MERCADOS HOY»: cabecera con logo oficial + fecha, titular blanco + palabra clave menta cursiva, tarjetas con icono/título/precio/variación (verde sube, rojo baja), bloque inferior con gráfico u otro dato y fuentes al pie. Datos siempre buscados al momento y con la fuente. Se renderiza con Chrome (viewport 1080×1920), se manda al usuario y con su «OK» se publica como Story en Instagram vía Metricool (imagen subida a Google Drive con enlace público).

## ⭐ NOVEDADES v12: DESCRIPCIÓN LIMPIA PARA COPIAR Y PEGAR
`<slug>_descripcion.txt` ya NO lleva rótulos («TÍTULO SEO…», «DESCRIPCIÓN + HASHTAGS…», «PALABRAS CLAVE») ni la lista de palabras clave. Contiene solo:
línea 1 = título · línea en blanco · descripción · línea en blanco · hashtags en una sola línea. Es el texto exacto que se publica (el título va al título de YouTube Shorts y la descripción + hashtags a Reels/Shorts).
`palabras_clave` sigue existiendo en `entrega.json` como ayuda para escribir el SEO, pero no se imprime en ningún sitio.
Al pegar la descripción en el chat, pegar ese mismo texto limpio (título, descripción y hashtags), sin rótulos.
Publicación: cuando el usuario responde «OK» a la entrega, Claude publica el vídeo en Instagram (Reel) y YouTube (Short) con Metricool, usando la mejor de las 2 portadas.

# (v11) Plantilla ALPHA MARKETS (vídeos verticales 9:16)
## ⭐ NOVEDADES v11: ESTILO FIJO DE PORTADA "foto_epica" + conversor a 9:16
El usuario quiere este **estilo** de miniatura de forma permanente (referencia: `portadas/referencias/foto_epica_referencia.png`).
⚠️ La referencia es **solo un EJEMPLO** (cumbre EEUU–China–Rusia, con 3 líderes). Lo que se copia es el estilo, NO que siempre haya 3 personas:
fondo verde con globo de puntos y velas, protagonistas grandes con brillo, **frase con punch** en el titular, píldora «fecha · sede» y skyline.
- **Protagonistas = los del vídeo (1 a 3, lo que toque):** si el vídeo habla de **1 persona**, sale 1; de **2**, salen 2; de **2 activos** (p. ej. bitcoin y Binance,
  Hyperliquid y BlackRock) salen sus **logos** como monedas gigantes con brillo de su color (con 2 logos aparece un "VS"; `"union": "×"` lo cambia, `""` lo quita);
  de un país o una cumbre, personas + banderas. Regla de oro: **todo protagonista que se nombre en el vídeo sale en la portada.**
- **Frase con punch (obligatoria):** titular de 2 líneas, MUY corto y que impacte: línea 1 en blanco (contexto, 1 palabra) + línea 2 `*en menta*` (el golpe, 1 palabra).
  Ejemplos: `["TENSIÓN","*EXTREMA*"]`, `["BITCOIN","*DESPLOMA*"]`, `["EL MAYOR","*ROBO*"]`, `["SOLO","*UNO*"]`. Nada de frases largas ni descriptivas; emoción + dato clave.
- **Plantilla**: `portadas/estilos/foto_epica.html` (1080×1920). Úsala como UNA de las dos portadas de cada vídeo (la otra, un concepto nuevo del catálogo).
  No cuenta para el anti-repetición (`ESTILOS_FIJOS` en `scripts/portadas_historial.py`): se puede repetir en todos los vídeos.
- **Cómo usarla** (`entrega.json`, bloque `portada`; todo opcional salvo titulo y fecha_sede):
  ```json
  "portada": {
    "titulo": ["BITCOIN", "*DESPLOMA*"],
    "fecha_sede": "18 NOV 2026 · BINANCE",
    "logos": [{"archivo": "bitcoin", "color": "#F7931A"}, {"archivo": "binance", "color": "#F0B90B"}],
    "personas": [{"nombre": "CZ"}],
    "banderas": ["us", "cn", "ru"],
    "skyline": true,
    "disenos": [
      {"html": "portadas/estilos/foto_epica.html", "arquetipo": "foto_epica", "concepto": "Bitcoin y Binance como monedas gigantes con VS", "tipografia": "Montserrat Black Italic", "paleta": "negro / menta"},
      {"html": "portadas/disenos/<slug>_b.html", "arquetipo": "<otro concepto del catálogo>", "concepto": "...", "tipografia": "...", "paleta": "..."}
    ]
  }
  ```
  · `personas` (fotos) + `logos` (activos) se combinan hasta 3 en total. · `banderas` (`us ru cn ua ir eu jp`) solo si el tema son países; sin ellas queda globo + brillo.
  · `fecha_sede`: lo que va tras el `·` sale en menta (sede, ciudad, empresa, mercado…). · Zona segura (y 240–1680) ya respetada.
- **Fotos de personas**: igual que siempre (v8): `entrega.py` las busca en `img/personas/<nombre>.png|jpg` y **para si faltan** (`FALTA LA FOTO DE ...`): pídeselas al usuario,
  nunca las generes ni las descargues. Mejor **PNG recortado sin fondo**. Los logos: `python scripts/logos.py <nombre>` si faltan.
- **Imagen ya hecha por el usuario** (p. ej. generada fuera) que pide en Reels/Shorts: `python scripts/portada_916.py <imagen> [salida.png]` → 1080×1920 sin recortar nada. Entrégala con SendUserFile.
- `entrega.py` admite `portada.personas` (lista, hasta 3) además de `persona`, y pasa a las portadas `banderas`, `fecha_sede` y `skyline`.

# (v10) Plantilla ALPHA MARKETS (vídeos verticales 9:16)
v10 = las portadas ya NO salen de dos maquetas fijas: **cada vídeo lleva 2 portadas diseñadas desde cero** (ver abajo).
Adjunta este .zip en un chat nuevo junto con tu audio y el tema del vídeo, y pide: "Usa la plantilla ALPHA MARKETS".

## ⚠️ NOVEDADES v10: PORTADAS ORIGINALES, DISEÑADAS DESDE CERO EN CADA VÍDEO (obligatorio)
El usuario se quejó de que siempre recibía "las 2 mismas portadas" (las maquetas v8 "plantilla" e "impacto" con otros textos).
Eso se acabó: `portada.html` y `portada_impacto.html` se han retirado a `portadas/antiguas/` y **no se usan** salvo que el usuario lo pida.
1. **Antes de diseñar**: `python scripts/entrega.py --historial` → muestra las últimas portadas entregadas y los conceptos libres.
   El historial vive en `%USERPROFILE%\.alpha_markets\` (sobrevive entre chats y versiones) y en `portadas/historial.json`.
2. **Elige 2 conceptos distintos** que cuenten la historia de ESTE vídeo (inspiración en `portadas/CATALOGO.md`: periódico, terminal,
   notificación de móvil, ticket, cartel de combate, se busca, revista, tuit, lupa, podio, blueprint... o inventa uno).
   Las dos deben diferir en **composición, tipografía protagonista, paleta dominante y "objeto"/mundo visual**.
3. **Escribe cada portada como un HTML nuevo** en `portadas/disenos/<slug>_a.html` y `<slug>_b.html`, desde una hoja en blanco
   (prohibido copiar un diseño anterior y cambiarle textos/colores). Solo se comparten piezas sueltas del kit:
   `<link rel="stylesheet" href="portadas/kit.css">` (fuentes, colores, `.marca`) y `<script src="portadas/kit.js"></script>`
   (`ajustar(el, anchoMax, fsMax, fsMin)`, `marca(variante, tam)`, `azar(semilla)`, `rgba()`, `esc()`; `window.D` = bloque `portada`).
   Rutas relativas a la raíz de la plantilla (`img/logos/x.png`, `img/personas/x.jpg`). Si maquetas con JS, define `window.fit()`.
4. **Itera mirando el resultado**: `python scripts/portada_preview.py portadas/disenos/<slug>_a.html --guia` → `out/<...>_preview.jpg`
   (la guía rosa marca la zona segura y = 240…1680). Abre el JPG, corrige solapes/cortes y repite hasta que esté impecable.
5. Declara los diseños en `entrega.json` → `portada.disenos`:
   ```json
   "disenos": [
     {"html": "portadas/disenos/<slug>_a.html", "arquetipo": "periodico", "concepto": "Portada de diario con sello 5,2%",
      "tipografia": "serif Georgia", "paleta": "crema / negro / rojo"},
     {"html": "portadas/disenos/<slug>_b.html", "arquetipo": "terminal", "concepto": "Terminal de bolsa con la tabla 13F",
      "tipografia": "mono Consolas", "paleta": "negro / ámbar / menta"}
   ]
   ```
6. `entrega.py` **rechaza la entrega** (`PORTADAS RECHAZADAS: ...`) si: falta `disenos`; las dos comparten arquetipo, tipografía o paleta;
   un arquetipo se usó en las **últimas 8 portadas**; se usa un arquetipo prohibido (`plantilla_v8`, `impacto_v8`...); o el HTML se parece
   estructuralmente (> 0,55) a la otra portada, a una portada anterior o a las maquetas antiguas. Solución: rediseñar, no maquillar.
   `--forzar-repeticion` solo si el USUARIO pide repetir un diseño concreto.
7. Reglas que siguen fijas: 1080×1920; marca 4LPHA MARKETS visible; **protagonistas reales** (foto de la persona —pedírsela al usuario
   si falta, nunca generarla— y **logos reales** de `img/logos/`; nunca un círculo con el nombre escrito haciendo de logo: si no hay logo
   descargable, el nombre va como texto); titular legible en miniatura; solo datos del guion.
Ejemplo completo: `portadas/disenos/hyperliquid_blackrock_purr_a.html` (periódico) y `_b.html` (terminal). Son ejemplos de nivel,
**no plantillas**: el historial ya los tiene y bloquea copias.

## (v8, SUSTITUIDO por v10) 2 PORTADAS TOTALMENTE DISTINTAS POR VÍDEO
> Lo de esta sección solo aplica con `"estilo": "v8"` en `portada` (solo si el usuario lo pide). La parte de **persona y logos** sí sigue vigente.
Con cada vídeo se entregan **dos portadas** para que el usuario elija: `entrega.py` las genera siempre y las mete las dos en el zip (`<slug>_portada_1.jpg` y `<slug>_portada_2.jpg`).
| | Portada 1 · "plantilla" (`portada.html`) | Portada 2 · "impacto" (`portada_impacto.html`) |
|---|---|---|
| Titular | Montserrat Black Italic, línea `*clave*` en degradado menta | **Anton** gigante, la palabra `*clave*` dentro de un **sello rojo** inclinado |
| Fondo | globo / rayos / gráfica / rejilla teñido con el color del logo | **pantalla partida por una grieta** blanca (duelo: rojo vs verde; sin duelo: oscuro vs color del logo) |
| Protagonista | persona en círculo menta + logos orbitando | persona con aro blanco y nombre en cartel; 1 logo = **moneda partida en dos** por la grieta |
| Abajo | tarjeta de cifra | **duelo de cifras** (izq VS der) o **cifra gigante** |
- El bloque `portada2` de `entrega.json` sobrescribe lo que quieras para la 2; la persona y los logos son los mismos en las dos:
  ```json
  "portada2": {
    "titulo": ["Dónde *nunca*", "comprar bitcoin"],          // OBLIGATORIO: titular propio, 1-2 palabras *sello* (no la línea entera)
    "duelo": {"izq": {"etiqueta": "Miedo", "cifra": "64K", "flecha": "abajo"},
              "der": {"etiqueta": "Fomo",  "cifra": "87K", "flecha": "arriba"}}   // opcional; colores por defecto rojo/verde, o "color"
  }
  ```
  Sin `duelo`, abajo sale la `cifra` del bloque `portada` en grande (con `cifra_etiqueta` encima; puedes cambiar ambas en `portada2`). Usa `duelo` siempre que el vídeo compare dos cosas (precio antes/después, compra/venta, miedo/fomo, empresa A vs B).
- Las dos portadas deben contar el mismo gancho con palabras distintas (no copiar el titular de la 1 en la 2).
- Al entregar: enviar al usuario el vídeo, el zip **y las dos portadas** (SendUserFile), y decirle que elija la que más le guste.

## NOVEDADES v8: PERSONAS Y LOGOS EN LA PORTADA (obligatorio)
La portada muestra ahora **a los protagonistas del vídeo**: la foto de la persona de la que se habla y los logos de las criptomonedas, DEX, exchanges o empresas que salen en el vídeo.
- **Si el vídeo habla de una persona** (CZ, Saylor, Vitalik, Musk…): su foto va en la portada. Se busca en `img/personas/<nombre>.jpg|png|webp` (nombre en minúsculas con `_`, p. ej. `michael_saylor.jpg`).
  - ⚠️ **Si no está la foto, PEDÍRSELA AL USUARIO** (no inventarla, no generarla con IA, no descargar fotos de personas por tu cuenta). Pídela en cuanto sepas el tema del vídeo (al escribir el guion), así no se frena la entrega. `entrega.py` se para con `FALTA LA FOTO DE "..."` si no la encuentra: es la única excepción a la entrega sin preguntar.
  - Guarda la foto que te envíe en `img/personas/` y reutilízala en próximos vídeos.
  - Foto normal (JPG) → sale en **círculo con aro menta** y el nombre en una píldora. PNG **recortado sin fondo** → sale grande, de cuerpo/busto, con contorno luminoso (se detecta solo por la transparencia).
- **Logos** (criptomonedas, DEX, exchanges, empresas): en `img/logos/`. Si falta alguno, descárgalo con
  `python scripts/logos.py uniswap pepe hyperliquid` (CoinGecko para monedas y exchanges, DefiLlama para DEX/DeFi, Simple Icons para empresas; `--fuente cripto|dex|marca` para forzar una). **Revisa que el logo descargado sea el correcto**; si no, guarda uno bueno a mano con ese nombre.
- Composición automática: persona + hasta 4 logos orbitando alrededor · solo persona · 1 logo grande · 2 logos enfrentados con "VS" · 3-4 logos en fila. La tarjeta de cifra sigue funcionando igual.
- Bloque `portada` de `entrega.json` (además de lo de v7):
  ```json
  "persona": {"nombre": "CZ"},                       // busca img/personas/cz.*  ·  o {"foto": "img/personas/cz.png", "nombre": "CZ"}
  "logos": ["binance", {"archivo": "bitcoin", "color": "#F7931A"}],
  "union": "VS"                                      // solo con 2 logos y sin persona: "VS", "×" o "" (nada)
  ```
  Opcionales de `persona`: `mostrar_nombre` (texto de la píldora), `etiqueta_nombre: false` (sin píldora), `encuadre` (p. ej. `"50% 20%"` si la cara queda cortada en el círculo), `recorte: true|false` (forzar modo).
  Opcionales de cada logo: `color` (aro y brillo; en PNG se calcula solo, en SVG monocromo ponlo siempre con el color de la marca), `modo`: `moneda` (llena el círculo, por defecto en PNG), `insignia` (logo dentro de una moneda oscura, por defecto en SVG), `blanco` (moneda blanca, para logos oscuros) o `libre` (sin marco).
  Compatibilidad: si no pones `logos` pero sí `icono`, ese icono se usa como logo (portadas v7 siguen funcionando).
- **Fondos variados** (para que dos portadas seguidas no se parezcan): `"fondo": "globo" | "rayos" | "grafica" | "rejilla"`. El fondo se tiñe solo con el color del logo principal (o con `"tono": "#F7931A"`). Si no pones `fondo`, se elige uno según el `slug`. **No repitas el fondo de la portada anterior**: elígelo a mano según el tema (`grafica` para precios/subidas/caídas, `rayos` para noticias y revelaciones, `rejilla` para tecnología/IA/futuro, `globo` para economía global).
- Regla: **si en el vídeo sale una persona o un logo concreto, tiene que salir en la portada.** Elige los 1-3 más importantes (no más de 4 logos).

## (v7, SUSTITUIDO por v10) ESTILO DE PORTADA "PLANTILLA"
La portada de Reels (`portada.html`, la genera `scripts/entrega.py`) usa ahora el estilo "plantilla": fondo verde oscuro con **globo + red de puntos + velas**, cabecera con avatar y **4LPHA MARKETS** a la izquierda y la **etiqueta** (píldora) a la derecha, titular en **Montserrat Black Italic** (línea normal en blanco, la `*destacada*` enorme en degradado menta con brillo, las líneas posteriores como subtítulo más pequeño), **tarjeta con borde luminoso** con icono + etiqueta + nombre + **cifra** en pistacho, e **icono grande** (p. ej. Binance) sobre el globo. Todo dentro de la zona segura del perfil (y 240–1680). Ya no usa el fotograma del vídeo como fondo.
- Bloque `portada` de `entrega.json`: `titulo` (líneas; la `*palabra*` entre asteriscos = línea grande en menta; lo que vaya después = subtítulo), `etiqueta`, `cifra` (opcional → activa la tarjeta), `cifra_etiqueta` (texto pequeño sobre el nombre, p. ej. "FORTUNA"), `cifra_nombre` (p. ej. "BINANCE"), `icono` + `icono_color` (SVG de `/img`), `pie` (opcional). Sin `cifra` no hay tarjeta; sin `icono` no hay icono grande.
- Ejemplo de titular de 3 líneas: `["De McDonald's", "*a prisión*", "La historia de CZ"]`.
- Para volver a la portada antigua con fotograma de fondo: `"estilo": "clasico"` en `portada` (usa `portada_clasica.html` y `fotograma`).
- La red y las velas se generan con una semilla (el `slug`), así que cada vídeo tiene una portada distinta pero reproducible.

## NOVEDADES v6 (obligatorio)
1. **Menos efectos de sonido (la mitad que antes).** Un vídeo de 30 s lleva **~14-19 efectos en total**, no 40. Máx. 2-3 `ev()` por escena y **un solo sonido por golpe** (nada de `riser`+`impact`+`shutter` en el mismo instante). Sin ticks en los subtítulos. Además `sfx.py` recorta solo lo que sobre (ver "Sonidos").
2. **Números girando con sonidos DIFERENTES.** Cada contador tipo ruleta (`roll`) suena distinto: `sfx.py` rota 6 sonidos (ruleta, marcador digital, contador de madera, tragaperras con campanita, reloj de paletas y caja registradora). Nunca el mismo sonido en dos contadores del mismo vídeo; usa siempre `ev(..., 'roll', 1)` y la rotación es automática (hasta 6 contadores sin repetir).
3. **Momentos dibujados.** En cada vídeo, **1-2 imágenes aparecen DIBUJÁNDOSE** en pantalla (2-3 si dura 45 s), con las skills de dibujo (claude-drawing / anidoodle / handdraw) + `scripts/dibujo.py`. Ver sección "MOMENTOS DIBUJADOS".

## ⚠️ OBLIGATORIO: RENDER EN MÁXIMA CALIDAD
El vídeo SIEMPRE se renderiza y exporta en máxima calidad, sin atajos de velocidad:
- Fotogramas capturados en **PNG sin pérdida** (nunca JPEG).
- Vídeo **H.264 High, preset slow, CRF 12**, color BT.709, **1080×1920 a 30 fps**, sin reescalar.
- Audio **AAC 320 kbps, 48 kHz**, normalizado a −16 LUFS (pico −1 dBTP), `+faststart`.
- Lo hacen `scripts/render.js video` + `scripts/final.py`. No cambies esos ajustes para ir más rápido.

## Flujo
1. Investigar y escribir el guion (máx. 30 s; hasta 45 s si la voz lo pide). **Si el vídeo trata de una persona y no está su foto en `img/personas/`, pídesela al usuario ya** (para la portada); descarga también los logos que falten con `scripts/logos.py`.
2. Transcribir la voz (`asr_run.py`, Whisper small de sherpa-onnx) y quedarse con las tomas buenas (`prep4.py` → `tmp/voz_cut.wav` + `tmp/timeline.json`).
3. Adaptar escenas/iconos en `template.html` (usa el MOTOR DE DINAMISMO, ver abajo). **Planificar insertos con las SKILLS DE EDICIÓN** (ver abajo): decidir qué escenas llevan un gráfico Manim, una pizarra HandDraw, una ilustración claude-drawing o un timelapse anidoodle, y generarlos en `insertos/`. **Obligatorio: 1-2 MOMENTOS DIBUJADOS por vídeo** (sección propia más abajo). En esas escenas deja vacía la caja central (solo cabecera y subtítulos; como mucho 1 `ev()` suave).
4. `python scripts/build.py` → `index.html`. Revisar con `node scripts/render.js stills 1.5 4 8 ...` (PNG en /out).
5. `node scripts/render.js video 4` → `tmp/video.mp4` (máxima calidad, en paralelo). Si hay insertos: `python scripts/insertos.py` (lee `insertos.json`, los mete en `tmp/video.mp4` con la misma calidad; revisar con fotogramas).
6. `node scripts/render.js events` + `python scripts/sfx.py tmp/events.json tmp/sfx.wav <duración>` → efectos con los sonidos reales de `/sonidos`. Comprueba la línea `control de saturación: X pedidos -> Y se conservan`: Y debe quedar en ~14-19 para 30 s. Si X pasa de ~30, quita `ev()` del HTML en vez de confiar solo en el recorte.
7. `python scripts/final.py out/video_final.mp4` → mezcla voz + efectos (con ducking: los efectos bajan solos cuando habla la voz) y exporta.
8. **ENTREGA POST-RENDER (obligatoria y automática, ver abajo)**: `entrega.py --historial` → diseñar 2 portadas nuevas desde cero (v10) → escribir `entrega.json` → `python scripts/entrega.py` → enviar vídeo + zip + portadas.
Requisitos: Python 3 + numpy + Pillow, ffmpeg, Node + `npm i playwright-core` y Google Chrome. Para insertos Manim: `pip install manim`.

## SKILLS DE EDICIÓN (instaladas en Claude Code, en `~/.claude/skills/`)
Todas siguen `estilos/ESTILO_ALPHA.md` (formato, paleta, fuentes, movimiento). Su salida entra al vídeo como **inserto** con `scripts/insertos.py`; nunca sustituyen a la voz, los subtítulos ni la entrega automática.
Regla de uso: 1–3 insertos por vídeo, cada uno donde aporte más que una escena HTML (datos que crecen, un proceso, una idea abstracta), **y al menos 1 de ellos es un MOMENTO DIBUJADO**. El resto sigue con el motor de dinamismo.

## ⚠️ OBLIGATORIO: MOMENTOS DIBUJADOS (v6)
Para que el vídeo sea más dinámico, las imágenes no aparecen siempre "de golpe": en **1-2 momentos por vídeo** (2-3 en vídeos de 45 s) la imagen **se dibuja sola** delante del espectador (trazo a lápiz/tiza con la punta en verde menta → se rellena de color → zoom lento).
- **Dónde**: cuando la voz presenta al protagonista del vídeo (empresa, persona, activo, lugar) o una idea que se entiende mejor con un dibujo. Nunca en el gancho de los 2 primeros segundos ni en el cierre `s6`.
- **Duración**: 3-4,5 s cada uno, en la zona `escena` (900×900). No pongas dos seguidos.
- **Cómo** (elige según el caso):
  1. **claude-drawing con etapas (preferido)**: pide la ilustración del tema en un estilo que pegue (pizarra con tiza, plano técnico/blueprint, collage de periódico, cyberpunk, risografía, synthwave, lápiz…), 1080×1080, paleta ALPHA, y genera sus etapas con `--stages` → `python scripts/dibujo.py --etapas <carpeta_etapas> insertos/dibujo1.mp4 --dur 4`.
  2. **Cualquier imagen** (ilustración claude-drawing sin etapas, el avatar, un logo, una foto de producto/edificio): `python scripts/dibujo.py <imagen> insertos/dibujo1.mp4 --dur 4 [--estilo pizarra|papel] [--sin-color]` → se traza y se colorea sola.
  3. **anidoodle** (timelapse de un dibujo que se hace solo) o **handdraw-skill** (pizarra blanca) cuando haya que explicar un proceso paso a paso.
- Mételo con `insertos.py`: `{ "clip": "insertos/dibujo1.mp4", "t0": 9.2, "dur": 4, "zona": "escena", "fundido": 0.2 }`.
- Sonido: como mucho 1 efecto suave al empezar (`whoosh` .4) o ninguno; el dibujo ya da el ritmo.
- Sin caras de personas reales generadas con IA (sí el avatar del canal).

| skill | para qué en ALPHA MARKETS | cómo |
|---|---|---|
| **manim-composer** → **manimce-best-practices** | gráficos que crecen, ejes, comparativas, curvas de precio, fórmulas (interés compuesto, PER) | planifica con manim-composer; escribe la escena en `estilos/` con `from manim_alpha import *`; `manim -qh -t --media_dir tmp/manim estilos/<escena>.py <Clase>` → `.mov` con fondo transparente → `insertos/` con `"esquinas": 0`. Ejemplo: `estilos/manim_alpha.py` (EjemploAlpha). LaTeX/`MathTex` necesita MiKTeX (no instalado): usa `Text`. |
| **manimgl-best-practices** | solo si se pide ManimGL/3b1b expresamente | ManimGL no está instalado (`pip install manimgl`); preferir ManimCE. |
| **handdraw-skill** | pizarra blanca dibujándose: explicar un concepto o proceso paso a paso | parte de `estilos/handdraw_alpha/` (900×900, tarjeta con borde menta); `node ~/.claude/skills/handdraw-skill/scripts/handdraw.mjs render <project.json> --output insertos/<x>.mp4 --assets <assets>` → zona `escena`. Sin narración (la voz es la tuya). |
| **claude-drawing** | ilustración fija hecha con código (83 estilos): pizarra con tiza, plano técnico, collage de periódico, cyberpunk, risografía, synthwave… | pide 1080×1080 o 1080×1920, paleta ALPHA; PNG → inserto con `"zoom": true` (Ken Burns) o su versión por etapas como timelapse. ⚠️ Su SKILL.md pesa ~740 KB: leer solo la sección del estilo elegido (buscar con Grep), nunca entero. |
| **anidoodle** | timelapse de un dibujo que se hace solo, explicativos animados, logo que se dibuja, 32 estilos | `node ~/.claude/skills/anidoodle/engine/tools/scaffold.mjs tmp/ani --film <id> --format 1x1 --duration 4` → `npm install` → `node tools/render.mjs <id> --out <mp4>` → zona `escena` (`"ajuste": "cubrir"`). Su música/voz no se usa. |
| **motion** | collage retro de papel animado a partir de una imagen (IA: Nano Banana + Kling) | requiere los MCP *nanobanana* (clave Gemini propia) y *higgsfield* con generación de vídeo; **gasta créditos: preguntar siempre antes**. Sin logos ni caras reales (regla de la skill). |
| **motion-art-direction** | decidir el lenguaje de movimiento, ritmo y jerarquía del vídeo | consultar al planificar escenas (paso 3). |
| **animation-principles** | curvas de easing, rebotes, escalonados que se sienten naturales | al tocar `show()`, `spring()`, transiciones o insertos. |
| **beat-sync-editing** | ritmo de cortes, golpes al tiempo de la voz, speed ramps | al colocar cambios de escena, `ev()` e `imp()`. |
| **shot-composition** | encuadre, zonas seguras 9:16, punto focal | al maquetar escenas, la portada y los insertos. |
| **color-motion** | gradientes, transiciones de color, gestión de color BT.709 | si los colores de un inserto no casan o salen lavados. |
| **logo-animation** | intro/cierre con el logo 4LPHA MARKETS | escena final (`s6`) o un inserto de 1–2 s. |
| **motion-background** | fondos animados (mesh, aurora, partículas) | variantes de `#bg`/`#grid` en `template.html`. |
| **remotion-video** / **after-effects** | solo si se pide trabajar en Remotion o After Effects | referencia; la plantilla no los necesita. |
Scripts de apoyo de motion-design (contact sheet, probe de MP4) en `~/.claude/skills/motion-design-scripts/` (bash: en Windows usar ffprobe directamente).

## ⚠️ OBLIGATORIO: ENTREGA AUTOMÁTICA TRAS EL RENDER
En cuanto exista `out/video_final.mp4`, Claude hace estos pasos **sin que el usuario lo pida y sin preguntar**:
1. **Descripción SEO + hashtags**: escribir `entrega.json` (copiar `entrega_ejemplo.json` y adaptarlo al vídeo), basándose en el guion y la transcripción reales:
   - `titulo_seo`: 50-70 caracteres, palabra clave principal al principio (para YouTube Shorts / TikTok).
   - `descripcion`: resumen del vídeo, en español y con emojis moderados.
     · 1ª línea = gancho con la palabra clave principal y la cifra/dato más fuerte (máx. 125 caracteres, es lo que se ve antes de "más").
     · 2-3 párrafos cortos con los datos clave y palabras clave secundarias escritas de forma natural (nombres propios, empresas, activos, cifras).
     · Una pregunta para provocar comentarios.
     · CTA: "👉 Sígueme en @4lphamarkets para no perderte nada de los mercados financieros."
     · Última línea: "⚠️ Esto no es consejo financiero."
   - `hashtags`: 8-15, sin repetir, mezcla de amplios (#inversiones #finanzas #bolsa / #criptomonedas), de nicho (empresa, activo, tema) y de marca (#4lphamarkets).
   - `palabras_clave`: 5-8 búsquedas que haría la gente para encontrar el vídeo.
   - `portada.disenos` (**v10, obligatorio**): las 2 portadas diseñadas desde cero para este vídeo (ver NOVEDADES v10). El resto de campos de `portada` son opcionales (llegan al diseño como `window.D`):
   - (antiguo, solo con `"estilo": "v8"`) `portada`: `titulo` (2-4 líneas cortas, gancho distinto a la 1ª frase del vídeo; la línea clave entre `*asteriscos*` sale enorme en verde menta y lo que vaya después es subtítulo), `etiqueta` (la misma píldora roja del vídeo), `cifra` opcional (dato estrella) con `cifra_etiqueta` y `cifra_nombre`, `icono` opcional (nombre de un SVG de `/img`) + `icono_color`. `fotograma` solo se usa con `"estilo": "clasico"`. **v8: `persona` (foto de quien protagoniza el vídeo; si no la tienes, pídesela al usuario) y `logos` (cripto/DEX/empresas del vídeo), ver NOVEDADES v8.**
2. `python scripts/entrega.py` → genera en `out/entrega/`:
   - `<slug>_descripcion.txt` (bloc de notas limpio, v12: título, descripción y hashtags, sin rótulos ni palabras clave),
   - `<slug>_portada_1.jpg` y `<slug>_portada_2.jpg` (las dos portadas diseñadas desde cero para este vídeo, 1080×1920; el texto queda dentro del recorte 3:4 de la cuadrícula del perfil) y las anota en el historial,
   - `<slug>_video.mp4`,
   y el zip `out/<slug>_ALPHA_MARKETS.zip` con los tres. Si el script imprime `AVISO:`, corregir `entrega.json` y repetir.
3. Revisar la portada (abrir el JPG): texto legible, nada cortado, fondo con sentido, **la persona y los logos del vídeo se ven y son los correctos** (cara no cortada en el círculo). Si no, cambiar `titulo` / `encuadre` / `logos` y repetir.
4. **Enviar al usuario, sin que lo pida, el vídeo final + el zip + las 2 portadas** (SendUserFile con `out/video_final.mp4`, `out/<slug>_ALPHA_MARKETS.zip`, `out/entrega/<slug>_portada_1.jpg` y `_portada_2.jpg`), y pegar también en el chat el texto limpio (título, descripción y hashtags, sin rótulos). Si el usuario no puede descargar desde el chat, copiar esos archivos a su Escritorio.

## Sonidos (/sonidos, ver catalogo.json)
Librería propia recortada y normalizada. En el HTML se lanzan con `ev(escena, tiempo, 'tipo', ganancia)`. El sonido se alinea para "golpear" en ese instante (un riser termina justo ahí; un whoosh tiene su pico ahí). Las variantes se rotan solas para no repetir.
| tipo | cuándo usarlo |
|---|---|
| `trans` | cambio de escena (automático) |
| `whoosh` / `whoosh_in` | elementos que entran volando / anticipación justo antes de un golpe |
| `riser` / `riser_long` | subir tensión ANTES de un dato clave (ponlo en el mismo instante que el impacto) |
| `impact` (=`thud`) / `bass` | sellos, cifras grandes, revelaciones |
| `click` / `pop` / `beep` | aparición de tarjetas, botones, iconos, confirmaciones |
| `shutter` (=`clack`) | sellos de goma, capturas, "fotos" |
| `flash` | aparición de logos, fotos de personas |
| `coin` | dinero, ingresos, beneficios |
| `metal` (=`ding`) | final de un contador, golpes de acento |
| `shimmer` | brillo suave (hielo, oro, premios) |
| `tech` (=`glitch`) | hackeos, datos, IA, errores |
| `roll` | números girando (contadores ruleta). **Rota solo entre 6 sonidos distintos**: ruleta → digital → madera → tragaperras → flip-clock → caja registradora. Cada contador del vídeo suena diferente |
| `tick`, `drop`, `freeze` | sintetizados: tick (ya no se usa en subtítulos), caídas, congelar |
### Presupuesto de sonido (v6) — NO saturar
- **Total: ~14-19 efectos en un vídeo de 30 s** (aprox. 1 cada 2 s). Antes se ponían ~40: ahora la mitad.
- Máx. **2-3 `ev()` por escena**, incluida la transición automática.
- **Un solo sonido por golpe**: para un dato clave basta `impact` (o `bass`) + `imp()` visual; el `riser` solo en el dato más fuerte del vídeo (1 vez).
- No sonorizar cada tarjeta, icono o moneda: elige el elemento principal de la escena. Nada de bucles de `coin`/`click` por cada elemento.
- `sfx.py` lo vigila solo: quita los `tick`, funde sonidos a menos de 0,30 s (se queda el más importante), deja ≥0,45 s entre efectos y aplica el tope (mitad de lo pedido, máx. 1 cada 1,6 s). `--todos` desactiva el filtro (no usarlo salvo que el usuario lo pida); `--factor 0.4` recorta aún más.
Efectos siempre por debajo de la voz.

## MOTOR DE DINAMISMO v2 (template.html)
- `show(el,t,a,{dx,dy,s,r})`: entrada con rebote (overshoot), **desenfoque de movimiento** automático y **barrido de luz** en las `.card`.
- `spring(p)`: escala con muelle amortiguado para logos e iconos.
- `runOdo(cols,t,a)`: contadores tipo ruleta con motion blur en los dígitos.
- `imp(escena,t,fuerza,x,y,color)`: golpe de cámara + zoom punch + rotación + **aberración cromática** + **ráfaga de partículas y onda expansiva** en (x,y).
- Transiciones automáticas entre escenas que rotan (whip con skew, zoom, slide, spin) con destello y barrido de luz.
- Cámara viva: deriva suave continua y zoom lento por escena; suelo de rejilla en perspectiva en movimiento; viñeta.
- Subtítulos karaoke: la palabra que suena se agranda y brilla; palabras clave entre `*asteriscos*` en verde menta.
Reglas: algo debe moverse siempre en pantalla; un dato por golpe; cada escena entra con transición; nunca dejar una escena estática más de 1,5 s.

## Estilo
Negro/gris + verde menta #34F5B0 y pistacho #B6E36A, avatar y logo del canal, subtítulos en blanco y mayúsculas con **Montserrat Black (900) recta** y contorno negro, palabra clave en verde menta (resto: Montserrat Black Italic para titulares y Anton para cifras), contadores de estilo bolsa, logos de empresas y banderas animadas.
Cierre de voz fijo: "Sígueme para no perderte nada de los mercados financieros, esto es... ALPHA MARKETS!!"
Fuentes: todas de Google Fonts y libres para uso comercial (Montserrat, Anton e Inter con licencia OFL; Permanent Marker con Apache 2.0). Sonidos: asegúrate de tener licencia de uso de cada efecto.
