#!/usr/bin/env python3
"""
Test cross-band covariance for multiple L-functions (v2)
Using INDEX-BASED bands instead of VALUE-BASED bands
to ensure comparable populations across L-functions.
"""

import math
import cmath
import random

from zeros_500 import ZEROS as ZETA_ZEROS
from beta_zeros import BETA_ZEROS

def spectral_contribution(x, gamma):
    """Contribution from zero at gamma to E(x)"""
    rho = complex(0.5, gamma)
    return -2 * (math.sqrt(x) * cmath.exp(1j * gamma * math.log(x)) / rho).real

def band_sum(x, zeros):
    """Sum of spectral contributions from a list of zeros"""
    return sum(spectral_contribution(x, g) for g in zeros)

def cross_band_covariance(zeros1, zeros2, N=10000, n_points=100):
    """Compute cross-band covariance between two sets of zeros"""
    xs = [10**(math.log10(2) + k * (math.log10(N) - math.log10(2)) / (n_points - 1))
          for k in range(n_points)]

    E1 = [band_sum(x, zeros1) for x in xs]
    E2 = [band_sum(x, zeros2) for x in xs]

    mu1 = sum(E1) / len(E1)
    mu2 = sum(E2) / len(E2)

    cov = sum((E1[k] - mu1) * (E2[k] - mu2) for k in range(len(xs))) / len(xs)
    return cov

def generate_gue_zeros(n, first_zero, last_zero):
    """Generate n zeros with GUE spacing, matching range"""
    density = n / (last_zero - first_zero)
    zeros = []
    pos = first_zero
    for _ in range(n):
        while True:
            s = random.expovariate(1) * 0.8
            p_s = (32 / math.pi**2) * s**2 * math.exp(-4 * s**2 / math.pi)
            q_s = 1.25 * math.exp(-s / 0.8) / 0.8
            if random.random() < p_s / q_s:
                break
        pos += s / density
        zeros.append(pos)
    return zeros

def analyze_lfunction(name, zeros, n_total=50, n_band1=15, n_gue=100):
    """Analyze a single L-function's cross-band covariance"""
    print(f"\n{'='*60}")
    print(f"{name}")
    print(f"{'='*60}")

    # Use first n_total zeros
    all_zeros = zeros[:n_total]

    # Index-based bands
    B1 = all_zeros[:n_band1]
    B2 = all_zeros[n_band1:]

    print(f"Total zeros: {len(all_zeros)}")
    print(f"B1 (zeros 1-{n_band1}): {len(B1)} zeros, range [{B1[0]:.2f}, {B1[-1]:.2f}]")
    print(f"B2 (zeros {n_band1+1}-{n_total}): {len(B2)} zeros, range [{B2[0]:.2f}, {B2[-1]:.2f}]")

    cov = cross_band_covariance(B1, B2)
    print(f"\nCross-band covariance: {cov:.4f}")

    # GUE comparison with matched density
    gue_covs = []
    for _ in range(n_gue):
        gue = generate_gue_zeros(n_total, all_zeros[0], all_zeros[-1])
        gue_B1 = gue[:n_band1]
        gue_B2 = gue[n_band1:]
        gue_covs.append(cross_band_covariance(gue_B1, gue_B2))

    mean_gue = sum(gue_covs) / len(gue_covs)
    std_gue = math.sqrt(sum((c - mean_gue)**2 for c in gue_covs) / len(gue_covs))

    sigma = (cov - mean_gue) / std_gue if std_gue > 0 else 0

    print(f"\nGUE comparison:")
    print(f"  GUE mean: {mean_gue:.4f}")
    print(f"  GUE std:  {std_gue:.4f}")
    print(f"  {name} is {sigma:.2f}σ from GUE mean")
    print(f"  Sign: {'NEGATIVE' if cov < 0 else 'POSITIVE'}")

    neg_frac = sum(1 for c in gue_covs if c < 0) / len(gue_covs)
    print(f"  GUE negative fraction: {neg_frac:.0%}")

    return cov, mean_gue, std_gue

def main():
    print("=" * 60)
    print("CROSS-BAND COVARIANCE: L-FUNCTIONS vs GUE")
    print("Using INDEX-based bands (same population per band)")
    print("=" * 60)

    # Analyze both L-functions
    results = {}

    results['zeta'] = analyze_lfunction("RIEMANN ZETA ζ(s)", ZETA_ZEROS)
    results['beta'] = analyze_lfunction("DIRICHLET BETA β(s) = L(s,χ₄)", BETA_ZEROS)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print("\n| L-function    | Cov(B1,B2) | vs GUE mean | Sign     |")
    print("|---------------|------------|-------------|----------|")

    for name, (cov, gue_mean, gue_std) in results.items():
        sigma = (cov - gue_mean) / gue_std if gue_std > 0 else 0
        sign = "NEGATIVE" if cov < 0 else "positive"
        print(f"| {name:13} | {cov:+10.4f} | {sigma:+.2f}σ       | {sign:8} |")

    print("\n" + "-" * 60)
    print("PHASE-MIXING PREDICTION:")
    print("L-functions with explicit formulas should have")
    print("DETERMINISTIC covariance (not zero-mean like GUE).")
    print("-" * 60)

    # Key insight
    print("\n*** KEY OBSERVATION ***")
    zeta_cov = results['zeta'][0]
    beta_cov = results['beta'][0]
    print(f"Zeta covariance:  {zeta_cov:.4f}")
    print(f"Beta covariance:  {beta_cov:.4f}")
    print(f"Difference:       {abs(zeta_cov - beta_cov):.4f}")
    print("\nBoth are DETERMINISTIC (single values, not distributions).")
    print("This is the key distinction from GUE (which fluctuates).")

if __name__ == "__main__":
    main()
