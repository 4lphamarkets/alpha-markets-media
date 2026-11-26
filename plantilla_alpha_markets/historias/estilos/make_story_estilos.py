#!/usr/bin/env python3
"""HISTORIAS v27 · 10 DISEÑOS RADICALMENTE DISTINTOS (cada historia del día se ve completamente diferente a la anterior).
uso: python3 historias/estilos/make_story_estilos.py datos.json salida.png [--estilo N|nombre|auto] [--hueco K]
  datos.json = UNA historia: {"t1":"BITCOIN","t2":"BAJO 62K","sub":"Primera vez desde <b>JULIO</b> · 20 NOV",
                "rows":[{"n":"PRECIO","s":"BTC · HOY","p":"$61,974","c":"-1.93%","cc":"r"}, ...],   # 2-6 filas (cc: r rojo / v verde)
                "tag":"ÚLTIMA HORA" (opcional), "logo":"btc|eth|sol|none" (opcional), "icono":"lock" o ["lock","bank"] (opcional: pegatina que ilustra la noticia; ver ICONOS), "fuente":"CoinDesk · Cointelegraph"}
  --estilo auto (por defecto): elige el diseño por el nº de hueco del día (--hueco K, 1-10) usando ORDEN, que alterna estilos
                 de familias opuestas (oscuro/claro, texto/gráfico, tipografía serif/mono/display) → NUNCA dos parecidos seguidos.
  --lista: imprime los diseños.
Estilos v30 (los únicos activos): noticia, alerta, velas, poster, gigante, tweet."""
import json, os, re, sys, html, base64, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]          # plantilla_alpha_markets
E = html.escape
ESTILOS = ['alerta', 'gigante', 'terminal', 'periodico', 'chat', 'grafica', 'stickers', 'versus', 'lockscreen', 'poster', 'tweet', 'ticket', 'tv']
# orden de rotación: cada par consecutivo cambia de familia (oscuro→claro→mono→serif→…); el hueco K usa ORDEN[(K-1) % len(ORDEN)]  (cartel ELIMINADO 26-11-2026: «no se entiende bien», orden de Antonio)
ORDEN = ['alerta', 'tweet', 'terminal', 'stickers', 'poster', 'periodico', 'grafica', 'ticket', 'chat', 'tv', 'gigante', 'lockscreen', 'versus']

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


# ---------- ICONOS (v28): pegatinas SVG que ilustran la noticia (las mismas 23 del modo dinámico) ----------
_tpl = (ROOT / 'template_dinamico.html').read_text(encoding='utf-8')
ICONS = {m.group(1): m.group(2) for m in re.finditer(r"^ (\w+):\{svg:`(.*?)`", _tpl, re.M)}
ICONOS = sorted(ICONS)
def icon(name, size, rot=0, extra=''):
    """pegatina SVG con contorno blanco (como en el vídeo). name: magnet siren rocket fire skull bomb shield lock clock scales warning up down bank oil gold bolt eye doc boom money trophy question"""
    svg = ICONS.get(name)
    if not svg: return ''
    return (f'<div style="width:{size}px;height:{size}px;transform:rotate({rot}deg);{extra}'
            f'filter:drop-shadow(0 0 0 #fff) drop-shadow(6px 0 0 #fff) drop-shadow(-6px 0 0 #fff) drop-shadow(0 6px 0 #fff) drop-shadow(0 -6px 0 #fff) drop-shadow(0 18px 22px rgba(0,0,0,.45))">'
            f'<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="overflow:visible">{svg}</svg></div>')
def icons_of(d):
    ic = d.get('icono') or []
    return [ic] if isinstance(ic, str) else list(ic)
def sticker(d, x, y, size, rot=0, i=0, z=20):
    """posición absoluta (x,y = esquina sup. izq.); i = qué icono de la lista; si no hay icono pero hay logo -> moneda"""
    ics = icons_of(d)
    if i < len(ics):
        inner = icon(ics[i], size, rot)
    elif i == 0 and d.get('logo') in ('btc', 'eth', 'sol'):
        inner = f'<div style="transform:rotate({rot}deg);filter:drop-shadow(0 0 0 #fff) drop-shadow(6px 0 0 #fff) drop-shadow(-6px 0 0 #fff) drop-shadow(0 6px 0 #fff) drop-shadow(0 -6px 0 #fff) drop-shadow(0 18px 22px rgba(0,0,0,.45))">{coin(d["logo"], size)}</div>'
    else: return ''
    return f'<div style="position:absolute;left:{x}px;top:{y}px;z-index:{z}">{inner}</div>'

