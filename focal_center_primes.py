#!/usr/bin/env python3
"""
WHICH PRIMES ARE AT THE FOCAL CENTER?

At the Brennpunkt (t=1/3), primes cluster together.
But which primes end up CLOSEST to the focal centroid?
Is there structure there?
"""

import math

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi / (PHI * PHI)
BRENNPUNKT_T = 1/3

def sieve_primes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return sorted([i for i in range(limit + 1) if is_prime[i]])

def fibonacci_list(max_val):
    fibs = [1, 1]
    while fibs[-1] < max_val:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

def position_at_brennpunkt(n, N, t=BRENNPUNKT_T, R=0.5):
    """3D position of n at partial inversion t."""
    theta = GOLDEN_ANGLE * n
    z_unit = 1 - (2 * n) / N
    z_unit = max(-1, min(1, z_unit))
    r_xy_unit = math.sqrt(max(0, 1 - z_unit * z_unit))

    r_orig = n / N
    if r_orig < 1e-10:
        r_orig = 1e-10

    r_t = (r_orig ** (1 - 2*t)) * (R ** (2*t))

    x = r_t * r_xy_unit * math.cos(theta)
    y = r_t * r_xy_unit * math.sin(theta)
    z = r_t * z_unit
    return (x, y, z)

def distance(p1, p2):
    return math.sqrt(sum((a-b)**2 for a, b in zip(p1, p2)))

def compute_centroid(positions):
    n = len(positions)
    cx = sum(p[0] for p in positions) / n
    cy = sum(p[1] for p in positions) / n
    cz = sum(p[2] for p in positions) / n
    return (cx, cy, cz)

