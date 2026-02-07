#!/usr/bin/env python3
"""Inverted zero tones: 1/gamma_k as frequencies"""
import struct,math,wave,os
R=22050; os.makedirs("audio",exist_ok=True)
z=[14.1347,21.022,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738,
   52.9703,56.4462,59.347,60.8318,65.1125]
inv=[1.0/g for g in z]; imx=max(inv)
s=[]; td=int(0.9*R); gap=int(0.08*R)
for k in range(len(inv)):
    f=220.0*inv[k]/imx; a=1.0/(1+k*0.15)
    for t in range(td):
        e=math.exp(-2.0*t/td); s.append(a*e*math.sin(2*math.pi*f*t/R))
    s.extend([0]*gap)
with wave.open("audio/17_inverted_zeros.wav",'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(R)
    mx=max(abs(x) for x in s) or 1
    w.writeframes(b''.join(struct.pack('<h',int(x/mx*30000)) for x in s))
print("17_inverted_zeros.wav %.1fs" % (len(s)/R))
