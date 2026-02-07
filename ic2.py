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
g1=14.1347; N=1000
L={};LN={}
for n in range(2,N+1):
    l=mg(n)
    if l>0:L[n]=l;LN[n]=math.log(n)

def peakQ(a,b):
    """Does the peak in F(t) land at gamma_1^a?"""
    t0=g1**a; bf=0;bt=t0
    for ti in range(-30,31):
        t=t0*(1+ti*0.02)
        if t<1:continue
        r=i=0.0
        for n,l in L.items():
            p=LN[n]**b;w=l/math.sqrt(n)
            r+=w*math.cos(-t*p);i+=w*math.sin(-t*p)
        f=r*r+i*i
        if f>bf:bf=f;bt=t
    r=i=0.0
    for n,l in L.items():
        p=LN[n]**b;w=l/math.sqrt(n)
        r+=w*math.cos(-t0*p);i+=w*math.sin(-t0*p)
    fg=r*r+i*i
    offset=(bt-t0)/t0*100
    return fg/bf if bf>0 else 0, offset

print("=== Which (alpha,beta) puts the peak AT gamma^alpha? ===")
print("ratio=1 means peak is exactly at gamma^alpha")
print()
print("%5s %5s %6s %7s" % ("alpha","beta","ratio","offset%"))
print("-"*28)
best_r=0;ba=1;bb=1
for ai in range(5,22):
    a=ai*0.1
    for bi in range(3,18):
        b=bi*0.1
        r,off=peakQ(a,b)
        if r>best_r:best_r=r;ba=a;bb=b
        if r>0.85:
            print("%5.1f %5.1f %6.3f %+7.1f" % (a,b,r,off))
print()
print("BEST: a=%.1f b=%.1f ratio=%.3f" % (ba,bb,best_r))
print("Standard (1,1):", end=" ")
r,off=peakQ(1.0,1.0)
print("ratio=%.3f, offset=%+.1f%%" % (r,off))
