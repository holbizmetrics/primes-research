"""Experiment 3: Multi-probe intersection — numbers bright across multiple wavelengths"""
import math

def sieve(n):
    s=[True]*(n+1);s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i):s[j]=False
    return set(i for i,v in enumerate(s) if v)

def phase_score(n, N, wl, R=0.5):
    """Phase contribution of number n at wavelength wl (no Brennpunkt, pure Ramanujan axis)"""
    # Direct phase: how much does n contribute to coherent sum?
    k = 2*math.pi*wl
    r = n/N
    if r < 0.01: return 0
    z = 1 - 2*r
    ph = 2*k*z
    return math.cos(ph)  # real part of contribution

def phase_score_brennpunkt(n, N, t, wl, R=0.5):
    """Phase with Brennpunkt"""
    k = 2*math.pi*wl
    r = n/N
    if r < 0.01: return 0
    rn = r**(1-2*t) * R**(2*t)
    z = 1 - 2*rn
    ph = 2*k*z
    return math.cos(ph)

N = 1000
ps = sieve(N)

# Strategy: For each number, compute a "primality score" from multiple wavelengths
# A number that looks prime-like across many probes is more likely prime

# Use primorial wavelengths (known best from distill)
wavelengths_ram = [2, 3, 5, 6, 7, 10, 11, 13, 30]
wavelengths_brn = [(6, 0.02), (10, 0.02), (30, 0.02), (35, 0.02)]

print('=== Multi-Probe Primality Classifier ===')
print()

# Method 1: Sum of cos(phase) across wavelengths (Ramanujan axis, no Brennpunkt)
scores = {}
for n in range(2, N+1):
    s = sum(phase_score(n, N, wl) for wl in wavelengths_ram)
    scores[n] = s

# Sort by score
ranked = sorted(scores.items(), key=lambda x: -x[1])

# How well does this separate primes?
top_k_counts = []
for k in [50, 100, 168, 200, 300, 500]:
    top_k = set(n for n, s in ranked[:k])
    primes_in_top = sum(1 for n in top_k if n in ps)
    total_primes = len([n for n in range(2, N+1) if n in ps])
    precision = primes_in_top / k
    recall = primes_in_top / total_primes
    print(f'  Top {k:>3}: {primes_in_top:>3} primes (precision={precision:.3f}, recall={recall:.3f})')

print()

# Method 2: Product of |cos(phase)| — multiplicative combination
print('Method 2: Geometric mean of |cos(phase)| across wavelengths')
scores2 = {}
for n in range(2, N+1):
    phases = [phase_score(n, N, wl) for wl in wavelengths_ram]
    # Use sum of squares (energy across wavelengths)
    s = sum(p*p for p in phases)
    scores2[n] = s

ranked2 = sorted(scores2.items(), key=lambda x: -x[1])
for k in [50, 100, 168, 200, 300]:
    top_k = set(n for n, s in ranked2[:k])
    primes_in_top = sum(1 for n in top_k if n in ps)
    total_primes = len([n for n in range(2, N+1) if n in ps])
    precision = primes_in_top / k
    recall = primes_in_top / total_primes
    print(f'  Top {k:>3}: {primes_in_top:>3} primes (precision={precision:.3f}, recall={recall:.3f})')

print()

# Method 3: Use modular residue directly (this IS what the phases encode)
print('Method 3: Residue-class voting (what phases actually encode)')
# For each wavelength λ, coprime residues vote "prime-like"
from math import gcd
scores3 = {}
for n in range(2, N+1):
    votes = 0
    for lam in [2, 3, 5, 6, 7, 11, 13, 30]:
        if gcd(n, lam) == 1:
            votes += 1
    scores3[n] = votes

ranked3 = sorted(scores3.items(), key=lambda x: -x[1])
for k in [50, 100, 168, 200, 300]:
    top_k = set(n for n, s in ranked3[:k])
    primes_in_top = sum(1 for n in top_k if n in ps)
    total_primes = len([n for n in range(2, N+1) if n in ps])
    precision = primes_in_top / k
    recall = primes_in_top / total_primes
    print(f'  Top {k:>3}: {primes_in_top:>3} primes (precision={precision:.3f}, recall={recall:.3f})')

print()

# Method 4: Combined — residue voting + phase coherence
print('Method 4: Combined residue voting + phase energy')
scores4 = {}
for n in range(2, N+1):
    votes = sum(1 for lam in [2,3,5,6,7,11,13,30] if gcd(n,lam)==1)
    energy = sum(phase_score(n, N, wl)**2 for wl in wavelengths_ram)
    scores4[n] = votes * 10 + energy  # weighted combination

ranked4 = sorted(scores4.items(), key=lambda x: -x[1])
for k in [50, 100, 168, 200, 300]:
    top_k = set(n for n, s in ranked4[:k])
    primes_in_top = sum(1 for n in top_k if n in ps)
    total_primes = len([n for n in range(2, N+1) if n in ps])
    precision = primes_in_top / k
    recall = primes_in_top / total_primes
    print(f'  Top {k:>3}: {primes_in_top:>3} primes (precision={precision:.3f}, recall={recall:.3f})')

print()
# Baseline: random classifier
import random
random.seed(42)
print('Baseline: random selection')
for k in [50, 100, 168, 200, 300]:
    rand_pick = random.sample(range(2, N+1), k)
    primes_in = sum(1 for n in rand_pick if n in ps)
    total_primes = len([n for n in range(2, N+1) if n in ps])
    print(f'  Top {k:>3}: {primes_in:>3} primes (precision={primes_in/k:.3f}, recall={primes_in/total_primes:.3f})')

print()
print('=== N-Stability Check ===')
for N2 in [500, 2000, 5000]:
    ps2 = sieve(N2)
    scores_n = {}
    for n in range(2, N2+1):
        s = sum(phase_score(n, N2, wl) for wl in wavelengths_ram)
        scores_n[n] = s
    ranked_n = sorted(scores_n.items(), key=lambda x: -x[1])
    total_p = len([n for n in range(2,N2+1) if n in ps2])
    k = total_p  # pick exactly as many as there are primes
    top_k = set(n for n, s in ranked_n[:k])
    primes_in = sum(1 for n in top_k if n in ps2)
    print(f'  N={N2:5d}: top {k} by score -> {primes_in} primes (precision={primes_in/k:.3f})')
