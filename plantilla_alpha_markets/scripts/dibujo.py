"""MOMENTOS DIBUJADOS: convierte una imagen en un clip donde se DIBUJA sola delante del espectador.
Sale un .mp4 listo para meter con insertos.py (zona "escena" 900x900 por defecto), en máxima calidad.

uso:
  python scripts/dibujo.py <imagen.png|jpg>  insertos/<salida>.mp4  [opciones]
      → la imagen se traza a lápiz/tiza (líneas que avanzan con la punta brillante) y después se rellena de color.
  python scripts/dibujo.py --etapas <carpeta_png>  insertos/<salida>.mp4  [opciones]
      → timelapse con las etapas de claude-drawing (`--stages`): cada etapa funde con la siguiente.

opciones:
  --dur 4          duración total en s (2–6; defecto 4)
  --tam 900x900    tamaño del clip (900x900 para zona escena, 1080x1920 para pantalla completa)
  --estilo pizarra pizarra (fondo negro ALPHA, trazo de tiza + punta menta) | papel (papel crema, grafito)
  --ajuste cubrir  cubrir (rellena recortando, defecto) | contener
  --sin-color      se queda en el boceto (no rellena color al final)
Solo usa numpy + Pillow + ffmpeg (los mismos requisitos que la plantilla)."""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter, ImageOps

FPS = 30
ENC = ['-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-profile:v', 'high', '-tune', 'animation',
       '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
       '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-r', str(FPS)]

a = sys.argv[1:]
def opt(name, default):
    if name in a: i = a.index(name); v = a[i + 1]; del a[i:i + 2]; return v
    return default
def flag(name):
    if name in a: a.remove(name); return True
    return False
DUR = float(opt('--dur', 4)); W, H = map(int, opt('--tam', '900x900').lower().split('x'))
ESTILO = opt('--estilo', 'pizarra'); AJ = opt('--ajuste', 'cubrir'); SINCOLOR = flag('--sin-color'); ETAPAS = flag('--etapas')
if len(a) != 2: sys.exit(__doc__)
SRC, OUT = a
N = max(2, round(DUR * FPS))
BG = np.array((4, 7, 6) if ESTILO == 'pizarra' else (243, 236, 220), np.float32) / 255
TINTA = np.array((244, 255, 249) if ESTILO == 'pizarra' else (40, 40, 44), np.float32) / 255
PUNTA = np.array((52, 245, 176), np.float32) / 255


def encaja(im):
    im = im.convert('RGB')
    return ImageOps.fit(im, (W, H), Image.LANCZOS) if AJ == 'cubrir' else ImageOps.pad(im, (W, H), Image.LANCZOS, color=tuple(int(c * 255) for c in BG))


def ease(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)


def ruido(seed, esc):
    """ruido suave de baja frecuencia (0..1) a partir de una rejilla aleatoria reescalada."""
    g = np.random.default_rng(seed).random((max(2, H // esc), max(2, W // esc))).astype(np.float32)
    r = np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    return (r - r.min()) / (np.ptp(r) + 1e-6)


def escribir(frames_fn):
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                           '-i', '-', *ENC, OUT], stdin=subprocess.PIPE)
    for f in frames_fn():
        ff.stdin.write((np.clip(f, 0, 1) * 255).astype(np.uint8).tobytes())
    ff.stdin.close()
    if ff.wait() != 0: sys.exit('ffmpeg falló')
    print(f'ok {OUT}  ({N} fotogramas, {DUR:.1f} s, {W}x{H})')


def zoom(f, k):
    """zoom lento centrado (Ken Burns) de factor 1+k."""
    if k <= 0.001: return f
    im = Image.fromarray((np.clip(f, 0, 1) * 255).astype(np.uint8))
    cw, ch = W / (1 + k), H / (1 + k); x0, y0 = (W - cw) / 2, (H - ch) / 2
    return np.asarray(im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)), np.float32) / 255


