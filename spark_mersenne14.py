#!/usr/bin/env python3
"""STRIKE 34: The twin prime constant connection — is it exact?

Rotation enrichment = product(fi/(fi-1) for fi|M_k) * C2_partial

where C2_partial = product(q(q-2)/(q-1)^2 for odd primes q ∤ M_k)

When ALL odd primes divide M_k (impossible, but hypothetically):
  C2_partial = 1, enrichment = full sieve product.
When NO odd primes divide M_k (M_k is prime, Mersenne prime):
  C2_partial = C2 = 0.6601..., enrichment = C2.

VERIFY: For Mersenne prime k (5,7,13,17):
  enrichment should ≈ C2 = 0.660.
  k=13: actual = 0.666, prediction = 0.660. Close!
  k=17: actual = 0.666, prediction = 0.660. Close!

The formula is: enrichment = C2 * product(fi/(fi-1) for fi|M_k) /
                                   product(fi(fi-2)/(fi-1)^2 for fi|M_k)
  = C2 * product(fi/(fi-1) * (fi-1)^2/(fi(fi-2))) for fi|M_k
  = C2 * product((fi-1)/(fi-2)) for fi|M_k

Let me verify this cleaner formula.
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

# Twin prime constant
small_primes = [n for n in range(3, 600) if is_p[n]]
C2 = math.prod(1 - 1/(p-1)**2 for p in small_primes)
print("C2 (twin prime constant, 100 primes): %.6f" % C2)
print("Known value:                           0.660162...")
print()

# The clean formula:
# enrichment = C2 * product((fi-1)/(fi-2) for odd prime fi | M_k)
#
# Derivation:
# Full product = product(fi/(fi-1) for fi|M_k) * product(q(q-2)/(q-1)^2 for q ∤ M_k)
# = product(fi/(fi-1) for fi|M_k) * C2 / product(fi(fi-2)/(fi-1)^2 for fi|M_k)
# = C2 * product(fi/(fi-1) * (fi-1)^2/(fi(fi-2)) for fi|M_k)
# = C2 * product((fi-1)/(fi-2) for fi|M_k)

print("=== STRIKE 34: Clean formula ===")
print("enrichment = C2 * product((fi-1)/(fi-2) for odd prime fi | M_k)")
print()
print("%3s %7s %7s %7s" % ("k", "actual", "formula", "ratio"))
print("-"*30)

for k in range(5, 18):
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
    actual = count / expected if expected else 0

    # Clean formula
    formula = C2 * math.prod((f-1)/(f-2) for f in factors if f > 2)

    ratio = actual / formula if formula else 0
    print("%3d %7.3f %7.3f %7.3f  factors=%s" % (k, actual, formula, ratio, factors))

print()

# THIS IS THE HARDY-LITTLEWOOD CONJECTURE ANALOG!
# For twin primes (p, p+2): density ~ C2 * product((p-1)/(p-2) for p|gcd stuff)
# For rotation primes (p, 2p-M_k): density ~ C2 * product((fi-1)/(fi-2) for fi|M_k)
#
# The reason: both are asking "how often is a LINEAR function of a prime also prime?"
# Twin primes: f(p) = p + 2.
# Rotation primes: f(p) = 2p - (2^k - 1).
#
# Hardy-Littlewood conjecture B (Bateman-Horn):
# For polynomial f, the count of primes p <= x where f(p) is also prime is
# approximately C * x / (ln x)^2 where C involves the same product over primes.
#
# Our f(p) = 2p - M_k. This is linear, degree 1, leading coeff 2.
# Bateman-Horn: C = product over primes q of (1 - omega(q)/q) / (1 - 1/q)^2
# where omega(q) = number of solutions to p * f(p) ≡ 0 mod q.
# For f(p) = 2p - M_k: p * (2p - M_k) ≡ 0 mod q
# Solutions: p ≡ 0 mod q OR p ≡ M_k/2 mod q.
# omega(q) = 2 if M_k/2 ≢ 0 mod q (two distinct roots).
# omega(q) = 1 if q | M_k (since M_k/2 ≡ 0 mod q means 2p ≡ 0, but p≡0 already counted... hmm)
# Actually: if q | M_k, then 2p - M_k ≡ 2p mod q, so f(p) ≡ 0 mod q iff p ≡ 0 mod q.
# Same root as p ≡ 0. So omega(q) = 1 when q | M_k.
# If q ∤ M_k: f(p) ≡ 0 mod q iff p ≡ M_k * 2^{-1} mod q. Different from p ≡ 0.
# So omega(q) = 2 when q ∤ M_k.
#
# Bateman-Horn constant:
# C = product(q) [(1 - omega(q)/q) / (1 - 1/q)^2]
# = product(q | M_k) [(1 - 1/q) / (1 - 1/q)^2] * product(q ∤ M_k) [(1 - 2/q) / (1-1/q)^2]
# = product(q | M_k) [1/(1-1/q)] * product(q ∤ M_k) [(q-2)/q / ((q-1)/q)^2]
# = product(q | M_k) [q/(q-1)] * product(q ∤ M_k) [q(q-2)/(q-1)^2]

print("=== STRIKE 34b: This IS the Bateman-Horn conjecture ===")
print()
print("For f(p) = 2p - M_k, the Bateman-Horn constant is:")
print("  C = product(q|M_k) [q/(q-1)] * product(q∤M_k) [q(q-2)/(q-1)^2]")
print("  = C2 * product(fi|M_k) [(fi-1)/(fi-2)]")
print()
print("This is EXACTLY what we derived from the sieve analysis!")
print("The bit rotation enrichment is a SPECIAL CASE of Bateman-Horn.")
print()

# FINAL: compare to proper Bateman-Horn prediction
# The enrichment we measure is proportional to C, not equal to it.
# Bateman-Horn gives: pi_{f}(x) ~ C * integral(dt/(ln t)^2, 2, x)
# Our "enrichment" is: actual_count / (expected from density^2)
# Expected ~ N_primes * density ~ N^2 / (k*ln2)^2
# Bateman-Horn ~ C * N / (k*ln2)^2
# Ratio = C.  So enrichment should equal the Bateman-Horn constant C.
# Which is what we found!

print("=== DIAMOND: Bit rotation enrichment = Bateman-Horn constant ===")
print()
for k in [8, 12, 13, 16, 17]:
    Mk = (1<<k)-1
    lo = 1<<(k-1); hi = (1<<k)-1
    if hi > N: continue
    factors = distinct_prime_factors(Mk)
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    count = 0
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi and is_p[r]:
            count += 1
    density = len(prm) / (hi - lo + 1)
    expected = len(prm) * density
    actual = count / expected if expected else 0

    BH = C2 * math.prod((f-1)/(f-2) for f in factors if f > 2)

    print("k=%2d: M_k=%d" % (k, Mk))
    print("  factors: %s" % factors)
    print("  actual enrichment:   %.3f" % actual)
    print("  Bateman-Horn const:  %.3f" % BH)
    print("  ratio:               %.3f" % (actual/BH if BH else 0))
    print()
