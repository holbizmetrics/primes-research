#!/usr/bin/env python3
import struct,math,wave,os
R=22050; os.makedirs("audio",exist_ok=True)
z=[14.1347,21.022,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738]
b=110.0; ns=int(4.0*R); s=[0.0]*ns
for k in range(10):
    f=b*z[k]/z[0]
    if f>R/2: continue
    a=1.0/(1+k*0.25); st=int(k*ns/12)
    dp=2*math.pi*f/R; p=0
    for t in range(st,ns):
        fd=min(1.0,(t-st)/(0.3*R)); s[t]+=a*fd*math.sin(p); p+=dp
with wave.open("audio/15_zero_chord.wav",'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(R)
    mx=max(abs(x) for x in s) or 1
    w.writeframes(b''.join(struct.pack('<h',int(x/mx*30000)) for x in s))
print("15_zero_chord.wav 4s")
