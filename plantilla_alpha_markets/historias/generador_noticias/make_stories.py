import re, json, sys, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]   # .../plantilla_alpha_markets
ICONS = ROOT.parent/'plantilla-historias'/'assets'/'icons'
SRC = (ROOT/'historias/nvidia_resultados.html').read_text(encoding='utf-8')
CSS = re.search(r'<style>(.*?)</style>', SRC, re.S).group(1)
UP = '<svg viewBox="0 0 24 24" fill="#34F5B0"><path d="M12 4l9 15H3z"/></svg>'
DN = '<svg viewBox="0 0 24 24" fill="#FF4A5C"><path d="M12 20L3 5h18z"/></svg>'
SQ = '<svg viewBox="0 0 24 24" fill="#FF4A5C"><rect x="5" y="5" width="14" height="14" rx="3"/></svg>'
NEU = '<svg viewBox="0 0 24 24" fill="#34F5B0"><circle cx="12" cy="12" r="6"/></svg>'
ICON = {'up': ('v', UP), 'dn': ('r', DN), 'sq': ('r', SQ), 'neu': ('v', NEU)}
E = html.escape

BTC = open(ROOT/'img/logos/bitcoin.svg').read().replace('<title>Bitcoin</title>','').replace('<svg ','<svg fill="#F7931A" ')
ANT = open(ROOT/'img/logos/anthropic.svg').read().replace('<title>Anthropic</title>','').replace('<svg ','<svg fill="#fff" ')
ETH = '<svg viewBox="0 0 24 24"><path fill="#8FA2FF" d="M12 1l-7 11.2L12 16z"/><path fill="#C3CCFF" d="M12 1l7 11.2L12 16z"/><path fill="#8FA2FF" d="M12 17.4l-7-4.2L12 23z"/><path fill="#C3CCFF" d="M12 17.4l7-4.2L12 23z"/></svg>'
LOGO = {
 'btc': ('<div class="lg" style="background:radial-gradient(circle at 50% 40%,rgba(247,147,26,.28),rgba(0,0,0,.55));border-color:#F7931A;box-shadow:0 0 60px rgba(247,147,26,.55),inset 0 0 40px rgba(247,147,26,.25)"><div class="li" style="width:62%;height:62%">'+BTC+'</div></div>'),
 'ant': ('<div class="lg" style="background:#D97757;border-color:#F3B49C;box-shadow:0 0 60px rgba(217,119,87,.6)"><div class="li" style="width:56%;height:56%">'+ANT+'</div></div>'),
 'eth': ('<div class="lg" style="background:radial-gradient(circle at 50% 40%,rgba(143,162,255,.28),rgba(0,0,0,.55));border-color:#8FA2FF;box-shadow:0 0 60px rgba(143,162,255,.5),inset 0 0 40px rgba(143,162,255,.2)"><div class="li" style="width:54%;height:54%">'+ETH+'</div></div>'),
 'hl': '<div class="lg" style="background:#0b2a22;border-color:#34F5B0;box-shadow:0 0 60px rgba(52,245,176,.55);overflow:hidden"><img src="../img/logos/hyperliquid.png" style="width:100%;height:100%;object-fit:cover"></div>',
}
def emo(e, c='#34F5B0'):
    return f'<div class="lg" style="background:radial-gradient(circle at 50% 40%,rgba(52,245,176,.18),rgba(0,0,0,.55));border-color:{c};box-shadow:0 0 60px rgba(52,245,176,.45),inset 0 0 40px rgba(52,245,176,.15)"><div class="li" style="font-size:150px;line-height:1;font-family:\'Noto Color Emoji\',sans-serif">{e}</div></div>'
LOGOCSS = '.lgw .lg{position:relative !important;left:0 !important;top:0 !important;width:100% !important;height:100% !important}.lg{position:absolute;left:800px;top:325px;width:250px;height:250px;border-radius:50%;border:5px solid;display:grid;place-items:center;z-index:6}.li{display:grid;place-items:center}.li svg{width:100%;height:100%}'


def row(i, r):
    cls, svg = ICON[r['ic']]
    top = 752 + 192 * i
    nfs = r.get('nfs', 54)
    s = f'<div class="fila" style="top:{top}px"><div class="ic {cls}">{svg}</div><div class="sep"></div>'
    s += f'<div class="nom"><b style="font-size:{nfs}px">{E(r["n"])}</b><i>{E(r["s"])}</i></div>'
    if r.get('p'):
        s += f'<div class="pr" style="font-size:{r.get("pfs",60)}px">{E(r["p"])}</div>'
    if r.get('c'):
        cc = 'v' if r.get('cc', 'v') == 'v' else 'r'
        s += f'<div class="ch {cc}" style="font-size:{r.get("cfs",62)}px;min-width:{r.get("cmin",230)}px">{E(r["c"])}</div>'
    return s + '</div>'

