#!/usr/bin/env python3
"""HISTORIAS v27 · 10 DISEÑOS RADICALMENTE DISTINTOS (cada historia del día se ve completamente diferente a la anterior).
uso: python3 historias/estilos/make_story_estilos.py datos.json salida.png [--estilo N|nombre|auto] [--hueco K]
  datos.json = UNA historia: {"t1":"BITCOIN","t2":"BAJO 62K","sub":"Primera vez desde <b>JULIO</b> · 20 NOV",
                "rows":[{"n":"PRECIO","s":"BTC · HOY","p":"$61,974","c":"-1.93%","cc":"r"}, ...],   # 2-6 filas (cc: r rojo / v verde)
                "tag":"ÚLTIMA HORA" (opcional), "logo":"btc|eth|ant|hl|sol|none" (opcional), "fuente":"CoinDesk · Cointelegraph"}
  --estilo auto (por defecto): elige el diseño por el nº de hueco del día (--hueco K, 1-10) usando ORDEN, que alterna estilos
                 de familias opuestas (oscuro/claro, texto/gráfico, tipografía serif/mono/display) → NUNCA dos parecidos seguidos.
  --lista: imprime los diseños.
Estilos: alerta, gigante, terminal, periodico, chat, cartel, grafica, stickers, versus, lockscreen."""
import json, os, re, sys, html, base64, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]          # plantilla_alpha_markets
E = html.escape
ESTILOS = ['alerta', 'gigante', 'terminal', 'periodico', 'chat', 'cartel', 'grafica', 'stickers', 'versus', 'lockscreen']
# orden de rotación: cada par consecutivo cambia de familia (oscuro→claro→mono→serif→…); el hueco K usa ORDEN[(K-1) % 10]
ORDEN = ['alerta', 'periodico', 'terminal', 'stickers', 'grafica', 'gigante', 'chat', 'cartel', 'lockscreen', 'versus']

FONTS = """@font-face{font-family:Mont;src:url(../../fonts/montserrat-latin-wght-normal.woff2);font-weight:100 900}
@font-face{font-family:Mont;src:url(../../fonts/montserrat-latin-wght-italic.woff2);font-weight:100 900;font-style:italic}
@font-face{font-family:Anton;src:url(../../fonts/anton-latin-400-normal.woff2)}
@font-face{font-family:Inter;src:url(../../fonts/inter-latin-wght-normal.woff2);font-weight:100 900}
@font-face{font-family:Marker;src:url(../../fonts/permanent-marker-latin-400-normal.woff2)}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1920px;overflow:hidden}"""
LOGO = '../../img/logo_alpha_wordmark.png'
AV = '../../img/avatar.jpg'
BTC = (ROOT / 'img/logos/bitcoin.svg').read_text(encoding='utf-8')
BTCD = re.search(r'<path d="([^"]+)"', BTC).group(1)

def coin(sym, size, c1='#FFB347'):
    if sym in ('btc', None, ''):
        return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}"><circle cx="12" cy="12" r="12" fill="#F7931A"/><path fill="#fff" transform="translate(4 4) scale(.66)" d="{BTCD}"/></svg>'
    if sym == 'eth':
        return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}"><circle cx="12" cy="12" r="12" fill="#627EEA"/><path fill="#fff" d="M12 4l-4.5 7.4L12 14zM12 4l4.5 7.4L12 14zM12 15l-4.5-2.6L12 20zM12 15l4.5-2.6L12 20z"/></svg>'
    if sym == 'sol':
        return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}"><circle cx="12" cy="12" r="12" fill="#14151c"/><path fill="#14F195" d="M6 7.5h12l-2 2.4H4zM6 11h12l-2 2.4H4zM6 14.6h12l-2 2.4H4z"/></svg>'
    return ''

def up(d):
    rs = d.get('rows', [])
    r = sum(1 for x in rs if x.get('cc') == 'r'); v = sum(1 for x in rs if x.get('cc') != 'r')
    return d.get('dir') != 'down' and v >= r if 'dir' not in d else d['dir'] == 'up'

def rows(d, n=6): return d.get('rows', [])[:n]
def big(d):
    rs = rows(d); r0 = rs[0] if rs else {}
    return (r0.get('c') or r0.get('p') or ''), (r0.get('p') or ''), r0
