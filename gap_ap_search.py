#!/usr/bin/env python3
"""Search for gap arithmetic progressions in primes."""

def sieve(n):
    """Simple sieve of Eratosthenes."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

def find_gap_ap(primes, min_len=6):
    """Find gap APs of length >= min_len."""
    results = []
    gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]

    for start in range(len(gaps) - min_len):
        d = gaps[start + 1] - gaps[start]
        if d == 0:
            continue
        length = 1
        for j in range(start + 1, len(gaps) - 1):
            if gaps[j + 1] - gaps[j] == d:
                length += 1
            else:
                break
        if length >= min_len:
            results.append((primes[start], length + 1, gaps[start:start+length+1], d))

    return results

print("Sieving primes up to 10^8...")
primes = sieve(10**8)
print(f"Found {len(primes)} primes")

print("\nSearching for gap APs of length >= 6...")
best = 0
for i in range(0, len(primes) - 20, 1000):
    chunk = primes[i:i+100]
    results = find_gap_ap(chunk, min_len=6)
    for p, length, gaps, d in results:
        if length > best:
            best = length
            print(f"NEW BEST: length {length} at p={p}")
            print(f"  Gaps: {gaps}")
            print(f"  Common diff: {d}")

print(f"\nBest found: length {best}")
