"""CONTROL DE CALIDAD del vídeo final (v23).
uso: python scripts/qa_video.py out/video_final.mp4 [--esperada <segundos>]
Comprueba con ffprobe/ffmpeg: 1080x1920, 30 fps, H.264 yuv420p BT.709, AAC 48 kHz estéreo, duración (≈ timeline.end),
volumen (-16 LUFS ± 1,5, pico ≤ -1 dBTP), que no haya fotogramas negros al principio ni silencio largo, y el tamaño.
Sale con código 1 si algo está mal (el vídeo NO debe entregarse hasta corregirlo)."""
import json, os, re, subprocess, sys
D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
esperada = None
if '--esperada' in sys.argv:
    i = sys.argv.index('--esperada'); esperada = float(sys.argv[i + 1]); del sys.argv[i:i + 2]
MAXD = 41
if '--max' in sys.argv:
    i = sys.argv.index('--max'); MAXD = float(sys.argv[i + 1]) + 1; del sys.argv[i:i + 2]
args = [a for a in sys.argv[1:] if not a.startswith('--')]
if not args: sys.exit(__doc__)
vid = args[0]
if not os.path.exists(vid): sys.exit(f'No existe {vid}')
if esperada is None and os.path.exists(os.path.join(D, 'tmp', 'timeline.json')):
    try: esperada = float(json.load(open(os.path.join(D, 'tmp', 'timeline.json'), encoding='utf-8-sig'))['end'])
    except Exception: pass

E, W, OK = [], [], []
def ffprobe():
    o = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', vid], capture_output=True, text=True)
    return json.loads(o.stdout)
P = ffprobe()
v = next((s for s in P['streams'] if s['codec_type'] == 'video'), None)
a = next((s for s in P['streams'] if s['codec_type'] == 'audio'), None)
dur = float(P['format']['duration'])
if not v: E.append('no tiene pista de vídeo')
else:
    if (v['width'], v['height']) != (1080, 1920): E.append(f'resolución {v["width"]}x{v["height"]} (debe ser 1080x1920)')
    else: OK.append('1080x1920')
    num, den = (int(x) for x in v['avg_frame_rate'].split('/'))
    fps = num / den if den else 0
    if abs(fps - 30) > 0.05: E.append(f'{fps:.2f} fps (deben ser 30)')
    else: OK.append('30 fps')
    if v['codec_name'] != 'h264': E.append(f'códec {v["codec_name"]} (debe ser h264)')
    if v.get('pix_fmt') != 'yuv420p': E.append(f'formato de píxel {v.get("pix_fmt")} (debe ser yuv420p)')
    if v.get('color_space') not in ('bt709', None): W.append(f'espacio de color {v.get("color_space")} (esperado bt709)')
    if v.get('profile') not in ('High', None): W.append(f'perfil H.264 {v.get("profile")} (esperado High)')
if not a: E.append('no tiene audio')
else:
    if a['codec_name'] != 'aac': E.append(f'audio {a["codec_name"]} (debe ser aac)')
    if int(a['sample_rate']) != 48000: E.append(f'audio a {a["sample_rate"]} Hz (deben ser 48000)')
    if a.get('channels') != 2: W.append(f'audio con {a.get("channels")} canal(es) (esperado estéreo)')
    if a.get('bit_rate') and int(a['bit_rate']) < 128000: W.append(f'audio a {int(a["bit_rate"]) // 1000} kbps (se pide 320k; el AAC de voz sencilla baja de forma natural, pero por debajo de 128 revisa final.py)')
if esperada is not None:
    if abs(dur - esperada) > 0.15: E.append(f'dura {dur:.2f} s pero el timeline dice {esperada:.2f} s (faltan o sobran fotogramas)')
    else: OK.append(f'duración {dur:.1f} s')
else: OK.append(f'duración {dur:.1f} s')
if dur > MAXD: E.append(f'duración {dur:.1f} s: el máximo es 40 s (regla v24)')
elif dur < 20: W.append(f'duración {dur:.0f} s muy corta (máx. 40 s)')
mb = os.path.getsize(vid) / 1e6
if mb > 250: W.append(f'{mb:.0f} MB: puede ser demasiado para Metricool/Instagram; revisa el CRF')
if a:
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', vid, '-vn', '-af', 'loudnorm=I=-16:TP=-1:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
    m = re.search(r'\{[^{}]*"input_i"[^{}]*\}', r.stderr, re.S)
    if m:
        j = json.loads(m.group(0)); li, tp = float(j['input_i']), float(j['input_tp'])
        if abs(li + 16) > 1.5: W.append(f'volumen {li:.1f} LUFS (objetivo -16 ± 1,5)')
        else: OK.append(f'{li:.1f} LUFS')
        if tp > -0.9: E.append(f'pico {tp:.1f} dBTP (debe ser ≤ -1): recorte al reproducir')
    s = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', vid, '-vn', '-af', 'silencedetect=n=-45dB:d=2.5', '-f', 'null', '-'], capture_output=True, text=True)
    sil = re.findall(r'silence_start: ([\d.]+)', s.stderr)
    if sil: W.append('silencio de más de 2,5 s hacia ' + ', '.join(f'{float(x):.1f}s' for x in sil[:4]) + ' (normal solo en la cola final)')
if v:
    b = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-t', '3', '-i', vid, '-an', '-vf', 'blackdetect=d=0.5:pix_th=0.06', '-f', 'null', '-'], capture_output=True, text=True)
    if re.search(r'black_start:0(\.0+)?\b', b.stderr): E.append('empieza con fotogramas negros (¿falló la carga de fuentes o imágenes?)')
print(f'QA {os.path.basename(vid)}: ' + ' · '.join(OK))
for w in W: print('  ! AVISO :', w)
for e in E: print('  ✘ ERROR :', e)
print('  ' + ('✘ NO ENTREGAR hasta corregirlo' if E else '✔ listo para entregar'))
sys.exit(1 if E else 0)
