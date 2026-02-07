import math, subprocess
"""
Statistical power analysis for 3rd cumulant detection.

GUE predicts kappa3(L=2) ~ 2.76
If actual kappa3 ~ 2.76, then with n independent windows:
  var(sample_mu3) ~ (mu6 - mu3^2)/n

For GUE, the 6th central moment is large, so we need MANY windows.

For a rough estimate: if the distribution is approximately Gaussian with var=sigma^2,
  mu3 ~ 0 (Gaussian has zero skewness)
  mu6 ~ 15*sigma^6

Actually for GUE counting statistics:
  kappa_2 ~ 0.4 for L=2 (sigma^2 ~ 0.4, sigma ~ 0.63)
  kappa_3 ~ 2.76 for L=2

Wait: kappa_3 = 2.76 is the GUE prediction. But the count is INTEGER-valued.
For L=2 and mean=2, the count takes values 0,1,2,3,4,...
With var=0.4, typical spread is ±0.63.
Third moment = sum of (count-2)^3 * P(count) / n_windows
For counts mostly 1,2,3:
  (1-2)^3 = -1, (2-2)^3 = 0, (3-2)^3 = +1
So mu3 = P(count=3) - P(count=1) + higher terms

Actually kappa3 = 2.76 seems WAY too large for integer counts with sigma ~ 0.63
sigma^3 = 0.25, so skewness = kappa3/sigma^3 = 2.76/0.25 = 11 ???

That can't be right. Let me recheck the GUE formula.
"""

# Let's verify by direct simulation of GUE
import random
random.seed(42)

def gue_eigenvalues(N):
    """Sample eigenvalues of N×N GUE matrix using tridiagonal reduction"""
    # GUE tridiagonal: diagonal ~ N(0,1), off-diag ~ chi_{n-1}/sqrt(2)
    # But simplest: direct matrix
    import cmath
    # Actually let's just do 2x2 for simplicity
    # For large N, eigenvalue density is semicircle on [-2sqrt(N), 2sqrt(N)]
    # Local statistics at the bulk are GUE

    # Simple: Box-Muller for Gaussian
    def randn():
        u1 = random.random()
        u2 = random.random()
        return math.sqrt(-2*math.log(u1+1e-15))*math.cos(2*math.pi*u2)

    # Generate NxN Hermitian matrix H = (A + A^*)/2 where A has complex Gaussian entries
    H = [[0.0]*N for _ in range(N)]
    for i in range(N):
        H[i][i] = randn()  # diagonal is real N(0,1)
        for j in range(i+1, N):
            re = randn() / math.sqrt(2)
            im = randn() / math.sqrt(2)
            H[i][j] = re  # for eigenvalue computation we'll use real symmetric
            H[j][i] = re

    # Eigenvalues via power iteration... too slow for large N
    # Use numpy if available, else skip
    return None  # placeholder

# Actually let's not simulate GUE. Instead, let's check: is the formula right?
# For determinantal processes with kernel K:
# kappa_n = integral of the n-th cluster function T_n
# T_2(x,y) = -K(x,y)^2  => kappa_2 = -int K^2 < 0 ...
# But Sigma2 = L + kappa_2 = L - int K^2 > 0  ✓
#
# T_3(x,y,z) = 2*K(x,y)*K(y,z)*K(z,x)
# kappa_3 = int T_3 = 2*int K*K*K
#
# This is POSITIVE for sine kernel (K > 0 for |x| < 1, oscillates for |x| > 1)
#
# For L=1: the integration domain is [0,1]^3
# K(x-y) = sin(pi(x-y))/(pi(x-y)) for x,y in [0,1]
# |x-y| < 1 always, so K > 0 for all pairs? No:
# K(0.9-0.1) = K(0.8) = sin(0.8*pi)/(0.8*pi) = sin(2.51)/2.51 = 0.588/2.51 = 0.234
# K is positive for |x|<1, zero at |x|=1, negative for 1<|x|<2, etc.
# For L=1: all differences |xi-xj| < 1, so K > 0 everywhere
# => integral of K*K*K is definitely positive
#
# For L=2: differences can be up to 2, so K can be negative
# K(1.5) = sin(1.5*pi)/(1.5*pi) = (-1)/(4.71) = -0.212
# Product of three K values: K(a-b)*K(b-c)*K(a-c)
# Can be positive or negative depending on signs

# Let me just verify numerically what kappa3 should be for L=1
def K(x):
    return 1.0 if abs(x)<1e-14 else math.sin(math.pi*x)/(math.pi*x)