def head(d): return E(re.sub('<[^>]+>', '', d.get('t1', ''))), E(re.sub('<[^>]+>', '', d.get('t2', '')))
def sub(d): return d.get('sub', '')   # puede llevar <b>
def fuente(d): return E(d.get('fuente') or 'Fuente: datos de mercado en directo')
def F(t, base, mc=9): return int(base*min(1, mc/max(1, len(t))))
def col(cc): return '#FF3B48' if cc == 'r' else '#34F5B0'

# ---------- 1. ALERTA: pantalla de última hora, rojo/negro, bandas de peligro ----------
def alerta(d):
    t1, t2 = head(d); c, p, r0 = big(d); R = rows(d, 4)
    items = ''.join(f'<div class="it"><b>{E(x["n"])}</b><span>{E(x.get("s",""))}</span><i style="color:{col(x.get("cc"))}">{E(x.get("p") or x.get("c",""))}</i></div>' for x in R)
    return f"""<style>body{{background:#0a0204;font-family:Mont}}
.bg{{position:absolute;inset:0;background:radial-gradient(circle at 50% 35%,#6a0a14,#1a0207 60%,#050001)}}
.hz{{position:absolute;left:0;right:0;height:96px;background:repeating-linear-gradient(-45deg,#FF2B3B 0 44px,#120508 44px 88px)}}
.siren{{position:absolute;left:50%;top:150px;width:900px;height:900px;margin-left:-450px;background:conic-gradient(from 0deg,rgba(255,40,60,.5),transparent 20%,transparent 50%,rgba(255,40,60,.5) 50%,transparent 70%);border-radius:50%;filter:blur(30px)}}
.tag{{position:absolute;left:60px;top:270px;background:#FF2B3B;color:#fff;font-weight:900;font-size:50px;padding:14px 36px;letter-spacing:.08em;box-shadow:0 0 50px #FF2B3B}}
.h1{{white-space:nowrap;position:absolute;left:50px;right:50px;top:420px;font-family:Anton;font-size:{F(t1,250,9)}px;line-height:.95;color:#fff;text-transform:uppercase;text-shadow:0 0 60px rgba(255,40,60,.7)}}
.h2{{white-space:nowrap;position:absolute;left:50px;right:50px;top:690px;font-family:Anton;font-size:{F(t2,215,8)}px;line-height:.95;color:#FF3B48;text-transform:uppercase;text-shadow:0 0 50px rgba(255,40,60,.8)}}
.sub{{position:absolute;left:56px;right:56px;top:1000px;font-weight:800;font-size:44px;color:#ffd6d9;line-height:1.25}}.sub b{{color:#fff;background:#FF2B3B;padding:0 12px}}
.list{{position:absolute;left:50px;right:50px;top:1160px}}.it{{display:flex;align-items:baseline;gap:18px;border-bottom:3px solid rgba(255,60,80,.45);padding:16px 0}}.it b{{font-size:44px;font-weight:900;color:#fff}}.it span{{flex:1;font-size:26px;color:#c99;font-weight:700}}.it i{{font-style:normal;font-size:58px;font-family:Anton}}
.logo{{position:absolute;right:50px;top:272px;height:78px}}.src{{position:absolute;left:50px;right:50px;bottom:200px;font-size:24px;color:#c99;font-weight:700}}</style>
<div class=bg></div><div class=siren></div><div class=hz style="top:150px"></div><div class=hz style="bottom:150px"></div>
<div class=tag>● {E(d.get('tag') or 'ÚLTIMA HORA')}</div><img class=logo src={LOGO}>
<div class=h1>{t1}</div><div class=h2>{t2}</div><div class=sub>{sub(d)}</div><div class=list>{items}</div><div class=src>{fuente(d)}</div>"""

