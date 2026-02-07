#!/usr/bin/env python3
"""SPARK: How do bits move when you multiply?
Primes are defined by multiplication (no nontrivial factors).
What does multiplication look like at the BIT level?
When you multiply two numbers, bits shift, carry, interact.
Is there a bit-level signature of primality?

SPRAY:
1. Bit patterns of primes vs composites
2. Hamming weight (popcount) of primes
3. Bit autocorrelation within primes
4. How multiplication scatters bits (multiply n*k, watch bits move)
5. XOR structure: n XOR (n*2), n XOR (n*3), etc.
6. Carry propagation: where do carries happen in n*k?
7. Bit-reversal: is reversed(prime) more/less likely prime?
"""
import math

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return s

N = 10000
is_prime = sieve(N)
primes = [n for n in range(2, N+1) if is_prime[n]]
composites = [n for n in range(4, N+1) if not is_prime[n] and n > 3]

def popcount(n):
    c = 0
    while n: c += n & 1; n >>= 1
    return c

def bits(n, width=0):
    if width == 0: width = n.bit_length()
    return [(n >> i) & 1 for i in range(width)]

# ==========================================
# STRIKE 1: Hamming weight of primes
# ==========================================
print("=== STRIKE 1: Hamming weight (popcount) ===")
print("Do primes have more/fewer 1-bits than composites?")
print()

# By bit length
for blen in [6, 8, 10, 12, 14]:
    lo = 1 << (blen-1); hi = (1 << blen) - 1
    pp = [p for p in primes if lo <= p <= hi]
    cc = [c for c in composites if lo <= c <= hi]
    if not pp or not cc: continue
    mean_p = sum(popcount(p) for p in pp) / len(pp)
    mean_c = sum(popcount(c) for c in cc) / len(cc)
    # Expected for uniform random: blen/2
    expected = blen / 2.0
    print("  %2d bits: primes=%.3f composites=%.3f expected=%.1f  diff=%+.3f" % (
        blen, mean_p, mean_c, expected, mean_p - mean_c))

print()

# ==========================================
# STRIKE 2: Bit autocorrelation
# For a number n with bits b0,b1,...,bk:
# A(d) = sum_i b_i * b_{i+d} / k
# Do primes have different bit autocorrelation?
# ==========================================
print("=== STRIKE 2: Bit autocorrelation ===")
print("A(d) = correlation between bit i and bit i+d")
print()

blen = 12
lo = 1 << (blen-1); hi = (1 << blen) - 1
pp12 = [p for p in primes if lo <= p <= hi]
cc12 = [c for c in composites if lo <= c <= hi]

print("12-bit numbers:")
print("  %3s %8s %8s %8s" % ("d", "A_prime", "A_comp", "diff"))
print("  " + "-"*32)
for d in range(1, 7):
    ap = 0.0; np = 0
    for p in pp12:
        b = bits(p, blen)
        for i in range(blen - d):
            ap += b[i] * b[i+d]; np += 1
    ap /= np if np else 1

    ac = 0.0; nc = 0
    for c in cc12:
        b = bits(c, blen)
        for i in range(blen - d):
            ac += b[i] * b[i+d]; nc += 1
    ac /= nc if nc else 1

    print("  %3d %8.4f %8.4f %8.4f" % (d, ap, ac, ap - ac))

print()

# ==========================================
# STRIKE 3: XOR scattering under multiplication
# When you compute n * 2, n * 3, etc., how do bits scatter?
# Measure: Hamming distance between n and n*k
# ==========================================
print("=== STRIKE 3: Bit scattering under multiplication ===")
print("H(n, n*k) = Hamming distance = number of bits that change")
print()

print("  %3s %10s %10s %8s" % ("k", "H_prime", "H_comp", "diff"))
print("  " + "-"*36)
for k in [2, 3, 5, 7, 11, 13]:
    hp = sum(popcount(p ^ (p*k)) for p in pp12) / len(pp12)
    hc = sum(popcount(c ^ (c*k)) for c in cc12) / len(cc12)
    print("  %3d %10.3f %10.3f %8.3f" % (k, hp, hc, hp - hc))

print()

# ==========================================
# STRIKE 4: Carry propagation in multiplication
# When computing n * k in binary, carries propagate.
# Count: how many positions generate a carry?
# Primes (odd, no small factors) might carry differently.
# ==========================================
print("=== STRIKE 4: Carry structure ===")
print("When you add n to itself (n*2=n+n), carries cascade.")
print("Longest carry chain in n+n:")
print()

def longest_carry(n):
    """Longest carry chain when computing n + n"""
    # n + n = 2n. Carry happens when bit i of n is 1.
    # Consecutive 1s create a chain.
    chain = 0; max_chain = 0
    while n:
        if n & 1:
            chain += 1
            max_chain = max(max_chain, chain)
        else:
            chain = 0
        n >>= 1
    return max_chain

def count_carries_mul(n, k):
    """Count carries when computing n * k via repeated addition"""
    # Simplified: count 1-bits in n*k XOR (n*(k-1) + n without carries)
    # Actually: count positions where n*k differs from n*(k-1) + n (no carry)
    result = n * k
    # Number of bit transitions
    return popcount(result ^ (result >> 1))

