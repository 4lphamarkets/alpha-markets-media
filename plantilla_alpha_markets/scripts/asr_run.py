import sherpa_onnx, numpy as np, wave, subprocess, sys
M=sys.argv[1]; wav=sys.argv[2]
segs=[(1.70,2.32),(3.95,9.77),(10.58,15.66),(16.20,16.90),(17.25,19.0),(19.45,21.12),(21.65,22.58),(23.21,27.78),(28.33,29.05),(29.28,31.67),(32.06,35.77),(36.22,39.23),(39.75,40.12),(41.25,45.03),(45.91,48.88),(49.60,50.84),(51.07,52.2)]
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M+'/small-encoder.int8.onnx',decoder=M+'/small-decoder.int8.onnx',tokens=M+'/small-tokens.txt',language='es',task='transcribe',num_threads=2)
raw=subprocess.run(['ffmpeg','-v','error','-i',wav,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32)
for a,b in segs:
    s=rec.create_stream();s.accept_waveform(16000,x[int(a*16000):int(b*16000)]);rec.decode_stream(s)
    print(f"{a:5.2f}-{b:5.2f} | {s.result.text.strip()}")
