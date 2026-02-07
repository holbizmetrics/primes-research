#!/usr/bin/env python3
"""SPARK: Overtones and twin prime resonances
If primes are a "chord", twin primes are a "harmonic series within a harmonic series"
The overtone structure of the twin prime subsequence should be different.

Key ideas:
1. Twin primes (p, p+2) as a single "note" — what's their overtone series?
2. The "fundamental frequency" of twin primes = 2 (their defining gap)
3. Laser on twins vs laser on all primes — where do they differ?
4. Overtones: laser at λ, 2λ, 3λ, ... on twin primes
5. The twin prime constant C₂ should appear as a resonance amplitude
"""
import math

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(2,n+1) if s[i]]

def laser(values, lam):
    ar=ai=0
    for v in values:
        ph=2*math.pi*v/lam; ar+=math.cos(ph); ai+=math.sin(ph)
    n=len(values)
    return (ar*ar+ai*ai)/(n*n) if n>0 else 0

N=50000; P=sieve(N); Pset=set(P)

# Extract prime subsets by gap type
twins = [p for p in P if p+2 in Pset]  # lower twin
cousins = [p for p in P if p+4 in Pset]  # cousin primes (gap 4)
sexys = [p for p in P if p+6 in Pset]  # sexy primes (gap 6)
isolated = [p for p in P if p-2 not in Pset and p+2 not in Pset]

print(f"N = {N}")
print(f"All primes: {len(P)}")
print(f"Twin primes (lower): {len(twins)}")
print(f"Cousin primes (gap 4): {len(cousins)}")
print(f"Sexy primes (gap 6): {len(sexys)}")
print(f"Isolated primes: {len(isolated)}")
print()

# ==========================================
# STRIKE 1: Overtone series — laser at λ = k (harmonics) for each subset
# The "fundamental" for twin primes is their gap = 2
# So check λ = 2, 4, 6, 8, ... (even harmonics)
# And λ = 1, 3, 5, 7, ... (odd harmonics)
# ==========================================
print("=== OVERTONE SERIES: laser at harmonics ===")
print(f"{'λ':>3} {'I_all':>10} {'I_twin':>10} {'I_cousin':>10} {'I_sexy':>10} {'I_isol':>10} {'twin/all':>10}")
print("-"*75)

for lam in range(2, 31):
    i_all = laser(P, lam)
    i_tw = laser(twins, lam)
    i_co = laser(cousins, lam)
    i_sx = laser(sexys, lam)
    i_is = laser(isolated, lam)
    ratio = i_tw/i_all if i_all > 1e-10 else float('inf')
    print(f"{lam:3d} {i_all:10.6f} {i_tw:10.6f} {i_co:10.6f} {i_sx:10.6f} {i_is:10.6f} {ratio:10.3f}")

# ==========================================
# STRIKE 2: The twin prime "beat frequency"
# Twin primes differ by 2, so exp(2πi(p+2)/λ) = exp(2πip/λ) * exp(4πi/λ)
# Playing BOTH twins: Σ_{(p,p+2) twin} [exp(2πip/λ) + exp(2πi(p+2)/λ)]
#                    = Σ exp(2πip/λ) * [1 + exp(4πi/λ)]
# = 2*cos(2π/λ) * Σ exp(2πi(p+1)/λ)  (after factoring)
# The MODULATION FACTOR is 2*cos(2π/λ)
# This is 0 when λ = 4/k for odd k → destructive at λ=4, 4/3, 4/5...
# This is maximum (=2) when λ = 1/k for integer k → constructive at all integers
# ==========================================
print("\n=== TWIN PRIME BEAT PATTERN ===")
print("Playing both p and p+2 simultaneously:")
print("Modulation factor = 2*cos(2π/λ)")
print()
print(f"{'λ':>5} {'mod_factor':>12} {'I_both':>10} {'I_lower':>10} {'ratio':>8}")
for lam in [2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 15, 21, 30]:
    mod = 2*math.cos(2*math.pi/lam)
    # Compute "both twins" laser
    both = []
    for p in P:
        if p+2 in Pset:
            both.extend([p, p+2])
    i_both = laser(both, lam)
    i_lower = laser(twins, lam)
    ratio = i_both/i_lower if i_lower > 1e-10 else float('inf')
    print(f"{lam:5d} {mod:+12.4f} {i_both:10.6f} {i_lower:10.6f} {ratio:8.3f}")

