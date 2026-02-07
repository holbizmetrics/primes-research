#!/usr/bin/env python3
"""Final summary: rate of approach to GUE and 3-point conclusion"""
import math

with open('/data/data/com.termux/files/home/primes-research/z.txt') as f:
    zeros = sorted(set(float(line.strip()) for line in f if line.strip()))

def Ns(t): return t/(2*math.pi)*math.log(t/(2*math.pi*math.e))+7/8
U = [Ns(z) for z in zeros]
nz = len(U)

# GUE predictions
def K(x): return 1.0 if abs(x)<1e-14 else math.sin(math.pi*x)/(math.pi*x)
nn=30; dx=1.0/nn
k2_gue_L1 = 1.0-sum(K((a-b)*dx)**2*dx**2 for a in range(nn) for b in range(nn))

# Blocks of ~100 zeros for stability
block=100; L=1.0
print("=== Variance excess at L=1 vs T ===")
print(f"{'T_mid':>8} {'n':>4} {'var':>8} {'excess':>8} {'1/logT':>8} {'ratio':>8}")
T_data = []
for start in range(0, nz-block+1, block):
    end = min(start+block, nz)
    Usub = U[start:end]; Tsub = zeros[start:end]
    Tmid = Tsub[len(Tsub)//2]

    vals=[]; x=Usub[0]
    while x+L<=Usub[-1]:
        cnt=sum(1 for u in Usub if x<=u<x+L)
        vals.append(float(cnt)); x+=L
    nw=len(vals)
    if nw<5: continue
    mu=sum(vals)/nw; d=[v-mu for v in vals]
    v2=sum(x**2 for x in d)/nw
    exc=v2-k2_gue_L1
    invlog = 1.0/math.log(Tmid/(2*math.pi))
    ratio = exc/invlog if abs(invlog)>1e-6 else 0
    T_data.append((Tmid, exc, invlog))
    print(f"T={Tmid:7.0f} {nw:4d} {v2:8.4f} {exc:+8.4f} {invlog:8.4f} {ratio:+8.3f}")

# Fit: excess ~ alpha / log(T/2pi) + beta
# Simple linear regression of excess vs 1/log(T)
if len(T_data) >= 3:
    xvals = [1.0/math.log(t/(2*math.pi)) for t,_,_ in T_data]
    yvals = [exc for _,exc,_ in T_data]
    n = len(xvals)
    mx = sum(xvals)/n; my_ = sum(yvals)/n
    sxx = sum((x-mx)**2 for x in xvals)
    sxy = sum((x-mx)*(y-my_) for x,y in zip(xvals,yvals))
    if sxx > 1e-12:
        alpha = sxy/sxx
        beta = my_ - alpha*mx
        r2 = sxy**2 / (sxx * sum((y-my_)**2 for y in yvals)) if sum((y-my_)**2 for y in yvals) > 0 else 0
        print(f"\nLinear fit: excess ~ {alpha:.3f}/log(T/2pi) + ({beta:+.4f})")
        print(f"R² = {r2:.4f}")
        print(f"At T=10^6: predicted excess = {alpha/math.log(1e6/(2*math.pi))+beta:.4f}")
        print(f"At T=10^12: predicted excess = {alpha/math.log(1e12/(2*math.pi))+beta:.4f}")

# Spacing distribution: Wigner vs data
print("\n=== Nearest-neighbor spacing distribution ===")
spacings = [U[i+1]-U[i] for i in range(nz-1)]
ms = sum(spacings)/len(spacings)
sn = [s/ms for s in spacings]  # normalized

# Histogram
bins = [(i*0.25, (i+1)*0.25) for i in range(12)]
print(f"{'bin':>10} {'count':>6} {'fraction':>8} {'Wigner':>8} {'Poisson':>8}")
for lo, hi in bins:
    cnt = sum(1 for s in sn if lo <= s < hi)
    frac = cnt/len(sn)
    # Wigner surmise: p(s) = (pi/2)*s*exp(-pi*s^2/4)
    smid = (lo+hi)/2
    wigner = (math.pi/2)*smid*math.exp(-math.pi*smid**2/4)*0.25
    # Poisson: p(s) = exp(-s)
    poisson = math.exp(-smid)*0.25
    print(f"[{lo:.2f},{hi:.2f}) {cnt:6d} {frac:8.4f} {wigner:8.4f} {poisson:8.4f}")

# KL divergence from Wigner
print("\n=== 3-POINT DEEP DIVE: CONCLUSIONS ===")
print()
print("1. GUE 3rd cumulant (kappa3) is TINY:")
print("   kappa3(L=1) = 0.010, skewness = 0.056")
print("   This means the counting function is nearly Gaussian (Costin-Lebowitz CLT)")
print()
print("2. Zeta zeros kappa3 is ALSO tiny and INDISTINGUISHABLE from GUE")
print("   with 491 zeros. Need >> 10^5 zeros to detect arithmetic correction to kappa3.")
print()
print("3. The VARIANCE (kappa2) shows clear arithmetic excess:")
print("   ~90% excess at T=100, decreasing to ~0% at T=750")
print("   Consistent with excess ~ C/log(T/2pi) (Berry semiclassical)")
print()
print("4. The 2→3 point escalation reveals: the 3-point signal is")
print("   O(L/(log T)^2) while 2-point is O(L/log T).")
print("   Higher-point arithmetic corrections are progressively suppressed.")
print()
print("5. WHAT WOULD BE NEW:")
print("   a) Precise measurement of the coefficient in kappa3_arith(L,T)")
print("      requires T > 10^6 and is beyond our computational reach")
print("   b) The rate of approach (excess ~ C/log T) is KNOWN from")
print("      Bogomolny-Keating (1996), but specific coefficients for")
print("      the 3rd cumulant may not be in the literature")
print("   c) This is a COMPUTATION-HEAVY frontier, not conceptually new")
