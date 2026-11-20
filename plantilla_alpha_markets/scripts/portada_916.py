"""Convierte una portada/miniatura (p. ej. 2:3, 3:4, 1:1...) a 9:16 vertical (1080x1920) SIN recortar nada:
escala al ancho 1080 y rellena arriba/abajo con degradado oscuro del propio borde (arriba) y un reflejo suave (abajo).
uso: python scripts/portada_916.py <imagen> [salida.png]   (por defecto <imagen>_9x16.png)
Pensado para imágenes ya hechas (p. ej. generadas fuera de la plantilla) que el usuario pide en formato Reels/Shorts."""
import sys, os
import numpy as np
from PIL import Image, ImageFilter, ImageOps
if len(sys.argv) < 2: sys.exit(__doc__)
src = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + '_9x16.png'
W, H = 1080, 1920
im = Image.open(src).convert('RGB'); h = round(im.height * W / im.width); b = im.resize((W, h), Image.LANCZOS)
if h >= H: sys.exit('La imagen ya es más alta que 9:16: recórtala en lugar de ampliar.')
ext = H - h; top = ext * 4 // 10; bot = ext - top
c = Image.new('RGB', (W, H)); c.paste(b, (0, top))
dark = np.array([4, 14, 10], np.float32)
row = b.crop((0, 0, W, 6)).resize((W, max(top, 1)), Image.BICUBIC).filter(ImageFilter.GaussianBlur(25))
a = np.linspace(.45, 1, max(top, 1))[:, None, None]
if top: c.paste(Image.fromarray((np.asarray(row, np.float32) * a + dark * (1 - a)).clip(0, 255).astype('uint8')), (0, 0))
if bot:
    bt = ImageOps.flip(b.crop((0, h - bot, W, h))).filter(ImageFilter.GaussianBlur(10))
    a2 = np.linspace(1, 0, bot)[:, None, None]; k = .2 + .8 * a2
    c.paste(Image.fromarray((np.asarray(bt, np.float32) * k + dark * (1 - k) * .6).clip(0, 255).astype('uint8')), (0, top + h))
for y0 in (top, top + h):
    if 0 < y0 < H: c.paste(c.crop((0, y0 - 14, W, y0 + 14)).filter(ImageFilter.GaussianBlur(6)), (0, y0 - 14))
c.save(out); print('listo', out, c.size)
