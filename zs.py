#!/usr/bin/env python3
"""Inversion sweep: gamma_k^alpha for alpha = 1, 0.5, 0, -0.5, -1"""
import struct,math,wave,os
R=22050; os.makedirs("audio",exist_ok=True)
z=[14.1347,21.022,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738]
b=110.0; sd=int(2.5*R); gap=int(0.25*R); s=[]
for alpha in [1.0, 0.5, 0.0, -0.5, -1.0]:
    seg=[0.0]*sd
    if alpha==0:
        freqs=[b*2]*len(z)
    else:
        mp=[g**alpha for g in z]; mn=min(mp); mx=max(mp)
        if mx>mn: freqs=[b+(b*4)*(m-mn)/(mx-mn) for m in mp]
        else: freqs=[b*2]*len(z)
    for k in range(len(z)):
        f=freqs[k]
        if f>R/2 or f<20: continue
        a=1.0/(1+k*0.3); dp=2*math.pi*f/R; ph=0
        for t in range(sd):
            fd=min(1.0,t/(0.15*R))*min(1.0,(sd-t)/(0.15*R))
            seg[t]+=a*fd*math.sin(ph); ph+=dp
    s.extend(seg); s.extend([0]*gap)
with wave.open("audio/20_zero_inversion_sweep.wav",'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(R)
    mx=max(abs(x) for x in s) or 1
    w.writeframes(b''.join(struct.pack('<h',int(x/mx*30000)) for x in s))
print("20_zero_inversion_sweep.wav %.1fs" % (len(s)/R))
