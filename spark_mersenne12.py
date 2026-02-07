#!/usr/bin/env python3
"""STRIKE 32: Final corrected prediction for ALL k.

Even k: 3 | M_k, rotation preserves coprimality to 3.
  All rotated primes are ≡ 1 or 5 mod 6 (prime-eligible).
  Enrichment ≈ product(fi/(fi-1)) for factors fi of M_k.

Odd k: 3 ∤ M_k, rotation maps ~half of primes to multiples of 3.
  Only primes ≡ 1 mod 3 survive (their rotation ≡ 1 mod 3, coprime to 3).
  Primes ≡ 2 mod 3 get mapped to 0 mod 3 (killed).
  So: effective count halved for the 3-killed portion.

Corrected prediction for odd k:
  Among primes, ~half are ≡ 1 mod 3, ~half ≡ 2 mod 3.
  The ≡1 primes: rotated is ≡1 mod 3, coprime to 3, prime rate = cop_rate.
  The ≡2 primes: rotated is ≡0 mod 3, prime rate = 0.
  So: rotation_prime_rate ≈ 0.5 * cop_rate + 0.5 * 0 = 0.5 * cop_rate.

  But cop_rate for odd k uses factors NOT including 3 (since 3 ∤ M_k).
  For even k: cop_rate includes factor 3 (since 3 | M_k).

  Net: odd k enrichment ≈ product(fi/(fi-1) for fi | M_k) * 0.5 * (3/2)
  = product(fi/(fi-1)) * 0.75
  The 3/2 comes from: the surviving half are coprime to 3, which enriches
  their density by 3/2 relative to all odds.

  Wait, let me be more careful...
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

# Let's build the corrected prediction from scratch.
#
# Setup: k-bit primes p, rotated to r = 2p mod M_k.
# If r is in [lo, hi] (k-bit range), check if r is prime.
#
# Expected count (null hypothesis): N_primes * P(in range) * P(prime | in range)
# = N_primes * 0.5 * density
# This gives expected = N_primes * density * 0.5 ... but our raw expected
# is N_primes * density (without the 0.5).
# Raw enrichment = count / (N_primes * density).
#
# Key facts:
# 1. P(in range) ≈ 0.5 (confirmed, both even and odd k)
# 2. All in-range rotations are ODD (confirmed)
# 3. For even k: all in-range rotations are coprime to 3 (confirmed, since 3|M_k)
#    For odd k: ~50% in-range rotations are div by 3
# 4. For even k: rotation preserves coprimality to ALL factors of M_k
#    For odd k: rotation preserves coprimality to factors of M_k EXCEPT:
#    the factor 3 is NOT a factor of M_k, so there's no preservation for 3.
#    Instead, it CREATES divisibility by 3 for half the inputs.
#
# Enrichment for even k:
#   All rotated in-range values are odd, coprime to all factors of M_k.
#   P(prime | odd, coprime to factors) = density_all * prod(fi/(fi-1))
#   where we include 2/(2-1)=2 for oddness and fi/(fi-1) for each fi|M_k.
#   But density_all already includes the 1/2 factor from even numbers being
#   non-prime. So:
#
#   Let me just do it directly.
#
#   count ≈ (N_primes * 0.5) * P(prime | odd, coprime to factors of M_k, in range)
#   raw_enrichment = count / (N_primes * density)
#
#   P(prime | odd, coprime to factors) = density * prod(fi/(fi-1)) for fi|M_k
#                                         * 2  (for odd)
#   count ≈ N_primes * 0.5 * density * 2 * prod(fi/(fi-1))
#         = N_primes * density * prod(fi/(fi-1))
#   raw_enrichment ≈ prod(fi/(fi-1))  ← MATCHES for even k!
#
# Enrichment for odd k:
#   In-range rotated values are all odd. ~50% are coprime to 3, ~50% div by 3.
#   The coprime-to-3 half: coprime to all factors of M_k AND to 3.
#   P(prime | odd, coprime to M_k factors, coprime to 3) = density * 2 * prod(fi/(fi-1)) * 3/2
#   The div-by-3 half: P(prime) = 0 (since >3 and div by 3).
#
#   count ≈ N_primes * 0.5 * [0.5 * density * 2 * prod(fi/(fi-1)) * 3/2 + 0.5 * 0]
#         = N_primes * 0.5 * 0.5 * density * 2 * prod * 3/2
#         = N_primes * density * prod * 3/4
#   raw_enrichment ≈ prod(fi/(fi-1)) * 3/4 = prod * 0.75

print("=== STRIKE 32: Final corrected prediction ===")
print()
print("%3s %7s %7s %7s %7s" % ("k", "actual", "old_pred", "new_pred", "ratio"))
print("-"*40)

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
    actual = count / expected if expected else 0

    old_pred = math.prod(f/(f-1) for f in factors)

    if k % 2 == 0:
        new_pred = old_pred  # 3 | M_k, full sieve preservation
    else:
        new_pred = old_pred * 0.75  # 3 ∤ M_k, half killed by 3

    ratio = actual / new_pred if new_pred else 0

    print("%3d %7.3f %7.3f %7.3f %7.3f  %s" % (
        k, actual, old_pred, new_pred, ratio,
        "" if k%2==0 else "(odd k, x0.75)"))

print()

# Hmm, for odd k with M_k prime (k=5,7,13,17), sieve_factor = 1.
# So new_pred = 0.75. But actual ≈ 0.66-0.83.
# Let me check if there are more small primes that create similar issues.

# For odd k: does 5 also cause problems?
# 5 | M_k when ord(2,5) | k, i.e., 4 | k. So k=4,8,12,16...
# For k odd: 5 ∤ M_k (since 4 ∤ k).
# Does rotation create 5-divisibility for odd k?
# r = 2p mod M_k. r mod 5 = (2p - M_k) mod 5 = (2p - M_k) mod 5.
# Need M_k mod 5: 2^k mod 5 cycles with period 4: 2,4,3,1,2,4,3,1,...
# k=9: 2^9=512, 512 mod 5=2, M_9 mod 5=1.
# r mod 5 = (2p-1) mod 5. If p≡3 mod 5: r≡0 mod 5!
# So for k≡1 mod 4 (2^k≡2 mod 5): ~1/4 of primes get killed by 5 too.

print("=== STRIKE 32b: Which small primes kill rotated values? ===")
print()

for k in range(8, 18):
    Mk = (1<<k)-1
    lo = 1<<(k-1); hi = (1<<k)-1
    if hi > N: break
    factors = distinct_prime_factors(Mk)
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    rotated_in_range = []
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi:
            rotated_in_range.append(r)

    if not rotated_in_range: continue

    # For each small prime q not dividing M_k:
    # what fraction of rotated values are div by q?
    print("k=%2d (M_k=%d, factors=%s):" % (k, Mk, factors))
    for q in [3, 5, 7, 11, 13]:
        if q in factors:
            print("  %2d: factor of M_k (preserved)" % q)
        else:
            div_q = sum(1 for r in rotated_in_range if r % q == 0)
            frac = div_q / len(rotated_in_range)
            expected_frac = 1/q  # random fraction div by q
            # Among odd numbers coprime to M_k factors, expected fraction div by q = 1/q
            # (if q is odd and not a factor of M_k)
            print("  %2d: %.1f%% div by %d (expected %.1f%%)" % (
                q, 100*frac, q, 100/q))
    print()

# FINAL PREDICTION: incorporate ALL small primes
print("=== STRIKE 32c: Full prediction with all small prime corrections ===")
print()

# For a prime q:
# q | M_k iff ord(2,q) | k.
# If q | M_k: rotation preserves coprimality to q (enrichment factor q/(q-1)).
# If q ∤ M_k: rotation maps fraction 1/q of rotated values to be div by q.
#   This is EXACTLY the random expectation. No enrichment from q.
#   But our old prediction gave enrichment factor 1 for these (correct).
#
# The issue: primes are ALREADY coprime to q. After rotation, fraction 1/q
# become div by q. These are LOST compared to the "coprime to everything" baseline.
#
# Correct enrichment = product over all primes q:
#   if q | M_k: factor = q/(q-1) (coprimality preserved)
#   if q ∤ M_k: factor = (q-1)/q * q/(q-1) * 1 = 1 ... wait
#
# Let me think about this differently.
#
# Rotated value r is a random-ish odd number in [lo, hi].
# It is coprime to each factor fi of M_k.
# For primes q ∤ M_k: r is random mod q (fraction 1/q div by q).
#
# P(prime | odd, coprime to {fi}) = P(prime | odd) * product(fi/(fi-1) for fi|M_k, fi>2)
# = (2 * density) * product(fi/(fi-1) for odd fi | M_k)
#
# raw_enrichment = count / (N_primes * density)
# count = (N_primes * 0.5) * (2 * density) * product(fi/(fi-1) for odd fi | M_k)
# raw_enrichment = product(fi/(fi-1) for odd fi | M_k)
#
# This is exactly the OLD prediction! The 3-killing for odd k is already
# captured by NOT including 3 in the product when 3 ∤ M_k.
#
# So why does the old prediction OVERESTIMATE for odd k?
# Because the old prediction DOES include 3 when 3 | M_k (even k),
# but for odd k where 3 ∤ M_k, the product already excludes 3.
# The product for odd k is SMALLER than for even k.
# And the actual enrichment matches this smaller product...
#
# Let me recheck the numbers.

print("Recheck: does product(fi/(fi-1)) for fi|M_k already handle everything?")
print()

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
    actual = count / expected if expected else 0

    sieve_pred = math.prod(f/(f-1) for f in factors)

    # The prediction = sieve_pred. That's it.
    # For even k, this includes 3/2. For odd k, it doesn't.
    # But is the prediction correct?
    ratio = actual / sieve_pred if sieve_pred else 0

    # For Mersenne prime M_k: sieve_pred = M_k/(M_k-1) ≈ 1.
    # Actual ≈ 0.66. So there IS an unexplained factor for Mersenne-prime k.
    # This isn't the 3 issue — it's that M_k prime means no small factor protection.

    parity = "even" if k%2==0 else "odd"
    print("k=%2d (%4s): sieve=%.3f actual=%.3f ratio=%.3f  factors=%s" % (
        k, parity, sieve_pred, actual, ratio, factors))
