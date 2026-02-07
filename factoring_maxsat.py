#!/usr/bin/env python3
"""
MAX-SAT Encoding for Factorization via onesFromPP
Given N and (possibly noisy) onesFromPP values, find p and q
"""

import random
from itertools import product

def is_prime(n, k=5):
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0: r += 1; d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def rand_prime(bits):
    while True:
        n = random.getrandbits(bits) | (1 << (bits-1)) | 1
        if is_prime(n): return n

def compute_ones_from_pp(p, q, bits):
    """Compute true onesFromPP values"""
    ones = []
    for k in range(2 * bits - 1):
        count = 0
        for i in range(bits):
            j = k - i
            if 0 <= j < bits:
                pi = (p >> i) & 1
                qj = (q >> j) & 1
                count += pi * qj
        ones.append(count)
    return ones

def add_noise(ones, error_rate=0.1):
    """Add ±1 noise to some values"""
    noisy = ones.copy()
    for i in range(len(noisy)):
        if random.random() < error_rate:
            delta = random.choice([-1, 1])
            noisy[i] = max(0, noisy[i] + delta)
    return noisy

def solve_maxsat_bruteforce(n, ones_pp, bits):
    """
    Brute-force MAX-SAT: find p, q that satisfy most constraints
    Only feasible for small bits (≤10)
    """
    best_p, best_q = None, None
    best_satisfied = -1

    # Constraints: p * q = n AND onesFromPP matches
    for p in range(1, 1 << bits, 2):  # odd only
        if n % p != 0:
            continue
        q = n // p
        if q >= (1 << bits) or q < (1 << (bits-1)):
            continue
        if q % 2 == 0:
            continue

        # Check onesFromPP constraints
        actual_ones = compute_ones_from_pp(p, q, bits)
        satisfied = sum(1 for a, b in zip(actual_ones, ones_pp) if a == b)

        if satisfied > best_satisfied:
            best_satisfied = satisfied
            best_p, best_q = p, q

    return best_p, best_q, best_satisfied, len(ones_pp)

def solve_maxsat_relaxed(n, ones_pp, bits, tolerance=1):
    """
    Relaxed MAX-SAT: allow ±tolerance in onesFromPP matching
    """
    best_p, best_q = None, None
    best_score = -1

    for p in range(1, 1 << bits, 2):
        if n % p != 0:
            continue
        q = n // p
        if q >= (1 << bits) or q < (1 << (bits-1)):
            continue
        if q % 2 == 0:
            continue

        actual_ones = compute_ones_from_pp(p, q, bits)
        # Score: count constraints satisfied within tolerance
        score = sum(1 for a, b in zip(actual_ones, ones_pp) if abs(a - b) <= tolerance)

        if score > best_score:
            best_score = score
            best_p, best_q = p, q

    return best_p, best_q, best_score, len(ones_pp)

def test_maxsat_factoring():
    print("=" * 60)
    print("MAX-SAT Factorization Test")
    print("=" * 60)
    print()

    for bits in [6, 8, 10]:
        print(f"--- {bits}-bit factors ---")

        successes_exact = 0
        successes_noisy = 0
        trials = 20 if bits <= 8 else 10

        for trial in range(trials):
            p = rand_prime(bits)
            q = rand_prime(bits)
            if p > q: p, q = q, p
            n = p * q

            # True onesFromPP
            ones_true = compute_ones_from_pp(p, q, bits)

            # Test with exact values
            found_p, found_q, sat, total = solve_maxsat_bruteforce(n, ones_true, bits)
            if found_p and found_q:
                if {found_p, found_q} == {p, q}:
                    successes_exact += 1

            # Test with 10% noise
            ones_noisy = add_noise(ones_true, 0.10)
            found_p, found_q, sat, total = solve_maxsat_relaxed(n, ones_noisy, bits, tolerance=1)
            if found_p and found_q:
                if {found_p, found_q} == {p, q}:
                    successes_noisy += 1

        print(f"  Exact onesFromPP:  {successes_exact}/{trials} ({100*successes_exact/trials:.0f}%)")
        print(f"  Noisy (10%, ±1):   {successes_noisy}/{trials} ({100*successes_noisy/trials:.0f}%)")
        print()

if __name__ == "__main__":
    test_maxsat_factoring()
