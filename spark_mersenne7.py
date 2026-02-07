#!/usr/bin/env python3
"""STRIKE 18-20: WHY is d=1 special among all rotations?

d=1 rotation = multiply by 2.
d=2 = multiply by 4.
d=3 = multiply by 8.
...

All preserve coprimality to M_k. But d=1 gives ~1.7x more enrichment.

Hypothesis: d=1 (multiply by 2) preserves PROXIMITY.
2p is "close" to p (it's just p shifted left one bit).
Other multiplications by 2^d scatter more.

In number terms: 2p mod M_k = 2p if 2p < M_k (i.e., p < M_k/2).
Since p is k-bit, p >= M_k/2, so 2p >= M_k, meaning 2p mod M_k = 2p - M_k.
So: rotated(p) = 2p - (2^k - 1) = 2p - 2^k + 1.

For k-bit p: p = 2^{k-1} + r where 0 <= r < 2^{k-1}.
rotated(p) = 2(2^{k-1} + r) - 2^k + 1 = 2r + 1.

So d=1 rotation maps p -> 2*(p - 2^{k-1}) + 1 = 2r + 1 where r = p mod 2^{k-1}.
This is a LINEAR MAP! It maps the lower k-1 bits linearly.
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

# STRIKE 18: Verify the linear map
print("=== STRIKE 18: d=1 rotation is a LINEAR map ===")
print()
print("For k-bit prime p (MSB=1): p = 2^{k-1} + r")
print("rotate(p,1,k) = 2r + 1")
print("This is ALWAYS ODD (LSB=1) and < 2^k.")
print()

k = 12; lo = 1<<(k-1); hi = (1<<k)-1
prm = [p for p in range(lo, hi+1) if is_p[p]]

for p in prm[:10]:
    r = p - lo  # lower k-1 bits
    predicted = 2*r + 1
    actual = bit_rotate(p, 1, k)
    print("  p=%d r=%d  predicted=2r+1=%d  actual=%d  match=%s" % (
        p, r, predicted, actual, predicted == actual))

print()
print("For d=2: p = 2^{k-1} + r, rotate(p,2,k) = ?")
# p in binary: 1 b_{k-2} ... b_1 b_0
# rotate left by 2: b_{k-2} ... b_1 b_0 1 b_{k-2}
# Wait, that's not right. Let me think about this differently.
# rotate(p, 2, k) = (p << 2 | p >> (k-2)) & ((1<<k)-1)
# p = 2^{k-1} + r
# p << 2 = 2^{k+1} + 4r
# p >> (k-2) = (2^{k-1} + r) >> (k-2) = 2 + (r >> (k-2))
# Combined: (2^{k+1} + 4r + 2 + (r >> (k-2))) & (2^k - 1)
# = (4r + 2 + (r >> (k-2))) mod 2^k
# Depends on MSB of r!

print("For d=2: rotate(p,2,k) depends on bit k-2 of p -> NOT linear in simple way")
print()

# STRIKE 19: d=1 maps primes to ODD numbers near 2p
# Key: 2p - (2^k - 1) is always odd.
# And: 2p is close to p (within factor 2).
# The arithmetic proximity means: if p avoids small factors,
# 2p likely avoids them too (deterministically for odd factors,
# and 2p is even but we subtract M_k which is odd, so 2p - M_k is odd).
#
# For d=2: 4p mod M_k. This scatters p further in the number line.
# The "proximity bonus" is weaker.
#
# QUANTIFY: distance between p and rotate(p,d,k)
print("=== STRIKE 19: Distance |p - rotate(p,d,k)| ===")
print()

for k in [12, 16]:
    lo = 1<<(k-1); hi = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    print("k=%d:" % k)
    for d in range(1, min(k, 8)):
        dists = []
        for p in prm:
            r = bit_rotate(p, d, k)
            if lo <= r <= hi:
                dists.append(abs(p - r))
        if dists:
            mean_d = sum(dists) / len(dists)
            max_d = max(dists)
            range_size = hi - lo
            print("  d=%d: mean_dist=%.0f (%.1f%% of range)  max=%.0f" % (
                d, mean_d, 100*mean_d/range_size, max_d))
    print()

# STRIKE 20: The REAL test — compare enrichment of multiply-by-2 mod M_k
# versus multiply-by-3 mod M_k (which also preserves coprimality!)
# If d=1 is special because of the linear/proximity structure,
# then multiply-by-3 should give LESS enrichment (3 is not a power of 2,
# so it's not a rotation, and scatters differently).
print("=== STRIKE 20: Rotation (x2) vs multiply-by-3,5,7 mod M_k ===")
print("All preserve coprimality. Does rotation (x2) beat them?")
print()

for k in [12, 14, 16]:
    lo = 1<<(k-1); hi = (1<<k)-1
    Mk = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]
    density = len(prm) / (hi - lo + 1)

    print("k=%d (%d primes):" % (k, len(prm)))
    for mult in [2, 3, 5, 7, 11, 13]:
        if math.gcd(mult, Mk) > 1:
            # mult shares a factor with M_k, skip
            continue
        count = 0
        in_range = 0
        for p in prm:
            r = (mult * p) % Mk
            if lo <= r <= hi:
                in_range += 1
                if r <= N and is_p[r]:
                    count += 1
        rate = count / in_range if in_range else 0
        expected_rate = density
        enrichment = rate / expected_rate if expected_rate > 0 else 0
        rot = "  <-- ROTATION" if mult == 2 else ""
        print("  x%2d: count=%3d in_range=%3d rate=%.4f enrichment=%.3f%s" % (
            mult, count, in_range, rate, enrichment, rot))
    print()
