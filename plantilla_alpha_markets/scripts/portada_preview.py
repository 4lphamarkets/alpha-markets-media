"""VISTA PREVIA DE UN DISEÑO DE PORTADA (v10) mientras se diseña, sin hacer la entrega completa.
uso: python scripts/portada_preview.py portadas/disenos/<slug>_a.html [salida.jpg] [--guia]
  --guia  dibuja la zona segura del recorte 3:4 del perfil (y = 240…1680) para comprobar que nada importante queda fuera.
Inyecta window.D con el bloque "portada" de entrega.json si existe (las rutas del HTML son relativas a la raíz de la plantilla)."""
import json, os, re, subprocess, sys
from PIL import Image

D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
if not args: sys.exit(__doc__)
html = os.path.join(D, args[0]) if not os.path.isabs(args[0]) else args[0]
sal = args[1] if len(args) > 1 else os.path.join(D, 'out', os.path.splitext(os.path.basename(html))[0] + '_preview.jpg')
datos = {}
try: datos = json.load(open(os.path.join(D, 'entrega.json'), encoding='utf-8-sig')).get('portada', {})
except Exception: pass
h = open(html, encoding='utf-8').read()
extra = '<script>window.GUIA = true;</script>' if '--guia' in sys.argv else ''
h = re.sub(r'<head[^>]*>', lambda m: m.group(0) + f'<script>window.D = {json.dumps(datos, ensure_ascii=False)};</script>' + extra, h, count=1)
open(os.path.join(D, 'portada_index.html'), 'w', encoding='utf-8').write(h)
subprocess.run(['node', os.path.join(D, 'scripts', 'render.js'), 'portada', 'sinfondo'], check=True, cwd=D)
os.makedirs(os.path.dirname(os.path.abspath(sal)), exist_ok=True)
Image.open(os.path.join(D, 'tmp', 'portada.png')).convert('RGB').save(sal, 'JPEG', quality=92)
print('preview:', sal)
