"""Experiment 1: Repulsive Brennpunkt — genuine prime glow at small/negative t"""
import math

def sieve(n):
    s=[True]*(n+1);s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i):s[j]=False
    return set(i for i,v in enumerate(s) if v)

def bs(nums, N, t, wl, R=0.5):
    """Correct fine_scan.py physics"""
    k=2*math.pi*wl; ar=ai=0; c=0
    for n in nums:
        r=n/N
        if r<0.01: continue
        c+=1
        rn = r**(1-2*t) * R**(2*t)
        z = 1 - 2*rn
        ph = 2*k*z
        ar+=math.cos(ph); ai+=math.sin(ph)
    return (ar*ar+ai*ai)/(c*c) if c else 0

def bs_repulsive(nums, N, t, wl, R=0.5):
    """Repulsive: r_new = r^(1+2t) * R^(-2t) — INVERSION of standard"""
    k=2*math.pi*wl; ar=ai=0; c=0
    for n in nums:
        r=n/N
        if r<0.01: continue
        c+=1
        # Repulsive: exponent flipped
        rn = r**(1+2*t) * R**(-2*t)
        rn = max(0.001, min(rn, 10))  # clamp
        z = 1 - 2*rn
        ph = 2*k*z
        ar+=math.cos(ph); ai+=math.sin(ph)
    return (ar*ar+ai*ai)/(c*c) if c else 0

import random
random.seed(42)

for N in [500, 1000, 2000]:
    ps = sieve(N)
    P = [n for n in range(2,N+1) if n in ps]
    C = [n for n in range(4,N+1) if n not in ps]
    # PNT-density random baseline
    R_set = sorted(random.sample(range(2,N+1), len(P)))

    print(f'=== N={N} (#P={len(P)}, #C={len(C)}) ===')

    # Standard small-t scan
    print(f'\n  Standard Brennpunkt, small t:')
    print(f'  {"lam":>4} {"t":>6} {"pEnh":>8} {"P":>10} {"C":>10} {"Rand":>10}')
    for lam in [6, 10, 30, 35, 59]:
        bt = bpe = 0
        for ti in range(1, 60):
            t = ti/1000
            bp = bs(P, N, t, lam)
            bc = bs(C, N, t, lam)
            br = bs(R_set, N, t, lam)
            # pEnh = prime coherence / random coherence
            pe = bp/br if br > 1e-12 else 0
            if pe > bpe and pe < 1e6:
                bpe = pe; bt = t
                best_bp, best_bc, best_br = bp, bc, br
        if bpe > 0:
            print(f'  {lam:>4} {bt:.3f} {bpe:>8.1f}x {best_bp:>10.6f} {best_bc:>10.6f} {best_br:>10.6f}')

    # Repulsive Brennpunkt
    print(f'\n  Repulsive Brennpunkt (inverted transform):')
    print(f'  {"lam":>4} {"t":>6} {"pEnh":>8} {"P":>10} {"C":>10} {"Rand":>10}')
    for lam in [6, 10, 30, 35, 59]:
        bt = bpe = 0
        for ti in range(1, 100):
            t = ti/1000
            bp = bs_repulsive(P, N, t, lam)
            bc = bs_repulsive(C, N, t, lam)
            br = bs_repulsive(R_set, N, t, lam)
            pe = bp/br if br > 1e-12 else 0
            if pe > bpe and pe < 1e6:
                bpe = pe; bt = t
                best_bp, best_bc, best_br = bp, bc, br
        if bpe > 0:
            print(f'  {lam:>4} {bt:.3f} {bpe:>8.1f}x {best_bp:>10.6f} {best_bc:>10.6f} {best_br:>10.6f}')

    print()
