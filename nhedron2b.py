#!/usr/bin/env python3
import math
N=1500
LAM={}
for n in range(2,N+1):
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]:
        if t==1: break
        k=0
        while t%p==0: t//=p; k+=1
        if k>0 and t==1: LAM[n]=math.log(p); break
    else:
        if t>1: LAM[n]=math.log(n)
best_F=0;best_t=0
zeros=[14.13,21.02,25.01,30.42,32.94,37.59,40.92,43.33,48.01,49.77]
print("Multiplicative laser F(t):")
for ti in range(0,5001,10):
    t=ti/100.0
    ar=ai=0.0
    for n,l in LAM.items():
        phase=-t*math.log(n)
        w=l/math.sqrt(n)
        ar+=w*math.cos(phase); ai+=w*math.sin(phase)
    F=ar**2+ai**2
    if F>best_F: best_F=F;best_t=t
    near=any(abs(t-z)<0.15 for z in zeros)
    if near or ti%500==0:
        tag=""
        if near: tag=" <-- zero"
        print("  t=%5.2f F=%8.1f%s" % (t,F,tag))
print("PEAK: t=%.2f F=%.1f" % (best_t,best_F))
print("Additive peak: I_L(q=2)=0.0069")
print("Multiplicative peak %.0fx stronger" % (best_F/0.0069))
