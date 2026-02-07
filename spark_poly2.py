#!/usr/bin/env python3
"""SPARK STRIKE 3,5,6,7: The inversions"""
import math

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(2,n+1) if s[i]]

N = 5000
P = sieve(N)
Pset = set(P)
C = [i for i in range(4, N+1) if i not in Pset]

# ==========================================
# STRIKE 3: Composites tile polyhedra, primes are gaps
# Idea: composites at regular n-gon positions, primes are where the n-gon DOESN'T land
# ==========================================
print("=== STRIKE 3: Composites as n-gon tiling ===")
print("For each n, count how many composites ≡ 0 (mod n), vs primes ≡ 0 (mod n)")
print("(Primes mod n are never 0 for p>n, composites are 1/n of the time)")
print()
# This is trivial: primes can't be ≡ 0 mod n (for n>1), composites can.
# But what about: composites on EDGES of n-gon (mod n), measuring structure
print("More interesting: for each n-gon (n=3..20), compute coherence of")
print("COMPOSITES at λ=n and compare to coherence of PRIMES at λ=n")
print()

def laser(values, lam):
    ar=ai=0
    for v in values:
        ph = 2*math.pi*v/lam
        ar += math.cos(ph); ai += math.sin(ph)
    n = len(values)
    return (ar*ar+ai*ai)/(n*n) if n>0 else 0

print(f"{'n':>3} {'I_C(n)':>10} {'I_P(n)':>10} {'C/P':>8} | composites glow MORE?")
print("-"*60)
for n in range(3, 21):
    ic = laser(C, n)
    ip = laser(P, n)
    cp = ic/ip if ip > 1e-10 else float('inf')
    arrow = "<<< C wins" if cp > 2 else (">>> P wins" if cp < 0.5 else "~equal")
    print(f"{n:3d} {ic:10.6f} {ip:10.6f} {cp:8.2f} | {arrow}")

# ==========================================
# STRIKE 5: Dual polyhedra = dual number classes
# Cube (V=8) ↔ Octahedron (V=6)
# λ=8 is non-squarefree, λ=6 is squarefree
# Dodec (V=20) ↔ Icosa (V=12)
# Both non-squarefree
# ==========================================
print("\n=== STRIKE 5: Dual polyhedra coherence ===")
print("Cube (λ=8) ↔ Octahedron (λ=6)")
print(f"  Primes at λ=8: {laser(P,8):.6f} (non-sqfree → dark)")
print(f"  Primes at λ=6: {laser(P,6):.6f} (sqfree → GLOW)")
print(f"  Composites at λ=8: {laser(C,8):.6f}")
print(f"  Composites at λ=6: {laser(C,6):.6f}")
print()
print("Dodecahedron (λ=20) ↔ Icosahedron (λ=12)")
print(f"  Primes at λ=20: {laser(P,20):.6f} (non-sqfree)")
print(f"  Primes at λ=12: {laser(P,12):.6f} (non-sqfree)")
print("Both dark. Duality doesn't create prime/composite separation here.")

# ==========================================
# STRIKE 6: Symmetry group representations as probes
# Instead of exp(2πip/q), use character values of S_n, A_n, etc.
# For cyclic group Z_n: characters ARE exp(2πikp/n) for k=0..n-1
# For dihedral D_n: additional 2D representations
# For A_5 (icosahedral): 5 irreps of dim 1,3,3,4,5
# ==========================================
print("\n=== STRIKE 6: Symmetry group representations ===")
print("Cyclic group Z_n: Σ exp(2πikp/n) for each k")
print("This is just the laser at λ=n/k! Already covered by Ramanujan.")
print()
print("For non-abelian groups (S_3, A_4, S_4, A_5):")
print("The irreps give CHARACTER values χ(p mod n)")
print("But: these characters decompose into sums of Dirichlet characters!")
print("So polyhedral symmetry → Ramanujan sums (again)")
print()
# Let's verify for A_5 (icosahedral group, order 60)
# Characters mod 60 contain all the information
# Irreps of A_5: trivial(1), two 3-dim, one 4-dim, one 5-dim
# Character table values at conjugacy classes: {e}, {(12)(34)}, {(123)}, {(12345)}, {(13245)}
# These map to specific combinations of χ mod 5, χ mod 4, χ mod 3

# Actually: since we're probing INTEGERS (not group elements),
# the representation theory of the group doesn't directly apply.
# We'd need a map from integers to group elements first.
# The natural map: n → n mod |G| → element of Z/|G|Z
# But Z/60Z ≠ A_5, so the icosahedral GROUP doesn't appear.
print("RESULT: Polyhedral symmetry groups don't naturally act on integers.")
print("The map n → n mod 60 gives Z/60Z ≠ A_5.")
print("Polyhedral groups are NON-ABELIAN but integer residues are ABELIAN.")
print("→ No meaningful icosahedral character sum on primes.")

# ==========================================
# STRIKE 7: FULL INVERSION — n-gon phases at each prime
# Place regular n-gon at prime p: vertices at p + k*(p/n) for k=0..n-1? No...
# Better: for each prime p, emit n-gon wave: Σ_{k=0}^{n-1} exp(2πi*k*x/n)
# at position x=p. Then sum over all primes.
# Total signal: Σ_p Σ_{k=0}^{n-1} exp(2πi*k*p/n) = n * #{p ≡ 0 mod n} + Σ_{k=1}^{n-1} Σ_p exp(2πikp/n)
# = (0 for p>n) + Σ_{k=1}^{n-1} c_n^(k)
# where c_n^(k) = Σ_p exp(2πikp/n) is just the laser at wavelength n/k!
# ==========================================
print("\n=== STRIKE 7: n-gon phases at each prime (INVERSION) ===")
print("Σ_p Σ_{k=0}^{n-1} exp(2πikp/n) = Σ_k laser(P, n/k)")
print("This decomposes into n laser measurements at wavelengths n/k")
print()

for n in [3, 4, 5, 6, 12, 20]:
    total_re = 0; total_im = 0
    components = []
    for k in range(n):
        if k == 0:
            components.append(('k=0', len(P)))  # all primes contribute 1
            total_re += len(P)
            continue
        # laser at effective wavelength n/k
        ar = ai = 0
        for p in P:
            ph = 2*math.pi*k*p/n
            ar += math.cos(ph); ai += math.sin(ph)
        intensity = (ar*ar+ai*ai)
        total_re += ar; total_im += ai
        components.append((f'k={k}', intensity/len(P)**2))

    total_intensity = (total_re**2 + total_im**2)/len(P)**2
    # The n-gon "emission" intensity
    print(f"n={n:2d}: total_I={total_intensity:.4f}")
    for label, val in components[1:]:
        if val > 0.01:
            print(f"       {label}: I={val:.5f}")

print("\n=== THE BIG INVERSION: What sees primes as gaps? ===")
print("If f(n) = 1 for composite, 0 for prime, then:")
print("Σ_c exp(2πic/q) = Σ_n exp(2πin/q) - Σ_p exp(2πip/q)")
print("= (sum over all n) - (laser on primes)")
print("= δ(q=1)*N - laser_P(q)")
print()
print("So composite coherence = |N*δ_{q,1} - A_P(q)|²/N_C²")
print("For q>1: composite signal = |A_P(q)|² * (N_P/N_C)² × (N_P²/N_C² correction)")
print("Composites carry the SAME information as primes — just rescaled!")
print("The duality is TRIVIAL: f_composite = 1 - f_prime (up to trivial term)")
