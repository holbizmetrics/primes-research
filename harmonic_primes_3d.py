#!/usr/bin/env python3
"""
Harmonic Primes in 3D - Combining spectral analysis with spatial projection

User insights:
- "twins create overtone resonances of others in their environment"
- "audio waves in the 3d projected space"
- "play the right note, chord or melody"
- "harmonics of frequencies"

CTA chain:
  P(harmonics) ⊗ T_spec ⊗ P(3D_projection) → P(prime_standing_waves)

Like Chladni figures: where do primes "settle" when we vibrate the space?
"""

import math

PHI = (1 + math.sqrt(5)) / 2  # Golden ratio

def sieve_primes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]

def find_twin_primes(primes):
    """Find twin prime pairs (gap of 2)."""
    twins = []
    for i in range(len(primes) - 1):
        if primes[i+1] - primes[i] == 2:
            twins.append((primes[i], primes[i+1]))
    return twins

def find_prime_tuples(primes):
    """Find various prime constellations."""
    twins = []      # gap 2: (p, p+2)
    cousins = []    # gap 4: (p, p+4)
    sexy = []       # gap 6: (p, p+6)
    triplets = []   # (p, p+2, p+6) or (p, p+4, p+6)

    prime_set = set(primes)

    for p in primes:
        if p + 2 in prime_set:
            twins.append((p, p+2))
        if p + 4 in prime_set:
            cousins.append((p, p+4))
        if p + 6 in prime_set:
            sexy.append((p, p+6))

        # Triplets
        if p + 2 in prime_set and p + 6 in prime_set:
            triplets.append((p, p+2, p+6))
        if p + 4 in prime_set and p + 6 in prime_set:
            triplets.append((p, p+4, p+6))

    return {'twins': twins, 'cousins': cousins, 'sexy': sexy, 'triplets': triplets}

def golden_spiral_3d(n, surface='sphere'):
    """
    Map integer n to 3D point using golden spiral.
    Same method as the 3D prime visualizer.
    """
    # Golden angle
    golden_angle = 2 * math.pi / (PHI * PHI)

    if surface == 'sphere':
        # Fibonacci sphere
        t = n / 1000  # Normalize
        theta = golden_angle * n
        phi = math.acos(1 - 2 * t) if 0 < t < 1 else 0

        x = math.sin(phi) * math.cos(theta)
        y = math.sin(phi) * math.sin(theta)
        z = math.cos(phi)
        return (x, y, z)

    elif surface == 'helix':
        theta = golden_angle * n
        r = 1
        z = n / 100
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return (x, y, z)

def wave_amplitude(x, y, z, freq, t=0):
    """
    3D standing wave at given frequency.
    Like a vibrating sphere/shell.
    """
    r = math.sqrt(x*x + y*y + z*z)
    if r < 0.001:
        return 1.0

    # Spherical wave
    return math.sin(2 * math.pi * freq * r + t) / r

def interference_at_point(x, y, z, frequencies, amplitudes=None):
    """
    Sum of waves from multiple frequencies (primes) at a point.
    Constructive interference where phases align.
    """
    if amplitudes is None:
        amplitudes = [1.0 / math.log(f) for f in frequencies]

    total = 0
    for freq, amp in zip(frequencies, amplitudes):
        total += amp * wave_amplitude(x, y, z, freq / 50)  # Scale frequencies

    return total

