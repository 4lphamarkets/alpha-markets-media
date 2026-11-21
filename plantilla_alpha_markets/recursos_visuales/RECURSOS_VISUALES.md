# Recursos visuales para reels y vídeos largos (ALPHA MARKETS)

Repos en /home/claude/repos (reinstalar con INSTALAR.sh). Regla: en cada vídeo nuevo, usar al menos 2-3 de estos recursos para que quede más animado y bonito, SIN romper el flujo de la plantilla v18 (HTML/Canvas + Playwright + ffmpeg, 1080x1920@30, voz siempre prioritaria, sin música).

| Repo | Qué aporta | Uso en ALPHA MARKETS | Disponible en el sandbox |
|---|---|---|---|
| earshot | 922 efectos de sonido generados por código, en CPU | `earshot make "whoosh transition" -o x.wav` para variar los SFX de sfx.py (impactos, whoosh, caja registradora, alarma, glitch). Ya probado | Sí |
| pixelfx | 244 efectos pixel-art (fuego, explosiones, magia, monedas) con export a sprite sheet | Insertos animados cortos (explosión al caer, fuego, monedas en subidas) como overlays vía insertos.json | Sí (node) |
| hyperframes | HTML a vídeo determinista con GSAP, registry de transiciones, subtítulos, gráficos y tarjetas | Escenas/transiciones/gráficos extra; skill en skills/hyperframes (leer SKILL.md antes) | Sí (node) |
| huashu-motion | Agente de motion graphics comerciales con edición visual | Aperturas y cierres tipo "película" de 3-5 s, tipografía cinética | Sí (node) |
| claude-animated-shorts | Pipeline three.js+Remotion de cortos animados 3D/2D con SFX y mezcla con ducking | Referencia para escenas 3D con cámara deslizante y estilo tinta en vídeos largos | Solo como guía |
| lemo-opuscar | Skill para hacer films por estilos (Neon Tubes, acuarela, LiDAR…) | Inspiración de estilos visuales; es plugin de Claude Code | Solo como guía |
| rea-video | Desmonta cualquier vídeo plano a plano (filmado/IA/código) y cómo rehacerlo | Analizar vídeos de la competencia para replicar ganchos y ritmo | Sí (pip) |
| react-three-rapier | Física 3D en React Three Fiber | Objetos 3D que caen/rebotan (monedas, velas, logos) en escenas three.js | Librería; solo con proyecto React |
| blender-mcp | Controla Blender desde Claude | Renders 3D (logos, toros/osos) | Necesita Blender instalado y abierto en el PC de Antonio; no hay en sandbox |
| Wan2.2 y LTX-Video | Generación de vídeo con IA | Clips de fondo generados | Necesitan GPU potente; el sandbox no tiene. Solo vía servicio externo |

Cómo aplicarlo en cada vídeo (checklist): 1) al guionizar, marcar 1 momento "wow" por escena (inserto pixelfx/hyperframes, cifra animada, transición); 2) SFX variados con earshot en lugar de repetir los mismos; 3) una apertura y un cierre distintivos; 4) no sobrecargar: la voz y la legibilidad mandan; 5) antes del render completo, mirar stills de los momentos con más elementos.
