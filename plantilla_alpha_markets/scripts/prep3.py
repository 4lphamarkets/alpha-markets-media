import numpy as np, wave, json, subprocess, sys
A=sys.argv[1]; R=44100
raw=subprocess.run(['ffmpeg','-v','error','-i',A+'/tmp/voz.m4a','-ac','1','-ar',str(R),'-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32)
LEAD,GAP=0.30,0.35
# (src_start, src_end, scene, islands[(src_a,src_b,[chunks])])
C=[
 (3.95,9.77,'s1',[(4.00,9.72,["Binance sufrió","el mayor *robo cripto*","de la historia:","*6.300 millones*","de dólares."])]),
 (10.58,15.66,'s2',[(10.63,15.61,["Todo empezó con","una *falsa entrevista*","de trabajo","y un *malware*","en los equipos","de sus ingenieros."])]),
 (16.20,22.58,'s3',[(16.25,16.85,["El *FBI*"]),(17.30,18.95,["apunta a","*TraderTraitor*,"]),(19.50,21.07,["hackers de","*Corea del Norte*."]),(21.70,22.53,["Ellos lo niegan."])]),
 (23.21,31.67,'s4',[(23.26,27.73,["Binance cubrió","las pérdidas con","*6.340 millones*","propios."]),(28.38,29.00,["De lo robado,"]),(29.33,31.62,["solo hay unos","*3.000 millones*","congelados."])]),
 (32.06,39.23,'s5',[(32.11,35.72,["Ese día *bitcoin*","cayó por debajo","de los *77.000 dólares*."]),(36.27,39.18,["y se liquidaron","*1.550 millones*."])]),
 (49.60,52.20,'s6',[(49.65,50.79,["Para más, sígueme"]),(51.12,52.15,["en *Alpha Markets*."])]),
]
out=[np.zeros(int(LEAD*R),np.float32)];t=LEAD;scenes=[];chunks=[]
fade=int(.015*R)
for i,(a,b,sid,isl) in enumerate(C):
    seg=x[int(a*R):int(b*R)].copy();seg[:fade]*=np.linspace(0,1,fade);seg[-fade:]*=np.linspace(1,0,fade)
    off=t-a
    for (ia,ib,ch) in isl:
        w=[len(c.replace('*',''))+4 for c in ch];T=sum(w);u=ia
        for c,wi in zip(ch,w):
            d=wi/T*(ib-ia);chunks.append({'s':sid,'text':c,'t0':round(u+off,3),'t1':round(u+d+off,3)});u+=d
    scenes.append({'id':sid,'v0':round(t,3),'v1':round(t+b-a,3)})
    out.append(seg);t+=b-a
    if i<len(C)-1: out.append(np.zeros(int(GAP*R),np.float32));t+=GAP
END=round(t+1.0,3);out.append(np.zeros(int(1.0*R),np.float32))
y=np.concatenate(out)
w=wave.open(A+'/tmp/voz_cut.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(R);w.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes());w.close()
# scene bounds: boundary midway in gaps, frame aligned
fr=lambda v:round(round(v*30)/30,4)
for i,s in enumerate(scenes):
    s['a']=0 if i==0 else fr((scenes[i-1]['v1']+s['v0'])/2)
for i,s in enumerate(scenes):
    s['b']=fr(END) if i==len(scenes)-1 else scenes[i+1]['a']
# extend chunk end to next chunk start (max +0.6) for readability
for i,c in enumerate(chunks):
    nxt=chunks[i+1]['t0'] if i+1<len(chunks) else END
    c['t1']=round(min(nxt,c['t1']+0.6),3)
json.dump({'end':fr(END),'scenes':scenes,'chunks':chunks},open(A+'/tmp/timeline.json','w'),ensure_ascii=False,indent=0)
print('END',fr(END));[print(s) for s in scenes]
