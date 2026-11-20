# Catálogo de conceptos de portada (v10)

Esto es **inspiración, no plantillas**. Para cada vídeo se diseñan DOS portadas nuevas desde cero, en HTML propio.
Elige (o inventa) dos conceptos que encajen con la historia del vídeo y que **no estén en el historial**
(`python scripts/entrega.py --historial`). Puedes inventar arquetipos nuevos: ponles un nombre corto en `arquetipo`.

**Prohibido** (ya se usaron demasiado en v8-v9): `plantilla_v8` (globo + titular Montserrat menta + tarjeta de cifra + moneda grande)
e `impacto_v8` (pantalla partida por grieta + sello rojo + duelo de cifras). Tampoco vale "la misma estructura con otro color".

| arquetipo | idea | encaja con |
|---|---|---|
| `foto_epica` | ⭐ **ESTILO FIJO (favorito del usuario, v11).** Miniatura de noticia de impacto: 1-3 protagonistas (personas y/o logos de activos en monedas gigantes) con brillo sobre globo verde con mapa de puntos y velas, **frase con punch** (blanco + palabra clave menta tipo pincel), píldora «fecha · sede» y skyline; banderas solo si son países. La referencia con 3 líderes es solo un ejemplo del estilo. Plantilla: `portadas/estilos/foto_epica.html` | cualquier noticia con protagonistas: personas, 2 activos enfrentados, cumbres, caídas, declaraciones |
| `dos_cifras` | 🆕 **v18.** Tarjetas enmarcadas con dos cifras enfrentadas (antes/después, cuánto/cuánto) sobre fondo oscuro, logo de la empresa arriba y **titular en pregunta** debajo (≤ 6 palabras). Distinto de `impacto_v8`: sin grieta ni sello rojo | resultados, valoraciones, comparativas (p. ej. «¿Cuánto ganan X e Y con Z?») |
| `cuenta_atras` | 🆕 **v18.** Portada de evento: la **hora o la fecha** es el elemento más grande (bloque amarillo/menta), nombre del activo o empresa en grande y un «esta semana»/«hoy» pequeño | resultados, Fed, salidas a bolsa, datos macro con hora |
| `periodico` | portada de periódico financiero: cabecera de diario con la marca, titular serif enorme, foto en semitono, columnas | noticias, entradas de instituciones, hitos |
| `terminal` | pantalla tipo terminal de bolsa: texto mono ámbar/verde, tabla de datos, una fila resaltada | 13F, accionistas, datos, flujos |
| `documento_filtrado` | documento oficial/SEC/clasificado con tachones negros, sello y subrayado a rotulador | revelaciones, regulación, filtraciones |
| `notificacion` | pantalla de bloqueo de móvil con una notificación gigante (banco, exchange, app) | alertas, liquidaciones, compras |
| `tuit` | publicación de red social enorme, con la persona como autor | declaraciones de una persona |
| `revista_persona` | portada de revista: persona recortada a sangre, nombre de cabecera detrás de su cabeza | perfiles (CZ, Saylor, Musk) |
| `cartel_combate` | póster de pelea de boxeo: dos rivales enfrentados, fecha, "VS" | A contra B, compradores vs vendedores |
| `marcador` | marcador deportivo / tablero de aeropuerto con letras split-flap | rankings, precio antes/después |
| `ticket` | recibo / ticket de compra larguísimo con el total subrayado | compras de empresas, gasto, comisiones |
| `billete` | billete o cheque gigante con la cifra y la cara/logo grabado | dinero, valoraciones, fortunas |
| `se_busca` | cartel de "SE BUSCA" del oeste, papel viejo, recompensa | hackeos, fraudes, huidas |
| `grafica_gigante` | una sola vela/línea enorme que rompe el marco y el texto se apoya en ella | subidas y caídas fuertes |
| `tipografia_total` | solo tipografía: 1-3 palabras a sangre que llenan la pantalla, logo pequeño | ganchos muy cortos |
| `minimal_blanco` | fondo blanco/claro, mucho aire, un objeto y una frase | contraste con el feed oscuro |
| `polaroid` | fotos instantáneas pegadas con cinta y notas a mano | historias, cronologías |
| `pizarra` | pizarra de tiza con flechas, círculos y cálculos | explicaciones, conceptos |
| `blueprint` | plano técnico azul con cotas y piezas del protocolo | tecnología, cómo funciona algo |
| `semaforo_alerta` | señal de peligro / cinta policial / luces de alerta | riesgos, avisos, caídas |
| `lupa` | lupa enorme ampliando un detalle (una línea de un informe, una cifra) | "nadie lo ha visto", letra pequeña |
| `podio` | podio 1-2-3 con logos o personas | comparativas, rankings |
| `mapa` | mapa con chinchetas y líneas de conexión | países, regulación, expansión |
| `ajedrez` | tablero con piezas = empresas/personas, jugada maestra | estrategia, movimientos institucionales |
| `cohete_espacio` | cohete/luna, estrellas, órbita | subidas, "to the moon", máximos |
| `pantalla_partida_vertical` | arriba/abajo (no izquierda/derecha) antes vs después | evoluciones, cambios de tendencia |
| `cromo` | carta coleccionable / cromo con estadísticas del protagonista | perfiles de monedas o personas |
| `chat` | conversación de WhatsApp/Telegram con el dato bomba | rumores, filtraciones, "me dijeron" |

> **foto_epica es la excepción a la regla anti-repetición:** se puede usar en TODOS los vídeos con protagonistas (una de las dos portadas); `entrega.py` no la bloquea ni la compara con anteriores. La otra portada sigue siendo un concepto nuevo y distinto.

## Lo que debe cambiar entre las dos portadas de un vídeo (y respecto a las anteriores)
- **Composición**: dónde va el titular, dónde el protagonista, cómo se lee la imagen.
- **Tipografía protagonista**: Mont, Anton, Marker, Inter, serif (Georgia), mono (Consolas) o bloque (Impact).
- **Paleta dominante**: no todo es negro + menta. Vale papel crema, blanco, rojo alerta, ámbar, azul plano...
  El verde menta puede quedarse como acento de marca.
- **Fondo / mundo visual**: el "objeto" que es la portada (periódico, móvil, ticket, terminal...).

## Lo que NO cambia (reglas fijas)
- 1080×1920, JPG. Todo lo importante dentro de **y = 240…1680** (recorte 3:4 de la cuadrícula del perfil).
- La **marca 4LPHA MARKETS** sale en algún sitio (`marca()` del kit, con la forma que pegue al concepto).
- Salen **los protagonistas reales**: foto de la persona (pedírsela al usuario si falta, nunca generarla) y **logos reales**
  de `img/logos/` (descargados con `scripts/logos.py`). Nunca un logo inventado (p. ej. un círculo con "HYPE" escrito):
  si una marca no tiene logo descargable, escribe su nombre como texto/wordmark.
- Titular legible en miniatura: la idea principal en ≤ 6 palabras grandes.
- Solo datos que salgan en el guion/descr. del vídeo. Nada inventado.
