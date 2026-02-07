#!/usr/bin/env python3
"""Destructive vs Constructive zero pairs"""
import struct,math,wave,os
R=22050; os.makedirs("audio",exist_ok=True)
z=[14.1347,21.022,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271]
b=220.0; s=[]; pd=int(2.0*R); gap=int(0.4*R)
# pairs: (i,j,label) — from overtone analysis
pairs=[(2,3,"DESTRUCTIVE g3+g4"),(3,4,"CONSTRUCTIVE g4+g5"),
       (1,3,"DESTRUCTIVE g2+g4"),(1,5,"CONSTRUCTIVE g2+g6")]
for i,j,lb in pairs:
    f1=b*z[i]/z[0]; f2=b*z[j]/z[0]
    for t in range(pd):
        e=1.0-0.3*t/pd
        s.append(0.5*e*(math.sin(2*math.pi*f1*t/R)+math.sin(2*math.pi*f2*t/R)))
    s.extend([0]*gap)
with wave.open("audio/19_destructive_vs_constructive.wav",'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(R)
    mx=max(abs(x) for x in s) or 1
    w.writeframes(b''.join(struct.pack('<h',int(x/mx*30000)) for x in s))
print("19_destructive_vs_constructive.wav %.1fs" % (len(s)/R))
