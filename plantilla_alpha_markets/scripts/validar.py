"""VALIDAR (v23): detecta errores ANTES de gastar minutos de render.
uso: python scripts/validar.py                       → comprueba el entorno (python, ffmpeg, node, playwright, Chrome, fuentes, sonidos)
     python scripts/validar.py timeline [ruta] [--modo analista|clasico]   → revisa tmp/timeline.json (por defecto)
Sale con código 1 si hay ERRORES; los AVISOS no paran nada. Lo usa scripts/montar.py automáticamente."""
import json, os, re, shutil, subprocess, sys

D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

ERR, AVISO = [], []
def err(m): ERR.append(m)
def aviso(m): AVISO.append(m)
def informe(titulo):
    print(f'== {titulo} ==')
    for m in ERR: print('  ✘ ERROR :', m)
    for m in AVISO: print('  ! AVISO :', m)
    if not ERR and not AVISO: print('  ✔ todo correcto')
    elif not ERR: print('  ✔ sin errores (revisa los avisos)')
    return 1 if ERR else 0

COMPONENTES = {'pill', 'tag', 'card', 'stat', 'num', 'vs', 'calendar', 'bars', 'candles', 'line', 'logo', 'follow', 'disc', 'gap'}
SEG_MIN, SEG_MAX = 25, 40          # v24: vídeos de 40 s como MÁXIMO (si el usuario pide otra duración, el aviso se ignora)
MAX_CARS_LINEA = 26                # prep_analista parte en líneas de <= 26 caracteres
CPS_MAX = 19                       # caracteres por segundo que se leen cómodos en pantalla


# ------------------------------------------------------------------ entorno
def entorno():
    def cmd(n, args=('-version',)):
        p = shutil.which(n)
        if not p: return None
        try: return subprocess.run([n, *args], capture_output=True, text=True, timeout=20).stdout.splitlines()[0]
        except Exception: return p
    if sys.version_info < (3, 8): err(f'Python {sys.version.split()[0]}: hace falta 3.8 o superior')
    for mod in ('numpy', 'PIL'):
        try: __import__(mod)
        except ImportError: err(f'falta el módulo Python "{mod}" (pip install numpy pillow)')
    for n in ('ffmpeg', 'ffprobe'):
        if not cmd(n): err(f'falta {n} en el PATH')
    if not cmd('node', ('--version',)): err('falta Node.js en el PATH')
    else:
        r = subprocess.run(['node', '-e', "try{require('playwright-core')}catch{require('playwright')}"], capture_output=True, text=True, cwd=D)
        if r.returncode: err('falta Playwright: npm i playwright-core (en la carpeta de la plantilla)')
    cands = [os.environ.get('CHROME'), r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
             '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable',
             '/usr/bin/chromium', '/usr/bin/chromium-browser']
    if not any(c and os.path.exists(c) for c in cands): aviso('no encuentro Google Chrome (se usará el de Playwright si está instalado; o fija CHROME=<ruta>)')
    for f in ('fonts/montserrat-latin-wght-normal.woff2', 'fonts/anton-latin-400-normal.woff2', 'fonts/inter-latin-wght-normal.woff2',
              'img/logo_alpha_wordmark.png', 'img/avatar.jpg', 'sonidos/catalogo.json'):
        if not os.path.exists(os.path.join(D, f)): err(f'falta {f}')
    try:
        cat = json.load(open(os.path.join(D, 'sonidos', 'catalogo.json'), encoding='utf-8'))
        faltan = [c['file'] for c in cat.values() if not os.path.exists(os.path.join(D, 'sonidos', c['file']))]
        if faltan: err('faltan sonidos: ' + ', '.join(faltan))
    except Exception as e: err(f'sonidos/catalogo.json ilegible: {e}')
    try: import sherpa_onnx  # noqa
    except ImportError: aviso('sherpa-onnx no instalado (solo hace falta para transcribir con scripts/transcribir.py: pip install sherpa-onnx)')
    return informe('ENTORNO')


