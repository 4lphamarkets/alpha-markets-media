#!/usr/bin/env python3
"""ALPHA MARKETS · generador de historias de Instagram (1080x1920).

Uso:
    python3 build_story.py cripto data.json historia.png 21:20 [AAAA-MM-DD]
    python3 build_story.py bolsa  data.json historia.png 21:20 [AAAA-MM-DD]
    python3 build_story.py --selftest

data.json (precio y variación % CON SIGNO tal como los muestra la web):
    cripto: BTC, ETH, HYPE, SOL, BNB, LIT -> {"price": 62546.1, "change": -0.29}
            FNG -> número entero 0-100 (Fear & Greed)
    bolsa : SPX, NDX, ANT, SPCX, AMZN, GOOGL, AAPL, NVDA, MSFT -> {"price": ..., "change": ...}
    "capturado": "2026-11-20T21:20:05+01:00"  (opcional: hora real de lectura; si falta se usa la hora
                 de modificación de data.json. En ambos casos se rechazan datos de más de 45 min)
    opcional por activo: "change_text": "-0.29%"  (se comprueba que el signo coincide)

Si algo no cuadra imprime "ERROR: ..." y sale con código 1: en ese caso NO se publica nada.
Solo necesita Pillow y numpy. Todo lo demás (fuentes, fondo, iconos) está en esta carpeta.
"""
import datetime as dt
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
MINT = (52, 245, 176)
GREEN = (40, 240, 150)
RED = (255, 84, 84)
WHITE = (255, 255, 255)
GREY = (150, 190, 176)

F_BLACK_IT = os.path.join(HERE, "fonts", "MontserratAlpha-BlackItalic.ttf")
F_XBOLD = os.path.join(HERE, "fonts", "MontserratAlpha-ExtraBold.ttf")
F_INTER = os.path.join(HERE, "fonts", "InterAlpha-Bold.ttf")

MESES = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]

# clave -> (ticker, subtítulo, mín, máx precio razonable, máx |variación| %)
CRIPTO = [  # v26 (26-11-2026): BTC, ETH, HYPE, SOL, BNB, LIT (Lighter) + Fear & Greed
    ("BTC", "BTC", "BITCOIN", 1e3, 1e7, 60),
    ("ETH", "ETH", "ETHEREUM", 50, 1e5, 60),
    ("HYPE", "HYPE", "HYPERLIQUID", 0.1, 1e4, 60),
    ("SOL", "SOL", "SOLANA", 1, 1e4, 60),
    ("BNB", "BNB", "BNB", 10, 1e5, 60),
    ("LIT", "LIT", "LIGHTER", 0.01, 1e3, 80),
]
BOLSA = [  # v26: S&P 500, Nasdaq, Anthropic, SpaceX, Amazon, Google, Apple, Nvidia, Microsoft (sin Fear & Greed)
    ("SPX", "S&P 500", "ÍNDICE", 1e3, 5e4, 15),
    ("NDX", "NASDAQ", "COMPOSITE", 1e3, 1e5, 15),
    ("ANT", "ANT", "ANTHROPIC", 1, 1e5, 80),
    ("SPCX", "SPCX", "SPACEX", 1, 1e5, 80),
    ("AMZN", "AMZN", "AMAZON", 1, 5e3, 40),
    ("GOOGL", "GOOGL", "GOOGLE", 1, 5e3, 40),
    ("AAPL", "AAPL", "APPLE", 1, 5e3, 40),
    ("NVDA", "NVDA", "NVIDIA", 1, 5e3, 40),
    ("MSFT", "MSFT", "MICROSOFT", 1, 5e3, 40),
]
INDICES = {"SPX", "NDX"}  # sin símbolo $


class StoryError(Exception):
    pass


# ───────────────────────── utilidades ─────────────────────────
def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError as e:
        raise StoryError(f"no se puede cargar la fuente {path}: {e}")


