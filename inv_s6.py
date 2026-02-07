#!/usr/bin/env python3
import math,random
random.seed(42)
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
Z=[14.1347,21.022,25.0109,30.4249,32.9351]
for N in [300,500,800]:
    L={};LN={}
    for n in range(2,N+1):
        l=mg(n)
        if l>0:L[n]=l;LN[n]=math.log(n)
    def Ab(t,b):
        r=i=0.0
        for n,l in L.items():
            p=LN[n]**b;w=l/math.sqrt(n);r+=w*math.cos(-t*p);i+=w*math.sin(-t*p)
        return r*r+i*i
    best=0;ba=1;bb=1
    for ai in range(8,18):
        a=ai*0.1
        for bi in range(5,13):
            b=bi*0.1
            sg=sum(Ab(g**a,b) for g in Z)/5
            tr=[g**a for g in Z];lo=min(tr)*0.6;hi=max(tr)*1.4
            bg=sum(Ab(lo+random.random()*(hi-lo),b) for _ in range(10))/10
            c=sg/bg if bg>1 else 0
            if c>best:best=c;ba=a;bb=b
    sg0=sum(Ab(g,1.0) for g in Z)/5
    bg0=sum(Ab(min(Z)*0.6+random.random()*(max(Z)*1.4-min(Z)*0.6),1.0) for _ in range(10))/10
    c0=sg0/bg0 if bg0>1 else 0
    print("N=%d: best a=%.1f b=%.1f C=%.2f  standard C=%.2f" % (N,ba,bb,best,c0))
