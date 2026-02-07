#!/usr/bin/env python3
"""STRIKE 12-14: The gap between rotation enrichment and sieve prediction.
And: is there ANYTHING beyond the sieve effect?

Strike 10 showed: coprime-to-M_k enrichment matches product(fi/(fi-1)) exactly.
But rotation enrichment is LOWER. Why?

Hypothesis: rotation can map a k-bit number OUTSIDE [2^{k-1}, 2^k-1].
When 2p mod M_k < 2^{k-1}, the rotated value loses its MSB and falls
out of range. This reduces the count.
"""
import math

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return s

N=131072; is_p=sieve(N)

def bit_rotate(n, d, w):
    d = d % w
    return ((n << d) | (n >> (w - d))) & ((1 << w) - 1)

def distinct_prime_factors(n):
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0: factors.add(d); n //= d
        d += 1
    if n > 1: factors.add(n)
    return sorted(factors)

# STRIKE 12: Out-of-range rate after rotation
print("=== STRIKE 12: How often does rotation leave k-bit range? ===")
print()

for k in range(8, 17):
    lo = 1<<(k-1); hi = (1<<k)-1
    Mk = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]
    in_range = 0; out_range = 0
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi:
            in_range += 1
        else:
            out_range += 1
    print("k=%2d: %d primes, %d stay in range (%.1f%%), %d leave (%.1f%%)" % (
        k, len(prm), in_range, 100*in_range/len(prm), out_range, 100*out_range/len(prm)))

print()

# STRIKE 13: Corrected enrichment — only count primes that stay in range
print("=== STRIKE 13: Corrected enrichment (in-range only) ===")
print("Compare: actual rotation vs sieve prediction vs corrected")
print()

for k in range(8, 17):
    lo = 1<<(k-1); hi = (1<<k)-1
    Mk = (1<<k)-1
    factors = distinct_prime_factors(Mk)
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    # Count: rotated prime that's in range and also prime
    rot_prime = 0
    rot_in_range = 0
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi:
            rot_in_range += 1
            if r <= N and is_p[r]:
                rot_prime += 1

    # Enrichment A: as before (count / expected from all primes)
    density = len(prm) / (hi - lo + 1)
    expected_all = len(prm) * density
    enrich_all = rot_prime / expected_all if expected_all > 0 else 0

    # Enrichment B: count / expected from in-range rotations only
    expected_inrange = rot_in_range * density
    enrich_inrange = rot_prime / expected_inrange if expected_inrange > 0 else 0

    # Sieve prediction
    sieve_pred = math.prod(f/(f-1) for f in factors)

    print("k=%2d: raw=%.3f  corrected=%.3f  sieve=%.3f  corr/sieve=%.3f" % (
        k, enrich_all, enrich_inrange, sieve_pred, enrich_inrange/sieve_pred if sieve_pred > 0 else 0))

print()
print("If corrected ~ sieve: the ENTIRE enrichment is from sieve preservation.")
print("If corrected > sieve: there's something BEYOND the sieve.")
print()

# STRIKE 14: The residual — what's left after removing sieve effect?
# If we take k-bit primes, compute 2p mod M_k, keep only in-range,
# and compare to random coprime-to-M_k numbers:
# Is the primality rate STILL enhanced?
print("=== STRIKE 14: Beyond the sieve — residual enrichment ===")
print()

for k in [10, 12, 14, 16]:
    lo = 1<<(k-1); hi = (1<<k)-1
    Mk = (1<<k)-1
    factors = distinct_prime_factors(Mk)
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    # Rotated primes that stay in range
    rotated_vals = []
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi:
            rotated_vals.append(r)

    # Prime rate among rotated values
    rate_rot = sum(1 for r in rotated_vals if is_p[r]) / len(rotated_vals) if rotated_vals else 0

    # Prime rate among ALL coprime-to-M_k odd numbers in range
    cop = [n for n in range(lo|1, hi+1, 2) if all(n % f != 0 for f in factors)]
    rate_cop = sum(1 for n in cop if is_p[n]) / len(cop) if cop else 0

    # Residual: how much more prime are rotated-primes vs random-coprime?
    residual = rate_rot / rate_cop if rate_cop > 0 else 0

    print("k=%2d: rate(rotated primes)=%.4f  rate(random coprime)=%.4f  residual=%.3f" % (
        k, rate_rot, rate_cop, residual))

print()
print("Residual > 1 means: rotated primes are MORE likely prime than")
print("random coprime-to-M_k numbers. That would be a REAL signal beyond sieve.")
print("Residual ≈ 1 means: the entire effect is explained by sieve preservation.")
print()

# STRIKE 14b: What if we don't restrict to k-bit range?
# Let rotation wrap freely: 2p mod M_k can be anywhere in [1, M_k-1].
# Is 2p mod M_k prime at an enhanced rate?
print("=== STRIKE 14b: Unrestricted rotation (ignore k-bit constraint) ===")
print()

for k in [10, 12, 14, 16]:
    Mk = (1<<k)-1
    lo = 1<<(k-1); hi = (1<<k)-1
    factors = distinct_prime_factors(Mk)
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    # 2p mod M_k for all primes
    rotated = [(2*p) % Mk for p in prm]
    rate_rot = sum(1 for r in rotated if 1 < r <= N and is_p[r]) / len(rotated)

    # Expected: prime density in [1, M_k]
    primes_in_Mk = sum(1 for n in range(2, min(Mk+1, N+1)) if is_p[n])
    rate_all = primes_in_Mk / Mk

    # Coprime expected rate
    cop_rate = rate_all * math.prod(f/(f-1) for f in factors)

    print("k=%2d: rate(2p mod M_k)=%.4f  rate(all)=%.4f  sieve_pred_rate=%.4f  ratio_to_sieve=%.3f" % (
        k, rate_rot, rate_all, cop_rate, rate_rot/cop_rate if cop_rate > 0 else 0))
