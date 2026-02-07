#!/usr/bin/env python3
"""STRIKE 15-17: Final mechanism + orbit primes + the real question.

Summary so far:
- Rotation = multiply by 2 mod M_k (confirmed)
- Enrichment tracks omega(M_k) exactly
- Coprime-to-M_k enrichment matches product(fi/(fi-1)) to 3 decimals
- Residual beyond sieve: ~0.95 (i.e., NONE)
- The entire effect is EXPLAINED: rotation preserves coprimality to factors of M_k

STRIKE 15: Can we predict enrichment for ANY d, not just d=1?
STRIKE 16: Is there a "rotation-prime" analog of twin primes?
STRIKE 17: What about the multiplicative ORDER — primes whose full
           orbit (under x2 mod M_k) contains unusually many primes?
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

def distinct_prime_factors(n):
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0: factors.add(d); n //= d
        d += 1
    if n > 1: factors.add(n)
    return sorted(factors)

# STRIKE 15: Enrichment for d=2 should be same as d=1
# Because 2^d mod fi still preserves coprimality.
# The sieve prediction is the SAME for all d (except d=0).
# So all non-identity rotations should give the same enrichment!
print("=== STRIKE 15: All rotations d=1..k-1 should give same enrichment ===")
print()

for k in [12, 14, 16]:
    lo = 1<<(k-1); hi = (1<<k)-1
    Mk = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]
    factors = distinct_prime_factors(Mk)
    density = len(prm) / (hi - lo + 1)
    expected = len(prm) * density
    sieve_pred = math.prod(f/(f-1) for f in factors)

    ratios = []
    for d in range(1, k):
        count = 0
        for p in prm:
            r = bit_rotate(p, d, k)
            if lo <= r <= hi and r <= N and is_p[r]:
                count += 1
        ratio = count / expected if expected > 0 else 0
        ratios.append(ratio)

    mean_r = sum(ratios) / len(ratios)
    min_r = min(ratios)
    max_r = max(ratios)
    print("k=%2d: sieve_pred=%.3f  mean_ratio=%.3f  min=%.3f  max=%.3f  spread=%.3f" % (
        k, sieve_pred, mean_r, min_r, max_r, max_r - min_r))
    # Show all
    for d in range(1, k):
        if ratios[d-1] > mean_r * 1.3 or ratios[d-1] < mean_r * 0.7:
            print("  d=%2d: ratio=%.3f  (outlier)" % (d, ratios[d-1]))

print()
print("If all ratios are similar: confirmed, mechanism is pure coprimality.")
print("If some d give higher ratio: there's structure in WHICH rotation.")
print()

# STRIKE 16: "Rotation twins" — primes p where BOTH p and rotate(p,1,k) are prime
# How does the count of such pairs grow with k?
# Is it ~ (density)^2 * N * sieve_correction, or more/less?
print("=== STRIKE 16: Rotation twin primes ===")
print("Primes p where both p and 2p mod M_k are prime")
print()

for k in range(8, 17):
    lo = 1<<(k-1); hi = (1<<k)-1
    Mk = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]
    factors = distinct_prime_factors(Mk)

    twins = []
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi and r <= N and is_p[r]:
            twins.append((p, r))

    density = len(prm) / (hi - lo + 1)
    # Expected if independent: density * len(prm) * P(in_range) * density * sieve
    in_range = sum(1 for p in prm if lo <= bit_rotate(p,1,k) <= hi)
    expected_naive = in_range * density
    sieve_pred = math.prod(f/(f-1) for f in factors)
    expected_sieve = in_range * density * sieve_pred

    # Hardy-Littlewood style: actual count vs expected
    print("k=%2d: pairs=%3d  naive_exp=%.1f  sieve_exp=%.1f  actual/sieve=%.3f" % (
        k, len(twins), expected_naive, expected_sieve,
        len(twins)/expected_sieve if expected_sieve > 0 else 0))

print()

# STRIKE 17: Multi-rotation primes — primes where the FULL orbit has many primes
# These are "rotation-rich" primes.
print("=== STRIKE 17: Rotation-rich orbits (most primes in orbit) ===")
print()

k = 16; lo = 1<<(k-1); hi = (1<<k)-1
Mk = (1<<k)-1
prm = set(p for p in range(lo, hi+1) if is_p[p])

seen = set()
orbit_data = []

for p in sorted(prm):
    if p in seen: continue
    orbit = []
    x = p
    for _ in range(k):
        if x in seen: break
        orbit.append(x)
        seen.add(x)
        x = (2 * x) % Mk

    in_range = [x for x in orbit if lo <= x <= hi]
    primes_in = [x for x in in_range if x in prm]
    orbit_data.append((len(primes_in), len(in_range), len(orbit), sorted(primes_in)[:4]))

orbit_data.sort(key=lambda x: -x[0])

print("k=%d: top rotation-rich orbits:" % k)
print("%5s %5s %5s  %s" % ("#prm", "inrng", "orbit", "primes (first 4)"))
for np, nir, norb, prms in orbit_data[:15]:
    print("%5d %5d %5d  %s" % (np, nir, norb, prms))

print()

# How many primes per orbit, vs expected?
from collections import Counter
dist = Counter(d[0] for d in orbit_data)
total_orbits = len(orbit_data)
print("Distribution of primes per orbit:")
for cnt in sorted(dist):
    print("  %d primes: %d orbits (%.1f%%)" % (cnt, dist[cnt], 100*dist[cnt]/total_orbits))