# ---------- 2. GIGANTE: una sola cifra enorme, fondo plano de color ----------
def gigante(d):
    t1, t2 = head(d); c, p, r0 = big(d); good = up(d)
    bg, fg, ac = ('#C6FF3D', '#0A0F0A', '#0A0F0A') if good else ('#FF3B30', '#FFF', '#FFF')
    txt = re.sub(r'<[^>]+>', '', c or p)
    fs = 430 if len(txt) <= 5 else 330 if len(txt) <= 7 else 250
    lines = ''.join(f'<div class="ln"><span>{E(x["n"])}</span><b>{E(x.get("p") or x.get("c",""))}</b></div>' for x in rows(d, 4)[1:])
    return f"""<style>body{{background:{bg};font-family:Mont;color:{fg}}}
.top{{position:absolute;left:60px;right:60px;top:260px;display:flex;justify-content:space-between;align-items:center}}.pl{{background:{fg};padding:10px 22px;border-radius:16px}}.pl img{{height:56px;display:block}}
.k{{font-weight:900;font-size:46px;letter-spacing:.16em;text-transform:uppercase}}
.num{{position:absolute;left:0;right:0;top:420px;text-align:center;font-family:Anton;font-size:{fs}px;line-height:1;letter-spacing:-.02em;transform:rotate(-4deg)}}
.t{{position:absolute;left:60px;right:60px;top:1000px;font-family:Anton;font-size:150px;line-height:.98;text-transform:uppercase}}
.sub{{position:absolute;left:62px;right:62px;top:1330px;font-weight:800;font-size:40px;line-height:1.25}}.sub b{{background:{fg};color:{bg};padding:0 10px}}
.ln{{position:absolute;display:none}}.src{{position:absolute;left:62px;bottom:200px;font-size:26px;font-weight:800;opacity:.7}}</style>
<div class=top><div class=pl><img src={LOGO}></div><div class=k>{E(d.get('tag') or 'HOY')}</div></div>
<div class=num>{E(txt)}</div><div class=t>{t1}<br>{t2}</div><div class=sub>{sub(d)}</div><div class=src>{fuente(d)}</div>"""

# ---------- 3. TERMINAL: monoespaciada ámbar, tabla ----------
def terminal(d):
    t1, t2 = head(d)
    body = ''.join(f'<tr><td>{E(x["n"])}</td><td class=m>{E(x.get("s",""))}</td><td class=r style="color:{"#ff5a5f" if x.get("cc")=="r" else "#37ff9c"}">{E(x.get("p") or "")}</td><td class=r style="color:{"#ff5a5f" if x.get("cc")=="r" else "#37ff9c"}">{E(x.get("c") or "")}</td></tr>' for x in rows(d))
    return f"""<style>body{{background:#050500;font-family:'Courier New',monospace;color:#FFB000}}
.scan{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.35) 0 3px,transparent 3px 6px);pointer-events:none;z-index:9}}
.glow{{position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,rgba(255,176,0,.14),transparent 70%)}}
.bar{{position:absolute;left:40px;right:40px;top:250px;display:flex;justify-content:space-between;font-size:30px;border:3px solid #FFB000;padding:12px 20px}}
.box{{position:absolute;left:40px;right:40px;top:350px;border:3px solid #FFB000;padding:34px;min-height:1100px}}
.cmd{{font-size:34px;color:#b88400;margin-bottom:24px}}.cmd i{{display:inline-block;width:20px;height:34px;background:#FFB000;vertical-align:-6px}}
h1{{font-size:112px;line-height:1.02;font-weight:900;text-shadow:0 0 22px rgba(255,176,0,.8)}}h2{{font-size:112px;line-height:1.02;font-weight:900;color:#fff;text-shadow:0 0 22px rgba(255,255,255,.5);margin-bottom:26px}}
.sub{{font-size:34px;color:#e8c066;margin:0 0 30px;line-height:1.3}}.sub b{{color:#fff}}
table{{width:100%;border-collapse:collapse;font-size:38px}}td{{padding:16px 6px;border-bottom:2px dashed rgba(255,176,0,.4)}}.m{{font-size:24px;color:#b88400}}.r{{text-align:right;font-weight:900}}
.src{{position:absolute;left:40px;right:40px;bottom:190px;font-size:26px;color:#b88400}}img.lg{{position:absolute;right:60px;top:268px;height:56px;filter:sepia(1) saturate(4) hue-rotate(-10deg) brightness(1.1);z-index:5}}</style>
<div class=glow></div><div class=scan></div>
<div class=bar><span>ALPHA&gt;MARKETS TERMINAL</span><span>{E(d.get('tag') or 'LIVE')} ●</span></div>
<div class=box><div class=cmd>&gt; NEWS --latest --asset {t1.split()[0] if t1 else 'ALL'}<i></i></div><h1>{t1}</h1><h2>{t2}</h2><div class=sub>{sub(d)}</div><table>{body}</table></div>
<div class=src>SRC: {fuente(d)}</div>"""

