#!/usr/bin/env python3
"""
Prime Resonance v2: Primes as Global Combining Operators

User insight: "overtones creating resonance like light breaking or sounds combining"
              "primes as a global operator - they combine"

CTA transformation:
  P(overtones) ⊗ T_combine ⊗ T_spec → P(prime_structure)

What if primes are not just numbers but OPERATORS that combine?
Like how harmonics combine to make timbre, primes combine to make integers.
"""

import math
from collections import defaultdict

def sieve_primes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]

def prime_factorization(n, primes):
    """Get prime factorization as frequency spectrum."""
    if n < 2:
        return {}
    factors = {}
    for p in primes:
        if p * p > n:
            break
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def factorization_spectrum(n, primes, max_prime=50):
    """
    Represent n as a "spectrum" over primes.
    Like a sound spectrum: amplitude at each frequency (prime).
    """
    factors = prime_factorization(n, primes)
    spectrum = [0] * max_prime
    for p, exp in factors.items():
        if p < max_prime:
            spectrum[p] = exp
    return spectrum

def spectral_distance(spec1, spec2):
    """Euclidean distance between two prime spectra."""
    return math.sqrt(sum((a-b)**2 for a,b in zip(spec1, spec2)))

def spectral_inner_product(spec1, spec2):
    """Inner product of spectra - measures harmonic similarity."""
    return sum(a*b for a,b in zip(spec1, spec2))

def prime_interference_pattern(primes, n_range=1000):
    """
    When we "play" all primes as frequencies, where do they constructively interfere?

    If prime p is a "frequency", then:
    - Multiples of p are "resonance points"
    - Numbers with many small prime factors = high resonance
    - Primes themselves = anti-resonance (only self-interference)
    """
    resonance = [0.0] * n_range

    # Each prime contributes amplitude at its multiples
    for p in primes:
        if p >= n_range:
            break
        amplitude = 1.0 / math.log(p)  # Larger primes = weaker contribution
        for multiple in range(p, n_range, p):
            resonance[multiple] += amplitude

    return resonance

def find_resonance_peaks(resonance, top_k=20):
    """Find numbers with highest resonance (highly composite-like)."""
    indexed = [(resonance[i], i) for i in range(2, len(resonance))]
    indexed.sort(reverse=True)
    return indexed[:top_k]

def prime_as_operator():
    """
    Key insight: Prime p acts as an OPERATOR on integers.

    The "multiplication by p" operator:
    - Maps n → p*n
    - In log space: log(n) → log(n) + log(p)
    - This is a TRANSLATION operator!

    So primes are translation operators in log-space.
    The integers are the "orbit" under these operators.
    """
    print("=" * 60)
    print("PRIMES AS OPERATORS")
    print("=" * 60)
    print("""
In music: a frequency f has harmonics at 2f, 3f, 4f, ...
          This is multiplication!

In number theory: prime p generates multiples p, 2p, 3p, ...
                  This is also multiplication!

Key mapping:
  - Musical frequency f ↔ Prime p
  - Harmonic nf ↔ Multiple np
  - Timbre (harmonic spectrum) ↔ Factorization spectrum
  - Chord (multiple frequencies) ↔ Product of primes

The INVERSE operation:
  - Music: Fourier analysis decomposes sound → frequencies
  - Numbers: Factorization decomposes integer → primes

PRIMES ARE THE FOURIER BASIS OF MULTIPLICATION!
""")

