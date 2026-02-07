#!/usr/bin/env python3
import math
def mg(n):
    if n<2:return 0
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29]:
        if t==1:break
        k=0
        while t%p==0:t//=p;k+=1
        if k>0 and t==1:return math.log(p)
    if t>1:return math.log(n)
    return 0
g1=14.1347; N=700
L={};LN={}
for n in range(2,N+1):
    l=mg(n)
    if l>0:L[n]=l;LN[n]=math.log(n)
def pQ(a,b):
    t0=g1**a;bf=0;bt=t0
    for ti in range(-20,21):
        t=t0*(1+ti*0.025)
        if t<1:continue
        r=i=0.0
        for n,l in L.items():
            p=LN[n]**b;w=l/math.sqrt(n);r+=w*math.cos(-t*p);i+=w*math.sin(-t*p)
        f=r*r+i*i
        if f>bf:bf=f;bt=t
    r=i=0.0
    for n,l in L.items():
        p=LN[n]**b;w=l/math.sqrt(n);r+=w*math.cos(-t0*p);i+=w*math.sin(-t0*p)
    fg=r*r+i*i
    return fg/bf if bf>0 else 0,(bt-t0)/t0*100
br=0;ba=1;bb=1
for ai in range(5,20):
    a=ai*0.1
    for bi in range(3,15):
        b=bi*0.1
        r,off=pQ(a,b)
        if r>br:br=r;ba=a;bb=b
        if r>0.9: print("a=%.1f b=%.1f ratio=%.3f off=%+.0f%%" % (a,b,r,off))
print("Best: a=%.1f b=%.1f ratio=%.3f" % (ba,bb,br))
r0,o0=pQ(1.0,1.0)
print("Standard: ratio=%.3f off=%+.0f%%" % (r0,o0))
