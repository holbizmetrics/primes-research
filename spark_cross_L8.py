#!/usr/bin/env python3
"""Strike 22: Is <r> = 0.65 a finite-size effect?

GUE random matrices of size N should give <r> → 0.531 as N → ∞.
For small N, <r> can be higher. Let's check with synthetic GUE.

Also: check <r> for zeta zeros (we have many more).
"""
import math, random

# Load zeta zeros from z.txt
zeta_zeros = []
with open('z.txt') as f:
    for line in f:
        try:
            zeta_zeros.append(float(line.strip()))
        except:
            pass

print("Loaded %d zeta zeros" % len(zeta_zeros))
print()

def spacing_ratios(zeros):
    spacings = [zeros[i+1]-zeros[i] for i in range(len(zeros)-1)]
    ratios = []
    for i in range(len(spacings)-1):
        s1, s2 = spacings[i], spacings[i+1]
        if max(s1,s2) > 0:
            ratios.append(min(s1,s2)/max(s1,s2))
    return ratios

# <r> for zeta zeros at different sample sizes
print("=== <r> for zeta zeros at different N ===")
for n in [20, 50, 100, 200, 400, 800]:
    if n > len(zeta_zeros): break
    r = spacing_ratios(zeta_zeros[:n])
    print("  N=%3d: <r> = %.4f" % (n, sum(r)/len(r)))

print()
print("GUE limit: 0.5307")
print("Poisson:   0.3863")
print()

# Synthetic GUE: eigenvalues of random Hermitian matrix
# For small N, <r> has finite-size corrections
print("=== Synthetic GUE <r> at different N ===")

def gue_eigenvalues(N):
    """Generate eigenvalues of N x N GUE matrix"""
    # A = (M + M^*) / (2*sqrt(2N)) where M has iid complex Gaussian entries
    M_real = [[random.gauss(0,1) for _ in range(N)] for _ in range(N)]
    M_imag = [[random.gauss(0,1) for _ in range(N)] for _ in range(N)]
    # Hermitian: H = (M + M^*) / 2
    H = [[0.0]*N for _ in range(N)]
    for i in range(N):
        for j in range(i, N):
            hr = (M_real[i][j] + M_real[j][i]) / 2
            hi = (M_imag[i][j] - M_imag[j][i]) / 2
            H[i][j] = hr  # just use real part for GOE (simpler)
            H[j][i] = hr

    # Use numpy-free eigenvalue computation? Too hard for large N.
    # For small N, use power iteration or just report.
    # Actually, let's just verify with a known N=3 case.
    return None  # Can't do eigendecomposition without numpy

# Instead: generate Poisson and semi-Poisson for comparison
print("=== Poisson test ===")
for N in [20, 50, 100, 200]:
    # Poisson: independent exponential spacings
    ratios = []
    for _ in range(100):  # 100 samples
        spacings = [random.expovariate(1.0) for _ in range(N)]
        for i in range(len(spacings)-1):
            s1, s2 = spacings[i], spacings[i+1]
            if max(s1,s2) > 0:
                ratios.append(min(s1,s2)/max(s1,s2))
    print("  Poisson N=%3d: <r> = %.4f (expect 0.386)" % (N, sum(ratios)/len(ratios)))

print()

# KEY CHECK: how does <r> for L-function zeros depend on which zeros we use?
# Maybe the high <r> is from using LOW-LYING zeros (first ~100)
# vs using zeros at larger height

print("=== <r> for zeta zeros by height range ===")
for start in [0, 100, 200, 400, 600]:
    end = start + 100
    if end > len(zeta_zeros): break
    chunk = zeta_zeros[start:end]
    r = spacing_ratios(chunk)
    if r:
        print("  zeros %d-%d (height %.1f-%.1f): <r> = %.4f" % (
            start, end, chunk[0], chunk[-1], sum(r)/len(r)))

print()
print("If <r> decreases toward 0.531 at larger height: finite-size effect.")
print("If <r> stays high: genuine arithmetic correction to GUE.")
