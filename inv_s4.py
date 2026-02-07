#!/usr/bin/env python3
"""Fine search around (alpha~1.5, beta~0.5-1.0)
Better background statistics: 30 random samples
Also test: does contrast peak CONVERGE as N grows?
"""
import math,random
random.seed(42)

def mg(n):
    if n<2: return 0
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71]:
        if t==1: break
        k=0
        while t%p==0: t//=p; k+=1
        if k>0 and t==1: return math.log(p)
    if t>1: return math.log(n)
    return 0

Z=[14.1347,21.022,25.0109,30.4249,32.9351]

def run_search(N):
    L={};LN={}
    for n in range(2,N+1):
        l=mg(n)
        if l>0: L[n]=l; LN[n]=math.log(n)

    def Ab(t,b):
        ar=ai=0.0
        for n,l in L.items():
            pos=LN[n]**b if b>0.01 else 1.0
            ph=-t*pos; w=l/math.sqrt(n)
            ar+=w*math.cos(ph); ai+=w*math.sin(ph)
        return ar**2+ai**2

    def contrast(a,b):
        sig=sum(Ab(g**a,b) for g in Z)/len(Z)
        tr=[g**a for g in Z]; lo=min(tr)*0.6; hi=max(tr)*1.4
        if hi<=lo: hi=lo+1
        bg=sum(Ab(lo+random.random()*(hi-lo),b) for _ in range(20))/20
        return sig/bg if bg>1 else 0

    best=0; bab=(1,1)
    for ai in range(5,22):
        a=ai*0.05+0.75  # 1.0 to 1.8
        for bi in range(1,20):
            b=bi*0.05+0.25  # 0.3 to 1.2
            c=contrast(a,b)
            if c>best: best=c; bab=(a,b)
    # Also check (1,1)
    c11=contrast(1.0,1.0)
    return bab[0],bab[1],best,c11

# Test convergence across N
print("=== Does the optimal (alpha,beta) CONVERGE? ===")
print("%6s %6s %6s %8s %8s" % ("N","alpha","beta","contrast","C(1,1)"))
print("-"*40)
for N in [400, 600, 800, 1000, 1500]:
    a,b,c,c11 = run_search(N)
    print("%6d %6.2f %6.2f %8.3f %8.3f" % (N, a, b, c, c11))
