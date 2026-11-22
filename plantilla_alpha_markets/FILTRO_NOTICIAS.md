# FILTRO DE NOTICIAS (v22) · subir solo lo que interesa y se comparte

Origen: análisis del 22-11-2026 de @h.analistasoficial (14,5 mil seguidores) y @lacartabursatil (29,8 mil). Muestra: 12 Reels recientes de cada uno; los de arriba dan 70-77 % de las vistas (1 solo Reel = 41-47 %). Hipótesis, no certezas.

## 1. Qué publican y qué funciona (muestra)
**Ganadores** (vistas · enviados/vistas aprox.):
- «Mañana jueves la bolsa se juega 3 cosas… y una no había pasado nunca» (Trump-Xi-Putin en la misma mesa, Walmart, salida a bolsa de Anthropic): **146 mil · 1,3 %**.
- «Nvidia cierra su peor semana desde 2008 · cae al Golden Pocket · −48 % del récord»: **194 mil · 1,3 %**.
- «Bitcoin: 3 ciclos alcistas, una sola línea (media móvil EMA 365)»: **86 mil · 1,9 %**.
- «En 2 horas, la bolsa puede caer 7 días seguidos (no pasa desde el covid)»: **61 mil · 1,2 %**.
- «Por primera vez, EE. UU., China y Rusia en la misma mesa»: 33 mil (LCB, 1,4 %). «Acción de Gracias: 64 de 76 años subió»: 33 mil · 1,0 %. «La bolsa se juega la semana en 3 días y ½»: 41 mil en 13 h.
**Flojos** (5-8 mil): Anthropic vs SpaceX tras su estreno (5,8 mil · 0,2 %), «Fibonacci · parte 1 de 10» (4,9 mil), «Quién te vende Bitcoin en lo más alto» (8,1 mil · 0,4 %), «somos un equipo de inversores…» (5,8 mil), «¿ha reventado la burbuja de IA?» (7,7 mil).

## 2. Lo que tienen en común los ganadores
1. **Reloj**: hay un momento concreto («mañana jueves», «en 2 horas», «cierre semanal», «lunes 15:30»).
2. **Rareza verificable**: «no pasa desde el covid», «peor semana desde 2008», «una no había pasado nunca», «Golden Pocket −48 %».
3. **Protagonista gigante o mercado entero**: Nvidia, Anthropic, Trump/Xi/Putin, Fed, S&P 500, Bitcoin.
4. **Un solo widget visual** que se entiende sin sonido (calendario, gráfico que se dibuja, cifra enorme).
5. **Útil para decidir/enviar a un amigo inversor** («¿qué pasa mañana?»): por eso se comparten (enviados/vistas ≥ 1 %).
6. Acaban en **pregunta abierta** y descripción larga con datos (35-172 comentarios en los grandes).
Lo flojo: temas atemporales/educativos sin gancho de hoy, autopromoción, comparaciones sin rareza histórica y análisis largos sin widget.
Aviso: la semana analizada fue de pánico (Nvidia −48 %, 7 caídas seguidas): parte del tirón es de ciclo de noticias; cuando el mercado se calme, los números bajarán para todos.

## 3. El filtro (puntuación 0-100) — `python scripts/filtro_noticias.py candidatas.json`
| Criterio | Puntos |
|---|---|
| Hora/día exacto en las próximas 48 h | +20 |
| Cifra histórica/rara verificable | +20 |
| Protagonista (conocido 8 / gigante 15) | +8 / +15 |
| Impacto en el bolsillo (indirecto 8 / «qué pasa mañana» 15) | +8 / +15 |
| Pregunta abierta (¿sube o cae?) | +10 |
| Se resume en 1 widget (calendario, gráfico, comparación, número) | +10 |
| Novedad (<24 h / <48 h) | +10 / +5 |
| Sin cifra concreta en la primera frase | −20 |
| Educativo atemporal sin gancho de hoy | −15 |
| Autopromoción / marca | −30 |
| Menos de 2 fuentes fiables | descartada |
**Decisión:** ≥ 70 → vídeo · 55-69 → historia o carrusel · < 55 → descartar. De los candidatos ≥ 60 se eligen los 2 vídeos del día con **máx. 1 por tema** (+ reglas de variedad de `RUTINA_DIARIA.md`). Si ninguno llega a 60, mejor 1 vídeo bueno que 2 flojos.
Un `patron_actual` (patrón histórico aplicado al precio de HOY, como la media móvil de Bitcoin) cuenta como noticia; un tema atemporal sin hoy no.

## 4. Qué NO subir
- Noticia sin 2 fuentes o con cifra que no podamos comprobar (rumores, «fecha límite» alarmista).
- Autopromo («quiénes somos»), series educativas largas, parte 2 de algo sin novedad.
- Mismo tema dos veces seguidas; el mismo activo en vídeo y en la historia de precios de las 21:30 sin aportar el porqué.
- Lo de las próximas horas se publica **antes** (el reloj es el gancho): un evento de las 20:00 se sube a mediodía, no a las 19:50.

## 5. Medir y recalibrar (cada viernes)
Por cada vídeo: puntuación del filtro, modo (analista/clásico), vistas 24 h, enviados/vistas, me gusta/vistas, seguidores ganados. Si un tema con ≥ 70 puntos queda por debajo de la mediana (1.047 el 20-11), se sube el peso del criterio que falló. El objetivo no es la media: es acertar los pocos Reels que dan el 70 % de las vistas.
