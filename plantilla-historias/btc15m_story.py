#!/usr/bin/env python3
"""ALPHA MARKETS · historia "BITCOIN 15 MIN" (gráfica de velas de 15 min con el precio de antes y el de ahora).

Uso:
    python3 btc15m_story.py chart.json historia.png HH:MM [horas=6] [ref=HH:MM]

chart.json (lo escribe la rutina con el JS de PROCEDIMIENTO.md, sección 6, desde coinmarketcap.com):
    {"pts": [[1795562400, 59926.33], [1795562700, 59931.1], ...],   # [timestamp UNIX s, precio USD], cada 5 min
     "capturado": "2026-11-26T09:10:05+01:00"}
    (también vale {"points": {"1795562400": 59926.33, ...}})

horas : ventana de la gráfica (por defecto 6 h; 3-12).
ref   : hora de Madrid (HH:MM) a comparar con el precio de ahora. Por defecto, el inicio de la ventana.

Si algo no cuadra imprime "ERROR: ..." y sale con código 1: en ese caso NO se publica nada.
Reutiliza el estilo, fondo, fuentes y cabecera de build_story.py (misma carpeta).
"""
import datetime as dt
import json
import math
import os
import sys

from PIL import Image, ImageDraw

import build_story as bs
from build_story import (F_BLACK_IT, F_INTER, F_XBOLD, GREEN, GREY, H, MINT, RED, W, WHITE, StoryError,
                         draw_footer, draw_header, draw_title, font, glow_layer, madrid_now, rr_mask,
                         text_w, vgrad)

MAD = None


def tz():
    global MAD
    if MAD is None:
        try:
            from zoneinfo import ZoneInfo
            MAD = ZoneInfo("Europe/Madrid")
        except Exception:
            MAD = madrid_now().tzinfo
    return MAD


def money(p):
    return f"${p:,.0f}" if p >= 1000 else f"${p:,.2f}" if p >= 1 else f"${p:,.4f}"


def pct(c):
    r = round(c, 2)
    return "0.00%" if r == 0 else f"{r:+.2f}%"


def load_points(path, pmin=1e3, pmax=1e7, asset="BTC"):
    try:
        raw = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        raise StoryError(f"no se puede leer {path}: {e}")
    pts = raw.get("pts")
    if pts is None and isinstance(raw.get("points"), dict):
        pts = [[int(k), float(v if not isinstance(v, dict) else v.get("v", [None])[0])] for k, v in raw["points"].items()]
    if not pts or len(pts) < 60:
        raise StoryError("faltan puntos de precio (se esperan ~288, uno cada 5 min)")
    pts = sorted((int(t), float(p)) for t, p in pts)
    cap = raw.get("capturado")
    if not cap:
        cap = dt.datetime.fromtimestamp(os.path.getmtime(path), dt.timezone.utc).isoformat()
    try:
        cdt = dt.datetime.fromisoformat(str(cap).replace("Z", "+00:00"))
        if cdt.tzinfo is None:
            raise ValueError("sin zona horaria")
    except Exception as e:
        raise StoryError(f'"capturado" no es una fecha ISO con zona horaria: {e}')
    now = dt.datetime.now(dt.timezone.utc)
    if (now - cdt.astimezone(dt.timezone.utc)).total_seconds() / 60 > 30:
        raise StoryError("los datos tienen más de 30 min: hay que volver a leerlos")
    last_t = dt.datetime.fromtimestamp(pts[-1][0], dt.timezone.utc)
    if (now - last_t).total_seconds() / 60 > 30:
        raise StoryError(f"el último punto de precio tiene {(now - last_t).total_seconds() / 60:.0f} min: datos antiguos")
    for _, p in pts:
        if not (math.isfinite(p) and pmin <= p <= pmax):
            raise StoryError(f"precio {p} fuera de rango razonable para {asset}")
    return pts


def candles15(pts, horas):
    """Velas OHLC de 15 min (hora de Madrid) de las últimas `horas` horas."""
    t_end = pts[-1][0]
    t_start = t_end - horas * 3600
    buckets = {}
    for t, p in pts:
        if t < t_start:
            continue
        b = t - (t % 900)
        buckets.setdefault(b, []).append(p)
    out = []
    for b in sorted(buckets):
        v = buckets[b]
        out.append((b, v[0], max(v), min(v), v[-1]))
    return out


def card(img, x0, y0, x1, y1, outline=(52, 245, 176, 150)):
    h = y1 - y0
    bl = glow_layer(lambda g: g.rounded_rectangle((x0, y0, x1, y1), radius=34, outline=outline, width=3), 9, 1.0)
    img.alpha_composite(bl)
    mask = rr_mask((W, H), (x0, y0, x1, y1), 34)
    fill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fill.paste(vgrad((W, h), (9, 46, 36, 225), (3, 22, 16, 235)), (0, y0))
    fill.putalpha(mask.point(lambda v: int(v * 0.95)))
    img.alpha_composite(fill)
    ImageDraw.Draw(img).rounded_rectangle((x0, y0, x1, y1), radius=34, outline=outline, width=2)


