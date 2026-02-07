#!/usr/bin/env python3
"""STRIKE 24-26: The full decomposition and what's genuinely new.

We've shown the bit rotation enrichment decomposes into:
1. Sieve preservation: coprimality to factors of M_k (exact prediction)
2. Parity preservation: x2 mod M_k always gives odd output (x2 advantage)
3. Proximity: maps large primes to values near small primes

Now: is there a RESIDUAL beyond these three effects?
And: does this connect to anything known about Mersenne structure?

STRIKE 24: Full decomposition with all corrections
STRIKE 25: Do rotation-surviving primes cluster in residue classes?
STRIKE 26: Convergence — does enrichment stabilize as k → ∞?
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

# STRIKE 24: Full decomposition
print("=== STRIKE 24: Complete decomposition of rotation enrichment ===")
print()
print("Raw enrichment = sieve_factor x parity_factor x residual")
print()

print("%3s %7s %7s %7s %7s %7s" % ("k", "raw", "sieve", "parity", "pred", "residual"))
print("-" * 48)

for k in range(8, 18):
    Mk = (1<<k)-1
    lo = 1<<(k-1); hi = (1<<k)-1
    if hi > N: break
    factors = distinct_prime_factors(Mk)
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    # Raw enrichment
    count = 0
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi and is_p[r]:
            count += 1
    density = len(prm) / (hi - lo + 1)
    expected = len(prm) * density
    raw = count / expected if expected else 0

    # Sieve factor: product(fi/(fi-1)) for prime factors fi of M_k
    sieve_f = math.prod(f/(f-1) for f in factors)

    # Parity factor: x2 gives 100% odd, random gives 50% odd
    # So among in-range results, all are odd for x2, but for random
    # number only half are odd. Prime density among odd numbers is
    # about 2x prime density among all numbers.
    parity_f = 2.0  # this is the factor from guaranteed oddness

    # But wait: we already measure density relative to ALL numbers in range.
    # Odd numbers are about half of [lo,hi]. Primes are all odd (>2).
    # So density_among_odd ≈ 2 * density_among_all.
    # The rotation always produces odd numbers AND in-range ~50% of time.
    # The effective enrichment should be:
    # (fraction in range) * (density among odd) / density_among_all
    # But our "expected" uses density_among_all.
    # So parity factor = density_among_odd / density_among_all ≈ 2.

    # Also: only ~50% of rotated primes land in range
    # Our raw enrichment already accounts for this (count/expected where
    # expected = #primes * density_all).

    # Actually let me think about this more carefully.
    # expected = N_primes * density = N_primes * (N_primes / N_range)
    # count = (primes whose rotation is in range AND prime)
    # raw = count / expected

    # If ALL rotated values were in range and random with density d:
    #   expected count = N_primes * d = expected
    # But only ~50% are in range, AND they're all odd.
    # Among in-range: all odd. P(prime|odd,in-range) ≈ 2*d if no other bias.
    # Expected prime count = N_primes * 0.5 * 2*d = N_primes * d = expected.
    # So the parity factor EXACTLY cancels the in-range factor!
    # The net is: parity and in-range cancel to give ratio ≈ 1 if no sieve.
    # Therefore: raw ≈ sieve_f * residual_beyond_sieve_and_parity.

    predicted = sieve_f  # parity and range cancel
    residual = raw / predicted if predicted else 0

    print("%3d %7.3f %7.3f %7s %7.3f %7.3f" % (
        k, raw, sieve_f, "cancels", predicted, residual))

print()
print("If residual ≈ 1.0: enrichment is FULLY explained by sieve preservation.")
print("If residual >> 1.0: something beyond sieve.")
print()

# STRIKE 25: Residue class concentration of survivors
print("=== STRIKE 25: Mod-30 distribution of rotation survivors ===")
print("Primes live in 8 residue classes mod 30: {1,7,11,13,17,19,23,29}")
print()

for k in [12, 14, 16]:
    lo = 1<<(k-1); hi = (1<<k)-1
    if hi > N: continue
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    survivors = []
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi and is_p[r]:
            survivors.append(p)

    # Mod 30 distribution
    residues = [1, 7, 11, 13, 17, 19, 23, 29]
    print("k=%d: %d survivors / %d primes" % (k, len(survivors), len(prm)))

    for r in residues:
        n_all = sum(1 for p in prm if p % 30 == r)
        n_surv = sum(1 for p in survivors if p % 30 == r)
        frac_all = n_all / len(prm) if prm else 0
        frac_surv = n_surv / len(survivors) if survivors else 0
        enrichment = frac_surv / frac_all if frac_all > 0 else 0
        flag = " *" if abs(enrichment - 1) > 0.2 else ""
        print("  r=%2d: all=%.3f surv=%.3f enrich=%.3f%s" % (
            r, frac_all, frac_surv, enrichment, flag))
    print()

# STRIKE 26: Convergence as k grows
print("=== STRIKE 26: Does residual converge as k → ∞? ===")
print()

residuals = []
for k in range(8, 18):
    Mk = (1<<k)-1
    lo = 1<<(k-1); hi = (1<<k)-1
    if hi > N: break
    factors = distinct_prime_factors(Mk)
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    count = 0
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi and is_p[r]:
            count += 1
    density = len(prm) / (hi - lo + 1)
    expected = len(prm) * density
    raw = count / expected if expected else 0
    sieve_f = math.prod(f/(f-1) for f in factors)
    residual = raw / sieve_f if sieve_f else 0
    residuals.append((k, residual, sieve_f))
    print("k=%2d: residual=%.3f  sieve=%.3f  raw=%.3f" % (k, residual, sieve_f, raw))

print()
mean_res = sum(r for _, r, _ in residuals) / len(residuals)
print("Mean residual: %.3f" % mean_res)
print("Std residual: %.3f" % (sum((r-mean_res)**2 for _, r, _ in residuals) / len(residuals))**.5)
print()

# STRIKE 26b: What PREDICTS the residual oscillation?
# Hypothesis: k even vs k odd matters (bit patterns)
even_res = [r for k, r, _ in residuals if k % 2 == 0]
odd_res = [r for k, r, _ in residuals if k % 2 == 1]
print("Even k residual: %.3f" % (sum(even_res)/len(even_res) if even_res else 0))
print("Odd k residual: %.3f" % (sum(odd_res)/len(odd_res) if odd_res else 0))
