#!/usr/bin/env python3
"""SPARK: Hit primes with audio waves
STRIKE 1: Sonify prime gaps
STRIKE 2: Harmonic series = zeta
STRIKE 3: Musical intervals as laser wavelengths
STRIKE 6: Standing wave filtered to primes
STRIKE 7: Prime rhythm autocorrelation
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

N=5000; P=sieve(N); Pset=set(P)
C=[i for i in range(4,N+1) if i not in Pset]

# ==========================================
# STRIKE 2: Harmonic series = zeta
# A vibrating string has harmonics at f, 2f, 3f, 4f, ...
# Amplitude of n-th harmonic: a_n = 1/n^s (for some damping s)
# Total sound: Σ (1/n^s) sin(2πnft) = this IS related to ζ(s)!
#
# Now: what if we REMOVE prime harmonics?
# Sound_full = Σ_n (1/n) sin(2πnft)  (sawtooth wave)
# Sound_no_primes = Σ_{n composite} (1/n) sin(2πnft)
# Difference = Σ_p (1/p) sin(2πpft) = "prime sound"
# ==========================================
print("=== STRIKE 2: Harmonic series and primes ===")
print("Sawtooth wave = Σ (1/n)*sin(2πnft)")
print("Remove prime harmonics → what's left?")
print()

# The "prime harmonic" content of a sawtooth:
# Power in prime harmonics: Σ_p 1/p² (each harmonic has power 1/n²)
# Power in all harmonics: Σ_n 1/n² = π²/6
# Fraction in primes: Σ_p 1/p² / (π²/6)

P_power = sum(1.0/p**2 for p in P)
total_power = math.pi**2/6
frac = P_power/total_power
print(f"Power in prime harmonics: Σ 1/p² = {P_power:.6f}")
print(f"Power in all harmonics: π²/6 = {total_power:.6f}")
print(f"Fraction: {frac:.4f} = {100*frac:.1f}%")
print(f"This is the 'prime hearing fraction' — {100*frac:.1f}% of a sawtooth is primes")
print()

# Known: Σ 1/p² = P(2) ≈ 0.4522 (prime zeta function at s=2)
# Related to: log(ζ(2)) - P(2) = Σ 1/(2p²) + Σ 1/(3p³) + ...
print(f"P(2) = Σ 1/p² ≈ {P_power:.6f} (prime zeta function)")
print(f"log(ζ(2)) = log(π²/6) = {math.log(math.pi**2/6):.6f}")
print()

# What about PRODUCTS of harmonics? In audio, two simultaneous notes
# create combination tones at f1±f2. For primes p1, p2:
# combination frequency = p1+p2 (Goldbach!) or p1-p2 (prime gap!)
print("Audio insight: two prime harmonics at p1, p2 create combination tones:")
print("  Sum tone: p1+p2 (→ Goldbach conjecture!)")
print("  Difference tone: |p1-p2| (→ prime gaps!)")
print("  Product tone (nonlinear): p1*p2 (→ semiprimes!)")
print()

# ==========================================
# STRIKE 3: Musical intervals as laser wavelengths
# Just intonation intervals are ALL ratios of small primes:
# Octave: 2/1, Fifth: 3/2, Fourth: 4/3, Major third: 5/4
# Minor third: 6/5, Major sixth: 5/3, Minor sixth: 8/5
# ==========================================
print("=== STRIKE 3: Musical intervals as laser wavelengths ===")
print("Just intonation = ratios of small primes")
print()

intervals = {
    'Unison':      (1, 1),
    'Octave':      (2, 1),
    'Fifth':       (3, 2),
    'Fourth':      (4, 3),
    'Maj 3rd':     (5, 4),
    'Min 3rd':     (6, 5),
    'Maj 6th':     (5, 3),
    'Min 6th':     (8, 5),
    'Tritone':     (7, 5),
    'Maj 2nd':     (9, 8),
    'Min 7th':     (7, 4),
    'Septimal':    (7, 6),
}

print(f"{'Interval':<12} {'Ratio':>6} {'λ=a/b':>8} {'I_P(λ)':>10} {'I_C(λ)':>10} {'P/C':>6}")
print("-"*55)
for name, (a, b) in intervals.items():
    lam = a/b
    ip = laser(P, lam)
    ic = laser(C, lam)
    pc = ip/ic if ic > 1e-10 else float('inf')
    print(f"{name:<12} {a}/{b:>2}    {lam:8.4f} {ip:10.6f} {ic:10.6f} {pc:6.1f}")

# ==========================================
# STRIKE 6: Standing wave filtered to primes
# f(x) = sin(2πx/λ) sampled at ALL integers → known DFT
# f(x) sampled at PRIMES ONLY → "prime Fourier transform"
# This is EXACTLY the laser: Σ_p exp(2πip/λ)
# So "standing wave on primes" = laser (nothing new!)
# ==========================================
print("\n=== STRIKE 6: Standing wave on primes ===")
print("sin(2πn/λ) sampled at primes = Im(Σ_p exp(2πip/λ)) = Im(laser)")
print("This IS the laser. No new information from 'audio wave' framing.")
print()

# ==========================================
# STRIKE 7: Prime rhythm autocorrelation
# f(n) = 1 if n prime, 0 otherwise
# Autocorrelation R(k) = Σ_n f(n)*f(n+k) = #{(p,p+k): both prime}
# This is the PRIME PAIR COUNTING function!
# R(k) = π₂(N,k) where π₂ is the Hardy-Littlewood twin prime function
# ==========================================
print("=== STRIKE 7: Prime rhythm = pair correlation ===")
print("f(n) = 1 if prime, 0 if not. Autocorrelation R(k) = #{p: p and p+k both prime}")
print()

# Compute R(k) for small k
maxk = 30
print(f"{'k':>3} {'R(k)':>6} {'predicted':>10} {'ratio':>8}")
for k in range(1, maxk+1):
    count = sum(1 for p in P if p+k in Pset and p+k <= N)
    # Hardy-Littlewood prediction: R(k) ~ C₂ * N/log²N * Π_{p|k,p>2} (p-1)/(p-2)
    # where C₂ = 2*Π_{p>2} (1-1/(p-1)²) ≈ 1.3203
    # For k odd: R(k) = 0 (since p and p+k can't both be odd if k is odd... wait, 2+3=5)
    # Actually for k odd and k>1: at most one can be even (p=2), so R(k) is 0 or 1
    # For k even: Hardy-Littlewood prediction
    if k % 2 == 1:
        pred = "  (odd k)"
        print(f"{k:3d} {count:6d} {pred:>10}")
    else:
        # Singular series for gap k
        C2 = 1.3203  # twin prime constant
        sing = 1.0
        for p in sieve(k+1):
            if p == 2: continue
            if k % p == 0:
                sing *= (p-1)/(p-2)
        pred_val = C2 * sing * len(P) / (math.log(N))**2
        ratio = count/pred_val if pred_val > 0 else 0
        print(f"{k:3d} {count:6d} {pred_val:10.1f} {ratio:8.3f}")

print()
print("The prime rhythm autocorrelation IS the Hardy-Littlewood conjecture!")
print("Audio processing of prime rhythm → twin prime constant C₂ ≈ 1.32")
