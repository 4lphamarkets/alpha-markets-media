# FLUJO DE TRABAJO ALPHA MARKETS (v25)

> 🆕 **v25: el montaje es SIEMPRE `montar.py … dinamico` (ver `ESTILO_DINAMICO.md`) y las portadas usan los 10 diseños de `historias/estilos/` (sin `foto_epica`). Donde este documento hable del modo analista/clásico o de portadas `foto_epica`/`disenos`, manda lo de v25.**

> 🆕 **v23: MONTAJE CON UN COMANDO.** `python scripts/montar.py revisar|video analista|clasico tmp/guion_*.json` hace prep → validar → build → (hoja de contacto) → render → insertos → efectos → mezcla −16 LUFS → control de calidad. Antes de renderizar se mira `out/hoja_contacto.jpg` (4 s) y `scripts/validar.py` avisa de errores de guion; el audio se transcribe con `scripts/transcribir.py`. Detalle en `LEEME.md`.

## 🆕 v19: RECURSOS VISUALES DE EDICIÓN (carpeta `recursos_visuales/`)
Se añadieron 11 repos de edición de vídeo (earshot, pixelfx, hyperframes, huashu-motion, claude-animated-shorts, lemo-opuscar, rea-video, react-three-rapier, blender-mcp, Wan2.2, LTX-Video). Leer `recursos_visuales/RECURSOS_VISUALES.md` (qué aporta cada uno y cuándo usarlo) y ejecutar `bash recursos_visuales/INSTALAR.sh` al empezar (reclona e instala todo; el sandbox es temporal). En **cada vídeo nuevo** usar 2-3 de estos recursos: SFX variados con earshot, insertos animados con pixelfx/hyperframes, apertura/cierre distintivos, sin romper el flujo v18 ni la legibilidad (la voz manda). Guías de cada repo en `recursos_visuales/guias/`.


> 🆕 **v18: PLAYBOOK DE COMPETENCIA.** Al elegir tema, escribir el gancho y diseñar portadas se aplica `PLAYBOOK_COMPETENCIA.md` (análisis de cuentas sin cara del nicho, 20-11-2026): eventos con hora exacta primero, gancho con paradoja/pregunta/calendario y un número concreto en la primera frase, portadas `dos_cifras` y `cuenta_atras`, 2 formatos de prueba por semana. Informe: https://claude.ai/artifact/KYBrHbufU4NPBDd2cYjzvy
> 🆕 **v22: MODO ANALISTA + FILTRO DE NOTICIAS.** (1) Antes de elegir tema se puntúan las candidatas con `FILTRO_NOTICIAS.md` (`python scripts/filtro_noticias.py`): solo vídeo si ≥ 70 (≥ 60 si hace falta rellenar), máx. 1 por tema. (2) El montaje usa por defecto el **modo analista** (`ESTILO_ANALISTA.md`: `prep_analista.py` → `build.py analista`) en 3 de cada 4 vídeos; 1 de cada 4 sigue en modo clásico (`template.html`) como control A/B durante 2 semanas. Lo demás (audio de Jaime, entrega, carpeta en el Escritorio, publicación) no cambia. (3) Al programar se anota: tema, puntuación, modo, vistas 24 h y enviados/vistas.

Este es el flujo acordado con el usuario para cada vídeo. Claude lo sigue **de principio a fin sin pedir permiso entre pasos**; las únicas paradas son las que se indican abajo (foto que falta, OK final).
Los detalles técnicos de cada paso (render, sonidos, portadas, insertos) están en `LEEME.md`.


> ⚠️ **REGLA v24: SIN PEDIR PERMISO.** La carpeta `<slug>` en el Escritorio lleva **TODO: vídeo, descripción y las 2 portadas** (4 archivos) y se deja **directamente, sin preguntar ni pedir confirmación en el chat** (Antonio: «No me pidas permiso, hazlo»). Si hay que conceder acceso a `~/Desktop`, se lanza `device_request_folder_access` sin avisar antes ni preguntar si se hace.

