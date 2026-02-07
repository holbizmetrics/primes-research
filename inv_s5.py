#!/usr/bin/env python3
import math,random
random.seed(42)
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
Z=[14.1347,21.022,25.0109,30.4249,32.9351]
print("%6s %6s %6s %8s %8s" % ("N","alpha","beta","best_C","C(1,1)"))
for N in [400,700,1000]:
    L={};LN={}
    for n in range(2,N+1):
        l=mg(n)
        if l>0: L[n]=l; LN[n]=math.log(n)
    def Ab(t,b):
        ar=ai=0.0
        for n,l in L.items():
            pos=LN[n]**b if b>0.01 else 1.0
            w=l/math.sqrt(n)
            ar+=w*math.cos(-t*pos); ai+=w*math.sin(-t*pos)
        return ar**2+ai**2
    def C(a,b):
        sg=sum(Ab(g**a,b) for g in Z)/5
        tr=[g**a for g in Z]; lo=min(tr)*0.6; hi=max(tr)*1.4
        if hi<=lo: hi=lo+1
        bg=sum(Ab(lo+random.random()*(hi-lo),b) for _ in range(15))/15
        return sg/bg if bg>1 else 0
    best=0;ba=1;bb=1
    for ai in range(8,20):
        a=ai*0.1
        for bi in range(4,14):
            b=bi*0.1
            c=C(a,b)
            if c>best: best=c;ba=a;bb=b
    c11=C(1.0,1.0)
    print("%6d %6.1f %6.1f %8.3f %8.3f" % (N,ba,bb,best,c11))