# colocación de las pegatinas en cada diseño (huecos libres): lista de (x, y, tamaño, rotación)
HERO = {
 'alerta':     [(700, 1440, 300, 10), (60, 1480, 190, -12)],
 'gigante':    [(690, 1420, 320, 12), (60, 1470, 200, -10)],
 'terminal':   [(700, 1210, 300, 8), (80, 1320, 200, -10)],
 'periodico':  [(680, 1380, 320, 8), (60, 1420, 200, -10)],
 'chat':       [(640, 1380, 340, 10), (60, 1420, 200, -8)],
 'cartel':     [(860, 1690, 160, 10)],
 'grafica':    [(660, 500, 330, 10), (60, 1500, 190, -10)],
 'stickers':   [(680, 620, 330, 12), (80, 1620, 200, -10)],
 'versus':     [(850, 1160, 200, 10), (870, 1660, 170, -10)],
 'lockscreen': [(700, 1480, 300, 10), (70, 1500, 190, -10)],
}

def _fit(t, base, mc): return int(base*min(1, mc/max(1, len(t))))

# ---------- 11. POSTER: icono gigante con rayos, titular debajo ----------
def poster(d):
    t1, t2 = head(d); c, p, r0 = big(d); good = up(d)
    a1, a2 = ('#0b3d2e', '#04130d') if good else ('#4a0a12', '#12030a'); ac = '#34F5B0' if good else '#FF4D5A'
    chips = ''.join(f'<div class=ch><small>{E(x["n"])}</small><b style="color:{col(x.get("cc"))}">{E(x.get("p") or x.get("c",""))}</b></div>' for x in rows(d, 3))
    rays = ''.join(f'<i style="transform:rotate({k*15}deg)"></i>' for k in range(24))
    return f"""<style>body{{background:radial-gradient(circle at 50% 28%,{a1},{a2} 70%);font-family:Mont;color:#fff}}
.rays{{position:absolute;left:50%;top:640px;width:0;height:0}}.rays i{{position:absolute;left:-14px;top:-1100px;width:28px;height:1100px;background:linear-gradient({ac}33,transparent);transform-origin:50% 100%}}
.glow{{position:absolute;left:190px;top:240px;width:700px;height:700px;border-radius:50%;background:radial-gradient({ac}55,transparent 65%)}}
.logo{{position:absolute;left:50%;transform:translateX(-50%);top:240px;height:70px;z-index:5}}
.h1{{position:absolute;left:40px;right:40px;top:1060px;text-align:center;font-family:Anton;font-size:{_fit(t1,200,9)}px;line-height:.95;text-transform:uppercase}}
.h2{{position:absolute;left:40px;right:40px;top:{1060+_fit(t1,200,9)}px;text-align:center;font-family:Anton;font-size:{_fit(t2,150,12)}px;line-height:1;text-transform:uppercase;color:{ac}}}
.sub{{position:absolute;left:70px;right:70px;top:1470px;text-align:center;font-weight:800;font-size:38px;line-height:1.25}}.sub b{{background:{ac};color:#000;padding:0 10px;border-radius:8px}}
.chs{{position:absolute;left:40px;right:40px;top:1570px;display:flex;gap:18px;justify-content:center}}.ch{{background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.2);border-radius:22px;padding:14px 24px;text-align:center}}.ch small{{display:block;font-size:20px;opacity:.7;font-weight:800}}.ch b{{font-family:Anton;font-size:46px}}
.src{{position:absolute;left:0;right:0;bottom:130px;text-align:center;font-size:24px;opacity:.55;font-weight:700}}</style>
<div class=glow></div><div class=rays>{rays}</div><img class=logo src={LOGO}>
{sticker(d,190,330,700,0,0,6) or sticker({'icono':['bolt']},190,330,700,0,0,6)}
<div class=h1>{t1}</div><div class=h2>{t2}</div><div class=sub>{sub(d)}</div><div class=chs>{chips}</div><div class=src>{fuente(d)}</div>"""

