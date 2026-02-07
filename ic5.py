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
g=14.1347;N=400;L={};LN={}
for n in range(2,N+1):
    l=mg(n)
    if l>0:L[n]=l;LN[n]=math.log(n)
br=0;ba=1;bb=1
for a in [0.5,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.5,1.7,1.9]:
    for b in [0.3,0.5,0.7,0.8,0.9,1.0,1.1,1.2,1.4]:
        t0=g**a;bf=0
        for d in range(-12,13):
            t=t0*(1+d*0.04)
            if t<0.5:continue
            r=i=0.0
            for n,l in L.items():
                p=LN[n]**b;w=l/math.sqrt(n);r+=w*math.cos(-t*p);i+=w*math.sin(-t*p)
            f=r*r+i*i
            if f>bf:bf=f
        r=i=0.0
        for n,l in L.items():
            p=LN[n]**b;w=l/math.sqrt(n);r+=w*math.cos(-t0*p);i+=w*math.sin(-t0*p)
        q=(r*r+i*i)/bf if bf>0 else 0
        if q>br:br=q;ba=a;bb=b
        if q>0.85:print("a=%.1f b=%.1f q=%.3f" % (a,b,q))
print("Best:a=%.1f b=%.1f q=%.3f  std:%.3f" % (ba,bb,br,0))
