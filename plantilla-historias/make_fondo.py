#!/usr/bin/env python3
"""Genera assets/fondo_historia.png (1080x1920): fondo ALPHA MARKETS verde oscuro
con nebulosa, globo de puntos, velas y partículas. Es determinista (semilla fija).
Solo hace falta ejecutarlo si se quiere regenerar el fondo; build_story.py usa el PNG ya guardado.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "fondo_historia.png")
MINT = (52, 245, 176)


def glow(layer, radius, strength=1.0):
    b = layer.filter(ImageFilter.GaussianBlur(radius))
    if strength != 1.0:
        a = b.getchannel("A").point(lambda v: min(255, int(v * strength)))
        b.putalpha(a)
    return b


def main():
    rnd = random.Random(7)
    np_rnd = np.random.default_rng(7)

    # 1) degradado base
    y = np.linspace(0, 1, H)[:, None, None]
    top = np.array([3, 22, 17]); mid = np.array([4, 28, 21]); bot = np.array([2, 12, 9])
    t = np.clip(y / 0.45, 0, 1)
    base = top * (1 - t) + mid * t
    t2 = np.clip((y - 0.45) / 0.55, 0, 1)
    base = base * (1 - t2) + bot * t2
    img = Image.fromarray(np.repeat(base, W, axis=1).astype("uint8"), "RGB").convert("RGBA")

    # 2) nebulosa (manchas gaussianas con ruido)
    neb = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(neb)
    for _ in range(46):
        cx = rnd.gauss(180, 170); cy = rnd.gauss(330, 190)
        r = rnd.randint(40, 150)
        a = rnd.randint(18, 60)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(20, 230, 160, a))
    for _ in range(24):
        cx = rnd.gauss(900, 140); cy = rnd.gauss(260, 150)
        r = rnd.randint(40, 120)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(30, 200, 150, rnd.randint(10, 34)))
    neb = neb.filter(ImageFilter.GaussianBlur(38))
    img = Image.alpha_composite(img, neb)

    # 3) globo: halo, borde y red de puntos
    cx, cy, R = 560, 600, 500
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(*MINT, 150), width=5)
    img = Image.alpha_composite(img, glow(halo, 22, 1.6))
    img = Image.alpha_composite(img, glow(halo, 6, 0.9))
    globe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(globe)
    gd.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(10, 70, 52, 70))
    tilt = math.radians(-18)
    for lat in range(-80, 90, 8):
        la = math.radians(lat)
        for lon in range(0, 360, 5):
            lo = math.radians(lon + lat * 0.6)
            x3 = math.cos(la) * math.sin(lo)
            y3 = math.sin(la)
            z3 = math.cos(la) * math.cos(lo)
            y3r = y3 * math.cos(tilt) - z3 * math.sin(tilt)
            z3r = y3 * math.sin(tilt) + z3 * math.cos(tilt)
            if z3r < -0.05:
                continue
            px = cx + R * 0.985 * x3; py = cy - R * 0.985 * y3r
            rad = 1.6 + 1.6 * z3r
            al = int(55 + 150 * z3r)
            gd.ellipse((px - rad, py - rad, px + rad, py + rad), fill=(*MINT, al))
    # arcos de conexión
    pts = []
    for _ in range(26):
        a = rnd.uniform(0, 2 * math.pi); rr = R * math.sqrt(rnd.uniform(0.05, 0.9))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.9))
    for i in range(len(pts) - 1):
        gd.line((pts[i], pts[i + 1]), fill=(*MINT, 70), width=2)
    img = Image.alpha_composite(img, glow(globe, 2.5, 1.2))
    img = Image.alpha_composite(img, globe)

    # 4) velas arriba a la derecha
    cand = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cand)
    x0 = 800; n = 8; wc = 22; gap = 12
    price = 250.0
    for i in range(n):
        x = x0 + i * (wc + gap)
        o = price
        c = o - rnd.uniform(14, 60)
        up = rnd.random() > 0.2
        if not up:
            c = o + rnd.uniform(8, 25)
        hi = min(o, c) - rnd.uniform(8, 30); lo = max(o, c) + rnd.uniform(8, 25)
        col = (*MINT, 215) if up else (255, 90, 90, 170)
        cd.line((x + wc // 2, hi, x + wc // 2, lo), fill=col, width=3)
        cd.rounded_rectangle((x, min(o, c), x + wc, max(o, c)), radius=3, fill=col)
        price = c
    img = Image.alpha_composite(img, glow(cand, 16, 1.4))
    img = Image.alpha_composite(img, cand)

    # 5) toro de marca, muy tenue, detrás del titular (blend "screen")
    toro = Image.open(os.path.join(HERE, "assets", "toro.png")).convert("RGB").resize((560, 500), Image.LANCZOS)
    tl = Image.new("RGB", (W, H), (0, 0, 0))
    tl.paste(toro, (590, 330))
    tl = tl.filter(ImageFilter.GaussianBlur(1.2))
    arr = np.asarray(img.convert("RGB")).astype("float32") / 255
    tarr = np.asarray(tl).astype("float32") / 255 * 0.55
    arr = 1 - (1 - arr) * (1 - tarr)
    img = Image.fromarray((arr * 255).astype("uint8"), "RGB").convert("RGBA")

    # 6) partículas
    part = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(part)
    for _ in range(520):
        px = rnd.uniform(0, W); py = abs(rnd.gauss(0, 520)) if rnd.random() < 0.7 else rnd.uniform(0, H)
        if py > H:
            continue
        r = rnd.choice([0.8, 1, 1, 1.4, 1.8, 2.4])
        pd.ellipse((px - r, py - r, px + r, py + r), fill=(*MINT, rnd.randint(70, 230)))
    img = Image.alpha_composite(img, glow(part, 3, 1.5))
    img = Image.alpha_composite(img, part)

    # 7) viñeta y oscurecimiento inferior
    yy, xx = np.mgrid[0:H, 0:W]
    v = ((xx - W / 2) / (W / 2)) ** 2 * 0.35 + ((yy - H * 0.45) / (H * 0.6)) ** 2 * 0.35
    v = np.clip(1 - v * 0.8, 0.35, 1)[..., None]
    arr = np.asarray(img.convert("RGB")).astype("float32") * v
    arr[int(H * 0.62):] *= np.linspace(1, 0.55, H - int(H * 0.62))[:, None, None]
    Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB").save(OUT)
    print("OK", OUT)


if __name__ == "__main__":
    main()