def stat(img, x0, y0, x1, y1, titulo, valor, color=WHITE, sub=None):
    card(img, x0, y0, x1, y1)
    d = ImageDraw.Draw(img)
    cx = (x0 + x1) / 2
    d.text((cx, y0 + 38), titulo, font=font(F_INTER, 25), fill=GREY, anchor="mm")
    size = 60
    while size > 30 and text_w(d, valor, font(F_INTER, size)) > (x1 - x0) - 36:
        size -= 2
    d.text((cx, y0 + (y1 - y0) // 2 + 14), valor, font=font(F_INTER, size), fill=color, anchor="mm")
    if sub:
        d.text((cx, y1 - 26), sub, font=font(F_INTER, 22), fill=GREY, anchor="mm")


def build(chart_path, out_path, hora, horas=6.0, ref=None, activo="BITCOIN", sim="BTC", fuente="CoinMarketCap", pmin=1e3, pmax=1e7):
    now = madrid_now()
    if not 3 <= horas <= 12:
        raise StoryError("horas debe estar entre 3 y 12")
    pts = load_points(chart_path, pmin, pmax, sim)
    cs = candles15(pts, horas)
    if len(cs) < int(horas * 4 * 0.7):
        raise StoryError(f"solo {len(cs)} velas de 15 min: datos incompletos")
    t_last = pts[-1][0]
    p_now = pts[-1][1]
    # precio de referencia
    if ref:
        try:
            hh, mm = ref.split(":")
            rd = now.replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)
        except Exception:
            raise StoryError(f"ref inválida '{ref}' (usa HH:MM)")
        if rd > now:
            rd -= dt.timedelta(days=1)
        t_ref = int(rd.timestamp())
    else:
        t_ref = cs[0][0]
    t_ref = max(t_ref, cs[0][0])
    ref_pt = min(pts, key=lambda tp: abs(tp[0] - t_ref))
    if abs(ref_pt[0] - t_ref) > 900:
        raise StoryError("no hay precio cercano a la hora de referencia")
    p_ref = ref_pt[1]
    ref_dt = dt.datetime.fromtimestamp(ref_pt[0], tz())
    ref_txt = ref_dt.strftime("%H:%M")
    chg = (p_now / p_ref - 1) * 100
    p24 = pts[0][1] if (t_last - pts[0][0]) >= 22 * 3600 else None
    c24 = (p_now / p24 - 1) * 100 if p24 else None
    hi = max(c[2] for c in cs)
    lo = min(c[3] for c in cs)

    fondo = os.path.join(bs.HERE, "assets", "fondo_historia.png")
    img = Image.open(fondo).convert("RGBA")
    fecha = now.date()
    draw_header(img, f"{fecha.day} {bs.MESES[fecha.month - 1]} {fecha.year}")
    draw_title(img, activo, "15 MIN")

    # ── tarjeta de la gráfica ──
    cx0, cy0, cx1, cy1 = 36, 574, 1044, 1236
    card(img, cx0, cy0, cx1, cy1)
    d = ImageDraw.Draw(img)
    d.text((72, cy0 + 40), f"{sim} · VELAS DE 15 MIN", font=font(F_INTER, 28), fill=WHITE, anchor="lm")
    d.text((1008, cy0 + 40), f"ÚLTIMAS {horas:g} H", font=font(F_INTER, 26), fill=GREY, anchor="rm")
    px0, px1 = 84, 900
    py0, py1 = cy0 + 96, cy1 - 70
    vmin, vmax = lo, hi
    pad = (vmax - vmin) * 0.12 or vmax * 0.002
    vmin -= pad
    vmax += pad

    def Y(v):
        return py1 - (v - vmin) / (vmax - vmin) * (py1 - py0)
    t0, t1 = cs[0][0], cs[-1][0] + 900

    def X(t):
        return px0 + (t - t0) / (t1 - t0) * (px1 - px0)
    # rejilla + etiquetas de precio
    for i in range(5):
        v = vmin + (vmax - vmin) * i / 4
        y = Y(v)
        d.line((px0, y, px1 + 8, y), fill=(52, 245, 176, 38), width=1)
        d.text((1014, y), money(v), font=font(F_INTER, 22), fill=GREY, anchor="rm")
    # etiquetas de hora (cada hora en punto)
    tt = t0 - (t0 % 3600) + 3600
    while tt < t1:
        x = X(tt)
        d.line((x, py0, x, py1), fill=(52, 245, 176, 24), width=1)
        d.text((x, py1 + 30), dt.datetime.fromtimestamp(tt, tz()).strftime("%H:%M"), font=font(F_INTER, 22),
               fill=GREY, anchor="mm")
        tt += 3600 * (2 if horas > 7 else 1)
    # línea de referencia (precio de antes) y velas
    xr = X(ref_pt[0])
    d.line((xr, py0 - 6, xr, py1), fill=(255, 255, 255, 120), width=2)
    cw = max(4, int((px1 - px0) / len(cs) * 0.62))
    for (b, o, h_, l_, c_) in cs:
        col = GREEN if c_ >= o else RED
        x = X(b + 450)
        d.line((x, Y(h_), x, Y(l_)), fill=col, width=3)
        y_a, y_b = sorted((Y(o), Y(c_)))
        if y_b - y_a < 3:
            y_b = y_a + 3
        d.rectangle((x - cw / 2, y_a, x + cw / 2, y_b), fill=col)
    # marcador del precio de ahora
    colnow = GREEN if chg >= 0 else RED
    yn = Y(p_now)
    d.line((px0, yn, px1, yn), fill=colnow + (200,), width=2)
    tag = money(p_now)
    ft = font(F_INTER, 26)
    tw = text_w(d, tag, ft) + 26
    d.rounded_rectangle((px1 + 6, yn - 20, px1 + 6 + tw, yn + 20), radius=12, fill=colnow)
    d.text((px1 + 6 + tw / 2, yn), tag, font=ft, fill=(8, 22, 18), anchor="mm")
    # punto y etiqueta del precio de referencia
    yr = Y(p_ref)
    d.ellipse((xr - 11, yr - 11, xr + 11, yr + 11), fill=WHITE, outline=MINT, width=4)
    lab = f"{ref_txt} · {money(p_ref)}"
    fl = font(F_INTER, 26)
    lw = text_w(d, lab, fl) + 30
    lx = min(max(xr - lw / 2, px0), px1 - lw)
    ly = py0 - 2 if yr > (py0 + py1) / 2 else py1 - 52
    d.rounded_rectangle((lx, ly, lx + lw, ly + 42), radius=14, fill=(0, 0, 0, 190), outline=(255, 255, 255, 150), width=2)
    d.text((lx + lw / 2, ly + 21), lab, font=fl, fill=WHITE, anchor="mm")

    # ── tarjetas de datos ──
    gap = 16
    cwid = (1008 - 2 * gap) / 3
    xs = [36 + i * (cwid + gap) for i in range(3)]
    r1y0, r1y1 = 1262, 1432
    stat(img, xs[0], r1y0, xs[0] + cwid, r1y1, f"A LAS {ref_txt}", money(p_ref))
    stat(img, xs[1], r1y0, xs[1] + cwid, r1y1, f"AHORA ({hora})", money(p_now))
    stat(img, xs[2], r1y0, xs[2] + cwid, r1y1, "VARIACIÓN", pct(chg), color=colnow)
    r2y0, r2y1 = r1y1 + gap, r1y1 + gap + 170
    stat(img, xs[0], r2y0, xs[0] + cwid, r2y1, f"MÁXIMO {horas:g} H", money(hi))
    stat(img, xs[1], r2y0, xs[1] + cwid, r2y1, f"MÍNIMO {horas:g} H", money(lo))
    if c24 is not None:
        stat(img, xs[2], r2y0, xs[2] + cwid, r2y1, "CAMBIO 24 H", pct(c24), color=GREEN if c24 >= 0 else RED)
    else:
        stat(img, xs[2], r2y0, xs[2] + cwid, r2y1, "RANGO", money(hi - lo))
    # frase resumen
    fy0, fy1 = r2y1 + gap, 1812
    card(img, 36, fy0, 1044, fy1, outline=colnow + (170,))
    d = ImageDraw.Draw(img)
    verbo = "SUBE" if chg > 0.005 else "BAJA" if chg < -0.005 else "SE MANTIENE"
    frase = f"{sim} {verbo} {abs(round(chg, 2)):.2f} % DESDE LAS {ref_txt}" if verbo != "SE MANTIENE" else f"{sim} SE MANTIENE DESDE LAS {ref_txt}"
    size = 54
    while size > 30 and text_w(d, frase, font(F_BLACK_IT, size)) > 940:
        size -= 2
    d.text((W / 2, (fy0 + fy1) / 2), frase, font=font(F_BLACK_IT, size), fill=colnow, anchor="mm")
    draw_footer(img, f"Datos consultados: {fuente} · {hora}h Madrid", 1866)
    out = img.convert("RGB")
    if out.size != (W, H):
        raise StoryError("la imagen final no mide 1080x1920")
    out.save(out_path, "PNG", optimize=True)
    print(f"OK {out_path} · {sim} {money(p_ref)} a las {ref_txt} → {money(p_now)} ahora ({pct(chg)}) · máx {money(hi)} mín {money(lo)}"
          + (f" · 24h {pct(c24)}" if c24 is not None else ""))


def main(argv):
    if len(argv) not in (4, 5, 6):
        print(__doc__)
        return 2
    try:
        horas = float(argv[4]) if len(argv) >= 5 else 6.0
        ref = argv[5] if len(argv) == 6 else None
        build(argv[1], argv[2], argv[3], horas, ref)
    except StoryError as e:
        print(f"ERROR: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: fallo inesperado ({type(e).__name__}: {e})")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
