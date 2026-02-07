#!/usr/bin/env python3
"""STRIKE 21-23: WHY does x2 beat x3, x5, x7?

All multiplications mod M_k preserve coprimality to factors of M_k.
But x2 gives ~1.7x more primality preservation. Why?

Key insight from Strike 18: rotation by 1 maps p -> 2r+1 where r = p - 2^{k-1}.
This map ALWAYS produces odd numbers. Other multiplications sometimes produce even.

Wait — M_k = 2^k-1 is odd. So a*p mod M_k has same parity as a*p.
If a is odd and p is odd: a*p is odd, a*p mod M_k is odd. All good.
If a is even (a=2): 2*p is even. 2*p mod M_k: since M_k is odd,
  2*p - M_k has parity opposite to M_k, so 2*p - M_k is odd!
  But only if 2*p > M_k. If 2*p < M_k, result is even.

For k-bit p: p >= 2^{k-1}, so 2p >= 2^k > M_k = 2^k-1.
So 2p mod M_k = 2p - M_k = 2p - 2^k + 1, which is ODD.

For x3: 3p mod M_k. If 3p < M_k: result is 3p (odd). If 3p > M_k: 3p - M_k
or 3p - 2*M_k. Parity: 3p is odd. M_k is odd. 3p - M_k is even!
3p - 2*M_k is odd again.

So x3 sometimes produces EVEN results, which can never be prime (>2).
This is why x2 wins!
"""
import math

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return s

N=65536; is_p=sieve(N)

def distinct_prime_factors(n):
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0: factors.add(d); n //= d
        d += 1
    if n > 1: factors.add(n)
    return sorted(factors)

# STRIKE 21: Parity of a*p mod M_k for different multipliers
print("=== STRIKE 21: Parity of a*p mod M_k ===")
print()

for k in [12, 16]:
    Mk = (1<<k)-1
    lo = 1<<(k-1); hi = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    print("k=%d:" % k)
    for a in [2, 3, 5, 7, 11]:
        if math.gcd(a, Mk) > 1: continue
        results = [(a * p) % Mk for p in prm]
        n_odd = sum(1 for r in results if r % 2 == 1)
        n_even = sum(1 for r in results if r % 2 == 0)
        in_range = sum(1 for r in results if lo <= r <= hi)
        in_range_odd = sum(1 for r in results if lo <= r <= hi and r % 2 == 1)
        print("  x%2d: odd=%d (%.1f%%)  even=%d (%.1f%%)  in_range=%d  in_range_odd=%d (%.1f%%)" % (
            a, n_odd, 100*n_odd/len(prm), n_even, 100*n_even/len(prm),
            in_range, in_range_odd, 100*in_range_odd/in_range if in_range else 0))
    print()

# STRIKE 22: Correct for parity — compare only ODD results
print("=== STRIKE 22: Enrichment among ODD results only ===")
print("Fair comparison: only count odd results that are in range")
print()

for k in [12, 14, 16]:
    Mk = (1<<k)-1
    lo = 1<<(k-1); hi = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]
    density = len(prm) / (hi - lo + 1)
    odd_density = len(prm) / ((hi - lo + 1) // 2)  # density among odd numbers

    print("k=%d:" % k)
    for a in [2, 3, 5, 7, 11, 13]:
        if math.gcd(a, Mk) > 1: continue
        primes_out = 0
        odd_in_range = 0
        for p in prm:
            r = (a * p) % Mk
            if lo <= r <= hi and r % 2 == 1:
                odd_in_range += 1
                if is_p[r]:
                    primes_out += 1
        rate = primes_out / odd_in_range if odd_in_range else 0
        enrichment = rate / odd_density if odd_density else 0
        rot = "  <-- ROTATION" if a == 2 else ""
        print("  x%2d: odd_in_range=%3d prime=%3d rate=%.4f enrichment=%.3f%s" % (
            a, odd_in_range, primes_out, rate, enrichment, rot))
    print()

# STRIKE 23: What about x2 in GENERAL (not mod M_k)?
# If p is prime and p > 2, is 2p+1 more likely prime than random?
# (These are "safe primes" — p where 2p+1 is also prime.)
# Our rotation gives 2r+1 where r = p - 2^{k-1}, not 2p+1.
# But the structure is similar: a linear map that preserves oddness.
print("=== STRIKE 23: Connection to safe primes ===")
print("Safe prime: p where 2p+1 is also prime.")
print("Our rotation: p -> 2(p - 2^{k-1}) + 1")
print()

# For k-bit primes, r = p - 2^{k-1} ranges from 0 to 2^{k-1}-1.
# mapped value = 2r + 1.
# If p is in [2^{k-1}, 2^k - 1], r is in [0, 2^{k-1}-1],
# mapped is in [1, 2^k - 1].
# Mapped is in [2^{k-1}, 2^k-1] iff r >= 2^{k-2}, i.e., p >= 3*2^{k-2}.
# So about half of rotated values are in k-bit range.

# The question: is 2r+1 prime correlated with p=2^{k-1}+r being prime?
# If r = (p-1)/2 and p is prime, then 2r+1 = p. Tautology.
# No — r = p - 2^{k-1}. So 2r+1 = 2p - 2^k + 1.
# Is 2p - 2^k + 1 prime when p is prime?

# This is the SAME as asking: is p + (p - 2^k + 1) = 2p - 2^k + 1 prime?
# The gap is: (2p - 2^k + 1) - p = p - 2^k + 1 (can be negative or positive).
# For p near 2^{k-1}: gap ≈ -2^{k-1} + 1 (negative, mapped is small).
# For p near 2^k: gap ≈ 2^k - 2^k + 1 = 1 (twin prime!).

print("For p near 2^k - 1: mapped ≈ 2p - 2^k + 1 ≈ p - 1 ≈ p")
print("For p near 2^{k-1}: mapped ≈ 1 (smallest primes)")
print()

k = 14; lo = 1<<(k-1); hi = (1<<k)-1
prm = [p for p in range(lo, hi+1) if is_p[p]]

# Correlation by position in range
thirds = len(prm) // 3
low_prm = prm[:thirds]
mid_prm = prm[thirds:2*thirds]
high_prm = prm[2*thirds:]

for label, subset in [("low third", low_prm), ("mid third", mid_prm), ("high third", high_prm)]:
    count = 0; in_range = 0
    for p in subset:
        r = 2*(p - lo) + 1
        if lo <= r <= hi:
            in_range += 1
            if is_p[r]:
                count += 1
    rate = count / in_range if in_range else 0
    density = len(prm) / (hi - lo + 1)
    print("  %s: %d primes, %d in range, %d mapped prime, enrichment=%.3f" % (
        label, len(subset), in_range, count,
        rate/density if density else 0))
    # Also: what range does mapped value fall in?
    mapped = [2*(p-lo)+1 for p in subset]
    print("    mapped range: [%d, %d], k-bit range: [%d, %d]" % (
        min(mapped), max(mapped), lo, hi))

print()
print("The high-third primes map to values NEAR themselves (p -> ~2p - 2^k + 1 ~ p).")
print("This is like twin prime / cousin prime proximity!")
