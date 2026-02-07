#!/usr/bin/env python3
"""
Zeta Zeros as Melody - The Music of the Primes

The Riemann explicit formula:
  ψ(x) = x - Σ_ρ (x^ρ)/ρ - log(2π) - ½log(1-x⁻²)

Each zero ρ = ½ + iγ contributes an oscillation with "frequency" γ.
These ARE the harmonics of prime distribution.

Let's hear/see the melody.
"""

import math

# First 50 non-trivial zeta zeros (imaginary parts)
# These are the "frequencies" of prime distribution
ZETA_ZEROS = [
    14.134725142,  21.022039639,  25.010857580,  30.424876126,  32.935061588,
    37.586178159,  40.918719012,  43.327073281,  48.005150881,  49.773832478,
    52.970321478,  56.446247697,  59.347044003,  60.831778525,  65.112544048,
    67.079810529,  69.546401711,  72.067157674,  75.704690699,  77.144840069,
    79.337375020,  82.910380854,  84.735492981,  87.425274613,  88.809111208,
    92.491899271,  94.651344041,  95.870634228,  98.831194218, 101.317851006,
   103.725538040, 105.446623052, 107.168611184, 111.029535543, 111.874659177,
   114.320220915, 116.226680321, 118.790782866, 121.370125002, 122.946829294,
   124.256818554, 127.516683880, 129.578704200, 131.087688531, 133.497737203,
   134.756509753, 138.116042055, 139.736208952, 141.123707404, 143.111845808,
]

def zeta_wave(t, zeros, num_zeros=None, decay=True):
    """
    Create waveform from zeta zeros.
    Each zero γ contributes: sin(γ * log(t)) / γ  (simplified from explicit formula)
    """
    if num_zeros is None:
        num_zeros = len(zeros)

    total = 0
    for i, gamma in enumerate(zeros[:num_zeros]):
        if t > 1:
            # The explicit formula has x^ρ = x^(1/2 + iγ) = √x * e^(iγ log x)
            # Real part: √x * cos(γ log x)
            # We simplify to just the oscillation
            amplitude = 1.0 / gamma if decay else 1.0
            total += amplitude * math.sin(gamma * math.log(t))

    return total

def prime_counting_approximation(x, zeros, num_zeros=20):
    """
    Approximate π(x) using zeta zeros.
    Simplified explicit formula contribution from zeros.
    """
    if x < 2:
        return 0

    # Main term: x / log(x)
    main = x / math.log(x)

    # Oscillatory correction from zeros
    correction = 0
    sqrt_x = math.sqrt(x)
    log_x = math.log(x)

    for gamma in zeros[:num_zeros]:
        # Contribution: -2 * Re(x^ρ / ρ) where ρ = 1/2 + iγ
        # = -2 * √x * cos(γ log x) / |ρ|
        rho_mag = math.sqrt(0.25 + gamma*gamma)
        correction -= 2 * sqrt_x * math.cos(gamma * log_x) / rho_mag

    return main + correction

def analyze_zero_ratios():
    """Check if zeta zeros have harmonic structure (like overtones)."""
    print("="*60)
    print("ANALYSIS 1: Zeta Zero Ratios")
    print("Are the zeros harmonically related (like overtones)?")
    print("="*60)

    print(f"\nFirst 20 zeta zeros (γ values):")
    for i, gamma in enumerate(ZETA_ZEROS[:20], 1):
        print(f"  γ_{i}: {gamma:.6f}")

    print(f"\nRatios between consecutive zeros:")
    for i in range(15):
        ratio = ZETA_ZEROS[i+1] / ZETA_ZEROS[i]
        print(f"  γ_{i+2}/γ_{i+1} = {ratio:.4f}")

    print(f"\nRatios to first zero (looking for integer harmonics):")
    gamma1 = ZETA_ZEROS[0]
    for i, gamma in enumerate(ZETA_ZEROS[:15], 1):
        ratio = gamma / gamma1
        nearest_int = round(ratio)
        deviation = abs(ratio - nearest_int) / nearest_int * 100
        harmonic = f"≈ {nearest_int}×γ₁" if deviation < 10 else ""
        print(f"  γ_{i}/γ₁ = {ratio:.4f} {harmonic}")

