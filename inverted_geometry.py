#!/usr/bin/env python3
"""
Geometric Inversion of Prime Space

"What if we turn each geometry inside out?"

Inversion through a sphere: r → R²/r
- Inside becomes outside
- Outside becomes inside
- Structure inverts

Apply to prime-decorated geometries.
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

def golden_spiral_3d(n, total, radius_func=None):
    """
    Map n to 3D point. radius_func(n) determines radial distance.
    Default: points on unit sphere.
    """
    theta = GOLDEN_ANGLE * n
    z = 1 - (2 * n) / total
    z = max(-1, min(1, z))
    r_xy = math.sqrt(max(0, 1 - z*z))

    if radius_func:
        r = radius_func(n)
        # Scale the point
        x = r * r_xy * math.cos(theta)
        y = r * r_xy * math.sin(theta)
        z = r * z
    else:
        x = r_xy * math.cos(theta)
        y = r_xy * math.sin(theta)

    return (x, y, z)

def invert_point(point, R=1.0):
    """
    Inversion through sphere of radius R centered at origin.
    P → R²/|P|² × P
    """
    x, y, z = point
    r_sq = x*x + y*y + z*z
    if r_sq < 1e-10:
        return (float('inf'), float('inf'), float('inf'))

    scale = R * R / r_sq
    return (x * scale, y * scale, z * scale)

def distance_from_origin(point):
    x, y, z = point
    return math.sqrt(x*x + y*y + z*z)

def analyze_inverted_primes():
    print("=" * 65)
    print("GEOMETRIC INVERSION OF PRIME SPACE")
    print("Turning the geometry inside-out")
    print("=" * 65)

    N = 500
    primes = sieve_primes(N)

    print(f"\nPoints: {N}, Primes: {len(primes)}")

    # Original: primes on unit sphere
    print("\n" + "=" * 65)
    print("ANALYSIS 1: Radial Distribution Before/After Inversion")
    print("=" * 65)

    # Map n to radius based on its value (not unit sphere)
    # r(n) = n / N  (so n=1 is at center, n=N is at surface)
    def radius_by_n(n):
        return n / N

    # Original positions
    original_positions = {}
    for n in range(1, N + 1):
        # Point on sphere scaled by n/N
        theta = GOLDEN_ANGLE * n
        z_unit = 1 - (2 * n) / N
        z_unit = max(-1, min(1, z_unit))
        r_xy = math.sqrt(max(0, 1 - z_unit*z_unit))

        r = n / N
        x = r * r_xy * math.cos(theta)
        y = r * r_xy * math.sin(theta)
        z = r * z_unit
        original_positions[n] = (x, y, z)

    # Inverted positions
    inverted_positions = {}
    for n, pos in original_positions.items():
        inverted_positions[n] = invert_point(pos, R=1.0)

    # Compare radial distances
    print("\nOriginal: small n → near center, large n → near surface")
    print("Inverted: small n → far out, large n → near center")

    print(f"\n{'n':<8}{'Prime?':<8}{'r (orig)':<12}{'r (inv)':<12}")
    print("-" * 40)

    for n in [2, 3, 5, 10, 50, 100, 250, 499]:
        is_p = "YES" if n in primes else ""
        r_orig = distance_from_origin(original_positions[n])
        r_inv = distance_from_origin(inverted_positions[n])
        print(f"{n:<8}{is_p:<8}{r_orig:<12.4f}{r_inv:<12.4f}")

    # Analysis 2: Where do primes cluster after inversion?
    print("\n" + "=" * 65)
    print("ANALYSIS 2: Prime Clustering After Inversion")
    print("=" * 65)

    # Bin by inverted radius
    bins = [(0, 0.5), (0.5, 1), (1, 2), (2, 5), (5, 10), (10, 50), (50, 500)]

    print("\nPrime density by inverted radius:")
    print(f"{'Radius range':<15}{'Total':<10}{'Primes':<10}{'Density':<10}")
    print("-" * 45)

    for lo, hi in bins:
        total_in_bin = 0
        primes_in_bin = 0
        for n in range(1, N + 1):
            r_inv = distance_from_origin(inverted_positions[n])
            if lo <= r_inv < hi:
                total_in_bin += 1
                if n in primes:
                    primes_in_bin += 1

        density = primes_in_bin / total_in_bin if total_in_bin > 0 else 0
        print(f"[{lo}, {hi}){'':<5}{total_in_bin:<10}{primes_in_bin:<10}{density:<10.3f}")

    # Analysis 3: The "inside" vs "outside" exchange
    print("\n" + "=" * 65)
    print("ANALYSIS 3: Inside-Outside Exchange")
    print("=" * 65)

    # In original: center = small n, surface = large n
    # In inverted: center = large n, surface = small n

    # Which primes were "inside" (small n) vs "outside" (large n)?
    small_primes = [p for p in primes if p <= N//4]
    large_primes = [p for p in primes if p > 3*N//4]

    print(f"\nSmall primes (n ≤ {N//4}): {len(small_primes)}")
    print(f"Large primes (n > {3*N//4}): {len(large_primes)}")

    print("\nAfter inversion:")
    print("  - Small primes (2,3,5,7,...) are now FAR from center")
    print("  - Large primes (491,499,...) are now NEAR center")

    # The "view from inside" vs "view from outside"
    print("\n" + "=" * 65)
    print("ANALYSIS 4: Angular Distribution Changes")
    print("=" * 65)

    # Before inversion: angular position determined by golden spiral
    # After inversion: angular position UNCHANGED (inversion preserves angles!)

    print("""
