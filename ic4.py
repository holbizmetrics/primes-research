#!/usr/bin/env python3
import math
def mg(n):
    if n<2:return 0
    t=n
    for p in [2,3,5,7,11,13]:
        if t==1:break
        k=0
        while t%p==0:t//=p;k+=1
        if k>0 and t==1:return math.log(p)
    if t>1:return math.log(n)
    return 0
g=14.1347;N=500;L={};LN={}
for n in range(2,N+1):
    l=mg(n)
    if l>0:L[n]=l;LN[n]=math.log(n)
def Q(a,b):
    t0=g**a;bf=0
    for d in range(-15,16):
        t=t0*(1+d*0.03)
        if t<0.5:continue
        r=i=0.0
        for n,l in L.items():
            p=LN[n]**b;w=l/math.sqrt(n);r+=w*math.cos(-t*p);i+=w*math.sin(-t*p)
        f=r*r+i*i
        if f>bf:bf=f
    r=i=0.0
    for n,l in L.items():
        p=LN[n]**b;w=l/math.sqrt(n);r+=w*math.cos(-t0*p);i+=w*math.sin(-t0*p)
    return (r*r+i*i)/bf if bf>0 else 0
br=0;ba=1;bb=1
for a10 in range(5,20):
    a=a10/10.0
    for b10 in range(3,15):
        b=b10/10.0
        q=Q(a,b)
        if q>br:br=q;ba=a;bb=b
        if q>0.9:print("a=%.1f b=%.1f Q=%.3f" % (a,b,q))
print("Best:a=%.1f b=%.1f Q=%.3f  Std:Q=%.3f" % (ba,bb,br,Q(1,1)))
