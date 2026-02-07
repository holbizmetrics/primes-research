#!/usr/bin/env python3
import struct,math,wave,os
R=22050; os.makedirs("audio",exist_ok=True)
z=[14.1347,21.022,25.0109,30.4249,32.9351,37.5862]
b=130.0; sd=int(1.5*R); gp=int(0.15*R); s=[]
for alpha in [1.0,0.5,0.0,-0.5,-1.0]:
    sg=[0.0]*sd
    if alpha==0: fs=[b*2]*6
    else:
        mp=[g**alpha for g in z]; mn=min(mp); mx=max(mp)
        fs=[b+(b*3)*(m-mn)/(mx-mn) for m in mp]
    for k in range(6):
        f=fs[k]; a=1.0/(1+k*0.3); dp=2*math.pi*f/R; ph=0
        for t in range(sd):
            fd=min(1.0,t/(0.08*R))*min(1.0,(sd-t)/(0.08*R))
            sg[t]+=a*fd*math.sin(ph); ph+=dp
    s.extend(sg); s.extend([0]*gp)
with wave.open("audio/20_zero_inversion_sweep.wav",'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(R)
    mx=max(abs(x) for x in s) or 1
    w.writeframes(b''.join(struct.pack('<h',int(x/mx*30000)) for x in s))
print("20 done")
