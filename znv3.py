#!/usr/bin/env python3
import struct,math,wave,os
R=22050; os.makedirs("audio",exist_ok=True)
z=[14.1347,21.022,25.0109,30.4249,32.9351,37.5862,40.9187]
b=130.0; hd=int(1.5*R); g=int(0.2*R); s=[0.0]*(2*hd+g)
for k in range(7):
    f=b*z[k]/z[0]; a=1.0/(1+k*0.3); dp=2*math.pi*f/R; ph=0
    for t in range(hd): fd=min(1.0,t/(0.1*R))*min(1.0,(hd-t)/(0.15*R)); s[t]+=a*fd*math.sin(ph); ph+=dp
iv=[1.0/x for x in z]; im=max(iv)
for k in range(7):
    f=b*iv[k]/im*(z[-1]/z[0]); a=1.0/(1+k*0.3); dp=2*math.pi*f/R; ph=0; st=hd+g
    for t in range(st,2*hd+g): fd=min(1.0,(t-st)/(0.1*R))*min(1.0,(2*hd+g-t)/(0.15*R)); s[t]+=a*fd*math.sin(ph); ph+=dp
with wave.open("audio/18_normal_vs_inverted.wav",'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(R)
    mx=max(abs(x) for x in s) or 1
    w.writeframes(b''.join(struct.pack('<h',int(x/mx*30000)) for x in s))
print("18 done")
