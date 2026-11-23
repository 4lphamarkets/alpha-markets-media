# RUTINA DIARIA ALPHA MARKETS · noticias → historias de Instagram + 3 vídeos

Carpeta protegida (NO BORRAR). La ejecuta la tarea programada de lunes a viernes a las **05:55 (Europe/Madrid)** (antes 08:30; cambiado el 23-11-2026). **Objetivo de Antonio: cuando se siente al ordenador a las 08:30, los 2 vídeos ya están hechos y en su Escritorio.** Cálculo del margen (23-11): arranque real hasta ~40 min tarde sobre la hora programada; noticias + 5 historias (mañana) ≈ 10 min; instalar el modelo de transcripción ≈ 5 min; cada vídeo de 40 s ≈ 20 min (guion, audio, transcripción, montaje, render, portadas, Escritorio) → ≈ 40 min; colchón para fallos ≈ 20 min. Total ≈ 2 h 15 min como máximo, normalmente ~1 h 30. Para que llegue al Escritorio, **el ordenador de Antonio debe estar encendido con la app de Claude abierta** a esa hora; si no responde, los archivos quedan en el chat y se notifica.
Antonio no está delante: no se hacen preguntas; se decide, se hace y se explica al final. Si algo bloquea, se notifica y se sigue con lo demás.

## 0. Cuántas noticias
- **DOS TANDAS AL DÍA (cambio de Antonio, 23-11-2026; vigente desde el martes 24-11):** las 10 historias diarias se dividen en **5 por la mañana + 5 por la tarde**, y cada tanda busca sus propias noticias en su momento del día (así la tarde recoge lo que ha pasado desde la mañana: solo lo MÁS relevante e importante y las noticias de última hora).
  - **Tanda de la MAÑANA** (la ejecuta la tarea de las 05:55, L-V): **5 noticias**, historias programadas **10:00, 11:00, 12:00, 13:00 y 14:00**.
  - **Tanda de la TARDE** (la ejecuta otra tarea programada a las **15:00**, L-V; ver sección 7): **5 noticias**, historias programadas **16:00, 17:00, 18:00, 19:00 y 20:00**. Termina antes de las historias fijas de las 21:30.
- Sábado y domingo: las tareas están pausadas (decisión de Antonio); si se reactivan, 5 noticias el día entero (10:00-14:00).
- Bolsa de EE. UU. cerrada (fin de semana o festivo): noticias de cripto y de empresas/macro de EE. UU. que sigan siendo noticia, sin inventar cotizaciones.
- «Buenas noticias» = buenas por interesantes, relevantes y bien contrastadas (no solo alcistas). Mezclar subidas, bajadas, regulación, adopción y empresas.

## 1. Buscar (en cada tanda: al empezar la tarea)
- Fuentes: Investing.com, CoinMarketCap, Cointelegraph, The Block, CoinDesk, Reuters, CNBC, y cualquier buscador/medio fiable (WebSearch y WebFetch; el shell no tiene internet).
- Noticias de las últimas 24-36 h. Cada cifra con **al menos una fuente fiable**; si dos fuentes difieren, usar la más primaria y decirlo en el pie. **Nunca inventar** cifras, citas ni fechas.
- Mirar `registro/` (últimos 3 días, y **la tanda de la mañana de hoy** si eres la tarde) para **no repetir** noticias ya publicadas, salvo que haya novedad clara.
- **Variedad (prioridad de Antonio):** no todo debe ser Bitcoin. Puede haber más de 2 de Bitcoin (incluidas las de ETF o empresas que compran BTC) **solo si van bien espaciadas**: al menos **2 horas libres entre dos de Bitcoin** (p. ej. 10:00, 13:00 y 19:00), nunca seguidas. Aun así, que Bitcoin no sea más de ~3 de las 10 del día (**máximo 1-2 por tanda**, y si la última de la mañana fue de Bitcoin, la primera de la tarde no); lo demás, variedad. El resto, repartido entre: Ethereum, altcoins (Solana, Hyperliquid, XRP, BNB…), DeFi/perps, stablecoins, regulación y países, bancos centrales/macro, bolsa de EE. UU. (índices, Nvidia, Tesla, Apple…), IA y empresas (Anthropic, OpenAI…), materias primas (oro, plata, petróleo). Si el día va muy sesgado a un tema, buscar activamente otros.
- **Complementar, no solapar, las historias fijas de las 21:30:** cada noche ya se publican «Cripto hoy» (precios BTC, HYPE, ETH, SOL, BNB, ZEC + Fear & Greed) y «Wall Street hoy» (S&P 500, Nasdaq, AAPL, AMZN, NVDA, INTC, AMD, ANT; solo L-V). Por tanto, **no hacer historias que sean solo un resumen de precios o variaciones de esos mismos activos**; sí noticias que expliquen el *porqué* o temas que esas historias no cubren. Si una noticia trata de uno de esos activos, debe aportar algo nuevo (dato, evento, causa), no solo el precio.
- Elegir las N noticias y **ordenarlas**: nunca dos seguidas del mismo activo o tema (bitcoin, ETF, Anthropic…): intercalar. Las que dependen del precio de mercado van antes en el día.