# ---------- 4. PERIÓDICO: papel crema, serif, columnas ----------
def periodico(d):
    t1, t2 = head(d)
    body = ''.join(f'<div class=ro><b>{E(x["n"])}</b><span>{E(x.get("s",""))}</span><i style="color:{"#b3141f" if x.get("cc")=="r" else "#0b6b3a"}">{E(x.get("p") or "")} {E(x.get("c") or "")}</i></div>' for x in rows(d, 5))
    return f"""<style>body{{background:#ECE4D0;font-family:Georgia,'Times New Roman',serif;color:#16120a}}
.paper{{position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#f4edda,#e2d8bf);}}
.mast{{position:absolute;left:50px;right:50px;top:250px;text-align:center;border-bottom:8px double #16120a;padding-bottom:16px}}.mast h4{{font-size:78px;font-weight:900;letter-spacing:.04em;font-family:Georgia}}.mast p{{display:flex;justify-content:space-between;font-size:24px;margin-top:6px;border-top:2px solid #16120a;padding-top:6px;font-family:Inter;font-weight:700;text-transform:uppercase}}
.h{{position:absolute;left:50px;right:50px;top:470px;font-size:{F(max(t1,t2,key=len),200,9)}px;white-space:nowrap;line-height:.92;font-weight:900;letter-spacing:-.03em;text-transform:uppercase}}.h em{{font-style:italic;color:#b3141f}}
.sub{{position:absolute;left:54px;right:54px;top:960px;font-size:42px;line-height:1.3;font-style:italic;border-top:4px solid #16120a;padding-top:20px}}.sub b{{background:#16120a;color:#ECE4D0;padding:0 8px;font-style:normal}}
.cols{{position:absolute;left:54px;right:54px;top:1160px;border-top:2px solid #16120a}}.ro{{display:flex;gap:16px;align-items:baseline;padding:14px 0;border-bottom:1px solid rgba(0,0,0,.4);font-size:36px}}.ro b{{font-family:Georgia;font-weight:900;min-width:300px}}.ro span{{flex:1;font-family:Inter;font-size:22px;opacity:.7;text-transform:uppercase;font-weight:700}}.ro i{{font-style:normal;font-weight:900;font-size:40px}}
.stamp{{position:absolute;right:70px;top:735px;transform:rotate(9deg);border:7px solid #b3141f;color:#b3141f;font-family:Anton;font-size:60px;padding:6px 22px;opacity:.88}}
.src{{position:absolute;left:54px;right:54px;bottom:200px;font-family:Inter;font-size:24px;font-weight:700;opacity:.7}}</style>
<div class=paper></div>
<div class=mast><h4>EL DIARIO 4LPHA</h4><p><span>Edición especial</span><span>{E(d.get('tag') or 'Mercados')}</span><span>@4lphamarkets</span></p></div>
<div class=h>{t1}<br><em>{t2}</em></div><div class=stamp>{E(d.get('tag') or 'EXCLUSIVA')}</div><div class=sub>{sub(d)}</div><div class=cols>{body}</div><div class=src>{fuente(d)}</div>"""