def chart_js(b):
    if b['type'] == 'line':
        pts = json.dumps(b['pts'])
        return f'''
const P={pts};const vs=P.map(p=>p[2]);const vmin=Math.min(...vs),vmax=Math.max(...vs);
const W=600,x0=50,dx=(W-100)/(P.length-1);
const pts=P.map((p,i)=>[x0+i*dx,160-((p[2]-vmin)/((vmax-vmin)||1))*95]);
let s=`<polyline points="${{pts.map(p=>p.join(',')).join(' ')}}" fill="none" stroke="#34F5B0" stroke-width="7" stroke-linejoin="round" stroke-linecap="round" style="filter:drop-shadow(0 0 10px rgba(52,245,176,.8))"/>`;
P.forEach((p,i)=>{{const [x,y]=pts[i];
 s+=`<circle cx="${{x}}" cy="${{y}}" r="11" fill="${{p[3]}}" stroke="#021008" stroke-width="3"/>`;
 s+=`<text x="${{x}}" y="${{y-20}}" text-anchor="middle" font-family="Mont" font-weight="900" font-size="${{b.vfs||30}}" fill="${{p[3]}}">${{p[1]}}</text>`;
 s+=`<text x="${{x}}" y="224" text-anchor="middle" font-family="Mont" font-weight="700" font-size="21" fill="#9fd9c4">${{p[0]}}</text>`;}});
document.getElementById('chart').innerHTML=s;'''.replace('b.vfs||30', str(b.get('vfs', 30)))
    if b['type'] == 'bars':
        items = json.dumps(b['items'])
        return f'''
const B={items};const m=Math.max(...B.map(x=>x[1]));const n=B.length;const bw=130,gap=(600-n*bw)/(n+1);
let s=`<line x1="0" y1="190" x2="600" y2="190" stroke="rgba(255,255,255,.25)"/>`;
B.forEach((x,i)=>{{const h=Math.max(8,(x[1]/m)*125);const bx=gap+i*(bw+gap);
 s+=`<rect x="${{bx}}" y="${{190-h}}" width="${{bw}}" height="${{h}}" rx="12" fill="${{x[3]}}" style="filter:drop-shadow(0 0 12px ${{x[3]}}88)"/>`;
 s+=`<text x="${{bx+bw/2}}" y="${{190-h-14}}" text-anchor="middle" font-family="Mont" font-weight="900" font-size="32" fill="${{x[3]}}">${{x[2]}}</text>`;
 s+=`<text x="${{bx+bw/2}}" y="222" text-anchor="middle" font-family="Mont" font-weight="700" font-size="21" fill="#9fd9c4">${{x[0]}}</text>`;}});
document.getElementById('chart').innerHTML=s;'''
    return ''


def one_logo(k, size, left, top):
    """k: 'btc','eth','ant','hl' (vectoriales) | 'icon:SOL' (PNG de plantilla-historias/assets/icons) | 'badge:NVDA' (ticker en círculo) | emoji o bandera (p. ej. 🇺🇸)"""
    if k in LOGO:
        h = LOGO[k]
    elif k.startswith('icon:'):
        p = ICONS/(k[5:]+'.png')
        h = f'<div class="lg" style="background:#0b2a22;border-color:#34F5B0;box-shadow:0 0 60px rgba(52,245,176,.5);overflow:hidden"><img src="file://{p}" style="width:100%;height:100%;object-fit:cover"></div>'
    elif k.startswith('badge:'):
        t = E(k[6:]); fs = 78 if len(t) <= 3 else (62 if len(t) == 4 else 48)
        h = f'<div class="lg" style="background:radial-gradient(circle at 50% 40%,rgba(52,245,176,.22),rgba(0,0,0,.6));border-color:#34F5B0;box-shadow:0 0 60px rgba(52,245,176,.5),inset 0 0 40px rgba(52,245,176,.15)"><div class="li" style="font-family:Mont;font-weight:900;font-style:italic;font-size:{fs}px;color:#fff">{t}</div></div>'
    else:
        h = emo(k)
    h = h.replace('font-size:150px', f'font-size:{int(size*0.6)}px')
    return f'<div class="lgw" style="position:absolute;left:{left}px;top:{top}px;width:{size}px;height:{size}px;z-index:6">{h}</div>'

def logos_html(lg):
    if not lg: return ''
    if isinstance(lg, str): lg = [lg]
    if len(lg) == 1: return one_logo(lg[0], 250, 800, 325)
    return one_logo(lg[0], 190, 830, 290) + one_logo(lg[1], 190, 830, 500)

