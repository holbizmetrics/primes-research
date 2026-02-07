#!/usr/bin/env python3
"""STRIKE 4-5: Why does enrichment oscillate with k? Orbit structure."""
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

# STRIKE 4: The orbit of a prime under rotation
# p -> 2p -> 4p -> 8p -> ... mod M_k
# This is the "necklace" or "binary necklace" of p.
# How many primes in the full orbit?

print("=== STRIKE 4: Full orbits under bit rotation ===")
print("Orbit = {p, 2p, 4p, 8p, ...} mod M_k")
print()

for k in [10, 12, 14, 16]:
    lo = 1<<(k-1); hi = (1<<k)-1
    Mk = (1<<k)-1
    prm = set(p for p in range(lo, hi+1) if is_p[p])

    seen = set()
    orbit_stats = []  # (orbit_size, primes_in_orbit, orbit)

    for p in sorted(prm):
        if p in seen: continue
        orbit = []
        x = p
        for _ in range(k):
            orbit.append(x)
            seen.add(x)
            x = (2 * x) % Mk

        # How many in orbit are prime AND in [lo, hi]?
        primes_in = sum(1 for x in orbit if lo <= x <= hi and x in prm)
        orbit_stats.append((len(set(orbit)), primes_in, orbit))

    # Distribution of primes_in_orbit
    from collections import Counter
    dist = Counter(s[1] for s in orbit_stats)
    n_orb = len(orbit_stats)

    print("k=%d: %d orbits from %d primes" % (k, n_orb, len(prm)))
    print("  primes_per_orbit distribution:")
    for cnt in sorted(dist.keys()):
        print("    %d primes: %d orbits (%.1f%%)" % (cnt, dist[cnt], 100*dist[cnt]/n_orb))

    # What fraction of orbits have ALL members prime (when in range)?
    all_prime = sum(1 for s in orbit_stats if s[1] == s[0])
    print("  All-prime orbits: %d (%.1f%%)" % (all_prime, 100*all_prime/n_orb))
    if all_prime > 0 and all_prime <= 5:
        for s in orbit_stats:
            if s[1] == s[0]:
                print("    orbit:", sorted(s[2])[:6], "...")
    print()

# STRIKE 5: Why even k vs odd k matters
# M_k = 2^k - 1.  Factorization of M_k determines the structure.
# If M_k = a * b, then Z/M_k has zero divisors -> more "collisions"
print("=== STRIKE 5: Factorization of M_k and enrichment ===")
print()

def smallest_factor(n):
    if n <= 1: return n
    if n % 2 == 0: return 2
    i = 3
    while i * i <= n:
        if n % i == 0: return i
        i += 2
    return n

for k in range(5, 17):
    Mk = (1 << k) - 1
    sf = smallest_factor(Mk)
    is_mp = (sf == Mk)
    nf = 0
    temp = Mk
    while temp > 1:
        f = smallest_factor(temp)
        nf += 1
        while temp % f == 0: temp //= f

    # Enrichment
    lo = 1<<(k-1); hi = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]
    count = sum(1 for p in prm if is_p.get(bit_rotate(p,1,k), False) if lo <= bit_rotate(p,1,k) <= hi) if False else 0
    # Redo properly
    count = 0
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi and r <= N and is_p[r]:
            count += 1
    density = len(prm) / (hi - lo + 1)
    expected = len(prm) * density
    ratio = count / expected if expected > 0 else 0

    print("k=%2d: M_k=%5d = %-20s  #factors=%d  enrichment=%.3f %s" % (
        k, Mk,
        ("%d (prime)" % Mk) if is_mp else str(Mk),
        nf, ratio,
        "MERSENNE" if is_mp else ""))

print()

# STRIKE 5b: Does 2 being a primitive root of M_k matter?
# If 2 is a primitive root mod M_k, the orbit is a SINGLE cycle of length k.
# Otherwise orbits are shorter.
print("=== STRIKE 5b: Order of 2 mod factors of M_k ===")
print()

def order_mod(a, m):
    """Order of a in (Z/mZ)*"""
    if math.gcd(a, m) > 1: return 0
    o = 1; x = a % m
    while x != 1:
        x = (x * a) % m
        o += 1
        if o > m: return 0  # shouldn't happen
    return o

for k in range(5, 17):
    Mk = (1 << k) - 1
    ord2 = order_mod(2, Mk)
    # ord2 should always be k (since 2^k = 1 mod M_k by definition)
    # But what about the factors?
    factors = []
    temp = Mk
    while temp > 1:
        f = smallest_factor(temp)
        factors.append(f)
        while temp % f == 0: temp //= f
    factor_orders = [(f, order_mod(2, f)) for f in factors]
    print("k=%2d: M_k=%5d  factors=%s  ord(2,f)=%s" % (
        k, Mk, factors, [(f,o) for f,o in factor_orders]))