# ---------- 5. CHAT: conversación tipo móvil con burbujas ----------
def chat(d):
    t1, t2 = head(d); R = rows(d, 3)
    bub = ''.join(f'<div class="b {"l" if i%2==0 else "r"}"><small>{E(x["n"])}</small><span style="color:{col(x.get("cc"))}">{E(x.get("p") or x.get("c") or "")}</span> {E(x.get("c") or "") if x.get("p") else ""}</div>' for i, x in enumerate(R))
    return f"""<style>body{{background:#0F1923;font-family:Inter}}
.hd{{position:absolute;left:0;right:0;top:230px;height:150px;background:#17212B;display:flex;align-items:center;gap:22px;padding:0 40px;border-bottom:2px solid #24303c}}.hd img.a{{width:96px;height:96px;border-radius:50%}}.hd b{{font-size:40px;color:#fff;display:block}}.hd span{{font-size:26px;color:#6DD16F}}
.chat{{position:absolute;left:36px;right:36px;top:430px;display:flex;flex-direction:column;gap:26px}}
.b{{max-width:820px;padding:26px 34px;border-radius:38px;font-size:44px;line-height:1.25;color:#fff;font-weight:600}}.b.l{{background:#2B5278;border-bottom-left-radius:8px;align-self:flex-start}}.b.r{{background:#3A7A4A;border-bottom-right-radius:8px;align-self:flex-end}}.b small{{display:block;font-size:24px;opacity:.7;text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px}}.b span{{font-weight:900;font-size:56px;background:rgba(0,0,0,.28);padding:0 12px;border-radius:12px}}
.big{{font-family:Anton;font-size:{F(max(t1,t2,key=len),128,12)}px;line-height:1;text-transform:uppercase;padding:30px 40px}}.big em{{font-style:normal;color:#FFD54A}}
.typing{{align-self:flex-start;background:#2B5278;border-radius:34px;padding:22px 34px;font-size:52px;letter-spacing:.3em;color:#9fc}}
.in{{position:absolute;left:36px;right:36px;bottom:210px;height:94px;background:#17212B;border-radius:50px;color:#6c7a88;font-size:34px;display:flex;align-items:center;padding:0 40px}}</style>
<div class=hd><img class=a src={AV}><div><b>4LPHA MARKETS</b><span>● en línea</span></div></div>
<div class=chat><div class="b l big">{t1}<br><em>{t2}</em></div><div class="b l" style="font-size:36px">{sub(d)}</div>{bub}<div class=typing>•••</div></div><div class=in>{fuente(d)}</div>"""

# ---------- 6. CARTEL: diagonal de color, tipografía gigante rotada ----------
def cartel(d):
    t1, t2 = head(d); c, p, r0 = big(d); good = up(d)
    A, B = ('#7B2FF7', '#FF7A18') if good else ('#111', '#FF2D55')
    chips = ''.join(f'<div class=ch><b>{E(x["n"])}</b> {E(x.get("p") or x.get("c") or "")}</div>' for x in rows(d, 4))
    return f"""<style>body{{background:{A};font-family:Mont;overflow:hidden}}
.d{{position:absolute;left:-300px;right:-300px;top:700px;height:1500px;background:{B};transform:rotate(-14deg)}}
.t1{{position:absolute;left:30px;top:250px;font-family:Anton;font-size:{F(t1,300,7)}px;line-height:.85;color:#fff;transform:rotate(-14deg);transform-origin:0 0;text-transform:uppercase;white-space:nowrap;text-shadow:12px 12px 0 rgba(0,0,0,.35)}}
.t2{{position:absolute;left:40px;top:1010px;font-family:Anton;font-size:{F(t2,220,10)}px;line-height:.9;color:#fff;transform:rotate(-14deg);transform-origin:0 0;text-transform:uppercase;text-shadow:10px 10px 0 rgba(0,0,0,.35)}}
.n{{position:absolute;right:30px;top:1120px;transform:rotate(-14deg);font-family:Anton;font-size:180px;color:#FFE600;text-shadow:8px 8px 0 #000}}
.chs{{position:absolute;left:50px;bottom:230px;display:flex;gap:14px;flex-wrap:wrap;width:980px}}.ch{{background:#000;color:#fff;font-weight:800;font-size:34px;padding:12px 22px;border-radius:12px}}.ch b{{color:#FFE600}}
.logo{{position:absolute;right:40px;top:250px;height:70px;background:#000;border-radius:16px;padding:8px 16px;z-index:3}}.t1{{top:330px!important}}.sub{{position:absolute;left:50px;bottom:420px;width:960px;font-weight:900;font-size:40px;color:#fff;text-shadow:3px 3px 0 #000}}.sub b{{background:#FFE600;color:#000;padding:0 8px}}</style>
<div class=d></div><div class=t1>{t1}</div><div class=t2>{t2}</div><div class=n>{E(re.sub('<[^>]+>','',c or p))}</div><div class=sub>{sub(d)}</div><div class=chs>{chips}</div><img class=logo src={LOGO}>"""