# ---------- 12. TWEET: tarjeta de publicación en X, clara ----------
def tweet(d):
    t1, t2 = head(d); rs = rows(d, 3)
    met = ''.join(f'<div class=m><b style="color:{col(x.get("cc"))}">{E(x.get("p") or x.get("c",""))}</b><span>{E(x["n"])}</span></div>' for x in rs)
    return f"""<style>body{{background:#E8EEF3;font-family:Inter,Mont;color:#0F1419}}
.tag{{position:absolute;left:0;right:0;top:250px;text-align:center;font-family:Mont;font-weight:900;font-size:34px;letter-spacing:.2em;color:#536471}}
.card{{position:absolute;left:50px;right:50px;top:340px;background:#fff;border-radius:40px;padding:46px 46px 40px;box-shadow:0 30px 80px rgba(0,0,0,.18)}}
.u{{display:flex;gap:22px;align-items:center}}.u img{{width:104px;height:104px;border-radius:50%}}.u b{{font-size:42px;display:block}}.u b i{{display:inline-block;width:38px;height:38px;border-radius:50%;background:#1D9BF0;color:#fff;font-style:normal;font-size:26px;text-align:center;line-height:38px;vertical-align:middle;margin-left:8px}}.u span{{font-size:30px;color:#536471}}
.x{{margin-left:auto;font-size:60px;font-weight:900}}
.tx{{font-size:{_fit(t1+t2,76,22)}px;font-weight:800;line-height:1.12;margin-top:34px}}.tx em{{font-style:normal;color:#1D9BF0}}
.sub{{font-size:38px;line-height:1.3;color:#344;margin-top:22px}}.sub b{{background:#DCEBFA;padding:0 8px;border-radius:8px}}
.hero{{height:470px;margin-top:30px;border-radius:30px;background:linear-gradient(135deg,#0F1D2D,#1d3b5a);position:relative;overflow:hidden}}
.mt{{display:flex;justify-content:space-around;margin-top:30px;padding-top:26px;border-top:2px solid #E1E8ED}}.m{{text-align:center}}.m b{{font-family:Anton;font-size:58px;display:block}}.m span{{font-size:22px;color:#536471;font-weight:800}}
.src{{position:absolute;left:0;right:0;bottom:190px;text-align:center;font-size:26px;color:#536471;font-weight:700;font-family:Mont}}</style>
<div class=tag>{E(d.get('tag') or 'EN TENDENCIA')}</div>
<div class=card><div class=u><img src={AV}><div><b>4LPHA MARKETS<i>✓</i></b><span>@4lphamarkets · ahora</span></div><div class=x>𝕏</div></div>
<div class=tx>{t1} <em>{t2}</em></div><div class=sub>{sub(d)}</div>
<div class=hero><div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)">{sticker(d,-190,-190,380,-6,0,1).replace('position:absolute;left:-190px;top:-190px','position:relative;left:0;top:0') or ''}</div></div>
<div class=mt>{met}</div></div><div class=src>{fuente(d)}</div>"""

# ---------- 13. TICKET: recibo/ticket de compra con sello gigante ----------
def ticket(d):
    t1, t2 = head(d); good = up(d); ac = '#0E9F6E' if good else '#E5333F'
    lines = ''.join(f'<div class=ln><span>{E(x["n"])}<small>{E(x.get("s",""))}</small></span><b style="color:{col(x.get("cc")) if x.get("cc")=="r" else "#0E9F6E"}">{E(x.get("p") or x.get("c",""))}</b></div>' for x in rows(d, 4))
    return f"""<style>body{{background:repeating-linear-gradient(45deg,#FF7A1A,#FF7A1A 40px,#FF8A33 40px,#FF8A33 80px);font-family:'Courier New',monospace;color:#111}}
.t{{position:absolute;left:90px;right:90px;top:260px;background:#FBFAF4;padding:56px 50px 90px;box-shadow:0 30px 70px rgba(0,0,0,.35);transform:rotate(-1.5deg);
 -webkit-mask:radial-gradient(circle 16px at 16px 100%,#0000 98%,#000) 0 0/32px 100% repeat-x;mask:linear-gradient(#000,#000)}}
.hd{{text-align:center;font-family:Mont;font-weight:900;font-size:34px;letter-spacing:.18em;border-bottom:4px dashed #111;padding-bottom:20px}}
.h1{{font-family:Anton;font-size:{_fit(t1,150,9)}px;line-height:1;text-transform:uppercase;text-align:center;margin-top:30px}}.h2{{font-family:Anton;font-size:{_fit(t2,110,12)}px;line-height:1;text-transform:uppercase;text-align:center;color:{ac}}}
.sub{{font-size:34px;text-align:center;margin:26px 0;line-height:1.3;font-weight:700}}.sub b{{background:#111;color:#FBFAF4;padding:0 8px}}
.ln{{display:flex;justify-content:space-between;align-items:flex-end;font-size:36px;font-weight:700;border-bottom:3px dashed #999;padding:16px 0}}.ln small{{display:block;font-size:22px;color:#777}}.ln b{{font-size:56px}}
.bar{{height:90px;margin-top:34px;background:repeating-linear-gradient(90deg,#111 0 4px,#fff 4px 10px,#111 10px 12px,#fff 12px 20px)}}
.src{{text-align:center;font-size:24px;margin-top:14px;color:#555}}
.logo{{position:absolute;left:50%;transform:translateX(-50%);top:1500px;height:64px;background:#111;border-radius:16px;padding:8px 18px}}</style>
<div class=t><div class=hd>★ ALPHA MARKETS ★</div><div class=h1>{t1}</div><div class=h2>{t2}</div><div class=sub>{sub(d)}</div>{lines}<div class=bar></div><div class=src>{fuente(d)}</div></div>
{sticker(d,660,1290,340,14,0,30)}{sticker(d,60,1430,220,-12,1,30)}<img class=logo src={LOGO}>"""