> ⚠️ **REGLA v17 (el usuario la reclamó): LA CARPETA EN EL ESCRITORIO NO ES OPCIONAL.** Al terminar cada vídeo, ANTES de escribir el mensaje final, Claude debe haber dejado `~/Desktop/<slug>/` con los 4 archivos (vídeo editado, descripción .txt, portada 1 y portada 2). El orden es siempre: (1) `SendUserFile` de los 4 archivos → (2) `get_device_info` / `device_request_folder_access` sobre `~/Desktop` si no está conectado → (3) `device_commit_files` con los 4 `file_uuid`. El mensaje final solo se escribe cuando el commit devuelve `written` con los 4 archivos, y dice textualmente «Carpeta `<slug>` en tu Escritorio». Si el ordenador no responde: reintentar una vez, y si sigue sin responder decir claramente «NO he podido dejar la carpeta en el Escritorio» (no dar el vídeo por entregado) y repetir en cuanto vuelva a estar conectado. Nunca cerrar la entrega con solo los archivos sueltos en el chat.

## Resumen

| # | Paso | Quién | Resultado |
|---|------|-------|-----------|
| 1 | Recibir el tema | Usuario | Imagen (captura, noticia, gráfico) **o** petición de un tema en texto |
| 2 | Escribir el guion | Claude | Texto de **40 s como máximo** |
| 3 | Generar el audio | Claude | Voz de Jaime en ElevenLabs, **[en tono juguetón]** |
| 4 | Montar el vídeo | Claude | Vídeo 9:16 editado con la plantilla |
| 5 | Preparar la entrega | Claude | Carpeta con descripción, vídeo editado y miniaturas |
| 5b | **Dejar la carpeta en el Escritorio (OBLIGATORIO, v17)** | Claude | `~/Desktop/<slug>/` con los 4 archivos, sin que lo pida y antes del mensaje final |
| 6 | Publicar (solo con el «OK» del usuario) | Claude | Reel en Instagram y Short en YouTube vía Metricool |

---

## 1. El usuario manda el tema
Dos formas, las dos válidas:
- **Imagen**: captura de una noticia, tuit, gráfico, titular… Claude lee la imagen, identifica el tema y busca en la web los datos actuales y verificables antes de escribir (cifras, fechas, protagonistas, fuentes).
- **Texto**: «hazme un guion sobre X» o «dame un tema». Si pide un tema, Claude propone **uno** (el más fuerte y actual que encuentre, con una línea de por qué) y arranca con él sin esperar; si el usuario prefiere otro, se cambia.

**Prioridad al proponer tema (v18):** (1) evento de las próximas horas con hora exacta, (2) noticia del día con cifra grande o personaje conocido (Nvidia, Anthropic, Fed, Trump, Musk), (3) cripto con cifra o conflicto concreto; lo atemporal, al final de la cola. Detalle en `PLAYBOOK_COMPETENCIA.md`.

Nada de preguntas previas si el tema está claro. Si el vídeo trata de **una persona** y falta su foto en `img/personas/`, se la pide ya (para la portada); es la única pausa del flujo antes del audio. Los logos que falten se descargan con `python scripts/logos.py <nombre>`.

## 2. Guion (máximo 40 s)
- **Duración: 40 segundos como MÁXIMO (v24, decisión de Antonio el 22-11-2026).** Sustituye al antiguo rango de 40 s – 1:20. Orientación a ritmo hablado: **~90–100 palabras (≈550–650 caracteres) para 35–40 s**; nunca más de 100 palabras. El vídeo final no puede pasar de 40 s (`qa_video.py` lo da como error). Si el usuario pide otra duración concreta, manda la suya.
- Estructura: **gancho** en los 2 primeros segundos (dato o pregunta que enganche) → contexto → datos clave (cifras que se puedan mostrar en contadores) → consecuencia para el mercado/inversor → **cierre**.
- **Gancho (v18):** la primera frase lleva siempre **un número concreto** y sigue una de estas fórmulas: **paradoja** («X vale ... y dicen que está más barata que cuando valía ...»), **pregunta con "falta algo"** («¿Por qué no se dispara X? Falta ...») o **calendario** («¿Casualidad o calendario?», «X se juega la semana el martes a las 22:20»). Nada que no se haya comprobado ni fechas límite alarmistas sin fuente sólida.
- **Formatos de prueba (v18, 2 por semana):** cuenta atrás de evento y meme de inversor con animación propia («Yo cuando ...», «POV: ...»; sin clips de películas ni vídeo de archivo ajeno). Duración: máximo 40 s salvo que el usuario pida otra.
- Tono: cercano, claro, dinámico y con chispa (la voz va en tono juguetón). Frases cortas, nada de relleno.
- Cierre fijo en los guiones de cripto: **«Sígueme para no perderte nada de los mercados financieros, esto es... ALFA MARKETS!!»**
- En el texto de audio la marca se escribe **«Alfa Markets»** (pronunciación). En pantalla es siempre **4LPHA MARKETS**.
- Sin música de fondo en ningún vídeo.
- Claude le enseña el guion en el chat (breve) y **sigue con el audio sin esperar aprobación**, salvo que el usuario haya pedido revisarlo antes.

