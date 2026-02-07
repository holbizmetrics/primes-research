#!/usr/bin/env python3
"""SPARK: The Unified Probe
Connect ALL physical metaphors to the factor lattice.
Audio wave, laser beam, X-ray, gamma ray — at what "energy"
does each probe see the prime structure best?

The factor lattice has weights w(p) = 1/(p-1)^2.
Each physical probe samples this at different points.

SPRAY:
1. Audio harmonic spectrum: heard at ALL harmonics simultaneously — 
   total energy = sum of lattice weights. What's the "sound" of the lattice?
2. X-ray (short wavelength): high-q laser probes high lattice dimensions.
   Does the lattice have structure beyond p=2,3?
3. Broadband sweep: scan wavelength continuously, find the TRANSFER FUNCTION
4. Two-probe interference: hit primes with two wavelengths at once
5. The MISSING frequency: where is the laser WEAKEST? (gaps in the spectrum)
6. Energy-momentum: if q = "momentum" and I(q) = "energy", what's the dispersion?
7. Resonance width: at each glowing q, how SHARP is the peak?
"""
import math
from collections import Counter

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(2,n+1) if s[i]]

def mobius(n):
    if n==1: return 1
    d=2;t=n;nf=0
    while d*d<=t:
        if t%d==0:
            nf+=1;t//=d
            if t%d==0: return 0
        d+=1
    if t>1: nf+=1
    return (-1)**nf

def euler_phi(n):
    r=n;d=2;t=n
    while d*d<=t:
        if t%d==0:
            while t%d==0: t//=d
            r-=r//d
        d+=1
    if t>1: r-=r//t
    return r

def laser(values, lam):
    ar=ai=0
    for v in values:
        ph=2*math.pi*v/lam; ar+=math.cos(ph); ai+=math.sin(ph)
    n=len(values)
    return (ar*ar+ai*ai)/(n*n) if n>0 else 0

N=10000; P=sieve(N); Pset=set(P)

# ==========================================
# STRIKE 1: The complete coherence spectrum up to q=200
# What does the full "emission spectrum" of primes look like?
# ==========================================
print("=== STRIKE 1: Full emission spectrum of primes ===")
print("Intensity I(q) for q = 1 to 200")
print()

bright = []  # squarefree
dark = []    # non-squarefree
for q in range(2, 201):
    mu = mobius(q)
    phi = euler_phi(q)
    i_actual = laser(P, q)
    i_predicted = (mu**2) / (phi**2) if phi > 0 else 0
    
    if mu != 0:
        bright.append((q, i_actual, i_predicted))
    else:
        dark.append((q, i_actual))

# Total brightness
total_bright = sum(i for _, i, _ in bright)
total_dark = sum(i for _, i in dark)
total_all = total_bright + total_dark

print(f"Squarefree (bright): {len(bright)} wavelengths, total I = {total_bright:.4f}")
print(f"Non-squarefree (dark): {len(dark)} wavelengths, total I = {total_dark:.6f}")
print(f"Bright/Dark ratio: {total_bright/total_dark:.0f}x")
print(f"Bright carries {total_bright/total_all*100:.1f}% of total coherence")
print()

# Cumulative: how fast does the spectrum sum up?
print("Cumulative coherence vs q_max:")
cumul = 0
for q in range(2, 201):
    mu = mobius(q)
    if mu != 0:
        phi = euler_phi(q)
        cumul += 1.0/phi**2

    if q in [5, 10, 20, 30, 50, 100, 200]:
        # Theoretical: Product_{p<=q_max} (1 + 1/(p-1)^2)
        print(f"  q<={q:3d}: cumulative = {cumul:.6f}")

# Theoretical infinite sum
prod = 1.0
for p in P[:100]:
    prod *= (1 + 1.0/(p-1)**2)
print(f"  q->inf: product = {prod:.6f}")
print()

# ==========================================
# STRIKE 3: The transfer function H(omega)
# Treat q as "frequency" and I(q) as "response"
# What's the frequency response of the prime filter?
# ==========================================
print("=== STRIKE 3: Transfer function — primes as a filter ===")
print("If you send a broadband signal through 'the primes',")
print("what frequencies pass and what get blocked?")
print()

# The transfer function is: H(q) = I_P(q) for integer q
# But we can also do NON-integer q (fractional wavelengths)
print(f"{'q':>8} {'I(q)':>10} {'mu':>4} {'pass/block':>12}")
for q_num in [20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100]:
    q = q_num / 10.0  # fractional q
    i = laser(P, q)
    # For integer q, check mu
    if q == int(q):
        mu = mobius(int(q))
        pb = "PASS" if mu != 0 else "BLOCK"
    else:
        pb = "frac"
    print(f"{q:8.1f} {i:10.6f} {pb:>12}")

print()

# ==========================================
# STRIKE 4: Two-probe interference
# Hit primes with wavelengths q1 AND q2 simultaneously
# Measure: I(q1, q2) = |A(q1) + A(q2)|^2 / (2N)^2
# Cross term: Re(A(q1) * conj(A(q2))) = ???
# ==========================================
print("=== STRIKE 4: Two-probe interference ===")
print("Cross-coherence: Re(A(q1) * conj(A(q2))) / N^2")
print()

