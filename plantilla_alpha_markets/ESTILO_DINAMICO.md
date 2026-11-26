# MODO DINÁMICO (v25, 26-11-2026) · el estilo de «bitcoin_miedo_extremo_video» — ES EL ESTILO POR DEFECTO

Antonio (26-11-2026): los 3 últimos vídeos del modo «analista» eran aburridos (texto que avanza y pantalla quieta). Se vuelve al estilo del vídeo
`bitcoin_miedo_extremo_video` y se amplía: **dinámico y animado TODO el rato**. El modo `analista` queda archivado (no usar).

## Qué lleva SIEMPRE cada vídeo
- Cabecera: avatar redondo + logo de letras (izquierda) y píldora roja con el tema («MIEDO EXTREMO», «H.R. 8957»…) a la derecha (`tag`/`tagTone` g|y).
- Fondo vivo: degradado verde-negro, rejilla en movimiento, velas japonesas de fondo, partículas, cámara con zoom suave continuo.
- Subtítulos del vídeo de referencia: palabra a palabra, Montserrat Black MAYÚSCULAS, blancas + palabras clave en verde (`*así*`), rojo (`#así#`) o dorado (`^así^`), con blur/pop al entrar, abajo (y≈1450-1560).
- Entre escenas: barrido de luz diagonal + transición (whip/zoom/slide/spin) + sonido.
- **Una pieza visual NUEVA cada 2-3 s** (nunca más de 3 s con la pantalla quieta) y **cada cosa que se nombra se ve**:
  habla de BTC → moneda BTC girando / lluvia de monedas BTC / gráfica; ETH → moneda ETH; dólares → lluvia de monedas `usd`; imán → `magnet`
  (imán rojo que atrae monedas, campo pulsante); reloj/plazo → `icon clock`; ley/documento → `icon doc`; banco/Fed → `icon bank`; prohibido/bloqueo → `icon lock`;
  petróleo → `icon oil`; oro → `icon gold`; alerta → `icon siren|warning`; pregunta → `icon question`; cohete/subida → `icon rocket|up`; bajada → `icon down`; fuego/bomba/calavera para pánico.
- Sellos que golpean la pantalla (`stamp`: «COLAPSO FTX», «20 AÑOS»), cifras con ruleta (`odo`), gauge de miedo/codicia, velas que suben/bajan, gráficas que se dibujan.
- Sonido: ~1 efecto cada 0,9 s (el filtro de sfx.py se relaja con `--cada 0.85 --hueco 0.3` en modo dinámico); `montar.py` lo hace solo.

## Efectos de pantalla (`fx` en la escena con `at`, o globales con `at` absoluto)
| type | parámetros | efecto |
|---|---|---|
| `crash` | `dur`, `text` («ALERTA», «CRASH») | **PSICOSIS**: pantalla roja pulsante, sirenas laterales, bandas de peligro, líneas de escáner, texto gigante parpadeante, glitch RGB, sacudida fuerte, riser+impact+bass+beeps. **Úsalo en CUALQUIER caída fuerte, liquidación, hackeo, quiebra.** |
| `pump` | `dur` | subida: flash verde + rayos dorados/verdes giratorios (+ lluvia de monedas con `rain`) |
| `flash` | `color`, `a` | destello de pantalla |
| `shake` | `dur`, `amp` | sacudida |
| `zoom` | `dur`, `amt` | golpe de zoom |
| `glitch` | `dur` | división RGB |
Escena con `"mood":"red"` = viñeta roja latiendo (noticia mala); `"green"` = viñeta verde; `"gold"` = fondo dorado.
**Regla:** noticia de caída/crash → `mood:"red"` + `crash` en la frase clave + `candles trend:"crash"` + moneda/lluvia cayendo. Noticia alcista → `pump` + `candles trend:"pump"` + `rain dir:"up"`.
**Si hay BTC, ETH o bolsa: SIEMPRE una gráfica (`candles`) y/o ruleta de números (`odo`) en alguna escena.**