# ------------------------------------------------------------------ timeline
def timeline(ruta, modo):
    try: tl = json.load(open(ruta, encoding='utf-8-sig'))
    except FileNotFoundError: err(f'no existe {ruta}'); return informe('TIMELINE')
    except Exception as e: err(f'JSON inválido en {ruta}: {e}'); return informe('TIMELINE')
    S, C, end = tl.get('scenes') or [], tl.get('chunks') or [], tl.get('end')
    if not S: err('timeline sin "scenes"'); return informe('TIMELINE')
    if not isinstance(end, (int, float)): err('timeline sin "end" numérico'); return informe('TIMELINE')
    ids = [s.get('id') for s in S]
    if len(set(ids)) != len(ids): err('hay ids de escena repetidos: ' + str([i for i in ids if ids.count(i) > 1]))
    # escenas contiguas, desde 0 hasta end
    if abs(S[0].get('a', 0)) > 1e-6: err(f'la primera escena empieza en {S[0].get("a")} s (debe ser 0: antes del inicio se vería la última escena)')
    for i, s in enumerate(S):
        a, b = s.get('a'), s.get('b')
        if a is None or b is None: err(f'escena {s.get("id")}: falta a o b'); continue
        if b <= a: err(f'escena {s["id"]}: dura {b - a:.2f} s (a={a}, b={b})')
        elif b - a < 1.5: aviso(f'escena {s["id"]} muy corta ({b - a:.1f} s)')
        if i + 1 < len(S) and S[i + 1].get('a') is not None and abs(S[i + 1]['a'] - b) > 1e-3:
            err(f'hueco/solape entre {s["id"]} (b={b}) y {S[i + 1]["id"]} (a={S[i + 1]["a"]})')
    if abs(S[-1].get('b', 0) - end) > 0.05: err(f'la última escena acaba en {S[-1].get("b")} pero "end" es {end}')
    if not SEG_MIN - 3 <= end <= SEG_MAX + 1: aviso(f'duración {end:.1f} s: el máximo es {SEG_MAX} s (ignorar si el usuario pidió otra)')
    # subtítulos
    por = {i: [] for i in ids}
    for k, c in enumerate(C):
        sid, t0, t1, txt = c.get('s'), c.get('t0'), c.get('t1'), c.get('text', '')
        if sid not in por: err(f'subtítulo {k} ("{txt[:20]}"): escena "{sid}" inexistente'); continue
        if t0 is None or t1 is None or t1 <= t0: err(f'subtítulo {k} ("{txt[:20]}"): tiempos incorrectos (t0={t0}, t1={t1})'); continue
        por[sid].append(c)
        if txt.count('*') % 2: err(f'subtítulo {k} ("{txt}"): asterisco sin cerrar')
        limpio = txt.replace('*', '')
        if modo == 'analista' and len(limpio) > MAX_CARS_LINEA + 2: aviso(f'subtítulo {k}: {len(limpio)} caracteres (> {MAX_CARS_LINEA}); saldrá en 2 líneas')
        if (t1 - t0) > 0 and len(limpio) / (t1 - t0) > CPS_MAX: aviso(f'subtítulo {k} ("{limpio}"): {len(limpio) / (t1 - t0):.0f} car/s, se lee muy deprisa')
        if k and C[k - 1].get('t1', 0) > t0 + 1e-3 and C[k - 1].get('s') == sid: aviso(f'subtítulos {k - 1} y {k} se solapan ({C[k - 1]["t1"]} > {t0})')
        s = next((x for x in S if x['id'] == sid), None)
        if s and (t0 < s['a'] - 0.05 or t0 >= s['b']): err(f'subtítulo {k} ("{limpio}"): empieza en {t0} fuera de su escena {sid} ({s["a"]}–{s["b"]})')
    if C and C[0].get('t0', 0) > 1.2: aviso(f'el primer subtítulo entra en {C[0]["t0"]} s: el gancho debe empezar en el primer segundo')
    for sid, lst in por.items():
        if not lst: aviso(f'la escena {sid} no tiene subtítulos')
    # modo analista: componentes y recursos
    if modo == 'analista':
        for s in S:
            comps = s.get('comps') or []
            if not comps: aviso(f'escena {s["id"]} sin componentes (solo se vería el fondo y el subtítulo)')
            vis = [c for c in comps if c.get('type') not in ('gap', 'disc', 'tag', 'logo')]
            if len(vis) > 4: aviso(f'escena {s["id"]}: {len(vis)} piezas visibles (máx. 3-4: se reducirá el tamaño para que quepan)')
            if len((s.get('kicker') or '')) > 38: aviso(f'escena {s["id"]}: kicker de {len(s["kicker"])} caracteres (> 38): saldrá con la letra más pequeña')
            if not s.get('kicker') and not tl.get('kicker_global'): aviso(f'escena {s["id"]} sin kicker')
            dur = s.get('b', 0) - s.get('a', 0)
            for c in comps:
                t = c.get('type')
                if t not in COMPONENTES: err(f'escena {s["id"]}: componente desconocido "{t}" (válidos: {", ".join(sorted(COMPONENTES))})'); continue
                at = c.get('at')
                if at is not None and at > dur - 0.3: err(f'escena {s["id"]}: "{t}" aparece en at={at} pero la escena dura {dur:.1f} s: nunca se vería')
                if t == 'num' and 'value' not in c: err(f'escena {s["id"]}: num sin "value"')
                if t == 'calendar' and not c.get('days'): err(f'escena {s["id"]}: calendar sin "days"')
                if t == 'bars' and not c.get('items'): err(f'escena {s["id"]}: bars sin "items"')
                if t == 'line' and not c.get('pts'): err(f'escena {s["id"]}: line sin "pts"')
                if t == 'candles' and not (c.get('data') or c.get('gen')): err(f'escena {s["id"]}: candles sin "data" ni "gen"')
                if t == 'candles' and c.get('gen') and not c.get('data'):
                    aviso(f'escena {s["id"]}: velas generadas ("gen") = solo ilustración; no afirmes niveles de precio con ellas (usa "data" real)')
                if t == 'logo' and c.get('src') and not os.path.exists(os.path.join(D, c['src'])): err(f'escena {s["id"]}: no existe {c["src"]}')
            if s.get('bg') and not os.path.exists(os.path.join(D, s['bg'])): err(f'escena {s["id"]}: no existe el fondo {s["bg"]}')
        tipos_ult = [c.get('type') for c in (S[-1].get('comps') or [])]
        if 'follow' not in tipos_ult: aviso('la última escena no lleva "follow" (tarjeta @4lphamarkets con botón Seguir)')
        if 'disc' not in tipos_ult and not any('consejo financiero' in str(c.get('text', '')).lower() for s in S for c in s.get('comps', [])):
            aviso('falta el descargo «esto no es consejo financiero» (componente "disc" en la última escena)')
    else:
        html = open(os.path.join(D, 'template.html'), encoding='utf-8').read()
        have = set(re.findall(r'<section class="scene" id="([^"]+)"', html))
        for s in S:
            if s['id'] not in have: err(f'la escena "{s["id"]}" no existe en template.html (hay: {", ".join(sorted(have))}); adapta template.html a este vídeo')
        for e in have - set(ids): aviso(f'template.html tiene la escena "{e}" que no está en el timeline (no se mostrará)')
    return informe(f'TIMELINE ({modo}) · {len(S)} escenas · {len(C)} subtítulos · {end:.1f} s')


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    if a and a[0] == 'timeline':
        modo = 'analista'
        if '--modo' in sys.argv: modo = sys.argv[sys.argv.index('--modo') + 1]; a = [x for x in a if x != modo]
        ruta = os.path.abspath(a[1]) if len(a) > 1 else os.path.join(D, 'tmp', 'timeline.json')
        sys.exit(timeline(ruta, modo))
    sys.exit(entorno())
