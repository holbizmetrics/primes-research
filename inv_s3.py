#!/usr/bin/env python3
import math,random
random.seed(42); N=800
def mg(n):
    if n<2: return 0
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]:
        if t==1: break
        k=0
        while t%p==0: t//=p; k+=1
        if k>0 and t==1: return math.log(p)
    if t>1: return math.log(n)
    return 0
L={};LN={}
for n in range(2,N+1):
    l=mg(n)
    if l>0: L[n]=l; LN[n]=math.log(n)
Z=[14.1347,21.022,25.0109,30.4249,32.9351]
def Ab(t,b):
    ar=ai=0.0
    for n,l in L.items():
        pos=LN[n]**b if b>0.01 else 1.0
        ph=-t*pos; w=l/math.sqrt(n)
        ar+=w*math.cos(ph); ai+=w*math.sin(ph)
    return ar**2+ai**2

print("=== Alpha sweep (beta=1) ===")
print("%6s %8s" % ("alpha","contrast"))
best_c=0;best_a=1
for ai in range(2,25):
    a=ai*0.1
    sig=sum(Ab(g**a,1.0) for g in Z)/5
    tr=[g**a for g in Z]; lo=min(tr)*0.7; hi=max(tr)*1.3
    if hi<=lo: hi=lo+1
    bg=sum(Ab(lo+random.random()*(hi-lo),1.0) for _ in range(8))/8
    c=sig/bg if bg>1 else 0
    if c>best_c: best_c=c;best_a=a
    print("%6.1f %8.3f%s" % (a,c," *" if c>1.5 else ""))
print("Best: alpha=%.1f, contrast=%.3f" % (best_a,best_c))
print()

print("=== 2D sweep (alpha, beta) ===")
best2=0;bab=(1,1);res=[]
for ai in range(3,18):
    a=ai*0.1
    for bi in range(3,18):
        b=bi*0.1
        sig=sum(Ab(g**a,b) for g in Z)/5
        tr=[g**a for g in Z]; lo=min(tr)*0.7; hi=max(tr)*1.3
        if hi<=lo: hi=lo+1
        bg=sum(Ab(lo+random.random()*(hi-lo),b) for _ in range(6))/6
        c=sig/bg if bg>1 else 0
        res.append((a,b,c))
        if c>best2: best2=c;bab=(a,b)
res.sort(key=lambda x:-x[2])
print("Top 15:")
for a,b,c in res[:15]:
    print("  a=%.1f b=%.1f: %.3f" % (a,b,c))
print()
print("BEST: alpha=%.1f beta=%.1f contrast=%.3f" % (bab[0],bab[1],best2))
print("Standard (1,1): %.3f" % [c for a,b,c in res if abs(a-1)<0.05 and abs(b-1)<0.05][0])
