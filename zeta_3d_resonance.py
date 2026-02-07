#!/usr/bin/env python3
"""
Zeta Zeros + 3D Prime Projection = Standing Wave Resonance

CTA Chain:
  P(zeta_zeros) ⊗ T_spec ⊗ P(3D_golden_spiral) ⊗ T_interference → ???

Like Chladni figures: vibrate a surface at specific frequencies,
sand settles at nodes. Here we "vibrate" the golden-ratio icosahedron
at zeta-zero frequencies and see where primes "settle".
"""

import math

PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
GOLDEN_ANGLE = 2 * math.pi / (PHI * PHI)  # ~137.5 degrees

# First 30 zeta zeros
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

def golden_spiral_sphere(n, total=1000):
    """
    Map integer n to point on unit sphere using Fibonacci/golden spiral.
    Same mapping as the 3D prime visualizer.
    """
    if n <= 0:
        return (0, 0, 1)

    # Golden angle increment
    theta = GOLDEN_ANGLE * n

    # Distribute points evenly in z (cosine of polar angle)
    z = 1 - (2 * n) / total
    z = max(-1, min(1, z))  # Clamp to [-1, 1]

    # Convert to spherical
    r_xy = math.sqrt(1 - z*z)
    x = r_xy * math.cos(theta)
    y = r_xy * math.sin(theta)

    return (x, y, z)

def icosahedron_vertices():
    """Return the 12 vertices of a regular icosahedron."""
    # Golden ratio coordinates
    vertices = []
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            vertices.append((0, s1, s2 * PHI))
            vertices.append((s1, s2 * PHI, 0))
            vertices.append((s2 * PHI, 0, s1))

    # Normalize to unit sphere
    normalized = []
    for v in vertices:
        mag = math.sqrt(sum(c*c for c in v))
        normalized.append(tuple(c/mag for c in v))

    return normalized

def nearest_icosa_vertex(point, vertices):
    """Find which icosahedron vertex is nearest to point."""
    best_dist = float('inf')
    best_idx = 0
    for i, v in enumerate(vertices):
        dist = sum((a-b)**2 for a, b in zip(point, v))
        if dist < best_dist:
            best_dist = dist
            best_idx = i
    return best_idx, math.sqrt(best_dist)

def zeta_standing_wave(point, zeros, num_zeros=20, t=0):
    """
    Calculate standing wave amplitude at a 3D point.
    Each zeta zero contributes a spherical harmonic-like oscillation.

    The amplitude depends on the point's position and the zero's "frequency".
    """
    x, y, z = point

    # Spherical coordinates
    r = math.sqrt(x*x + y*y + z*z)
    if r < 0.001:
        r = 0.001
    theta = math.atan2(y, x)  # Azimuthal angle
    phi = math.acos(z / r)    # Polar angle

    total = 0
    for gamma in zeros[:num_zeros]:
        # Each zero creates a standing wave pattern
        # Simplified: use gamma to set angular frequency
        # Real spherical harmonics would be more complex

        # Wave pattern: combines radial and angular parts
        angular = math.sin(gamma * theta / 10) * math.sin(gamma * phi / 10)
        radial = math.cos(gamma * r + t)

        amplitude = 1.0 / math.sqrt(gamma)  # Higher zeros contribute less
        total += amplitude * angular * radial

    return total

def zeta_resonance_at_integer(n, zeros, num_zeros=20):
    """
    Calculate total zeta resonance at the 3D position of integer n.
    """
    point = golden_spiral_sphere(n, 1000)
    return zeta_standing_wave(point, zeros, num_zeros)

