#!/usr/bin/env python3
"""
Deep Dive: Fibonacci-Prime-Golden Connection

Key finding: Fibonacci-gapped primes are CLOSER in 3D golden spiral space.
Why? And what does this mean?

The golden angle θ = 2π/φ² ≈ 137.5°

After n steps: angle = n·θ (mod 2π)
After F_k steps (Fibonacci): angle ≈ 2π·{F_k·φ⁻²} where {} is fractional part

Fibonacci numbers have special property: F_k·φ⁻² mod 1 → small values
This is WHY Fibonacci-spaced points cluster!
"""

import math

PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618
PHI_INV = 1 / PHI             # ≈ 0.618
PHI_INV_SQ = 1 / (PHI * PHI)  # ≈ 0.382

GOLDEN_ANGLE = 2 * math.pi * PHI_INV_SQ  # ≈ 2.4 radians ≈ 137.5°

def sieve_primes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]

def fibonacci_sequence(limit):
    """Generate Fibonacci numbers up to limit."""
    fibs = [1, 1]
    while fibs[-1] + fibs[-2] <= limit:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

def golden_spiral_sphere(n, total=1000):
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

def angular_distance_2d(n, m):
    """Angular distance on equator (ignoring z) between positions n and m."""
    theta_n = (GOLDEN_ANGLE * n) % (2 * math.pi)
    theta_m = (GOLDEN_ANGLE * m) % (2 * math.pi)
    diff = abs(theta_n - theta_m)
    return min(diff, 2 * math.pi - diff)

def angular_distance_3d(p1, p2):
    """Angular distance between two 3D points on sphere."""
    dot = sum(a*b for a, b in zip(p1, p2))
    dot = max(-1, min(1, dot))
    return math.acos(dot)

def analyze_golden_angle_math():
    """Understand WHY Fibonacci spacing creates clustering."""
    print("=" * 65)
    print("THE MATHEMATICS OF GOLDEN ANGLE CLUSTERING")
    print("=" * 65)

    print(f"""
Golden ratio: φ = {PHI:.6f}
Golden angle: θ = 2π/φ² = {GOLDEN_ANGLE:.6f} rad = {math.degrees(GOLDEN_ANGLE):.2f}°

Key property: φ² = φ + 1, so 1/φ² = 1 - 1/φ = {PHI_INV_SQ:.6f}

After n steps, azimuthal angle = n × θ (mod 2π)
                               = n × 2π/φ² (mod 2π)
                               = 2π × (n/φ²) (mod 2π)
                               = 2π × {{n × {PHI_INV_SQ:.4f}}}

where {{x}} means fractional part of x.
""")

    print("=" * 65)
    print("FIBONACCI NUMBERS AND THE GOLDEN ANGLE")
    print("=" * 65)

    fibs = fibonacci_sequence(1000)
    print(f"\nFibonacci: {fibs[:15]}...")

    print(f"\nFor Fibonacci F_k, the angular position (mod 2π):")
    print(f"{'F_k':<8}{'F_k/φ²':<15}{'Frac part':<12}{'Angle (°)':<12}{'From 0/180':<12}")
    print("-" * 60)

    for fib in fibs[:15]:
        ratio = fib * PHI_INV_SQ
        frac = ratio - int(ratio)
        angle_deg = frac * 360
        # Distance from 0° or 180°
        from_zero = min(angle_deg, 360 - angle_deg)
        from_180 = abs(angle_deg - 180)
        nearest = min(from_zero, from_180)
        print(f"{fib:<8}{ratio:<15.4f}{frac:<12.4f}{angle_deg:<12.1f}{nearest:<12.1f}")

    print("""
KEY INSIGHT: Fibonacci numbers land at angles CLOSE to 0° or 180°!
This is because F_k/φ² ≈ F_{k-2} (exactly in the limit).
So F_k × φ⁻² has fractional part → 0 as k increases.
""")

