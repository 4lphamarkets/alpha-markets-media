# MODO ANALISTA (v22) · cómo editar como @h.analistasoficial y @lacartabursatil

Origen: análisis del 22-11-2026 de los dos perfiles (informe completo con datos en el doc «Análisis H.Analistas y La Carta Bursátil»). Lo que sigue es lo que cambia en la edición.
Las causas son hipótesis (Instagram no da tiempo de visionado ni retención de cuentas ajenas); se validan con nuestras propias métricas.

## 1. Qué hacen ellos → qué cambia en la plantilla
| Observado en sus Reels | Cambio en el modo analista |
|---|---|
| **Un elemento nuevo cada vez**, apilado: píldora con hora/fecha → titular en tarjeta → widget (calendario, gráfico) → dato en píldora roja/dorada. Nada se mueve sin motivo. | Escena = columna centrada; cada pieza entra por turnos (`at`/`chunk`), fundido + subida corta. Sin sacudidas, partículas, rejilla ni aberración. |
| **El gancho es una hora o una cifra rara** («EN 2 HORAS · cierra Wall Street», «Le basta caer 0,2 %», «7 seguidos: no pasa desde el covid»). | Cada vídeo abre con píldora `pill` (hora/fecha/serie) + `card` con la cifra, y cierra la escena con un `stat` rojo/dorado con la rareza. |
| **Widgets de infografía** (calendario de días en verde/rojo, números enfrentados). | Componentes `calendar`, `vs`, `num`, `bars`. |
| **Gráficos que se dibujan** (velas que caen, franja «Golden Pocket», línea con 3 hitos) y una cifra gigante (-48 %). | Componentes `candles` (con `zone` y `big`) y `line` (con `marks`). |
| **Marca pequeña** en la esquina + kicker de 2-3 palabras («NVIDIA · CIERRE SEMANAL»). | Cabecera discreta: kicker a la izquierda (`kicker` de la escena) y logo de letras pequeño a la derecha. |
| **Fondo oscuro sobrio**, a veces foto del tema desenfocada. | Degradado verde-negro + `bg` opcional (foto del tema borrosa y oscurecida). |
| **Series** («PARTE 1», «PARTE 2») y mismo formato siempre → reconocibles. | Componente `tag` + misma estructura en todos los vídeos. |
| Texto en pantalla pequeño y contenido; el protagonista es el dato. | Subtítulos más pequeños (50 px), una frase cada vez, sin karaoke ni zoom. **Se mantienen tus reglas**: mayúsculas, blancos, Montserrat Black. |

## 2. Anatomía de un Reel (5-6 escenas, un solo mensaje)
1. **Escena 1 (0-8 s) · gancho**: `pill` (hora/fecha) → `card` con la cifra → widget (`calendar`, `vs` o `num`) → `stat` con la rareza. Es la escena que se comparte.
2. **Escena 2-3 · la prueba**: `candles` o `line` (el gráfico se dibuja mientras se habla) + `card` oscura con una frase corta + `stat`.
3. **Escena 4 · contexto histórico**: `bars` o `num` («desde 1950, 36 de 46 veces...»).
4. **Escena 5 · pregunta abierta** («¿el jueves sube o cae? 👇»): invita a comentar.
5. **Escena final**: `follow` (tarjeta @4lphamarkets con botón Seguir) + `disc` («esto no es consejo financiero»).
Reglas: **un solo dato grande por escena**; máx. 3 piezas visibles a la vez; 4-6 escenas; la duración la sigue marcando el flujo (40 s – 1:20) salvo que el usuario pida otra. Nuestro cierre fijo de cripto se mantiene en el guion.

