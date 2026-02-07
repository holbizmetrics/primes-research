#!/usr/bin/env python3
"""
Search for gap APs with d=30 (primorial hierarchy test)
Prediction: d=30 gap APs should appear around ~10^7 primes
"""

import numpy as np
from math import isqrt

def sieve_primes(limit):
    """Sieve of Eratosthenes"""
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0:2] = False
    for i in range(2, isqrt(limit) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return np.nonzero(is_prime)[0]

def find_gap_aps(primes, target_d, min_length=5):
    """Find arithmetic progressions in consecutive gaps with difference d"""
    gaps = np.diff(primes)
    n = len(gaps)
    results = []

    i = 0
    while i < n - min_length + 1:
        # Check if gaps starting at i form an AP with difference target_d or -target_d
        for d in [target_d, -target_d]:
            length = 1
            j = i
            while j + 1 < n:
                if gaps[j + 1] - gaps[j] == d:
                    length += 1
                    j += 1
                else:
                    break

            if length >= min_length:
                gap_seq = gaps[i:i+length].tolist()
                prime_idx = i
                prime_start = int(primes[i])
                results.append({
                    'length': length,
                    'd': d,
                    'prime_idx': prime_idx,
                    'prime_start': prime_start,
                    'gaps': gap_seq,
                    'primes': [int(p) for p in primes[i:i+length+1]]
                })
        i += 1

    return results

def main():
    print("Gap AP Search: d=30 (Primorial Hierarchy Test)")
    print("=" * 55)
    print()

    # Search in stages
    stages = [
        (10**6, "10^6"),
        (5 * 10**6, "5×10^6"),
        (10**7, "10^7"),
        (2 * 10**7, "2×10^7"),
        (5 * 10**7, "5×10^7"),
    ]

    all_results = []

    for limit, label in stages:
        print(f"Searching primes up to {label} ({limit:,})...")
        primes = sieve_primes(limit)
        n_primes = len(primes)
        print(f"  {n_primes:,} primes found")

        # Search for d=30 gap APs of length 5+
        results = find_gap_aps(primes, target_d=30, min_length=5)
        new_results = [r for r in results if r not in all_results]

        if new_results:
            print(f"  ✓ Found {len(new_results)} new gap APs with |d|=30!")
            for r in new_results:
                print(f"    L{r['length']}: p={r['prime_start']:,}, d={r['d']}, gaps={r['gaps'][:6]}...")
                # Check residue class mod 30
                mod30 = r['prime_start'] % 30
                mod6 = r['prime_start'] % 6
                print(f"         p ≡ {mod30} (mod 30), p ≡ {mod6} (mod 6)")
            all_results.extend(new_results)
        else:
            print(f"  No new d=30 gap APs found at this stage")
        print()

    print("=" * 55)
    print(f"TOTAL: {len(all_results)} gap APs with |d|=30 found")
    print()

    if all_results:
        print("Summary:")
        for r in all_results:
            print(f"  L{r['length']}: p={r['prime_start']:,}, d={r['d']}")
            print(f"       gaps: {r['gaps']}")
            print(f"       p mod 30 = {r['prime_start'] % 30}")
            print()

        # Check if d=30 primes are ≡ 1 mod 30 (like d=6 was ≡ 1 mod 6)
        print("Residue class analysis:")
        for r in all_results:
            mods = [p % 30 for p in r['primes']]
            print(f"  L{r['length']}: primes mod 30 = {mods}")
    else:
        print("No d=30 gap APs found in range.")
        print("Prediction may need larger range or lower length threshold.")

        # Try length 4 as fallback
        print("\nTrying L4 (length 4) as fallback...")
        primes = sieve_primes(5 * 10**7)
        results_l4 = find_gap_aps(primes, target_d=30, min_length=4)
        if results_l4:
            print(f"Found {len(results_l4)} L4 gap APs with |d|=30:")
            for r in results_l4[:10]:  # Show first 10
                print(f"  p={r['prime_start']:,}, gaps={r['gaps']}")

if __name__ == "__main__":
    main()
