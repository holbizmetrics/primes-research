#!/usr/bin/env python3
import struct,math,wave,os
R=22050; os.makedirs("audio",exist_ok=True)
z=[14.1347,21.022,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738]
ns=int(3.0*R); s=[]
for t in range(ns):
    lx=1.0+6.0*t/ns; xh=math.exp(lx/2); o=0.0
    for g in z:
        d=0.25+g*g; ph=g*lx
        o-=2*(xh*math.cos(ph)*0.5/d-xh*math.sin(ph)*(-g/d))
    s.append(o/math.exp(lx))
with wave.open("audio/16_explicit_formula.wav",'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(R)
    mx=max(abs(x) for x in s) or 1
    w.writeframes(b''.join(struct.pack('<h',int(x/mx*30000)) for x in s))
print("16 done %.1fs" % (len(s)/R))