def analyze_prime_resonance():
    """Main analysis: do primes sit at special resonance points?"""

    print("=" * 65)
    print("ZETA ZEROS + 3D GOLDEN SPIRAL PROJECTION")
    print("Standing wave resonance analysis")
    print("=" * 65)
    print()
    print("CTA: P(zeta_zeros) ⊗ T_wave ⊗ P(golden_3D) → resonance pattern")
    print()

    LIMIT = 500
    primes = set(sieve_primes(LIMIT))
    icosa_verts = icosahedron_vertices()

    print(f"Analyzing integers 1 to {LIMIT}")
    print(f"Primes in range: {len(primes)}")
    print(f"Using {20} zeta zeros as frequencies")
    print()

    # Calculate resonance for all integers
    resonances = []
    for n in range(1, LIMIT + 1):
        res = zeta_resonance_at_integer(n, ZETA_ZEROS, 20)
        is_prime = n in primes
        resonances.append((res, n, is_prime))

    # Analysis 1: Compare prime vs composite resonance
    print("=" * 65)
    print("ANALYSIS 1: Prime vs Composite Resonance Distribution")
    print("=" * 65)

    prime_res = [r for r, n, is_p in resonances if is_p]
    composite_res = [r for r, n, is_p in resonances if not is_p and n > 1]

    prime_mean = sum(prime_res) / len(prime_res)
    prime_std = math.sqrt(sum((r - prime_mean)**2 for r in prime_res) / len(prime_res))

    comp_mean = sum(composite_res) / len(composite_res)
    comp_std = math.sqrt(sum((r - comp_mean)**2 for r in composite_res) / len(composite_res))

    print(f"\nPrimes:     mean={prime_mean:+.4f}, std={prime_std:.4f}, n={len(prime_res)}")
    print(f"Composites: mean={comp_mean:+.4f}, std={comp_std:.4f}, n={len(composite_res)}")
    print(f"Difference: {abs(prime_mean - comp_mean):.4f}")

    # Statistical test: are they different?
    pooled_std = math.sqrt((prime_std**2 + comp_std**2) / 2)
    effect_size = abs(prime_mean - comp_mean) / pooled_std if pooled_std > 0 else 0
    print(f"Effect size (Cohen's d): {effect_size:.3f}")

    # Analysis 2: Extremal resonance points
    print("\n" + "=" * 65)
    print("ANALYSIS 2: Extremal Resonance Points")
    print("=" * 65)

    sorted_res = sorted(resonances, key=lambda x: x[0])

    print("\nLowest resonance (nodes - destructive interference):")
    print(f"{'Rank':<6}{'n':<8}{'Resonance':<14}{'Prime?':<8}")
    print("-" * 36)
    prime_count_low = 0
    for i, (res, n, is_p) in enumerate(sorted_res[:20]):
        marker = "YES" if is_p else ""
        if is_p:
            prime_count_low += 1
        print(f"{i+1:<6}{n:<8}{res:<14.4f}{marker:<8}")
    print(f"Primes in bottom 20: {prime_count_low}/20 ({100*prime_count_low/20:.0f}%)")

    print("\nHighest resonance (antinodes - constructive interference):")
    print(f"{'Rank':<6}{'n':<8}{'Resonance':<14}{'Prime?':<8}")
    print("-" * 36)
    prime_count_high = 0
    for i, (res, n, is_p) in enumerate(sorted_res[-20:][::-1]):
        marker = "YES" if is_p else ""
        if is_p:
            prime_count_high += 1
        print(f"{i+1:<6}{n:<8}{res:<14.4f}{marker:<8}")
    print(f"Primes in top 20: {prime_count_high}/20 ({100*prime_count_high/20:.0f}%)")

    # Expected by chance
    expected = 20 * len(primes) / LIMIT
    print(f"\nExpected primes by chance: {expected:.1f}/20")

    # Analysis 3: Icosahedral face distribution
    print("\n" + "=" * 65)
    print("ANALYSIS 3: Icosahedral Vertex Clustering")
    print("=" * 65)
    print("Which icosahedron vertices do primes cluster near?")

    vertex_counts_prime = [0] * 12
    vertex_counts_all = [0] * 12
    vertex_resonance = [[] for _ in range(12)]

    for n in range(1, LIMIT + 1):
        point = golden_spiral_sphere(n, LIMIT)
        vert_idx, dist = nearest_icosa_vertex(point, icosa_verts)
        vertex_counts_all[vert_idx] += 1

        if n in primes:
            vertex_counts_prime[vert_idx] += 1
            res = zeta_resonance_at_integer(n, ZETA_ZEROS, 20)
            vertex_resonance[vert_idx].append(res)

    print(f"\n{'Vertex':<8}{'All #':<10}{'Prime #':<10}{'Prime %':<10}{'Mean Res':<12}")
    print("-" * 50)
    for i in range(12):
        all_c = vertex_counts_all[i]
        prime_c = vertex_counts_prime[i]
        pct = 100 * prime_c / all_c if all_c > 0 else 0
        mean_res = sum(vertex_resonance[i]) / len(vertex_resonance[i]) if vertex_resonance[i] else 0
        print(f"{i:<8}{all_c:<10}{prime_c:<10}{pct:<10.1f}{mean_res:<12.4f}")

    # Analysis 4: Resonance vs prime gap
    print("\n" + "=" * 65)
    print("ANALYSIS 4: Resonance Predicting Prime Gaps?")
    print("=" * 65)

    prime_list = sorted(primes)
    gaps_and_res = []
    for i in range(len(prime_list) - 1):
        p = prime_list[i]
        gap = prime_list[i+1] - p
        res = zeta_resonance_at_integer(p, ZETA_ZEROS, 20)
        gaps_and_res.append((gap, res, p))

    # Correlation between resonance and following gap
    mean_gap = sum(g for g, r, p in gaps_and_res) / len(gaps_and_res)
    mean_res = sum(r for g, r, p in gaps_and_res) / len(gaps_and_res)

    cov = sum((g - mean_gap) * (r - mean_res) for g, r, p in gaps_and_res) / len(gaps_and_res)
    std_gap = math.sqrt(sum((g - mean_gap)**2 for g, r, p in gaps_and_res) / len(gaps_and_res))
    std_res = math.sqrt(sum((r - mean_res)**2 for g, r, p in gaps_and_res) / len(gaps_and_res))

    correlation = cov / (std_gap * std_res) if std_gap > 0 and std_res > 0 else 0

    print(f"\nCorrelation between prime's resonance and following gap: {correlation:.4f}")

    # Group by gap size
    print("\nMean resonance by gap size:")
    gap_groups = {}
    for gap, res, p in gaps_and_res:
        if gap not in gap_groups:
            gap_groups[gap] = []
        gap_groups[gap].append(res)

    print(f"{'Gap':<8}{'Count':<8}{'Mean Res':<12}{'Std Res':<12}")
    print("-" * 40)
    for gap in sorted(gap_groups.keys())[:10]:
        vals = gap_groups[gap]
        mean = sum(vals) / len(vals)
        std = math.sqrt(sum((v - mean)**2 for v in vals) / len(vals)) if len(vals) > 1 else 0
        print(f"{gap:<8}{len(vals):<8}{mean:<12.4f}{std:<12.4f}")

    # Analysis 5: Phase relationship
    print("\n" + "=" * 65)
    print("ANALYSIS 5: Resonance Phase Patterns")
    print("=" * 65)

    # Look at consecutive primes - do their resonances have phase relationship?
    print("\nConsecutive prime resonance patterns:")
    print(f"{'p1':<6}{'p2':<6}{'Gap':<6}{'Res1':<12}{'Res2':<12}{'Δ Res':<12}")
    print("-" * 54)

    for i in range(min(15, len(prime_list) - 1)):
        p1, p2 = prime_list[i], prime_list[i+1]
        gap = p2 - p1
        res1 = zeta_resonance_at_integer(p1, ZETA_ZEROS, 20)
        res2 = zeta_resonance_at_integer(p2, ZETA_ZEROS, 20)
        delta = res2 - res1
        print(f"{p1:<6}{p2:<6}{gap:<6}{res1:<12.4f}{res2:<12.4f}{delta:<+12.4f}")

    # Twin prime resonance
    print("\n--- Twin Prime Resonance ---")
    twins = [(p, p+2) for p in prime_list if p+2 in primes]
    print(f"Twin pairs found: {len(twins)}")

    twin_res_diffs = []
    for p1, p2 in twins[:10]:
        res1 = zeta_resonance_at_integer(p1, ZETA_ZEROS, 20)
        res2 = zeta_resonance_at_integer(p2, ZETA_ZEROS, 20)
        diff = abs(res2 - res1)
        twin_res_diffs.append(diff)
        print(f"  ({p1}, {p2}): res1={res1:+.4f}, res2={res2:+.4f}, |Δ|={diff:.4f}")

    if twin_res_diffs:
        print(f"Mean |Δ| for twins: {sum(twin_res_diffs)/len(twin_res_diffs):.4f}")

    # Synthesis
    print("\n" + "=" * 65)
    print("SYNTHESIS")
    print("=" * 65)
    print(f"""
COMBINING ZETA ZEROS + 3D GOLDEN PROJECTION:

1. Primes vs Composites:
   - Mean resonance difference: {abs(prime_mean - comp_mean):.4f}
   - Effect size: {effect_size:.3f} {'(small)' if effect_size < 0.2 else '(medium)' if effect_size < 0.8 else '(large)'}

2. Extremal points:
   - Primes in lowest-resonance 20: {prime_count_low}/20 (expected ~{expected:.0f})
   - Primes in highest-resonance 20: {prime_count_high}/20 (expected ~{expected:.0f})

3. Resonance-gap correlation: {correlation:.4f}

INTERPRETATION:
""")

    if abs(correlation) > 0.1:
        print("   → Resonance has weak predictive signal for prime gaps")
    else:
        print("   → No strong correlation between resonance and gaps")

    if effect_size > 0.2:
        print("   → Primes occupy measurably different resonance positions")
    else:
        print("   → Primes and composites have similar resonance distribution")

    print("""
The 3D projection + zeta waves creates a "resonance landscape".
The question: do primes sit at special points in this landscape?

This is exploratory - the specific wave model is simplified.
A more sophisticated version would use actual spherical harmonics
weighted by zeta zeros, or the explicit formula contribution directly.

NEXT DIRECTIONS:
1. Try different wave equations (actual spherical harmonics)
2. Vary the number of zeros used
3. Animate through time parameter
4. Look at local neighborhoods, not just point values
""")

if __name__ == "__main__":
    analyze_prime_resonance()