## 3. Cómo se monta (con el flujo de siempre)
1. Audio de Jaime → transcribir (`asr_run.py`) como siempre.
2. Escribir `tmp/guion_analista.json` (ver cabecera de `scripts/prep_analista.py`): escenas con `a` (segundo de inicio), `kicker`, `segs` (subtítulos por frase con `*clave*`) y `comps`.
3. `python scripts/prep_analista.py tmp/guion_analista.json` → `tmp/timeline.json` (+ `tmp/voz_cut.wav`).
4. `python scripts/build.py analista` → `index.html`.
5. `node scripts/render.js stills 2 8 14 …` y **mirar los fotogramas** (nada tapado, nada fuera de y = 240…1680).
6. `node scripts/render.js events` → `sfx.py` → `final.py` → `entrega.py`, igual que el modo clásico.
Ejemplo completo: `timeline_ejemplo_analista.json` (cópialo a `tmp/timeline.json` y haz build/stills para verlo).

## 4. Componentes (`comps` de cada escena)
Todos aceptan `at` (s desde el inicio de la escena) o `chunk` (índice del subtítulo de la escena) y opcionalmente `from:"side"` (entra de lado). `*palabra*` = color clave (`key`: g verde · r rojo · p pistacho · m menta).
| type | campos | uso |
|---|---|---|
| `pill` | `text`, `sub`, `tone` gold/red/green/dark, `ic` | hora, fecha, «PARTE 1» |
| `tag` | `text` | etiqueta de serie |
| `card` | `text`, `sub`, `tone` cream/dark, `size` (78), `key` | titular grande con la cifra clave |
| `stat` | `text`, `sub`, `tone` red/green/gold, `size` | el dato raro (la «píldora roja») |
| `num` | `value`, `from`, `dec`, `prefix`, `suffix`, `label`, `sub`, `tone`, `size`, `dur` | cifra que cuenta hacia arriba (suena a ruleta) |
| `vs` | `a`/`b`: `{label,value,sub,tone,vt}`, `mid` | dos cifras enfrentadas |
| `calendar` | `days:[{d,n,st,label}]` (st: up/down/unk/today/closed/half), `cols`, `step` | semana de mercado, rachas |
| `bars` | `items:[[nombre,valor,'g|r|p',"texto"]]` | reparto/ranking |
| `candles` | `data:[[o,h,l,c]…]` o `gen:{n,shape}` (caida, subida, lateral, caida_final), `zone:{from,to,label}`, `big:{text,tone}`, `title`, `dur`, `h` | velas que se dibujan; `zone` = franja resaltada; `big` = cifra gigante final |
| `line` | `pts:[[x,y]…]` (0-1), `ref` (línea de referencia), `marks:[{x,y,label,sub}]`, `color`, `title`, `dur`, `h` | línea con hitos (ciclos, medias móviles) |
| `logo` | `src`, `h` | logo de la empresa (de `img/logos`) |
| `follow` | `sub`, `tapAt` | tarjeta de perfil con botón Seguir |
| `disc` | `text` | descargo («no es consejo financiero») |
| `gap` | `h` | espacio |
Notas: si una escena lleva demasiado, se reduce sola para caber (y = 330…1420); aun así, **máx. 3-4 piezas**. Con datos reales de precio, pasar `data` real a `candles`/`line` (si no hay, `gen` solo vale como ilustración y NO puede afirmar niveles de precio).

## 5. Sonido en modo analista
Menos y más discreto: transición suave entre escenas, `pop` en la tarjeta y el dato rojo, `click` en gráficos y calendario, ruleta solo en `num`. `sfx.py` ya recorta el exceso. Sin música (regla del canal).

## 6. A/B: cómo se decide si funciona
- Primeras 2 semanas: **3 de cada 4 vídeos en modo analista y 1 de cada 4 en clásico** (control), mismo tipo de tema.
- Se anota por vídeo: modo, tema, puntuación del filtro, vistas a 24 h, **enviados/vistas** y me gusta/vistas. En los perfiles analizados los Reels ganadores tienen enviados/vistas ≈ 0,9–1,9 % y los flojos ≈ 0,2–0,4 %.
- Viernes 27-11 y 4-12: se compara con la línea base del 20-11 (mediana 1.047 vistas, 57 seguidores) y se ajusta este documento.