KEY INSIGHT: Spherical inversion PRESERVES ANGLES!

The angular distribution (θ, φ) is the same before and after.
What changes is ONLY the radial distance.

So the spherical harmonic structure (l, m modes) is UNCHANGED.

But the RADIAL structure inverts:
- Primes that were "core" become "halo"
- Primes that were "halo" become "core"
""")

    # Analysis 5: What about composites?
    print("\n" + "=" * 65)
    print("ANALYSIS 5: The Composite Complement")
    print("=" * 65)

    composites = set(range(2, N+1)) - primes

    print(f"\nComposites: {len(composites)}")

    # Highly composite numbers
    def count_divisors(n):
        count = 0
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                count += 2 if i != n // i else 1
        return count

    highly_composite = sorted(composites, key=count_divisors, reverse=True)[:10]

    print("\nHighly composite numbers and their inverted positions:")
    print(f"{'n':<8}{'Divisors':<10}{'r (orig)':<12}{'r (inv)':<12}")
    print("-" * 42)

    for n in highly_composite:
        div = count_divisors(n)
        r_orig = distance_from_origin(original_positions[n])
        r_inv = distance_from_origin(inverted_positions[n])
        print(f"{n:<8}{div:<10}{r_orig:<12.4f}{r_inv:<12.4f}")

    print("""
After inversion, highly composite numbers (360, 420, 480...)
move toward the CENTER, while small primes (2, 3, 5, 7...)
move toward INFINITY.

This is the "dual view":
- Original: primes are the "atoms", composites fill space
- Inverted: composites concentrate at core, primes form halo
""")

    # Analysis 6: Torus inversion?
    print("\n" + "=" * 65)
    print("ANALYSIS 6: Other Geometries")
    print("=" * 65)

    print("""
SPHERE: Inversion through center
  - Clean mathematical inversion
  - Radial distances flip
  - Angles preserved

TORUS: More complex!
  - Has a hole (genus 1)
  - Inversion through center would...
    - Map inner surface to outer
    - The "hole" becomes the "exterior"
  - Creates interesting topology

ICOSAHEDRON:
  - 20 faces → 20 inverted faces
  - The "soccer ball cells" would invert
  - Dual polyhedron is the dodecahedron!

HELIX:
  - Inversion creates... involute spiral?
  - The "coiling" direction reverses sense
""")

    # Synthesis
    print("\n" + "=" * 65)
    print("SYNTHESIS")
    print("=" * 65)
    print("""
GEOMETRIC INVERSION = T_inv applied to SPACE

What we learn:
1. Angular structure is PRESERVED (spherical harmonics unchanged)
2. Radial structure INVERTS (core ↔ halo)
3. Primes and composites exchange "inside/outside" roles
4. The DUAL VIEW reveals complementary structure

CTA chain:
  P(prime_geometry) ⊗ T_inv → P(inverted_prime_geometry)

The "inside-out" view shows what the original hides:
- Where do composites cluster?
- What's the structure of "prime absence"?
- The negative space has its own patterns.

NEXT: Combine inversion with wave propagation
      - Shine a wave from the center outward
      - vs. shine a wave from infinity inward
      - How do the scattering patterns differ?
""")

if __name__ == "__main__":
    analyze_inverted_primes()