def analyze_prime_operators():
    print("=" * 60)
    print("PRIME RESONANCE ANALYSIS v2")
    print("=" * 60)
    print()

    LIMIT = 1000
    primes = sieve_primes(LIMIT)
    print(f"Working with primes up to {LIMIT}")

    # Analysis 1: Factorization as spectrum
    print("\n" + "="*60)
    print("ANALYSIS 1: Numbers as Prime Spectra")
    print("="*60)

    examples = [12, 30, 60, 72, 100, 360, 420, 840]
    print("\nHighly composite numbers as 'rich' spectra:")
    print(f"{'n':<8}{'Factorization':<25}{'Spectrum (2,3,5,7,11)':<30}")
    print("-" * 60)

    for n in examples:
        factors = prime_factorization(n, primes)
        factor_str = " × ".join(f"{p}^{e}" if e > 1 else str(p) for p,e in sorted(factors.items()))
        spec = factorization_spectrum(n, primes, 13)
        spec_str = str([spec[p] for p in [2,3,5,7,11]])
        print(f"{n:<8}{factor_str:<25}{spec_str:<30}")

    # Analysis 2: Spectral similarity
    print("\n" + "="*60)
    print("ANALYSIS 2: Spectral Similarity Between Numbers")
    print("="*60)
    print("\nWhich numbers 'sound alike' (similar factorization spectrum)?")

    # Compare some numbers
    test_pairs = [(12, 18), (12, 20), (30, 42), (60, 84), (100, 144)]
    print(f"\n{'Pair':<15}{'Spectra':<40}{'Distance':<10}")
    print("-" * 65)

    for a, b in test_pairs:
        spec_a = factorization_spectrum(a, primes, 15)
        spec_b = factorization_spectrum(b, primes, 15)
        dist = spectral_distance(spec_a, spec_b)
        print(f"({a}, {b}){'':<7}{str(spec_a[2:8]):<20}{str(spec_b[2:8]):<20}{dist:<10.3f}")

    # Analysis 3: Resonance pattern
    print("\n" + "="*60)
    print("ANALYSIS 3: Resonance Pattern")
    print("="*60)
    print("\nIf each prime p emits 'signal' at multiples, where is resonance highest?")

    resonance = prime_interference_pattern(primes, 500)
    peaks = find_resonance_peaks(resonance, 20)

    print(f"\nTop 20 resonance points (like anti-nodes in standing wave):")
    print(f"{'Rank':<6}{'n':<8}{'Resonance':<12}{'Factorization':<25}")
    print("-" * 50)

    for rank, (res, n) in enumerate(peaks, 1):
        factors = prime_factorization(n, primes)
        factor_str = " × ".join(f"{p}^{e}" if e > 1 else str(p) for p,e in sorted(factors.items()))
        print(f"{rank:<6}{n:<8}{res:<12.3f}{factor_str:<25}")

    # Check: are these highly composite numbers?
    print("\n→ High resonance points are numbers with MANY small prime factors")
    print("→ Primes have LOW resonance (only self-interference)")

    # Analysis 4: Prime anti-resonance
    print("\n" + "="*60)
    print("ANALYSIS 4: Primes as Anti-Resonance Points")
    print("="*60)

    # Primes should have minimal resonance
    prime_resonances = [(resonance[p], p) for p in primes if p < 500]
    prime_resonances.sort()

    print("\nLowest resonance numbers (should be primes!):")
    lowest = sorted([(resonance[n], n) for n in range(2, 500)])[:20]
    for res, n in lowest:
        is_p = "PRIME" if n in primes else ""
        print(f"  n={n}: resonance={res:.3f} {is_p}")

    # Analysis 5: The "primordial spectrum"
    print("\n" + "="*60)
    print("ANALYSIS 5: The Primordial Spectrum")
    print("="*60)
    print("""
If we think of the sequence of primes as a "signal":
  2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, ...

The GAPS between primes form an oscillation:
  1, 2, 2, 4, 2, 4, 2, 4, 6, 2, 6, ...

This oscillation has a dominant "period" of 6 (mod 6 structure).

The zeta zeros are the FREQUENCIES of this oscillation!
Riemann: ψ(x) = x - Σ_ρ x^ρ/ρ - ...

The zeros ρ are literally the spectral decomposition of prime counting!
""")

    # Operator interpretation
    prime_as_operator()

    # Synthesis
    print("\n" + "="*60)
    print("SYNTHESIS: CTA Chain")
    print("="*60)
    print("""
Your transformation chain:

  P(overtones/harmonics)
    ⊗ T_inv (invert: decomposition → composition)
    ⊗ T_mrg (merge: frequencies → single sound)
  → P(musical_timbre)

  T_spec: apply to integers

  → P(prime_structure):
    - Primes = fundamental frequencies
    - Factorization = spectral decomposition
    - Highly composite = rich timbre (many harmonics)
    - Primes = pure tones (single frequency)

The GLOBAL OPERATOR aspect:
  - Each prime p defines a translation: log(n) → log(n) + log(p)
  - Together they generate all positive integers
  - The structure comes from how they COMBINE (multiplicatively)
  - Zeta zeros = eigenfrequencies of this system

Next steps:
  1. What's the "timbre" that distinguishes integer sequences?
  2. Can we find the "fundamental" that generates the prime gaps?
  3. How do zeta zeros relate to this spectral picture?
""")

if __name__ == "__main__":
    analyze_prime_operators()
