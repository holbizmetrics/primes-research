#!/usr/bin/env python3
"""STRIKE 33: The excess divisibility — why rotated primes have MORE
div-by-q than random, for q not dividing M_k.

For odd k: 57% of rotated values div by 3 (vs 33% expected).
Why the EXCESS? Because primes are coprime to 3. The rotation
r = 2p mod M_k, and for odd k, M_k ≡ 1 mod 3.
So r ≡ 2p - M_k ≡ 2p - 1 mod 3.
If p ≡ 1 mod 3: r ≡ 1 mod 3 (coprime).
If p ≡ 2 mod 3: r ≡ 0 mod 3 (div by 3).
Primes: ~half are ≡1, ~half are ≡2. So ~50% become div by 3.
Random numbers: 1/3 are div by 3.
50% >> 33% because primes AVOID being div by 3, but the rotation
maps exactly the "≡2 mod 3" primes to "≡0 mod 3" numbers.

Same logic for 5: primes avoid 5. Rotation maps specific residue
classes to 0 mod 5. If 5 ∤ M_k, then about 1/4 of primes map to 0 mod 5
(since primes have 4 nonzero residue classes mod 5, and rotation sends
one of them to 0).

General: for prime q ∤ M_k:
  - Primes have (q-1) equally populated residue classes mod q
  - Rotation is multiplication by 2 mod M_k
  - 2p ≡ 0 mod q iff p ≡ 0 mod q (impossible, p is prime and > q)
  Wait: r = 2p mod M_k, not 2p mod q.
  r mod q = (2p mod M_k) mod q = (2p - c*M_k) mod q for some c.
  For k-bit p: c=1 (since M_k < 2p < 2*M_k).
  So r = 2p - M_k.
  r mod q = (2p - M_k) mod q.

  If q | M_k: r mod q = 2p mod q. Since gcd(2,q)=1 and p≢0 mod q: r ≢ 0 mod q. Good.
  If q ∤ M_k: r ≡ 2p - M_k mod q. This is 0 when 2p ≡ M_k mod q,
  i.e., p ≡ M_k * 2^{-1} mod q.

  Is this residue class one that primes can occupy? Yes (unless it's 0 mod q).
  M_k * 2^{-1} mod q = (2^k - 1) * 2^{-1} mod q = (2^{k-1} - 2^{-1}) mod q.
  This is some specific nonzero residue mod q (unless q | M_k).

  So: exactly 1/(q-1) fraction of primes map to 0 mod q.
  (Since primes are equidistributed among (q-1) nonzero residues mod q.)

  For random odd numbers: 1/q are div by q.
  For rotated primes: 1/(q-1) are div by q.
  1/(q-1) > 1/q always!

  Excess: 1/(q-1) - 1/q = 1/(q(q-1)).

  This means: for EVERY prime q not dividing M_k, rotated primes are
  MORE likely div by q than random. The enrichment from coprimality
  to M_k factors is PARTIALLY offset by excess divisibility by non-factors.
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

# THE CORRECTED PREDICTION:
# For factors fi of M_k: enrichment = product(fi/(fi-1))
# For primes q not dividing M_k: depletion = product((q-1)/q / ((q-2)/(q-1)))
# Wait, let me think about this more carefully.
#
# Among rotated values:
# P(coprime to q) = 1 - 1/(q-1) = (q-2)/(q-1)  for q ∤ M_k
# P(coprime to q) = 1                             for q | M_k
#
# Among random odd numbers:
# P(coprime to q) = 1 - 1/q = (q-1)/q
#
# Prime density among numbers coprime to set S = density * product(q/(q-1) for q in S)
#
# For rotated values, the effective coprime set is:
# - Guaranteed coprime to 2 (all odd)
# - Guaranteed coprime to each fi | M_k
# - For q ∤ M_k: fraction (q-2)/(q-1) coprime, fraction 1/(q-1) not coprime
#
# The sieve prediction captures the fi | M_k part.
# The depletion from q ∤ M_k: each such q contributes a factor of
# (1 - 1/(q-1)) / (1 - 1/q) = (q-2)/(q-1) * q/(q-1) = q(q-2)/(q-1)^2
# to the effective density... no wait.
#
# Let me use inclusion-exclusion or just the product formula.
#
# P(prime | rotated, in range) ≈ C / (ln N) * product over primes q:
#   if q = 2: factor = 2 (all odd)
#   if q | M_k: factor = q/(q-1) (all coprime to q)
#   if q ∤ M_k: factor = ((q-2)/(q-1)) * (q/(q-1)) + (1/(q-1)) * 0 = q(q-2)/(q-1)^2
#     No — for those coprime to q: factor q/(q-1) from sieving
#     For those div by q: factor 0 (not prime)
#     Weighted: (q-2)/(q-1) * q/(q-1) + 1/(q-1) * 0 = q(q-2)/(q-1)^2
#
# Compare to random odd: product = product(q/(q-1)) for all odd primes q.
#
# Enrichment = product(q | M_k) [q/(q-1)] *
#              product(q ∤ M_k) [q(q-2)/(q-1)^2] /
#              product(all odd q) [q/(q-1)]
#
#            = product(q | M_k) [q/(q-1)] *
#              product(q ∤ M_k) [(q-2)/(q-1)]  /
#              product(q | M_k) [q/(q-1)]    ... hmm this isn't right.
#
# Simpler approach: ratio of P(prime | rotated) / P(prime | random k-bit).
# P(prime | random) ≈ 1 / (k * ln 2).
# P(prime | rotated) ≈ product over all primes q of (adjustment factor).
#
# Actually, the simplest correct formula:
#
# Among rotated values (which are odd), for each odd prime q:
# - If q | M_k: all rotated values are coprime to q.
#   Compared to random odd numbers (where fraction (q-1)/q are coprime to q),
#   this gives a boost of q/(q-1).
# - If q ∤ M_k: fraction (q-2)/(q-1) of rotated values are coprime to q.
#   Compared to random odd numbers (where fraction (q-1)/q are coprime to q),
#   this gives factor [(q-2)/(q-1)] / [(q-1)/q] = q(q-2)/(q-1)^2.
#
# Total enrichment vs random odd =
#   product(q|M_k) [q/(q-1)] * product(q∤M_k, q small) [q(q-2)/(q-1)^2]
# Then multiply by 2 for odd vs all, and divide by 2 for 50% in-range.
# These cancel, giving just the product above.
#
# But we measure enrichment vs density among ALL numbers in range:
# raw_enrichment = P(prime|rotated) / density_all
# = [P(prime|random_odd) * product_factors] / density_all
# = [2*density_all * product_factors] / density_all
# = 2 * product_factors * 0.5 (in-range)
# = product_factors
#
# So: enrichment = product(q|M_k) [q/(q-1)] * product(q∤M_k) [q(q-2)/(q-1)^2]

print("=== STRIKE 33: Full product formula with depletion ===")
print()

# Use first 100 primes for the product
small_primes = []
for n in range(3, 600):
    if is_p[n]:
        small_primes.append(n)
    if len(small_primes) >= 100:
        break

for k in range(8, 18):
    Mk = (1<<k)-1
    lo = 1<<(k-1); hi = (1<<k)-1
    if hi > N: break
    factors = set(distinct_prime_factors(Mk))
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    count = 0
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi and is_p[r]:
            count += 1
    density = len(prm) / (hi - lo + 1)
    expected = len(prm) * density
    actual = count / expected if expected else 0

    # Old prediction (only factors of M_k)
    old_pred = math.prod(f/(f-1) for f in factors)

    # New prediction (include depletion from non-factors)
    new_pred = 1.0
    for q in small_primes:
        if q in factors:
            new_pred *= q / (q - 1)
        else:
            new_pred *= q * (q - 2) / (q - 1)**2
            # This product converges quickly since q(q-2)/(q-1)^2 → 1

    ratio = actual / new_pred if new_pred else 0

    print("k=%2d: actual=%.3f old=%.3f new=%.3f  actual/new=%.3f" % (
        k, actual, old_pred, new_pred, ratio))

print()
print("The depletion from non-factors should bring the prediction DOWN,")
print("closer to the actual values.")
print()

# What is the depletion product for non-factors?
# product(q(q-2)/(q-1)^2) = product((1 - 1/(q-1)^2)) ≈ product of Mertens-like terms
print("=== Depletion factors ===")
dep = 1.0
for q in small_primes[:20]:
    factor = q * (q - 2) / (q - 1)**2
    dep *= factor
    print("  q=%3d: q(q-2)/(q-1)^2 = %.6f  cumulative = %.6f" % (q, factor, dep))

print()
print("The twin prime constant C2 = product(1 - 1/(p-1)^2) for p>=3 = 0.6601...")
print("Our depletion is the SAME product! (Since q(q-2)/(q-1)^2 = 1 - 1/(q-1)^2)")
print()

# VERIFY: our depletion product = twin prime constant!
dep_full = 1.0
for q in small_primes:
    dep_full *= q * (q - 2) / (q - 1)**2
print("Depletion product (100 primes): %.6f" % dep_full)
print("Twin prime constant C2:         0.660162...")