# ---------- 14. TV: informativo con gran imagen arriba, rótulo rojo y cinta ----------
def tv(d):
    t1, t2 = head(d); good = up(d); ac = '#34F5B0' if good else '#FF3B48'
    tk = ' ● '.join(E(x['n'] + ' ' + (x.get('p') or x.get('c', ''))) for x in rows(d, 4)) or E(fuente(d))
    return f"""<style>body{{background:#071B3A;font-family:Mont;color:#fff;overflow:hidden}}
.bg{{position:absolute;inset:0;background:radial-gradient(circle at 50% 30%,#1a4d9c,#071B3A 70%)}}.grid{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,#ffffff0d 0 2px,transparent 2px 60px),repeating-linear-gradient(90deg,#ffffff0d 0 2px,transparent 2px 60px)}}
.live{{position:absolute;left:50px;top:250px;background:#E5101F;font-weight:900;font-size:40px;padding:10px 28px;border-radius:10px;letter-spacing:.08em}}.live:before{{content:'';display:inline-block;width:18px;height:18px;border-radius:50%;background:#fff;margin-right:14px}}
.logo{{position:absolute;right:50px;top:246px;height:72px}}
.lt{{position:absolute;left:0;right:0;top:1060px}}.lt .a{{background:{ac};color:#000;font-family:Anton;font-size:{_fit(t1,150,11)}px;line-height:1.05;padding:12px 50px;text-transform:uppercase;width:fit-content;max-width:1000px;transform:skewX(-6deg);margin-left:30px}}
.lt .b{{background:#fff;color:#071B3A;font-family:Anton;font-size:{_fit(t2,118,14)}px;line-height:1.05;padding:10px 50px;text-transform:uppercase;margin:0 30px 0 0;width:fit-content;max-width:1000px;transform:skewX(-6deg);margin-left:60px}}
.sub{{position:absolute;left:60px;right:60px;top:1470px;font-weight:800;font-size:40px;line-height:1.3}}.sub b{{color:{ac}}}
.tk{{position:absolute;left:0;right:0;bottom:200px;background:#000;border-top:6px solid {ac};padding:20px 0;overflow:hidden;white-space:nowrap;font-weight:900;font-size:36px;letter-spacing:.04em}}.tk span{{display:inline-block;padding-left:40px}}</style>
<div class=bg></div><div class=grid></div><div class=live>{E(d.get('tag') or 'EN DIRECTO')}</div><img class=logo src={LOGO}>
{sticker(d,210,390,660,-4,0,6) or sticker({'icono':['eye']},210,390,660,-4,0,6)}
<div class=lt><div class=a>{t1}</div><div class=b>{t2}</div></div><div class=sub>{sub(d)}</div><div class=tk><span>{tk} ● {tk}</span></div>"""

FN = dict(alerta=alerta, gigante=gigante, terminal=terminal, periodico=periodico, chat=chat, grafica=grafica, stickers=stickers, versus=versus, lockscreen=lockscreen, poster=poster, tweet=tweet, ticket=ticket, tv=tv)

