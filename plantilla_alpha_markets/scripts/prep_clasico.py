"""Prepara tmp/timeline.json del MODO CLÁSICO (template.html) a partir de un guion en JSON (v23).
Sustituye a los prep_oro.py / prep_nvidia.py / prep3.py / prep4.py (uno por vídeo, con los tiempos escritos a mano; ahora en archivo/).
uso: python scripts/prep_clasico.py tmp/guion_clasico.json      (luego: python scripts/build.py   y   node scripts/render.js stills ...)

guion_clasico.json:
{
 "audio": "tmp/voz.wav",                 # opcional: si existe, el vídeo dura lo que el audio + 1,2 s de cola y se crea tmp/voz_cut.wav
 "tag": "ORO Y PLATA",                   # opcional: texto de la píldora roja de la cabecera
 "escenas": [ {"id":"s1","a":0}, {"id":"s2","a":9.8}, ... ],         # a = segundo en que EMPIEZA cada escena (la 1ª siempre 0)
 "frases":  [ {"s":"s1","a":0.05,"b":1.5,"lineas":["¡Alerta en los","*metales*!"]}, ... ]   # subtítulos: a/b = inicio/fin de la frase en el audio
}
- Las líneas de una frase se reparten el tiempo [a, b] según su longitud; *palabra* = clave.
- Cada subtítulo se alarga hasta 0,6 s (sin pisar al siguiente) para que dé tiempo a leerlo.
- Las ids de escena (s1, s2…) deben existir en template.html (el clásico se adapta a mano para cada vídeo, ver LEEME).
Comprueba el resultado con:  python scripts/validar.py timeline --modo clasico"""
import json, os, subprocess, sys, wave
import numpy as np

A = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if len(sys.argv) < 2: sys.exit(__doc__)
spec = json.load(open(sys.argv[1], encoding='utf-8-sig'))
TAIL, R = 1.2, 44100
fr = lambda v: round(round(v * 30) / 30, 4)
frases = spec.get('frases') or []
if not spec.get('escenas') or not frases: sys.exit('El guion necesita "escenas" y "frases" (ver cabecera de este script).')

END = max(f['b'] for f in frases) + TAIL
audio = spec.get('audio') and os.path.join(A, spec['audio'])
if audio and os.path.exists(audio):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio, '-ac', '1', '-ar', str(R), '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    if not len(x): sys.exit(f'No he podido leer el audio {audio} (¿ffmpeg instalado y archivo correcto?)')
    END = len(x) / R + TAIL
    y = np.concatenate([x, np.zeros(int(TAIL * R), np.float32)])
    os.makedirs(A + '/tmp', exist_ok=True)
    w = wave.open(A + '/tmp/voz_cut.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(R)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    if max(f['b'] for f in frases) > len(x) / R + 0.5: print('AVISO: hay frases que acaban después del audio; revisa los tiempos')
else:
    print('(sin audio: la duración sale de la última frase + cola)')

scenes = [{'id': e['id'], 'a': 0 if i == 0 else fr(e['a'])} for i, e in enumerate(spec['escenas'])]
if abs(spec['escenas'][0]['a']) > 1e-6: print('AVISO: la primera escena se ha puesto en a=0')
for i, s in enumerate(scenes): s['b'] = fr(END) if i == len(scenes) - 1 else scenes[i + 1]['a']
chunks = []
for f in frases:
    ls = f['lineas']; wts = [len(l.replace('*', '')) + 4 for l in ls]; T = sum(wts); u = f['a']
    for l, wi in zip(ls, wts):
        d = wi / T * (f['b'] - f['a']); chunks.append({'s': f['s'], 'text': l, 't0': round(u, 3), 't1': round(u + d, 3)}); u += d
chunks.sort(key=lambda c: c['t0'])
for i, c in enumerate(chunks):
    nxt = chunks[i + 1]['t0'] if i + 1 < len(chunks) else END
    c['t1'] = round(min(nxt, c['t1'] + 0.6), 3)
tl = {'end': fr(END), 'scenes': scenes, 'chunks': chunks}
if spec.get('tag'): tl['tag'] = spec['tag']
os.makedirs(A + '/tmp', exist_ok=True)
json.dump(tl, open(A + '/tmp/timeline.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('timeline.json OK · fin', fr(END), '·', len(scenes), 'escenas ·', len(chunks), 'subtítulos')
