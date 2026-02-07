#!/usr/bin/env python3
"""Generate audio files from prime number structures — fast version"""
import struct, math, wave, os, sys

RATE = 22050  # lower rate = faster generation
OUTDIR = "/data/data/com.termux/files/home/primes-research/audio"
os.makedirs(OUTDIR, exist_ok=True)

def write_wav(filename, samples, rate=RATE):
    path = os.path.join(OUTDIR, filename)
    with wave.open(path, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        mx = max(abs(s) for s in samples) or 1
        data = b''.join(struct.pack('<h', int(s/mx*30000)) for s in samples)
        w.writeframes(data)
    dur = len(samples)/rate
    print(f"  {path} ({dur:.1f}s, {len(samples)} samples)")
    sys.stdout.flush()

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(2,n+1) if s[i]]

P = sieve(10000)
Pset = set(P)
print(f"{len(P)} primes up to 10000"); sys.stdout.flush()

which = sys.argv[1] if len(sys.argv) > 1 else "all"

if which in ("1","all"):
    print("1. Prime rhythm"); sys.stdout.flush()
    smp = []
    sppi = 40
    click = [math.sin(2*math.pi*800*t/RATE)*math.exp(-t/RATE*50) for t in range(sppi)]
    silence = [0.0]*sppi
    for n in range(2, 301):
        smp.extend(click if n in Pset else silence)
    write_wav("01_prime_rhythm.wav", smp)

if which in ("2","all"):
    print("2. Gap melody"); sys.stdout.flush()
    gaps = [P[i+1]-P[i] for i in range(150)]
    smp = []
    for g in gaps:
        freq = max(150, min(1500, 880.0/(g/2.0)))
        ns = int(0.07*RATE)
        smp.extend([0.7*math.exp(-3*t/ns)*math.sin(2*math.pi*freq*t/RATE) for t in range(ns)])
    write_wav("02_gap_melody.wav", smp)

if which in ("3","all"):
    print("3. Sawtooth: full vs prime vs composite"); sys.stdout.flush()
    dur=2.5; base=110; mh=50; ns=int(dur*RATE)
    for label, harms in [("full", range(1,mh+1)),
                          ("primes", [h for h in range(2,mh+1) if h in Pset]),
                          ("composites", [h for h in range(4,mh+1) if h not in Pset])]:
        smp=[0.0]*ns
        for h in harms:
            a=1.0/h
            for t in range(ns): smp[t]+=a*math.sin(2*math.pi*base*h*t/RATE)
        write_wav(f"03_{label}.wav", smp)

if which in ("4","all"):
    print("4. Twin prime beats"); sys.stdout.flush()
    twins = [(p,p+2) for p in P[:300] if p+2 in Pset][:20]
    smp = []
    for p,q in twins:
        ns=int(0.4*RATE); f1=300; f2=f1*q/p
        for t in range(ns):
            e=math.exp(-2*t/ns)
            smp.append(0.5*e*(math.sin(2*math.pi*f1*t/RATE)+math.sin(2*math.pi*f2*t/RATE)))
        smp.extend([0]*int(0.03*RATE))
    write_wav("04_twin_beats.wav", smp)

if which in ("5","all"):
    print("5. Laser sweep"); sys.stdout.flush()
    smp=[]
    Psub=P[:1000]
    for lam in range(2,31):
        ar=ai=0
        for p in Psub:
            ph=2*math.pi*p/lam; ar+=math.cos(ph); ai+=math.sin(ph)
        coh=math.sqrt((ar*ar+ai*ai)/len(Psub)**2)
        freq=220*(lam/5.0); amp=min(1.0,coh*2)
        ns=int(0.22*RATE)
        smp.extend([amp*math.sin(2*math.pi*freq*t/RATE)*math.exp(-1.5*t/ns) for t in range(ns)])
    write_wav("05_laser_sweep.wav", smp)

if which in ("6","all"):
    print("6. Goldbach comet"); sys.stdout.flush()
    smp=[]
    for n in range(4,152,2):
        pairs=[(p,n-p) for p in P if p<=n//2 and n-p in Pset]
        ns=int(0.1*RATE); note=[0.0]*ns
        for p1,p2 in pairs[:6]:
            f=200+p1*3; a=0.3/max(1,len(pairs))
            for t in range(ns): note[t]+=a*math.sin(2*math.pi*f*t/RATE)*math.exp(-3*t/ns)
        smp.extend(note)
    write_wav("06_goldbach.wav", smp)

if which in ("7","all"):
    print("7. Singular series chord"); sys.stdout.flush()
    def mobius(n):
        if n==1: return 1
        d=2;t=n;nf=0
        while d*d<=t:
            if t%d==0:
                nf+=1;t//=d
                if t%d==0: return 0
            d+=1
        if t>1: nf+=1
        return (-1)**nf
    def euler_phi(n):
        r=n;d=2;t=n
        while d*d<=t:
            if t%d==0:
                while t%d==0:t//=d
                r-=r//d
            d+=1
        if t>1:r-=r//t
        return r
    def pfact(n):
        f=[];d=2;t=n
        while d*d<=t:
            if t%d==0:
                f.append(d)
                while t%d==0:t//=d
            d+=1
        if t>1:f.append(t)
        return f

    ns=int(4.0*RATE); base=110; smp=[0.0]*ns
    for q in range(2,35):
        mu=mobius(q)
        if mu==0: continue
        phi=euler_phi(q)
        amp=1.0/(phi**2)
        for p in pfact(q):
            if p>2: amp*=(p-1)/(p-2)
        freq=base*q
        if freq>6000: continue
        for t in range(ns): smp[t]+=amp*math.sin(2*math.pi*freq*t/RATE)
    write_wav("07_singular_series.wav", smp)

print("\nDone! Files in:", OUTDIR)
