# RUTINA DIARIA v27 — ALPHA MARKETS (desde el 26-11-2026)

> **v27 (26-11-2026, orden de Antonio):** (1) los vídeos se montan SIEMPRE con el **MODO DINÁMICO** (`ESTILO_DINAMICO.md`, `montar.py … dinamico`): animado todo el rato, stickers/monedas/imán/gráficas/ruletas que ilustran lo que se dice, y **en noticias de caída: pantalla roja + sirena + glitch (`crash`)**. El modo «analista» queda prohibido. (2) Las **portadas** de los vídeos usan los mismos 10 diseños (sin `foto_epica`; ver `ESTILO_DINAMICO.md` §Portadas). (3) Las historias de noticia usan `historias/estilos/make_story_estilos.py` con **10 diseños radicalmente distintos**: cada una distinta de la anterior (ver §3).

Una sola tarea programada ("RELOJ ALPHA MARKETS") se despierta cada hora en punto (Madrid) y ejecuta SOLO el hueco que toca según la tabla de abajo. Todo es autónomo: **se publica sin pedir permiso**. Si algo falla, se anota en el registro y se sigue con el siguiente hueco (nunca se publica algo roto o con datos antiguos).

Zona horaria: Europe/Madrid. Metricool: blogId 8199629. Instagram @4lphamarkets + YouTube.

## 0. Al despertar (siempre, ≤2 min)
1. Hora y día de la semana de Madrid: `TZ=Europe/Madrid date`. Si la hora no está en la tabla, no hay nada que hacer: termina.
2. Clonar el repo (`GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/4lphamarkets/alpha-markets-media`) y leer `registro/AAAA-MM-DD.json` de hoy (qué se ha hecho ya: noticias usadas, huecos hechos, vídeos). **Si el hueco ya consta como hecho, no repetirlo** (otra ejecución pudo adelantarse).
3. ¿Hoy hay bolsa de EEUU? Consultar la lista de festivos NYSE (sección 6). Si NO hay bolsa (festivo o fin de semana) → **modo 100 % cripto** (todas las noticias, historias y vídeos son de cripto; no se hace la historia de precios de Wall Street). Si hay bolsa → cripto + acciones EEUU.
4. Leer las reglas del canal: `LEEME.md`, `ESTILO_ANALISTA.md`, `FILTRO_NOTICIAS.md`, `FLUJO_DE_TRABAJO.md`, `PLAYBOOK_COMPETENCIA.md` (solo las que necesite el hueco).
5. **Nunca tocar** las carpetas `plantilla-historias` ni `plantilla_alpha_markets` (no borrarlas ni vaciarlas). Trabajar en carpetas nuevas y borrar solo los temporales propios.

## 1. Mapa de huecos — LUNES a VIERNES
| Hora (Madrid) | Qué hacer | Se publica a |
|---|---|---|
| 06:00 | Vídeo A (el más importante de la noche/mañana temprana) | 09:00 |
| 09:00 | Historia 1 (noticia fresca) **y después** Vídeo B | historia 09:30 · vídeo 12:00 |
| 10:00 | Historia 2 | 10:30 |
| 11:00 | Historia 3 (una de las dos de la mañana es la **gráfica BTC 15 MIN**, al azar) | 11:30 |
| 12:00 | Historia 4 | 12:30 |
| 13:00 | Historia 5 | 13:30 |
| 14:00 | Vídeo C (noticia de la apertura de Wall Street / mañana) | 15:30 |
| 15:00 | Historia 6 | 16:00 |
| 16:00 | Historia 7 **y después** Vídeo D | historia 17:00 · vídeo 18:30 |
| 17:00 | Historia 8 (una de las de la tarde es la **gráfica BTC 15 MIN**, al azar) | 18:00 |
| 18:00 | Historia 9 | 19:00 |
| 19:00 | Historia 10 | 20:00 |
| 21:00 | Historias de precios: leer precios ~21:20 y publicar **"Cripto hoy" a las 21:30** y **"Wall Street hoy" a las 21:31** | 21:30 / 21:31 |

Notas L-V:
- Si en un hueco de historia la mejor noticia es de última hora y crítica (hackeo grande, ETF, caída/subida >5 %, decisión de la SEC/Fed, quiebra, etc.), **priorizarla**: publicarla a +5 min en vez de la hora prevista, y la noticia que iba a tocar pasa al hueco siguiente si sigue vigente.
- Las historias del hueco 09:00…13:00 (mañana) y 15:00…19:00 (tarde): la tarde busca noticias que hayan pasado por la mañana o en la apertura de Wall Street, y **jamás repite** una noticia ya publicada (consultar el registro del día).
- Los vídeos A, B, C y D duran **máximo 40 s**, con las reglas y el **estilo dinámico** de la plantilla (`montar.py … dinamico`, `entrega.py`, `qa_video.py`): ilustrar con imagen/animación TODO lo que se nombra, nunca >3 s con la pantalla quieta, gráfica/ruleta si hay BTC/ETH/bolsa, `crash` si es una caída. Cada vídeo sale de una de las noticias ya vistas ese día (las más importantes).
- Entre semana también se puede añadir algún vídeo atemporal de la cola (carpeta de vídeos atemporales del Escritorio) si hay hueco y sin pasar de 5 vídeos al día; así se acaba la carpeta.

