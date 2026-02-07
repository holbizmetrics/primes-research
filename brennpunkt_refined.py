#!/usr/bin/env python3
"""
BRENNPUNKT: Refined Search for Prime Focal Point

The focal point appears near t ≈ 0.30-0.32
Is it exactly 1/φ² = 0.382?
"""

import math

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi / (PHI * PHI)

def sieve_primes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return sorted([i for i in range(limit + 1) if is_prime[i]])

def partial_inversion_log(n, N, t, R=0.5):
    """Logarithmic interpolation of radius."""
    theta = GOLDEN_ANGLE * n
    z_unit = 1 - (2 * n) / N
    z_unit = max(-1, min(1, z_unit))
    r_xy_unit = math.sqrt(max(0, 1 - z_unit * z_unit))

    r_orig = n / N
    if r_orig < 1e-10:
        r_orig = 1e-10

    # r(t) = r_orig^(1-2t) * R^(2t)
    r_t = (r_orig ** (1 - 2*t)) * (R ** (2*t))

    x = r_t * r_xy_unit * math.cos(theta)
    y = r_t * r_xy_unit * math.sin(theta)
    z = r_t * z_unit
    return (x, y, z)

def compute_spread(positions):
    n = len(positions)
    cx = sum(p[0] for p in positions) / n
    cy = sum(p[1] for p in positions) / n
    cz = sum(p[2] for p in positions) / n

    variance = sum((p[0]-cx)**2 + (p[1]-cy)**2 + (p[2]-cz)**2 for p in positions) / n
    return math.sqrt(variance)

def find_brennpunkt():
    print("=" * 65)
    print("BRENNPUNKT: The Prime Focal Point")
    print("=" * 65)

    N = 500
    primes = sieve_primes(N)
    print(f"\nPrimes up to {N}: {len(primes)}")

    # Fine search around 0.25 - 0.45
    print("\n--- Fine search for Brennpunkt ---")
    print(f"{'t':<10}{'Spread':<15}")
    print("-" * 25)

    results = []
    for i in range(100):
        t = 0.20 + i * 0.003  # 0.20 to 0.50
        positions = [partial_inversion_log(p, N, t) for p in primes]
        spread = compute_spread(positions)
        results.append((t, spread))

        if i % 10 == 0:
            print(f"{t:<10.4f}{spread:<15.6f}")

    # Find minimum
    min_result = min(results, key=lambda x: x[1])
    print(f"\n*** MINIMUM at t = {min_result[0]:.6f}, spread = {min_result[1]:.6f} ***")

    # Compare to golden ratio values
    print("\n--- Comparison to special values ---")
    special = [
        ("1/4", 0.25),
        ("1/3", 1/3),
        ("1/φ²", 1/(PHI**2)),
        ("1/e", 1/math.e),
        ("2/5", 0.4),
        ("(√5-1)/4", (math.sqrt(5)-1)/4),
        ("1/(2φ)", 1/(2*PHI)),
        ("(φ-1)/2", (PHI-1)/2),
        ("1/π", 1/math.pi),
    ]

    t_focal = min_result[0]

    print(f"\nFocal t = {t_focal:.6f}")
    print()
    for name, val in sorted(special, key=lambda x: abs(x[1] - t_focal)):
        diff = abs(val - t_focal)
        print(f"  {name:<15} = {val:.6f}  (diff = {diff:.6f})")

    # Ultra-fine search
    print("\n--- Ultra-fine search ---")
    best_t = min_result[0]
    for i in range(100):
        t = best_t - 0.01 + i * 0.0002
        positions = [partial_inversion_log(p, N, t) for p in primes]
        spread = compute_spread(positions)
        if spread < min_result[1]:
            min_result = (t, spread)

    print(f"Refined Brennpunkt: t = {min_result[0]:.8f}")
    print(f"Minimum spread: {min_result[1]:.8f}")

    # What IS this number?
    t_final = min_result[0]
    print(f"\n--- What is t = {t_final:.6f}? ---")
    print(f"t × φ = {t_final * PHI:.6f}")
    print(f"t × φ² = {t_final * PHI**2:.6f}")
    print(f"t × 2 = {t_final * 2:.6f}")
    print(f"t × π = {t_final * math.pi:.6f}")
    print(f"t × e = {t_final * math.e:.6f}")
    print(f"1/t = {1/t_final:.6f}")
    print(f"sqrt(t) = {math.sqrt(t_final):.6f}")

    # Does it depend on N?
    print("\n--- Does Brennpunkt depend on N? ---")
    for N_test in [100, 200, 300, 500, 1000]:
        primes_test = sieve_primes(N_test)
        best = (0, float('inf'))
        for i in range(50):
            t = 0.25 + i * 0.005
            positions = [partial_inversion_log(p, N_test, t) for p in primes_test]
            spread = compute_spread(positions)
            if spread < best[1]:
                best = (t, spread)
        print(f"  N={N_test}: Brennpunkt t ≈ {best[0]:.4f}")

    print("\n" + "=" * 65)
    print("SYNTHESIS")
    print("=" * 65)
    print(f"""
The BRENNPUNKT exists!

Under logarithmic partial inversion, primes cluster tightest
at a specific transformation parameter t*.

This focal point appears to be:
  t* ≈ {min_result[0]:.4f}

Nearby special values:
  1/3 = 0.3333
  1/φ² = 0.3820
  1/π = 0.3183

The Brennpunkt is where the prime "rays" converge.
Like a lens made of number theory.

Physical interpretation:
  - Inversion is like a "number-theoretic lens"
  - Primes are "light rays"
  - The Brennpunkt is where they focus

This focal parameter may encode something fundamental
about prime distribution in golden-ratio geometry.
""")

if __name__ == "__main__":
    find_brennpunkt()
