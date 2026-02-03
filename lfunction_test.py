#!/usr/bin/env python3
"""
Test cross-band covariance for multiple L-functions
Verifying the phase-mixing hypothesis prediction:
- L-functions should have DETERMINISTIC, NEGATIVE covariance
- GUE should have ZERO-MEAN with high variance
"""

import math
import cmath
import random

# Import zeros
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
    # Sample points logarithmically
    xs = [10**(math.log10(2) + k * (math.log10(N) - math.log10(2)) / (n_points - 1))
          for k in range(n_points)]

    # Compute band sums
    E1 = [band_sum(x, zeros1) for x in xs]
    E2 = [band_sum(x, zeros2) for x in xs]

    # Compute means
    mu1 = sum(E1) / len(E1)
    mu2 = sum(E2) / len(E2)

    # Compute covariance
    cov = sum((E1[k] - mu1) * (E2[k] - mu2) for k in range(len(xs))) / len(xs)

    return cov

def generate_gue_zeros(n, density):
    """Generate n zeros with GUE spacing statistics"""
    # Wigner surmise for GUE: p(s) = (32/pi^2) * s^2 * exp(-4s^2/pi)
    zeros = []
    pos = 0
    for _ in range(n):
        # Sample from Wigner distribution using rejection sampling
        while True:
            s = random.expovariate(1) * 0.8  # proposal
            p_s = (32 / math.pi**2) * s**2 * math.exp(-4 * s**2 / math.pi)
            q_s = 1.25 * math.exp(-s / 0.8) / 0.8  # proposal density
            if random.random() < p_s / q_s:
                break
        pos += s / density
        zeros.append(pos)
    return zeros

def main():
    print("=" * 70)
    print("PHASE-MIXING HYPOTHESIS TEST")
    print("Testing: Do L-functions violate PM (deterministic, negative covariance)?")
    print("=" * 70)

    # Use first 50 zeros for comparable analysis
    n_zeros = 50

    # Define bands (same cutoffs for both)
    c1, c2 = 50, 100

    # --- RIEMANN ZETA ---
    print("\n" + "=" * 70)
    print("RIEMANN ZETA FUNCTION")
    print("=" * 70)

    zeta = ZETA_ZEROS[:n_zeros]
    B1_zeta = [g for g in zeta if g < c1]
    B2_zeta = [g for g in zeta if c1 <= g < c2]

    print(f"Using {len(zeta)} zeros with bands at {c1}, {c2}")
    print(f"B1: {len(B1_zeta)} zeros, B2: {len(B2_zeta)} zeros")

    cov_zeta = cross_band_covariance(B1_zeta, B2_zeta)
    print(f"\nCross-band covariance: {cov_zeta:.6f}")

    # --- DIRICHLET BETA ---
    print("\n" + "=" * 70)
    print("DIRICHLET BETA FUNCTION (L(s, chi_4))")
    print("=" * 70)

    beta = BETA_ZEROS[:n_zeros]
    B1_beta = [g for g in beta if g < c1]
    B2_beta = [g for g in beta if c1 <= g < c2]

    print(f"Using {len(beta)} zeros with bands at {c1}, {c2}")
    print(f"B1: {len(B1_beta)} zeros, B2: {len(B2_beta)} zeros")

    cov_beta = cross_band_covariance(B1_beta, B2_beta)
    print(f"\nCross-band covariance: {cov_beta:.6f}")

    # --- GUE COMPARISON ---
    print("\n" + "=" * 70)
    print("GUE RANDOM MATRIX ENSEMBLE (100 realizations)")
    print("=" * 70)

    # Match density to zeta zeros
    density = n_zeros / zeta[-1]

    gue_covs = []
    for _ in range(100):
        gue = generate_gue_zeros(n_zeros, density)
        B1_gue = [g for g in gue if g < c1]
        B2_gue = [g for g in gue if c1 <= g < c2]
        if B1_gue and B2_gue:
            gue_covs.append(cross_band_covariance(B1_gue, B2_gue))

    mean_gue = sum(gue_covs) / len(gue_covs)
    std_gue = math.sqrt(sum((c - mean_gue)**2 for c in gue_covs) / len(gue_covs))

    print(f"Mean covariance: {mean_gue:.6f}")
    print(f"Std deviation: {std_gue:.6f}")
    print(f"Range: [{min(gue_covs):.3f}, {max(gue_covs):.3f}]")

    # Count negative
    neg_count = sum(1 for c in gue_covs if c < 0)
    print(f"Fraction negative: {neg_count}/100 = {neg_count/100:.0%}")

    # --- SUMMARY ---
    print("\n" + "=" * 70)
    print("SUMMARY: PHASE-MIXING HYPOTHESIS TEST")
    print("=" * 70)

    print("\n| L-function | Cov(B1,B2) | vs GUE | PM Status |")
    print("|------------|------------|--------|-----------|")

    zeta_sigma = abs(cov_zeta - mean_gue) / std_gue if std_gue > 0 else float('inf')
    beta_sigma = abs(cov_beta - mean_gue) / std_gue if std_gue > 0 else float('inf')

    zeta_status = "VIOLATES" if zeta_sigma > 2 else "uncertain"
    beta_status = "VIOLATES" if beta_sigma > 2 else "uncertain"

    print(f"| Riemann ζ  | {cov_zeta:+.4f}    | {zeta_sigma:.1f}σ   | {zeta_status} |")
    print(f"| Dirichlet β| {cov_beta:+.4f}    | {beta_sigma:.1f}σ   | {beta_status} |")
    print(f"| GUE (mean) | {mean_gue:+.4f}    | -      | satisfies |")

    print("\n" + "-" * 70)
    print("PREDICTION from theory: Both L-functions should VIOLATE PM")
    print("(deterministic non-zero covariance, negative)")
    print("-" * 70)

    both_negative = cov_zeta < 0 and cov_beta < 0
    both_significant = zeta_sigma > 2 and beta_sigma > 2

    if both_negative and both_significant:
        print("\n✓ PREDICTION CONFIRMED:")
        print("  - Both L-functions have NEGATIVE covariance")
        print("  - Both are statistical outliers from GUE distribution")
        print("  - This supports the phase-mixing hypothesis framework")
    elif both_negative:
        print("\n◐ PARTIAL SUPPORT:")
        print("  - Both L-functions have NEGATIVE covariance")
        print(f"  - Statistical significance: zeta={zeta_sigma:.1f}σ, beta={beta_sigma:.1f}σ")
    else:
        print("\n✗ UNEXPECTED RESULT - requires investigation")

    # Determinism check
    print("\n" + "-" * 70)
    print("DETERMINISM CHECK")
    print("-" * 70)
    print("L-functions: Single realization (deterministic by construction)")
    print(f"GUE variance across realizations: {std_gue**2:.4f}")
    print("→ L-function values are FIXED; GUE values FLUCTUATE")

if __name__ == "__main__":
    main()