## 2. Mapa de huecos — SÁBADO y DOMINGO
| Hora (Madrid) | Qué hacer | Se publica a |
|---|---|---|
| 09:00 | Historia 1 | 10:00 |
| 11:00 | Vídeo nuevo del día (la noticia cripto más importante) | 12:00 |
| 13:00 | Historia 2 | 14:00 |
| 17:00 | Historia 3 | 18:00 |
| 21:00 | Leer precios ~21:40 y publicar historia **"Cripto hoy" a las 22:00** | 22:00 |
Además (ya están programados en Metricool, no hay que hacer nada salvo comprobar que han salido): vídeos atemporales de la cola a las 16:00 y 20:00. **Máximo 3 vídeos al día en fin de semana.**
Fin de semana = modo 100 % cripto. Si hay una noticia crítica, priorizarla igual.
Las horas de ejecución de fin de semana: el reloj se despierta cada hora, pero en fin de semana solo actúa en 09:00, 11:00, 13:00, 17:00 y 21:00; en el resto termina sin hacer nada.

## 3. Cómo se hace una HISTORIA de noticia (just-in-time) — v27: CADA UNA, UN DISEÑO RADICALMENTE DISTINTO
1. **Buscar la noticia más fresca** (últimos 30-60 min) justo antes: WebSearch (modo `extended` si lo normal sale flojo). Solo dos nichos: **cripto** y **acciones/índices de EEUU**. Relevantes, con atención real, verificadas en 2 fuentes si es posible. Descartar las ya publicadas hoy (registro) y las de más de 12 h (salvo que sigan siendo el tema del día).
2. Escribir el JSON de UNA historia (campos en la cabecera de `historias/estilos/make_story_estilos.py`: `t1`, `t2`, `sub`, `rows` 2-4 filas, `tag`, `fuente`) y generar la imagen 1080×1920:
   `python3 historias/estilos/make_story_estilos.py datos.json historia.png --hueco K` donde **K = nº de historia del día (1-10)**: el script elige el diseño de la lista `ORDEN` (alerta → periódico → terminal → stickers → gráfica → gigante → chat → cartel → lockscreen → versus), pensada para que **dos historias seguidas no se parezcan en nada** (oscuro/claro, serif/mono/display, texto/gráfica). Con `--estilo <nombre>` se fuerza uno (p. ej. `alerta` si es una noticia crítica de caída). **Prohibido repetir el mismo diseño en el mismo día** y prohibido el antiguo generador `make_stories.py` de tarjetas (todas iguales).
   Mirar la imagen (Read) antes de publicar: texto sin cortes, sin solapes, cifras correctas.
3. Subir la imagen al repo temporal con **nombre único** (`tmp/AAAA-MM-DD_HHMM_hN.png`, `git pull --rebase` antes del push; si hay conflicto, reintentar), programar en Metricool como STORY de Instagram con la URL `https://raw.githubusercontent.com/4lphamarkets/alpha-markets-media/main/tmp/...` a la hora de publicación; esperar a que Metricool copie el medio a `static.metricool.com`, y después `git rm` del temporal y push.
4. Si la hora de publicación ya ha pasado o faltan <3 min, publicar con la hora actual +3 min.
5. Anotar en `registro/AAAA-MM-DD.json` (añadir sin pisar: leer, fusionar, escribir): hueco, **estilo usado**, titular, fuentes, hora de publicación, id de Metricool.

## 4. Historia "BITCOIN 15 MIN" (una al azar por la mañana y otra por la tarde)
Es el hueco de historia normal, pero con gráfica en lugar de noticia. Elegir al azar (dado en el primer hueco del bloque) cuál de las historias de la mañana (09-13) y de la tarde (15-19) lo es; anotar la elección en el registro para que la ejecución siguiente no la repita.
1. Con el navegador integrado, abrir `https://coinmarketcap.com/` y ejecutar con `javascript_tool` el script de la sección 6 de `plantilla-historias/PROCEDIMIENTO.md` (devuelve `{capturado, pts}` con ~289 puntos de 5 min). Guardarlo como `/tmp/chart.json`.
2. `python3 plantilla-historias/btc15m_story.py /tmp/chart.json /tmp/btc15m.png HH:MM 6 [ref=HH:MM]` — compara el precio de una hora anterior (por defecto, hace 6 h; elegir una `ref` con sentido, p. ej. la hora de apertura de Wall Street 15:30 o las 09:00) con el de ahora.
3. Mirar la imagen y publicarla como una historia más (paso 3 de la sección 3). Si el script imprime `ERROR`, hacer una historia de noticia normal en su lugar.

