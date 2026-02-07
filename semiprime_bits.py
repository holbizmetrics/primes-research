#!/usr/bin/env python3
"""
Semiprime Bit Pattern Analysis
Testing if bit patterns in n = p*q reveal structure about p, q
"""

import random
from math import gcd, log2, floor
from collections import defaultdict

def is_prime(n, k=10):
    """Miller-Rabin primality test"""
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def random_prime(bits):
    """Generate random prime with given bit length"""
    while True:
        n = random.getrandbits(bits) | (1 << (bits-1)) | 1  # Ensure top bit set and odd
        if is_prime(n):
            return n

def get_bits(n, num_bits=None):
    """Get bit representation as list (LSB first)"""
    if num_bits is None:
        num_bits = n.bit_length()
    return [(n >> i) & 1 for i in range(num_bits)]

def analyze_semiprimes(prime_bits=32, num_samples=1000):
    """Analyze bit patterns in semiprimes"""

    print(f"=== Semiprime Bit Pattern Analysis ===")
    print(f"Prime size: {prime_bits} bits")
    print(f"Samples: {num_samples}")
    print()

    semiprime_bits = 2 * prime_bits

    # Collect data
    semiprimes = []
    factors = []

    print("Generating semiprimes...")
    for i in range(num_samples):
        p = random_prime(prime_bits)
        q = random_prime(prime_bits)
        n = p * q
        semiprimes.append(n)
        factors.append((p, q))
        if (i + 1) % 200 == 0:
            print(f"  {i+1}/{num_samples}")

    # Analysis 1: Bit frequency at each position
    print("\n--- Bit Frequency by Position ---")
    bit_counts = defaultdict(int)
    for n in semiprimes:
        bits = get_bits(n, semiprime_bits)
        for i, b in enumerate(bits):
            bit_counts[i] += b

    print("Position | Frequency | Deviation from 0.5")
    print("-" * 45)
    deviations = []
    for i in range(semiprime_bits):
        freq = bit_counts[i] / num_samples
        dev = freq - 0.5
        deviations.append(abs(dev))
        if i < 5 or i >= semiprime_bits - 5 or abs(dev) > 0.05:
            print(f"  {i:3d}     |   {freq:.4f}  |  {dev:+.4f} {'*' if abs(dev) > 0.05 else ''}")

    avg_dev = sum(deviations) / len(deviations)
    max_dev = max(deviations)
    print(f"\nAverage |deviation|: {avg_dev:.4f}")
    print(f"Max |deviation|: {max_dev:.4f} at position {deviations.index(max_dev)}")

    # Analysis 2: Compare to random odd numbers
    print("\n--- Comparison to Random Odd Numbers ---")
    random_bit_counts = defaultdict(int)
    for _ in range(num_samples):
        # Random odd number of similar size
        r = random.getrandbits(semiprime_bits) | 1
        bits = get_bits(r, semiprime_bits)
        for i, b in enumerate(bits):
            random_bit_counts[i] += b

    diff_sum = 0
    significant_diffs = []
    for i in range(semiprime_bits):
        semi_freq = bit_counts[i] / num_samples
        rand_freq = random_bit_counts[i] / num_samples
        diff = abs(semi_freq - rand_freq)
        diff_sum += diff
        if diff > 0.03:
            significant_diffs.append((i, semi_freq, rand_freq, diff))

    print(f"Average frequency difference: {diff_sum/semiprime_bits:.4f}")
    if significant_diffs:
        print("Significant differences (>0.03):")
        for pos, sf, rf, d in significant_diffs[:10]:
            print(f"  Position {pos}: semiprime={sf:.3f}, random={rf:.3f}, diff={d:.3f}")
    else:
        print("No significant differences found.")

    # Analysis 3: Bit correlations
    print("\n--- Bit Correlations ---")
    # Check if certain bit pairs are correlated
    correlations = []
    test_pairs = [(0, 1), (0, 2), (1, 2), (0, prime_bits),
                  (prime_bits-1, prime_bits), (prime_bits-1, prime_bits+1)]

    for i, j in test_pairs:
        if j >= semiprime_bits:
            continue
        count_both = 0
        count_i = 0
        count_j = 0
        for n in semiprimes:
            bi = (n >> i) & 1
            bj = (n >> j) & 1
            count_i += bi
            count_j += bj
            count_both += bi & bj

        # Expected if independent: P(i)*P(j)
        pi = count_i / num_samples
        pj = count_j / num_samples
        expected = pi * pj
        actual = count_both / num_samples
        correlation = actual - expected
        correlations.append((i, j, correlation))
        print(f"  Bits ({i}, {j}): corr = {correlation:+.4f}")

    # Analysis 4: LSB patterns (always interesting for odd primes)
    print("\n--- LSB Analysis ---")
    lsb_patterns = defaultdict(int)
    for n in semiprimes:
        pattern = n & 0b1111  # Last 4 bits
        lsb_patterns[pattern] += 1

    print("Last 4 bits distribution (semiprimes are always odd):")
    for pattern in sorted(lsb_patterns.keys()):
        if pattern % 2 == 1:  # Only odd
            count = lsb_patterns[pattern]
            expected = num_samples / 8  # 8 odd patterns
            ratio = count / expected
            print(f"  {pattern:04b} ({pattern:2d}): {count:4d} (ratio to expected: {ratio:.2f})")

    # Analysis 5: Relationship between factor bits and product bits
    print("\n--- Factor Bit → Product Bit Correlation ---")
    print("Testing if bit k of p predicts bit k of n:")

    for k in [0, 1, 2, prime_bits//2, prime_bits-2, prime_bits-1]:
        matches = 0
        for n, (p, q) in zip(semiprimes, factors):
            p_bit = (p >> k) & 1
            n_bit = (n >> k) & 1
            if p_bit == n_bit:
                matches += 1
        match_rate = matches / num_samples
        print(f"  Bit {k:2d}: p[k]==n[k] in {match_rate:.1%} (random would be 50%)")

    # Analysis 6: MSB region
    print("\n--- MSB Region Analysis ---")
    print("High bits of n vs high bits of p*q approximation:")
    msb_matches = 0
    for n, (p, q) in zip(semiprimes, factors):
        # Top 4 bits
        n_top = n >> (semiprime_bits - 4)
        pq_approx_top = (p >> (prime_bits - 2)) * (q >> (prime_bits - 2))
        # They should be related
        if abs(n_top - pq_approx_top) <= 2:
            msb_matches += 1
    print(f"  MSB approximation holds: {msb_matches/num_samples:.1%}")

    # Analysis 7: Hamming weight
    print("\n--- Hamming Weight (number of 1-bits) ---")
    semi_weights = [bin(n).count('1') for n in semiprimes]
    rand_weights = [bin(random.getrandbits(semiprime_bits) | 1).count('1')
                    for _ in range(num_samples)]

    semi_avg = sum(semi_weights) / num_samples
    rand_avg = sum(rand_weights) / num_samples
    expected = semiprime_bits / 2

    print(f"  Semiprime average: {semi_avg:.2f}")
    print(f"  Random average: {rand_avg:.2f}")
    print(f"  Expected (uniform): {expected:.2f}")
    print(f"  Semiprime deviation: {semi_avg - expected:+.2f}")

    print("\n=== Analysis Complete ===")

if __name__ == "__main__":
    # Run with different prime sizes
    analyze_semiprimes(prime_bits=32, num_samples=1000)
    print("\n" + "="*60 + "\n")
    analyze_semiprimes(prime_bits=64, num_samples=500)