# ---------- 7. GRÁFICA: velas a pantalla completa con el titular encima ----------
def grafica(d):
    import random
    t1, t2 = head(d); good = up(d); rnd = random.Random(sum(map(ord, t1 + t2)))
    n = 26; v = .78 if not good else .18; cs = []
    for i in range(n):
        tgt = (.18 + .64 * i / n) if good else (.82 - .64 * i / n); o = v; v = tgt + (rnd.random() - .5) * .14; cs.append((o, v))
    W, H = 1080, 1000; bw = W / n; s = ''
    for i, (o, c) in enumerate(cs):
        up_ = c >= o; cc = '#34F5B0' if up_ else '#FF3B48'; yo, yc = H - o * H, H - c * H; hi = min(yo, yc) - rnd.random() * 50; lo = max(yo, yc) + rnd.random() * 50
        s += f'<line x1="{i*bw+bw/2}" x2="{i*bw+bw/2}" y1="{hi}" y2="{lo}" stroke="{cc}" stroke-width="5"/><rect x="{i*bw+8}" y="{min(yo,yc)}" width="{bw-16}" height="{max(10,abs(yo-yc))}" fill="{cc}"/>'
    c, p, r0 = big(d); ac = '#34F5B0' if good else '#FF3B48'
    chips = ''.join(f'<div class=k><span>{E(x["n"])}</span><b style="color:{col(x.get("cc"))}">{E(x.get("p") or x.get("c") or "")}</b></div>' for x in rows(d, 4))
    return f"""<style>body{{background:#0B1020;font-family:Mont}}
.gr{{position:absolute;inset:0;background:linear-gradient(180deg,#0B1020,#101a35)}}svg{{position:absolute;left:0;top:560px;opacity:.95}}
.t{{position:absolute;left:50px;right:50px;top:250px;white-space:nowrap;font-family:Anton;font-size:{F(max(t1,t2,key=len),190,10)}px;line-height:.93;color:#fff;text-transform:uppercase;text-shadow:0 10px 40px #000}}.t em{{font-style:normal;color:{ac}}}
.px{{position:absolute;right:30px;top:1020px;background:{ac};color:#04120d;font-weight:900;font-size:58px;padding:10px 24px;border-radius:14px;box-shadow:0 0 40px {ac}}}
.ks{{position:absolute;left:40px;right:40px;bottom:200px;display:flex;gap:14px}}.k{{flex:1;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.14);border-radius:22px;padding:18px 20px}}.k span{{display:block;font-size:22px;color:#9fb;font-weight:800;text-transform:uppercase}}.k b{{font-size:44px;font-weight:900}}
.sub{{position:absolute;left:54px;right:54px;top:790px;font-weight:800;font-size:38px;color:#dfe8ff;text-shadow:0 4px 20px #000}}.sub b{{color:{ac}}}</style>
<div class=gr></div><svg width="{W}" height="{H}">{s}</svg><div class=t>{t1}<br><em>{t2}</em></div><div class=sub>{sub(d)}</div><div class=px>{E(re.sub('<[^>]+>','',p or c))}</div><div class=ks>{chips}</div>"""

