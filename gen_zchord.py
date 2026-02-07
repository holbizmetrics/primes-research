#!/usr/bin/env python3
import struct, math, wave, os
RATE=22050; OUTDIR="audio"; os.makedirs(OUTDIR, exist_ok=True)
def write_wav(fn, s):
    p=os.path.join(OUTDIR, fn)
    with wave.open(p,'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        mx=max(abs(x) for x in s) or 1
        w.writeframes(b''.join(struct.pack('<h',int(x/mx*30000)) for x in s))
    print("  %s (%.1fs)" % (p, len(s)/RATE))

zeros=[]
with open('z.txt') as f:
    for line in f:
        line=line.strip()
        if line: zeros.append(float(line))
zeros=zeros[:20]

print("3. Zero chord buildup")
base=110.0; dur=int(8.0*RATE); nz=20
smp=[0.0]*dur
for k in range(nz):
    freq=base*zeros[k]/zeros[0]
    if freq>RATE/2: continue
    amp=1.0/(1+k*0.2)
    start=int(k*dur/(nz+2))
    dphi=2*math.pi*freq/RATE; phi=0
    for t in range(start, dur):
        fade=min(1.0,(t-start)/(0.5*RATE))
        smp[t]+=amp*fade*math.sin(phi); phi+=dphi
write_wav("15_zero_chord.wav", smp)