def amplitude(values, lam):
    ar=ai=0
    for v in values:
        ph=2*math.pi*v/lam; ar+=math.cos(ph); ai+=math.sin(ph)
    return complex(ar, ai) / len(values)

print(f"{'q1':>3} {'q2':>3} {'I(q1)':>10} {'I(q2)':>10} {'cross':>10} {'|cross|':>10} {'note':>10}")
print("-"*65)
pairs_tested = []
for q1 in [2, 3, 5, 6, 7, 10, 11, 13, 14, 15]:
    for q2 in [2, 3, 5, 6, 7, 10, 11, 13, 14, 15]:
        if q2 <= q1: continue
        a1 = amplitude(P, q1)
        a2 = amplitude(P, q2)
        cross = (a1 * a2.conjugate()).real
        i1 = abs(a1)**2
        i2 = abs(a2)**2
        note = ""
        if abs(cross) > 0.01:
            note = "STRONG"
        elif abs(cross) > 0.001:
            note = "weak"
        
        if abs(cross) > 0.001 or (q1 <= 6 and q2 <= 7):
            pairs_tested.append((abs(cross), q1, q2, cross))
            print(f"{q1:3d} {q2:3d} {i1:10.6f} {i2:10.6f} {cross:+10.6f} {abs(cross):10.6f} {note:>10}")

print()

# ==========================================
# STRIKE 5: The missing frequencies
# Where is the laser response MINIMUM for squarefree q?
# ==========================================
print("=== STRIKE 5: Weakest squarefree responses ===")
print("Which squarefree q has the smallest I(q)?")
print()

sf_intensities = []
for q in range(2, 501):
    if mobius(q) == 0: continue
    phi = euler_phi(q)
    predicted = 1.0/phi**2
    sf_intensities.append((predicted, q, phi))

sf_intensities.sort()
print("Dimmest 15 squarefree wavelengths:")
for pred, q, phi in sf_intensities[:15]:
    print(f"  q={q:4d}: phi={phi:3d}, I = 1/phi^2 = {pred:.8f}")

print()
print("Brightest 10:")
sf_intensities.sort(reverse=True)
for pred, q, phi in sf_intensities[:10]:
    print(f"  q={q:4d}: phi={phi:3d}, I = 1/phi^2 = {pred:.6f}")

print()

# ==========================================
# STRIKE 6: Dispersion relation E(k)
# If q = "momentum" and I(q) = "energy"
# What's the dispersion relation?
# In physics: E = hbar^2 k^2 / 2m (free particle), E = hbar*c*k (photon)
# For primes: I(q) = 1/phi(q)^2 for squarefree q
# phi(q) ~ q * product(1-1/p) ~ q * C
# So I(q) ~ 1/(q * C)^2 ~ 1/q^2 for large q
# This is like E ~ 1/k^2 — an INVERTED parabola!
# ==========================================
print("=== STRIKE 6: Dispersion relation I(q) vs q ===")
print("For squarefree q: I(q) = 1/phi(q)^2")
print("At large q: phi(q) ~ q * prod(1-1/p) → I ~ 1/q^2")
print()

print(f"{'q':>4} {'phi':>4} {'I_pred':>10} {'1/q^2':>10} {'ratio':>8}")
for q in [2,3,5,6,7,10,11,13,14,15,21,30,42,66,70,105,210]:
    if mobius(q) == 0: continue
    phi = euler_phi(q)
    i_pred = 1.0/phi**2
    inv_q2 = 1.0/q**2
    ratio = i_pred / inv_q2
    print(f"{q:4d} {phi:4d} {i_pred:10.6f} {inv_q2:10.6f} {ratio:8.3f}")

print()
print("The ratio I(q) / (1/q^2) = q^2/phi(q)^2 = (q/phi(q))^2")
print("This is the square of the 'density ratio' n/phi(n)")
print("Which peaks at highly composite numbers (many small prime factors)")
print()

# ==========================================
# STRIKE 7: Resonance width
# At squarefree q, the laser peaks. How SHARP is the peak?
# Measure I(q + epsilon) for small epsilon around integer q
# ==========================================
print("=== STRIKE 7: Resonance width (line broadening) ===")
print("How sharp is the coherence peak at each bright q?")
print()

for q in [2, 3, 5, 6, 7, 10, 30]:
    if mobius(q) == 0: continue
    peak = laser(P, q)
    # Measure half-max points
    # Scan epsilon
    half = peak / 2
    eps_half = None
    for ei in range(1, 1000):
        eps = ei * 0.001
        i_plus = laser(P, q + eps)
        if i_plus < half:
            eps_half = eps
            break
    
    width = 2 * eps_half if eps_half else float('inf')
    Q_factor = q / width if width < float('inf') else float('inf')
    print(f"  q={q:3d}: I_peak={peak:.6f}, half-width={eps_half:.3f}, full-width={width:.3f}, Q={Q_factor:.1f}")

print()
print("Q factor = q / width = 'quality' of resonance")
print("Higher Q = sharper peak = more like a laser")
print("Lower Q = broader = more like a lamp")
