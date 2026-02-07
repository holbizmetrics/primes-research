#!/usr/bin/env python3
"""DEEP INSIDE-OUT: Why are primes symmetric under modular inversion?

STRIKE 7 showed I_orig ≈ I_inv for p → p⁻¹ mod q.
This means the "laser" can't tell primes from their modular inverses.

WHY? Is this trivial or deep?

Also: what about OTHER inversions that preserve arithmetic structure?
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

# ==========================================
# DEEP STRIKE A: WHY is I_orig ≈ I_inv?
# 
# The laser on residues: I(q) = |Σ_p exp(2πi·(p mod q)/q)|² / n²
# Under p → p⁻¹ mod q: I_inv(q) = |Σ_p exp(2πi·p⁻¹ mod q / q)|² / n²
#
# Key identity: Σ_{a ∈ S} exp(2πia/q) = Σ_{a ∈ S} exp(2πi·a⁻¹/q)
# This is TRUE when S is a subgroup of (Z/qZ)*, but primes are NOT a subgroup.
#
# Actually, for the FULL Ramanujan sum c_q(n), we have:
# c_q(n) = Σ_{(a,q)=1} exp(2πian/q) = μ(q/gcd(n,q))·φ(q)/φ(q/gcd(n,q))
#
# The laser at λ=q on the primes is:
# A = Σ_p exp(2πip/q)
# Under inversion: A_inv = Σ_p exp(2πi·p⁻¹/q)
#
# These are NOT the same in general. But |A| ≈ |A_inv| when?
# 
# The distribution of primes mod q is nearly uniform (by Dirichlet).
# The fluctuation is small: O(√N/log N).
# Under inversion, the fluctuation maps to a different one, but
# |A|² measures the TOTAL fluctuation, not its direction.
# 
# Conjecture: |A|² ≈ |A_inv|² because the fluctuation magnitudes
# are comparable (both are deviations from uniformity).
# ==========================================
print("=== DEEP A: Phase analysis of A_P(q) vs A_P_inv(q) ===")
print("A_P(q) = Σ_p exp(2πip/q), A_inv(q) = Σ_p exp(2πi·p⁻¹/q)")
print()

print(f"{'q':>3} {'|A_P|²/n²':>10} {'|A_inv|²/n²':>12} {'phase_P':>8} {'phase_inv':>10} {'Δphase':>8}")
print("-"*60)
for q in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
    # Original
    ar_o=ai_o=0
    ar_i=ai_i=0
    n_count = 0
    for p in P:
        if p % q == 0: continue
        n_count += 1
        ph_o = 2*math.pi*(p%q)/q
        ar_o += math.cos(ph_o); ai_o += math.sin(ph_o)
        inv_p = pow(p, -1, q)
        ph_i = 2*math.pi*inv_p/q
        ar_i += math.cos(ph_i); ai_i += math.sin(ph_i)
    
    i_o = (ar_o**2+ai_o**2)/n_count**2
    i_i = (ar_i**2+ai_i**2)/n_count**2
    phase_o = math.atan2(ai_o, ar_o)
    phase_i = math.atan2(ai_i, ar_i)
    dphi = (phase_i - phase_o) % (2*math.pi)
    if dphi > math.pi: dphi -= 2*math.pi
    
    print(f"{q:3d} {i_o:10.6f} {i_i:12.6f} {phase_o:8.3f} {phase_i:10.3f} {dphi:8.3f}")

print()
print("If Δphase ≈ 0: inversion preserves direction (trivial)")
print("If Δphase ≈ π: inversion reverses direction (anti-symmetric)")
print("If random Δphase but same |A|: deeper symmetry")

# ==========================================
# DEEP STRIKE B: Multiplicative inversion on the FULL integer set
# For each n coprime to q, n → n⁻¹ mod q is a permutation of (Z/qZ)*
# The CHARACTER sum: Σ_n χ(n) = Σ_n χ(n⁻¹) = Σ_n χ̄(n)
# So inversion = complex conjugation in character space
# For primes: Σ_p χ(p) = some value L
# Under inversion: Σ_p χ(p⁻¹) = Σ_p χ̄(p) = L̄
# So |Σ_p χ(p)|² = |L̄|² = |L|²
# The intensities MUST be equal! It's a character theory identity!
# ==========================================
print("\n=== DEEP B: Character theory explains symmetry! ===")
print("p → p⁻¹ mod q acts as complex conjugation on characters")
print("Σ_p χ(p⁻¹) = Σ_p χ̄(p) = conjugate(Σ_p χ(p))")
print("|Σ_p χ(p⁻¹)|² = |conjugate(Σ_p χ(p))|² = |Σ_p χ(p)|²")
print()
print("→ The laser intensity |A|² is ALWAYS preserved under mod inversion!")
print("→ This is NOT about primes — it holds for ANY subset of integers!")
print()

# Verify: random subsets also have I_orig = I_inv
import random
random.seed(42)
print("Verification: random subsets of [1..5000] coprime to q=13:")
for trial in range(5):
    S = random.sample([n for n in range(1, N+1) if n % 13 != 0], 200)
    ar_o=ai_o=ar_i=ai_i=0
    for n in S:
        ph_o = 2*math.pi*(n%13)/13
        ar_o += math.cos(ph_o); ai_o += math.sin(ph_o)
        inv_n = pow(n, -1, 13)
        ph_i = 2*math.pi*inv_n/13
        ar_i += math.cos(ph_i); ai_i += math.sin(ph_i)
    i_o = (ar_o**2+ai_o**2)/len(S)**2
    i_i = (ar_i**2+ai_i**2)/len(S)**2
    print(f"  Trial {trial+1}: I_orig={i_o:.6f}  I_inv={i_i:.6f}  same={'YES' if abs(i_o-i_i)<0.001 else 'NO'}")

# ==========================================
# DEEP STRIKE C: What inversions DO break symmetry?
# Mod inversion doesn't. What about:
# - p → -p mod q (negation)
# - p → p² mod q (squaring)
# - p → 2p mod q (doubling)
# ==========================================
print("\n=== DEEP C: Which maps break symmetry? ===")
print("Testing: p → f(p) mod q, compare |A|²")
print()

for q in [7, 11, 13, 23, 29]:
    primes_mod = [p for p in P if p % q != 0]
    # Original
    ar=ai=0
    for p in primes_mod:
        ph=2*math.pi*(p%q)/q; ar+=math.cos(ph); ai+=math.sin(ph)
    i_orig = (ar**2+ai**2)/len(primes_mod)**2
    
    results = [f"orig={i_orig:.4f}"]
    
    for label, func in [("neg", lambda p,q: (-p)%q),
                         ("inv", lambda p,q: pow(p,-1,q)),
                         ("sq", lambda p,q: (p*p)%q),
                         ("dbl", lambda p,q: (2*p)%q)]:
        ar=ai=0
        for p in primes_mod:
            val = func(p, q)
            ph=2*math.pi*val/q; ar+=math.cos(ph); ai+=math.sin(ph)
        i_f = (ar**2+ai**2)/len(primes_mod)**2
        results.append(f"{label}={i_f:.4f}")
    
    print(f"  q={q:2d}: {', '.join(results)}")

print()
print("neg: p → -p — also preserves |A|² (conjugation of exp(2πip/q))")
print("inv: p → p⁻¹ — preserves |A|² (character conjugation)")
print("sq:  p → p² — may CHANGE |A|² (not an involution)")
print("dbl: p → 2p — may change (not a conjugation)")

# ==========================================
# DEEP STRIKE D: The MULTIPLICATIVE Fourier transform
# Instead of exp(2πip/q) (additive character),
# use Dirichlet characters χ(p) (multiplicative characters)
# These are the natural "inside-out" for multiplicative structure
# ==========================================
print("\n=== DEEP D: Multiplicative vs Additive inside-out ===")
print("Additive: exp(2πip/q) — periodic in p")
print("Multiplicative: χ(p) — periodic in p but respects multiplication")
print()

# For q prime, the characters mod q are: χ_k(p) = exp(2πi·k·ind_g(p)/φ(q))
# where g is a primitive root and ind_g(p) is the discrete log
# The "laser" using multiplicative characters:
# I_mult(k, q) = |Σ_p χ_k(p)|² / n²

def primitive_root(q):
    """Find primitive root mod q (q prime)"""
    for g in range(2, q):
        s = set()
        val = 1
        for i in range(q-1):
            val = (val * g) % q
            s.add(val)
        if len(s) == q-1:
            return g
    return None

def discrete_log(n, g, q):
    """Compute ind_g(n) mod q"""
    val = 1
    for i in range(q-1):
        if val == n % q:
            return i
        val = (val * g) % q
    return None

print(f"{'q':>3} {'k':>3} {'I_add(q)':>10} {'I_mult(k,q)':>12}")
print("-"*35)
for q in [7, 11, 13]:
    g = primitive_root(q)
    if g is None: continue
    
    # Additive laser at λ=q
    i_add = laser([p%q for p in P if p%q != 0], q)
    
    # Multiplicative characters
    for k in range(1, min(6, q)):
        ar=ai=0
        n_ct = 0
        for p in P:
            if p % q == 0: continue
            n_ct += 1
            idx = discrete_log(p, g, q)
            if idx is None: continue
            ph = 2*math.pi*k*idx/(q-1)
            ar += math.cos(ph); ai += math.sin(ph)
        i_mult = (ar**2+ai**2)/n_ct**2
        mark = " ← Legendre" if k == (q-1)//2 else ""
        print(f"{q:3d} {k:3d} {i_add:10.6f} {i_mult:12.6f}{mark}")
    print()

print("The Legendre symbol χ(p) = (p/q) is the 'halfway' character")
print("It measures quadratic residuosity — a DEEP inside-out")
