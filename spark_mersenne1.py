#!/usr/bin/env python3
"""SPARK: Mersenne bit rotation — WHY does d=±1 preserve primality 2.3x?

In k-bit field, rotation left by d = multiplication by 2^d mod (2^k - 1).
So d=1 means: p -> 2p mod M_k where M_k = 2^k - 1.

STRIKE 1: Does the enrichment depend on whether M_k is prime (Mersenne prime)?
STRIKE 2: What primes survive rotation? Are they special?
STRIKE 3: How does enrichment scale with bit length?
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

# STRIKE 1: Enrichment vs bit length, noting Mersenne prime status
# M_k = 2^k-1 is prime for k = 2,3,5,7,13,17,19,31,...
mersenne_exp = {2,3,5,7,13,17,19,31}

print("=== STRIKE 1: Rotation d=1 enrichment vs bit length ===")
print("Is enrichment higher when 2^k-1 is Mersenne prime?")
print()
print("%3s %6s %5s %5s %7s %8s  %s" % ("k","#prm","rot_p","exp","ratio","M_k","note"))
print("-"*60)

ratios_mersenne = []
ratios_non = []

for k in range(5, 17):
    lo = 1<<(k-1); hi = (1<<k)-1
    Mk = (1<<k)-1
    is_mersenne = is_p[Mk] if Mk <= N else (k in mersenne_exp)

    prm = [p for p in range(lo, hi+1) if is_p[p]]
    if not prm: continue

    # Rotate by 1 (= multiply by 2 mod M_k)
    count = 0
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi and is_p[r]:
            count += 1

    density = len(prm) / (hi - lo + 1)
    expected = len(prm) * density
    ratio = count / expected if expected > 0 else 0

    tag = "MERSENNE" if is_mersenne else ""
    print("%3d %6d %5d %5.1f %7.3f %8d  %s" % (k, len(prm), count, expected, ratio, Mk, tag))

    if is_mersenne:
        ratios_mersenne.append(ratio)
    else:
        ratios_non.append(ratio)

print()
if ratios_mersenne:
    print("Mean enrichment (Mersenne k): %.3f" % (sum(ratios_mersenne)/len(ratios_mersenne)))
if ratios_non:
    print("Mean enrichment (non-Mersenne k): %.3f" % (sum(ratios_non)/len(ratios_non)))
print()

# STRIKE 2: Which primes survive? Look at residues mod small numbers
print("=== STRIKE 2: What's special about rotation-surviving primes? ===")
print()

k = 12; lo = 1<<(k-1); hi = (1<<k)-1
prm = [p for p in range(lo, hi+1) if is_p[p]]
survivors = []
for p in prm:
    r = bit_rotate(p, 1, k)
    if lo <= r <= hi and is_p[r]:
        survivors.append(p)

print("k=%d: %d primes, %d survive rotation (%.1f%%)" % (k, len(prm), len(survivors), 100*len(survivors)/len(prm)))

# Mod structure of survivors vs all primes
for m in [3, 5, 7, 11, 13]:
    surv_res = {}
    all_res = {}
    for p in survivors:
        r = p % m
        surv_res[r] = surv_res.get(r, 0) + 1
    for p in prm:
        r = p % m
        all_res[r] = all_res.get(r, 0) + 1

    print("  mod %2d:" % m, end="")
    for r in sorted(set(list(surv_res.keys()) + list(all_res.keys()))):
        sf = surv_res.get(r, 0) / len(survivors) if survivors else 0
        af = all_res.get(r, 0) / len(prm)
        if af > 0:
            enr = sf / af
            flag = " *" if abs(enr - 1) > 0.15 else ""
            print("  r=%d: %.2f%s" % (r, enr, flag), end="")
    print()

print()

# STRIKE 3: The rotation IS multiplication by 2 mod M_k.
# So we're asking: if p is prime, is 2p mod M_k also prime?
print("=== STRIKE 3: Direct verification — rotation = 2p mod M_k ===")
k = 12; Mk = (1 << k) - 1
print("k=%d, M_k=%d = 2^%d - 1" % (k, Mk, k))
print()

mismatches = 0
for p in prm[:20]:
    rotated = bit_rotate(p, 1, k)
    arith = (2 * p) % Mk
    match = "OK" if rotated == arith else "MISMATCH"
    if rotated != arith: mismatches += 1
    if p < prm[10]:
        print("  p=%d: rot=%d, 2p mod %d=%d  %s" % (p, rotated, Mk, arith, match))

print("  ... checked %d primes, %d mismatches" % (len(prm), mismatches))