## 3. Audio con Jaime en ElevenLabs
- Herramienta: ElevenLabs, **texto a voz**, locutor **«Jaime - Confident, Clear and Warm»**.
- **Al texto se le añade siempre al principio la etiqueta `[en tono juguetón]`.**
- **Una sola generación** por audio (no se hacen 2 tomas).
- **Créditos (v24):** con un guion de 40 s (~600 caracteres) el audio cuesta ≈ 600 créditos. **NO se pide el OK para generar el audio mientras el coste estimado sea de 2.000 créditos o menos por audio**: se genera directamente (decir el coste en el mensaje de entrega, sin esperar respuesta). **Solo se pregunta si el audio supera los 2.000 créditos** (decir cuánto cuesta y esperar el OK). Esta regla sustituye a la de «avisar siempre antes de gastar créditos» para ElevenLabs; otras herramientas de pago (p. ej. motion/IA) siguen pidiendo permiso.
- Se genera desde el conector de ElevenLabs (herramienta `creative_generate_speech` / `creative_list_voices` para localizar a Jaime). Se guarda el audio como `tmp/voz.mp3` (o `.wav`) de la plantilla y de ahí sigue el montaje (`python scripts/transcribir.py tmp/voz.mp3` → tiempos de cada frase → guion de montaje → `montar.py`).
- Si el conector no estuviera disponible, Claude lo dice en una línea y pide al usuario el audio generado a mano con esos mismos ajustes.

## 4. Montaje del vídeo
Con el audio y esta plantilla, se sigue `LEEME.md` §1 (6 pasos con `montar.py`): transcribir → guion de montaje (`tmp/guion_analista.json`; en modo clásico, además, adaptar las escenas de `template.html`) → **hoja de contacto y corrección** → render PNG sin pérdida → efectos de sonido → mezcla final → control de calidad. Detalle técnico en `REFERENCIA_TECNICA.md`.
Reglas fijas del canal (todas en `LEEME.md`): 1080×1920, máxima calidad (H.264 slow CRF 12, AAC 320), subtítulos en mayúsculas y blancos (Montserrat Black y/o Awesome Serif Italic Bold ExtraTall, variando según lo que mejor quede), logos de las empresas citadas, banderas y animaciones divertidas, contadores con sonido distinto cada uno, 1–3 momentos dibujados (más en vídeos largos), efectos de sonido con la voz siempre por delante, tarjeta de perfil con botón Seguir al final (@4lphamarkets), cabecera con el logo de letras.
Con vídeos de 40 s como máximo bastan 1–2 momentos dibujados; si el usuario pidiera expresamente un vídeo más largo, se escalan los insertos y los momentos dibujados (2–3).

## 5. Entrega: una carpeta por vídeo
Claude **genera sin que se lo pidan** la carpeta del vídeo con todo dentro:

```
<slug>/
  <slug>_video.mp4          ← vídeo editado final
  <slug>_descripcion.txt    ← título · descripción · hashtags (texto limpio, sin rótulos)
  <slug>_portada_1.jpg      ← miniatura 1 (estilo foto épica)
  <slug>_portada_2.jpg      ← miniatura 2 (concepto nuevo desde cero)
```

