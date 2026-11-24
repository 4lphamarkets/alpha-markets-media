"""Mezcla final y exportación en MÁXIMA CALIDAD.
uso: python scripts/final.py <salida.mp4> [voz.wav]
 - voz (por defecto tmp/voz_cut.wav) + efectos tmp/sfx.wav con ducking (los efectos bajan solos cuando habla la voz)
 - normaliza a -16 LUFS, pico -1 dBTP, 48 kHz  (v23: en DOS PASADAS con loudnorm lineal → llega al objetivo con precisión;
   antes, una sola pasada dinámica dejaba el volumen final entre -17 y -14 LUFS según el vídeo)
 - vídeo tmp/video.mp4 se copia sin recomprimir (ya está en CRF 12) + AAC 320 kbps + faststart"""
import json, os, re, subprocess, sys
D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if len(sys.argv) < 2: sys.exit(__doc__)
out = sys.argv[1]
voz = sys.argv[2] if len(sys.argv) > 2 else os.path.join(D, 'tmp', 'voz_cut.wav')
sfx = os.path.join(D, 'tmp', 'sfx.wav'); vid = os.path.join(D, 'tmp', 'video.mp4')
raw, mix = os.path.join(D, 'tmp', 'mix_raw.wav'), os.path.join(D, 'tmp', 'mix.wav')
if not os.path.exists(vid): sys.exit('Falta tmp/video.mp4: renderiza antes (node scripts/render.js video).')
OBJ = 'I=-16:TP=-1:LRA=11'

def ff(*a): subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)

# 1) mezcla sin normalizar
if os.path.exists(voz) and os.path.exists(sfx):
    fc = ('[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[v][sc];'
          '[1:a]aformat=sample_rates=48000:channel_layouts=stereo[s];'
          '[s][sc]sidechaincompress=threshold=0.04:ratio=5:attack=8:release=280:makeup=1[sd];'
          '[v][sd]amix=inputs=2:normalize=0:duration=longest[a]')
    ff('-i', voz, '-i', sfx, '-filter_complex', fc, '-map', '[a]', '-ar', '48000', raw)
elif os.path.exists(voz):
    print('(sin efectos: solo voz)'); ff('-i', voz, '-af', 'aformat=sample_rates=48000:channel_layouts=stereo', '-ar', '48000', raw)
elif os.path.exists(sfx):
    print('(sin voz: solo efectos)'); ff('-i', sfx, '-ar', '48000', raw)
else:
    sys.exit('No hay audio: faltan tmp/voz_cut.wav y tmp/sfx.wav')

# 2) medir (pasada 1) y aplicar con los valores medidos (pasada 2, lineal)
p = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', raw, '-af', f'loudnorm={OBJ}:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
m = re.search(r'\{[^{}]*"input_i"[^{}]*\}', p.stderr, re.S)
try:
    j = json.loads(m.group(0)); assert float(j['input_i']) > -70       # audio casi mudo = medición inútil
    af = (f"loudnorm={OBJ}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
          f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    print(f"medido: {float(j['input_i']):.1f} LUFS, pico {float(j['input_tp']):.1f} dBTP → objetivo -16 LUFS")
except Exception:
    af = f'loudnorm={OBJ}'; print('AVISO: no he podido medir el volumen; normalizo en una sola pasada')
ff('-i', raw, '-af', af, '-ar', '48000', mix)

# 3) vídeo + audio
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
ff('-i', vid, '-i', mix, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-ar', '48000',
   '-shortest', '-movflags', '+faststart', out)
print('exportado', out)
