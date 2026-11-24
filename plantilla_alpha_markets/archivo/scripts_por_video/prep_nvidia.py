"""Timeline del vídeo NVIDIA (audio sin cortes, ElevenLabs Jaime). uso: python scripts/prep_nvidia.py"""
import numpy as np, wave, json, subprocess, os
A=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'); R=44100
raw=subprocess.run(['ffmpeg','-v','error','-i',A+'/tmp/voz.wav','-ac','1','-ar',str(R),'-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32); TAIL=1.2
END=len(x)/R+TAIL
y=np.concatenate([x,np.zeros(int(TAIL*R),np.float32)])
w=wave.open(A+'/tmp/voz_cut.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(R);w.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes());w.close()
B=[('s1',0),('s2',9.0),('s3',24.5),('s4',45.0),('s5',57.0),('s6',65.5),('s7',73.4),('s8',86.9),('s9',95.5)]
C=[
('s1',0.05,3.40,["Nvidia pierde","un *33 %* en","solo *2 semanas*..."]),
('s1',3.50,6.00,["¡y acaba de","*duplicar* sus","*ingresos*!"]),
('s1',6.48,7.40,["¿*Cómo* es","posible?"]),
('s1',7.87,8.85,["Vamos por","*partes*."]),
('s2',9.20,13.45,["El viernes se","desplomó un *14 %*","y cerró en","*125 dólares*"]),
('s2',13.83,15.96,["En la semana","pierde casi","un *23 %*."]),
('s2',16.36,18.85,["Hace dos viernes","valía *186*."]),
('s2',19.25,21.46,["Siete semanas","*seguidas* en rojo:"]),
('s2',21.77,24.23,["su *peor racha*","desde la crisis","de *2008*."]),
('s3',24.75,27.40,["*Primera causa*:","el *escándalo*","de su fundador."]),
('s3',27.89,31.10,["El *8 de noviembre*","el consejo abre","una *investigación*"]),
('s3',31.25,35.55,["tras saberse que","*Jensen Huang* fue objetivo","de una operación de","*inteligencia extranjera*."]),
('s3',36.00,38.82,["Admite una relación","*extramatrimonial* con","*Alice Huang*,"]),
('s3',39.08,40.34,["ejecutiva de","*Megaspeed*,"]),
('s3',40.60,44.82,["a quien EE. UU. señala","como *presunta agente*","*china*."]),
('s4',45.21,48.61,["El *12 de noviembre*","*dimite* tras","*33 años*."]),
('s4',48.96,51.35,["*Colette Kress*","queda como CEO","*interina*."]),
('s4',51.72,56.69,["En solo *2 sesiones*","se esfumaron","*430.000 millones*","de dólares."]),
('s5',57.08,58.90,["*Segunda causa*:","la *SEC*."]),
('s5',59.23,62.46,["Según *Reuters*,","investiga sus *prácticas*","*contables*,"]),
('s5',62.71,65.28,["y *California* también","la tiene en","el *punto de mira*."]),
('s6',65.69,69.20,["*Tercera*: el miedo","a la *burbuja*","de la *IA*."]),
('s6',69.52,73.27,["Dudan de que tanto","gasto en chips","dé *beneficios*."]),
('s7',73.63,77.70,["Y lo más loco:","el *17 de noviembre*","*resultados récord*."]),
('s7',78.04,80.21,["*115.844 millones*","en *ingresos*,"]),
('s7',80.46,82.15,["un *103 %* más,"]),
('s7',82.46,84.93,["y *65.287 millones*","de *beneficio*."]),
('s7',85.28,86.60,["Y aun así...","*¡cae!*"]),
('s8',87.02,89.14,["¿Y *ahora*?","*Nuevo CEO*,"]),
('s8',89.36,93.59,["resolver las *investigaciones*","y demostrar que el negocio","aguanta *sin su fundador*."]),
('s8',93.90,95.33,["*Volatilidad*","asegurada."]),
('s9',95.69,99.54,["Sígueme para no","perderte nada de","los *mercados*","financieros,"]),
('s9',99.83,101.04,["esto es...","*4LPHA MARKETS*!!"]),
]
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