def madrid_now():
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("Europe/Madrid"))
    except Exception:  # sin tzdata: regla UE (último domingo de marzo/octubre, 01:00 UTC)
        u = dt.datetime.now(dt.timezone.utc)

        def last_sun(y, m):
            d = dt.datetime(y, m, 31, 1, tzinfo=dt.timezone.utc)
            return d - dt.timedelta(days=(d.weekday() + 1) % 7)
        off = 2 if last_sun(u.year, 3) <= u < last_sun(u.year, 10) else 1
        return u.astimezone(dt.timezone(dt.timedelta(hours=off)))


def fmt_price(key, p):
    if key in INDICES:
        return f"{p:,.2f}"
    if key in {r[0] for r in CRIPTO}:
        return f"${p:,.0f}" if p >= 1000 else f"${p:,.2f}"
    return f"${p:,.2f}"


def fmt_change(c):
    r = round(c, 2)
    if r == 0:
        return "0.00%"
    return f"{r:+.2f}%"


def text_w(d, s, f):
    return d.textlength(s, font=f)


def rr_mask(size, box, radius, k=3):
    m = Image.new("L", (size[0] * k, size[1] * k), 0)
    ImageDraw.Draw(m).rounded_rectangle([v * k for v in box], radius=radius * k, fill=255)
    return m.resize(size, Image.LANCZOS)


def glow_layer(draw_fn, blur, boost=1.0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(lay))
    g = lay.filter(ImageFilter.GaussianBlur(blur))
    if boost != 1.0:
        g.putalpha(g.getchannel("A").point(lambda v: min(255, int(v * boost))))
    return g


def vgrad(size, c1, c2):
    w, h = size
    g = Image.new("RGBA", size)
    px = g.load()
    for y in range(h):
        t = y / max(1, h - 1)
        col = tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(len(c1)))
        for x in range(w):
            px[x, y] = col
    return g


# ───────────────────────── iconos ─────────────────────────
BADGES = {  # clave: (color, texto, color texto)
    "ZEC": ((244, 183, 40), "Z", WHITE),
    "NDX": ((0, 128, 204), "N", WHITE),
    "AAPL": ((38, 38, 44), "A", WHITE),
    "AMZN": ((255, 153, 0), "a", (20, 20, 20)),
    "NVDA": ((118, 185, 0), "N", WHITE),
    "INTC": ((0, 113, 197), "i", WHITE),
    "AMD": ((20, 22, 24), "AMD", WHITE),
    "ANT": ((217, 119, 87), "A", WHITE),
    "SPCX": ((18, 20, 24), "X", WHITE),
    "GOOGL": ((66, 133, 244), "G", WHITE),
    "MSFT": ((0, 120, 212), "M", WHITE),
    "LIT": ((38, 38, 44), "L", (52, 245, 176)),
}


def make_icon(key, size):
    path = os.path.join(HERE, "assets", "icons", f"{key}.png")
    if os.path.exists(path):  # un PNG propio en assets/icons/ siempre manda
        return Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
    if key not in BADGES:
        raise StoryError(f"falta el icono de {key}")
    col, txt, tcol = BADGES[key]
    k = 4
    S = size * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, S - 1, S - 1), fill=col + (255,))
    hi = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(hi).ellipse((S * 0.08, S * 0.04, S * 0.92, S * 0.55), fill=(255, 255, 255, 38))
    im = Image.alpha_composite(im, hi)
    d = ImageDraw.Draw(im)
    d.ellipse((k, k, S - 1 - k, S - 1 - k), outline=(255, 255, 255, 70), width=3 * k)
    fs = int(S * (0.34 if len(txt) > 1 else 0.56))
    f = font(F_INTER, fs)
    bb = d.textbbox((0, 0), txt, font=f)
    d.text(((S - (bb[2] - bb[0])) / 2 - bb[0], (S - (bb[3] - bb[1])) / 2 - bb[1]), txt, font=f, fill=tcol)
    return im.resize((size, size), Image.LANCZOS)


