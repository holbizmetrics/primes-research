#!/usr/bin/env python3
"""
ZETA ZEROS AS 3D OPERATORS

Hypothesis: γ₂ ≈ 21 = F_8 encodes a 3D location/operator
on the golden-spiral prime space.

What's special about position 21 on the sphere?
What about 21 + 1/45?
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
    return set(i for i in range(limit + 1) if is_prime[i])

def fibonacci_list(max_val):
    fibs = [1, 1]
    while fibs[-1] < max_val:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

def golden_spiral_3d(n, N):
    """Map n to 3D point on sphere."""
    theta = GOLDEN_ANGLE * n
    z = 1 - (2 * n) / N
    z = max(-1, min(1, z))
    r_xy = math.sqrt(max(0, 1 - z*z))
    x = r_xy * math.cos(theta)
    y = r_xy * math.sin(theta)
    return (x, y, z)

def distance_3d(p1, p2):
    return math.sqrt(sum((a-b)**2 for a, b in zip(p1, p2)))

def angular_distance(p1, p2):
    dot = sum(a*b for a, b in zip(p1, p2))
    dot = max(-1, min(1, dot))
    return math.acos(dot)

def analyze_zeta_positions():
    print("=" * 70)
    print("ZETA ZEROS AS 3D POSITIONS/OPERATORS")
    print("=" * 70)

    N = 500
    primes = sieve_primes(N)
    fibs = set(fibonacci_list(N))

    print(f"\nMapped to golden-spiral sphere with N={N}")

    # Map zeta zeros to 3D positions (treating them as indices)
    print("\n" + "=" * 70)
    print("ZETA ZEROS AS POSITIONS ON GOLDEN SPIRAL")
    print("=" * 70)

    print(f"\n{'Zero':<8}{'γ':<12}{'Position':<30}{'Near prime?':<15}")
    print("-" * 65)

    for i, gamma in enumerate(ZETA_ZEROS, 1):
        # Treat gamma as a continuous index
        pos = golden_spiral_3d(gamma, N)

        # Is gamma near a prime?
        near_primes = [p for p in primes if abs(p - gamma) < 2]
        near_str = str(near_primes) if near_primes else ""

        # Is gamma near a Fibonacci?
        near_fib = [f for f in fibs if abs(f - gamma) < 2]

        marker = ""
        if near_fib:
            marker = f"NEAR F={near_fib[0]}"

        print(f"γ_{i:<5}{gamma:<12.3f}({pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}){near_str:<15}{marker}")

    # Position 21 specifically
    print("\n" + "=" * 70)
    print("POSITION 21 (γ₂ ≈ 21 = F_8)")
    print("=" * 70)

    pos_21 = golden_spiral_3d(21, N)
    pos_21_022 = golden_spiral_3d(21.022, N)

    print(f"\nPosition 21.000: ({pos_21[0]:.6f}, {pos_21[1]:.6f}, {pos_21[2]:.6f})")
    print(f"Position 21.022: ({pos_21_022[0]:.6f}, {pos_21_022[1]:.6f}, {pos_21_022[2]:.6f})")
    print(f"Distance between them: {distance_3d(pos_21, pos_21_022):.6f}")

    # What's near position 21?
    print("\nIntegers closest to position 21 on sphere:")

    distances_to_21 = [(angular_distance(golden_spiral_3d(n, N), pos_21), n) for n in range(1, 100)]
    distances_to_21.sort()

    for ang_dist, n in distances_to_21[:15]:
        is_prime = "PRIME" if n in primes else ""
        is_fib = "FIB" if n in fibs else ""
        print(f"  n={n}: angular dist={ang_dist:.4f} {is_prime} {is_fib}")

    # Primes near each zeta zero position
    print("\n" + "=" * 70)
    print("PRIMES IN NEIGHBORHOOD OF EACH ZETA ZERO")
    print("=" * 70)

    for i, gamma in enumerate(ZETA_ZEROS[:5], 1):
        pos_gamma = golden_spiral_3d(gamma, N)

        # Find primes closest to this position
        prime_dists = [(angular_distance(golden_spiral_3d(p, N), pos_gamma), p) for p in primes if p < 100]
        prime_dists.sort()

        nearest = [p for _, p in prime_dists[:5]]
        print(f"\nγ_{i} = {gamma:.3f}: nearest primes = {nearest}")

    # The correction 1/45
    print("\n" + "=" * 70)
    print("THE CORRECTION 1/45")
    print("=" * 70)

    correction = 1/45
    print(f"\nγ₂ = 21 + {correction:.6f}")
    print(f"1/45 = {correction:.6f}")

    # In 3D terms
    pos_21 = golden_spiral_3d(21, N)
    pos_21_plus = golden_spiral_3d(21 + correction, N)

    displacement = (pos_21_plus[0] - pos_21[0],
                   pos_21_plus[1] - pos_21[1],
                   pos_21_plus[2] - pos_21[2])

    print(f"\n3D displacement from adding 1/45:")
    print(f"  Δx = {displacement[0]:.6f}")
    print(f"  Δy = {displacement[1]:.6f}")
    print(f"  Δz = {displacement[2]:.6f}")
    print(f"  |Δ| = {math.sqrt(sum(d**2 for d in displacement)):.6f}")

    # Angular displacement
    ang_disp = angular_distance(pos_21, pos_21_plus)
    print(f"  Angular: {ang_disp:.6f} rad = {math.degrees(ang_disp):.4f}°")

    # What's 45 in this context?
    print("\n" + "=" * 70)
    print("WHAT IS 45?")
    print("=" * 70)

    print(f"\n45 = 9 × 5 = 3² × 5")
    print(f"45 = 2×21 + 3 = 2×F_8 + 3")
    print(f"45 is position on golden spiral too:")

    pos_45 = golden_spiral_3d(45, N)
    print(f"Position 45: ({pos_45[0]:.4f}, {pos_45[1]:.4f}, {pos_45[2]:.4f})")

    # Angular relationship between 21 and 45
    ang_21_45 = angular_distance(pos_21, pos_45)
    print(f"Angular distance 21 ↔ 45: {ang_21_45:.4f} rad = {math.degrees(ang_21_45):.2f}°")

    # Is 45 = 21 + 24 = F_8 + 24 related?
    print(f"\n45 - 21 = 24 = 4! (factorial)")
    print(f"45 - 21 = 24 = 2³ × 3")

    # Operator interpretation
    print("\n" + "=" * 70)
    print("OPERATOR INTERPRETATION")
    print("=" * 70)

    print(f"""
