"""Experiment 2: Power Mean Family — different focusing functions"""
import math

def sieve(n):
    s=[True]*(n+1);s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i):s[j]=False
    return set(i for i,v in enumerate(s) if v)

def bs_general(nums, N, t, wl, mean_type='geometric', R=0.5):
    """Backscatter with different mean types for focusing"""
    k=2*math.pi*wl; ar=ai=0; c=0
    for n in nums:
        r=n/N
        if r<0.01: continue
        c+=1

        if mean_type == 'geometric':
            # Standard: r^(1-2t) * R^(2t) — power mean with p→0
            rn = r**(1-2*t) * R**(2*t)
        elif mean_type == 'arithmetic':
            # Linear interpolation: (1-t)*r + t*R
            rn = (1-t)*r + t*R
        elif mean_type == 'harmonic':
            # Harmonic: 1/((1-t)/r + t/R)
            rn = 1.0/((1-t)/r + t/R) if r > 1e-10 else r
        elif mean_type == 'quadratic':
            # RMS: sqrt((1-t)*r² + t*R²)
            rn = math.sqrt((1-t)*r*r + t*R*R)
        elif mean_type == 'cubic':
            # Cubic mean: ((1-t)*r³ + t*R³)^(1/3)
            rn = ((1-t)*r**3 + t*R**3)**(1/3)
        elif mean_type == 'min':
            # min-mean (p→-inf): tends toward smaller
            rn = min(r, R) if t > 0.5 else r*(1-t) + min(r,R)*t
        else:
            rn = r

        z = 1 - 2*rn
        ph = 2*k*z
        ar+=math.cos(ph); ai+=math.sin(ph)
    return (ar*ar+ai*ai)/(c*c) if c else 0

import random
random.seed(42)

means = ['geometric', 'arithmetic', 'harmonic', 'quadratic', 'cubic']

for N in [500, 1000, 2000]:
    ps = sieve(N)
    P = [n for n in range(2,N+1) if n in ps]
    C = [n for n in range(4,N+1) if n not in ps]
    R_set = sorted(random.sample(range(2,N+1), len(P)))

    print(f'=== N={N} ===')
    print(f'{"mean":>12} {"lam":>4} {"best_t":>7} {"P/C":>8} {"pEnh":>8} {"P":>10} {"C":>10}')
    print('-'*65)

    for mean_type in means:
        for lam in [6, 10, 30, 35]:
            bt_r = btr = 0  # best by P/C ratio
            bt_e = bte = 0  # best by pEnh (vs random)
            for ti in range(5, 490):
                t = ti/500
                bp = bs_general(P, N, t, lam, mean_type)
                bc = bs_general(C, N, t, lam, mean_type)
                br = bs_general(R_set, N, t, lam, mean_type)

                ratio = bp/bc if bc > 1e-12 else 0
                penh = bp/br if br > 1e-12 else 0

                if penh > bte and penh < 1e6:
                    bte = penh; bt_e = t
                    best_ratio_at_e = ratio
                    best_bp, best_bc = bp, bc

            if bte > 1:
                print(f'{mean_type:>12} {lam:>4} {bt_e:>7.3f} {best_ratio_at_e:>8.1f} {bte:>8.1f}x {best_bp:>10.6f} {best_bc:>10.6f}')

    print()