# ---------------- modo etapas (claude-drawing --stages) ----------------
if ETAPAS:
    fs = sorted(f for f in os.listdir(SRC) if f.lower().endswith(('.png', '.jpg', '.jpeg')))
    if len(fs) < 2: sys.exit('La carpeta necesita al menos 2 etapas PNG/JPG')
    if len(fs) > 40: fs = [fs[round(i * (len(fs) - 1) / 39)] for i in range(40)]   # máx. 40 etapas
    imgs = [np.asarray(encaja(Image.open(os.path.join(SRC, f))), np.float32) / 255 for f in fs]
    def gen():
        hold = int(N * .22); M = N - hold                      # 78 % dibujándose, 22 % obra terminada con zoom
        for i in range(N):
            if i < M:
                x = (i / max(1, M - 1)) * (len(imgs) - 1); k = min(int(x), len(imgs) - 2); fr = ease((x - k) * 1.6)
                yield imgs[k] * (1 - fr) + imgs[k + 1] * fr
            else:
                yield zoom(imgs[-1], .05 * ease((i - M) / max(1, hold)))
    escribir(gen); sys.exit()

# ---------------- modo imagen → se dibuja sola ----------------
col = np.asarray(encaja(Image.open(SRC)), np.float32) / 255
g = Image.fromarray((col.mean(2) * 255).astype(np.uint8))
# boceto a lápiz: "color dodge" de la imagen gris con su negativo desenfocado
inv = ImageOps.invert(g).filter(ImageFilter.GaussianBlur(max(2, W // 110)))
gf, bf = np.asarray(g, np.float32) / 255, np.asarray(inv, np.float32) / 255
sk = np.clip((gf + .08) / (1 - bf + .08), 0, 1)                   # +0.08: las zonas oscuras lisas no se rellenan
linea = np.clip((1 - sk) * 2.6, 0, 1) ** 1.4                       # intensidad del trazo (0 = papel)
bordes = np.asarray(g.filter(ImageFilter.GaussianBlur(1)).filter(ImageFilter.FIND_EDGES), np.float32) / 255
linea = np.clip(np.maximum(linea, np.clip(bordes * 2.2, 0, 1) ** 1.3), 0, 1)
grano = np.random.default_rng(3).random((H, W)).astype(np.float32)
linea *= .75 + .25 * grano                                         # textura de tiza / grafito

# orden de dibujo: barrido diagonal + "trazos" por zonas (ruido) → parece que una mano va rellenando
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
diag = (xx / W * .55 + yy / H * .45)
T1 = diag * .55 + ruido(7, 90) * .30 + ruido(11, 22) * .15
T1 = (T1 - T1.min()) / np.ptp(T1)
T2 = (1 - yy / H) * .5 + ruido(19, 120) * .5                        # el color entra como una aguada
T2 = (T2 - T2.min()) / np.ptp(T2)
# fondo de pizarra/papel con viñeta suave
vig = 1 - .35 * (((xx / W - .5) ** 2 + (yy / H - .5) ** 2) * 2)
fondo = BG[None, None] * vig[..., None] + (grano[..., None] - .5) * (.025 if ESTILO == 'pizarra' else .04)

P1, P2 = (.62, 1.0) if SINCOLOR else (.50, .80)                    # fin del trazo, fin del color (fracción de N)
def gen():
    for i in range(N):
        u = i / (N - 1)
        p = ease(u / P1) * 1.04                                    # frente del trazo
        vis = np.clip((p - T1) / .035, 0, 1)
        f = fondo * (1 - linea[..., None] * vis[..., None]) + TINTA * (linea * vis)[..., None]
        if p < 1.02:                                               # punta brillante en el frente
            fr = np.exp(-((T1 - p) / .012) ** 2) * (linea > .15)
            f = f * (1 - fr[..., None] * .8) + PUNTA * fr[..., None] * .8 + PUNTA * fr[..., None] * .4
        if not SINCOLOR and u > P1 * .85:
            q = ease((u - P1 * .85) / (P2 - P1 * .85)) * 1.15
            c = np.clip((q - T2) / .12, 0, 1)[..., None]
            f = f * (1 - c) + col * c
            f = f * (1 - .22 * linea[..., None] * c)               # el trazo se queda marcado sobre el color
        if u > P2:
            f = zoom(f, .05 * ease((u - P2) / (1 - P2 + 1e-6)))
        yield f
escribir(gen)