## 5. Cómo se hace un VÍDEO
Seguir `FLUJO_DE_TRABAJO.md` con `montar.py … dinamico` / `entrega.py` / `qa_video.py` (plantilla v25, **modo dinámico**: leer `ESTILO_DINAMICO.md` antes de escribir el guion de montaje): guion ≤40 s con el estilo del analista, voz ElevenLabs Jaime (`43h7ymOnaaYdWr3dRbsS`, modelo `eleven_v4`).
- ElevenLabs: **una sola generación** por audio (`generations_count` 1), **nunca reintentar** (cada reintento cuesta créditos); ≈600 créditos por audio. Antes de generar comprobar `account_get_usage`: si quedan **<4.000 créditos no generar** (hacer en su lugar una historia más y anotar el motivo); pedir OK solo si el audio costaría >2.000 créditos.
- Subir el vídeo automáticamente (sin pedir permiso) a Metricool como REEL de Instagram + Short de YouTube a la hora de publicación indicada en la tabla.
- **Regla del dueño (26-11-2026): con CADA vídeo nuevo, enviar siempre al chat las 2 portadas (`SendUserFile` de `<slug>_portada_1.jpg` y `<slug>_portada_2.jpg`), esté o no accesible el Escritorio**, para que pueda cambiarla sin pedirla. Mandar también el vídeo y la descripción.
- Entregar la carpeta del vídeo en el Escritorio: `SendUserFile` + `device_commit_files` a `C:\Users\orden\Desktop\<slug>\` (carpeta por vídeo).
- Vídeos de la cola atemporal: no se generan; ya están programados en Metricool. Si se quiere usar uno entre semana, reprogramarlo con `updateScheduledPost` (necesita el `info` completo original; el `id` cambia, el `uuid` no).
- Dos vídeos del mismo día jamás deben ser de la misma noticia.

## 6. Historias de precios (cierre del día)
Generador: `plantilla-historias/build_story.py` (ver `plantilla-historias/PROCEDIMIENTO.md`).
- **Cripto hoy:** BTC, ETH, HYPE, SOL, BNB, LIT (Lighter) + Fear & Greed abajo del todo. Datos de coinmarketcap.com (navegador integrado).
- **Wall Street hoy:** S&P 500, Nasdaq, Anthropic (ANT), SpaceX (SPCX), Amazon, Google (GOOGL), Apple, Nvidia, Microsoft (MSFT). Datos de investing.com (navegador integrado). Sin Fear & Greed.
- L-V a las 21:00 se leen precios ~21:20 y se publican **Cripto hoy a las 21:30** y **Wall Street hoy a las 21:31** (seguidas). Wall Street solo si hay bolsa ese día.
- Sáb/Dom: solo **Cripto hoy a las 22:00**.
- Si los datos tienen >45 min o no cuadran, `build_story.py` falla: reintentar la lectura una vez; si sigue mal, no publicar ese precio y anotarlo.
- Festivos NYSE 2026 (cierre total): 26-11 (Thanksgiving), 25-12 (Navidad). Media sesión: 27-11 (cierra 19:00 Madrid) y 24-12 (cierra 19:00 Madrid). 2027: 1-1, 18-1, 15-2, 26-3 (Viernes Santo), 31-5, 18-6 (Juneteenth observado), 5-7 (Día de la Independencia observado), 6-9, 25-11, 24-12 (Navidad observada). En fecha dudosa, consultar `https://www.nyse.com/trade/hours-calendars` con WebSearch.
- Regla del dueño: **festivo en EEUU = 100 % cripto**; cuando la bolsa vuelve a abrir, se vuelve a cripto + acciones.

## 7. Concurrencia y seguridad
- Varias ejecuciones pueden coincidir (p. ej. 09:00 termina vídeo cuando llega 10:00): nombres de archivo únicos con fecha y hora, `git pull --rebase` antes de cada push, el registro se fusiona (nunca se sobrescribe a ciegas), y antes de empezar un hueco se comprueba en el registro que no está hecho.
- Si una ejecución empieza con >20 min de retraso sobre su hora, publica con la hora actual +3 min y lo anota.
- Si Metricool rechaza una publicación por cupo o error, anotarlo en el registro y avisar en el resumen final del día (21:xx).
- Nunca publicar noticias sin fecha clara, rumores sin verificar, consejos de inversión ni promesas de rentabilidad. Tono informativo; estilo según `ESTILO_ANALISTA.md`.
- No pedir permiso para publicar. Sí detenerse y anotar si se pide algo irreversible fuera de este flujo (compras, pagos, cambios de cuenta).

## 8. Registro diario (`registro/AAAA-MM-DD.json`)
Estructura mínima: `{"fecha": "...", "modo": "cripto+bolsa|cripto", "huecos": {"06:00": {"estado": "ok|error|omitido", "detalle": "..."}}, "noticias": [{"titular": "...", "hora_pub": "...", "tipo": "historia|video|btc15m"}], "btc15m": {"manana": "11:00", "tarde": "17:00"}}`. Hacer `git pull --rebase` antes y push después.

## 9. Resumen final
A las 21:00 L-V (tras publicar los precios) dejar al dueño un resumen de 5 líneas en el chat: qué salió bien, qué falló, créditos ElevenLabs restantes y cola Metricool de mañana.