def render(d, out, estilo):
    over = ''
    if estilo in HERO and not d.get('sin_icono'):
        for i, (x, y, sz, rot) in enumerate(HERO[estilo]):
            over += sticker(d, x, y, sz, rot, i)
    page = f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}</style></head><body>{FN[estilo](d)}{over}</body></html>'
    p = ROOT / 'historias' / 'estilos' / f'_tmp_{estilo}.html'
    p.write_text(page, encoding='utf-8')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=['--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
        pg.goto('file://' + str(p)); pg.wait_for_timeout(300); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        pg.screenshot(path=out, type='png'); b.close()
    p.unlink(missing_ok=True)


# =====================================================================================
# v30 (26-11-2026, orden de Antonio): SOLO 6 DISEÑOS, todos con la IDENTIDAD DE MARCA (fondo verde oscuro, menta, cabecera logo+fecha);
# rojo/verde solo para lo que sube o baja. noticia + velas = los 2 modelos de Antonio (gráficas, cualquier activo cripto o bolsa);
# alerta + poster + gigante + tweet = los 4 más llamativos de los 13 anteriores, rehechos en colores de marca.
# =====================================================================================
BR = '../../../plantilla-historias/assets/'
MESES = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
def fecha_txt(d):
    if d.get('fecha'): return d['fecha']
    import datetime as dt
    try:
        from zoneinfo import ZoneInfo; n = dt.datetime.now(ZoneInfo('Europe/Madrid'))
    except Exception: n = dt.datetime.now()
    return f"{n.day} {MESES[n.month-1]} {n.year}"
def fitw(t, maxw, maxfs, k=0.8):
    t = re.sub('<[^>]+>', '', t); return int(min(maxfs, maxw / (max(1, len(t)) * k)))
def num(s):
    m = re.search(r'-?\d+(?:[.,]\d+)?', str(s or '')); 
    if not m: return None
    v = float(m.group(0).replace(',', '.'));  return -abs(v) if '-' in str(s) or '−' in str(s) else v
CAL = '<svg width="44" height="44" viewBox="0 0 44 44" fill="none" stroke="#34F5B0" stroke-width="4"><rect x="4" y="8" width="36" height="32" rx="6"/><path d="M4 18h36M13 3v9M22 3v9M31 3v9"/></svg>'
BCSS = f"""body{{background:#06150f url({BR}fondo_historia.png) center/cover;font-family:Mont;color:#fff}}
.blogo{{position:absolute;left:58px;top:62px;width:460px}}
.bdate{{position:absolute;left:590px;top:86px;width:422px;height:88px;border-radius:30px;background:rgba(0,0,0,.47);border:2px solid rgba(52,245,176,.2);display:flex;align-items:center;gap:20px;padding-left:34px;font-weight:800;font-size:44px;letter-spacing:.01em}}
.bcard{{border-radius:34px;border:2px solid rgba(52,245,176,.55);background:linear-gradient(rgba(9,46,36,.9),rgba(3,22,16,.94));box-shadow:0 0 30px rgba(52,245,176,.18)}}
.g2{{background:linear-gradient(#8bffd0,#0fb872);-webkit-background-clip:text;background-clip:text;color:transparent;font-style:italic;font-weight:900;text-transform:uppercase;filter:drop-shadow(0 0 26px rgba(52,245,176,.5))}}
.bsub{{font-weight:800;line-height:1.25;color:#cfeee2}}.bsub b{{color:#04130d;background:#34F5B0;padding:0 12px;border-radius:8px}}
.bsrc{{position:absolute;left:50px;right:50px;font-style:italic;font-size:25px;font-weight:600;color:#9fc5b6;text-align:center}}"""
def bhead(d): return f'<style>{BCSS}</style><img class=blogo src={BR}logo_alpha_wordmark.png><div class=bdate>{CAL}<span>{fecha_txt(d)}</span></div>'
def rcol(cc): return '#FF5454' if cc == 'r' else '#28F096'
def arrow(cc, s=96):
    c = rcol(cc); pts = '30,38 70,38 50,66' if cc == 'r' else '30,62 70,62 50,34'
    return f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="rgba(0,0,0,.35)" stroke="{c}" stroke-width="4"/><polygon points="{pts}" fill="{c}"/></svg>'

# ---------- A. NOTICIA (modelo 1 de Antonio): titular + filas de precios + gráfica de barras con oso/toro ----------
def noticia(d):
    t1, t2 = head(d); R = rows(d, 4); good = up(d)
    logos = d.get('logos') or []
    if isinstance(logos, str): logos = [logos]
    bad = ''
    for i, l in enumerate(logos[:2]):
        import os
        fp = ROOT.parent / 'plantilla-historias' / 'assets' / 'icons' / f'{l.upper()}.png'
        inner = f'<img src="{BR}icons/{l.upper()}.png" style="width:120px;height:120px">' if fp.exists() else f'<span style="font-size:{fitw(l,150,50,.85)}px">{E(l)}</span>'
        st = 'border:5px solid #34F5B0;background:rgba(0,0,0,.25)' if i == 0 else 'background:#D07A5E;box-shadow:0 0 40px rgba(208,122,94,.5)'
        bad += f'<div style="width:210px;height:210px;border-radius:50%;{st};display:flex;align-items:center;justify-content:center;font-weight:900;font-style:italic;margin-bottom:22px">{inner}</div>'
    maxw = 740 if logos else 960
    fs1 = fitw(t1, maxw, 200); fs2 = fitw(t2, maxw, 210)
    rws = ''
    for x in R:
        p = E(x.get('p') or ''); c = E(x.get('c') or '')
        right = (f'<div style="font-size:58px;font-weight:900">{p}</div>' if p else '') + f'<div style="font-size:58px;font-weight:900;color:{rcol(x.get("cc"))};min-width:260px;text-align:right">{c}</div>'
        rws += f'<div class="bcard" style="height:128px;margin-bottom:16px;display:flex;align-items:center;padding:0 34px;gap:26px;border-color:rgba(52,245,176,.35)">{arrow(x.get("cc"))}<div style="width:3px;height:84px;background:rgba(52,245,176,.35)"></div><div style="flex:1"><div style="font-size:46px;font-weight:900;text-transform:uppercase">{E(x["n"])}</div><div style="font-size:27px;font-weight:700;color:#9fd8c2;text-transform:uppercase">{E(x.get("s",""))}</div></div><div style="display:flex;gap:30px;align-items:center">{right}</div></div>'
    vals = [(x['n'], num(x.get('c'))) for x in R if num(x.get('c')) is not None]
    graf = ''
    if len(vals) >= 2:
        mx = max(abs(v) for _, v in vals) or 1; bw = min(130, 540 // len(vals) - 14)
        bars = ''.join(f'<div style="width:{bw}px;text-align:center"><div style="font-size:26px;font-weight:800;color:{rcol("r" if v<0 else "v")};margin-bottom:6px">{v:+g}%</div><div style="height:{max(14,int(abs(v)/mx*150))}px;border-radius:12px 12px 0 0;background:{rcol("r" if v<0 else "v")};box-shadow:0 0 24px {rcol("r" if v<0 else "v")}88"></div></div>' for _, v in vals)
        labs = ''.join(f'<div style="width:{bw}px;text-align:center;font-size:21px;font-weight:700;color:#9fd8c2;text-transform:uppercase">{E(n)}</div>' for n, _ in vals)
        graf = f'''<div class=bcard style="position:absolute;left:44px;right:44px;top:1370px;height:440px;overflow:hidden">
<img src={BR}oso.png style="position:absolute;left:0;bottom:60px;height:230px;opacity:.55;mix-blend-mode:screen"><img src={BR}toro.png style="position:absolute;right:0;bottom:60px;height:230px;opacity:.55;mix-blend-mode:screen">
<div style="text-align:center;font-size:40px;font-weight:900;margin-top:22px;text-transform:uppercase">{E(d.get("grafico") or ("Subidas" if good else "Caídas"))} (%)</div>
<div style="position:absolute;left:0;right:0;top:116px;display:flex;justify-content:center;gap:14px;align-items:flex-end;height:190px">{bars}</div>
<div style="position:absolute;left:0;right:0;top:308px;border-top:2px solid rgba(255,255,255,.25);display:flex;justify-content:center;gap:14px;padding-top:6px">{labs}</div>
<div style="position:absolute;left:0;right:0;bottom:20px;text-align:center;font-size:30px;font-weight:800">{d.get("nota","")}</div></div>'''
    return f"""{bhead(d)}<style>.badges{{position:absolute;right:46px;top:215px}}</style>
<div style="position:absolute;left:50px;top:205px;font-weight:900;text-transform:uppercase;font-size:{fs1}px;line-height:1.02;text-shadow:0 8px 24px rgba(0,0,0,.7)">{t1}</div>
<div class=g2 style="position:absolute;left:50px;top:{205+int(fs1*1.0)}px;font-size:{fs2}px;line-height:1.05;white-space:nowrap">{t2}</div>
<div class=badges>{bad}</div>
<div class=bsub style="position:absolute;left:50px;width:{maxw}px;top:{205+int(fs1*1.0)+int(fs2*1.12)+14}px;font-size:32px;letter-spacing:.05em;text-transform:uppercase">{sub(d)}</div>
<div style="position:absolute;left:44px;right:44px;top:{770 if len(R)>=4 else 800}px">{rws}</div>{graf}
<div class=bsrc style="top:1830px">{fuente(d)}</div>"""

# ---------- B. ALERTA (marca): última hora con bandas de peligro, titular y filas ----------
def alerta(d):
    t1, t2 = head(d); R = rows(d, 4); good = up(d)
    ac = '#28F096' if good else '#FF3B48'
    items = ''.join(f'<div class="bcard" style="height:132px;margin-bottom:18px;display:flex;align-items:center;padding:0 30px;gap:22px;border-color:{rcol(x.get("cc"))}88">{arrow(x.get("cc"),84)}<div style="flex:1"><div style="font-size:42px;font-weight:900;text-transform:uppercase">{E(x["n"])}</div><div style="font-size:24px;font-weight:700;color:#9fd8c2;text-transform:uppercase">{E(x.get("s",""))}</div></div><div style="font-size:60px;font-weight:900;color:{rcol(x.get("cc"))}">{E(x.get("p") or x.get("c",""))}</div></div>' for x in R)
    return f"""{bhead(d)}<style>.hz{{position:absolute;left:0;right:0;height:46px;background:repeating-linear-gradient(-45deg,{ac} 0 38px,#0a1410 38px 76px)}}</style>
<div style="position:absolute;left:50%;top:360px;width:900px;height:900px;margin-left:-450px;background:radial-gradient({ac}44,transparent 65%)"></div>
<div class=hz style="top:206px"></div><div class=hz style="bottom:84px"></div>
<div style="position:absolute;left:50px;top:290px;background:{ac};color:#fff;font-weight:900;font-size:46px;padding:12px 34px;border-radius:14px;letter-spacing:.08em;box-shadow:0 0 44px {ac}">● {E(d.get('tag') or 'ÚLTIMA HORA')}</div>
<div style="position:absolute;left:50px;top:400px;font-weight:900;text-transform:uppercase;font-size:{fitw(t1,780,210)}px;line-height:1;text-shadow:0 8px 28px rgba(0,0,0,.7);white-space:nowrap">{t1}</div>
<div class=g2 style="position:absolute;left:50px;top:{400+fitw(t1,780,210)+6}px;font-size:{fitw(t2,960,200)}px;line-height:1.05;white-space:nowrap">{t2}</div>
<div class=bsub style="position:absolute;left:54px;right:54px;top:930px;font-size:42px">{sub(d)}</div>
<div style="position:absolute;left:44px;right:44px;top:1090px">{items}</div>
<div class=bsrc style="bottom:150px">{fuente(d)}</div>"""

# ---------- C. POSTER (marca): icono gigante con rayos, titular debajo ----------
def poster(d):
    t1, t2 = head(d); good = up(d); ac = '#28F096' if good else '#FF4D5A'
    chips = ''.join(f'<div class="bcard" style="padding:14px 26px;text-align:center;border-radius:24px"><small style="display:block;font-size:20px;color:#9fd8c2;font-weight:800;text-transform:uppercase">{E(x["n"])}</small><b style="font-size:56px;font-weight:900;color:{rcol(x.get("cc"))}">{E(x.get("p") or x.get("c",""))}</b></div>' for x in rows(d, 3))
    rays = ''.join(f'<i style="transform:rotate({k*15}deg)"></i>' for k in range(24))
    return f"""{bhead(d)}<style>.rays{{position:absolute;left:50%;top:640px;width:0;height:0}}.rays i{{position:absolute;left:-14px;top:-1000px;width:28px;height:1000px;background:linear-gradient({ac}40,transparent);transform-origin:50% 100%}}</style>
<div style="position:absolute;left:190px;top:240px;width:700px;height:700px;border-radius:50%;background:radial-gradient({ac}66,transparent 65%)"></div><div class=rays>{rays}</div>
{sticker(d,190,260,700,0,0,6) or sticker({'icono':['bolt']},190,260,700,0,0,6)}
<div style="position:absolute;left:40px;right:40px;top:1000px;text-align:center;font-weight:900;text-transform:uppercase;font-size:{fitw(t1,1000,200)}px;line-height:1;text-shadow:0 8px 28px rgba(0,0,0,.7)">{t1}</div>
<div class=g2 style="position:absolute;left:40px;right:40px;top:{1000+fitw(t1,1000,200)+6}px;text-align:center;font-size:{fitw(t2,1000,170)}px;line-height:1.05;white-space:nowrap">{t2}</div>
<div class=bsub style="position:absolute;left:70px;right:70px;top:1470px;text-align:center;font-size:38px">{sub(d)}</div>
<div style="position:absolute;left:40px;right:40px;top:1590px;display:flex;gap:18px;justify-content:center">{chips}</div>
<div class=bsrc style="bottom:96px">{fuente(d)}</div>"""

# ---------- D. GIGANTE (marca): una cifra enorme en rojo/verde sobre el fondo de marca ----------
def gigante(d):
    t1, t2 = head(d); c, p, r0 = big(d); good = up(d); ac = '#28F096' if good else '#FF4D5A'
    txt = re.sub(r'<[^>]+>', '', c or p); fs = 400 if len(txt) <= 5 else 310 if len(txt) <= 7 else 230
    chips = ''.join(f'<div class="bcard" style="flex:1;padding:18px 10px;text-align:center;border-radius:26px"><small style="display:block;font-size:22px;color:#9fd8c2;font-weight:800;text-transform:uppercase">{E(x["n"])}</small><b style="font-size:58px;font-weight:900;color:{rcol(x.get("cc"))}">{E(x.get("p") or x.get("c",""))}</b></div>' for x in rows(d, 4)[1:4])
    return f"""{bhead(d)}
<div style="position:absolute;left:50px;top:230px;border:3px solid #34F5B0;color:#34F5B0;font-weight:900;font-size:40px;letter-spacing:.18em;padding:8px 26px;border-radius:14px;text-transform:uppercase">{E(d.get('tag') or 'HOY')}</div>
<div style="position:absolute;left:0;right:0;top:440px;text-align:center;font-family:Anton;font-size:{fs}px;line-height:1;color:{ac};transform:rotate(-4deg);text-shadow:0 0 70px {ac}99">{E(txt)}</div>
<div style="position:absolute;left:50px;right:50px;top:{440+fs+40}px;font-weight:900;text-transform:uppercase;font-size:{fitw(t1,960,150)}px;line-height:1;text-shadow:0 8px 28px rgba(0,0,0,.7)">{t1}</div>
<div class=g2 style="position:absolute;left:50px;right:50px;top:{440+fs+40+fitw(t1,960,150)+6}px;font-size:{fitw(t2,960,150)}px;line-height:1.05;white-space:nowrap">{t2}</div>
<div class=bsub style="position:absolute;left:54px;right:54px;top:1400px;font-size:38px">{sub(d)}</div>
<div style="position:absolute;left:44px;right:44px;top:1560px;display:flex;gap:16px">{chips}</div>
<div class=bsrc style="bottom:150px">{fuente(d)}</div>"""

# ---------- E. TWEET (marca): publicación de X sobre el fondo verde de marca ----------
def tweet(d):
    t1, t2 = head(d); rs = rows(d, 3); ics = icons_of(d) or ['bolt']
    met = ''.join(f'<div class=m><b style="color:{rcol(x.get("cc"))}">{E(x.get("p") or x.get("c",""))}</b><span>{E(x["n"])}</span></div>' for x in rs)
    return f"""{bhead(d)}<style>.card{{position:absolute;left:50px;right:50px;top:300px;background:#fff;border-radius:40px;padding:46px 46px 40px;box-shadow:0 0 0 4px rgba(52,245,176,.7),0 30px 90px rgba(0,0,0,.5);color:#0F1419;font-family:Inter,Mont}}
.u{{display:flex;gap:22px;align-items:center}}.u img{{width:104px;height:104px;border-radius:50%}}.u b{{font-size:42px;display:block}}.u b i{{display:inline-block;width:38px;height:38px;border-radius:50%;background:#1D9BF0;color:#fff;font-style:normal;font-size:26px;text-align:center;line-height:38px;vertical-align:middle;margin-left:10px}}.u span{{font-size:28px;color:#536471}}
.x{{margin-left:auto;font-size:60px;font-weight:900}}.tx{{font-size:{fitw(t1+' '+t2,880,96,.5)}px;font-weight:800;line-height:1.12;margin-top:34px}}.tx em{{font-style:normal;color:#0fa968}}
.sub{{font-size:38px;line-height:1.3;color:#344;margin-top:22px}}.sub b{{background:#c9f7e3;padding:0 8px;border-radius:8px}}
.hero{{height:640px;margin-top:30px;border-radius:30px;background:radial-gradient(circle at 50% 40%,#0d4a38,#04130d);position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center}}
.mt{{display:flex;justify-content:space-around;margin-top:30px;padding-top:26px;border-top:2px solid #E1E8ED}}.m{{text-align:center}}.m b{{font-family:Anton;font-size:58px;display:block}}.m span{{font-size:22px;color:#536471;font-weight:800;text-transform:uppercase}}</style>
<div style="position:absolute;left:0;right:0;top:205px;text-align:center;font-weight:900;font-size:32px;letter-spacing:.2em;color:#34F5B0">{E(d.get('tag') or 'EN TENDENCIA')}</div>
<div class=card><div class=u><img src={AV}><div><b>4LPHA MARKETS<i>✓</i></b><span>@4lphamarkets · ahora</span></div><div class=x>𝕏</div></div>
<div class=tx>{t1} <em>{t2}</em></div><div class=sub>{sub(d)}</div><div class=hero>{icon(ics[0],460,-6)}</div><div class=mt>{met}</div></div>
<div class=bsrc style="bottom:170px">{fuente(d)}</div>"""

FN.update(noticia=noticia, alerta=alerta, poster=poster, gigante=gigante, tweet=tweet)
ESTILOS = ['noticia', 'alerta', 'velas', 'poster', 'gigante', 'tweet']
ORDEN = ['noticia', 'alerta', 'velas', 'poster', 'gigante', 'tweet']       # hueco K -> ORDEN[(K-1)%6]; 10 huecos => 7-10 repiten (nunca dos seguidas)
HERO = {'alerta': [(790, 280, 230, 10)], 'gigante': [(800, 215, 200, 12)]}
def render_velas(d, out):
    import sys as _s
    _s.path.insert(0, str(ROOT.parent / 'plantilla-historias'))
    import btc15m_story as B
    import datetime as dt
    try:
        from zoneinfo import ZoneInfo; hh = dt.datetime.now(ZoneInfo('Europe/Madrid')).strftime('%H:%M')
    except Exception: hh = dt.datetime.now().strftime('%H:%M')
    B.build(d['chart'], out, d.get('hora') or hh, float(d.get('horas', 6)), d.get('ref'), d.get('activo', 'BITCOIN').upper(), d.get('simbolo', 'BTC').upper(),
            d.get('fuente_datos', 'CoinMarketCap'), float(d.get('pmin', 1e3)), float(d.get('pmax', 1e7)))
_render_html = render
def render(d, out, estilo):
    if estilo == 'velas': return render_velas(d, out)
    return _render_html(d, out, estilo)

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