# ---------- 8. STICKERS: colorido, pegatinas giradas, estilo pop ----------
def stickers(d):
    t1, t2 = head(d); good = up(d); bg = '#FFD84A' if good else '#7DE3FF'
    cols = ['#FF4D8D', '#2EE6A6', '#7B5CFF', '#FF8A1F', '#111']
    st = ''.join(f'<div class=s style="background:{cols[i%5]};transform:rotate({[-5,4,-3,6][i%4]}deg);margin-left:{[0,80,20,100][i%4]}px"><small>{E(x["n"])}</small>{E(x.get("p") or x.get("c") or "")} <u>{E(x.get("c") or "") if x.get("p") else ""}</u></div>' for i, x in enumerate(rows(d, 4)))
    return f"""<style>body{{background:{bg};font-family:Mont;color:#111}}
.dots{{position:absolute;inset:0;background-image:radial-gradient(rgba(0,0,0,.14) 4px,transparent 5px);background-size:44px 44px}}
.burst{{position:absolute;right:30px;top:250px;width:330px;height:330px;background:#FF2D55;clip-path:polygon(50% 0%,61% 18%,80% 8%,80% 29%,100% 35%,86% 50%,100% 65%,80% 71%,80% 92%,61% 82%,50% 100%,39% 82%,20% 92%,20% 71%,0 65%,14% 50%,0 35%,20% 29%,20% 8%,39% 18%);display:flex;align-items:center;justify-content:center;transform:rotate(12deg);color:#fff;font-family:Anton;font-size:72px;text-align:center;line-height:1}}
.t{{position:absolute;left:50px;top:380px;width:980px;white-space:nowrap;font-family:Marker;font-size:{F(max(t1,t2,key=len),160,8)}px;line-height:.9;transform:rotate(-4deg);text-shadow:8px 8px 0 #fff}}.t2{{color:{'#12A773' if good else '#E5333F'}}}
.sub{{position:absolute;left:60px;right:60px;top:1010px;font-weight:900;font-size:42px;background:#fff;border:6px solid #111;border-radius:24px;padding:20px 26px;box-shadow:10px 10px 0 #111;transform:rotate(1.5deg)}}
.st{{position:absolute;left:50px;right:50px;top:1260px;display:flex;flex-direction:column;gap:18px}}.s{{color:#fff;font-weight:900;font-size:56px;padding:14px 30px;border-radius:22px;border:5px solid #111;box-shadow:8px 8px 0 #111;width:max-content;max-width:100%}}.s small{{font-size:22px;letter-spacing:.1em;display:block;opacity:.85}}.s u{{text-decoration:none;opacity:.85;font-size:.7em}}
.lg{{position:absolute;left:50px;top:262px;height:70px;background:#111;border-radius:16px;padding:8px 16px}}</style>
<div class=dots></div><img class=lg src={LOGO}><div class=burst>{E(d.get('tag') or 'WOW!')}</div>
<div class=t>{t1}<br><span class=t2>{t2}</span></div><div class=sub>{sub(d)}</div><div class=st>{st}</div>"""

# ---------- 9. VERSUS: pantalla partida verde/rojo ----------
def versus(d):
    t1, t2 = head(d); R = rows(d, 2) + [{}] * 2; a, b = R[0], R[1]
    def half(x, color, dark, y, lab):
        return f'<div class=h style="top:{y}px;background:{color};color:{dark}"><div class=l>{lab}</div><div class=n>{E(x.get("p") or x.get("c") or "—")}</div><div class=m>{E(x.get("n",""))} · {E(x.get("s",""))}</div><div class=c>{E(x.get("c") or "")}</div></div>'
    return f"""<style>body{{background:#000;font-family:Mont}}
.h{{position:absolute;left:0;right:0;height:840px;padding:150px 60px 0;text-align:center}}.h .l{{font-weight:900;font-size:40px;letter-spacing:.3em}}.h .n{{font-family:Anton;font-size:250px;line-height:1.05}}.h .m{{font-weight:800;font-size:38px;text-transform:uppercase}}.h .c{{font-family:Anton;font-size:100px}}
.mid{{position:absolute;left:0;right:0;top:830px;height:260px;background:#000;border-top:10px solid #fff;border-bottom:10px solid #fff;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:5;transform:skewY(-3deg);padding-left:140px}}.mid b{{white-space:nowrap;font-family:Anton;font-size:{F(t1+' · '+t2,116,16)}px;color:#fff;text-transform:uppercase;line-height:1}}.mid span{{font-size:32px;color:#FFE600;font-weight:900;margin-top:6px}}.mid span b{{font:inherit;color:#fff}}
.vs{{position:absolute;left:36px;top:950px;width:110px;height:110px;border-radius:50%;background:#FFE600;color:#000;font-family:Anton;font-size:52px;display:flex;align-items:center;justify-content:center;z-index:8;border:8px solid #000}}.logo{{position:absolute;left:40px;top:250px;height:62px;z-index:9;background:#000;border-radius:14px;padding:6px 14px}}</style>
{half(a,'#12A773','#fff',0,'SUBE' if a.get('cc')!='r' else 'CAE')}{half(b,'#E5333F','#fff',1080,'CAE' if b.get('cc')=='r' else 'SUBE')}
<div class=mid><b>{t1} · {t2}</b><span>{sub(d)}</span></div><div class=vs>VS</div><img class=logo src={LOGO}>"""

