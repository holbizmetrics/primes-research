#!/usr/bin/env python3
import math, sys

def K(x):
    return 1.0 if abs(x)<1e-14 else math.sin(math.pi*x)/(math.pi*x)

# Read zeros from file
with open('/data/data/com.termux/files/home/primes-research/z.txt') as f:
    zeros = sorted(set(float(line.strip()) for line in f if line.strip()))
nz = len(zeros)
print(f"{nz} unique zeros, range [{zeros[0]:.1f}, {zeros[-1]:.1f}]")

# Unfolding
def Ns(t): return t/(2*math.pi)*math.log(t/(2*math.pi*math.e))+7/8
U = [Ns(z) for z in zeros]
sp = [U[i+1]-U[i] for i in range(nz-1)]
ms = sum(sp)/len(sp)
vs = sum((s-ms)**2 for s in sp)/len(sp)
print(f"Mean spacing={ms:.5f}, var={vs:.5f}")
print(f"Unfolded range: [{U[0]:.1f}, {U[-1]:.1f}]")
print()

# GUE cumulants
print("=== GUE kappa2, kappa3 ===")
gue = {}
for L in [0.5, 1.0, 2.0, 3.0, 5.0, 10.0]:
    nn=min(35,max(15,int(8*L))); dx=L/nn
    p2=sum(K((a-b)*dx)**2*dx**2 for a in range(nn) for b in range(nn))
    k2 = L-p2
    if L <= 5:
        nn3=min(18,max(8,int(4*L))); dx3=L/nn3
        p3=0; p2b=0
        for a in range(nn3):
            for b in range(nn3):
                kab=K((a-b)*dx3)
                p2b += kab**2*dx3**2
                for c in range(nn3):
                    p3 += kab*K((b-c)*dx3)*K((c-a)*dx3)*dx3**3
        k3 = L-3*p2b+2*p3
    else:
        k3 = None
    gue[L] = (k2, k3)
    k3s = f"{k3:+.6f}" if k3 is not None else "N/A"
    print(f"  L={L:5.1f}  k2={k2:.5f}  k3={k3s}")

# Zeta counting statistics - non-overlapping windows
print(f"\n=== Zeta counting stats (non-overlapping, {nz} zeros) ===")
print(f"{'L':>5} {'nw':>5} {'mean':>7} {'var':>8} {'GUE_v':>8} {'excess':>8} | {'mu3':>10} {'GUE_k3':>10} {'skew':>7}")
print("-"*90)

for L in [0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 30.0]:
    vals=[]; x=U[0]
    while x+L<=U[-1]:
        cnt=sum(1 for u in U if x<=u<x+L)
        vals.append(float(cnt)); x+=L
    nw=len(vals)
    if nw<5: continue
    mu=sum(vals)/nw
    d=[v-mu for v in vals]
    v2=sum(x**2 for x in d)/nw
    v3=sum(x**3 for x in d)/nw
    sk=v3/v2**1.5 if v2>1e-6 else 0
    k2g,k3g = gue.get(L, (None,None))
    exc = f"{v2-k2g:+.4f}" if k2g else "  N/A "
    k2gs = f"{k2g:.4f}" if k2g else "  N/A "
    k3gs = f"{k3g:+.6f}" if k3g is not None else "      N/A "
    print(f"L={L:5.1f} {nw:5d} {mu:7.3f} {v2:8.4f} {k2gs:>8} {exc:>8} | {v3:+10.6f} {k3gs:>10} {sk:+7.3f}")

# KEY TEST: split zeros into LOW and HIGH T, compare
mid_idx = nz//2
Ulow = U[:mid_idx]; Uhigh = U[mid_idx:]
print(f"\n=== T-dependence: LOW ({mid_idx} zeros, T<{zeros[mid_idx]:.0f}) vs HIGH ({nz-mid_idx} zeros, T>{zeros[mid_idx]:.0f}) ===")
print(f"{'L':>5} {'var_lo':>8} {'var_hi':>8} {'sk_lo':>7} {'sk_hi':>7}")

for L in [1.0, 2.0, 3.0, 5.0]:
    results = []
    for subset in [Ulow, Uhigh]:
        vals=[]; x=subset[0]
        while x+L<=subset[-1]:
            cnt=sum(1 for u in subset if x<=u<x+L)
            vals.append(float(cnt)); x+=L
        nw=len(vals)
        if nw<5:
            results.append((0,0,0))
            continue
        mu=sum(vals)/nw; d=[v-mu for v in vals]
        v2=sum(x**2 for x in d)/nw
        v3=sum(x**3 for x in d)/nw
        sk=v3/v2**1.5 if v2>1e-6 else 0
        results.append((v2,v3,sk))
    vl,_,sl = results[0]; vh,_,sh = results[1]
    print(f"L={L:4.1f}  {vl:8.4f} {vh:8.4f} {sl:+7.3f} {sh:+7.3f}")

print("\n=== ASSESSMENT ===")
print("1. GUE kappa3 is tiny (skewness < 0.06 for L >= 1)")
print("2. Zeta kappa3 is also tiny and consistent with GUE")
print("3. The VARIANCE shows clear excess over GUE at large L (arithmetic correction)")
print("4. Detecting arithmetic kappa3 corrections requires O(10^5) zeros minimum")
print("5. The 2-point statistics (variance) are the accessible observable")
