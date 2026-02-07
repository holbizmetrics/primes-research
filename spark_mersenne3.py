#!/usr/bin/env python3
"""STRIKE 6-8: Orbit fragmentation, the CRT connection, and d>1 sweeps."""
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

def smallest_factor(n):
    if n <= 1: return n
    for i in range(2, int(n**.5)+1):
        if n % i == 0: return i
    return n

def num_distinct_factors(n):
    nf = 0
    while n > 1:
        f = smallest_factor(n)
        nf += 1
        while n % f == 0: n //= f
    return nf

# STRIKE 6: Correlation between omega(M_k) and enrichment
print("=== STRIKE 6: omega(M_k) vs enrichment ===")
print("omega = number of distinct prime factors of 2^k - 1")
print()

data = []
for k in range(5, 17):
    Mk = (1 << k) - 1
    omega = num_distinct_factors(Mk)
    lo = 1<<(k-1); hi = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]
    count = 0
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi and r <= N and is_p[r]:
            count += 1
    density = len(prm) / (hi - lo + 1)
    expected = len(prm) * density
    ratio = count / expected if expected > 0 else 0
    data.append((k, omega, ratio))
    print("k=%2d  omega=%d  ratio=%.3f" % (k, omega, ratio))

print()
# Group by omega
from collections import defaultdict
by_omega = defaultdict(list)
for k, o, r in data:
    by_omega[o].append(r)

print("By omega(M_k):")
for o in sorted(by_omega):
    vals = by_omega[o]
    print("  omega=%d: mean=%.3f  values=%s" % (o, sum(vals)/len(vals), ["%.3f"%v for v in vals]))

print()

# STRIKE 7: The CRT decomposition
# Z/(2^k-1)Z ≅ Z/f1 × Z/f2 × ... when M_k = f1*f2*...
# Rotation = multiply by 2 in each component.
# More components = more "independent" chances for both p and 2p to avoid
# being divisible by the component primes.
#
# KEY INSIGHT: p mod fi and (2p) mod fi are linked.
# If fi | p, then fi | 2p. If fi ∤ p, then fi ∤ 2p (since gcd(2,fi)=1 for odd fi).
# So: p is coprime to M_k <=> 2p mod M_k is coprime to M_k.
# The rotation PRESERVES coprimality to M_k!
#
# For a k-bit number: p has MSB=1, so p >= 2^{k-1}.
# After rotation: 2p mod M_k. Is it still in [2^{k-1}, 2^k-1]?

print("=== STRIKE 7: CRT — rotation preserves coprimality to M_k ===")
print()

k = 12; Mk = (1<<k)-1; lo = 1<<(k-1); hi = (1<<k)-1
prm = [p for p in range(lo, hi+1) if is_p[p]]

# Factor M_k
factors_Mk = []
temp = Mk
while temp > 1:
    f = smallest_factor(temp)
    factors_Mk.append(f)
    while temp % f == 0: temp //= f

print("M_%d = %d = %s" % (k, Mk, " x ".join(str(f) for f in factors_Mk)))
print()

# For each prime p, check: p mod fi, and rotated(p) mod fi
print("p mod fi -> rotated(p) mod fi  (should be 2p mod fi)")
for p in prm[:8]:
    r = bit_rotate(p, 1, k)
    mods_p = [p % f for f in factors_Mk]
    mods_r = [r % f for f in factors_Mk]
    mods_2p = [(2*p) % f for f in factors_Mk]
    print("  p=%d: p mod fi=%s  rot=%d: rot mod fi=%s  2p mod fi=%s  match=%s" % (
        p, mods_p, r, mods_r, mods_2p, mods_r == mods_2p))

print()

# KEY: What fraction of k-bit primes are coprime to M_k?
cop = sum(1 for p in prm if math.gcd(p, Mk) == 1)
print("%d of %d primes are coprime to M_%d (%.1f%%)" % (cop, len(prm), k, 100*cop/len(prm)))
print("(Expected: product of (1 - 1/fi) = %.3f)" % (
    math.prod((1 - 1/f) for f in factors_Mk)))
print()

# STRIKE 8: Full rotation sweep for multiple k values
# For d=1,...,k-1, measure enrichment
print("=== STRIKE 8: Full rotation sweep for k=12,14,16 ===")
print()

for k in [12, 14, 16]:
    lo = 1<<(k-1); hi = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]
    density = len(prm) / (hi - lo + 1)
    expected = len(prm) * density

    print("k=%d (%d primes):" % (k, len(prm)))
    best_d = 0; best_r = 0
    for d in range(k):
        count = 0
        for p in prm:
            r = bit_rotate(p, d, k)
            if lo <= r <= hi and r <= N and is_p[r]:
                count += 1
        ratio = count / expected if expected > 0 else 0
        tag = ""
        if d == 0: tag = " (identity)"
        elif d == 1: tag = " (x2)"
        elif d == k-1: tag = " (x2^-1)"
        elif d == k//2: tag = " (half-flip)"
        if ratio > 1.5 or d in [0,1,k-1,k//2]:
            print("  d=%2d: ratio=%.3f%s" % (d, ratio, tag))
        if d > 0 and ratio > best_r:
            best_r = ratio; best_d = d
    print("  best non-identity: d=%d ratio=%.3f" % (best_d, best_r))
    print()
