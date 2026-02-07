#!/usr/bin/env python3
"""SPARK: Primes as Information
STRIKE 1: Shannon entropy of prime gaps
STRIKE 2: Mutual information between consecutive gaps
STRIKE 3: Lempel-Ziv complexity of prime bitmap
"""
import math, sys
from collections import Counter

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(2,n+1) if s[i]]

N=100000; P=sieve(N); Pset=set(P)
gaps = [P[i+1]-P[i] for i in range(len(P)-1)]
print(f"N={N}, {len(P)} primes, {len(gaps)} gaps")
print()

# ==========================================
# STRIKE 1: Shannon entropy of gap distribution
# H = -Σ p(g) log₂ p(g)
# Compare to geometric distribution (max entropy for given mean)
# ==========================================
print("=== STRIKE 1: Shannon entropy of prime gaps ===")

gap_counts = Counter(gaps)
total = len(gaps)
probs = {g: c/total for g, c in gap_counts.items()}

H = -sum(p * math.log2(p) for p in probs.values() if p > 0)
print(f"Shannon entropy H = {H:.4f} bits per gap")
print(f"Mean gap = {sum(gaps)/len(gaps):.2f}")
print(f"Number of distinct gap values = {len(gap_counts)}")
print()

# Geometric distribution with same mean
mean_gap = sum(gaps)/len(gaps)
# Geometric: P(k) = (1-p)^(k-1) * p, mean = 1/p
# But gaps are even (>2), so adjust: P(g) for g=2,4,6,...
# Model: geometric on even gaps
even_gaps = [g for g in gaps if g >= 2]
mean_even = sum(even_gaps)/len(even_gaps)
p_geom = 2.0/mean_even  # parameter for geometric on {2,4,6,...}
H_geom = 0
for g, c in gap_counts.items():
    if g < 2: continue
    k = g // 2  # g = 2k
    p_g = p_geom * (1-p_geom)**(k-1)
    if p_g > 0:
        H_geom -= (c/total) * math.log2(p_g)  # cross-entropy

# Actually compute geometric entropy directly
H_geom_pure = -(math.log2(p_geom) + (1-p_geom)/p_geom * math.log2(1-p_geom))
print(f"Geometric distribution entropy (same mean) = {H_geom_pure:.4f} bits")
print(f"Efficiency = H_actual / H_geometric = {H/H_geom_pure:.4f}")
print(f"→ Primes use {H/H_geom_pure*100:.1f}% of maximum entropy")
print()

# Distribution of top gaps
print("Gap distribution (top 15):")
for g, c in sorted(gap_counts.items(), key=lambda x: -x[1])[:15]:
    p = c/total
    info = -math.log2(p)
    bar = '#' * int(p * 200)
    print(f"  g={g:3d}: {c:5d} ({p:.4f}) {info:.2f} bits  {bar}")

print()
sys.stdout.flush()

# ==========================================
# STRIKE 2: Mutual information between consecutive gaps
# I(g_n; g_{n+1}) = H(g_n) + H(g_{n+1}) - H(g_n, g_{n+1})
# ==========================================
print("=== STRIKE 2: Mutual information — does gap_n predict gap_{n+1}? ===")

# Joint distribution
joint = Counter()
for i in range(len(gaps)-1):
    joint[(gaps[i], gaps[i+1])] += 1

total_j = sum(joint.values())
H_joint = -sum((c/total_j)*math.log2(c/total_j) for c in joint.values() if c > 0)
MI = 2*H - H_joint  # since H(g_n) ≈ H(g_{n+1}) ≈ H
print(f"H(gap) = {H:.4f} bits")
print("H(gap_n, gap_n+1) = %.4f bits" % H_joint)
print(f"Mutual information I = {MI:.4f} bits")
print(f"Normalized MI = {MI/H:.4f} (fraction of entropy explained)")
print()

# Which gap pairs are most informative?
print("Most over-represented gap pairs (highest pointwise MI):")
pmi_list = []
for (g1, g2), c in joint.items():
    p_joint = c / total_j
    p1 = gap_counts[g1] / total
    p2 = gap_counts[g2] / total
    if p1 > 0 and p2 > 0 and p_joint > 0:
        pmi = math.log2(p_joint / (p1 * p2))
        if c >= 10:  # enough samples
            pmi_list.append((pmi, g1, g2, c))

pmi_list.sort(reverse=True)
for pmi, g1, g2, c in pmi_list[:10]:
    print(f"  ({g1:2d},{g2:2d}): PMI = {pmi:+.3f} bits, count = {c}")

print()
print("Most AVOIDED gap pairs:")
pmi_list.sort()
for pmi, g1, g2, c in pmi_list[:10]:
    print(f"  ({g1:2d},{g2:2d}): PMI = {pmi:+.3f} bits, count = {c}")

print()
sys.stdout.flush()

# ==========================================
# STRIKE 3: Lempel-Ziv complexity of prime bitmap
# The prime indicator: 0,0,1,1,0,1,0,1,0,0,0,1,...
# LZ complexity measures how compressible this is
# ==========================================
print("=== STRIKE 3: Lempel-Ziv complexity of prime bitmap ===")

def lz_complexity(s):
    """Lempel-Ziv 76 complexity"""
    n = len(s)
    i = 0; c = 1; l = 1
    while l + i < n:
        # Find longest match of s[i+1:i+l+1] in s[0:i+l]
        found = False
        sub = s[i+1:i+l+1]
        if sub in s[:i+l]:
            l += 1
        else:
            c += 1
            i += l
            l = 1
    return c

# Build bitmap
bitmap = ''.join('1' if i in Pset else '0' for i in range(2, N+1))

# LZ complexity
lz = lz_complexity(bitmap)

# For comparison: random bitmap with same density
import random
random.seed(42)
density = len(P) / (N-1)
rand_bitmap = ''.join('1' if random.random() < density else '0' for _ in range(len(bitmap)))
lz_rand = lz_complexity(rand_bitmap)

# Theoretical: random binary string LZ ~ n / log₂(n)
n = len(bitmap)
lz_theory = n / math.log2(n)

print(f"Bitmap length: {n}")
print(f"Prime density: {density:.4f}")
print(f"LZ complexity (primes): {lz}")
print(f"LZ complexity (random, same density): {lz_rand}")
print(f"LZ theoretical (random): {lz_theory:.0f}")
print(f"Ratio primes/random: {lz/lz_rand:.4f}")
print(f"Ratio primes/theoretical: {lz/lz_theory:.4f}")
print()
if lz < lz_rand:
    print(f"→ Primes are MORE compressible than random by {(1-lz/lz_rand)*100:.1f}%")
else:
    print(f"→ Primes are LESS compressible than random by {(lz/lz_rand-1)*100:.1f}%")
sys.stdout.flush()
