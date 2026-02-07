#!/usr/bin/env python3
"""
Prime Focal Point: Partial Inversion

"Is there a limit of partial inside-out inversion where all primes meet?"

Parameterized inversion: t ∈ [0, 1]
  t=0: original geometry
  t=1: fully inverted
  t=?: focal point where primes cluster tightest

Like finding the focal length of a lens made of primes.
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
    return set(i for i in range(limit + 1) if is_prime[i])

def original_position(n, N):
    """Original 3D position: golden spiral, radius = n/N."""
    theta = GOLDEN_ANGLE * n
    z_unit = 1 - (2 * n) / N
    z_unit = max(-1, min(1, z_unit))
    r_xy = math.sqrt(max(0, 1 - z_unit * z_unit))

    r = n / N
    x = r * r_xy * math.cos(theta)
    y = r * r_xy * math.sin(theta)
    z = r * z_unit
    return (x, y, z)

def inverted_position(point, R=1.0):
    """Full inversion through sphere of radius R."""
    x, y, z = point
    r_sq = x*x + y*y + z*z
    if r_sq < 1e-10:
        return (1e10, 1e10, 1e10)
    scale = R * R / r_sq
    return (x * scale, y * scale, z * scale)

def partial_inversion(original, inverted, t):
    """
    Interpolate between original (t=0) and inverted (t=1).

    Linear interpolation in position space.
    """
    return tuple(
        (1 - t) * o + t * i
        for o, i in zip(original, inverted)
    )

def partial_inversion_log(n, N, t, R=1.0):
    """
    Logarithmic interpolation of radius:
    r(t) = r_orig^(1-t) * r_inv^t

    This is smoother for inversion since r_inv = R²/r_orig.
    """
    theta = GOLDEN_ANGLE * n
    z_unit = 1 - (2 * n) / N
    z_unit = max(-1, min(1, z_unit))
    r_xy_unit = math.sqrt(max(0, 1 - z_unit * z_unit))

    r_orig = n / N
    if r_orig < 1e-10:
        r_orig = 1e-10
    r_inv = R * R / r_orig

    # Log interpolation: r(t) = r_orig^(1-t) * r_inv^t
    # = r_orig^(1-t) * (R²/r_orig)^t
    # = r_orig^(1-2t) * R^(2t)
    r_t = (r_orig ** (1 - 2*t)) * (R ** (2*t))

    x = r_t * r_xy_unit * math.cos(theta)
    y = r_t * r_xy_unit * math.sin(theta)
    z = r_t * z_unit
    return (x, y, z)

def distance(p1, p2):
    return math.sqrt(sum((a-b)**2 for a, b in zip(p1, p2)))

def compute_spread(positions):
    """Compute spread (standard deviation from centroid) of positions."""
    n = len(positions)
    if n == 0:
        return 0, (0, 0, 0)

    # Centroid
    cx = sum(p[0] for p in positions) / n
    cy = sum(p[1] for p in positions) / n
    cz = sum(p[2] for p in positions) / n
    centroid = (cx, cy, cz)

    # RMS distance from centroid
    variance = sum(distance(p, centroid)**2 for p in positions) / n
    spread = math.sqrt(variance)

    return spread, centroid

def compute_max_distance(positions):
    """Compute maximum pairwise distance (diameter)."""
    max_dist = 0
    for i, p1 in enumerate(positions):
        for p2 in positions[i+1:]:
            d = distance(p1, p2)
            if d > max_dist:
                max_dist = d
    return max_dist

def find_focal_point():
    print("=" * 65)
    print("PRIME FOCAL POINT")
    print("Finding where primes cluster under partial inversion")
    print("=" * 65)

    N = 300
    primes = sieve_primes(N)
    prime_list = sorted(primes)

    print(f"\nPrimes up to {N}: {len(primes)}")

    # Compute original and inverted positions
    original_pos = {p: original_position(p, N) for p in prime_list}
    inverted_pos = {p: inverted_position(original_pos[p], R=0.5) for p in prime_list}

    print("\n" + "=" * 65)
    print("SEARCH 1: Linear Interpolation")
    print("=" * 65)

    # Scan t from 0 to 1
    t_values = [i/50 for i in range(51)]
    results = []

    for t in t_values:
        positions = [partial_inversion(original_pos[p], inverted_pos[p], t)
                     for p in prime_list]
        spread, centroid = compute_spread(positions)
        results.append((t, spread, centroid))

    # Find minimum spread
    min_result = min(results, key=lambda x: x[1])

    print(f"\n{'t':<8}{'Spread':<15}{'Centroid dist from origin':<25}")
    print("-" * 48)

    for t, spread, centroid in results[::5]:  # Every 5th
        cent_dist = distance(centroid, (0,0,0))
        marker = " ← MIN" if t == min_result[0] else ""
        print(f"{t:<8.2f}{spread:<15.4f}{cent_dist:<25.4f}{marker}")

    print(f"\nMinimum spread at t = {min_result[0]:.2f}")
    print(f"Spread = {min_result[1]:.4f}")

    # Finer search around minimum
    print("\n--- Fine search around minimum ---")
    t_min = max(0, min_result[0] - 0.1)
    t_max = min(1, min_result[0] + 0.1)
    t_fine = [t_min + i*(t_max-t_min)/50 for i in range(51)]

    results_fine = []
    for t in t_fine:
        positions = [partial_inversion(original_pos[p], inverted_pos[p], t)
                     for p in prime_list]
        spread, centroid = compute_spread(positions)
        results_fine.append((t, spread, centroid))

    min_fine = min(results_fine, key=lambda x: x[1])
    print(f"Refined minimum at t = {min_fine[0]:.4f}")
    print(f"Spread = {min_fine[1]:.6f}")

    print("\n" + "=" * 65)
    print("SEARCH 2: Logarithmic Interpolation (smoother)")
    print("=" * 65)

    results_log = []
    for t in t_values:
        positions = [partial_inversion_log(p, N, t, R=0.5) for p in prime_list]
        # Filter out extreme positions
        positions = [p for p in positions if distance(p, (0,0,0)) < 100]
        if len(positions) < len(prime_list) * 0.5:
            continue
        spread, centroid = compute_spread(positions)
        results_log.append((t, spread, centroid, len(positions)))

    if results_log:
        min_log = min(results_log, key=lambda x: x[1])

        print(f"\n{'t':<8}{'Spread':<15}{'Points':<10}")
        print("-" * 33)

        for t, spread, centroid, count in results_log[::5]:
            marker = " ← MIN" if t == min_log[0] else ""
            print(f"{t:<8.2f}{spread:<15.4f}{count:<10}{marker}")

        print(f"\nMinimum spread at t = {min_log[0]:.2f}")

    print("\n" + "=" * 65)
    print("ANALYSIS: What happens at the focal point?")
    print("=" * 65)

    t_focal = min_result[0]
    focal_positions = [partial_inversion(original_pos[p], inverted_pos[p], t_focal)
                       for p in prime_list]

    # Which primes are closest to centroid at focal point?
    _, focal_centroid = compute_spread(focal_positions)

    distances_to_center = [(distance(focal_positions[i], focal_centroid), prime_list[i])
                           for i in range(len(prime_list))]
    distances_to_center.sort()

    print(f"\nAt focal point t = {t_focal:.2f}:")
    print(f"Centroid: ({focal_centroid[0]:.4f}, {focal_centroid[1]:.4f}, {focal_centroid[2]:.4f})")

    print("\nPrimes closest to focal centroid:")
    for dist, p in distances_to_center[:15]:
        orig_r = distance(original_pos[p], (0,0,0))
        print(f"  p={p}: distance={dist:.4f}, original_r={orig_r:.4f}")

    print("\nPrimes farthest from focal centroid:")
    for dist, p in distances_to_center[-10:]:
        orig_r = distance(original_pos[p], (0,0,0))
        print(f"  p={p}: distance={dist:.4f}, original_r={orig_r:.4f}")

    # Is the focal t related to golden ratio?
    print("\n" + "=" * 65)
    print("IS FOCAL t SPECIAL?")
    print("=" * 65)

    t_focal = min_result[0]
    print(f"\nFocal t = {t_focal:.6f}")
    print(f"1/φ = {1/PHI:.6f}")
    print(f"1/φ² = {1/(PHI*PHI):.6f}")
    print(f"(φ-1)/φ = {(PHI-1)/PHI:.6f}")
    print(f"1/2 = 0.500000")
    print(f"1/e = {1/math.e:.6f}")

    # Synthesis
    print("\n" + "=" * 65)
    print("SYNTHESIS")
    print("=" * 65)
    print(f"""
PRIME FOCAL POINT EXISTS at t ≈ {t_focal:.2f}

This is the transformation parameter where primes cluster tightest.

Interpretation:
- t=0: primes spread from center to surface (original)
- t=1: primes spread from surface to infinity (inverted)
- t={t_focal:.2f}: primes FOCUS to minimum spread

Like a lens focusing light, partial inversion FOCUSES primes.

The focal parameter may relate to:
- Golden ratio (φ, 1/φ, 1/φ²)?
- The geometry of the golden spiral?
- Something deeper about prime distribution?

NEXT:
- Does the focal point change with different geometries?
- What's special about primes AT the focal point vs far from it?
- Is there a "focal surface" rather than a point?
""")

if __name__ == "__main__":
    find_focal_point()
