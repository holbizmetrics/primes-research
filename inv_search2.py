#!/usr/bin/env python3
"""Search for optimal partial inversion — CONTRAST measure
Signal = F(at_zero) / F(off_zero)
This normalizes out the DC divergence at small frequencies.
"""
import math, random
random.seed(42)
N=1200
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

zeros=[14.1347,21.022,25.0109,30.4249,32.9351]

def A_ab(t, beta):
    """Amplitude with geometry log(n)^beta"""
    ar=ai=0.0
    for n,lam in LAM.items():
        pos = LN[n]**beta if beta > 0.01 else 1.0
        phase = -t * pos
        w = lam/math.sqrt(n)
        ar+=w*math.cos(phase); ai+=w*math.sin(phase)
    return ar**2+ai**2

def contrast(alpha, beta):
    """Signal at zeros / background"""
    sig = 0.0
    for g in zeros:
        t = g**alpha if abs(alpha)>0.01 else 1.0
        sig += A_ab(t, beta)
    sig /= len(zeros)
    # Background: random frequencies in same range
    bg = 0.0
    t_range = [g**alpha if abs(alpha)>0.01 else 1.0 for g in zeros]
    t_lo = min(t_range)*0.8; t_hi = max(t_range)*1.2
    if t_hi <= t_lo: t_hi = t_lo + 1
    for _ in range(10):
        t_rnd = t_lo + random.random()*(t_hi-t_lo)
        bg += A_ab(t_rnd, beta)
    bg /= 10
    return sig / bg if bg > 1 else sig

# STRIKE 1: alpha sweep, beta=1
print("=== STRIKE 1: Alpha sweep (beta=1) ===")
print("Contrast = F(at zeros)/F(background)")
print()
print("%6s %10s %10s %10s" % ("alpha","signal","background","contrast"))
print("-"*42)
best_c=0; best_a=0
for ai in range(-15, 25):
    alpha = ai * 0.1
    if abs(alpha) < 0.05: continue
    sig=0
    for g in zeros:
        t=g**alpha; sig+=A_ab(t,1.0)
    sig/=len(zeros)
    t_range=[g**alpha for g in zeros]
    t_lo=min(t_range)*0.8; t_hi=max(t_range)*1.2
    if t_hi<=t_lo: t_hi=t_lo+1
    bg=0
    for _ in range(10):
        bg+=A_ab(t_lo+random.random()*(t_hi-t_lo),1.0)
    bg/=10
    c=sig/bg if bg>1 else 0
    if c>best_c: best_c=c; best_a=alpha
    if c>0.5 or abs(alpha-1.0)<0.05:
        print("%6.1f %10.1f %10.1f %10.3f%s" % (alpha,sig,bg,c,
            " <-- PEAK" if c>best_c*0.95 else ""))
print()
print("Best contrast: alpha=%.1f, C=%.3f" % (best_a, best_c))

# STRIKE 2: 2D sweep (alpha, beta)
print()
print("=== STRIKE 2: 2D sweep (alpha, beta) ===")
print("Looking for convergence point")
print()
best_c2=0; best_ab=(1,1)
results=[]
for ai in range(2, 20):
    alpha = ai * 0.1
    for bi in range(2, 20):
        beta = bi * 0.1
        c = contrast(alpha, beta)
        results.append((alpha, beta, c))
        if c > best_c2: best_c2=c; best_ab=(alpha,beta)

# Top 10
results.sort(key=lambda x:-x[2])
print("Top 10 (alpha, beta) by contrast:")
for alpha, beta, c in results[:10]:
    print("  alpha=%.1f beta=%.1f: contrast=%.3f" % (alpha, beta, c))
print()
print("BEST: alpha=%.1f, beta=%.1f, contrast=%.3f" % (best_ab[0], best_ab[1], best_c2))
print("Standard (1,1): contrast=%.3f" % contrast(1.0, 1.0))
