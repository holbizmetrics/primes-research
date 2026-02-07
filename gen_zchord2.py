#!/usr/bin/env python3
import struct, math, wave, os
R=22050
zeros=[]
with open('z.txt') as f:
    for l in f:
        l=l.strip()
        if l: zeros.append(float(l))
zeros=zeros[:15]
base=110.0; dur=int(6.0*R); smp=[0.0]*dur
for k in range(len(zeros)):
    freq=base*zeros[k]/zeros[0]
    if freq>R/2: continue
    amp=1.0/(1+k*0.2); start=int(k*dur/(len(zeros)+2))
    dp=2*math.pi*freq/R; ph=0
    for t in range(start,dur):
        fd=min(1.0,(t-start)/(0.4*R))
        smp[t]+=amp*fd*math.sin(ph); ph+=dp
os.makedirs("audio",exist_ok=True)
with wave.open("audio/15_zero_chord.wav",'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(R)
    mx=max(abs(x) for x in smp) or 1
    w.writeframes(b''.join(struct.pack('<h',int(x/mx*30000)) for x in smp))
print("audio/15_zero_chord.wav (%.1fs)" % (len(smp)/R))
