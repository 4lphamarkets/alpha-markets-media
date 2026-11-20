"""Mezcla final y exportación en MÁXIMA CALIDAD.
uso: python scripts/final.py <salida.mp4> [voz.wav]
 - voz (por defecto tmp/voz_cut.wav) + efectos tmp/sfx.wav con ducking (los efectos bajan solos cuando habla la voz)
 - normaliza a -16 LUFS, pico -1 dBTP, 48 kHz
 - vídeo tmp/video.mp4 se copia sin recomprimir (ya está en CRF 12) + AAC 320 kbps + faststart"""
import os, subprocess, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
out = sys.argv[1]
voz = sys.argv[2] if len(sys.argv) > 2 else os.path.join(D, 'tmp', 'voz_cut.wav')
sfx = os.path.join(D, 'tmp', 'sfx.wav'); vid = os.path.join(D, 'tmp', 'video.mp4'); mix = os.path.join(D, 'tmp', 'mix.wav')
if os.path.exists(voz):
    fc = ('[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[v][sc];'
          '[1:a]aformat=sample_rates=48000:channel_layouts=stereo[s];'
          '[s][sc]sidechaincompress=threshold=0.04:ratio=5:attack=8:release=280:makeup=1[sd];'
          '[v][sd]amix=inputs=2:normalize=0:duration=longest,loudnorm=I=-16:TP=-1:LRA=11[a]')
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', voz, '-i', sfx, '-filter_complex', fc, '-map', '[a]', '-ar', '48000', mix]
else:
    print('(sin voz: solo efectos)')
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', sfx, '-af', 'loudnorm=I=-16:TP=-1:LRA=11', '-ar', '48000', mix]
subprocess.run(cmd, check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', mix, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-shortest', '-movflags', '+faststart', out], check=True)
print('exportado', out)
