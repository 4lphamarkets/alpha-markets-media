# RUTINA DIARIA ALPHA MARKETS · noticias → historias de Instagram + 3 vídeos

Carpeta protegida (NO BORRAR). La ejecuta la tarea programada de las 08:30 (Europe/Madrid), a partir del sábado 21-11-2026.
Antonio no está delante: no se hacen preguntas; se decide, se hace y se explica al final. Si algo bloquea, se notifica y se sigue con lo demás.

## 0. Cuántas noticias
- Lunes a viernes: **10 noticias** (cripto y bolsa de EE. UU. mezcladas; lo más relevante e interesante del día).
- Sábado y domingo: **5 noticias**.
- Bolsa de EE. UU. cerrada (fin de semana o festivo): noticias de cripto y de empresas/macro de EE. UU. que sigan siendo noticia, sin inventar cotizaciones.
- «Buenas noticias» = buenas por interesantes, relevantes y bien contrastadas (no solo alcistas). Mezclar subidas, bajadas, regulación, adopción y empresas.

## 1. Buscar (08:30-09:00)
- Fuentes: Investing.com, CoinMarketCap, Cointelegraph, The Block, CoinDesk, Reuters, CNBC, y cualquier buscador/medio fiable (WebSearch y WebFetch; el shell no tiene internet).
- Noticias de las últimas 24-36 h. Cada cifra con **al menos una fuente fiable**; si dos fuentes difieren, usar la más primaria y decirlo en el pie. **Nunca inventar** cifras, citas ni fechas.
- Mirar `registro/` (últimos 3 días) para **no repetir** noticias ya publicadas, salvo que haya novedad clara.
- Elegir las N noticias y **ordenarlas**: nunca dos seguidas del mismo activo o tema (bitcoin, ETF, Anthropic…): intercalar. Las que dependen del precio de mercado van antes en el día.

## 2. Escribir las historias (JSON)
Formato: ver `historias/generador_noticias/ejemplo_20-11-2026.json` (lista de objetos). Campos:
- `slug` (`h01_tema`), `t1` (blanco, 1-2 palabras, MAYÚSCULAS), `t2` (verde cursiva, el golpe, corto), `sub` (línea bajo el titular, admite `<b>…</b>` en menta).
- `rows`: **exactamente 4 filas** `{ic: up|dn|sq|neu, n: nombre, s: subtítulo, p: valor, c: cambio, cc: v|r}`; `ic` up=verde, dn=rojo, neu=punto verde, sq=cuadrado rojo. Textos cortos y en MAYÚSCULAS; si una fila queda apretada, bajar `nfs`/`pfs`. Rojo solo para caídas/riesgo; verde para subidas.
- `block`: `{type: line|bars|text, title, ... , res}`. `line` = `pts:[[etiqueta,"texto",valor,color]…]`; `bars` = `items:[[etiqueta,valor,"texto",color]…]`; `text` = `big` (frase con `<span style='color:#34F5B0'>`), `fs`. `res` = frase final con `<b>` en menta.
- `pie`: «Fuentes: … · fecha». `logo`: ver abajo. La fecha de la cabecera es siempre la de HOY (edítala en el generador si cambia: busca `20 NOV 2026` y sustitúyela por la fecha del día en MAYÚSCULAS, p. ej. `21 NOV 2026`).
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
4. Horas: **una por hora empezando a las 10:00** (L-V: 10:00 a 19:00; S-D: 10:00 a 14:00). Si al terminar ya pasó una hora de esa lista, usar la siguiente hora libre; nunca fechas pasadas.
5. Comprobar con `getScheduledPosts` que están todas y que `media` ya apunta a `static.metricool.com`; entonces `git rm` de los JPG de `stories/`, commit y push. **Nunca tocar** `plantilla-historias/` ni `plantilla_alpha_markets/`.
6. Guardar `registro/AAAA-MM-DD.json` (títulos y temas publicados) en el repo y subirlo.

## 5. Los 3 vídeos (después de programar las historias)
1. De las noticias del día, elegir **las 3 más importantes** (impacto en el mercado, interés, novedad). Preferir temas que se cuenten con logos/banderas; si una noticia necesita foto de una persona y no está en `img/personas/`, descartarla y coger la siguiente (no se puede preguntar).
2. Para cada una, seguir **`FLUJO_DE_TRABAJO.md` y `LEEME.md`** de esta carpeta: guion de 40 s a 1:20 con gancho, datos, cierre fijo («Sígueme para no perderte nada de los mercados financieros, esto es... Alfa Markets!!») y aviso «esto no es consejo financiero» en la descripción.
3. **Audio ElevenLabs (gasto automático autorizado por Antonio el 20-11-2026)**: voz `43h7ymOnaaYdWr3dRbsS` («Jaime - Confident, Clear and Warm»), modelo `eleven_v4`, `generations_count: 1`, texto con `[en tono juguetón]` al principio, **una sola generación por vídeo y nunca reintentar** (un reintento cobra otra vez).
   - Guion de unos 1.100-1.300 caracteres (≈1.060 créditos, ≈0,19 $ por audio; ≈3.200 créditos/día con los 3).
   - Antes de generar: `account_get_usage`; si quedan menos de 4.000 créditos hasta el reinicio, **no generar** y notificar. Hacer `estimate_only` primero y no generar si supera 1.600 créditos.
4. Montar y entregar según el flujo (vídeo 1080×1920, 2 portadas, descripción). Slug: `AAAA-MM-DD-tema`.
5. **Entrega: carpeta en el ESCRITORIO** (`~/Desktop/<slug>/` con vídeo, 2 portadas y descripción): `SendUserFile` de los 4 archivos → `device_request_folder_access` sobre `~/Desktop` si no está conectado → `device_commit_files`. Si el ordenador no responde, reintentar una vez; si sigue sin responder, **no darlo por entregado** y notificar claramente «NO he podido dejar la carpeta en el Escritorio» (los archivos quedan enviados al chat).
6. Los vídeos **no se publican**: Antonio los revisa y los envía a la organización de vídeos.

## 6. Cierre
Resumen corto: historias programadas (hora y tema), los 3 vídeos elegidos y su estado, créditos ElevenLabs gastados, y cualquier fallo. Si se puede, enviar también una notificación push.