If zeta zeros are 3D operators:

γ₂ = 21 + 1/45 could mean:

1. "GO TO" operator:
   - Go to position F_8 = 21 on golden spiral
   - The operator "points at" position 21

2. "NEIGHBORHOOD" operator:
   - Position 21 ± ε defines a region
   - ε = 1/45 ≈ 0.022 is the "radius"

3. "CORRECTION" operator:
   - Start at Fibonacci position 21
   - Apply small correction toward next structure
   - 1/(2×21+3) = 1/45 relates 21 to its "neighborhood size"

4. "RESONANCE" operator:
   - Position 21 resonates with primes nearby
   - The zeros mark resonant positions on the sphere

The formula γ₂ = F_8 + 1/(2F_8 + 3) suggests:
- Each Fibonacci position has a characteristic "correction"
- The correction shrinks as F grows
- This defines a sequence of 3D operators
""")

    # Test: do other zeros follow similar pattern?
    print("\n" + "=" * 70)
    print("DO OTHER ZEROS FOLLOW SIMILAR PATTERN?")
    print("=" * 70)

    fibs = fibonacci_list(200)

    for i, gamma in enumerate(ZETA_ZEROS[:6], 1):
        # Find nearest Fibonacci
        nearest_fib = min(fibs, key=lambda f: abs(f - gamma))
        diff = gamma - nearest_fib

        if abs(diff) < 3:
            # Check if diff ≈ 1/(2F + k) for some small k
            for k in range(-5, 10):
                denom = 2 * nearest_fib + k
                if denom > 0:
                    predicted = 1 / denom
                    if abs(diff - predicted) < 0.01:
                        print(f"γ_{i} = {gamma:.3f} ≈ F={nearest_fib} + 1/{denom} (k={k})")
                        break
            else:
                print(f"γ_{i} = {gamma:.3f} ≈ F={nearest_fib} + {diff:.4f} (no simple formula)")
        else:
            print(f"γ_{i} = {gamma:.3f} not near Fibonacci")

if __name__ == "__main__":
    analyze_zeta_positions()
