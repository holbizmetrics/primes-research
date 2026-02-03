#!/usr/bin/env python3
"""Analyze patterns around twin primes."""

def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return is_prime

def main():
    limit = 10000000  # 10 million
    print(f"Sieving up to {limit}...")
    is_prime = sieve(limit)
    primes = [i for i in range(2, limit + 1) if is_prime[i]]
    print(f"Found {len(primes)} primes")

    gaps = [primes[i+1] - primes[i] for i in range(len(primes) - 1)]

    # Find twin primes (gap = 2)
    twin_indices = [i for i, g in enumerate(gaps) if g == 2]
    print(f"Found {len(twin_indices)} twin prime pairs")

    # Question 1: What's the gap AFTER a twin prime pair?
    # i.e., if gap[i] = 2, what's gap[i+1]?
    gaps_after_twin = [gaps[i+1] for i in twin_indices if i+1 < len(gaps)]

    print("\n=== Gaps immediately after twin primes ===")
    from collections import Counter
    after_counts = Counter(gaps_after_twin)
    print("Most common:")
    for gap, count in after_counts.most_common(10):
        pct = 100 * count / len(gaps_after_twin)
        print(f"  Gap {gap}: {count} times ({pct:.2f}%)")

    # Question 2: What's the gap BEFORE a twin prime pair?
    gaps_before_twin = [gaps[i-1] for i in twin_indices if i > 0]
    print("\n=== Gaps immediately before twin primes ===")
    before_counts = Counter(gaps_before_twin)
    print("Most common:")
    for gap, count in before_counts.most_common(10):
        pct = 100 * count / len(gaps_before_twin)
        print(f"  Gap {gap}: {count} times ({pct:.2f}%)")

    # Question 3: General gap distribution (for comparison)
    print("\n=== General gap distribution ===")
    all_counts = Counter(gaps)
    print("Most common:")
    for gap, count in all_counts.most_common(10):
        pct = 100 * count / len(gaps)
        print(f"  Gap {gap}: {count} times ({pct:.2f}%)")

    # Question 4: Average gap after twin vs average overall
    avg_after_twin = sum(gaps_after_twin) / len(gaps_after_twin)
    avg_overall = sum(gaps) / len(gaps)
    print(f"\n=== Averages ===")
    print(f"Average gap after twin: {avg_after_twin:.4f}")
    print(f"Average gap overall:    {avg_overall:.4f}")
    print(f"Ratio: {avg_after_twin/avg_overall:.4f}")

    # Question 5: Consecutive twin primes? (twin, gap, twin)
    # Pattern: gap=2, gap=X, gap=2
    consecutive_twins = []
    for i in range(len(gaps) - 2):
        if gaps[i] == 2 and gaps[i+2] == 2:
            consecutive_twins.append((primes[i], gaps[i+1], primes[i+3]))

    print(f"\n=== Consecutive twin prime pairs (twin-gap-twin) ===")
    print(f"Found {len(consecutive_twins)} instances")
    if len(consecutive_twins) > 0:
        middle_gaps = [t[1] for t in consecutive_twins]
        print(f"Middle gaps: {Counter(middle_gaps).most_common(10)}")
        print(f"First few examples:")
        for i, (p1, g, p2) in enumerate(consecutive_twins[:10]):
            print(f"  ({p1},{p1+2}) -- gap {g} -- ({p2},{p2+2})")

if __name__ == "__main__":
    main()
