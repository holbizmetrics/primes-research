#!/usr/bin/env python3
"""3D geometry + multiplicative probes, part B: overtone combinations"""
import math, random
random.seed(42)
N=2000
def mangoldt(n):
    if n<2: return 0
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]:
        if t==1: break
        k=0
        while t%p==0: t//=p; k+=1
        if k>0 and t==1: return math.log(p)
    if t>1: return math.log(n)
    return 0
LAM={}
for n in range(2,N+1):
    l=mangoldt(n)
    if l>0: LAM[n]=l

zeros=[]
try:
    with open('z.txt') as f:
        for line in f:
            line=line.strip()
            if line: zeros.append(float(line))
except:
    zeros=[14.1347,21.0220,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738]

def F_log(t):
    ar=ai=0.0
    for n,lam in LAM.items():
        phase=-t*math.log(n); w=lam/math.sqrt(n)
        ar+=w*math.cos(phase); ai+=w*math.sin(phase)
    return ar**2+ai**2

# Background
bg=[F_log(random.uniform(5,100)) for _ in range(50)]
bg_m=sum(bg)/len(bg); bg_s=math.sqrt(sum((v-bg_m)**2 for v in bg)/len(bg))
thresh=bg_m+3*bg_s

print("=== STRIKE 3: Sum/difference frequencies ===")
print("Background: mean=%.1f, std=%.1f, threshold=%.1f" % (bg_m,bg_s,thresh))
print()
print("%3s %3s %7s %7s %9s %9s %s" % ("i","j","gi+gj","gi-gj","F(sum)","F(diff)","notes"))
print("-"*60)
for i in range(min(6,len(zeros))):
    for j in range(i+1,min(6,len(zeros))):
        gs=zeros[i]+zeros[j]; gd=abs(zeros[i]-zeros[j])
        Fs=F_log(gs) if gs<200 else 0
        Fd=F_log(gd) if gd>1 else 0
        tag=""
        if Fs>thresh: tag+=" SUM!"
        if Fd>thresh: tag+=" DIFF!"
        for k,g in enumerate(zeros[:50]):
            if abs(gs-g)<0.5: tag+=" sum~g%d" % (k+1)
            if abs(gd-g)<0.5: tag+=" diff~g%d" % (k+1)
        if tag: print("%3d %3d %7.2f %7.2f %9.1f %9.1f %s" % (i+1,j+1,gs,gd,Fs,Fd,tag))

print()
print("=== STRIKE 4: Harmonic ratios ===")
print("gamma_i/gamma_j near simple fractions -> overtone resonance")
print()
def best_rat(x,md=12):
    be=1;bp=0;bq=1
    for q in range(1,md+1):
        p=round(x*q)
        e=abs(x-p/q)
        if e<be: be=e;bp=p;bq=q
    return bp,bq,be
print("%3s %3s %9s %8s %8s" % ("i","j","ratio","frac","quality"))
print("-"*40)
for i in range(min(8,len(zeros))):
    for j in range(i+1,min(8,len(zeros))):
        r=zeros[i]/zeros[j]; p,q,e=best_rat(r)
        quality=1.0/(e*q+0.001)
        if quality>20:
            print("%3d %3d %9.6f %5d/%-3d %8.1f" % (i+1,j+1,r,p,q,quality))

print()
print("=== STRIKE 5: Constructive interference hotspots ===")
print("x where sum cos(gamma_k * log(x)) is maximized")
print()
nz=min(30,len(zeros))
best_sc=-999;best_x=0
for li in range(10,100):
    lx=li/10.0; x=math.exp(lx)
    sc=sum(math.cos(zeros[k]*lx) for k in range(nz))
    if sc>best_sc: best_sc=sc;best_x=x
    if abs(sc)>5:
        nn=round(x)
        lam=mangoldt(nn) if 2<=nn<=10000 else 0
        pp="PRIME" if lam>0 and round(x)==nn else ""
        print("  x=%.1f (log=%.1f) sum_cos=%.2f near %d %s" % (x,lx,sc,nn,pp))
print()
print("Max constructive: x=%.1f, sum=%.2f" % (best_x,best_sc))
nn=round(best_x); lam=mangoldt(nn) if 2<=nn<=10000 else 0
print("Nearest integer %d: Lambda=%.3f %s" % (nn,lam,"(prime power!)" if lam>0 else ""))