# ───────────────────────── validación ─────────────────────────
def load_data(path, filas, modo, now):
    try:
        with open(path, encoding="utf-8") as fh:
            raw = json.load(fh)
    except Exception as e:
        raise StoryError(f"no se puede leer {path}: {e}")
    if not isinstance(raw, dict):
        raise StoryError("data.json debe ser un objeto JSON")
    cap = raw.get("capturado")
    if not cap:  # sin "capturado": vale la hora a la que se escribió data.json
        cap = dt.datetime.fromtimestamp(os.path.getmtime(path), dt.timezone.utc).isoformat()
    try:
        cdt = dt.datetime.fromisoformat(str(cap).replace("Z", "+00:00"))
        if cdt.tzinfo is None:
            raise ValueError("sin zona horaria")
    except Exception as e:
        raise StoryError(f'"capturado" no es una fecha ISO con zona horaria: {e}')
    edad = (dt.datetime.now(dt.timezone.utc) - cdt.astimezone(dt.timezone.utc)).total_seconds() / 60
    if edad > 45:
        raise StoryError(f"los datos tienen {edad:.0f} min: son antiguos, hay que volver a leerlos")
    if edad < -5:
        raise StoryError('"capturado" está en el futuro')

    rows, seen = [], {}
    for key, ticker, sub, pmin, pmax, cmax in filas:
        if key not in raw:
            raise StoryError(f"falta {key} en data.json")
        v = raw[key]
        try:
            p = float(v["price"])
            c = float(v["change"])
        except Exception:
            raise StoryError(f"{key}: hace falta price y change numéricos")
        if not (math.isfinite(p) and math.isfinite(c)):
            raise StoryError(f"{key}: valores no finitos")
        if not (pmin <= p <= pmax):
            raise StoryError(f"{key}: precio {p} fuera de rango razonable ({pmin}-{pmax}); posible lectura errónea")
        if abs(c) > cmax:
            raise StoryError(f"{key}: variación {c}% fuera de rango razonable (±{cmax}%); posible lectura errónea")
        ct = v.get("change_text")
        if ct is not None:
            t = str(ct).replace("−", "-").replace("%", "").strip()
            try:
                tv = float(t.replace("+", ""))
            except ValueError:
                raise StoryError(f"{key}: change_text '{ct}' no es un porcentaje")
            neg_t = t.startswith("-") and tv != 0
            neg_c = c < 0
            if (tv != 0 or c != 0) and (neg_t != neg_c or abs(abs(tv) - abs(c)) > 0.011):
                raise StoryError(f"{key}: el signo/valor de change ({c}) no coincide con el texto de la web ({ct})")
        sig = (round(p, 4), round(c, 4))
        if sig in seen:
            raise StoryError(f"{key} y {seen[sig]} tienen exactamente el mismo precio y variación: lectura duplicada")
        seen[sig] = key
        rows.append((key, ticker, sub, p, c))
    fng = None
    if modo == "cripto":
        f = raw.get("FNG")
        if isinstance(f, dict):
            f = f.get("value")
        try:
            fng = int(round(float(f)))
        except Exception:
            raise StoryError("falta FNG (Fear & Greed, número 0-100)")
        if not 0 <= fng <= 100:
            raise StoryError(f"FNG {fng} fuera de 0-100")
    return rows, fng