# Very fine grid for L=1
L = 1.0
nn = 40
dx = L/nn
s3 = 0.0
for a in range(nn):
    xa = (a+0.5)*dx
    for b in range(nn):
        xb = (b+0.5)*dx
        kab = K(xa-xb)
        for c in range(nn):
            xc = (c+0.5)*dx
            s3 += 2*kab*K(xb-xc)*K(xa-xc)*dx**3
print(f"kappa3(L=1) = {s3:.6f}")

# And kappa2
s2 = 0.0
for a in range(nn):
    xa = (a+0.5)*dx
    for b in range(nn):
        xb = (b+0.5)*dx
        s2 += K(xa-xb)**2*dx**2
k2 = L - s2
print(f"kappa2(L=1) = {k2:.6f}")
print(f"sigma = {math.sqrt(k2):.4f}")
print(f"skewness = kappa3/sigma^3 = {s3/k2**1.5:.4f}")

# The skewness is huge! This means the distribution is VERY non-Gaussian.
# For integer-valued counts, this is plausible if the distribution is very peaked.

# Let's compute the actual GUE gap distribution for nearest-neighbor
# and see what the count distribution looks like at L=1
# P(N([0,1]) = 0) = probability of no eigenvalue in interval of length 1
# P(N([0,1]) = k) for the sine-kernel determinantal process

# Actually, for the sine kernel det process:
# P(N([0,L])=0) = det(I - K_L) where K_L is the integral operator on [0,L]
# This is known: the gap probability E(0,L) = product formula
# E(0,L) ~ exp(-pi^2*L^2/... )  for large L
# For L=1: E(0,1) ~ 0.48  (about half the time there's no zero in a unit interval)
# With mean = 1, P(0) ~ 0.48 means P(1) + P(2) + ... ~ 0.52

# Actually let me look at the actual zeta zeros
r = subprocess.run(['gp','-q'], input='Z=lfunzeros(1,300);for(i=1,#Z,printf("%.10f\\n",Z[i]))\n',
                    capture_output=True, text=True, timeout=30)
zeros = [float(x) for x in r.stdout.strip().split('\n') if x.strip()]
nz = len(zeros)
def Ns(t): return t/(2*math.pi)*math.log(t/(2*math.pi*math.e))+7/8
U = [Ns(z) for z in zeros]

# Count distribution at L=1
from collections import Counter
counts = Counter()
x = U[0]
while x + 1.0 <= U[-1]:
    c = sum(1 for u in U if x <= u < x+1.0)
    counts[c] += 1
    x += 1.0
total = sum(counts.values())
print(f"\nCount distribution for L=1 (non-overlapping, {total} windows):")
for k in sorted(counts.keys()):
    print(f"  N=={k}: {counts[k]} ({100*counts[k]/total:.1f}%)")

# For L=2
counts2 = Counter()
x = U[0]
while x + 2.0 <= U[-1]:
    c = sum(1 for u in U if x <= u < x+2.0)
    counts2[c] += 1
    x += 2.0
total2 = sum(counts2.values())
print(f"\nCount distribution for L=2 (non-overlapping, {total2} windows):")
for k in sorted(counts2.keys()):
    print(f"  N=={k}: {counts2[k]} ({100*counts2[k]/total2:.1f}%)")

# For L=5
counts5 = Counter()
x = U[0]
while x + 5.0 <= U[-1]:
    c = sum(1 for u in U if x <= u < x+5.0)
    counts5[c] += 1
    x += 5.0
total5 = sum(counts5.values())
print(f"\nCount distribution for L=5 (non-overlapping, {total5} windows):")
for k in sorted(counts5.keys()):
    print(f"  N=={k}: {counts5[k]} ({100*counts5[k]/total5:.1f}%)")

print(f"\n=== BOTTOM LINE ===")
print(f"kappa3(GUE, L=1) = {s3:.4f}, but sigma^3 = {k2**1.5:.4f}")
print(f"So GUE skewness = {s3/k2**1.5:.2f}")
print(f"To detect skew={s3/k2**1.5:.2f} at 2-sigma with {total} windows:")
print(f"  SE(skewness) ~ sqrt(6/n) = {math.sqrt(6/total):.3f}")
print(f"  Z-score ~ skew/SE = {(s3/k2**1.5)/math.sqrt(6/total):.2f}")
print(f"Need n > 6*(2/skew)^2 = {6*(2/(s3/k2**1.5))**2:.0f} independent windows for 2-sigma detection")