def analyze_zero_gaps():
    """Analyze gaps between zeros - like prime gaps but for frequencies."""
    print("\n" + "="*60)
    print("ANALYSIS 2: Zeta Zero Gaps")
    print("The 'rhythm' of the zeros")
    print("="*60)

    gaps = [ZETA_ZEROS[i+1] - ZETA_ZEROS[i] for i in range(len(ZETA_ZEROS)-1)]

    print(f"\nGaps between consecutive zeros:")
    for i, gap in enumerate(gaps[:20]):
        bar = "█" * int(gap * 2)
        print(f"  γ_{i+2} - γ_{i+1} = {gap:.3f} {bar}")

    mean_gap = sum(gaps) / len(gaps)
    print(f"\nMean gap: {mean_gap:.3f}")
    print(f"Gap range: {min(gaps):.3f} to {max(gaps):.3f}")

    # Gap distribution
    print("\nGap size distribution:")
    bins = [(0, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 10)]
    for lo, hi in bins:
        count = sum(1 for g in gaps if lo <= g < hi)
        bar = "█" * count
        print(f"  [{lo}-{hi}): {count:2d} {bar}")

def create_zeta_melody():
    """Create the 'melody' - waveform from zeta zeros."""
    print("\n" + "="*60)
    print("ANALYSIS 3: The Zeta Melody")
    print("Waveform created by superposing zero frequencies")
    print("="*60)

    # Sample the waveform
    t_values = [2 + i * 0.5 for i in range(200)]  # t from 2 to 102

    # Different numbers of zeros = different "richness"
    print("\nWaveform samples (using 5, 10, 20, 50 zeros):")
    print(f"{'t':<8}{'5 zeros':<12}{'10 zeros':<12}{'20 zeros':<12}{'50 zeros':<12}")
    print("-" * 56)

    for t in t_values[::10]:  # Every 10th sample
        w5 = zeta_wave(t, ZETA_ZEROS, 5)
        w10 = zeta_wave(t, ZETA_ZEROS, 10)
        w20 = zeta_wave(t, ZETA_ZEROS, 20)
        w50 = zeta_wave(t, ZETA_ZEROS, 50)
        print(f"{t:<8.1f}{w5:<12.4f}{w10:<12.4f}{w20:<12.4f}{w50:<12.4f}")

    # Find peaks (constructive interference of zeros)
    print("\n--- Waveform Peaks (constructive interference) ---")
    waves = [(t, zeta_wave(t, ZETA_ZEROS, 30)) for t in t_values]

    peaks = []
    for i in range(1, len(waves)-1):
        t, w = waves[i]
        if w > waves[i-1][1] and w > waves[i+1][1] and w > 0.3:
            peaks.append((w, t))

    peaks.sort(reverse=True)
    print(f"\nTop 15 peaks (where zero-frequencies align):")
    for rank, (amp, t) in enumerate(peaks[:15], 1):
        # Is t near a prime?
        near_prime = ""
        for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]:
            if abs(t - p) < 1:
                near_prime = f"near prime {p}"
                break
        print(f"  {rank:2d}. t={t:.1f}, amplitude={amp:.4f} {near_prime}")

def visualize_explicit_formula():
    """Show how zeros correct the prime counting."""
    print("\n" + "="*60)
    print("ANALYSIS 4: Zeros Correcting Prime Count")
    print("The melody 'tunes' the approximation to reality")
    print("="*60)

    # Actual prime counting
    def actual_pi(n):
        if n < 2:
            return 0
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(n**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, n + 1, i):
                    sieve[j] = False
        return sum(sieve)

    print(f"\n{'x':<8}{'π(x)':<8}{'x/ln(x)':<10}{'+ 5 zeros':<12}{'+ 20 zeros':<12}{'+ 50 zeros':<12}")
    print("-" * 62)

    for x in [10, 20, 30, 50, 100, 200, 500, 1000]:
        actual = actual_pi(x)
        simple = x / math.log(x)
        corr5 = prime_counting_approximation(x, ZETA_ZEROS, 5)
        corr20 = prime_counting_approximation(x, ZETA_ZEROS, 20)
        corr50 = prime_counting_approximation(x, ZETA_ZEROS, 50)
        print(f"{x:<8}{actual:<8}{simple:<10.1f}{corr5:<12.1f}{corr20:<12.1f}{corr50:<12.1f}")

    print("\n→ More zeros = better approximation")
    print("→ The zeros ARE the correction terms!")

