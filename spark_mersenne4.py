#!/usr/bin/env python3
"""STRIKE 9-11: WHY does omega(M_k) predict enrichment?

The mechanism: Via CRT, Z/M_k ≅ Z/f1 x Z/f2 x ...
Rotation = (x2 mod f1, x2 mod f2, ...)
A prime p ≠ fi means p is nonzero mod fi.
After rotation: 2p is also nonzero mod fi (since 2 is invertible).

So the rotation preserves "not divisible by fi" for ALL factors of M_k.
More factors = more constraints preserved = higher enrichment.

This is like: rotation acts as a sieve-preserving map for all primes dividing M_k.
"""
import math

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return s

N=65536; is_p=sieve(N)

def bit_rotate(n, d, w):
    d = d % w
    return ((n << d) | (n >> (w - d))) & ((1 << w) - 1)

# STRIKE 9: Predicted enrichment from sieve preservation
# If rotation preserves coprimality to f1,...,fm (factors of M_k),
# then among rotated numbers, the fraction coprime to each fi is higher.
#
# Enrichment prediction:
# Random number in [lo,hi]: P(prime) ≈ density
# Number coprime to f1,...,fm: P(prime) is higher by factor of
# product(fi/(fi-1)) for primes fi not already sieved by.
#
# Actually: a number coprime to {f1,...,fm} has eliminated those as
# factors. The probability of being prime, given coprime to {f1,...,fm},
# is density / product(1 - 1/fi) for those fi.

print("=== STRIKE 9: Predicted vs actual enrichment ===")
print()
print("If rotation preserves coprimality to factors of M_k,")
print("enrichment ≈ product(fi/(fi-1)) for prime factors fi of M_k")
print("that are NOT already accounted for by general prime sieving.")
print()

def factorize(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1: factors.append(n)
    return factors

def distinct_prime_factors(n):
    return list(set(factorize(n)))

for k in range(5, 17):
    Mk = (1 << k) - 1
    lo = 1<<(k-1); hi = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]
    factors = distinct_prime_factors(Mk)

    # Actual enrichment
    count = 0
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi and r <= N and is_p[r]:
            count += 1
    density = len(prm) / (hi - lo + 1)
    expected = len(prm) * density
    actual = count / expected if expected > 0 else 0

    # Predicted: product of fi/(fi-1) for ODD prime factors of M_k
    # But we need to be careful: primes already can't be divisible by 2,
    # and primes in [lo,hi] are all > fi for small fi.
    # The key: a random k-bit odd number has P(prime) ≈ 2/(k*ln2).
    # A random k-bit odd number coprime to {f1,...,fm} has P(prime) ≈
    # 2/(k*ln2) * product(fi/(fi-1)) for each fi.
    #
    # But WAIT: the k-bit primes are ALREADY not divisible by any fi.
    # So when we rotate a prime, 2p mod M_k is also not divisible by any fi.
    # The enrichment comes from: the ROTATED value is drawn from
    # "numbers coprime to all fi" rather than "all k-bit numbers".
    # Among "coprime to all fi", prime density is higher by
    # product(fi/(fi-1)) for fi that are relevant.
    #
    # But only factors fi ≤ sqrt(hi) could divide numbers in [lo,hi].
    # All factors fi < lo are automatically coprime for primes in range.
    # The enrichment only matters for fi that divide some composites in range.

    predicted = math.prod(f/(f-1) for f in factors)

    print("k=%2d: M_k=%5d  factors=%-20s  pred=%.3f  actual=%.3f  pred/actual=%.3f" % (
        k, Mk, str(factors), predicted, actual, predicted/actual if actual > 0 else 0))

print()
print("If pred ~ actual: the mechanism is pure sieve preservation.")
print("If pred != actual: something else is going on.")
print()

# STRIKE 10: Test the mechanism directly
# Take random k-bit odd numbers coprime to all factors of M_k.
# What fraction are prime? Compare to all k-bit odd numbers.
print("=== STRIKE 10: Direct test — coprime-to-M_k numbers ===")
print()

for k in [8, 10, 12, 14, 16]:
    Mk = (1 << k) - 1
    lo = 1<<(k-1); hi = (1<<k)-1
    factors = distinct_prime_factors(Mk)

    all_odd = [n for n in range(lo|1, hi+1, 2)]
    cop = [n for n in all_odd if all(n % f != 0 for f in factors)]

    primes_all = sum(1 for n in all_odd if is_p[n])
    primes_cop = sum(1 for n in cop if is_p[n])

    rate_all = primes_all / len(all_odd) if all_odd else 0
    rate_cop = primes_cop / len(cop) if cop else 0
    obs_enrichment = rate_cop / rate_all if rate_all > 0 else 0

    pred = math.prod(f/(f-1) for f in factors)

    print("k=%2d: factors=%s" % (k, factors))
    print("      odd:%d prime_rate=%.4f | cop:%d prime_rate=%.4f" % (
        len(all_odd), rate_all, len(cop), rate_cop))
    print("      enrichment: observed=%.3f  predicted=%.3f  diff=%+.3f" % (
        obs_enrichment, pred, obs_enrichment - pred))
    print()

# STRIKE 11: The orbit length distribution
# CRT: Z/M_k ≅ Z/f1 x Z/f2 x ...
# Orbit of x under multiplication by 2:
# In each component Z/fi, the orbit length is ord(2, fi).
# The orbit length in Z/M_k is lcm of individual orbit lengths.
# Shorter orbits = more structure preserved.
print("=== STRIKE 11: Orbit lengths and prime density ===")
print()

def order_mod(a, m):
    if math.gcd(a, m) > 1: return 0
    o = 1; x = a % m
    while x != 1:
        x = (x * a) % m; o += 1
        if o > m: return 0
    return o

k = 12; Mk = (1<<k)-1; lo = 1<<(k-1); hi = (1<<k)-1
factors = distinct_prime_factors(Mk)
print("k=%d, M_k=%d = %s" % (k, Mk, " x ".join(str(f) for f in factors)))
print("ord(2, fi):", [(f, order_mod(2, f)) for f in factors])
print()

# Actual orbit lengths for k-bit primes
from collections import Counter
orbit_lens = []
seen = set()
for n in range(lo, hi+1):
    if n in seen: continue
    orbit = []
    x = n
    for _ in range(k):
        if x in seen: break
        orbit.append(x)
        seen.add(x)
        x = (2 * x) % Mk
    olen = len(orbit)
    # How many primes?
    np = sum(1 for x in orbit if lo <= x <= hi and is_p[x])
    if np > 0:
        orbit_lens.append((olen, np))

# By orbit length
by_len = {}
for olen, np in orbit_lens:
    if olen not in by_len:
        by_len[olen] = []
    by_len[olen].append(np)

print("Orbit length -> mean primes per orbit:")
for olen in sorted(by_len):
    vals = by_len[olen]
    print("  len=%2d: %3d orbits, mean primes=%.2f" % (olen, len(vals), sum(vals)/len(vals)))