## 2. Escribir las historias (JSON)
Formato: ver `historias/generador_noticias/ejemplo_20-11-2026.json` (lista de objetos). Campos:
- `slug` (`h01_tema`), `t1` (blanco, 1-2 palabras, MAYÚSCULAS), `t2` (verde cursiva, el golpe, corto), `sub` (línea bajo el titular, admite `<b>…</b>` en menta).
- `rows`: **exactamente 4 filas** `{ic: up|dn|sq|neu, n: nombre, s: subtítulo, p: valor, c: cambio, cc: v|r}`; `ic` up=verde, dn=rojo, neu=punto verde, sq=cuadrado rojo. Textos cortos y en MAYÚSCULAS; si una fila queda apretada, bajar `nfs`/`pfs`. Rojo solo para caídas/riesgo; verde para subidas.
- `block`: `{type: line|bars|text, title, ... , res}`. `line` = `pts:[[etiqueta,"texto",valor,color]…]`; `bars` = `items:[[etiqueta,valor,"texto",color]…]`; `text` = `big` (frase con `<span style='color:#34F5B0'>`), `fs`. `res` = frase final con `<b>` en menta.
- `pie`: «Fuentes: … · fecha». `logo`: ver abajo. La fecha de la cabecera se pone sola (hoy, hora de Madrid).
- Datos exactos y con su unidad. Sin consejos de inversión; tono claro y fácil de entender.

### Logos (`logo`: texto o lista de máximo 2)
Si se habla de… → bitcoin `btc` · ethereum `eth` · Anthropic `ant` · Hyperliquid `hl` · Solana `icon:SOL` · BNB `icon:BNB` · S&P 500 `icon:SPX` · HYPE `icon:HYPE` · EE. UU. `🇺🇸` · China `🇨🇳` · Rusia `🇷🇺` · UE `🇪🇺` · Japón `🇯🇵` · ballena `🐋` · Fed/bancos `🏦` · SEC/justicia `⚖️` · Congreso/regulación `🏛️` · empresa cotizada `badge:NVDA` (ticker) · oro/plata y otros: emoji que encaje (🥇, 🥈). Con 2 logos se muestran más pequeños apilados (activo + país, por ejemplo `["btc","🇺🇸"]`).

## 3. Generar y revisar
```bash
cd /home/claude/alpha-markets-media/plantilla_alpha_markets/historias/generador_noticias
python3 make_stories.py /ruta/noticias.json /tmp/historias     # crea .png y .jpg 1080x1920
```
Mirar **todas** con `Read` (o una hoja de contacto): sin solapes, sin texto cortado, cifras y signos correctos. Corregir el JSON y regenerar si hace falta.

## 4. Programar en Instagram (Metricool, sin pedir OK)
1. `add_repo` con `access: push` de `4lphamarkets/alpha-markets-media`; clonar con `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1`.
2. Copiar los `.jpg` a `stories/AAAA-MM-DD-<slug>.jpg`, `git add`, commit y `git push origin main` (el aviso «push negotiation failed» es normal).
3. Por cada historia `createScheduledPost`: blogId `8199629`, red `instagram`, `instagramData.type = "STORY"`, `text` vacío, `media` = `https://raw.githubusercontent.com/4lphamarkets/alpha-markets-media/main/stories/<archivo>.jpg`, `autoPublish: true`, zona **Europe/Madrid**.
4. Horas: **una por hora**. Tanda de la mañana: 10:00, 11:00, 12:00, 13:00, 14:00. Tanda de la tarde: 16:00, 17:00, 18:00, 19:00, 20:00. Si al terminar ya pasó una hora de esa lista, usar la siguiente hora libre del hueco (nunca solapar con otra historia ni pasar de las 21:00); nunca fechas pasadas.
5. Comprobar con `getScheduledPosts` que están todas y que `media` ya apunta a `static.metricool.com`; entonces `git rm` de los JPG de `stories/`, commit y push. **Nunca tocar** `plantilla-historias/` ni `plantilla_alpha_markets/`.
6. Guardar el registro en el repo y subirlo: la tanda de la mañana en `registro/AAAA-MM-DD.json` y la de la tarde en `registro/AAAA-MM-DD-tarde.json` (títulos y temas publicados), para que cada tarea no pise lo de la otra.
7. **ENVIAR LAS HISTORIAS A ANTONIO PARA VERLAS (orden de Antonio, 23-11-2026):** al generarlas y revisarlas (paso 3), mandar los JPG con `SendUserFile` (`display: attach`, `status: proactive`, en orden de publicación, caption «Las 5 historias de la mañana (o de la tarde), solo para verlas») además de programarlas. **No se dejan en el Escritorio**: solo los vídeos van ahí. Guardar los JPG en una carpeta temporal (p. ej. `/tmp/historias`) hasta enviarlos, porque se borran de `stories/` tras comprobar Metricool.

