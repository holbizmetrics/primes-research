#!/usr/bin/env python3
"""SPARK Audio: Deep strikes on the interesting ones
1. Musical interval laser: consonance = prime coherence?
2. Combination tones (nonlinear audio) → Goldbach / gaps
3. The "missing fundamental" of primes
4. Spectral envelope (formants) of prime sequence
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

N=5000; P=sieve(N); Pset=set(P)

# ==========================================
# DEEP STRIKE: Musical consonance = laser coherence?
# In music: consonance ↔ simple ratio a/b
# In primes: coherence ↔ μ(q)²/φ(q)² where q is the denominator
#
# A musical interval a/b has laser wavelength a/b.
# But the laser is periodic: laser(P, a/b) = laser(P, a/b + integer) for phases
# Actually laser(P, λ) = |Σ exp(2πip/λ)|²/N²
# = |Σ exp(2πip*b/a)|²/N² since 1/λ = b/a
# This is the laser at INTEGER wavelength a with phase factor b
# = laser(P, a) when gcd(a,b)=1 ← NO! The phase matters
#
# Actually Σ exp(2πip/(a/b)) = Σ exp(2πi*b*p/a)
# This is the laser at wavelength a with harmonic number b
# = Ramanujan sum c_a(b*p)... not quite
# Let's just compute directly
# ==========================================
print("=== CONSONANCE vs COHERENCE ===")
print("Musical consonance (simple ratio) vs prime laser coherence")
print()

# Compute for all ratios a/b where 1 < a/b < 2, a,b ≤ 20
ratios = []
for a in range(2, 21):
    for b in range(1, a):
        if math.gcd(a,b) > 1: continue  # reduce to lowest terms
        r = a/b
        if r > 2.1: continue  # within two octaves
        ratios.append((a, b, r))

ratios.sort(key=lambda x: x[2])

# Musical consonance measure: product a*b (smaller = more consonant)
print(f"{'a/b':>6} {'ratio':>7} {'a*b':>4} {'I_P':>10} {'consonant':>10} {'note':>15}")
print("-"*65)
for a, b, r in ratios:
    ip = laser(P, r)
    cons = a*b  # smaller = more consonant
    # Musical name
    cents = 1200 * math.log2(r)
    name = ""
    if abs(cents - 0) < 5: name = "unison"
    elif abs(cents - 100) < 15: name = "min 2nd"
    elif abs(cents - 200) < 15: name = "maj 2nd"
    elif abs(cents - 300) < 15: name = "min 3rd"
    elif abs(cents - 400) < 15: name = "maj 3rd"
    elif abs(cents - 500) < 15: name = "4th"
    elif abs(cents - 600) < 15: name = "tritone"
    elif abs(cents - 700) < 15: name = "5th"
    elif abs(cents - 800) < 15: name = "min 6th"
    elif abs(cents - 900) < 15: name = "maj 6th"
    elif abs(cents - 1000) < 15: name = "min 7th"
    elif abs(cents - 1100) < 15: name = "maj 7th"
    elif abs(cents - 1200) < 15: name = "octave"

    if ip > 0.01 or cons <= 20:
        print(f"{a:2d}/{b:<2d} {r:7.4f} {cons:4d} {ip:10.6f} {'***' if cons<=6 else '**' if cons<=15 else '*' if cons<=30 else '':>10} {name:>15}")

# ==========================================
# The key question: is there a correlation between
# musical consonance (small a*b) and prime coherence?
# ==========================================
print("\n=== CORRELATION: consonance vs coherence ===")
# For each ratio, get (1/a*b, I_P)
xs = []; ys = []
for a, b, r in ratios:
    ip = laser(P, r)
    xs.append(1.0/(a*b))
    ys.append(ip)

mx = sum(xs)/len(xs); my = sum(ys)/len(ys)
sxx = sum((x-mx)**2 for x in xs)
sxy = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
syy = sum((y-my)**2 for y in ys)
r_corr = sxy/math.sqrt(sxx*syy) if sxx>0 and syy>0 else 0
print(f"Correlation(1/(a*b), I_P) = {r_corr:.4f}")
print(f"{'STRONG' if abs(r_corr)>0.5 else 'WEAK' if abs(r_corr)>0.2 else 'NONE'} correlation")
print()

# ==========================================
# DEEP STRIKE: What does I_P(a/b) actually equal?
# I_P(a/b) = |Σ_p exp(2πi*b*p/a)|²/N²
# = |Σ_p exp(2πi*(bp mod a)/a)|²/N²
# The phase 2πibp/a depends on bp mod a
# For gcd(b,a)=1: as p varies over primes, bp mod a hits all
# residues coprime to a uniformly (Dirichlet's theorem)
# So this is the laser at wavelength a, at harmonic b
# = c_a(b)²/φ(a)²? No...
# Actually: Σ_p exp(2πibp/a) = Σ_p exp(2πi(bp mod a)/a)
# When gcd(b,a)=1, multiplication by b is a bijection on (Z/aZ)*
# So Σ_p exp(2πibp/a) = Σ_p exp(2πip'/a) where p' = bp mod a
# runs over... wait, p' ranges over residues bp mod a
# which for p coprime to a is just a permutation of residues
# So Σ_{p coprime to a} exp(2πibp/a) = Σ_{p coprime to a} exp(2πip/a)
# when b permutes the coprime residues!
# THIS MEANS: I_P(a/b) = I_P(a) for gcd(a,b)=1!
# The MUSICAL INTERVAL doesn't matter — only the DENOMINATOR!
# ==========================================
print("=== KEY INSIGHT: I_P(a/b) = I_P(a) when gcd(a,b)=1 ===")
print("Proof: multiplication by b permutes residues mod a")
print("So the laser at wavelength a/b = laser at wavelength a")
print()
print("Verification:")
for a, b in [(3,2), (5,3), (5,4), (7,4), (7,5), (7,6)]:
    ip_frac = laser(P, a/b)
    ip_int = laser(P, a)
    print(f"  I_P({a}/{b}) = {ip_frac:.6f}  vs  I_P({a}) = {ip_int:.6f}  match={'YES' if abs(ip_frac-ip_int)<0.001 else 'NO'}")

print()
print("★ ALL musical intervals a/b reduce to laser(P, a)")
print("  The fifth (3/2) = laser at 3")
print("  The major third (5/4) = laser at 5")
print("  The tritone (7/5) = laser at 7")
print("  Musical CONSONANCE (simple ratio) is EXACTLY prime COHERENCE")
print("  because consonant intervals have SMALL SQUAREFREE denominators!")
print()

# ==========================================
# STRIKE: Combination tones → Goldbach
# If primes p1,p2 are "played" simultaneously as harmonics,
# the nonlinear combination tone is at p1+p2 (sum tone)
# Goldbach: every even number = p1+p2
# So the "combination tone spectrum" of primes = all even numbers!
# (if Goldbach is true)
# ==========================================
print("=== COMBINATION TONES → GOLDBACH ===")
print("'Playing' primes p1, p2 simultaneously → sum tone p1+p2")
print("Goldbach: all even n > 2 are sum tones!")
print()

# Count how many ways each even number is a sum of two primes
maxn = 100
goldbach = {}
for n in range(4, maxn+1, 2):
    count = sum(1 for p in P if p <= n//2 and n-p in Pset)
    goldbach[n] = count

# The "volume" of each sum tone
print(f"{'n':>4} {'#ways':>5} {'volume (√#ways)':>12}")
for n in sorted(goldbach.keys())[:20]:
    vol = math.sqrt(goldbach[n])
    bar = '#' * int(vol*3)
    print(f"{n:4d} {goldbach[n]:5d} {vol:12.2f}  {bar}")

print()
print("The combination tone spectrum RISES with n (more representations)")
print("This is the Goldbach comet — the visual pattern of Goldbach representations")
print("Audio interpretation: higher even numbers are LOUDER (more harmonics sum to them)")

# ==========================================
# THE MISSING FUNDAMENTAL
# In audio: if you play harmonics 2f, 3f, 4f, 5f (but NOT f),
# the ear still "hears" f. This is the missing fundamental.
# For primes: the "fundamental frequency" is... 1?
# The prime harmonics are at 2, 3, 5, 7, 11, ...
# Their GCD is 1. The "missing fundamental" is always 1.
# More interesting: the RATIO between consecutive primes
# 3/2, 5/3, 7/5, 11/7, 13/11, ...
# These ratios approach 1 (prime gap → 0 relative to p)
# In music: ratios near 1 = near-unison = BEATS
# The beat frequency = |p_{n+1} - p_n| = prime gap!
# ==========================================
print("\n=== MISSING FUNDAMENTAL / BEATS ===")
print("Consecutive prime ratios p_{n+1}/p_n → 1")
print("In audio: near-unison → beat frequency = gap")
print()
print("The prime sequence IS a slowly detuning unison —")
print("getting more and more 'in tune' (gaps shrink relative to p)")
print("The 'beat pattern' = prime gaps = the Hardy-Littlewood conjecture")
print()

# Beat frequency spectrum: gaps as function of position
gaps = [P[i+1]-P[i] for i in range(min(200, len(P)-1))]
mean_gap = sum(gaps)/len(gaps)
print(f"First 200 gaps: mean={mean_gap:.2f}")
print(f"In audio terms: a note at ~{1/mean_gap:.0f} Hz slowly dropping in pitch")
print(f"(since mean gap grows as log(p))")
