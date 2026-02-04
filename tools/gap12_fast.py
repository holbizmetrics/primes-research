#!/usr/bin/env python3
"""Fast search for length-12 gap arithmetic progressions using Miller-Rabin."""

def miller_rabin(n, witnesses=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]):
    """Deterministic Miller-Rabin for n < 3,317,044,064,679,887,385,961,981."""
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for a in witnesses:
        if a >= n: continue
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

def next_prime(n):
    n += 1
    if n <= 2: return 2
    if n % 2 == 0: n += 1
    while not miller_rabin(n):
        n += 2
    return n

def check_gap_ap(p):
    """Check if 12 consecutive primes starting at p form a gap AP."""
    primes = [p]
    for _ in range(11):
        primes.append(next_prime(primes[-1]))

    gaps = [primes[i+1] - primes[i] for i in range(11)]
    d = gaps[1] - gaps[0]

    for i in range(1, 10):
        if gaps[i+1] - gaps[i] != d:
            return False, None, None, None

    return True, primes, gaps, d

def search(start, count, report_every=500000):
    p = next_prime(start - 1)
    checked = 0
    found = 0

    print(f"Searching from {start:,} for {count:,} primes...", flush=True)

    while checked < count:
        ok, primes, gaps, d = check_gap_ap(p)
        if ok:
            found += 1
            print(f"\n*** FOUND #{found}: p={p} ***")
            print(f"  Primes: {primes}")
            print(f"  Gaps: {gaps}")
            print(f"  Common diff: {d}\n")

        checked += 1
        if checked % report_every == 0:
            print(f"Checked {checked:,} at p={p:,}", flush=True)

        p = next_prime(p)

    print(f"\nDone. Checked {checked:,}, found {found}.")
    return found

if __name__ == "__main__":
    search(10**12, 5_000_000, report_every=10_000)
