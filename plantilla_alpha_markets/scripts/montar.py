"""MONTAR: todo el montaje del vídeo con UN comando (v23). Sustituye a lanzar a mano prep → build → stills → render → insertos → events → sfx → final.
uso:
  python scripts/montar.py revisar analista tmp/guion_analista.json     # prep + validar + build + HOJA DE CONTACTO (out/hoja_contacto.jpg); no renderiza el vídeo
  python scripts/montar.py video   analista tmp/guion_analista.json     # todo: prep, validar, build, render, insertos, efectos, mezcla, QA → out/video_final.mp4
  python scripts/montar.py video   clasico  tmp/guion_clasico.json      # igual con template.html (el clásico se adapta a mano; ver LEEME)
  opciones: --workers N   --salida out/otro.mp4   --sin-hoja (en 'video' no genera la hoja)   --sin-prep (usa el tmp/timeline.json que ya existe)
Recomendado: primero «revisar» (segundos), mirar la hoja de contacto, corregir, y solo entonces «video» (minutos).
Cada paso muestra cuánto tarda; si uno falla, el script se para y dice cuál fue."""
import json, os, subprocess, sys, time
D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SC = os.path.join(D, 'scripts')
PY = sys.executable
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

def opt(n, default=None):
    if n in sys.argv:
        i = sys.argv.index(n); v = sys.argv[i + 1] if i + 1 < len(sys.argv) else default
        del sys.argv[i:i + 2]; return v
    return default
def flag(n):
    if n in sys.argv: sys.argv.remove(n); return True
    return False

workers = opt('--workers'); salida = opt('--salida', os.path.join('out', 'video_final.mp4'))
sin_hoja, sin_prep = flag('--sin-hoja'), flag('--sin-prep')
a = sys.argv[1:]
if len(a) < 2 or a[0] not in ('revisar', 'video') or a[1] not in ('analista', 'clasico'): sys.exit(__doc__)
accion, modo = a[0], a[1]
guion = os.path.abspath(a[2]) if len(a) > 2 else None
PREP = 'prep_analista.py' if modo == 'analista' else 'prep_clasico.py'
pasos = []
T0 = time.time()

def paso(titulo, cmd, cwd=D, tolerar=False):
    n = len(pasos) + 1; t = time.time()
    print(f'\n[{n}] {titulo}', flush=True)
    r = subprocess.run(cmd, cwd=cwd)
    dt = time.time() - t
    if r.returncode and not tolerar:
        sys.exit(f'\n✘ FALLÓ el paso {n} ({titulo}) tras {dt:.0f} s. Corrige y vuelve a lanzar (los pasos anteriores no hace falta repetirlos con --sin-prep).')
    pasos.append((titulo, dt)); print(f'    ({dt:.1f} s)', flush=True)

def hoja_contacto():
    """Dos fotogramas por escena (al 35 % y al 85 %) → out/hoja_contacto.jpg, para revisar el vídeo de un vistazo."""
    from PIL import Image, ImageDraw
    tl = json.load(open(os.path.join(D, 'tmp', 'timeline.json'), encoding='utf-8-sig'))
    tiempos = []
    for s in tl['scenes']:
        d = s['b'] - s['a']
        for q in (.35, .85): tiempos.append((s['id'], round(s['a'] + q * d, 2)))
    paso(f'Fotogramas de revisión ({len(tiempos)})', ['node', os.path.join('scripts', 'render.js'), 'stills', *[str(t) for _, t in tiempos]])
    cols, tw, th = 6, 270, 480
    filas = (len(tiempos) + cols - 1) // cols
    hoja = Image.new('RGB', (cols * tw, filas * (th + 26)), (8, 12, 10)); dr = ImageDraw.Draw(hoja)
    for i, (sid, t) in enumerate(tiempos):
        p = os.path.join(D, 'out', f'still_{t}.png')
        if not os.path.exists(p): continue
        im = Image.open(p).convert('RGB').resize((tw, th), Image.LANCZOS)
        x, y = (i % cols) * tw, (i // cols) * (th + 26)
        hoja.paste(im, (x, y + 26)); dr.text((x + 6, y + 6), f'{sid} · {t:.1f}s', fill=(52, 245, 176))
    dest = os.path.join(D, 'out', 'hoja_contacto.jpg'); hoja.save(dest, quality=88)
    print('    hoja de contacto: out/hoja_contacto.jpg  (ábrela y busca texto cortado, solapes o piezas fuera de la zona segura)')

os.makedirs(os.path.join(D, 'tmp'), exist_ok=True); os.makedirs(os.path.join(D, 'out'), exist_ok=True)
print(f'MONTAR · {accion} · modo {modo}')
paso('Comprobar entorno', [PY, os.path.join(SC, 'validar.py')])
if not sin_prep:
    if guion: paso(f'Preparar timeline ({PREP})', [PY, os.path.join(SC, PREP), guion])
    elif not os.path.exists(os.path.join(D, 'tmp', 'timeline.json')): sys.exit('Indica el guion (python scripts/montar.py ... tmp/guion_*.json) o deja un tmp/timeline.json hecho.')
    else: print('\n(sin guion: se usa el tmp/timeline.json existente)')
paso('Validar timeline', [PY, os.path.join(SC, 'validar.py'), 'timeline', '--modo', modo])
paso('Generar index.html', [PY, os.path.join(SC, 'build.py'), modo])

if accion == 'revisar':
    hoja_contacto()
else:
    if not sin_hoja: hoja_contacto()
    paso('Render del vídeo (PNG sin pérdida → H.264 CRF 12)', ['node', os.path.join('scripts', 'render.js'), 'video', *([workers] if workers else [])])
    try: ins = json.load(open(os.path.join(D, 'insertos.json'), encoding='utf-8-sig')).get('insertos', [])
    except Exception: ins = []
    if ins: paso(f'Insertos ({len(ins)})', [PY, os.path.join(SC, 'insertos.py')])
    else: print('\n(insertos.json vacío: sin insertos; recuerda que cada vídeo lleva 1-2 momentos dibujados, ver LEEME)')
    fin = json.load(open(os.path.join(D, 'tmp', 'timeline.json'), encoding='utf-8-sig'))['end']
    paso('Eventos de sonido', ['node', os.path.join('scripts', 'render.js'), 'events'])
    paso('Efectos de sonido', [PY, os.path.join(SC, 'sfx.py'), os.path.join('tmp', 'events.json'), os.path.join('tmp', 'sfx.wav'), str(fin)])
    paso('Mezcla final (voz + efectos, -16 LUFS)', [PY, os.path.join(SC, 'final.py'), salida])
    paso('Control de calidad', [PY, os.path.join(SC, 'qa_video.py'), salida, '--esperada', str(fin)])
print(f'\n✔ TERMINADO en {time.time() - T0:.0f} s')
for t, dt in pasos: print(f'   {dt:6.1f} s  {t}')
if accion == 'video': print(f'\nSiguiente paso: escribir entrega.json y  python scripts/entrega.py {salida}')
