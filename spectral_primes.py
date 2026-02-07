#!/usr/bin/env python3
"""
Spectral Analysis of Primes - Exploring overtone/resonance structure
CTA approach: P(sound/overtones) ⊗ T_spec → P(primes)

What happens when we treat primes as a signal and decompose into frequencies?
"""

import numpy as np
import math

def sieve_primes(limit):
    """Generate primes up to limit using Sieve of Eratosthenes."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]

def prime_indicator(limit):
    """Create prime indicator function: χ(n) = 1 if prime, 0 otherwise."""
    primes = set(sieve_primes(limit))
    return np.array([1 if n in primes else 0 for n in range(limit)])

def prime_gaps(primes):
    """Compute sequence of prime gaps."""
    return np.array([primes[i+1] - primes[i] for i in range(len(primes)-1)])

def analyze_spectrum(signal, name, top_k=10):
    """
    Compute FFT and analyze dominant frequencies.
    """
    n = len(signal)

    # FFT
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(n)

    # Power spectrum (magnitude squared)
    power = np.abs(fft)**2

    # Only positive frequencies (spectrum is symmetric for real signals)
    positive_mask = freqs > 0
    pos_freqs = freqs[positive_mask]
    pos_power = power[positive_mask]

    # Find dominant frequencies
    top_indices = np.argsort(pos_power)[-top_k:][::-1]

    print(f"\n{'='*60}")
    print(f"Spectral Analysis: {name}")
    print(f"{'='*60}")
    print(f"Signal length: {n}")
    print(f"Total power: {np.sum(power):.2f}")
    print(f"\nTop {top_k} frequency components:")
    print(f"{'Rank':<6}{'Frequency':<15}{'Period':<15}{'Power':<15}{'% Total':<10}")
    print("-" * 60)

    for rank, idx in enumerate(top_indices, 1):
        freq = pos_freqs[idx]
        period = 1/freq if freq > 0 else float('inf')
        pwr = pos_power[idx]
        pct = 100 * pwr / np.sum(power)
        print(f"{rank:<6}{freq:<15.6f}{period:<15.2f}{pwr:<15.2f}{pct:<10.2f}")

    return pos_freqs, pos_power

def find_resonances(power, freqs, threshold_factor=3):
    """
    Find resonance peaks - frequencies with power significantly above average.
    """
    mean_power = np.mean(power)
    std_power = np.std(power)
    threshold = mean_power + threshold_factor * std_power

    resonance_mask = power > threshold
    resonance_freqs = freqs[resonance_mask]
    resonance_powers = power[resonance_mask]

    return resonance_freqs, resonance_powers, threshold

def analyze_overtone_structure(freqs, powers, fundamental_candidates=5):
    """
    Check if frequency peaks show overtone structure (integer ratios).
    Like harmonics in music: f, 2f, 3f, 4f, ...
    """
    print(f"\n--- Overtone Structure Analysis ---")

    # Get top frequencies by power
    top_indices = np.argsort(powers)[-20:][::-1]
    top_freqs = freqs[top_indices]
    top_powers = powers[top_indices]

    # Check each candidate as potential fundamental
    for i in range(min(fundamental_candidates, len(top_freqs))):
        fundamental = top_freqs[i]
        if fundamental < 1e-10:
            continue

        print(f"\nIf fundamental = {fundamental:.6f} (period = {1/fundamental:.2f}):")

        # Check for harmonics
        harmonics_found = []
        for j, freq in enumerate(top_freqs):
            if freq < 1e-10:
                continue
            ratio = freq / fundamental
            # Check if ratio is close to an integer
            nearest_int = round(ratio)
            if nearest_int > 0 and abs(ratio - nearest_int) < 0.05:
                harmonics_found.append((nearest_int, freq, top_powers[j]))

        if len(harmonics_found) > 2:
            print(f"  Harmonics detected: {[h[0] for h in harmonics_found]}")
            for h_num, h_freq, h_power in harmonics_found[:5]:
                print(f"    {h_num}x: freq={h_freq:.6f}, power={h_power:.2f}")

def spectral_entropy(power):
    """
    Compute spectral entropy - measure of how "spread out" the spectrum is.
    Low entropy = concentrated in few frequencies (like pure tones)
    High entropy = spread across many frequencies (like noise)
    """
    # Normalize to probability distribution
    p = power / np.sum(power)
    p = p[p > 0]  # Remove zeros for log
    entropy = -np.sum(p * np.log2(p))
    max_entropy = np.log2(len(power))
    normalized_entropy = entropy / max_entropy

    return entropy, normalized_entropy

def main():
    print("=" * 60)
    print("SPECTRAL ANALYSIS OF PRIMES")
    print("Exploring overtone/resonance structure via FFT")
    print("=" * 60)

    # Parameters
    LIMIT = 10000

    # Generate primes
    primes = sieve_primes(LIMIT)
    print(f"\nGenerated {len(primes)} primes up to {LIMIT}")

    # Analysis 1: Prime indicator function χ(n)
    print("\n" + "="*60)
    print("ANALYSIS 1: Prime Indicator Function")
    print("χ(n) = 1 if n is prime, 0 otherwise")
    print("="*60)

    indicator = prime_indicator(LIMIT)
    freqs1, power1 = analyze_spectrum(indicator, "Prime Indicator χ(n)")

    # Resonances
    res_freqs, res_powers, threshold = find_resonances(power1, freqs1)
    print(f"\nResonances (power > {threshold:.2f}): {len(res_freqs)} found")

    # Spectral entropy
    entropy, norm_entropy = spectral_entropy(power1)
    print(f"Spectral entropy: {entropy:.2f} bits (normalized: {norm_entropy:.3f})")

    # Overtone structure
    analyze_overtone_structure(freqs1, power1)

    # Analysis 2: Prime gaps
    print("\n" + "="*60)
    print("ANALYSIS 2: Prime Gap Sequence")
    print("g_n = p_{n+1} - p_n")
    print("="*60)

    gaps = prime_gaps(primes)
    print(f"Gap sequence length: {len(gaps)}")
    print(f"Mean gap: {np.mean(gaps):.2f}")
    print(f"Gap range: {np.min(gaps)} to {np.max(gaps)}")

    freqs2, power2 = analyze_spectrum(gaps, "Prime Gaps")

    # Resonances in gaps
    res_freqs2, res_powers2, threshold2 = find_resonances(power2, freqs2)
    print(f"\nResonances (power > {threshold2:.2f}): {len(res_freqs2)} found")

    # Spectral entropy
    entropy2, norm_entropy2 = spectral_entropy(power2)
    print(f"Spectral entropy: {entropy2:.2f} bits (normalized: {norm_entropy2:.3f})")

    # Overtone structure
    analyze_overtone_structure(freqs2, power2)

    # Analysis 3: Log-weighted prime signal
    print("\n" + "="*60)
    print("ANALYSIS 3: Log-Weighted Prime Signal")
    print("Λ(n) = log(p) if n=p^k, 0 otherwise (von Mangoldt)")
    print("="*60)

    # Simplified: just log(p) at prime positions
    log_signal = np.zeros(LIMIT)
    for p in primes:
        if p < LIMIT:
            log_signal[p] = np.log(p)

    freqs3, power3 = analyze_spectrum(log_signal, "Log-weighted primes")
    analyze_overtone_structure(freqs3, power3)

    # Analysis 4: Prime-to-prime intervals in "frequency" space
    print("\n" + "="*60)
    print("ANALYSIS 4: Primes as Frequencies")
    print("What if primes ARE the frequencies? Interference pattern?")
    print("="*60)

    # Create a signal that's sum of sinusoids at prime frequencies
    t = np.linspace(0, 10, 10000)  # Time axis
    signal = np.zeros_like(t)

    # Use first 50 primes as frequencies (scaled)
    for p in primes[:50]:
        signal += np.sin(2 * np.pi * p * t / 100)  # Scale primes to reasonable freq

    freqs4, power4 = analyze_spectrum(signal, "Sum of prime-frequency sinusoids")

    print("\n" + "="*60)
    print("OBSERVATIONS")
    print("="*60)

    print("""
Key questions from spectral analysis:

1. Do prime gaps show periodic structure?
   - If dominant frequencies exist, primes have hidden rhythm

2. Is there overtone (harmonic) structure?
   - Would suggest fundamental "prime frequency" with harmonics

3. How does spectral entropy compare to random?
   - Low entropy = structured, high = noise-like

4. What happens when primes ARE the frequencies?
   - Interference patterns might reveal relationships

Next: Compare to null hypothesis (random primes, shuffled gaps)
""")

if __name__ == "__main__":
    main()