## 5. VÍDEOS · ⏸ PAUSADOS desde el 23-11-2026 (orden de Antonio: no tiene créditos suficientes). NO producir vídeos, NO usar ElevenLabs/Higgsfield, NO entregar nada en el Escritorio. Reanudar solo cuando Antonio lo pida expresamente. (Lo siguiente queda como referencia.)

### (Referencia pausada) Los 2 vídeos (después de programar las historias) · ACTUALIZADO 22-11-2026: son 2, no 3 (créditos y no saturar el perfil; ya hay otros vídeos programados por otra automatización)
1. **Filtro v22 (`FILTRO_NOTICIAS.md`):** puntuar TODAS las noticias candidatas del día con `python scripts/filtro_noticias.py` (hora exacta, cifra histórica, protagonista, impacto, pregunta abierta, widget visual, novedad; menos de 2 fuentes = descartada). Elegir **como máximo 2 vídeos entre los de ≥ 60 puntos (mejor ≥ 70), máx. 1 por tema**; las de 55-69 van a historias; si solo 1 llega a 60, hacer solo ese (mejor pocos y buenos). Los eventos de las próximas horas se montan primero (el reloj es el gancho). Anotar en `registro/AAAA-MM-DD.json` la puntuación y el modo de cada vídeo.
   (Criterio base anterior: impacto en el mercado, interés y novedad.) Preferir temas que se cuenten con logos/banderas; si una noticia necesita foto de una persona y no está en `img/personas/`, descartarla y coger la siguiente (no se puede preguntar).
2. Para cada una, seguir **`FLUJO_DE_TRABAJO.md` y `LEEME.md`** de esta carpeta, aplicando **`PLAYBOOK_COMPETENCIA.md` (v18 + v22)**. **Estilo de montaje v22:** modo analista (`ESTILO_ANALISTA.md`: `prep_analista.py` → `build.py analista`) en 3 de cada 4 vídeos y modo clásico en 1 de cada 4 (control A/B 2 semanas); el vídeo nº 4, 8, 12… de la cuenta es el clásico. Además: entre las candidatas, primero eventos con hora exacta y noticias con cifra grande o personaje conocido; gancho con un número concreto en la primera frase (paradoja, pregunta o calendario); portadas `dos_cifras` o `cuenta_atras` cuando encajen; como máximo 2 formatos de prueba por semana, a criterio de la rutina: guion de 40 s a 1:20 con gancho, datos, cierre fijo («Sígueme para no perderte nada de los mercados financieros, esto es... Alfa Markets!!») y aviso «esto no es consejo financiero» en la descripción.
3. **Audio ElevenLabs (gasto automático autorizado por Antonio el 20-11-2026)**: voz `43h7ymOnaaYdWr3dRbsS` («Jaime - Confident, Clear and Warm»), modelo `eleven_v4`, `generations_count: 1`, texto con `[en tono juguetón]` al principio, **una sola generación por vídeo y nunca reintentar** (un reintento cobra otra vez).
   - **DURACIÓN MÁXIMA DE CADA VÍDEO: 40 s (orden de Antonio, 23-11-2026).** Guion de unos 600-680 caracteres (~100-110 palabras; ≈16 caracteres por segundo de audio: el de 1.200 caracteres del 23-11 duró 73 s). Comprobar con `ffprobe` que el audio dura ≤ 40 s; si se pasa, recortar el guion **antes** de montar. Con ese largo: ≈600 créditos (≈0,11 $) por audio, ≈1.200 créditos/día con los 2. Gancho con cifra + 2-3 datos + pregunta + cierre fijo, sin relleno. Un solo dato grande por escena, 3-4 escenas.
   - Antes de generar: `account_get_usage`; si quedan menos de 1.500 créditos hasta el reinicio, **no generar** y notificar. Hacer `estimate_only` primero y no generar si supera 900 créditos (señal de guion demasiado largo: recortarlo).