for blen in [10, 12, 14]:
    lo = 1 << (blen-1); hi = (1 << blen) - 1
    pp = [p for p in primes if lo <= p <= hi]
    cc = [c for c in composites if lo <= c <= hi]
    if not pp or not cc: continue
    lp = sum(longest_carry(p) for p in pp) / len(pp)
    lc = sum(longest_carry(c) for c in cc) / len(cc)
    # Bit transitions in n*3
    tp = sum(count_carries_mul(p, 3) for p in pp) / len(pp)
    tc = sum(count_carries_mul(c, 3) for c in cc) / len(cc)
    print("  %2d bits: carry_chain prime=%.3f comp=%.3f diff=%+.3f | transitions(n*3) p=%.3f c=%.3f" % (
        blen, lp, lc, lp-lc, tp, tc))

print()

# ==========================================
# STRIKE 5: Bit reversal and primality
# Reverse the bits of n. Is the result more/less likely prime?
# ==========================================
print("=== STRIKE 5: Bit reversal ===")
print("Reverse bits of n. Is reversed(prime) often prime?")
print()

def bit_reverse(n, width):
    result = 0
    for i in range(width):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result

for blen in [8, 10, 12, 14]:
    lo = 1 << (blen-1); hi = (1 << blen) - 1
    pp = [p for p in primes if lo <= p <= hi]
    rev_prime = 0; rev_comp = 0
    for p in pp:
        r = bit_reverse(p, blen)
        if r <= N and is_prime[r]:
            rev_prime += 1
    # Expected: density of primes in this range
    total_in_range = hi - lo + 1
    prime_density = len(pp) / total_in_range
    expected = len(pp) * prime_density
    print("  %2d bits: %d primes, %d with reversed also prime (expected %.1f), ratio=%.3f" % (
        blen, len(pp), rev_prime, expected, rev_prime/expected if expected > 0 else 0))

print()

# ==========================================
# STRIKE 6: Bit patterns forbidden in primes
# Which bit patterns never appear in primes?
# ==========================================
print("=== STRIKE 6: Forbidden/preferred bit suffixes ===")
print("Last k bits of primes (must be odd, not div by small primes)")
print()

for k in [3, 4, 5]:
    mask = (1 << k) - 1
    prime_hist = {}; all_hist = {}
    for n in range(1 << (k+3), N+1):
        suffix = n & mask
        if is_prime[n]:
            prime_hist[suffix] = prime_hist.get(suffix, 0) + 1
        all_hist[suffix] = all_hist.get(suffix, 0) + 1

    total_p = sum(prime_hist.values())
    total_a = sum(all_hist.values())

    # Sort by enrichment
    enrichment = []
    for suffix in range(1 << k):
        pc = prime_hist.get(suffix, 0)
        ac = all_hist.get(suffix, 0)
        if ac > 0:
            obs = pc / total_p if total_p > 0 else 0
            exp = ac / total_a
            enrichment.append((suffix, obs/exp if exp > 0 else 0, pc))

    enrichment.sort(key=lambda x: -x[1])
    print("  %d-bit suffix (top 5 enriched, bottom 5 depleted):" % k)
    for suffix, enr, count in enrichment[:5]:
        print("    ...%s: enrichment=%.3f (count=%d)%s" % (
            bin(suffix)[2:].zfill(k), enr, count,
            " MUST be odd" if suffix % 2 == 1 else " FORBIDDEN (even)"))
    print("    ...")
    for suffix, enr, count in enrichment[-3:]:
        print("    ...%s: enrichment=%.3f (count=%d)%s" % (
            bin(suffix)[2:].zfill(k), enr, count,
            " div by %d" % ([d for d in [2,3,4,5,6,7,8] if suffix % d == 0 and d > 1][0]) if any(suffix % d == 0 for d in [2,3,4,5]) else ""))
    print()

# ==========================================
# STRIKE 7: Multiplication as bit permutation
# n * 2 = left shift. n * 3 = n + (n<<1).
# What's the "bit signature" of multiplying by each small prime?
# Compute the BIT CORRELATION MATRIX:
# C(i,j) = correlation between bit i of n and bit j of n*p
# ==========================================
print("=== STRIKE 7: Bit correlation matrix of multiplication ===")
print("C(i,j) = P(bit j of n*p = 1 | bit i of n = 1)")
print("For 8-bit primes, multiplied by 3:")
print()

blen = 8; lo = 1<<(blen-1); hi = (1<<blen)-1
pp8 = [p for p in primes if lo <= p <= hi]
mult = 3
out_len = (blen + 2)  # n*3 can be up to blen+2 bits

# Correlation matrix
C = [[0.0]*out_len for _ in range(blen)]
N1 = [0]*blen  # count of n with bit i = 1

for p in pp8:
    prod = p * mult
    nb = bits(p, blen)
    pb = bits(prod, out_len)
    for i in range(blen):
        if nb[i]:
            N1[i] += 1
            for j in range(out_len):
                if pb[j]:
                    C[i][j] += 1

# Normalize
for i in range(blen):
    if N1[i] > 0:
        for j in range(out_len):
            C[i][j] /= N1[i]

print("Bit of n -> Bit of n*3:")
print("    ", end="")
for j in range(out_len): print(" b%d " % j, end="")
print()
for i in range(blen):
    print("b%d: " % i, end="")
    for j in range(out_len):
        v = C[i][j]
        if v > 0.7: ch = "###"
        elif v > 0.4: ch = " # "
        elif v > 0.2: ch = " . "
        else: ch = "   "
        print(ch, end=" ")
    print()

print()
print("### = strong correlation (>0.7)")
print(" #  = medium (0.4-0.7)")
print(" .  = weak (0.2-0.4)")
print()
print("For n*2 (pure shift), this would be a perfect diagonal offset by 1.")
print("For n*3 = n + 2n, the carries create OFF-DIAGONAL correlations.")
print("These off-diagonal terms are where multiplication 'mixes' bits.")
