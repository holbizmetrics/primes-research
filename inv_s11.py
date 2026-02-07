#!/usr/bin/env python3
"""Does the peak converge to gamma_1 as N grows?
And: is there ANY partial inversion that helps convergence?"""
import math
def mg(n):
    if n<2:return 0
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71]:
        if t==1:break
        k=0
        while t%p==0:t//=p;k+=1
        if k>0 and t==1:return math.log(p)
    if t>1:return math.log(n)
    return 0
g1=14.1347

print("=== Does F(t) peak converge to gamma_1 as N grows? ===")
print("Standard: alpha=1, beta=1")
print()
for N in [200,500,1000,2000,3000]:
    L={};LN={}
    for n in range(2,N+1):
        l=mg(n)
        if l>0:L[n]=l;LN[n]=math.log(n)
    def F(t):
        r=i=0.0
        for n,l in L.items():
            w=l/math.sqrt(n);r+=w*math.cos(-t*LN[n]);i+=w*math.sin(-t*LN[n])
        return r*r+i*i
    # Find peak near gamma_1
    best_t=0;best_f=0
    for ti in range(800,2000):
        t=ti*0.01
        f=F(t)
        if f>best_f:best_f=f;best_t=t
    Fg1=F(g1)
    err=abs(best_t-g1)/g1*100
    print("  N=%4d: peak at t=%.2f (gamma_1=14.13, error %.1f%%), F_peak=%.0f, F(g1)=%.0f, ratio=%.2f" % (
        N,best_t,err,best_f,Fg1,Fg1/best_f))
print()
print("As N grows, the peak should converge to gamma_1.")
print("If ratio -> 1, the peak IS at gamma_1.")
