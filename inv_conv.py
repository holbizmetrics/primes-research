#!/usr/bin/env python3
import math
def mg(n):
    if n<2:return 0
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]:
        if t==1:break
        k=0
        while t%p==0:t//=p;k+=1
        if k>0 and t==1:return math.log(p)
    if t>1:return math.log(n)
    return 0
g1=14.1347
for N in [200,500,1000,2000]:
    L={};LN={}
    for n in range(2,N+1):
        l=mg(n)
        if l>0:L[n]=l;LN[n]=math.log(n)
    bt=0;bf=0
    for ti in range(800,1800):
        t=ti*0.01;r=i=0.0
        for n,l in L.items():
            w=l/math.sqrt(n);r+=w*math.cos(-t*LN[n]);i+=w*math.sin(-t*LN[n])
        f=r*r+i*i
        if f>bf:bf=f;bt=t
    r=i=0.0
    for n,l in L.items():
        w=l/math.sqrt(n);r+=w*math.cos(-g1*LN[n]);i+=w*math.sin(-g1*LN[n])
    fg=r*r+i*i
    print("N=%4d peak=%.2f err=%.1f%% F_peak=%.0f F(g1)=%.0f ratio=%.2f" % (
        N,bt,abs(bt-g1)/g1*100,bf,fg,fg/bf))
