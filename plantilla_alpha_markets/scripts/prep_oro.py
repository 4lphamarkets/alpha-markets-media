"""Timeline del vídeo ORO Y PLATA (audio sin cortes). uso: python scripts/prep_oro.py"""
import numpy as np, wave, json, subprocess, os
A=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'); R=44100
raw=subprocess.run(['ffmpeg','-v','error','-i',A+'/tmp/voz.wav','-ac','1','-ar',str(R),'-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32); TAIL=1.2
END=len(x)/R+TAIL
y=np.concatenate([x,np.zeros(int(TAIL*R),np.float32)])
w=wave.open(A+'/tmp/voz_cut.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(R);w.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes());w.close()
B=[('s1',0),('s2',9.80),('s3',17.29),('s4',25.99),('s5',30.20),('s6',39.10),('s7',48.00),('s8',52.25)]
C=[('s1',0.05,1.50,["¡Alerta en los","*metales*!"]),('s1',1.80,5.88,["El *oro* se hunde","por debajo de","*3.750 dólares*","la onza."]),('s1',6.23,8.87,["Y la *plata* cae","por debajo","de los *45*."]),('s1',9.20,9.59,["¡*OJO*!"]),
('s2',10.02,14.88,["El oro lleva","*3 días seguidos*","cayendo y toca","su nivel *más bajo*","en *14 meses*,"]),('s2',15.12,17.07,["desde *septiembre*","de *2025*."]),
('s3',17.51,21.32,["Desde sus máximos","de enero pierde","más de un *30 %*,"]),('s3',21.63,23.50,["y la plata...","casi un *60 %*."]),('s3',23.88,25.81,["¿Y por qué?","Por culpa","del *dólar*."]),
('s4',26.25,29.99,["El billete verde","está en su nivel","*más alto* desde","*abril de 2025*."]),
('s5',30.40,32.37,["Y encima,","la *Reserva Federal*","no ayuda."]),('s5',32.71,35.67,["*Musalem* pide","varias *subidas*","de tipos antes","de primavera,"]),('s5',35.97,38.87,["y *Waller* habla","de subir *medio punto*","en diciembre."]),
('s6',39.30,42.11,["Tipos altos y","*dólar fuerte*:","veneno para","el *oro*,"]),('s6',42.35,43.60,["porque no paga","*intereses*."]),('s6',43.92,44.52,["*Resultado*:"]),('s6',44.86,47.65,["¡el oro va camino","de su *peor año*","desde *2015*!"]),
('s7',48.10,50.50,["¿*Oportunidad* o","el *cuchillo*","sigue cayendo?"]),('s7',50.91,52.11,["Cuéntamelo","en *comentarios*."]),
('s8',52.39,55.31,["Sígueme para no","perderte nada de","los *mercados*","financieros,"]),('s8',55.52,57.48,["esto es...","*4LPHA MARKETS*!!"])]
fr=lambda v:round(round(v*30)/30,4)
scenes=[{'id':s,'a':fr(a)} for s,a in B]
for i,s in enumerate(scenes): s['b']=fr(END) if i==len(scenes)-1 else scenes[i+1]['a']
chunks=[]
for sid,a,b,ls in C:
    wts=[len(l.replace('*',''))+4 for l in ls];T=sum(wts);u=a
    for l,wi in zip(ls,wts):
        d=wi/T*(b-a);chunks.append({'s':sid,'text':l,'t0':round(u,3),'t1':round(u+d,3)});u+=d
for i,c in enumerate(chunks):
    nxt=chunks[i+1]['t0'] if i+1<len(chunks) else END; c['t1']=round(min(nxt,c['t1']+0.6),3)
json.dump({'end':fr(END),'scenes':scenes,'chunks':chunks},open(A+'/tmp/timeline.json','w'),ensure_ascii=False)
print('END',fr(END),len(chunks),'chunks')
