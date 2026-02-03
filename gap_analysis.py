#!/usr/bin/env python3
"""Compare prime gaps at prime indices vs composite indices."""

def sieve(n):
    """Sieve of Eratosthenes."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return is_prime

def main():
    # Generate primes up to a limit that gives us 100k primes
    # p_100000 ≈ 1.3 million
    limit = 1500000
    print(f"Sieving up to {limit}...")
    is_prime = sieve(limit)

    primes = [i for i in range(2, limit + 1) if is_prime[i]]
    print(f"Found {len(primes)} primes")

    # Compute gaps
    gaps = [primes[i+1] - primes[i] for i in range(len(primes) - 1)]

    # Separate by whether the INDEX is prime
    prime_set = set(primes)

    prime_idx_gaps = []  # gaps where the index n is prime
    comp_idx_gaps = []   # gaps where the index n is composite

    for n in range(2, min(100001, len(gaps))):
        if n in prime_set:
            prime_idx_gaps.append(gaps[n-1])  # gap at position n (0-indexed: n-1)
        else:
            comp_idx_gaps.append(gaps[n-1])

    print(f"\n=== Results for n from 2 to 100000 ===")
    print(f"Prime indices: count={len(prime_idx_gaps)}, avg_gap={sum(prime_idx_gaps)/len(prime_idx_gaps):.6f}")
    print(f"Composite idx: count={len(comp_idx_gaps)}, avg_gap={sum(comp_idx_gaps)/len(comp_idx_gaps):.6f}")

    ratio = (sum(prime_idx_gaps)/len(prime_idx_gaps)) / (sum(comp_idx_gaps)/len(comp_idx_gaps))
    print(f"Ratio (prime/comp): {ratio:.6f}")

    # Also check if this is statistically significant
    import statistics
    prime_std = statistics.stdev(prime_idx_gaps)
    comp_std = statistics.stdev(comp_idx_gaps)
    print(f"\nPrime indices: std={prime_std:.4f}")
    print(f"Composite idx: std={comp_std:.4f}")

    # Effect size
    pooled_std = ((prime_std**2 + comp_std**2) / 2) ** 0.5
    effect = (sum(comp_idx_gaps)/len(comp_idx_gaps) - sum(prime_idx_gaps)/len(prime_idx_gaps)) / pooled_std
    print(f"Effect size (Cohen's d): {effect:.4f}")

if __name__ == "__main__":
    main()