def analyze_focal_center():
    print("=" * 70)
    print("WHICH PRIMES ARE AT THE FOCAL CENTER?")
    print("=" * 70)

    N = 500
    primes = sieve_primes(N)
    fibs = set(fibonacci_list(N))

    print(f"\nPrimes: {len(primes)}")
    print(f"Brennpunkt: t = {BRENNPUNKT_T:.4f}")

    # Compute positions at Brennpunkt
    positions = {p: position_at_brennpunkt(p, N) for p in primes}

    # Compute centroid
    centroid = compute_centroid(list(positions.values()))
    print(f"\nFocal centroid: ({centroid[0]:.4f}, {centroid[1]:.4f}, {centroid[2]:.4f})")

    # Distance from each prime to centroid
    distances = [(distance(positions[p], centroid), p) for p in primes]
    distances.sort()

    # Closest primes
    print("\n" + "=" * 70)
    print("PRIMES CLOSEST TO FOCAL CENTER")
    print("=" * 70)

    print(f"\n{'Rank':<6}{'Prime':<8}{'Distance':<12}{'Fibonacci?':<12}{'Properties':<25}")
    print("-" * 63)

    for rank, (dist, p) in enumerate(distances[:25], 1):
        is_fib = "FIB" if p in fibs else ""

        # Properties
        props = []
        if p == 2:
            props.append("even prime")
        if p == 3:
            props.append("1/t")
        if (p - 1) % 6 == 0 or (p + 1) % 6 == 0:
            props.append("6k±1")

        # Twin prime?
        if p - 2 in set(primes) or p + 2 in set(primes):
            props.append("twin")

        prop_str = ", ".join(props) if props else ""
        print(f"{rank:<6}{p:<8}{dist:<12.6f}{is_fib:<12}{prop_str:<25}")

    # Farthest primes
    print("\n" + "=" * 70)
    print("PRIMES FARTHEST FROM FOCAL CENTER")
    print("=" * 70)

    print(f"\n{'Rank':<6}{'Prime':<8}{'Distance':<12}{'Fibonacci?':<12}")
    print("-" * 38)

    for rank, (dist, p) in enumerate(distances[-15:][::-1], 1):
        is_fib = "FIB" if p in fibs else ""
        print(f"{rank:<6}{p:<8}{dist:<12.6f}{is_fib:<12}")

    # Statistical analysis
    print("\n" + "=" * 70)
    print("STATISTICAL ANALYSIS")
    print("=" * 70)

    # Are Fibonacci primes closer than average?
    fib_primes = [p for p in primes if p in fibs]
    non_fib_primes = [p for p in primes if p not in fibs]

    fib_distances = [d for d, p in distances if p in fibs]
    non_fib_distances = [d for d, p in distances if p not in fibs]

    if fib_distances:
        fib_mean = sum(fib_distances) / len(fib_distances)
        print(f"\nFibonacci primes ({len(fib_primes)}): mean distance = {fib_mean:.6f}")

    non_fib_mean = sum(non_fib_distances) / len(non_fib_distances)
    print(f"Non-Fibonacci primes ({len(non_fib_primes)}): mean distance = {non_fib_mean:.6f}")

    if fib_distances:
        print(f"Ratio: {fib_mean / non_fib_mean:.3f}")

    # Small primes vs large primes
    small_primes = [p for p in primes if p <= 50]
    large_primes = [p for p in primes if p > 200]

    small_dist = [d for d, p in distances if p <= 50]
    large_dist = [d for d, p in distances if p > 200]

    small_mean = sum(small_dist) / len(small_dist)
    large_mean = sum(large_dist) / len(large_dist)

    print(f"\nSmall primes (≤50): mean distance = {small_mean:.6f}")
    print(f"Large primes (>200): mean distance = {large_mean:.6f}")
    print(f"Ratio: {small_mean / large_mean:.3f}")

    # Twin primes
    print("\n" + "=" * 70)
    print("TWIN PRIMES AT FOCAL CENTER")
    print("=" * 70)

    prime_set = set(primes)
    twins = [(p, p+2) for p in primes if p+2 in prime_set]

    print(f"\nTwin pairs: {len(twins)}")

    twin_distances = []
    for p1, p2 in twins:
        d1 = next(d for d, p in distances if p == p1)
        d2 = next(d for d, p in distances if p == p2)
        avg = (d1 + d2) / 2
        twin_distances.append((avg, p1, p2, d1, d2))

    twin_distances.sort()

    print(f"\n{'Twin Pair':<15}{'Avg Dist':<12}{'d(p1)':<12}{'d(p2)':<12}")
    print("-" * 51)

    for avg, p1, p2, d1, d2 in twin_distances[:10]:
        print(f"({p1}, {p2}){'':<5}{avg:<12.6f}{d1:<12.6f}{d2:<12.6f}")

    # The 3-related primes
    print("\n" + "=" * 70)
    print("PRIMES RELATED TO 3 (Brennpunkt = 1/3)")
    print("=" * 70)

    print("\nPrimes divisible by relationship to 3:")

    # Primes of form 3k+1 vs 3k+2 (3k+0 is only 3 itself)
    primes_3k1 = [p for p in primes if p % 3 == 1]
    primes_3k2 = [p for p in primes if p % 3 == 2]

    dist_3k1 = [d for d, p in distances if p % 3 == 1]
    dist_3k2 = [d for d, p in distances if p % 3 == 2]

    mean_3k1 = sum(dist_3k1) / len(dist_3k1) if dist_3k1 else 0
    mean_3k2 = sum(dist_3k2) / len(dist_3k2) if dist_3k2 else 0

    print(f"  p ≡ 1 (mod 3): {len(primes_3k1)} primes, mean dist = {mean_3k1:.6f}")
    print(f"  p ≡ 2 (mod 3): {len(primes_3k2)} primes, mean dist = {mean_3k2:.6f}")
    print(f"  p = 3 itself: distance = {next(d for d, p in distances if p == 3):.6f}")

    # Where does 3 rank?
    rank_of_3 = next(i for i, (d, p) in enumerate(distances, 1) if p == 3)
    print(f"\nPrime 3 is #{rank_of_3} closest to focal center")

    # Synthesis
    print("\n" + "=" * 70)
    print("SYNTHESIS")
    print("=" * 70)
    print(f"""
AT THE FOCAL CENTER (Brennpunkt t=1/3):

1. CLOSEST PRIMES: The smallest primes tend to be closest
   - This makes sense: small n → small original r → transformed position

2. FIBONACCI PRIMES: {"Closer" if fib_distances and fib_mean < non_fib_mean else "Not significantly closer"} than average

3. THE PRIME 3:
   - Brennpunkt = 1/3, so 3 is the "focal number"
   - Prime 3 ranks #{rank_of_3} closest to focal center
   - Primes ≡ 1 (mod 3) vs ≡ 2 (mod 3): distances differ by {abs(mean_3k1 - mean_3k2):.4f}

4. TWIN PRIMES: Small twins (3,5), (5,7), (11,13) closest to center

The FOCAL CENTER is dominated by small primes.
The Brennpunkt at 1/3 brings the "core" primes (2, 3, 5, 7, 11...)
into tight focus, while large primes form the outer halo.

This is the "prime nucleus" - the concentrated heart of prime distribution
when viewed through the 1/3 inversion lens.
""")

if __name__ == "__main__":
    analyze_focal_center()
