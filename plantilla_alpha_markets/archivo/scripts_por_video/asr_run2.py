import sherpa_onnx, numpy as np, wave, subprocess, sys
M=sys.argv[1]; wav=sys.argv[2]
segs=[(0,3.2),(3.4,5.6),(5.9,10.9),(11.15,13.5),(13.65,15.62),(15.93,16.97),(17.25,21.59),(21.89,25.15),(25.42,31.41),(31.66,35.0)]
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M+'/small-encoder.int8.onnx',decoder=M+'/small-decoder.int8.onnx',tokens=M+'/small-tokens.txt',language='es',task='transcribe',num_threads=2)
raw=subprocess.run(['ffmpeg','-v','error','-i',wav,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32)
for a,b in segs:
    s=rec.create_stream();s.accept_waveform(16000,x[int(a*16000):int(b*16000)]);rec.decode_stream(s)
    print(f"{a:5.2f}-{b:5.2f} | {s.result.text.strip()}")
