"""Prepara tmp/timeline.json del MODO DINÁMICO (v25) a partir de un guion con escenas.
uso: python scripts/prep_dinamico.py tmp/guion_dinamico.json     (luego: python scripts/build.py dinamico)

guion_dinamico.json:
{
 "audio": "tmp/voz.mp3",                 # opcional: crea tmp/voz_cut.wav con 1,2 s de cola
 "tag": "MIEDO EXTREMO", "tagTone": "" | "g" | "y",   # píldora de la cabecera (cada escena puede poner la suya: "tag")
 "fx": [{"at":12.3,"type":"crash","dur":2.4,"text":"ALERTA"}],     # efectos globales (tiempo absoluto)
 "scenes": [
  {"id":"s1","a":0.0,"tag":"...","mood":"red|green|gold|","comps":[...],"fx":[{"at":1.0,"type":"flash"}],
   "segs":[[0.35,2.9,"¿Comprar *bitcoin* en miedo extremo?"]]}      # [inicio_s, fin_s, texto] con *verde* #rojo# ^dorado^
 ]
}
Efectos (fx): flash{color} · shake{dur,amp} · zoom{dur,amt} · glitch{dur} · pump{dur} (rayos + flash verde) · crash{dur,text} (PSICOSIS: pantalla roja, sirenas, glitch, sacudida)
Componentes (comps, cada uno con "at" = segundos desde el inicio de la escena, "y" = posición vertical, "enter"): ver ESTILO_DINAMICO.md
"""
import json, os, re, subprocess, sys, wave
import numpy as np
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
spec = json.load(open(sys.argv[1] if len(sys.argv) > 1 else A + '/tmp/guion_dinamico.json', encoding='utf-8-sig'))
TAIL = 1.2
fr = lambda v: round(round(v * 30) / 30, 4)
MAXC = int(spec.get('maxc', 30))

def partir(text):
    """Parte una frase en trozos de <= MAXC caracteres (sin cortar palabras ni marcas)."""
    words = text.split(); out, cur = [], []
    plain = lambda ws: len(' '.join(ws).replace('*', '').replace('#', '').replace('^', ''))
    for w in words:
        if cur and plain(cur + [w]) > MAXC: out.append(cur); cur = []
        cur.append(w)
    if cur: out.append(cur)
    # evita un trozo final de 1 palabra corta
    if len(out) > 1 and len(out[-1]) == 1 and plain(out[-1]) <= 4: out[-2] += out.pop()
    res, ab = [], None
    for ws in out:   # las marcas * # ^ se cierran dentro de cada trozo
        t = ' '.join(ws)
        if ab: t = ab + t
        ab = None
        for m in '*#^':
            if t.count(m) % 2: t += m; ab = m
        res.append(t)
    return res

def palabras(text, t0, t1):
    toks = text.split(); ws = []; mark = None
    for tk in toks:
        k = None; clean = tk
        for m, c in (('*', 'k'), ('#', 'r'), ('^', 'y')):
            if m in tk:
                if mark == m: k = c; mark = None
                elif mark is None and tk.startswith(m): mark = m; k = c
                if mark == m and not tk.count(m) % 2: pass
                clean = clean.replace(m, '')
        if mark and k is None: k = {'*': 'k', '#': 'r', '^': 'y'}[mark]
        ws.append([clean, k])
    # el color se mantiene entre las palabras marcadas
    cur = None; res = []
    stack = None
    for tk in toks:
        starts = [m for m in '*#^' if tk.startswith(m)]
        if starts: stack = starts[0]
        col = {'*': 'k', '#': 'r', '^': 'y'}.get(stack)
        clean = tk.replace('*', '').replace('#', '').replace('^', '')
        res.append({'w': clean, 'k': col})
        ends = [m for m in '*#^' if tk.endswith(m) and len(tk) > 1]
        if ends and stack == ends[0] and not starts: stack = None
        elif ends and starts and tk.count(ends[0]) >= 2: stack = None
    L = [len(w['w']) + 2 for w in res]; T = sum(L) or 1; u = t0; d = (t1 - t0) * .92
    for w, l in zip(res, L):
        w['t0'] = round(u, 3); u += l / T * d
    return res

END = max([b for s in spec['scenes'] for _, b, _ in s.get('segs', [])] or [0]) + TAIL
if spec.get('audio') and os.path.exists(os.path.join(A, spec['audio'])):
    R = 44100
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(A, spec['audio']), '-ac', '1', '-ar', str(R), '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    if not len(x): sys.exit('No he podido leer el audio')
    END = len(x) / R + TAIL
    y = np.concatenate([x, np.zeros(int(TAIL * R), np.float32)])
    os.makedirs(A + '/tmp', exist_ok=True)
    w = wave.open(A + '/tmp/voz_cut.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(R)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

scenes, chunks = [], []
for i, s in enumerate(spec['scenes']):
    sc = {k: v for k, v in s.items() if k != 'segs'}
    sc['a'] = 0 if i == 0 else fr(s['a']); scenes.append(sc)
for i, sc in enumerate(scenes): sc['b'] = fr(END) if i == len(scenes) - 1 else scenes[i + 1]['a']
for s in spec['scenes']:
    for a, b, text in s.get('segs', []):
        ps = partir(text); wts = [len(p.replace('*', '').replace('#', '').replace('^', '')) + 3 for p in ps]; T = sum(wts); u = a
        for p, wi in zip(ps, wts):
            d = wi / T * (b - a); chunks.append({'s': s['id'], 'text': p, 't0': round(u, 3), 't1': round(u + d, 3)}); u += d
for i, c in enumerate(chunks):
    nxt = chunks[i + 1]['t0'] if i + 1 < len(chunks) else END
    c['t1'] = round(min(nxt, c['t1'] + 0.6), 3)
    c['words'] = palabras(c['text'], c['t0'], c['t1'])
tl = {'end': fr(END), 'scenes': scenes, 'chunks': chunks}
for k in ('tag', 'tagTone', 'fx'):
    if spec.get(k): tl[k] = spec[k]
os.makedirs(A + '/tmp', exist_ok=True)
json.dump(tl, open(A + '/tmp/timeline.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('timeline.json OK · fin', fr(END), '·', len(scenes), 'escenas ·', len(chunks), 'subtítulos')