- **Portadas (v18):** si el tema encaja, una de las dos puede ser `dos_cifras` (tarjetas con cifras enfrentadas + titular en pregunta) o, en vídeos de eventos, `cuenta_atras` (la hora o la fecha como elemento más grande); ver `portadas/CATALOGO.md`. Siguen las reglas de portadas muy distintas entre vídeos consecutivos.
- Se genera con `python scripts/entrega.py` (ver «ENTREGA AUTOMÁTICA TRAS EL RENDER» y las reglas de portadas v10/v11 en `LEEME.md`): descripción SEO, 2 portadas distintas, historial anti-repetición.
- **Entrega sin comprimir** (el usuario no tiene WinRAR): se mandan con SendUserFile el vídeo, las 2 miniaturas y el .txt por separado, y se pega en el chat el texto limpio (título, descripción y hashtags). Si hay carpetas del PC conectadas, se deja también la carpeta del vídeo allí. El .zip es opcional.
- Cierre del mensaje de entrega: una línea con el resultado y la pregunta de si todo está bien para publicar.

### 5b. Dejar la carpeta en el Escritorio (v16, obligatorio y automático)
En cuanto termina el montaje y la entrega (paso 5), Claude **deja la carpeta del vídeo (portadas, descripción y vídeo) en el Escritorio del usuario**, sin que lo pida, **sin preguntar y sin pedir permiso (v24)**:
1. Enviar los 4 archivos con `SendUserFile` (vídeo, 2 miniaturas, descripción); cada envío devuelve un `file_uuid`.
2. Si el Escritorio no está conectado (`get_device_info` → `connectedFolders`), pedir acceso **una sola vez** con `device_request_folder_access` sobre `~/Desktop` (razón: «Guardar la carpeta <slug> en tu Escritorio»).
3. `device_commit_files` con cada `fileUuid` → `~/Desktop/<slug>/<slug>_video.mp4`, `<slug>_portada_1.jpg`, `<slug>_portada_2.jpg`, `<slug>_descripcion.txt` (se crea la carpeta `<slug>` sola).
4. En el mensaje de entrega decir en una línea que la carpeta `<slug>` está en el Escritorio. Si el ordenador no responde (apagado, app cerrada), decirlo y dejar los archivos enviados por el chat; no repetir escrituras que pudieran haberse hecho.
Esto va **además** del envío por el chat (que sigue siendo sin comprimir, sin .zip).

## 6. Publicación (cuando el usuario dice «OK»)
Con el **OK** del usuario, Claude sube el vídeo solo, sin más preguntas:
- **Instagram (Reel)** de 4lphamarkets y **YouTube (Short)** a través de Metricool (blogId 8199629, zona Europe/Madrid).
- Se usa la miniatura que Claude considere **más atractiva y visible** (en Instagram la mejor; si hay 2, la segunda en YouTube). Título de YouTube sacado de la primera línea de la descripción.
- Procedimiento técnico probado (repo público `4lphamarkets/alpha-markets-media` como almacén temporal, `createScheduledPost`, limpieza del repo después): ver `LEEME.md` → publicación, y la memoria del canal. Al terminar se avisa de que el historial de git conserva el archivo y se ofrece vaciarlo.
- Si hay varios vídeos pendientes, Claude elige fechas y horas (hasta 3 al día).

---

## Reglas de oro del flujo
1. **Cero fricción**: el usuario da la idea (imagen o tema) y Claude hace todo hasta tener la carpeta lista; después, con su OK, lo deja publicado.
2. **Solo se para** para: pedir la foto de una persona que falta, conceder el acceso al Escritorio (primera vez), avisar de un fallo que bloquea (p. ej. ElevenLabs sin acceso) o esperar el OK de publicación.
3. **Datos siempre verificados** en la web y con fuente; nada inventado en cifras ni citas.
4. **Esto no es consejo financiero**: va siempre en la última línea de la descripción.
5. Si el usuario adjunta una plantilla nueva, esa pasa a ser la vigente y Claude actualiza su memoria.
6. **Medir y corregir (v18):** al programar cada vídeo se anota tema, fórmula de gancho, formato y vistas a las 24 h; cada viernes se revisa qué sube y se ajusta `PLAYBOOK_COMPETENCIA.md`.