4. Montar y entregar según el flujo (vídeo 1080×1920, 2 portadas, descripción). Slug: `AAAA-MM-DD-tema`.
5. **Entrega: EL VÍDEO SE DEJA SIEMPRE EN EL ESCRITORIO (OBLIGATORIO, orden de Antonio del 23-11-2026).** Cada vídeo termina en `~/Desktop/<slug>/` con 4 archivos: vídeo, 2 portadas y descripción. No se da por entregado un vídeo que no esté ahí. Pasos:
   1. `SendUserFile` de los 4 archivos (cada uno devuelve un `file_uuid`).
   2. Las herramientas del ordenador son diferidas: cargarlas con `ToolSearch` (`select:mcp__remote-devices__get_device_info,mcp__remote-devices__device_request_folder_access,mcp__remote-devices__device_commit_files,mcp__remote-devices__device_bash`) **antes** de dar nada por imposible. El 23-11 no se cargaron a tiempo y la carpeta no se dejó: no repetir ese fallo.
   3. `get_device_info` → si `~/Desktop` no está en `connectedFolders`, `device_request_folder_access` sobre `~/Desktop` (una sola vez, razón: «Guardar la carpeta <slug> en tu Escritorio»).
   4. `device_commit_files` con los 4 `fileUuid` → `~/Desktop/<slug>/<slug>_video.mp4`, `_portada_1.jpg`, `_portada_2.jpg`, `_descripcion.txt`.
   5. Si falla, reintentar una vez; si sigue sin responder, **no darlo por entregado**: dejar los archivos en el chat y notificar claramente «NO he podido dejar la carpeta en el Escritorio» con el motivo. Los vídeos del día pendientes se entregan en la siguiente ejecución o cuando Antonio abra la sesión.
6. Los vídeos **no se publican**: Antonio los revisa y los envía a la organización de vídeos.
7. **HORAS DE SUBIDA DE LOS VÍDEOS (orden de Antonio, 23-11-2026): a las 10:00 y a las 18:00 (Europe/Madrid)**, un vídeo en cada hora (el 1.º a las 10:00, el 2.º a las 18:00). La rutina no los publica por su cuenta: quedan en el Escritorio para que Antonio los revise; cuando dé el OK, se programan en Metricool (blogId 8199629, Reel en Instagram y Short en YouTube) a esas horas, nunca en fechas pasadas (si ya pasó la hora, la siguiente de la lista). Anotar en la descripción de la entrega y en `registro/AAAA-MM-DD.json` la hora prevista de cada vídeo (`hora_subida`).

## 6. Cierre de la tanda de la mañana
Resumen corto: historias programadas (hora y tema), los 2 vídeos elegidos y su estado, créditos ElevenLabs gastados, y cualquier fallo. Si se puede, enviar también una notificación push.

## 7. TANDA DE LA TARDE (tarea programada a las 15:00, L-V) · desde el 24-11-2026
Tarea independiente de la de la mañana: **solo historias, sin vídeos, sin ElevenLabs y sin Escritorio** (no necesita el ordenador de Antonio).
1. `add_repo` (push) del repo, un solo clon superficial, `register_repo_root`. Leer esta rutina (secciones 0-4) y seguirla sin preguntar.
2. Buscar **5 noticias nuevas** (cripto y bolsa de EE. UU., lo ocurrido desde la mañana: apertura de Wall Street a las 15:30, datos macro, movimientos de cripto, anuncios de empresas). Leer antes `registro/AAAA-MM-DD.json` (la mañana de hoy) y los 3 días anteriores para **no repetir nada** y mantener la variedad (Bitcoin como máximo 1-2 en la tarde).
3. Generar las 5 historias (secciones 2 y 3), programarlas a las **16:00, 17:00, 18:00, 19:00 y 20:00** (sección 4) y guardar `registro/AAAA-MM-DD-tarde.json`. Si son más de las 16:00 cuando termina, usar las siguientes horas libres hasta las 20:00 y, si no caben las 5, programar las que quepan y avisar.
4. Enviar a Antonio los 5 JPG con `SendUserFile` (solo para verlos) y cerrar con 2-3 líneas y notificación push. No tocar las tareas de las 21:30 ni las carpetas de plantillas.
