#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
python3 - <<'P'
L=open('template.html',encoding='utf-8').read().split('\n')
ln=lambda i:i-1
scenes=open('tmp/scenes_nvidia.html',encoding='utf-8').read().rstrip('\n').split('\n')
js=open('tmp/scenes_nvidia.js',encoding='utf-8').read().rstrip('\n').split('\n')
out=L[:ln(66)]+scenes+L[ln(161):ln(209)]+js+L[ln(291):]
t='\n'.join(out).replace('<div class="tag"><i></i>ORO Y PLATA</div>','<div class="tag"><i></i>NVIDIA EN CAÍDA</div>')
open('template_nvidia.html','w',encoding='utf-8').write(t)
import re
def svg(n):
    d=re.search(r'<path d="([^"]+)"',open(f'img/{n}.svg',encoding='utf-8').read()).group(1)
    return f'<svg viewBox="0 0 24 24" width="100%" height="100%"><path fill="currentColor" d="{d}"/></svg>'
h=t
for n in ('binance','bitcoin','instagram'):h=h.replace('{{'+n.upper()+'}}',svg(n))
h=h.replace('{{TL}}',open('tmp/timeline.json',encoding='utf-8').read())
open('index.html','w',encoding='utf-8').write(h);print('index ok')
P
