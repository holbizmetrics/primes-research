#!/usr/bin/env python3
import math
def mg(n):
    if n<2:return 0
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29,31]:
        if t==1:break
        k=0
        while t%p==0:t//=p;k+=1
        if k>0 and t==1:return math.log(p)
    if t>1:return math.log(n)
    return 0
g1=14.1347
def get_Q(N,a,b):
    L={};LN={}
    for n in range(2,N+1):
        l=mg(n)
        if l>0:L[n]=l;LN[n]=math.log(n)
    def F(t):
        r=i=0.0
        for n,l in L.items():
            p=LN[n]**b;w=l/math.sqrt(n);r+=w*math.cos(-t*p);i+=w*math.sin(-t*p)
        return r*r+i*i
    t0=g1**a;fp=F(t0)
    fw=sum(F(t0+d) for d in [-t0*.15,-t0*.08,t0*.08,t0*.15])/4
    return fp/fw if fw>0.1 else 0

print("Convergence check:")
for N in [300,600,1000]:
    print("N=%d:" % N)
    print("  Q(1.0,1.0)=%.2f" % get_Q(N,1.0,1.0))
    print("  Q(1.9,0.7)=%.2f" % get_Q(N,1.9,0.7))
    print("  Q(1.5,1.0)=%.2f" % get_Q(N,1.5,1.0))
    bQ=0;ba=0;bb=0
    for ai in range(15,22):
        a=ai*0.1
        for bi in range(4,13):
            b=bi*0.1
            Q=get_Q(N,a,b)
            if Q>bQ:bQ=Q;ba=a;bb=b
    print("  BEST: a=%.1f b=%.1f Q=%.2f" % (ba,bb,bQ))
