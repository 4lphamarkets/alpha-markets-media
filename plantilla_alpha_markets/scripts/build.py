"""Genera index.html: template.html + iconos SVG de /img + tmp/timeline.json.
uso: python scripts/build.py   (desde cualquier carpeta)"""
import os, re
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
def svg(n):
    d = re.search(r'<path d="([^"]+)"', open(f'{A}/img/{n}.svg', encoding='utf-8').read()).group(1)
    return f'<svg viewBox="0 0 24 24" width="100%" height="100%"><path fill="currentColor" d="{d}"/></svg>'
h = open(f'{A}/template.html', encoding='utf-8').read()
for n in ('binance', 'bitcoin', 'instagram'):
    h = h.replace('{{' + n.upper() + '}}', svg(n))
h = h.replace('{{TL}}', open(f'{A}/tmp/timeline.json', encoding='utf-8').read())
open(f'{A}/index.html', 'w', encoding='utf-8').write(h)
print('index.html ok')
