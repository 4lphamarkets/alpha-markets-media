"""Prepara tmp/timeline.json del MODO ANALISTA (v22) a partir de un guion con escenas.
uso: python scripts/prep_analista.py tmp/guion_analista.json      (luego: python scripts/build.py analista)

guion_analista.json:
{
 "audio": "tmp/voz.wav",                       # opcional: si existe se crea tmp/voz_cut.wav con 1,2 s de cola (como prep_oro.py)
 "kicker_global": "",                          # opcional: kicker fijo en todo el vídeo (si no, cada escena pone el suyo)
 "scenes": [
  {"id":"s1","a":0.0,"kicker":"Wall Street · semana 23-27 nov","kickerTone":"r","bg":"img/xxx.jpg",
   "segs":[[0.35,2.9,"La bolsa se juega *la semana*"],[2.9,6.1,"en solo *tres días y medio*"]],    # [inicio_s, fin_s, texto] con *clave*
   "comps":[{"type":"pill","text":"...","at":0.2},{"type":"card","text":"...","chunk":0}, ...]},   # ver ESTILO_ANALISTA.md
  ...
 ]
}
- "a" = segundo del audio en que EMPIEZA la escena (la escena acaba donde empieza la siguiente; la última, al final del audio + cola).
- Cada seg se parte solo en líneas de <= 26 caracteres, repartidas por tiempo según su longitud.
- En "comps": "at" = segundos desde el inicio de la escena; "chunk" = índice del subtítulo de la escena (aparece cuando se dice).
"""
import json, os, re, subprocess, sys, wave
import numpy as np
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
spec = json.load(open(sys.argv[1] if len(sys.argv) > 1 else A + '/tmp/guion_analista.json', encoding='utf-8-sig'))
TAIL, FPS = 1.2, 30
fr = lambda v: round(round(v * 30) / 30, 4)

def split_lines(text, maxc=26):
    """Parte la frase en las líneas MÍNIMAS (<= maxc caracteres) y BALANCEADAS: «y viene de caer siete días seguidos» →
    «y viene de caer» / «siete días seguidos» (v23: antes salía «...siete días» + «SEGUIDOS» suelto, una palabra huérfana en pantalla)."""
    words = text.split(); plain = lambda ws: len(' '.join(ws).replace('*', ''))
    n = max(1, -(-plain(words) // maxc))                      # nº mínimo de líneas
    def mejores(ws, k):                                       # reparto de ws en k líneas minimizando la más larga (y luego el desequilibrio)
        if k == 1: return (plain(ws), plain(ws) ** 2), [ws]
        best = None
        for c in range(1, len(ws) - k + 2):
            sc, rest = mejores(ws[c:], k - 1)
            cand = ((max(plain(ws[:c]), sc[0]), plain(ws[:c]) ** 2 + sc[1]), [ws[:c]] + rest)
            if best is None or cand[0] < best[0]: best = cand
        return best
    n = min(n, len(words))
    sc, parts = mejores(words, n)
    if sc[0] > maxc and n < len(words):                       # alguna palabra larga no cabe: una línea más
        sc2, parts2 = mejores(words, n + 1)
        if sc2[0] < sc[0]: parts = parts2
    lines = [' '.join(p) for p in parts]
    # el * debe cerrarse dentro de cada línea
    out, open_ = [], False
    for l in lines:
        if open_: l = '*' + l
        open_ = l.count('*') % 2 == 1
        if open_: l += '*'
        out.append(l)
    return out

END = max([b for s in spec['scenes'] for _, b, _ in s.get('segs', [])] or [0]) + TAIL
if spec.get('audio') and os.path.exists(os.path.join(A, spec['audio'])):
    R = 44100
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(A, spec['audio']), '-ac', '1', '-ar', str(R), '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    if not len(x): sys.exit('No he podido leer el audio (¿ffmpeg instalado y archivo correcto?)')
    END = len(x) / R + TAIL
    y = np.concatenate([x, np.zeros(int(TAIL * R), np.float32)])
    os.makedirs(A + '/tmp', exist_ok=True)
    w = wave.open(A + '/tmp/voz_cut.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(R)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

scenes, chunks = [], []
for i, s in enumerate(spec['scenes']):
    sc = {k: v for k, v in s.items() if k not in ('segs',)}
    sc['a'] = 0 if i == 0 else fr(s['a']); scenes.append(sc)   # v23: la 1ª escena siempre en 0 (si no, antes de su inicio se vería la última)
for i, sc in enumerate(scenes): sc['b'] = fr(END) if i == len(scenes) - 1 else scenes[i + 1]['a']
for s in spec['scenes']:
    for a, b, text in s.get('segs', []):
        ls = split_lines(text); wts = [len(l.replace('*', '')) + 3 for l in ls]; T = sum(wts); u = a
        for l, wi in zip(ls, wts):
            d = wi / T * (b - a); chunks.append({'s': s['id'], 'text': l, 't0': round(u, 3), 't1': round(u + d, 3)}); u += d
for i, c in enumerate(chunks):
    nxt = chunks[i + 1]['t0'] if i + 1 < len(chunks) else END
    c['t1'] = round(min(nxt, c['t1'] + 0.5), 3)
tl = {'end': fr(END), 'scenes': scenes, 'chunks': chunks}
if spec.get('kicker_global'): tl['kicker_global'] = spec['kicker_global']
os.makedirs(A + '/tmp', exist_ok=True)
json.dump(tl, open(A + '/tmp/timeline.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('timeline.json OK · fin', fr(END), '·', len(scenes), 'escenas ·', len(chunks), 'subtítulos')
