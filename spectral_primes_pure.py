#!/usr/bin/env python3
"""
Spectral Analysis of Primes - Pure Python version
Exploring overtone/resonance structure

CTA approach: P(sound/overtones) ⊗ T_spec → P(primes)
User insight: "overtones creating resonance like light breaking or sounds combining"
              "primes as a global operator - they combine"
"""

import math
import cmath
from collections import defaultdict

def sieve_primes(limit):
    """Generate primes up to limit."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]

def dft(signal):
    """
    Discrete Fourier Transform (direct computation).
    For small signals - O(n^2) but no dependencies.
    """
    n = len(signal)
    result = []
    for k in range(n):
        total = 0
        for t in range(n):
            angle = -2 * math.pi * k * t / n
            total += signal[t] * cmath.exp(complex(0, angle))
        result.append(total)
    return result

def fft(signal):
    """
    Fast Fourier Transform - Cooley-Tukey algorithm.
    Requires length to be power of 2.
    """
    n = len(signal)
    if n <= 1:
        return signal

    if n % 2 != 0:
        # Pad to power of 2
        next_pow2 = 1
        while next_pow2 < n:
            next_pow2 *= 2
        signal = list(signal) + [0] * (next_pow2 - n)
        n = next_pow2

    # Recursive FFT
    if n <= 32:
        return dft(signal)

    even = fft(signal[0::2])
    odd = fft(signal[1::2])

    result = [0] * n
    for k in range(n // 2):
        t = cmath.exp(complex(0, -2 * math.pi * k / n)) * odd[k]
        result[k] = even[k] + t
        result[k + n // 2] = even[k] - t

    return result

def power_spectrum(fft_result):
    """Compute power spectrum (magnitude squared)."""
    return [abs(x)**2 for x in fft_result]

def find_peaks(power, freqs, top_k=10):
    """Find top-k frequency peaks by power."""
    indexed = [(power[i], freqs[i], i) for i in range(len(power)) if freqs[i] > 0]
    indexed.sort(reverse=True)
    return indexed[:top_k]

def check_harmonic_ratios(peak_freqs):
    """
    Check if frequencies show harmonic (overtone) ratios.
    In music: fundamental f has overtones at 2f, 3f, 4f, ...
    """
    if len(peak_freqs) < 2:
        return []

    results = []
    # Try each frequency as potential fundamental
    for i, f1 in enumerate(peak_freqs[:5]):
        if f1 < 1e-10:
            continue
        harmonics = []
        for f2 in peak_freqs:
            if f2 < 1e-10:
                continue
            ratio = f2 / f1
            nearest = round(ratio)
            if nearest > 0 and abs(ratio - nearest) < 0.08:
                harmonics.append((nearest, f2))
        if len(harmonics) > 2:
            results.append((f1, harmonics))

    return results

def prime_resonance_analysis():
    """
    Main analysis: Do primes exhibit resonance/overtone structure?

    Key insight from user: primes might act as "global operators"
    that combine like overtones creating resonance.
    """
    print("=" * 60)
    print("SPECTRAL PRIMES: Resonance & Overtone Analysis")
    print("=" * 60)
    print()
    print("Hypothesis: Primes as frequencies that combine/resonate")
    print("Like: light → prism → spectrum")
    print("Like: sound → harmonics → overtones")
    print()

    # Generate primes
    LIMIT = 2048  # Power of 2 for FFT
    primes = sieve_primes(LIMIT)
    print(f"Primes up to {LIMIT}: {len(primes)}")

    # Create prime indicator signal
    indicator = [0] * LIMIT
    for p in primes:
        if p < LIMIT:
            indicator[p] = 1

    print(f"\n{'='*60}")
    print("ANALYSIS 1: Prime Indicator χ(n)")
    print("What frequencies are 'hidden' in prime positions?")
    print("='*60")

    # FFT
    print("Computing FFT...")
    fft_result = fft(indicator)
    power = power_spectrum(fft_result)

    # Frequencies
    n = len(fft_result)
    freqs = [k/n for k in range(n)]

    # Find peaks
    peaks = find_peaks(power, freqs, top_k=15)

    print(f"\nTop 15 frequency components:")
    print(f"{'Rank':<6}{'Freq':<12}{'Period':<12}{'Power':<15}")
    print("-" * 45)

    peak_freqs = []
    for rank, (pwr, freq, idx) in enumerate(peaks, 1):
        period = 1/freq if freq > 0 else float('inf')
        print(f"{rank:<6}{freq:<12.6f}{period:<12.2f}{pwr:<15.2f}")
        peak_freqs.append(freq)

    # Check for harmonic structure
    print(f"\n--- Harmonic (Overtone) Structure Check ---")
    harmonics = check_harmonic_ratios(peak_freqs)

    if harmonics:
        for fundamental, harm_list in harmonics:
            period = 1/fundamental
            print(f"\nPotential fundamental: {fundamental:.6f} (period ≈ {period:.1f})")
            print(f"  Harmonics found: {[h[0] for h in harm_list]}")
    else:
        print("No clear harmonic structure detected in top peaks")

    # Analysis 2: Prime gaps
    print(f"\n{'='*60}")
    print("ANALYSIS 2: Prime Gap Spectrum")
    print("Gaps g_n = p_{n+1} - p_n")
    print("='*60")

    gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]

    # Pad to power of 2
    gap_len = 1
    while gap_len < len(gaps):
        gap_len *= 2
    gaps_padded = gaps + [0] * (gap_len - len(gaps))

    print(f"Gap sequence: {len(gaps)} values (padded to {gap_len})")
    print(f"Mean gap: {sum(gaps)/len(gaps):.2f}")
    print(f"Gap range: {min(gaps)} to {max(gaps)}")

    fft_gaps = fft(gaps_padded)
    power_gaps = power_spectrum(fft_gaps)
    freqs_gaps = [k/gap_len for k in range(gap_len)]

    peaks_gaps = find_peaks(power_gaps, freqs_gaps, top_k=10)

    print(f"\nTop 10 gap frequencies:")
    gap_peak_freqs = []
    for rank, (pwr, freq, idx) in enumerate(peaks_gaps, 1):
        period = 1/freq if freq > 0 else float('inf')
        print(f"{rank:<6}{freq:<12.6f}{period:<12.2f}{pwr:<15.2f}")
        gap_peak_freqs.append(freq)

    # Analysis 3: Primes AS frequencies (interference)
    print(f"\n{'='*60}")
    print("ANALYSIS 3: Primes as Frequencies - Interference Pattern")
    print("If each prime p is a frequency, what's the combined wave?")
    print("='*60")

    # Sum of cosines at prime frequencies
    N_SAMPLES = 1024
    t_max = 100
    signal = [0.0] * N_SAMPLES

    # Use first 30 primes as frequencies
    for p in primes[:30]:
        for i in range(N_SAMPLES):
            t = t_max * i / N_SAMPLES
            signal[i] += math.cos(2 * math.pi * p * t / 50)

    # Where does this combined signal peak? (constructive interference)
    peaks_signal = []
    for i in range(1, N_SAMPLES - 1):
        if signal[i] > signal[i-1] and signal[i] > signal[i+1]:
            t = t_max * i / N_SAMPLES
            peaks_signal.append((signal[i], t))

    peaks_signal.sort(reverse=True)

    print(f"\nTop constructive interference points:")
    print(f"(where prime-frequency waves align)")
    print(f"{'Rank':<6}{'t value':<12}{'Amplitude':<12}")
    print("-" * 30)
    for rank, (amp, t) in enumerate(peaks_signal[:10], 1):
        print(f"{rank:<6}{t:<12.4f}{amp:<12.2f}")

    # Analysis 4: Resonance - which intervals between primes recur?
    print(f"\n{'='*60}")
    print("ANALYSIS 4: Gap Resonances")
    print("Which prime gaps 'resonate' (appear most often)?")
    print("='*60")

    gap_counts = defaultdict(int)
    for g in gaps:
        gap_counts[g] += 1

    sorted_gaps = sorted(gap_counts.items(), key=lambda x: -x[1])

    print(f"\nMost common gaps (resonant intervals):")
    print(f"{'Gap':<8}{'Count':<10}{'Frequency':<12}")
    print("-" * 30)
    for gap, count in sorted_gaps[:15]:
        freq = count / len(gaps)
        print(f"{gap:<8}{count:<10}{freq:<12.4f}")

    # Check: are resonant gaps related by simple ratios?
    print(f"\n--- Gap Ratio Analysis ---")
    top_gaps = [g for g, c in sorted_gaps[:6]]
    print(f"Top gaps: {top_gaps}")

    print("Ratios between top gaps:")
    for i in range(len(top_gaps)):
        for j in range(i+1, len(top_gaps)):
            ratio = top_gaps[j] / top_gaps[i] if top_gaps[i] > 0 else 0
            print(f"  {top_gaps[j]}/{top_gaps[i]} = {ratio:.3f}")

    # Observation: gaps are often multiples of 6 (after 2,3)
    print(f"\n--- Gap mod 6 analysis ---")
    mod6_counts = defaultdict(int)
    for g in gaps:
        mod6_counts[g % 6] += 1
    print("Gap mod 6 distribution:")
    for m in range(6):
        print(f"  ≡{m} (mod 6): {mod6_counts[m]}")

    # Summary
    print(f"\n{'='*60}")
    print("SYNTHESIS: Primes as Spectral Operators")
    print("='*60")
    print("""
The CTA chain being explored:

  P(sound/overtones) ⊗ T_spec ⊗ P(light/prism) → P(primes)

Observations:
1. Prime indicator has frequency components - not pure noise
2. Prime gaps cluster at multiples of 6 (resonance!)
3. When primes ARE frequencies, they create interference patterns
4. The "combining" happens through arithmetic constraints

Key insight to develop:
- If primes are "fundamental frequencies" of integers
- Then composites are "chords" (products = frequency products)
- The prime decomposition is the "spectral decomposition"
- Zeta zeros might be the "overtones" of this system

Next: What's the "fundamental frequency" of the primes?
      What operator generates the overtone series?
""")

if __name__ == "__main__":
    prime_resonance_analysis()