def build(st):
    lg = st.get('logo')
    logohtml = logos_html(lg)
    TITCSS = '#tit{right:290px !important}' if lg else ''
    rows = ''.join(row(i, r) for i, r in enumerate(st['rows']))
    b = st['block']
    chart = '<svg id="chart" viewBox="0 0 600 230"></svg>' if b['type'] != 'text' else ''
    textblock = ''
    if b['type'] == 'text':
        textblock = f'<div id="big" style="position:absolute;left:150px;right:150px;top:78px;height:160px;display:flex;align-items:center;justify-content:center;text-align:center;font-family:Mont;font-weight:900;font-size:{b.get("fs",44)}px;line-height:1.15;color:#fff"><div>{b["big"]}</div></div>'
    TW = 740 if lg else 900
    js = f'''
document.getElementById('marca').innerHTML=marca('',82);
document.querySelectorAll('#marca img').forEach(i=>i.src='../img/logo_alpha_wordmark.png');
document.fonts.ready.then(()=>{{ajustar(document.getElementById('t1'),{TW},270,50); ajustar(document.getElementById('t2'),{TW},170,36);
 const sb=document.getElementById('sub');sb.style.whiteSpace='nowrap';sb.style.display='inline-block';sb.style.left='50%';sb.style.right='auto';sb.style.transform='translateX(-50%)';let f=34;while(sb.scrollWidth>1000&&f>20){{f-=1;sb.style.fontSize=f+'px';}}
 document.querySelectorAll('.nom').forEach(n=>{{const b=n.querySelector('b'),i=n.querySelector('i');i.style.whiteSpace='nowrap';
  let fb=parseInt(getComputedStyle(b).fontSize);while(b.scrollWidth>n.clientWidth&&fb>26){{fb-=2;b.style.fontSize=fb+'px';}}
  let fi=28;while(i.scrollWidth>n.clientWidth&&fi>16){{fi-=1;i.style.fontSize=fi+'px';}}}});}});
const c=document.getElementById('bgc').getContext('2d'), r=azar({json.dumps(st['slug'])});
for(let i=0;i<900;i++){{const x=r()*1080,y=r()*1920,d=Math.hypot(x-540,y-640);const a=d<460?.22:.07;c.fillStyle=`rgba(52,245,176,${{a*r()*1.6}})`;c.fillRect(x,y,2.2,2.2);}}
for(let k=0;k<2;k++){{let x=k?900:60;for(let i=0;i<5;i++){{const h=40+r()*120,y=(k?330:300)+r()*160,up=r()>.35;c.fillStyle=up?'rgba(52,245,176,.75)':'rgba(255,74,92,.5)';c.fillRect(x+(k?1:-1)*i*34,y,12,h);c.fillRect(x+(k?1:-1)*i*34+5,y-24,2,h+48);}}}}
for(let y0 of [0,1920]){{const g=c.createLinearGradient(0,y0,0,y0?1700:220);g.addColorStop(0,'rgba(52,245,176,.22)');g.addColorStop(1,'rgba(52,245,176,0)');c.fillStyle=g;c.fillRect(0,y0?1700:0,1080,220);}}
for(let i=0;i<22;i++){{const x=20+i*49+r()*14,top=r()>.5,h=top?30+r()*70:8+r()*14,up=r()>.35;c.fillStyle=up?'rgba(52,245,176,.35)':'rgba(255,74,92,.28)';c.fillRect(x,top?0:1920-h,10,h);}}
''' + chart_js(b)
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="../portadas/kit.css"><script src="../portadas/kit.js"></script>
<style>{CSS}{LOGOCSS}{TITCSS}</style></head><body><div id="p">
<canvas id="bgc" width="1080" height="1920"></canvas>
<div id="globo"></div>
<div id="head"><div id="marca"></div>
 <div id="fecha"><svg viewBox="0 0 24 24" fill="none" stroke="#34F5B0" stroke-width="1.8"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>20 NOV 2026</div></div>
<div id="tit"><span class="a" id="t1">{E(st['t1'])}</span><span class="b" id="t2">{E(st['t2'])}</span></div>
{logohtml}
<div id="sub">{st['sub']}</div>
{rows}
<div id="bloque">
 <img class="animal oso" src="assets/oso.png"><img class="animal toro" src="assets/toro.png">
 <div id="bt">{E(b['title'])}</div>
 {chart}{textblock}
 <div id="res">{b['res']}</div>
</div>
<div id="pie"><span>{E(st['pie'])}</span></div>
<script>{js}</script></div></body></html>'''

def render_all(jpath, outdir, quality=95):
    import subprocess, shutil
    chrome = shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')
    if not chrome: raise SystemExit('ERROR: no hay Chrome/Chromium')
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    stories = json.load(open(jpath, encoding='utf-8'))
    from PIL import Image
    for st in stories:
        h = ROOT/'historias'/f"{st['slug']}.html"; h.write_text(build(st), encoding='utf-8')
        png = outdir/f"{st['slug']}.png"
        subprocess.run([chrome,'--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--window-size=1080,1920','--virtual-time-budget=6000',f'--screenshot={png}',f'file://{h}'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=120)
        h.unlink()
        im = Image.open(png).convert('RGB')
        assert im.size == (1080,1920), (png, im.size)
        jpg = png.with_suffix('.jpg'); im.save(jpg,'JPEG',quality=quality,subsampling=0); 
        print('OK', jpg)

if __name__ == '__main__':
    # uso: python3 make_stories.py noticias.json carpeta_salida   -> genera .png y .jpg 1080x1920 de cada historia
    render_all(sys.argv[1], sys.argv[2])
