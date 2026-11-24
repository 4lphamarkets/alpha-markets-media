"""INSERTOS: mete clips e imágenes hechos con las skills (Manim, anidoodle, HandDraw, claude-drawing, motion...)
dentro del vídeo de la plantilla, en MÁXIMA CALIDAD (mismos ajustes que render.js).
uso: python scripts/insertos.py [insertos.json]      ← entre `render.js video` y `final.py`

Lee insertos.json (ver insertos_ejemplo.json). Cada inserto:
  clip     ruta a .mp4 / .mov (con o sin alfa) / .webm / .png / .jpg   (relativa a la plantilla)
  t0       segundo del vídeo en que aparece          dur   cuánto dura (s)
  desde    (vídeo) segundo del clip desde el que empieza, por defecto 0
  zona     "escena"   = la caja de las escenas (x90 y330 900x900): cabecera y subtítulos siguen visibles  [defecto]
           "completa" = pantalla completa 1080x1920 (tapa también los subtítulos)
           [x, y, w, h] = caja a medida
  ajuste   "contener" (cabe entero, defecto) | "cubrir" (rellena la caja recortando)
  esquinas radio de las esquinas en px (defecto 36 en "escena", 0 en "completa"; 0 para clips con fondo transparente)
  fundido  fundido de entrada/salida en s (defecto 0.25)
  zoom     true = zoom lento tipo Ken Burns (para imágenes fijas; defecto true en imágenes)
El vídeo original se guarda en tmp/video_sin_insertos.mp4 y siempre se parte de él → se puede repetir sin acumular."""
import json, os, shutil, subprocess, sys
from PIL import Image, ImageDraw

D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
FPS = 30
ZONAS = {'escena': (90, 330, 900, 900), 'completa': (0, 0, 1080, 1920)}
ENC = ['-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-profile:v', 'high', '-tune', 'animation',
       '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-r', str(FPS)]
IMG = ('.png', '.jpg', '.jpeg', '.webp')

cfg = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(D, 'insertos.json')
items = json.load(open(cfg, encoding='utf-8'))['insertos']
tmp = os.path.join(D, 'tmp'); vid = os.path.join(tmp, 'video.mp4'); orig = os.path.join(tmp, 'video_sin_insertos.mp4')
if not os.path.exists(orig): shutil.copyfile(vid, orig)
if not items:
    shutil.copyfile(orig, vid); print('sin insertos: vídeo restaurado'); sys.exit(0)   # v23: antes salía con código 1


def tam(path):
    if path.lower().endswith(IMG): return Image.open(path).size
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', path],
                       capture_output=True, text=True, check=True).stdout.strip().split(',')
    return int(o[0]), int(o[1])


ins, fc, base = ['-i', orig], [], '[0:v]'
k = 1
for n, it in enumerate(items):
    clip = os.path.join(D, it['clip']); t0 = float(it['t0']); dur = float(it['dur'])
    if not os.path.exists(clip): sys.exit(f'No existe el clip: {clip}')
    z = it.get('zona', 'escena'); X, Y, W, H = ZONAS[z] if isinstance(z, str) else z
    img = clip.lower().endswith(IMG)
    rad = int(it.get('esquinas', 0 if z == 'completa' else 36)); fade = float(it.get('fundido', 0.25))
    cw, ch = tam(clip)
    if it.get('ajuste', 'contener') == 'cubrir': s = max(W / cw, H / ch)
    else: s = min(W / cw, H / ch)
    w, h = int(cw * s) // 2 * 2, int(ch * s) // 2 * 2
    ow, oh = min(w, W), min(h, H)              # tamaño final tras recortar (cubrir)
    if img: ins += ['-loop', '1', '-framerate', str(FPS), '-t', f'{dur}', '-i', clip]
    else: ins += ['-ss', f"{float(it.get('desde', 0))}", '-t', f'{dur}', '-i', clip]
    ci = k; k += 1
    f = f'[{ci}:v]fps={FPS},format=rgba,'
    if img and it.get('zoom', True):
        nfr = max(1, round(dur * FPS))
        f += (f"scale={w * 2}:{h * 2},zoompan=z='1+0.07*on/{nfr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={w}x{h}:fps={FPS},format=rgba,")
    else:
        f += f'scale={w}:{h}:flags=lanczos,'
    if (ow, oh) != (w, h): f += f'crop={ow}:{oh},'
    if rad > 0:
        m = Image.new('L', (ow, oh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, ow - 1, oh - 1], rad, fill=255)
        mp = os.path.join(tmp, f'inserto_mask{n}.png'); m.save(mp)
        ins += ['-loop', '1', '-framerate', str(FPS), '-t', f'{dur}', '-i', mp]; mi = k; k += 1
        fc.append(f'[{mi}:v]format=gray[m{n}]')
        f += f'trim=duration={dur}[r{n}];[r{n}][m{n}]alphamerge,'
    else:
        f += f'trim=duration={dur},'
    if fade > 0: f += f'fade=t=in:st=0:d={fade}:alpha=1,fade=t=out:st={max(0, dur - fade)}:d={fade}:alpha=1,'
    f += f'setpts=PTS-STARTPTS+{t0}/TB[c{n}]'
    fc.append(f)
    x, y = X + (W - ow) // 2, Y + (H - oh) // 2
    fc.append(f"{base}[c{n}]overlay={x}:{y}:enable='between(t,{t0},{t0 + dur})':eof_action=pass:format=auto[b{n}]")
    base = f'[b{n}]'
fc.append(f'{base}scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[out]')
out = os.path.join(tmp, 'video_insertos.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fc), '-map', '[out]', *ENC, out], check=True)
shutil.move(out, vid)
print(f'{len(items)} inserto(s) aplicados -> tmp/video.mp4  (original en tmp/video_sin_insertos.mp4)')
