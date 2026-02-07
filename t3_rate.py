#!/usr/bin/env python3
"""Rate of approach to GUE: how does variance excess depend on T?"""
import math

def K(x):
    return 1.0 if abs(x)<1e-14 else math.sin(math.pi*x)/(math.pi*x)

with open('/data/data/com.termux/files/home/primes-research/z.txt') as f:
    zeros = sorted(set(float(line.strip()) for line in f if line.strip()))

def Ns(t): return t/(2*math.pi)*math.log(t/(2*math.pi*math.e))+7/8
U = [Ns(z) for z in zeros]
nz = len(U)

# GUE kappa2 at L=1
nn=30; dx=1.0/nn
p2=sum(K((a-b)*dx)**2*dx**2 for a in range(nn) for b in range(nn))
k2_gue = 1.0-p2
print(f"GUE Sigma2(L=1) = {k2_gue:.5f}")
print(f"Poisson var(L=1) = 1.0")
print()

# Split into bins by T-height and compute variance at L=1 in each
# Use blocks of ~60 zeros
block_size = 60
L = 1.0

print(f"{'T_mid':>8} {'n_win':>6} {'var':>8} {'excess':>8} {'(var-GUE)/GUE':>14} {'lag1':>7}")
print("-"*60)

for start in range(0, nz-block_size+1, block_size):
    end = min(start+block_size, nz)
    Usub = U[start:end]
    Tmid = zeros[(start+end)//2]

    # Non-overlapping count at L=1
    vals=[]; x=Usub[0]
    while x+L<=Usub[-1]:
        cnt=sum(1 for u in Usub if x<=u<x+L)
        vals.append(float(cnt)); x+=L
    nw=len(vals)
    if nw<5: continue
    mu=sum(vals)/nw; d=[v-mu for v in vals]
    v2=sum(x**2 for x in d)/nw
    exc=v2-k2_gue
    ratio=(v2-k2_gue)/k2_gue

    # Also compute spacing lag-1 autocorrelation
    spacings = [Usub[i+1]-Usub[i] for i in range(len(Usub)-1)]
    ms=sum(spacings)/len(spacings)
    ds=[s-ms for s in spacings]
    vs=sum(x**2 for x in ds)/len(ds)
    cov=sum(ds[i]*ds[i+1] for i in range(len(ds)-1))/(len(ds)-1)
    lag1=cov/vs if vs>1e-6 else 0

    print(f"T={Tmid:7.0f} {nw:6d} {v2:8.4f} {exc:+8.4f} {ratio:+14.3f} {lag1:+7.3f}")

# Now let's check: does the excess scale as 1/log(T)?
# Berry-Keating: the non-universal correction to pair correlation is
# R2_arith(x) ~ -(1/2pi) * sum_p (log p)^2 / p * cos(x*log(p))
# integrated over x from 0 to L:
# Sigma2_arith(L) ~ (1/(2*pi^2)) * sum_p (log p)^2 / p * (L - sin(L*log(p))/log(p))
# The dominant term for L not too large is proportional to sum_p (log p)^2/p ~ log(T)
# Wait, that's the PRIME sum, which diverges. The actual formula involves a cutoff.

# Goldston (1987): the number variance of zeta zeros includes
# Sigma2_total(L) = Sigma2_GUE(L) + (2/pi^2) * (Li_2(exp(-L*2*pi/log(T/2pi))) + ...)
# For L << log(T/(2*pi)), the excess is approximately L/(log(T/(2*pi)))

print(f"\n=== Predicted arithmetic excess at L=1 ===")
for Tmid in [50, 100, 200, 500]:
    logN = math.log(Tmid/(2*math.pi))
    predicted = 1.0/logN  # very rough: excess ~ L/log(T/2pi)
    print(f"T={Tmid:4.0f}  log(T/2pi)={logN:.2f}  predicted_excess~{predicted:.4f}")

print(f"\nThe excess should DECREASE as T grows (zeros become more GUE-like)")
print("This is exactly Berry's semiclassical correspondence:")
print("  small T → classical (large excess, Poisson-like)")
print("  large T → quantum (small excess, GUE-like)")
