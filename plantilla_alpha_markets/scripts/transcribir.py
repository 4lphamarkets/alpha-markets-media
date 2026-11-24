"""TRANSCRIBIR (v23): audio de ElevenLabs → frases con su tiempo de inicio/fin, para escribir el guion de montaje.
Sustituye a asr_run.py / asr_run2.py (llevaban los tiempos de UN vídeo escritos a mano; ahora en archivo/).
uso: python scripts/transcribir.py tmp/voz.mp3 [--modelo <carpeta>] [--salida tmp/transcripcion.json] [--silencio 0.30]
Qué hace: detecta las pausas de la voz, corta en frases y transcribe cada una con Whisper small (sherpa-onnx, en español, sin internet).
Salida: tabla en pantalla + JSON [{"a":1.70,"b":4.10,"texto":"..."}]. Los textos de Whisper pueden fallar en nombres propios y cifras:
el texto bueno es el del GUION; de aquí solo se usan los TIEMPOS (a/b) para prep_analista.py / prep_clasico.py.
Modelo (una sola vez):  pip install sherpa-onnx  y descargar
  https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2  (descomprimir)
Se busca en: --modelo · $ALPHA_WHISPER · ~/.alpha_markets/sherpa-onnx-whisper-small · ./sherpa-onnx-whisper-small · ./modelos/sherpa-onnx-whisper-small"""
import json, os, subprocess, sys
import numpy as np

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
def opt(n, default=None):
    if n in sys.argv:
        i = sys.argv.index(n); v = sys.argv[i + 1]; del sys.argv[i:i + 2]; return v
    return default
modelo = opt('--modelo'); salida = opt('--salida', os.path.join(D, 'tmp', 'transcripcion.json')); pausa = float(opt('--silencio', '0.30'))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
if not args: sys.exit(__doc__)
audio = args[0]
if not os.path.exists(audio): sys.exit(f'No existe {audio}')

SR = 16000
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
if not len(x): sys.exit('No he podido leer el audio (¿ffmpeg instalado?)')

def segmentar(x, pausa):
    """Regiones con voz según la energía (umbral adaptativo: 38 dB por debajo del pico, mínimo -55 dBFS)."""
    h = int(.02 * SR); n = len(x) // h
    rms = np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(1) + 1e-12)
    db = 20 * np.log10(rms); umbral = max(db.max() - 38, -55)
    voz = db > umbral
    reg, ini = [], None
    for i, v in enumerate(voz):
        if v and ini is None: ini = i
        if not v and ini is not None: reg.append([ini, i]); ini = None
    if ini is not None: reg.append([ini, n])
    fus = []                                                    # fundir regiones separadas por menos de `pausa` s
    for r in reg:
        if fus and (r[0] - fus[-1][1]) * .02 < pausa: fus[-1][1] = r[1]
        else: fus.append(r)
    fus = [r for r in fus if (r[1] - r[0]) * .02 >= .25]
    out = []
    for a, b in fus:                                            # Whisper admite ~30 s: partir las regiones largas por su punto más tranquilo
        while (b - a) * .02 > 25:
            mid = a + int(10 / .02); fin = a + int(22 / .02)
            c = mid + int(np.argmin(db[mid:fin])); out.append((a * .02, c * .02)); a = c
        out.append((a * .02, b * .02))
    return [(max(0, round(a - .05, 2)), round(min(len(x) / SR, b + .08), 2)) for a, b in out]

segs = segmentar(x, pausa)
print(f'{len(segs)} frases detectadas en {len(x) / SR:.1f} s de audio')

cands = [modelo, os.environ.get('ALPHA_WHISPER'), os.path.join(os.path.expanduser('~'), '.alpha_markets', 'sherpa-onnx-whisper-small'),
         os.path.join(os.getcwd(), 'sherpa-onnx-whisper-small'), os.path.join(D, 'modelos', 'sherpa-onnx-whisper-small')]
M = next((c for c in cands if c and os.path.exists(os.path.join(c, 'small-encoder.int8.onnx'))), None)
res = []
if not M:
    print('AVISO: no encuentro el modelo Whisper (ver cabecera de este script): se guardan solo los tiempos, sin texto.')
    res = [{'a': a, 'b': b, 'texto': ''} for a, b in segs]
else:
    try: import sherpa_onnx
    except ImportError: sys.exit('Falta sherpa-onnx:  pip install sherpa-onnx')
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M + '/small-encoder.int8.onnx', decoder=M + '/small-decoder.int8.onnx',
                                                     tokens=M + '/small-tokens.txt', language='es', task='transcribe', num_threads=2)
    for a, b in segs:
        s = rec.create_stream(); s.accept_waveform(SR, x[int(a * SR):int(b * SR)]); rec.decode_stream(s)
        res.append({'a': a, 'b': b, 'texto': s.result.text.strip()})
for r in res: print(f"{r['a']:6.2f} - {r['b']:6.2f} | {r['texto']}")
os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
json.dump(res, open(salida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('guardado', salida)
