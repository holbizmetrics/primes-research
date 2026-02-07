#!/usr/bin/env python3
"""Normal vs Inverted zero chord side by side"""
import struct,math,wave,os
R=22050; os.makedirs("audio",exist_ok=True)
z=[14.1347,21.022,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738]
b=110.0; hd=int(3.0*R); gap=int(0.4*R); s=[0.0]*(2*hd+gap)
# First half: normal
for k in range(10):
    f=b*z[k]/z[0]
    if f>R/2: continue
    a=1.0/(1+k*0.25); dp=2*math.pi*f/R; ph=0
    for t in range(hd):
        fd=min(1.0,t/(0.2*R))*min(1.0,(hd-t)/(0.3*R))
        s[t]+=a*fd*math.sin(ph); ph+=dp
# Second half: inverted (1/gamma)
inv=[1.0/g for g in z]; imx=max(inv)
for k in range(10):
    f=b*inv[k]/imx*(z[-1]/z[0])
    if f>R/2 or f<20: continue
    a=1.0/(1+k*0.25); dp=2*math.pi*f/R; ph=0; st=hd+gap
    for t in range(st,2*hd+gap):
        fd=min(1.0,(t-st)/(0.2*R))*min(1.0,(2*hd+gap-t)/(0.3*R))
        s[t]+=a*fd*math.sin(ph); ph+=dp
with wave.open("audio/18_normal_vs_inverted.wav",'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(R)
    mx=max(abs(x) for x in s) or 1
    w.writeframes(b''.join(struct.pack('<h',int(x/mx*30000)) for x in s))
print("18_normal_vs_inverted.wav %.1fs" % (len(s)/R))
