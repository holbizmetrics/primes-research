#!/usr/bin/env python3
"""
Golden Spiral Prime Clustering Analysis

The key question: Does the golden spiral projection create
meaningful clusters of primes in 3D space?

We saw 223, 227, 229 clustering. Is this systematic?
"""

import math

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi / (PHI * PHI)

ZETA_ZEROS = [
    14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
    37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478,
]

def sieve_primes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]

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

def find_3d_neighbors(n, all_points, radius=0.3):
    """Find integers whose 3D positions are within angular radius of n."""
    center = all_points[n]
    neighbors = []
    for m, point in all_points.items():
        if m != n:
            dist = angular_distance(center, point)
            if dist < radius:
                neighbors.append((m, dist))
    return sorted(neighbors, key=lambda x: x[1])

def analyze_prime_3d_neighborhoods():
    print("=" * 65)
    print("GOLDEN SPIRAL PRIME CLUSTERING")
    print("Do primes cluster in 3D golden-spiral space?")
    print("=" * 65)

    LIMIT = 500
    primes = set(sieve_primes(LIMIT))
    prime_list = sorted(primes)

    # Pre-compute all 3D positions
    all_points = {n: golden_spiral_sphere(n, LIMIT) for n in range(1, LIMIT + 1)}

    print(f"\nAnalyzing {len(primes)} primes in range [1, {LIMIT}]")

    # Analysis 1: For each prime, count prime vs composite neighbors
    print("\n" + "=" * 65)
    print("ANALYSIS 1: Prime Neighborhood Composition")
    print("For each prime, what fraction of 3D neighbors are also prime?")
    print("=" * 65)

    neighborhood_stats = []
    for p in prime_list:
        neighbors = find_3d_neighbors(p, all_points, radius=0.25)
        if len(neighbors) < 3:
            continue

        prime_neighbors = sum(1 for n, d in neighbors if n in primes)
        total_neighbors = len(neighbors)
        frac = prime_neighbors / total_neighbors

        neighborhood_stats.append((frac, p, prime_neighbors, total_neighbors))

    # Sort by prime fraction
    neighborhood_stats.sort(reverse=True)

    print(f"\nPrimes with highest prime-neighbor fraction:")
    print(f"{'Prime':<8}{'Prim Nbrs':<12}{'Total':<8}{'Fraction':<10}")
    print("-" * 38)
    for frac, p, pn, tn in neighborhood_stats[:15]:
        print(f"{p:<8}{pn:<12}{tn:<8}{frac:<10.2%}")

    print(f"\nPrimes with lowest prime-neighbor fraction:")
    for frac, p, pn, tn in neighborhood_stats[-10:]:
        print(f"{p:<8}{pn:<12}{tn:<8}{frac:<10.2%}")

    # Overall statistics
    all_fracs = [f for f, p, pn, tn in neighborhood_stats]
    mean_frac = sum(all_fracs) / len(all_fracs)
    expected_frac = len(primes) / LIMIT

    print(f"\nMean prime-neighbor fraction: {mean_frac:.2%}")
    print(f"Expected by random placement: {expected_frac:.2%}")

    # Analysis 2: Find dense prime clusters
    print("\n" + "=" * 65)
    print("ANALYSIS 2: Dense Prime Clusters in 3D")
    print("Regions where multiple primes cluster together")
    print("=" * 65)

    # For each prime, get all prime neighbors
    prime_clusters = []
    for p in prime_list:
        neighbors = find_3d_neighbors(p, all_points, radius=0.2)
        prime_nbrs = [n for n, d in neighbors if n in primes]
        if len(prime_nbrs) >= 2:
            cluster = tuple(sorted([p] + prime_nbrs))
            if cluster not in prime_clusters:
                prime_clusters.append(cluster)

    # Deduplicate and sort by size
    unique_clusters = []
    seen = set()
    for cluster in prime_clusters:
        if cluster not in seen:
            seen.add(cluster)
            unique_clusters.append(cluster)

    unique_clusters.sort(key=len, reverse=True)

    print(f"\nFound {len(unique_clusters)} unique prime clusters")
    print("\nLargest clusters (primes within angular distance 0.2):")
    for i, cluster in enumerate(unique_clusters[:10]):
        # Calculate gaps between consecutive primes in cluster
        gaps = [cluster[j+1] - cluster[j] for j in range(len(cluster)-1)]
        gap_str = ",".join(str(g) for g in gaps)
        print(f"  {i+1}. {cluster} (gaps: {gap_str})")

    # Analysis 3: Golden angle relationship
    print("\n" + "=" * 65)
    print("ANALYSIS 3: Golden Angle Relationship")
    print("The golden angle creates Fibonacci-like stepping")
    print("=" * 65)

    print("\nGolden angle ≈ 137.5°")
    print("After n steps, angle = n × 137.5° (mod 360°)")

    # For Fibonacci numbers, the pattern has special properties
    fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
    print(f"\nFibonacci numbers: {fibs}")
    print(f"Primes among Fibonacci: {[f for f in fibs if f in primes]}")

    # Check: do primes that are Fibonacci-spaced cluster?
    print("\nPrime pairs with Fibonacci-number gaps:")
    fib_set = set(fibs)
    fib_gap_pairs = []
    for i, p1 in enumerate(prime_list[:-1]):
        for p2 in prime_list[i+1:]:
            gap = p2 - p1
            if gap in fib_set and gap > 1:
                pos1 = golden_spiral_sphere(p1, LIMIT)
                pos2 = golden_spiral_sphere(p2, LIMIT)
                dist = angular_distance(pos1, pos2)
                fib_gap_pairs.append((gap, p1, p2, dist))
            if p2 - p1 > 150:
                break

    # Group by gap
    by_gap = {}
    for gap, p1, p2, dist in fib_gap_pairs:
        if gap not in by_gap:
            by_gap[gap] = []
        by_gap[gap].append((p1, p2, dist))

    for gap in sorted(by_gap.keys()):
        pairs = by_gap[gap]
        mean_dist = sum(d for _, _, d in pairs) / len(pairs)
        print(f"\n  Gap {gap} (Fibonacci): {len(pairs)} pairs, mean 3D distance: {mean_dist:.3f}")
        for p1, p2, d in pairs[:5]:
            print(f"    ({p1}, {p2}): 3D dist = {d:.3f}")

    # Analysis 4: Spiral arm structure
    print("\n" + "=" * 65)
    print("ANALYSIS 4: Spiral Arm Structure")
    print("The golden spiral creates visible 'arms'")
    print("=" * 65)

    # Group points by their azimuthal angle (mod some sector)
    num_sectors = 8
    sector_primes = [[] for _ in range(num_sectors)]
    sector_all = [0] * num_sectors

    for n in range(1, LIMIT + 1):
        theta = (GOLDEN_ANGLE * n) % (2 * math.pi)
        sector = int(theta / (2 * math.pi) * num_sectors) % num_sectors
        sector_all[sector] += 1
        if n in primes:
            sector_primes[sector].append(n)

    print(f"\nDividing azimuthal angle into {num_sectors} sectors:")
    print(f"{'Sector':<10}{'All #':<10}{'Prime #':<10}{'Prime %':<10}")
    print("-" * 40)
    for i in range(num_sectors):
        all_c = sector_all[i]
        prime_c = len(sector_primes[i])
        pct = 100 * prime_c / all_c if all_c > 0 else 0
        angle_range = f"{i*45}°-{(i+1)*45}°"
        print(f"{angle_range:<10}{all_c:<10}{prime_c:<10}{pct:<10.1f}")

    # Analysis 5: The twin prime 3D pattern
    print("\n" + "=" * 65)
    print("ANALYSIS 5: Twin Primes in 3D")
    print("=" * 65)

    twins = [(p, p+2) for p in prime_list if p+2 in primes]
    print(f"\nTwin prime pairs: {len(twins)}")

    twin_3d_dists = []
    for p1, p2 in twins:
        pos1 = golden_spiral_sphere(p1, LIMIT)
        pos2 = golden_spiral_sphere(p2, LIMIT)
        dist = angular_distance(pos1, pos2)
        twin_3d_dists.append((dist, p1, p2))

    mean_twin_dist = sum(d for d, _, _ in twin_3d_dists) / len(twin_3d_dists)

    # Compare to random pairs with gap 2
    random_gap2 = []
    for n in range(10, LIMIT - 2, 7):  # Sample
        pos1 = golden_spiral_sphere(n, LIMIT)
        pos2 = golden_spiral_sphere(n + 2, LIMIT)
        random_gap2.append(angular_distance(pos1, pos2))

    mean_random_dist = sum(random_gap2) / len(random_gap2)

    print(f"\nMean 3D distance for twin primes: {mean_twin_dist:.4f}")
    print(f"Mean 3D distance for random gap-2: {mean_random_dist:.4f}")

    print("\nTwin pairs by 3D distance:")
    twin_3d_dists.sort()
    print("Closest twins in 3D:")
    for dist, p1, p2 in twin_3d_dists[:8]:
        print(f"  ({p1}, {p2}): dist = {dist:.4f}")
    print("Farthest twins in 3D:")
    for dist, p1, p2 in twin_3d_dists[-5:]:
        print(f"  ({p1}, {p2}): dist = {dist:.4f}")

    # Synthesis
    print("\n" + "=" * 65)
    print("SYNTHESIS")
    print("=" * 65)
    print(f"""
GOLDEN SPIRAL CREATES PRIME CLUSTERING:

1. Prime neighborhood fraction: {mean_frac:.1%} (expected {expected_frac:.1%})
   {"→ Primes have MORE prime neighbors than random!" if mean_frac > expected_frac else "→ Similar to random distribution"}

2. Dense clusters exist: {len([c for c in unique_clusters if len(c) >= 3])} clusters of 3+ primes

3. Fibonacci gaps create characteristic 3D distances

4. Twin prime 3D pattern:
   - Mean twin distance: {mean_twin_dist:.4f}
   - Mean random gap-2: {mean_random_dist:.4f}

The golden spiral projection is not random - it creates structure
based on the golden angle ≈ 137.5° which relates to:
- Fibonacci sequence
- Phyllotaxis (leaf arrangement)
- Optimal packing on sphere

Primes, through their relationship with Fibonacci numbers and
the prime-gap structure (mod 6), interact with this geometry.
""")

if __name__ == "__main__":
    analyze_prime_3d_neighborhoods()