# ───────────────────────── dibujo ─────────────────────────
def draw_header(img, fecha):
    d = ImageDraw.Draw(img)
    logo = Image.open(os.path.join(HERE, "assets", "logo_alpha_wordmark.png")).convert("RGBA")
    lw = 460
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    img.alpha_composite(logo, (58, 62))
    d.line((560, 92, 560, 168), fill=(52, 245, 176, 110), width=3)
    # píldora de fecha
    pill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill)
    pd.rounded_rectangle((590, 86, 1012, 174), radius=30, fill=(0, 0, 0, 120), outline=(52, 245, 176, 40), width=2)
    img.alpha_composite(pill)
    # icono calendario
    cx, cy = 632, 130
    d.rounded_rectangle((cx - 20, cy - 18, cx + 20, cy + 20), radius=6, outline=MINT, width=4)
    d.line((cx - 20, cy - 6, cx + 20, cy - 6), fill=MINT, width=4)
    for dx in (-10, 0, 10):
        d.line((cx + dx, cy - 24, cx + dx, cy - 14), fill=MINT, width=4)
    for ry in (4, 13):
        for rx in (-11, -2, 7):
            d.rectangle((cx + rx, cy + ry - 1, cx + rx + 4, cy + ry + 3), fill=MINT)
    f = font(F_XBOLD, 44)
    d.text((676, 130), fecha, font=f, fill=WHITE, anchor="lm")


def draw_title(img, l1, l2):
    d = ImageDraw.Draw(img)
    # línea 1: blanca, ajustada al ancho
    size = 168
    while size > 80:
        f1 = font(F_XBOLD, size)
        if text_w(d, l1, f1) <= 900:
            break
        size -= 4
    f1 = font(F_XBOLD, size)
    cy1 = 305
    sh = glow_layer(lambda g: g.text((W / 2, cy1 + 8), l1, font=f1, fill=(0, 0, 0, 200), anchor="mm"), 10)
    img.alpha_composite(sh)
    d = ImageDraw.Draw(img)
    d.text((W / 2, cy1), l1, font=f1, fill=WHITE, anchor="mm")
    # línea 2: menta en cursiva con degradado y resplandor
    f2 = font(F_BLACK_IT, 215)
    cy2 = 470
    g = glow_layer(lambda gg: gg.text((W / 2, cy2), l2, font=f2, fill=(52, 245, 176, 255), anchor="mm"), 20, 1.5)
    img.alpha_composite(g)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).text((W / 2, cy2), l2, font=f2, fill=255, anchor="mm")
    bb = mask.getbbox()
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gv = vgrad((W, bb[3] - bb[1]), (80, 255, 190), (14, 175, 110))
    grad.paste(gv, (0, bb[1]))
    img.paste(grad, (0, 0), mask)
    # trazo luminoso bajo el titular
    ln = glow_layer(lambda gg: gg.line((60, 566, 1020, 540), fill=(52, 245, 176, 230), width=4), 6, 1.6)
    img.alpha_composite(ln)