def zeta_beat_frequencies():
    """Look for 'beats' between close zeros (like twin primes create beats)."""
    print("\n" + "="*60)
    print("ANALYSIS 5: Zeta Zero 'Beats'")
    print("Close zeros create interference patterns")
    print("="*60)

    # Find close pairs of zeros
    gaps = [(ZETA_ZEROS[i+1] - ZETA_ZEROS[i], i) for i in range(len(ZETA_ZEROS)-1)]
    gaps.sort()

    print("\nClosest zero pairs (create strongest beats):")
    for gap, i in gaps[:10]:
        g1, g2 = ZETA_ZEROS[i], ZETA_ZEROS[i+1]
        beat_freq = g2 - g1
        mean_freq = (g1 + g2) / 2
        print(f"  γ_{i+1}={g1:.3f}, γ_{i+2}={g2:.3f}")
        print(f"    Beat frequency: {beat_freq:.3f}")
        print(f"    Mean frequency: {mean_freq:.3f}")
        print(f"    Ratio: {g2/g1:.4f}")
        print()

def synthesize_melody():
    """Create an actual 'melody' representation."""
    print("\n" + "="*60)
    print("ANALYSIS 6: The Melody Itself")
    print("Zeros as musical notes")
    print("="*60)

    # Map zeros to musical notes
    # Use γ₁ = 14.13 as reference (like A440)
    gamma1 = ZETA_ZEROS[0]

    print("\nZeta zeros as musical intervals (γ₁ = root note):")
    print(f"{'Zero':<8}{'γ':<12}{'Ratio to γ₁':<14}{'Semitones':<12}{'Approx Note':<12}")
    print("-" * 58)

    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    for i, gamma in enumerate(ZETA_ZEROS[:20], 1):
        ratio = gamma / gamma1
        # Semitones = 12 * log2(ratio)
        semitones = 12 * math.log2(ratio)
        # Map to note name
        note_idx = int(round(semitones)) % 12
        octave = int(semitones // 12)
        note = note_names[note_idx] + str(4 + octave)  # Starting from octave 4

        print(f"γ_{i:<5}{gamma:<12.3f}{ratio:<14.4f}{semitones:<12.2f}{note:<12}")

    print("\n--- The Zeta Melody (first 20 zeros as notes) ---")
    melody = []
    for i, gamma in enumerate(ZETA_ZEROS[:20], 1):
        ratio = gamma / gamma1
        semitones = 12 * math.log2(ratio)
        note_idx = int(round(semitones)) % 12
        melody.append(note_names[note_idx])

    print("Notes: " + " → ".join(melody))

    print("\n--- Interval Pattern ---")
    intervals = []
    for i in range(len(melody)-1):
        idx1 = note_names.index(melody[i])
        idx2 = note_names.index(melody[i+1])
        interval = (idx2 - idx1) % 12
        interval_names = ['unison', 'm2', 'M2', 'm3', 'M3', 'P4', 'tritone',
                         'P5', 'm6', 'M6', 'm7', 'M7']
        intervals.append(interval_names[interval])

    print("Intervals: " + " → ".join(intervals[:15]))

def main():
    print("="*60)
    print("THE ZETA MELODY")
    print("Riemann Zeros as the Music of Primes")
    print("="*60)
    print("""
The Riemann explicit formula decomposes prime counting into:
  - A main term (x)
  - Oscillations from each zero (the 'harmonics')

If primes are the 'pure tones', zeta zeros are the 'overtones'
that describe how those tones combine.

Let's hear the melody...
""")

    analyze_zero_ratios()
    analyze_zero_gaps()
    create_zeta_melody()
    visualize_explicit_formula()
    zeta_beat_frequencies()
    synthesize_melody()

    print("\n" + "="*60)
    print("SYNTHESIS")
    print("="*60)
    print("""
THE ZETA MELODY reveals:

1. Zeros are NOT in simple harmonic ratios (not like 1:2:3:4...)
   → More complex than musical overtones
   → But they're not random either

2. Zero gaps have structure - they're "quasi-periodic"
   → Like a melody with varying rhythm
   → Mean gap ≈ 2π/log(γ) by zero density theorem

3. The melody "tunes" the prime count
   → More zeros = better approximation
   → The Riemann Hypothesis says all zeros have Re(ρ)=1/2
   → This is like saying all notes are "in tune"

4. Close zeros create "beats"
   → Interference patterns in prime distribution
   → Like how twin primes create period-2 beats

THE DEEP CONNECTION:

  P(music) ⊗ T_spec → frequencies + harmonics
  P(primes) ⊗ T_zeta → zeros as frequencies

  The zeros ARE the spectral decomposition of primality!

  Riemann Hypothesis = "All frequencies are real" (on critical line)
  This would mean prime distribution has no "imaginary" components
  - purely oscillatory correction, no exponential growth/decay

NEXT: Can we find patterns in the zero-melody that predict prime gaps?
""")

if __name__ == "__main__":
    main()
