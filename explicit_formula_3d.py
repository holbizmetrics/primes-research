#!/usr/bin/env python3
"""
Explicit Formula in 3D - Using actual Riemann contribution

The explicit formula gives:
  ψ(x) = x - Σ_ρ (x^ρ)/ρ - log(2π) - ½log(1-x⁻²)

Each zero contributes: -x^ρ/ρ = -x^(1/2+iγ)/(1/2+iγ)

The real part of this oscillates as x changes.
Project this into 3D golden-spiral space.
"""

import math

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi / (PHI * PHI)

ZETA_ZEROS = [
    14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
    37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478,
    52.970321478, 56.446247697, 59.347044003, 60.831778525, 65.112544048,
    67.079810529, 69.546401711, 72.067157674, 75.704690699, 77.144840069,
    79.337375020, 82.910380854, 84.735492981, 87.425274613, 88.809111208,
    92.491899271, 94.651344041, 95.870634228, 98.831194218, 101.317851006,
]

def sieve_primes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]

def explicit_oscillation(x, zeros, num_zeros=20):
    """
    Calculate the oscillatory part from zeta zeros at point x.

    From explicit formula: -Σ x^ρ/ρ where ρ = 1/2 + iγ

    x^ρ = x^(1/2) * e^(iγ log x) = √x * (cos(γ log x) + i sin(γ log x))

    Real part of -x^ρ/ρ involves √x * cos(γ log x - arg(ρ)) / |ρ|
    """
    if x <= 1:
        return 0

    sqrt_x = math.sqrt(x)
    log_x = math.log(x)

    total = 0
    for gamma in zeros[:num_zeros]:
        # |ρ| = |1/2 + iγ| = sqrt(1/4 + γ²)
        rho_mag = math.sqrt(0.25 + gamma * gamma)

        # arg(ρ) = arctan(γ / 0.5) = arctan(2γ)
        rho_arg = math.atan(2 * gamma)

        # Contribution: -2 * Re(x^ρ / ρ)
        # = -2 * √x * cos(γ log x - rho_arg) / rho_mag
        contribution = -2 * sqrt_x * math.cos(gamma * log_x - rho_arg) / rho_mag
        total += contribution

    return total

def golden_spiral_sphere(n, total=500):
    """Map n to unit sphere via golden spiral."""
    if n <= 0:
        return (0, 0, 1)

    theta = GOLDEN_ANGLE * n
    z = 1 - (2 * n) / total
    z = max(-1, min(1, z))
    r_xy = math.sqrt(max(0, 1 - z*z))
    x = r_xy * math.cos(theta)
    y = r_xy * math.sin(theta)

    return (x, y, z)

def angular_distance(p1, p2):
    """Angular distance between two points on sphere."""
    dot = sum(a*b for a, b in zip(p1, p2))
    dot = max(-1, min(1, dot))
    return math.acos(dot)

def neighborhood_oscillation(n, radius_indices=5):
    """
    Average oscillation in neighborhood of n on the 3D sphere.
    """
    center = golden_spiral_sphere(n)
    values = []

    for dn in range(-radius_indices, radius_indices + 1):
        m = n + dn
        if m >= 2:
            osc = explicit_oscillation(m, ZETA_ZEROS, 20)
            point = golden_spiral_sphere(m)
            dist = angular_distance(center, point)
            weight = math.exp(-dist * 5)  # Closer = more weight
            values.append((osc, weight))

    if not values:
        return 0

    total_weight = sum(w for _, w in values)
    if total_weight == 0:
        return 0

    return sum(o * w for o, w in values) / total_weight