def draw_card(img, y, h, key, ticker, sub, price, change):
    x0, x1 = 36, 1044
    mask = rr_mask((W, H), (x0, y, x1, y + h), 34)
    # resplandor del borde
    bl = glow_layer(lambda g: g.rounded_rectangle((x0, y, x1, y + h), radius=34, outline=(52, 245, 176, 150), width=3), 9, 1.0)
    img.alpha_composite(bl)
    fill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fill.paste(vgrad((W, h), (9, 46, 36, 225), (3, 22, 16, 235)), (0, y))
    fill.putalpha(Image.eval(mask, lambda v: v).point(lambda v: int(v * 0.95)))
    img.alpha_composite(fill)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x0, y, x1, y + h), radius=34, outline=(52, 245, 176, 150), width=2)
    cy = y + h // 2
    # icono
    isz = int(h * 0.66)
    ic = make_icon(key, isz)
    img.alpha_composite(ic, (110 - isz // 2, cy - isz // 2))
    d = ImageDraw.Draw(img)
    d.line((184, cy - 34, 184, cy + 34), fill=(52, 245, 176, 120), width=2)
    # ticker y subtítulo
    ft = font(F_INTER, 48 if len(ticker) <= 5 else 44)
    fs = font(F_INTER, 24)
    d.text((206, cy - 14), ticker, font=ft, fill=WHITE, anchor="ls" if False else "lm")
    d.text((207, cy + 28), sub, font=fs, fill=GREY, anchor="lm")
    # precio y variación
    col = GREEN if round(change, 2) > 0 else RED if round(change, 2) < 0 else (210, 225, 220)
    fp = font(F_INTER, 54)
    d.text((752, cy), fmt_price(key, price), font=fp, fill=WHITE, anchor="rm")
    d.line((774, cy - 34, 774, cy + 34), fill=(52, 245, 176, 120), width=2)
    d.text((1008, cy), fmt_change(change), font=fp, fill=col, anchor="rm")


def paste_feather(img, src_path, box, flip=False):
    """Pega oso/toro (fondo oscuro) con bordes difuminados para fundirlos con la tarjeta."""
    x, y, w, h = box
    s = Image.open(src_path).convert("RGB").resize((w, h), Image.LANCZOS)
    if flip:
        s = s.transpose(Image.FLIP_LEFT_RIGHT)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).ellipse((int(w * 0.06), int(h * 0.06), int(w * 0.94), int(h * 0.94)), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(min(w, h) * 0.12))
    lay = s.convert("RGBA")
    lay.putalpha(m)
    img.alpha_composite(lay, (x, y))


def fng_label(v):
    if v <= 24:
        return "MIEDO EXTREMO", (255, 72, 72)
    if v <= 44:
        return "MIEDO", (255, 128, 50)
    if v <= 55:
        return "NEUTRAL", (235, 200, 40)
    if v <= 74:
        return "CODICIA", (60, 215, 110)
    return "CODICIA EXTREMA", (30, 225, 120)


def draw_fng(img, y, h, v):
    x0, x1 = 36, 1044
    bl = glow_layer(lambda g: g.rounded_rectangle((x0, y, x1, y + h), radius=34, outline=(52, 245, 176, 130), width=3), 9, 1.0)
    img.alpha_composite(bl)
    mask = rr_mask((W, H), (x0, y, x1, y + h), 34)
    fill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fill.paste(vgrad((W, h), (8, 42, 33, 230), (3, 20, 15, 238)), (0, y))
    fill.putalpha(mask.point(lambda a: int(a * 0.95)))
    img.alpha_composite(fill)
    paste_feather(img, os.path.join(HERE, "assets", "oso.png"), (44, y + 70, 215, 188))
    paste_feather(img, os.path.join(HERE, "assets", "toro.png"), (822, y + 62, 216, 192))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x0, y, x1, y + h), radius=34, outline=(52, 245, 176, 130), width=2)
    d.text((W / 2, y + 46), "FEAR & GREED INDEX", font=font(F_INTER, 40), fill=WHITE, anchor="mm")
    # número grande + /100
    fb = font(F_XBOLD, 176)
    fsm = font(F_XBOLD, 78)
    s = str(v)
    wn = text_w(d, s, fb)
    wd = text_w(d, "/100", fsm)
    x = (W - (wn + wd)) / 2
    base = y + 232
    d.text((x, base), s, font=fb, fill=WHITE, anchor="ls")
    d.text((x + wn, base), "/100", font=fsm, fill=(235, 240, 238), anchor="ls")
    # etiqueta
    lab, col = fng_label(v)
    fl = font(F_BLACK_IT, 46)
    lw = text_w(d, lab, fl) + 110
    py0 = y + 256
    pl = glow_layer(lambda g: g.rounded_rectangle((W / 2 - lw / 2, py0, W / 2 + lw / 2, py0 + 74), radius=37, fill=col + (255,)), 14, 1.0)
    img.alpha_composite(pl)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((W / 2 - lw / 2, py0, W / 2 + lw / 2, py0 + 74), radius=37, fill=col)
    d.text((W / 2, py0 + 37), lab, font=fl, fill=(255, 255, 255), anchor="mm")
    # barra 0-100 con degradado rojo→naranja→amarillo→verde
    bx0, bx1, by = 96, 984, y + h - 52
    stops = [(0, (255, 60, 60)), (0.33, (255, 140, 30)), (0.55, (250, 235, 30)), (1, (30, 235, 90))]

    def colat(t):
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                u = (t - t0) / (t1 - t0)
                return tuple(int(c0[j] * (1 - u) + c1[j] * u) for j in range(3))
        return stops[-1][1]
    bar = Image.new("RGBA", (bx1 - bx0, 16))
    bp = bar.load()
    for xx in range(bar.width):
        c = colat(xx / (bar.width - 1))
        for yy in range(16):
            bp[xx, yy] = c + (255,)
    bm = rr_mask((bar.width, 16), (0, 0, bar.width, 16), 8)
    bar.putalpha(bm)
    img.alpha_composite(bar, (bx0, by - 8))
    mx = bx0 + (bx1 - bx0) * v / 100
    mk = glow_layer(lambda g: g.ellipse((mx - 24, by - 24, mx + 24, by + 24), fill=col + (200,)), 10, 1.0)
    img.alpha_composite(mk)
    d = ImageDraw.Draw(img)
    d.ellipse((mx - 23, by - 23, mx + 23, by + 23), fill=(255, 255, 255))
    d.ellipse((mx - 16, by - 16, mx + 16, by + 16), fill=col)


