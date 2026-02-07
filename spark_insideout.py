#!/usr/bin/env python3
"""SPARK: Turn geometries inside out
STRIKE 1: Full sphere inversion (r → 1/r)
STRIKE 3: Modular inversion τ → -1/τ
STRIKE 4: Stereographic/reciprocal primes
STRIKE 5: Fourier transform of 1/p
STRIKE 7: Modular inverse primes
"""
import math, sys

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
# STRIKE 1: Full sphere inversion
# Map n → N/n (sends small↔large)
# Primes p → N/p (NOT integers anymore)
# Composites c → N/c
# Then run laser on the inverted positions
# ==========================================
print("=== STRIKE 1: Full inversion n → N/n ===")
print("Primes p → N/p, composites c → N/c")
print()

P_inv = [N/p for p in P]  # inverted primes
C_inv = [N/c for c in C]  # inverted composites

# Laser on inverted positions
print(f"{'λ':>5} {'I_P':>10} {'I_P_inv':>10} {'I_C':>10} {'I_C_inv':>10} {'P/C_inv':>8}")
for lam in [2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 21, 30]:
    ip = laser(P, lam)
    ip_inv = laser(P_inv, lam)
    ic = laser(C, lam)
    ic_inv = laser(C_inv, lam)
    pc_inv = ip_inv/ic_inv if ic_inv > 1e-10 else float('inf')
    print(f"{lam:5d} {ip:10.6f} {ip_inv:10.6f} {ic:10.6f} {ic_inv:10.6f} {pc_inv:8.1f}")

print()
print("Inverted primes: large primes (near N) → near 1, small primes → large values")
print("The inversion SCRAMBLES the coherence — no clean Ramanujan structure")
sys.stdout.flush()

# ==========================================
# STRIKE 4: Reciprocal primes {1/p}
# Study Σ exp(2πi/(pλ)) — the laser on 1/p
# ==========================================
print("\n=== STRIKE 4: Reciprocal primes 1/p ===")
print("Laser on {1/2, 1/3, 1/5, 1/7, ...}")
print()

Prec = [1.0/p for p in P]
Crec = [1.0/c for c in C]

print(f"{'λ':>8} {'I_1/P':>10} {'I_1/C':>10} {'ratio':>8}")
for lam in [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]:
    ip = laser(Prec, lam)
    ic = laser(Crec, lam)
    ratio = ip/ic if ic > 1e-10 else float('inf')
    print(f"{lam:8.3f} {ip:10.6f} {ic:10.6f} {ratio:8.2f}")

sys.stdout.flush()

# ==========================================
# STRIKE 5: Fourier transform of the reciprocal prime measure
# F(ξ) = Σ_p exp(2πi·ξ/p)
# This probes the HARMONIC structure of 1/p
# Note: ξ/p = ξ × (1/p), so this is the laser at wavelength 1/ξ
# on the reciprocal primes. Let's scan ξ.
# ==========================================
print("\n=== STRIKE 5: Fourier of 1/p at frequency ξ ===")
print("F(ξ) = |Σ_p exp(2πiξ/p)|²/N²")
print()

print(f"{'ξ':>8} {'|F(ξ)|²/N²':>12} {'note':>20}")
peaks = []
for xi_int in range(1, 61):
    xi = float(xi_int)
    ar=ai=0
    for p in P:
        ph = 2*math.pi*xi/p
        ar += math.cos(ph); ai += math.sin(ph)
    intensity = (ar*ar+ai*ai)/len(P)**2
    note = ""
    if xi_int in Pset: note = "prime"
    elif xi_int in [1,4,6,8,9,10,12]: note = ""
    peaks.append((intensity, xi_int))
    if intensity > 0.01 or xi_int <= 10 or xi_int in Pset:
        print(f"{xi:8.0f} {intensity:12.6f} {note:>20}")

peaks.sort(reverse=True)
print(f"\nTop 5 peaks: {[(f'ξ={x}',f'{v:.4f}') for v,x in peaks[:5]]}")
sys.stdout.flush()

# ==========================================
# STRIKE 7: Modular inverse primes
# For prime q, each prime p (coprime to q) has an inverse p⁻¹ mod q
# Map p → p⁻¹ mod q, then run laser
# This is an ARITHMETIC inside-out: inverting the residues
# ==========================================
print("\n=== STRIKE 7: Modular inverse — p → p⁻¹ mod q ===")
print("Replace each prime p with its modular inverse p⁻¹ mod q")
print("Then compute laser on the inverted residues")
print()

for q in [7, 11, 13, 17, 19, 23, 29, 31]:
    # Original: laser on p mod q
    orig = [p % q for p in P if p % q != 0]
    # Inverted: laser on p^{-1} mod q
    inverted = [pow(p, -1, q) for p in P if p % q != 0]

    # These should actually give the SAME coherence!
    # Because p → p⁻¹ is a bijection on (Z/qZ)*
    # and Σ exp(2πi·p⁻¹/q) over primes...
    # Actually it's NOT the same because the map is on the RESIDUES not the primes

    # Let me compute both
    i_orig = laser(orig, q)
    i_inv = laser(inverted, q)

    # Also: what's the laser on the inverted VALUES (not mod q)?
    # p⁻¹ mod q gives values in {1,...,q-1}
    # Laser at wavelength q on these values
    ar_o=ai_o=ar_i=ai_i=0
    for p in P:
        if p % q == 0: continue
        ph_o = 2*math.pi*(p%q)/q
        ar_o += math.cos(ph_o); ai_o += math.sin(ph_o)
        inv_p = pow(p, -1, q)
        ph_i = 2*math.pi*inv_p/q
        ar_i += math.cos(ph_i); ai_i += math.sin(ph_i)

    n = sum(1 for p in P if p%q != 0)
    io = (ar_o**2+ai_o**2)/n**2
    ii = (ar_i**2+ai_i**2)/n**2

    print(f"q={q:2d}: I_orig={io:.6f}  I_inv={ii:.6f}  same={'YES' if abs(io-ii)<0.001 else 'NO'}")

print()
print("If I_orig = I_inv: the inversion is invisible (primes are symmetric under mod inverse)")
print("If different: primes have a CHIRALITY in modular arithmetic")
sys.stdout.flush()