## Componentes (`comps` de cada escena; todos admiten `at` (s desde el inicio de la escena), `x`,`y` (centro x / arriba y), `w`, `enter`, `ed`, `until`)
`enter`: pop · up · down (cae y rebota) · left · right · zoom · slam (golpe) · spin · none. `until` = segundo en que desaparece.
| type | campos |
|---|---|
| `coin` | `sym` btc/eth/usd/sol, `size`, `mode` spin · float · beat · **paint** (BTC dibujado a trazo y luego relleno) |
| `rain` | `sym` («btc,eth»), `n`, `dir` down/up, `spread`, `floor`, `bounce` — lluvia de monedas a pantalla completa |
| `magnet` | `sym`, `n`, `h` — imán que atrae monedas |
| `icon` | `name`: magnet siren rocket fire skull bomb shield lock clock scales warning up down bank oil gold bolt eye doc boom money trophy question · `size`, `anim` wiggle pulse shake bob spin rise drop |
| `candles` | `trend` up pump down crash chop dip, `style` candles/line/area, `title`, `price0`,`price1`, `n`, `dur`, `h`, `w`, `big` (cifra gigante final) |
| `gauge` | `from`,`to`,`label` (miedo y codicia) |
| `odo` | `value` («306.795»), `prefix`, `suffix`, `size`, `color`, `label`, `dur` — ruleta que gira (suena a ruleta) |
| `stamp` | `text`, `tone` red/green/gold/white, `size`, `rot` — sello que golpea |
| `headline` | `text`, `size` — palabras que se estrellan una a una |
| `card` · `stat` · `pill` | texto con tarjeta / dato raro / píldora |
| `vs` | `a`,`b`:{label,value,sub,tone} — dos cifras enfrentadas |
| `bars` · `dots` | barras que crecen · puntos que se llenan («26 lecturas») |
| `ticker` | `text`, `tone` — cinta roja/verde que corre («ÚLTIMA HORA») |
| `logo` | `src`, `size` — logo de empresa |
| `follow` · `disc` | tarjeta de seguir + «no es consejo financiero» (escena final) |

## Cómo se monta
1. Audio de Jaime → `python scripts/transcribir.py tmp/voz.mp3` (tiempos).
2. `tmp/guion_dinamico.json` (ver cabecera de `scripts/prep_dinamico.py`; ejemplo: `guion_dinamico_ejemplo.json`). Los números en el JSON van como `0.5` (no `.5`).
3. `python scripts/montar.py revisar dinamico tmp/guion_dinamico.json` → mirar `out/hoja_contacto.jpg` (¿hay huecos de más de 3 s sin pieza nueva? ¿algo tapa los subtítulos?).
4. `python scripts/montar.py video dinamico tmp/guion_dinamico.json` (añade `--max 45` si el audio ya está hecho y pasa de 40 s).
5. `entrega.py` como siempre (2 portadas, descripción) y publicación según `RUTINA_DIARIA.md`.
Zona de piezas: y 330-1350; subtítulos y≈1450-1560; cabecera y≈196-290. Render ≈ 4-6 min.

## Portadas (v28) — los mismos 10 diseños que las historias
La portada «foto_epica» (globo verde + moneda + titular) está **retirada** (pasada de moda). Cada vídeo lleva 2 portadas con **dos diseños radicalmente distintos** entre sí y distintos de los de los últimos 4 vídeos (el historial lo controla solo).
En `entrega.json`, sin `portada.disenos`:
```json
"portada": {"t1":"BITCOIN","t2":"7.000M $ EN JUEGO","tag":"MAÑANA 09:00","sub":"Vencen <b>opciones</b> por 7.000M$",
            "rows":[{"n":"PUT/CALL","s":"HOY","p":"0,89","c":"","cc":"r"},{"n":"OCTUBRE","s":"ANTES","p":"0,55","c":"","cc":"v"}],
            "dir":"down", "estilos":["gigante","periodico"]}   // dir y estilos opcionales; máx. 2 filas; titular corto (la portada es una miniatura)
```
Estilos: alerta · gigante · terminal · periodico · chat · cartel · grafica · stickers · versus · lockscreen. Con `cc:"r"` salen en rojo, con `cc:"v"` en verde; `dir:"down"` pone la gráfica bajista. Elegir a mano `estilos` cuando la noticia lo pida (crash → `alerta`; cifra única → `gigante`; dos cifras → `versus`; ley/política → `periodico`). Mirar siempre las 2 portadas (Read) antes de entregar.
Las portadas con HTML propio (`portada.disenos`) siguen funcionando, pero no se usan salvo petición expresa.


## v29 (26-11-2026): historias y portadas con IMAGEN y 14 diseños
Antonio: «las historias siguen siendo iguales todas». Los 10 diseños cambiaban de maqueta pero eran solo texto sobre color. Ahora:
- Cada historia/portada lleva **pegatinas SVG grandes que ilustran la noticia** (`icono` en el JSON: bank, doc, lock, bomb, skull, siren, warning, rocket, up, down, shield, magnet, clock, scales, money, oil, gold, bolt, eye, trophy, question, fire, boom; y `logo` btc/eth/sol = moneda). En portadas: `portada.iconos` (lista) y `portada.logo` en `entrega.json`.
- 4 diseños nuevos centrados en la imagen: **poster** (icono gigante con rayos), **tweet** (publicación de X con el icono como foto), **ticket** (recibo con sello) y **tv** (informativo con rótulo y cinta). Total 14: alerta, gigante, terminal, periodico, chat, cartel, grafica, stickers, versus, lockscreen, poster, tweet, ticket, tv.
- `ORDEN` alterna familias (oscuro/claro, texto/imagen/gráfica) para que dos seguidas no se parezcan. Con `"sin_icono": true` se desactivan las pegatinas en los 10 diseños clásicos.