def analyze_prime_wave_pattern():
    print("=" * 60)
    print("HARMONIC PRIMES IN 3D")
    print("Standing waves & resonance patterns")
    print("=" * 60)
    print()

    LIMIT = 500
    primes = sieve_primes(LIMIT)
    print(f"Primes up to {LIMIT}: {len(primes)}")

    # Find prime constellations
    tuples = find_prime_tuples(primes)
    twins = tuples['twins']
    print(f"\nPrime constellations found:")
    print(f"  Twin primes (gap 2): {len(twins)}")
    print(f"  Cousin primes (gap 4): {len(tuples['cousins'])}")
    print(f"  Sexy primes (gap 6): {len(tuples['sexy'])}")
    print(f"  Triplets: {len(tuples['triplets'])}")

    # Analysis 1: Twin prime "beats"
    print("\n" + "="*60)
    print("ANALYSIS 1: Twin Prime 'Beats'")
    print("="*60)
    print("""
When two close frequencies combine: beat frequency = |f1 - f2|
Twin primes have gap 2, so their "beat" frequency is always 2.

This creates a standing wave pattern with period 2 overlaid on the prime field.
""")

    # Calculate beat patterns
    print("Twin pairs and their 'mean frequency' (geometric):")
    for p1, p2 in twins[:10]:
        mean_freq = math.sqrt(p1 * p2)
        beat = p2 - p1  # Always 2 for twins
        print(f"  ({p1}, {p2}): mean={mean_freq:.2f}, beat={beat}")

    # Analysis 2: 3D interference pattern
    print("\n" + "="*60)
    print("ANALYSIS 2: 3D Interference Pattern")
    print("="*60)
    print("Using small primes as frequencies, where is interference highest?")

    small_primes = primes[:10]  # 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
    print(f"Frequencies (primes): {small_primes}")

    # Sample points on sphere
    sample_points = []
    for i in range(200):
        pos = golden_spiral_3d(i * 5, 'sphere')
        sample_points.append((i * 5, pos))

    # Calculate interference at each point
    interferences = []
    for n, (x, y, z) in sample_points:
        interf = interference_at_point(x, y, z, small_primes)
        interferences.append((interf, n, x, y, z))

    # Find maxima (constructive interference)
    interferences.sort(reverse=True)

    print("\nTop 15 constructive interference points (nodes):")
    print(f"{'Rank':<6}{'n':<8}{'Amplitude':<12}{'Is Prime':<10}")
    print("-" * 40)

    for rank, (amp, n, x, y, z) in enumerate(interferences[:15], 1):
        is_prime = "YES" if n in primes else ""
        print(f"{rank:<6}{n:<8}{amp:<12.4f}{is_prime:<10}")

    # Find minima (destructive interference)
    print("\nBottom 15 (destructive interference - anti-nodes):")
    for rank, (amp, n, x, y, z) in enumerate(interferences[-15:], 1):
        is_prime = "YES" if n in primes else ""
        print(f"{rank:<6}{n:<8}{amp:<12.4f}{is_prime:<10}")

    # Analysis 3: Prime "chord" combinations
    print("\n" + "="*60)
    print("ANALYSIS 3: Prime 'Chords'")
    print("="*60)
    print("""
In music: major chord = 1:5/4:3/2 frequency ratio
         minor chord = 1:6/5:3/2
         perfect fifth = 2:3

What "chords" do primes form?
""")

    # Check prime ratios
    print("Frequency ratios between small primes:")
    for i in range(min(8, len(primes))):
        for j in range(i+1, min(8, len(primes))):
            p1, p2 = primes[i], primes[j]
            ratio = p2 / p1
            # Check if close to simple ratio
            for num in range(1, 6):
                for den in range(1, 6):
                    if abs(ratio - num/den) < 0.05:
                        print(f"  {p2}/{p1} = {ratio:.3f} ≈ {num}/{den}")

    # Analysis 4: Harmonic series of 2
    print("\n" + "="*60)
    print("ANALYSIS 4: Harmonic Series")
    print("="*60)
    print("""
If 2 is the "fundamental frequency":
  Harmonics: 2, 4, 6, 8, 10, 12, ...
  These are the EVEN numbers!

If we remove the 2-harmonics, we get odd numbers.
The remaining "dissonance" pattern = primes (mostly).

The primes are what's LEFT after removing harmonic structure.
They're the "irreducible frequencies".
""")

    # Residual after removing harmonics
    all_nums = set(range(3, 100))
    # Remove harmonics of 2, 3, 5
    for p in [2, 3, 5]:
        for k in range(2, 100 // p + 1):
            all_nums.discard(p * k)

    remaining = sorted(all_nums)
    print(f"Numbers that aren't harmonics of 2, 3, or 5:")
    print(f"  {remaining}")
    print(f"\nOf these, primes are: {[n for n in remaining if n in primes]}")

    # Analysis 5: Twin resonance environment
    print("\n" + "="*60)
    print("ANALYSIS 5: Twin Prime Environment")
    print("="*60)
    print("""
Your insight: twins "create overtone resonances of others in their environment"

Near twin primes, what's the interference pattern?
""")

    for p1, p2 in twins[5:8]:
        print(f"\nTwin pair ({p1}, {p2}):")
        # Check numbers in neighborhood
        neighborhood = range(max(2, p1-10), p2+11)
        for n in neighborhood:
            # Wave from twin pair
            d1 = abs(n - p1)
            d2 = abs(n - p2)
            # Simple interference model
            if d1 > 0 and d2 > 0:
                wave1 = math.sin(2 * math.pi * p1 * d1 / 20)
                wave2 = math.sin(2 * math.pi * p2 * d2 / 20)
                combined = (wave1 + wave2) / 2
            else:
                combined = 1.0

            marker = "◆" if n in primes else "○"
            bar = "█" * int(10 * (combined + 1))
            twin_marker = " ← TWIN" if n == p1 or n == p2 else ""
            print(f"  {marker} {n:3d}: {combined:+.3f} {bar}{twin_marker}")

    # Synthesis
    print("\n" + "="*60)
    print("SYNTHESIS")
    print("="*60)
    print("""
PRIMES AS HARMONIC STRUCTURE:

1. Primes are the "fundamental frequencies" - can't be decomposed further
2. Composites are "chords" (products of prime frequencies)
3. Twins create "beat frequencies" with period 2
4. In 3D projection, interference patterns may reveal structure

THE KEY INSIGHT:
  "Harmonics of frequencies" - YES!

  - In music: overtones are integer MULTIPLES of fundamental
  - In primes: zeta zeros are the FREQUENCIES of prime distribution
  - The Riemann explicit formula IS the Fourier decomposition!

  ψ(x) = x - Σ_ρ (x^ρ)/ρ - ...

  Each zero ρ = 1/2 + iγ contributes an oscillation with frequency γ.
  These ARE the harmonics of the prime-counting function!

NEXT: What's the "melody"? The sequence of zeta zeros...
""")

if __name__ == "__main__":
    analyze_prime_wave_pattern()
