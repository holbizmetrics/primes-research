import math
import subprocess
import re

# Sinc kernel for GUE
def K(x):
    if abs(x) < 1e-14:
        return 1.0
    return math.sin(math.pi * x) / (math.pi * x)

# GUE cumulants via numerical integration
print("=== GUE cumulants (kernel integration, n=25 grid) ===")
print(f"{'L':>5}  {'kappa2':>8}  {'kappa3':>10}")
Lvals = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
gue_k2 = {}
gue_k3 = {}
for L in Lvals:
    nn = 25
    dx = L / nn
    # kappa2 = L - int int K(x-y)^2 dx dy
    s2 = 0.0
    for a in range(nn):
        xa = (a + 0.5) * dx
        for b in range(nn):
            xb = (b + 0.5) * dx
            s2 += K(xa - xb)**2 * dx**2
    k2 = L - s2

    # kappa3 = 2 * triple integral of K(a-b)*K(b-c)*K(a-c)
    s3 = 0.0
    for a in range(nn):
        xa = (a + 0.5) * dx
        for b in range(nn):
            xb = (b + 0.5) * dx
            kab = K(xa - xb)
            for c in range(nn):
                xc = (c + 0.5) * dx
                s3 += 2 * kab * K(xb - xc) * K(xa - xc) * dx**3

    gue_k2[L] = k2
    gue_k3[L] = s3
    print(f"L={L:4.1f}  k2={k2:8.5f}  k3={s3:+10.5f}")

# Now get zeta zeros from PARI/GP
print("\nGetting zeta zeros from PARI/GP...")
result = subprocess.run(
    ['gp', '-q'],
    input='Z=lfunzeros(1,300);for(i=1,#Z,printf("%.10f\\n",Z[i]))\n',
    capture_output=True, text=True, timeout=30
)
zeros = [float(x) for x in result.stdout.strip().split('\n') if x.strip()]
print(f"Got {len(zeros)} zeros")

# Unfolding: N(T) ~ T/(2pi) * log(T/(2pi*e)) + 7/8
def Nsmooth(t):
    if t < 1:
        return 0.0
    return t / (2*math.pi) * math.log(t / (2*math.pi*math.e)) + 7.0/8.0

U = [Nsmooth(z) for z in zeros]
nz = len(U)

# Compute counting function statistics
print(f"\n=== Zeta zero counting cumulants (N={nz} zeros) ===")
print(f"{'L':>5}  {'nw':>4}  {'mean':>7}  {'var':>8}  {'mu3':>10}  {'skew':>7}  {'gue_k2':>8}  {'gue_k3':>10}  k3_ratio")
print("-" * 95)

for L in Lvals:
    vals = []
    for j in range(nz):
        x0 = U[j]
        if x0 + L > U[-1]:
            break
        cnt = sum(1 for k in range(j, nz) if U[k] < x0 + L)
        vals.append(float(cnt))

    nw = len(vals)
    if nw < 20:
        continue

    mu = sum(vals) / nw
    d = [v - mu for v in vals]
    v2 = sum(x**2 for x in d) / nw
    v3 = sum(x**3 for x in d) / nw
    skew = v3 / v2**1.5 if v2 > 1e-6 else 0

    k2g = gue_k2.get(L, 0)
    k3g = gue_k3.get(L, 0)
    ratio = v3 / k3g if abs(k3g) > 1e-6 else float('inf')

    print(f"L={L:4.1f}  {nw:4d}  {mu:7.3f}  {v2:8.5f}  {v3:+10.5f}  {skew:+7.3f}  {k2g:8.5f}  {k3g:+10.5f}  {ratio:+8.4f}")

print("\n=== Analysis ===")
print("If kappa3_zeta / kappa3_GUE ~ 1: GUE matches")
print("If ratio << 1 or negative: arithmetic corrections dominate")
print("GUE kappa2 = number variance (Sigma2) - should match for small L, excess for large L")
