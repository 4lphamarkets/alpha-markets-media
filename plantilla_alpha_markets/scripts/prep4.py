import numpy as np, wave, json, subprocess, sys
A=sys.argv[1]; R=44100
raw=subprocess.run(['ffmpeg','-v','error','-i',A+'/tmp/voz11.mp3','-ac','1','-ar',str(R),'-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32)
LEAD,GAP,TAIL=0.30,0.45,1.2
C=[
 (0.0,5.70,'s1',[(0.05,2.16,["Binance sufrió","el mayor *robo cripto*"]),(2.26,3.12,["de la historia."]),(3.45,5.56,["*6.300 millones*."])]),
 (5.80,11.0,'s2',[(5.95,10.85,["Todo empezó con","una *falsa entrevista*","de trabajo","y un *malware*","en los equipos","de sus ingenieros."])]),
 (11.05,17.10,'s3',[(11.20,13.46,["El *FBI* apunta a","*TraderTraitor*,"]),(13.69,15.58,["un grupo de hackers","de *Corea del Norte*."]),(15.98,16.93,["Ellos lo niegan."])]),
 (17.15,25.30,'s4',[(17.29,21.54,["Binance cubrió","las pérdidas con","*6.340 millones*","propios."]),(21.93,25.10,["De lo robado,","solo hay unos","*3.000 millones*","congelados."])]),
 (25.32,31.55,'s5',[(25.47,28.59,["Ese día *bitcoin*","cayó bajo","*77.000 dólares*"]),(28.69,31.37,["y se liquidaron","*1.550 millones*."])]),
 (31.58,35.0,'s6',[(31.71,33.13,["Si no quieres","perderte nada,"]),(33.26,34.84,["sígueme en","*Alpha Markets*."])]),
]
out=[np.zeros(int(LEAD*R),np.float32)];t=LEAD;scenes=[];chunks=[];fade=int(.012*R)
for i,(a,b,sid,isl) in enumerate(C):
    seg=x[int(a*R):int(b*R)].copy();seg[:fade]*=np.linspace(0,1,fade);seg[-fade:]*=np.linspace(1,0,fade);off=t-a
    for (ia,ib,ch) in isl:
        w=[len(c.replace('*',''))+4 for c in ch];T=sum(w);u=ia
        for c,wi in zip(ch,w):
            d=wi/T*(ib-ia);chunks.append({'s':sid,'text':c,'t0':round(u+off,3),'t1':round(u+d+off,3)});u+=d
    scenes.append({'id':sid,'v0':round(t,3),'v1':round(t+b-a,3)});out.append(seg);t+=b-a
    if i<len(C)-1: out.append(np.zeros(int(GAP*R),np.float32));t+=GAP
END=t+TAIL;out.append(np.zeros(int(TAIL*R),np.float32));y=np.concatenate(out)
w=wave.open(A+'/tmp/voz_cut.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(R);w.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes());w.close()
fr=lambda v:round(round(v*30)/30,4)
for i,s in enumerate(scenes): s['a']=0 if i==0 else fr((scenes[i-1]['v1']+s['v0'])/2)
for i,s in enumerate(scenes): s['b']=fr(END) if i==len(scenes)-1 else scenes[i+1]['a']
for i,c in enumerate(chunks):
    nxt=chunks[i+1]['t0'] if i+1<len(chunks) else END; c['t1']=round(min(nxt,c['t1']+0.6),3)
json.dump({'end':fr(END),'scenes':scenes,'chunks':chunks},open(A+'/tmp/timeline.json','w'),ensure_ascii=False)
print('END',fr(END))