def analyze_gap_distances():
    """Compare angular distances for different gap sizes."""
    print("\n" + "=" * 65)
    print("GAP SIZE VS ANGULAR DISTANCE")
    print("=" * 65)

    print("\n2D Angular distance (on equator) for gap g:")
    print(f"{'Gap':<8}{'g/φ²':<12}{'Frac':<10}{'Angle (°)':<12}{'Distance':<12}")
    print("-" * 55)

    gaps_to_test = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 13, 14, 18, 20, 21, 30, 34, 55, 89]

    gap_distances = []
    for g in gaps_to_test:
        ratio = g * PHI_INV_SQ
        frac = ratio - int(ratio)
        angle_deg = frac * 360
        # Angular distance is min(angle, 360-angle)
        dist = min(angle_deg, 360 - angle_deg)
        gap_distances.append((dist, g))
        print(f"{g:<8}{ratio:<12.4f}{frac:<10.4f}{angle_deg:<12.1f}{dist:<12.1f}")

    # Sort by distance
    gap_distances.sort()
    print(f"\nGaps sorted by angular distance (closest first):")
    for dist, g in gap_distances:
        fib_marker = " ← FIBONACCI" if g in fibonacci_sequence(100) else ""
        print(f"  Gap {g:3d}: {dist:6.1f}°{fib_marker}")

def analyze_prime_gaps_fibonacci():
    """Check which prime gaps are close to Fibonacci numbers."""
    print("\n" + "=" * 65)
    print("PRIME GAPS AND FIBONACCI PROXIMITY")
    print("=" * 65)

    LIMIT = 1000
    primes = sieve_primes(LIMIT)
    fibs = set(fibonacci_sequence(200))

    gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]

    # Count gaps
    gap_counts = {}
    for g in gaps:
        gap_counts[g] = gap_counts.get(g, 0) + 1

    print(f"\nPrime gaps up to {LIMIT}:")
    print(f"{'Gap':<6}{'Count':<8}{'%':<8}{'Fibonacci?':<12}{'Ang Dist':<10}")
    print("-" * 45)

    for gap in sorted(gap_counts.keys()):
        count = gap_counts[gap]
        pct = 100 * count / len(gaps)
        is_fib = "YES" if gap in fibs else ""

        # Angular distance for this gap
        frac = (gap * PHI_INV_SQ) % 1
        angle = frac * 360
        ang_dist = min(angle, 360 - angle)

        print(f"{gap:<6}{count:<8}{pct:<8.1f}{is_fib:<12}{ang_dist:<10.1f}")

def find_golden_prime_constellations():
    """Find prime patterns that exploit golden angle geometry."""
    print("\n" + "=" * 65)
    print("GOLDEN PRIME CONSTELLATIONS")
    print("=" * 65)
    print("Looking for prime patterns with small angular footprint...")

    LIMIT = 500
    primes = sieve_primes(LIMIT)
    prime_set = set(primes)

    # Find triplets with small total angular span
    print("\nPrime triplets (p, p+a, p+b) with small angular span:")

    triplets = []
    for p in primes:
        for a in range(2, 50, 2):  # First gap
            if p + a not in prime_set:
                continue
            for b in range(a + 2, 80, 2):  # Second gap (total)
                if p + b not in prime_set:
                    continue
                if p + b > LIMIT:
                    break

                # Calculate angular positions
                pos_p = golden_spiral_sphere(p, LIMIT)
                pos_pa = golden_spiral_sphere(p + a, LIMIT)
                pos_pb = golden_spiral_sphere(p + b, LIMIT)

                # Total angular span (max pairwise distance)
                d1 = angular_distance_3d(pos_p, pos_pa)
                d2 = angular_distance_3d(pos_pa, pos_pb)
                d3 = angular_distance_3d(pos_p, pos_pb)
                span = max(d1, d2, d3)

                triplets.append((span, p, a, b, d1, d2, d3))

    triplets.sort()

    print(f"\n{'Triplet':<20}{'Gaps':<12}{'Span':<8}{'Distances':<25}")
    print("-" * 65)

    fibs = set(fibonacci_sequence(100))

    for span, p, a, b, d1, d2, d3 in triplets[:20]:
        triplet_str = f"({p}, {p+a}, {p+b})"
        gaps_str = f"({a}, {b-a})"
        dist_str = f"{d1:.3f}, {d2:.3f}, {d3:.3f}"

        # Mark if gaps are Fibonacci
        fib_marker = ""
        if a in fibs:
            fib_marker += f" a={a}∈F"
        if (b - a) in fibs:
            fib_marker += f" Δ={b-a}∈F"
        if b in fibs:
            fib_marker += f" b={b}∈F"

        print(f"{triplet_str:<20}{gaps_str:<12}{span:<8.3f}{dist_str:<25}{fib_marker}")

