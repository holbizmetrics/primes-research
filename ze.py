#!/usr/bin/env python3
"""Explicit formula oscillation as audio"""
import struct,math,wave,os
R=22050; os.makedirs("audio",exist_ok=True)
z=[14.1347,21.022,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738,
   52.9703,56.4462,59.347,60.8318,65.1125,67.0798,69.5464,72.0672,75.7047,77.1448]
ns=int(5.0*R); s=[]
for t in range(ns):
    lx=1.0+7.0*t/ns; xh=math.exp(lx/2); osc=0.0
    for g in z:
        d=0.25+g*g; rr=0.5/d; ri=-g/d; ph=g*lx
        re=xh*math.cos(ph); im=xh*math.sin(ph)
        osc-=2*(re*rr-im*ri)
    s.append(osc/math.exp(lx))
with wave.open("audio/16_explicit_formula.wav",'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(R)
    mx=max(abs(x) for x in s) or 1
    w.writeframes(b''.join(struct.pack('<h',int(x/mx*30000)) for x in s))
print("16_explicit_formula.wav 5s")
