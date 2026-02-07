#!/usr/bin/env python3
"""STRIKE 27-29: Why even k gives residual ~0.92 and odd k gives ~0.70.

Even k: M_k = 2^k - 1 is always divisible by 3 when k is even.
  M_2=3, M_4=15=3*5, M_6=63=3*7*3, M_8=255=3*5*17, M_10=1023=3*11*31...
  Actually: 2^k ≡ 1 mod 3 when k is even, so 3 | M_k for even k.
  And 2^k ≡ 2 mod 3 when k is odd, so M_k ≡ 1 mod 3, 3 ∤ M_k for odd k.

When 3 | M_k: sieve factor includes 3/(3-1) = 1.5.
When 3 ∤ M_k: sieve factor doesn't include the 3-correction.

But we ALREADY account for this in the sieve prediction. So why does
the residual differ?

The issue: our sieve prediction is product(fi/(fi-1)), but this assumes
the NUMBER is a random integer coprime to M_k's factors. However, the
ROTATED value is not random — it's 2r+1 which is ALWAYS coprime to 2.
Being coprime to 2 is already captured by the parity effect.

For even k (3 | M_k): rotation preserves coprimality to 3.
But primes are ALREADY coprime to 3. So the sieve factor of 3/2=1.5
is the enrichment from "coprime to 3 among all k-bit numbers."
Among odd k-bit numbers (which rotated values are), the fraction
coprime to 3 is different!

We need to compare against ODD numbers coprime to factors of M_k.
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

# STRIKE 27: Corrected sieve factor for ODD coprime numbers
print("=== STRIKE 27: Sieve factor corrected for oddness ===")
print()
print("Old prediction: product(fi/(fi-1)) over ALL factors of M_k")
print("New prediction: product(fi/(fi-1)) over ODD factors only,")
print("                relative to prime density among ODD numbers")
print()

print("%3s %7s %7s %7s %7s %7s" % ("k", "raw", "old_sv", "new_sv", "old_res", "new_res"))
print("-" * 50)

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

    old_sieve = math.prod(f/(f-1) for f in factors)

    # Corrected: rotation gives odd numbers. Prime density among odd
    # k-bit numbers = 2 * density.
    # Among odd numbers coprime to odd factors of M_k:
    # density = 2*density * product(fi/(fi-1)) for odd fi.
    # So enrichment vs all numbers = 2 * product(fi/(fi-1)) for odd fi.
    # But expected already uses density_all.
    # And ~50% of rotated values are in range.
    # Count / expected = count / (N_primes * density_all)
    #
    # count ≈ N_primes * 0.5 * 2*density * product(fi/(fi-1) for odd fi)
    #       = N_primes * density * product(fi/(fi-1) for odd fi)
    # So raw ≈ product(fi/(fi-1) for odd fi).
    #
    # The "2" factor includes factor {2} itself, which means:
    # if 2 is NOT a factor of M_k (M_k is always odd), then
    # the correction is just: exclude factor 2 from the product (if present).
    # M_k is always odd, so 2 is never a factor. The old sieve is correct.
    #
    # Wait — I'm overcomplicating this. Let me just do it empirically.

    # Empirical: prime rate among odd k-bit numbers coprime to factors of M_k
    odd_in_range = list(range(lo|1, hi+1, 2))
    cop = [n for n in odd_in_range if all(n % f != 0 for f in factors)]
    rate_odd = sum(1 for n in odd_in_range if is_p[n]) / len(odd_in_range)
    rate_cop = sum(1 for n in cop if is_p[n]) / len(cop) if cop else 0
    empirical_sieve = rate_cop / rate_odd if rate_odd else 0

    old_res = raw / old_sieve if old_sieve else 0
    new_res = raw / empirical_sieve if empirical_sieve else 0

    print("%3d %7.3f %7.3f %7.3f %7.3f %7.3f" % (
        k, raw, old_sieve, empirical_sieve, old_res, new_res))

print()

# STRIKE 28: In-range fraction depends on k parity too
print("=== STRIKE 28: In-range fraction vs k parity ===")
print()

for k in range(8, 18):
    lo = 1<<(k-1); hi = (1<<k)-1
    if hi > N: break
    prm = [p for p in range(lo, hi+1) if is_p[p]]
    in_range = sum(1 for p in prm if lo <= bit_rotate(p,1,k) <= hi)
    frac = in_range / len(prm)
    print("k=%2d: in-range=%.4f (%s)" % (k, frac, "even" if k%2==0 else "odd"))

print()

# STRIKE 29: The DEFINITIVE test.
# Measure: among k-bit primes p, compute 2p mod M_k.
# Filter to: in k-bit range (MSB=1) and odd (LSB=1).
# What fraction of these are prime?
# Compare to: among ALL k-bit odd coprime-to-M_k numbers, what fraction prime?
# The RATIO is the true residual.
print("=== STRIKE 29: Definitive residual test ===")
print()

for k in range(8, 18):
    Mk = (1<<k)-1
    lo = 1<<(k-1); hi = (1<<k)-1
    if hi > N: break
    factors = distinct_prime_factors(Mk)
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    # Rotated values: all in range, all odd (proven)
    rotated = []
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi:
            rotated.append(r)

    rate_rot = sum(1 for r in rotated if is_p[r]) / len(rotated) if rotated else 0

    # Control: odd, in-range, coprime to factors of M_k
    cop = [n for n in range(lo|1, hi+1, 2) if all(n % f != 0 for f in factors)]
    rate_cop = sum(1 for n in cop if is_p[n]) / len(cop) if cop else 0

    residual = rate_rot / rate_cop if rate_cop else 0

    print("k=%2d: rot_prime_rate=%.4f  cop_prime_rate=%.4f  residual=%.3f  (%s)" % (
        k, rate_rot, rate_cop, residual, "even" if k%2==0 else "odd"))

print()
print("residual ≈ 1.0: rotation enrichment FULLY explained by sieve+parity")
print("residual > 1.0: genuine structure beyond sieve+parity")
print("residual < 1.0: rotation actively HURTS (mapping to prime-poor regions)")