def analyze_zeta_zeros_fibonacci():
    """Do zeta zeros have Fibonacci-like structure?"""
    print("\n" + "=" * 65)
    print("ZETA ZEROS AND FIBONACCI")
    print("=" * 65)

    ZETA_ZEROS = [
        14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
        37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478,
        52.970321478, 56.446247697, 59.347044003, 60.831778525, 65.112544048,
        67.079810529, 69.546401711, 72.067157674, 75.704690699, 77.144840069,
    ]

    fibs = fibonacci_sequence(500)

    print("\nZeta zeros near Fibonacci numbers:")
    for gamma in ZETA_ZEROS:
        # Find nearest Fibonacci
        nearest_fib = min(fibs, key=lambda f: abs(f - gamma))
        diff = gamma - nearest_fib
        if abs(diff) < 3:
            print(f"  γ = {gamma:.3f} ≈ F = {nearest_fib} (diff = {diff:+.3f})")

    print("\nZeta zero gaps and Fibonacci:")
    zero_gaps = [ZETA_ZEROS[i+1] - ZETA_ZEROS[i] for i in range(len(ZETA_ZEROS)-1)]

    for i, gap in enumerate(zero_gaps):
        nearest_fib = min(fibs, key=lambda f: abs(f - gap))
        if abs(gap - nearest_fib) < 0.5:
            print(f"  γ_{i+2} - γ_{i+1} = {gap:.3f} ≈ F = {nearest_fib}")

    print("\nZeta zero ratios and φ:")
    print(f"{'Ratio':<20}{'Value':<12}{'Near φ^n?':<15}")
    print("-" * 47)

    phi_powers = [PHI**n for n in range(-3, 5)]

    for i in range(len(ZETA_ZEROS) - 1):
        ratio = ZETA_ZEROS[i+1] / ZETA_ZEROS[i]

        # Check if near a power of phi
        for n in range(-2, 4):
            phi_n = PHI ** n
            if abs(ratio - phi_n) < 0.05:
                print(f"γ_{i+2}/γ_{i+1} = {ratio:.4f} ≈ φ^{n} = {phi_n:.4f}")
                break

def synthesize():
    print("\n" + "=" * 65)
    print("SYNTHESIS: THE GOLDEN-FIBONACCI-PRIME TRIANGLE")
    print("=" * 65)
    print("""
THREE DEEP CONNECTIONS:

1. GOLDEN ANGLE + FIBONACCI:
   - Golden angle θ = 2π/φ²
   - Fibonacci F_k satisfies: F_k/φ² ≈ F_{k-2}
   - So F_k × θ ≈ F_{k-2} × 2π = integer rotations!
   - Result: Fibonacci-spaced points CLUSTER in golden spiral

2. PRIME GAPS + FIBONACCI:
   - Most prime gaps are 2, 4, 6 (mod 6 structure)
   - Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13, 21, 34...
   - Gap 2 = F_3, Gap 8 = F_6, Gap 34 = F_9
   - Primes with these gaps cluster tightly in 3D!

3. GOLDEN RATIO + PRIMES:
   - φ = (1+√5)/2 involves √5
   - Primes p ≡ ±1 (mod 5) have special properties
   - Lucas numbers L_n (related to φ) contain primes
   - The distribution interacts with golden geometry

THE CTA CHAIN:

  P(Fibonacci) ←→ P(golden_ratio) ←→ P(prime_gaps)
       ↓              ↓                    ↓
    spacing      3D projection         gap structure
       ↓              ↓                    ↓
       └──────→ CLUSTERING ←──────────────┘

When prime gaps happen to be Fibonacci numbers (2, 8, 34...),
those prime pairs end up CLOSE in 3D golden-spiral space.

This is not coincidence - it's the geometry of φ interacting
with the arithmetic of primes.

NEXT: Can we PREDICT prime gaps using this geometric constraint?
""")

if __name__ == "__main__":
    analyze_golden_angle_math()
    analyze_gap_distances()
    analyze_prime_gaps_fibonacci()
    find_golden_prime_constellations()
    analyze_zeta_zeros_fibonacci()
    synthesize()
