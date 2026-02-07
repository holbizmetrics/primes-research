#!/usr/bin/env python3
"""Search for optimal partial inversion of zeta zeros + geometry
Two knobs:
  alpha: zero power map, gamma_k -> gamma_k^alpha
  beta:  geometry power map, log(n) -> log(n)^beta
Signal: F(alpha,beta) = sum_k |A(gamma_k^alpha, beta)|^2
where A(t, beta) = sum Lambda(n)/sqrt(n) * exp(-i*t*log(n)^beta)
"""
import math
N=1500
def mangoldt(n):
    if n<2: return 0
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]:
        if t==1: break
        k=0
        while t%p==0: t//=p; k+=1
        if k>0 and t==1: return math.log(p)
    if t>1: return math.log(n)
    return 0
LAM={}; LN={}
for n in range(2,N+1):
    l=mangoldt(n)
    if l>0: LAM[n]=l; LN[n]=math.log(n)

zeros=[14.1347,21.022,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738]

def F_ab(alpha, beta):
    """Total signal: sum over first 5 zeros of |A(gamma^alpha)|^2
    with geometry log(n)^beta"""
    total=0.0
    for g in zeros[:5]:
        t = g**alpha if alpha != 0 else 1.0
        ar=ai=0.0
        for n,lam in LAM.items():
            pos = LN[n]**beta if beta != 0 else 1.0
            phase = -t * pos
            w = lam/math.sqrt(n)
            ar+=w*math.cos(phase); ai+=w*math.sin(phase)
        total += ar**2 + ai**2
    return total

# Strike 1: Sweep alpha with beta=1 (standard geometry)
print("=== STRIKE 1: Sweep alpha (zero power) with beta=1 ===")
print("F(alpha) = sum_k |A(gamma_k^alpha)|^2")
print()
print("%6s %12s" % ("alpha", "F"))
print("-"*22)
best_F=0; best_a=0
for ai in range(-20, 21):
    alpha = ai * 0.1
    F = F_ab(alpha, 1.0)
    if F > best_F and abs(alpha)>0.01: best_F=F; best_a=alpha
    print("%6.1f %12.1f" % (alpha, F))
print()
print("Best alpha=%.1f, F=%.1f" % (best_a, best_F))
print("(alpha=1.0 is standard, F=%.1f)" % F_ab(1.0, 1.0))
