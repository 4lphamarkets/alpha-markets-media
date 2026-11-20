# Estilo ALPHA MARKETS para TODAS las skills
Lo que se genere con cualquier skill tiene que parecer hecho por la misma mano que `template.html`.
Pásale estos datos a la skill al pedirle algo (y revisa el resultado contra ellos).

## Formato
- Vídeo final: **1080×1920, 30 fps**, H.264 (lo pone la plantilla). Cada inserto se entrega a 30 fps.
- Inserto en la **zona de escena**: caja de **900×900** en x90 y330 (cabecera arriba y subtítulos abajo siguen visibles). Genera los clips en 900×900 (o 1080×1080) cuando vayan ahí.
- Inserto a **pantalla completa**: 1080×1920, y deja libres arriba 0–300 px y abajo 1400–1920 px si debe convivir con cabecera y subtítulos.
- Zona segura de Reels: nada importante en los 250 px de abajo ni en la franja derecha (botones de la app).
- Duración de un inserto: 2–6 s. Algo se mueve siempre; nunca más de 1,5 s quieto.

## Paleta
| token | hex | uso |
|---|---|---|
| fondo | `#040706` | fondo general (o transparente si el clip lo permite) |
| tinta | `#F4FFF9` | texto principal |
| gris | `#8FA39A` | texto secundario, ejes |
| menta | `#34F5B0` | acento principal, subidas, palabra clave |
| pistacho | `#B6E36A` | acento secundario, datos positivos |
| rojo | `#FF5A5F` | caídas, alertas, sellos |
| hielo | `#9FE4FF` | frío, congelado, datos neutros |
| oro | `#F0B90B` | dinero, monedas, Binance |
Regla: fondo oscuro + **un solo acento** fuerte por plano (menta salvo que el dato sea negativo → rojo).

## Tipografía (en `/fonts`; versiones .ttf para Manim y apps de escritorio en `/fonts/ttf`)
- Titulares: **Montserrat Black Italic** (`MontserratAlpha-BlackItalic.ttf`).
- Cifras: **Anton** (`Anton-Regular.ttf`), estilo bolsa, con contorno negro.
- Etiquetas: Montserrat ExtraBold. Texto de interfaz: Inter Bold.
- Firma/acento: Permanent Marker (solo "MARKETS").
- Subtítulos: los pone la plantilla (Montserrat Black 900, recta, mayúsculas, contorno negro, palabra clave en menta); no metas subtítulos dentro de los insertos.

## Movimiento (skill animation-principles)
- Entradas con rebote (ease-out-back / overshoot ~10 %), salidas rápidas (ease-in, 0,15–0,25 s).
- Escalonado de 60–120 ms entre elementos de una lista.
- Cada dato clave: subida de tensión + golpe (en la plantilla: `riser` + `impact` + `imp()`).
- Cortes y golpes alineados con la voz o con el beat (skill beat-sync-editing).

## Voz y audio
- La voz es siempre la del usuario (`tmp/voz_cut.wav`). Los insertos entran **sin audio**; los efectos los pone `sfx.py` con `ev()`.
- Si una skill necesita voz de prueba (HandDraw, anidoodle): Edge TTS `es-ES-AlvaroNeural`, nunca la voz china por defecto.

## Contenido
- Logos de empresas/criptos: los SVG de `/img` (la skill **motion** prohíbe logos en lo que genera con IA: respétalo ahí).
- Nada de caras de personas reales generadas con IA.

## Portada (v7)
Fondo `#040706`→verde oscuro con brillo menta, globo con red de puntos y velas (menta/rojo), tarjetas redondeadas (radio ~34 px) con borde menta luminoso y degradado verde muy oscuro. Titulares Montserrat Black Italic (blanco; línea clave en degradado menta con resplandor), cifra en pistacho con brillo, icono de marca grande con resplandor de su color (oro para Binance). Nada importante fuera de y 240–1680. Plantilla: `portada.html`.