# ---------- 10. LOCKSCREEN: pantalla de bloqueo con notificaciones ----------
def lockscreen(d):
    t1, t2 = head(d); good = up(d)
    notes = ''.join(f'<div class=nt><img src={AV}><div><small>4LPHA MARKETS · ahora</small><b>{E(x["n"])}</b><p><span style="color:{"#7CFFB8" if x.get("cc")!="r" else "#FF8088"}">{E(x.get("p") or "")} {E(x.get("c") or "")}</span> · {E(x.get("s",""))}</p></div></div>' for x in rows(d, 4))
    return f"""<style>body{{font-family:Inter;color:#fff;background:linear-gradient(160deg,{'#0f3d6e,#1b1f5a 45%,#4a1a6b' if good else '#4a0f1f,#1f0f3a 50%,#0a1a3a'})}}
.glow{{position:absolute;left:-200px;top:300px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,{'rgba(52,245,176,.35)' if good else 'rgba(255,59,72,.4)'},transparent 65%)}}
.date{{position:absolute;left:0;right:0;top:240px;text-align:center;font-size:40px;font-weight:600;opacity:.9}}.time{{position:absolute;left:0;right:0;top:290px;text-align:center;font-size:250px;font-weight:200;letter-spacing:-.02em}}
.hl{{position:absolute;left:40px;right:40px;top:640px;background:rgba(255,255,255,.16);backdrop-filter:blur(20px);border-radius:46px;padding:36px 40px;border:2px solid rgba(255,255,255,.2)}}.hl small{{font-size:28px;opacity:.8;font-weight:700;letter-spacing:.05em}}.hl h1{{font-size:104px;line-height:1;font-weight:900;margin-top:10px;text-transform:uppercase}}.hl h1 em{{font-style:normal;color:{'#7CFFB8' if good else '#FF8088'}}}.hl p{{font-size:36px;margin-top:14px;opacity:.92}}.hl p b{{background:rgba(255,255,255,.25);padding:0 8px;border-radius:8px}}
.nts{{position:absolute;left:40px;right:40px;top:1090px;display:flex;flex-direction:column;gap:16px}}.nt{{display:flex;gap:22px;align-items:center;background:rgba(255,255,255,.14);backdrop-filter:blur(16px);border-radius:38px;padding:22px 28px;border:1px solid rgba(255,255,255,.18)}}.nt img{{width:92px;height:92px;border-radius:22px}}.nt small{{font-size:22px;opacity:.7;display:block}}.nt b{{font-size:34px}}.nt p{{font-size:30px;margin-top:2px}}
.bt{{position:absolute;left:0;right:0;bottom:200px;text-align:center;font-size:26px;opacity:.6}}</style>
<div class=glow></div><div class=date>{E(d.get('tag') or 'Mercados')} · hoy</div><div class=time>9:41</div>
<div class=hl><small>● NOTICIA</small><h1>{t1}<br><em>{t2}</em></h1><p>{sub(d)}</p></div><div class=nts>{notes}</div><div class=bt>{fuente(d)}</div>"""

FN = dict(alerta=alerta, gigante=gigante, terminal=terminal, periodico=periodico, chat=chat, cartel=cartel, grafica=grafica, stickers=stickers, versus=versus, lockscreen=lockscreen)

def render(d, out, estilo):
    page = f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}</style></head><body>{FN[estilo](d)}</body></html>'
    p = ROOT / 'historias' / 'estilos' / f'_tmp_{estilo}.html'
    p.write_text(page, encoding='utf-8')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=['--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
        pg.goto('file://' + str(p)); pg.wait_for_timeout(300); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        pg.screenshot(path=out, type='png'); b.close()
    p.unlink(missing_ok=True)

if __name__ == '__main__':
    a = [x for x in sys.argv[1:]]
    if '--lista' in a: print(' · '.join(ESTILOS)); sys.exit(0)
    def opt(n, dflt=None):
        if n in a: i = a.index(n); v = a[i + 1]; del a[i:i + 2]; return v
        return dflt
    est = opt('--estilo', 'auto'); hueco = int(opt('--hueco', '1'))
    if len(a) < 2: sys.exit(__doc__)
    d = json.load(open(a[0], encoding='utf-8-sig'))
    if isinstance(d, list): d = d[0]
    if est == 'auto': est = ORDEN[(hueco - 1) % len(ORDEN)]
    elif est.isdigit(): est = ESTILOS[int(est) % len(ESTILOS)]
    render(d, a[1], est); print('OK', est, a[1])
