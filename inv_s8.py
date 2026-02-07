#!/usr/bin/env python3
"""Fine scan around alpha~1.9 beta~0.7 and convergence check"""
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
ZZ=[14.1347,21.022,25.0109,30.4249,32.9351]
g1=ZZ[0]

def get_Q(N, alpha, beta):
    L={};LN={}
    for n in range(2,N+1):
        l=mg(n)
        if l>0:L[n]=l;LN[n]=math.log(n)
    def F(t):
        ar=ai=0.0
        for n,l in L.items():
            pos=LN[n]**beta; w=l/math.sqrt(n)
            ar+=w*math.cos(-t*pos); ai+=w*math.sin(-t*pos)
        return ar*ar+ai*ai
    t0=g1**alpha; fp=F(t0)
    fw=sum(F(t0+d) for d in [-t0*0.15,-t0*0.08,t0*0.08,t0*0.15])/4
    return fp/fw if fw>0.1 else 0, fp

# Fine scan around peak
print("=== Fine scan: alpha 1.5-2.1, beta 0.4-1.0, N=800 ===")
N=800; best_Q=0; ba=0;bb=0
for ai in range(30,43):
    a=ai*0.05
    for bi in range(8,21):
        b=bi*0.05
        Q,_=get_Q(N,a,b)
        if Q>best_Q: best_Q=Q;ba=a;bb=b
        if Q>5: print("  a=%.2f b=%.2f Q=%.1f" % (a,b,Q))
print("BEST: a=%.2f b=%.2f Q=%.1f" % (ba,bb,best_Q))
print()

# Convergence
print("=== Convergence: does (alpha,beta) stabilize? ===")
print("%5s %6s %6s %6s %6s" % ("N","Q(1,1)","Q(1.9,0.7)","Q(best_a,best_b)","best_a,b"))
for N in [300,500,800,1200]:
    Q11,_=get_Q(N,1.0,1.0)
    Q19,_=get_Q(N,1.9,0.7)
    # Quick local search
    bQ=0;ba2=1.9;bb2=0.7
    for ai in range(35,42):
        a=ai*0.05
        for bi in range(10,18):
            b=bi*0.05
            Q,_=get_Q(N,a,b)
            if Q>bQ: bQ=Q;ba2=a;bb2=b
    print("%5d %6.2f %6.2f %6.2f       (%.2f,%.2f)" % (N,Q11,Q19,bQ,ba2,bb2))

print()
# Check: is alpha~2 just SQUARING the zero?
# gamma^2 ~ 200. At t~200 with beta=0.7, we're probing
# short-range oscillations in log(n)^0.7
# What IS log(n)^0.7?
print("=== What IS log(n)^0.7? ===")
for n in [2,3,5,10,50,100,500,1000]:
    ln=math.log(n)
    print("  n=%4d: log(n)=%.3f  log(n)^0.7=%.3f  log(n)^0.5=%.3f" % (n,ln,ln**0.7,ln**0.5))
print()
print("log(n)^0.7 compresses the scale: large n are closer together.")
print("Combined with gamma^1.9: we're looking at high-frequency")
print("oscillations in a COMPRESSED log-space.")
print()
print("This is the multiplicative analog of the Legendre magnifier!")
print("Compress the geometry (beta<1) while expanding the probe (alpha>1)")
print("= 'stretch the lens while zooming the target'")
