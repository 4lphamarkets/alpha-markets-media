"""Genera index.html: plantilla + iconos SVG de /img + tmp/timeline.json.
uso: python scripts/build.py                (modo clásico: template.html)
     python scripts/build.py analista       (modo ANALISTA v22: template_analista.html)
     python scripts/build.py analista otra_timeline.json
v23: error claro si falta el timeline, comprueba que no queden {{marcadores}} sin sustituir y que el JSON no cierre el <script>."""
import json, os, re, sys
args = [a for a in sys.argv[1:] if not a.startswith('--')]
MODO = args[0] if args and args[0] in ('analista', 'clasico', 'dinamico') else ''
rest = [a for a in args if a not in ('analista', 'clasico', 'dinamico')]
TPL = {'analista': 'template_analista.html', 'dinamico': 'template_dinamico.html'}.get(MODO, 'template.html')
A = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
TLP = os.path.abspath(rest[0]) if rest else os.path.join(A, 'tmp', 'timeline.json')
if not os.path.exists(TLP):
    sys.exit(f'No existe {TLP}: genera antes el timeline (prep_analista.py / prep_clasico.py).')
tl = open(TLP, encoding='utf-8-sig').read()
try: json.loads(tl)
except Exception as e: sys.exit(f'{TLP} no es un JSON válido: {e}\n(pista: los números van como 0.5, no .5; sin comas finales; comillas dobles)')
def svg(n):
    d = re.search(r'<path d="([^"]+)"', open(f'{A}/img/{n}.svg', encoding='utf-8').read()).group(1)
    return f'<svg viewBox="0 0 24 24" width="100%" height="100%"><path fill="currentColor" d="{d}"/></svg>'
h = open(f'{A}/{TPL}', encoding='utf-8').read()
for n in ('binance', 'bitcoin', 'instagram'):
    h = h.replace('{{' + n.upper() + '}}', svg(n))
h = h.replace('{{TL}}', tl.replace('</', '<\\/'))
pend = re.findall(r'\{\{[A-Z_]+\}\}', h)
if pend: sys.exit(f'Quedan marcadores sin sustituir en {TPL}: {sorted(set(pend))}')
open(f'{A}/index.html', 'w', encoding='utf-8').write(h)
print('index.html ok ·', TPL)