def draw_footer(img, texto, y):
    d = ImageDraw.Draw(img)
    f = font(F_INTER, 26)
    tw = text_w(d, texto, f)
    d.text((W / 2, y), texto, font=f, fill=(172, 205, 192), anchor="mm")
    d.line((60, y, W / 2 - tw / 2 - 26, y), fill=(52, 245, 176, 150), width=2)
    d.line((W / 2 + tw / 2 + 26, y, W - 60, y), fill=(52, 245, 176, 150), width=2)


def build(modo, data_path, out_path, hora, fecha_iso=None):
    now = madrid_now()
    if fecha_iso:
        try:
            fecha = dt.date.fromisoformat(fecha_iso)
        except ValueError:
            raise StoryError(f"fecha inválida: {fecha_iso}")
    else:
        fecha = now.date()
    try:
        hh, mm = hora.split(":")
        int(hh), int(mm)
    except Exception:
        raise StoryError(f"hora inválida '{hora}' (usa HH:MM)")
    filas = CRIPTO if modo == "cripto" else BOLSA
    rows, fng = load_data(data_path, filas, modo, now)
    fondo = os.path.join(HERE, "assets", "fondo_historia.png")
    if not os.path.exists(fondo):
        raise StoryError("falta assets/fondo_historia.png (ejecuta make_fondo.py)")
    img = Image.open(fondo).convert("RGBA")
    if img.size != (W, H):
        raise StoryError(f"el fondo mide {img.size}, debe ser {W}x{H}")
    fecha_txt = f"{fecha.day} {MESES[fecha.month - 1]} {fecha.year}"
    draw_header(img, fecha_txt)
    if modo == "cripto":
        draw_title(img, "CRIPTO", "HOY")
        h, gap, y0 = 124, 12, 574
    else:
        draw_title(img, "WALL STREET", "HOY")
        h, gap, y0 = 124, 12, 574  # 9 filas
    for i, (key, ticker, sub, p, c) in enumerate(rows):
        draw_card(img, y0 + i * (h + gap), h, key, ticker, sub, p, c)
    if modo == "cripto":
        fy = y0 + len(rows) * (h + gap) + 4
        draw_fng(img, fy, 1812 - fy, fng)
        pie = f"Datos consultados: CoinMarketCap · {hora}h Madrid"
    else:
        pie = f"Datos consultados: Investing.com · {hora}h Madrid"
    draw_footer(img, pie, 1866)
    out = img.convert("RGB")
    if out.size != (W, H):
        raise StoryError("la imagen final no mide 1080x1920")
    out.save(out_path, "PNG", optimize=True)
    resumen = ", ".join(f"{k} {fmt_price(k, p)} {fmt_change(c)}" for k, _, _, p, c in rows)
    if fng is not None:
        resumen += f", Fear&Greed {fng}/100 ({fng_label(fng)[0]})"
    print(f"OK {out_path} · {fecha_txt} · {resumen}")