def analyze_explicit_3d():
    print("=" * 65)
    print("EXPLICIT FORMULA OSCILLATION IN 3D")
    print("Using actual Riemann explicit formula contribution")
    print("=" * 65)

    LIMIT = 300
    primes = set(sieve_primes(LIMIT))
    prime_list = sorted(primes)

    print(f"\nAnalyzing n = 2 to {LIMIT}")
    print(f"Primes: {len(primes)}")
    print()

    # Calculate explicit formula oscillation for each n
    oscillations = []
    for n in range(2, LIMIT + 1):
        osc = explicit_oscillation(n, ZETA_ZEROS, 25)
        is_prime = n in primes
        oscillations.append((osc, n, is_prime))

    # Analysis 1: Does oscillation peak at primes?
    print("=" * 65)
    print("ANALYSIS 1: Oscillation at Primes vs Composites")
    print("=" * 65)

    prime_osc = [o for o, n, is_p in oscillations if is_p]
    comp_osc = [o for o, n, is_p in oscillations if not is_p]

    p_mean = sum(prime_osc) / len(prime_osc)
    p_std = math.sqrt(sum((o - p_mean)**2 for o in prime_osc) / len(prime_osc))

    c_mean = sum(comp_osc) / len(comp_osc)
    c_std = math.sqrt(sum((o - c_mean)**2 for o in comp_osc) / len(comp_osc))

    print(f"\nPrimes:     mean={p_mean:+.2f}, std={p_std:.2f}")
    print(f"Composites: mean={c_mean:+.2f}, std={c_std:.2f}")

    # Analysis 2: Local maxima of oscillation
    print("\n" + "=" * 65)
    print("ANALYSIS 2: Local Maxima of Oscillation")
    print("=" * 65)
    print("Where does the explicit formula oscillation peak?")

    local_maxima = []
    for i in range(1, len(oscillations) - 1):
        o_prev = oscillations[i-1][0]
        o_curr = oscillations[i][0]
        o_next = oscillations[i+1][0]

        if o_curr > o_prev and o_curr > o_next:
            local_maxima.append(oscillations[i])

    print(f"\nFound {len(local_maxima)} local maxima")

    prime_maxima = sum(1 for _, n, is_p in local_maxima if is_p)
    total_maxima = len(local_maxima)
    expected = total_maxima * len(primes) / LIMIT

    print(f"Primes at local maxima: {prime_maxima}/{total_maxima} ({100*prime_maxima/total_maxima:.1f}%)")
    print(f"Expected by chance: {expected:.1f} ({100*expected/total_maxima:.1f}%)")

    print("\nTop 20 local maxima:")
    sorted_maxima = sorted(local_maxima, reverse=True)[:20]
    print(f"{'Rank':<6}{'n':<8}{'Oscillation':<14}{'Prime?':<8}")
    print("-" * 36)
    for rank, (osc, n, is_p) in enumerate(sorted_maxima, 1):
        marker = "YES" if is_p else ""
        print(f"{rank:<6}{n:<8}{osc:<14.2f}{marker:<8}")

    # Analysis 3: Derivative / rate of change
    print("\n" + "=" * 65)
    print("ANALYSIS 3: Oscillation Derivative")
    print("=" * 65)
    print("Rate of change of oscillation - primes as 'jumps'?")

    derivatives = []
    for i in range(len(oscillations) - 1):
        o1, n1, _ = oscillations[i]
        o2, n2, is_p2 = oscillations[i + 1]
        deriv = o2 - o1
        derivatives.append((deriv, n2, is_p2))

    # Large positive derivatives
    sorted_derivs = sorted(derivatives, reverse=True)

    print("\nLargest positive jumps in oscillation:")
    print(f"{'Rank':<6}{'n':<8}{'Δ Osc':<14}{'Prime?':<8}")
    print("-" * 36)
    jump_primes = 0
    for rank, (deriv, n, is_p) in enumerate(sorted_derivs[:20], 1):
        marker = "YES" if is_p else ""
        if is_p:
            jump_primes += 1
        print(f"{rank:<6}{n:<8}{deriv:<+14.2f}{marker:<8}")

    print(f"\nPrimes in top 20 jumps: {jump_primes}/20")

    # Analysis 4: Oscillation at consecutive primes
    print("\n" + "=" * 65)
    print("ANALYSIS 4: Oscillation Pattern at Consecutive Primes")
    print("=" * 65)

    print(f"\n{'p':<6}{'Osc(p)':<12}{'Osc(p+1)':<12}{'Osc(p+2)':<12}{'Gap':<6}")
    print("-" * 48)

    for i in range(min(20, len(prime_list) - 1)):
        p = prime_list[i]
        gap = prime_list[i+1] - p if i < len(prime_list) - 1 else 0
        osc_p = explicit_oscillation(p, ZETA_ZEROS, 25)
        osc_p1 = explicit_oscillation(p + 1, ZETA_ZEROS, 25)
        osc_p2 = explicit_oscillation(p + 2, ZETA_ZEROS, 25)
        print(f"{p:<6}{osc_p:<+12.2f}{osc_p1:<+12.2f}{osc_p2:<+12.2f}{gap:<6}")

    # Analysis 5: 3D neighborhood effect
    print("\n" + "=" * 65)
    print("ANALYSIS 5: 3D Neighborhood Smoothing")
    print("=" * 65)
    print("Does smoothing over golden-spiral neighbors reveal structure?")

    smoothed = []
    for n in range(10, LIMIT - 10):
        sm = neighborhood_oscillation(n, radius_indices=3)
        is_prime = n in primes
        smoothed.append((sm, n, is_prime))

    # Extremes of smoothed
    sorted_smooth = sorted(smoothed)

    print("\nLowest smoothed oscillation (3D neighborhood):")
    prime_count = 0
    for sm, n, is_p in sorted_smooth[:15]:
        marker = "YES" if is_p else ""
        if is_p:
            prime_count += 1
        print(f"  n={n}: {sm:+.2f} {marker}")
    print(f"Primes: {prime_count}/15")

    print("\nHighest smoothed oscillation:")
    prime_count = 0
    for sm, n, is_p in sorted_smooth[-15:][::-1]:
        marker = "YES" if is_p else ""
        if is_p:
            prime_count += 1
        print(f"  n={n}: {sm:+.2f} {marker}")
    print(f"Primes: {prime_count}/15")

    # Synthesis
    print("\n" + "=" * 65)
    print("SYNTHESIS")
    print("=" * 65)
    print(f"""
The explicit formula oscillation encodes prime information:

1. Primes vs Composites:
   - Mean oscillation: primes={p_mean:+.2f}, composites={c_mean:+.2f}

2. Local maxima:
   - {prime_maxima}/{total_maxima} maxima at primes ({100*prime_maxima/total_maxima:.0f}%)
   - Expected: {expected:.0f} ({100*expected/total_maxima:.0f}%)

3. Jump analysis:
   - {jump_primes}/20 largest jumps occur at primes

KEY INSIGHT:
The explicit formula oscillation IS the prime-counting correction.
By definition, it encodes primes. The question is whether the
3D golden-spiral projection reveals ADDITIONAL structure.

The neighborhood smoothing tests whether primes cluster in
certain 3D regions - beyond what 1D position would predict.

WHAT WE'RE REALLY TESTING:
Does golden_spiral(prime) cluster differently than golden_spiral(composite)?
This would mean the 3D projection "knows" about primality through
the combination of golden ratio and spherical geometry.
""")

if __name__ == "__main__":
    analyze_explicit_3d()
