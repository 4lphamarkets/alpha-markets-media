"""DESCARGA DE LOGOS PARA LA PORTADA (v8) → img/logos/<nombre>.png|svg
uso: python scripts/logos.py <nombre> [<nombre> ...] [--fuente auto|cripto|dex|marca] [--forzar]

  cripto : CoinGecko (monedas y exchanges: bitcoin, solana, pepe, binance, kraken…)  → PNG redondo
  dex    : DefiLlama (protocolos DeFi / DEX: uniswap, pancakeswap, hyperliquid, aave…) → PNG
  marca  : Simple Icons (empresas: nvidia, tesla, apple, blackrock…)                 → SVG monocromo
  auto   : prueba cripto → dex → marca (por defecto)

El nombre del archivo es el que se usa en entrega.json → "logos": ["uniswap", "bitcoin"].
Si ya existe en img/logos/ no se vuelve a descargar (salvo --forzar). Revisa siempre el resultado:
si el logo no es el correcto, guarda uno bueno a mano en img/logos/ con ese mismo nombre."""
import io, json, os, re, sys, unicodedata, urllib.parse, urllib.request
from PIL import Image
for _s in (sys.stdout, sys.stderr):   # v10: en la consola de Windows (cp1252) los "→" rompían el script
    try: _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(D, 'img', 'logos'); os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (logo-fetch)', 'Accept': '*/*'}

def norm(s): return re.sub(r'[^a-z0-9]+', '_', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()).strip('_')
def get(url, timeout=20):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r: return r.read()
def guardar_png(data, dest):
    im = Image.open(io.BytesIO(data)); im.load()
    if min(im.size) < 64: raise ValueError(f'imagen demasiado pequeña {im.size}')
    im.convert('RGBA').save(dest, 'PNG'); return dest

def cripto(n, dest):
    r = json.loads(get('https://api.coingecko.com/api/v3/search?query=' + urllib.parse.quote(n)))
    q = norm(n)
    cands = [(c, 'coin') for c in r.get('coins', [])] + [(e, 'exchange') for e in r.get('exchanges', [])]
    if not cands: raise LookupError('sin resultados')
    # preferir coincidencia exacta de id / símbolo / nombre; si no, el primero (más capitalización)
    exacto = [c for c in cands if q in (norm(c[0].get('id', '')), norm(c[0].get('symbol', '') or ''), norm(c[0].get('name', '')))]
    c, tipo = (exacto or cands)[0]
    url = c.get('large') or c.get('thumb')
    url = url.replace('/thumb/', '/large/').replace('/small/', '/large/')
    print(f'   CoinGecko {tipo}: {c.get("name")} ({c.get("id")})')
    return guardar_png(get(url), dest)

def dex(n, dest):
    for slug in dict.fromkeys([n.lower().replace(' ', '-'), norm(n).replace('_', '-'), norm(n).replace('_', '')]):
        try:
            png = guardar_png(get(f'https://icons.llamao.fi/icons/protocols/{slug}?w=512&h=512'), dest)
            print(f'   DefiLlama: {slug}'); return png
        except Exception: pass
    raise LookupError('no está en DefiLlama')

def marca(n, dest):
    slug = re.sub(r'[^a-z0-9]', '', n.lower())
    svg = get(f'https://cdn.jsdelivr.net/npm/simple-icons@13/icons/{slug}.svg').decode('utf-8')
    if '<svg' not in svg: raise LookupError('no es un SVG')
    dest = os.path.splitext(dest)[0] + '.svg'
    open(dest, 'w', encoding='utf-8').write(svg)
    print(f'   Simple Icons: {slug} (monocromo: pon "color" en entrega.json con el color de la marca)')
    return dest

FUENTES = {'cripto': [cripto], 'dex': [dex], 'marca': [marca], 'auto': [cripto, dex, marca]}

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    fuente = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == '--fuente' and i + 1 < len(sys.argv)), 'auto')
    args = [a for a in args if a != fuente] if '--fuente' in sys.argv else args
    if not args: sys.exit(__doc__)
    fallos = 0
    for n in args:
        base = os.path.join(OUT, norm(n))
        ya = [base + e for e in ('.png', '.svg', '.webp', '.jpg') if os.path.exists(base + e)]
        if ya and '--forzar' not in sys.argv: print(f'{n}: ya existe → {os.path.relpath(ya[0], D)}'); continue
        print(f'{n}:')
        for f in FUENTES[fuente]:
            try: print('   OK →', os.path.relpath(f(n, base + '.png'), D)); break
            except Exception as e: print(f'   {f.__name__}: {e}')
        else: fallos += 1; print(f'   NO ENCONTRADO: búscalo a mano y guárdalo como img/logos/{norm(n)}.png')
    sys.exit(1 if fallos else 0)