def selftest():
    import tempfile
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    cripto = {"capturado": now, "FNG": 12,
              "BTC": {"price": 62546.1, "change": -0.29}, "HYPE": {"price": 67.73, "change": -1.03},
              "ETH": {"price": 1795.2, "change": -0.71}, "SOL": {"price": 75.1, "change": 1.22},
              "BNB": {"price": 580.97, "change": 0.14}, "LIT": {"price": 3.05, "change": 3.4}}
    bolsa = {"capturado": now,
             "SPX": {"price": 7416.59, "change": -1.92}, "NDX": {"price": 24980.1, "change": -2.3},
             "ANT": {"price": 95.05, "change": 4.2}, "SPCX": {"price": 210.4, "change": -1.8},
             "AMZN": {"price": 231.7, "change": -1.1}, "GOOGL": {"price": 301.2, "change": 0.9},
             "AAPL": {"price": 268.4, "change": 0.45}, "NVDA": {"price": 192.3, "change": 2.35},
             "MSFT": {"price": 481.6, "change": -0.35}}
    with tempfile.TemporaryDirectory() as td:
        for modo, dat in (("cripto", cripto), ("bolsa", bolsa)):
            jp = os.path.join(td, f"{modo}.json")
            with open(jp, "w") as fh:
                json.dump(dat, fh)
            build(modo, jp, os.path.join(td, f"{modo}.png"), "21:20")
        # casos que DEBEN fallar
        malos = [
            ("capturado antiguo", lambda d: d.__setitem__("capturado", "2020-01-01T00:00:00+00:00")),
            ("falta SOL", lambda d: d.pop("SOL")),
            ("signo distinto", lambda d: d["BTC"].update(change_text="+0.29%")),
            ("precio absurdo", lambda d: d["BTC"].update(price=5)),
            ("duplicado", lambda d: d["ETH"].update(price=62546.1, change=-0.29)),
            ("FNG fuera de rango", lambda d: d.__setitem__("FNG", 140)),
        ]
        for nombre, mut in malos:
            d = json.loads(json.dumps(cripto))
            mut(d)
            jp = os.path.join(td, "malo.json")
            with open(jp, "w") as fh:
                json.dump(d, fh)
            try:
                build("cripto", jp, os.path.join(td, "malo.png"), "21:20")
            except StoryError:
                continue
            raise SystemExit(f"SELFTEST FALLA: '{nombre}' debería haber dado ERROR")
        # sin "capturado" y con el archivo viejo (mtime antiguo) también debe fallar
        d = json.loads(json.dumps(cripto)); d.pop("capturado")
        jp = os.path.join(td, "viejo.json")
        with open(jp, "w") as fh:
            json.dump(d, fh)
        os.utime(jp, (1600000000, 1600000000))
        try:
            build("cripto", jp, os.path.join(td, "viejo.png"), "21:20")
        except StoryError:
            pass
        else:
            raise SystemExit("SELFTEST FALLA: data.json antiguo sin 'capturado' debería dar ERROR")
    print("SELFTEST OK")


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        selftest()
        return 0
    if len(argv) not in (5, 6) or argv[1] not in ("cripto", "bolsa"):
        print(__doc__)
        return 2
    try:
        build(argv[1], argv[2], argv[3], argv[4], argv[5] if len(argv) == 6 else None)
    except StoryError as e:
        print(f"ERROR: {e}")
        return 1
    except Exception as e:  # cualquier fallo inesperado = no publicar
        print(f"ERROR: fallo inesperado ({type(e).__name__}: {e})")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
