#!/usr/bin/env python3
"""SPARK STRIKE 4 + DEEP INVERSION
Strike 4: Symmetry group order = Ramanujan modulus
Deep inversion: What if the GEOMETRY is the output, not the input?
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

def euler_phi(n):
    result=n; d=2; temp=n
    while d*d<=temp:
        if temp%d==0:
            while temp%d==0: temp//=d
            result-=result//d
        d+=1
    if temp>1: result-=result//temp
    return result

N=5000; P=sieve(N); Pset=set(P); C=[i for i in range(4,N+1) if i not in Pset]

# ==========================================
# STRIKE 4: |Sym| as modulus
# Tet: 12, Oct/Cube: 24, Icosa/Dodec: 60
# 12 = 4×3, not squarefree → dark
# 24 = 8×3, not squarefree → dark
# 60 = 4×3×5, not squarefree → dark
# ALL Platonic symmetry group orders are non-squarefree!
# ==========================================
print("=== STRIKE 4: All Platonic |Sym| are non-squarefree ===")
for n, name in [(12,'Tet'), (24,'Oct/Cube'), (60,'Icosa/Dodec')]:
    mu = mobius(n)
    print(f"  |Sym({name})| = {n}: μ({n}) = {mu} → {'DARK' if mu==0 else 'GLOW'}")
print("ALL dark. Platonic symmetry orders cannot distinguish primes.")
print("This is because all have factor 4 (4|12, 4|24, 4|60).")
print()

# ==========================================
# DEEP INVERSION: "What geometry does the prime laser CREATE?"
#
# Instead of: impose geometry → measure primes
# Do: let primes → create geometry
#
# Method: the prime coherence I_P(q) for q=1,2,3,...
# defines a function on the integers.
# What SHAPE does this function have?
# ==========================================
print("=== DEEP INVERSION: What shape does prime coherence trace? ===")
print("I_P(q) = |Σ_p exp(2πip/q)|²/N²")
print()

# Compute coherence spectrum
qvals = list(range(2, 61))
Ip = [laser(P, q) for q in qvals]

# Where does it peak?
peaks = sorted(zip(Ip, qvals), reverse=True)[:10]
print("Top 10 coherence peaks:")
for val, q in peaks:
    mu = mobius(q)
    phi = euler_phi(q)
    pred = mu*mu/(phi*phi) if phi>0 else 0
    print(f"  q={q:3d}: I_P={val:.5f}  μ={mu:+d}  φ={phi:3d}  μ²/φ²={pred:.5f}  {'✓' if abs(val-pred)<0.01 else '✗'}")

# The shape: I_P(q) = μ(q)²/φ(q)² for squarefree q, ≈0 otherwise
# This IS a well-known arithmetic function!
# f(q) = μ(q)²/φ(q)² is multiplicative:
# f(p) = 1/(p-1)² for prime p
# f(p²) = 0
# The Dirichlet series: Σ f(q)/q^s = Π_p (1 + 1/((p-1)²*p^s))

print("\n=== What IS this function? ===")
print("I_P(q) = μ(q)²/φ(q)² = Π_{p|q} 1/(p-1)²  (for squarefree q)")
print()
print("This is the SINGULAR SERIES from Hardy-Littlewood!")
print("The singular series S(q) for prime counting is related to:")
print("  Π_{p|q} p/(p-1) × Π_{p∤q} (1-1/(p-1)²)")
print()
print("The shape the primes trace out in 'q-space' IS the singular series.")
print("This connects to twin prime constant, prime k-tuples, etc.")

# ==========================================
# DEEPER INVERSION: What if we look at the PHASE, not just amplitude?
# A_P(q) = |A|*exp(iθ). What does θ(q) look like?
# ==========================================
print("\n=== PHASE of prime coherence ===")
print("A_P(q) = R*exp(iθ). What pattern does θ(q) follow?")
print()
print(f"{'q':>3} {'|A|/N':>8} {'θ/π':>8} {'μ(q)':>5} {'note':>20}")
print("-"*50)
for q in range(2, 31):
    ar=ai=0
    for p in P:
        ph=2*math.pi*p/q; ar+=math.cos(ph); ai+=math.sin(ph)
    amp = math.sqrt(ar*ar+ai*ai)/len(P)
    theta = math.atan2(ai, ar)/math.pi
    mu = mobius(q)
    note = ""
    if mu == -1: note = "μ=-1"
    elif mu == 1: note = "μ=+1"
    elif mu == 0: note = "(dark)"
    # For squarefree q: does the phase tell us something?
    if mu != 0:
        # sign of real part
        sign_re = "+" if ar > 0 else "-"
        note += f" Re{sign_re}"
    print(f"{q:3d} {amp:8.5f} {theta:+8.4f} {mu:+5d} {note:>20}")

print("\n=== PHASE PATTERN ===")
print("For squarefree q with μ(q)=+1 (even # prime factors): θ ≈ 0 (real, positive)")
print("For squarefree q with μ(q)=-1 (odd # prime factors): θ ≈ π (real, negative)")
print("The SIGN of the coherence amplitude = μ(q)!")
print("This is just c_q(1) = μ(q), confirming the Ramanujan identity.")
print()

# ==========================================
# THE REAL INVERSION: "What do COMPOSITES know that primes don't?"
# ==========================================
print("=== THE REAL INVERSION ===")
print("Not 'what shape do primes make' but 'what does REMOVING primes reveal?'")
print()
# For all integers: Σ_{n=1}^{N} exp(2πin/q) = geometric sum = nearly 0 for q>1
# So: Σ_composite exp(2πic/q) = -Σ_prime exp(2πip/q) + O(1)
# The composite signal is the NEGATIVE of the prime signal!
# But normalized differently: N_C >> N_P, so I_C = I_P × (N_P/N_C)²

for q in [3, 5, 6, 7, 10]:
    ip = laser(P, q)
    ic = laser(C, q)
    ratio = ip/ic if ic > 1e-10 else float('inf')
    np_nc = len(P)/len(C)
    predicted_ratio = 1/np_nc**2
    print(f"q={q}: I_P/I_C = {ratio:.1f}, predicted (N_C/N_P)² = {1/np_nc**2:.1f}")

print()
print("=== FINAL INVERSION: What n-hedron has SQUAREFREE vertex count? ===")
print("The laser only cares about squarefree λ.")
print("Squarefree numbers: 1,2,3,5,6,7,10,11,13,14,15,17,19,21,22,23,26,29,30...")
print()
print("Regular n-gons with squarefree n are the 'prime-resonant' polygons.")
print("These are NOT Platonic solids! They're:")
print("  triangle(3), pentagon(5), hexagon(6), heptagon(7), decagon(10),")
print("  hendecagon(11), tridecagon(13), ...")
print()
print("The Platonic solids (V=4,6,8,12,20) have only ONE squarefree: 6 (octahedron).")
print("The icosahedron (12=4×3) is structurally invisible to the laser.")
print()
print("★ INVERTED PRINCIPLE: Don't ask 'which solid fits primes?'")
print("  Ask 'which n has μ(n)≠0?' — that's a NUMBER THEORY question, not geometry.")
print("  The polyhedra are a RED HERRING. The arithmetic function μ(q) is everything.")
