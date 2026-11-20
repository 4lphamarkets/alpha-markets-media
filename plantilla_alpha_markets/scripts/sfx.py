"""Efectos de sonido: mezcla los sonidos reales de /sonidos (catalogo.json) en los eventos del vídeo.
uso: python sfx.py <events.json> <salida.wav> <duración_s> [carpeta_sonidos]

Cada evento {t, type, g}: t = instante en que el sonido debe "golpear" (se alinea con el 'hit' del clip,
así un riser termina justo en t y un whoosh tiene su pico en t). g = ganancia relativa.
Tipos con sonido real (se rotan las variantes para no repetir):
  whoosh, whoosh_in, trans, riser, riser_long, impact (=thud), bass, click, pop, shutter (=clack),
  beep, coin, metal (=ding), flash, shimmer, tech (=glitch)
Tipos sintetizados (sin equivalente en la librería): roll (ruleta de contadores), tick, drop, freeze.
'roll' (números girando) rota entre 6 sonidos DISTINTOS: ruleta, digital, madera, tragaperras, flip-clock y
caja registradora → cada contador del vídeo suena diferente (hasta 6 contadores sin repetir).

v6 — CONTROL DE SATURACIÓN (automático): el vídeo NO debe ir cargado de efectos.
  1. Se descartan los 'tick' de subtítulos (relleno).
  2. Sonidos casi simultáneos (< 0,30 s) se funden en uno: se queda el más importante.
  3. Hueco mínimo de 0,45 s entre efectos (las transiciones de escena siempre se respetan).
  4. Presupuesto: la MITAD de los efectos pedidos (sin bajar de ~1 cada 2,2 s) y nunca más de 1 cada 1,6 s
     (30 s → 14-19 efectos); si sobran, se quitan primero los de menos prioridad (click/pop/beep/coin...).
  opciones:  --factor 0.5  (fracción de los pedidos que se conserva)   --todos  (desactiva el filtro)"""
import json, math, os, sys, wave
import numpy as np

argv = [a for a in sys.argv[1:] if not a.startswith('--')]
FACTOR, TODOS = 0.5, '--todos' in sys.argv
for i, a in enumerate(sys.argv):
    if a == '--factor': FACTOR = float(sys.argv[i + 1]); argv.remove(sys.argv[i + 1])