# ==========================================
# STRIKE 3: Twin prime coherence vs Hardy-Littlewood prediction
# For twin primes, the analog of Ramanujan sums involves
# the TWIN PRIME singular series:
# S₂(q) = Π_{p|q, p>2} (p-1)/(p-2) × μ(q)²/φ(q)²
# (extra factor from twin prime condition)
# ==========================================
print("\n=== TWIN PRIME SINGULAR SERIES ===")
print("Prediction: I_twin(q) ~ S₂(q) = μ(q)²/φ(q)² × Π_{p|q,p>2} (p-1)/(p-2)")
print()

def mobius(n):
    if n==1: return 1
    d=2; temp=n; nf=0
    while d*d<=temp:
        if temp%d==0:
            nf+=1; temp//=d
            if temp%d==0: return 0
        d+=1
    if temp>1: nf+=1
    return (-1)**nf

def euler_phi(n):
    result=n; d=2; temp=n
    while d*d<=temp:
        if temp%d==0:
            while temp%d==0: temp//=d
            result-=result//d
        d+=1
    if temp>1: result-=result//temp
    return result

def prime_factors(n):
    factors = []
    d = 2
    temp = n
    while d*d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0: temp //= d
        d += 1
    if temp > 1: factors.append(temp)
    return factors

print(f"{'q':>3} {'μ(q)':>5} {'I_twin':>10} {'μ²/φ²':>10} {'S₂(q)':>10} {'I_tw/S₂':>10}")
print("-"*55)
for q in range(2, 31):
    mu = mobius(q)
    if mu == 0:
        i_tw = laser(twins, q)
        print(f"{q:3d} {mu:5d} {i_tw:10.6f}      0          0      (dark)")
        continue
    phi = euler_phi(q)
    base = 1.0/(phi**2)  # μ²/φ²
    # Twin prime correction
    correction = 1.0
    for p in prime_factors(q):
        if p > 2:
            correction *= (p-1)/(p-2)
    S2 = base * correction
    i_tw = laser(twins, q)
    ratio = i_tw/S2 if S2 > 1e-10 else 0
    print(f"{q:3d} {mu:5d} {i_tw:10.6f} {base:10.6f} {S2:10.6f} {ratio:10.3f}")

# ==========================================
# STRIKE 4: Can we HEAR the twin prime constant?
# C₂ = 2 × Π_{p>2} (1 - 1/(p-1)²) ≈ 1.3203
# This should appear as a ratio between twin prime and all-prime coherence
# ==========================================
print("\n=== CAN WE HEAR THE TWIN PRIME CONSTANT? ===")
print("C₂ = 2 × Π_{p>2} (1 - 1/(p-1)²) ≈ 1.3203")
print()

# The density of twin primes ~ C₂/(log N)² compared to primes ~ 1/log N
# So n_twin/n_prime ~ C₂/log N
# I_twin = coherence of TWIN subset
# The twin prime singular series S₂(q) relates I_twin to I_all via:
# I_twin(q) ≈ I_all(q) × correction involving C₂

# Actually, let's just measure the ratio directly
print("Ratio I_twin(q) / I_all(q) for squarefree q:")
ratios = []
for q in [3, 5, 6, 7, 10, 11, 13, 14, 15]:
    if mobius(q) == 0: continue
    i_tw = laser(twins, q)
    i_all = laser(P, q)
    r = i_tw/i_all if i_all > 1e-10 else 0
    # Predicted correction: Π_{p|q, p>2} (p-1)/(p-2)
    corr = 1.0
    for p in prime_factors(q):
        if p > 2: corr *= (p-1)/(p-2)
    ratios.append(r)
    print(f"  q={q:2d}: I_twin/I_all = {r:.4f}  predicted_correction = {corr:.4f}")

print(f"\n  Mean ratio: {sum(ratios)/len(ratios):.4f}")
print(f"  This should relate to density correction × singular series")
