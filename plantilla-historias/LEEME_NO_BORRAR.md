# ⚠️ NO BORRAR · plantilla de historias ALPHA MARKETS

Esta carpeta es la plantilla que usan las rutinas diarias de Instagram (**Cripto hoy** y **Wall Street hoy**, 21:20 datos / 21:30 publicación, hora de Madrid).
Si desaparece, las dos rutinas fallan.

**Regla de Antonio:** al purgar o vaciar el repo se borra TODO menos las carpetas de plantillas:
`plantilla-historias/` y `plantilla_alpha_markets/`. Nunca se tocan.

Contenido: `build_story.py` (generador), `make_fondo.py` (regenera el fondo), `PROCEDIMIENTO.md` (pasos y scripts de lectura de datos), `assets/` (fondo, logo, oso, toro, iconos), `fonts/`.
Comprobación rápida: `python3 build_story.py --selftest`.