EV, OUT, DUR = argv[0], argv[1], float(argv[2])
SND = argv[3] if len(argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sonidos')
R = 48000
rng = np.random.default_rng(5)

cat = json.load(open(os.path.join(SND, 'catalogo.json'), encoding='utf-8'))
CLIP = {}
def clip(name):
    if name not in CLIP:
        w = wave.open(os.path.join(SND, cat[name]['file']), 'rb')
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32767
        CLIP[name] = x
    return CLIP[name]
BYCAT = {}
for n, c in cat.items():
    BYCAT.setdefault(c['cat'], []).append(n)

# tipo de evento -> (categoría del catálogo, ganancia base)
MAP = {'whoosh': ('whoosh', .55), 'whoosh_in': ('whoosh_in', .5), 'trans': ('transition', .6), 'riser': ('riser', .45),
       'riser_long': ('riser_long', .35), 'impact': ('impact', .7), 'thud': ('impact', .6), 'bass': ('bass', .6),
       'click': ('click', .35), 'pop': ('pop', .4), 'shutter': ('shutter', .45), 'clack': ('shutter', .45),
       'beep': ('beep', .3), 'coin': ('coin', .4), 'metal': ('metal', .3), 'ding': ('metal', .3), 'flash': ('flash', .45),
       'shimmer': ('shimmer', .9), 'tech': ('tech', .35), 'glitch': ('tech', .35)}
rot = {}

# ---- sintetizados ----
def env(n, a=.004, dec=None):
    t = np.arange(n) / R; e = np.minimum(1, t / a); return e * (np.exp(-t * dec) if dec else 1)
def sweep(n, f0, f1): return np.sin(2 * np.pi * np.cumsum(np.geomspace(f0, f1, n)) / R)
def tick(): n = int(.035 * R); return sweep(n, 1400, 900) * env(n, .002, 90) * .16
def drop(): n = int(.6 * R); return sweep(n, 600, 140) * np.sin(np.linspace(0, np.pi, n)) * .14
def freeze():
    n = int(.8 * R); t = np.arange(n) / R; nz = rng.standard_normal(n); hp = np.diff(nz, prepend=0)
    return (hp * .12 + np.sin(2 * np.pi * np.cumsum(np.linspace(1800, 2600, n)) / R) * .2) * np.sin(np.linspace(0, np.pi, n)) ** 2 * .22
# ---- contadores giratorios: 6 sonidos DISTINTOS que se rotan (nunca el mismo dos veces seguidas) ----
D_ROLL = 1.35
def _clicks(f_fn, dec, ruido, paso_fn, vol, D=D_ROLL):
    n = int(D * R); y = np.zeros(n); t = 0.; k = 0
    while t < D - 0.05:
        m = int(.03 * R); tt = np.arange(m) / R; f = f_fn(k, t / D)
        c = (np.sin(2 * np.pi * f * tt) * (1 - ruido) + rng.standard_normal(m) * ruido) * np.exp(-tt * dec)
        i = int(t * R); y[i:i + m] += c[:n - i]; k += 1; t += paso_fn(t / D)
    return y * vol
def roll_ruleta():      # trinquete agudo que frena (el clásico)
    return _clicks(lambda k, p: 2600 + rng.uniform(-200, 200) - k * 15, 260, .3, lambda p: .028 + .11 * p ** 2.2, .32)
def roll_digital():     # pitidos electrónicos que suben de tono, tipo marcador digital
    return _clicks(lambda k, p: 900 + 1400 * p, 90, .0, lambda p: .045 + .05 * p ** 2, .3)
def roll_madera():      # golpecitos graves de madera, tipo contador mecánico antiguo
    return _clicks(lambda k, p: 420 + rng.uniform(-40, 40), 120, .12, lambda p: .035 + .09 * p ** 1.8, .32)
def roll_slot():        # tragaperras: tic-tic rápido constante + campanita final
    y = np.zeros(int((D_ROLL + .5) * R))
    c = _clicks(lambda k, p: 1800 + (k % 2) * 500, 220, .2, lambda p: .04, .26, D_ROLL - .15); y[:len(c)] += c
    n = int(.5 * R); tt = np.arange(n) / R; s = int((D_ROLL - .1) * R)
    y[s:s + n] += (np.sin(2 * np.pi * 2093 * tt) + .5 * np.sin(2 * np.pi * 3136 * tt)) * np.exp(-tt * 7) * .22
    return y
def roll_flip():        # reloj de paletas (flip clock): clacks secos de papel
    return _clicks(lambda k, p: 3200, 600, .85, lambda p: .06 + .08 * p ** 1.5, .38)
def roll_caja():        # caja registradora: tecleo + "cling" al llegar
    y = _clicks(lambda k, p: 1200 + rng.uniform(-300, 300), 180, .6, lambda p: .07 + .06 * p, .2)
    n = int(.45 * R); tt = np.arange(n) / R
    cling = (np.sin(2 * np.pi * 2637 * tt) + np.sin(2 * np.pi * 3520 * tt) * .6) * np.exp(-tt * 9) * .2
    s = int((D_ROLL - .45) * R); y[s:s + n] += cling[:len(y) - s]
    return y
ROLLS = [roll_ruleta, roll_digital, roll_madera, roll_slot, roll_flip, roll_caja]
_rk = [0]
def roll():
    f = ROLLS[_rk[0] % len(ROLLS)]; _rk[0] += 1; return f()
SYN = dict(roll=roll, tick=tick, drop=drop, freeze=freeze)

mix = np.zeros((int(DUR * R) + R * 4, 2), np.float32)
ev = sorted(json.load(open(EV, encoding='utf-8')), key=lambda e: e['t'])

# ---- control de saturación ----
PRIO = {'trans': 10, 'impact': 9, 'thud': 9, 'bass': 9, 'riser': 7, 'riser_long': 7, 'roll': 6, 'flash': 6,
        'shutter': 5, 'clack': 5, 'tech': 5, 'glitch': 5, 'freeze': 5, 'drop': 5, 'whoosh': 4, 'whoosh_in': 3,
        'metal': 3, 'ding': 3, 'shimmer': 3, 'coin': 2, 'pop': 2, 'click': 1, 'beep': 1, 'tick': 0}
def thin(ev):
    ev = [e for e in ev if e['type'] != 'tick']
    pedidos = len(ev)
    # 1) fundir sonidos casi simultáneos: se queda el de más prioridad (un riser cuenta como su golpe)
    grupos = []
    for e in ev:
        if grupos and float(e['t']) - float(grupos[-1][0]['t']) < .30: grupos[-1].append(e)
        else: grupos.append([e])
    ev = [max(g, key=lambda e: (PRIO.get(e['type'], 2), float(e.get('g', 1)))) for g in grupos]
    # 2) hueco mínimo entre efectos (las transiciones siempre entran)
    out = []
    for e in ev:
        if out and float(e['t']) - float(out[-1]['t']) < .45 and e['type'] != 'trans':
            if PRIO.get(e['type'], 2) > PRIO.get(out[-1]['type'], 2) and out[-1]['type'] != 'trans': out[-1] = e
            continue
        out.append(e)
    # 3) presupuesto: la mitad de lo pedido (pero sin bajar de ~1 cada 2,2 s) y nunca más de 1 cada 1,6 s
    #    → un vídeo de 30 s queda en unos 14-19 efectos
    tope = max(4, min(max(math.ceil(pedidos * FACTOR), math.ceil(DUR / 2.2)), math.ceil(DUR / 1.6)))
    if len(out) > tope:
        orden = sorted(range(len(out)), key=lambda i: (-PRIO.get(out[i]['type'], 2), -float(out[i].get('g', 1)), i))
        keep = set(orden[:tope]); out = [e for i, e in enumerate(out) if i in keep]
    print(f'control de saturación: {pedidos} efectos pedidos -> {len(out)} se conservan (tope {tope})')
    return out
if not TODOS: ev = thin(ev)
last = {}
used = 0
for e in ev:
    ty, t, g = e['type'], float(e['t']), float(e.get('g', 1))
    if ty in SYN:
        s = SYN[ty]()[:, None].repeat(2, 1); start = int(t * R)
    elif ty in MAP:
        c, base = MAP[ty]
        names = BYCAT.get(c)
        if not names:
            continue
        # evita apilar el mismo tipo de sonido dentro de 120 ms
        if t - last.get(c, -9) < .12:
            continue
        last[c] = t
        i = rot.get(c, 0); rot[c] = i + 1
        n = names[i % len(names)]
        s = clip(n) * base; start = int((t - cat[n]['hit']) * R)
    else:
        print('tipo desconocido:', ty); continue
    s = s * g
    if start < 0:
        s = s[-start:]; start = 0
    end = min(len(mix), start + len(s))
    mix[start:end] += s[:end - start]; used += 1
mix = mix[:int(DUR * R)]
pk = np.abs(mix).max()
if pk > 10 ** (-3 / 20):
    mix *= 10 ** (-3 / 20) / pk
w = wave.open(OUT, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(R)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
print('ok', used, 'sonidos colocados')
