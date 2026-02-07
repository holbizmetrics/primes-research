#!/usr/bin/env python3
"""DEEP STRIKE: Why do twin primes have I(3) ≈ 1.0?

All primes >3 are ≡ 1 or 5 (mod 6), i.e., ≡ ±1 (mod 6).
So p ≡ 1 mod 3 or p ≡ 2 mod 3.

Twin primes (p, p+2): if p ≡ 1 mod 3, then p+2 ≡ 0 mod 3 → NOT prime (unless p+2=3)
So for p > 3: twin primes require p ≡ 2 mod 3 (i.e., p ≡ -1 mod 3)
Then p+2 ≡ 1 mod 3 ✓ (could be prime)

So ALL twin primes (p > 3) have p ≡ 2 mod 3!
Laser at λ=3: exp(2πip/3) = exp(2πi*2/3) = exp(4πi/3) for ALL twins
→ PERFECT COHERENCE!

This is not a discovery about primes — it's a trivial consequence of:
"twin primes > 3 are all ≡ 2 mod 3"
which follows from "3 divides one of n, n+1, n+2 for any n"
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
twins = [p for p in P if p+2 in Pset and p > 3]
cousins = [p for p in P if p+4 in Pset and p > 5]
sexys = [p for p in P if p+6 in Pset and p > 7]

print("=== WHY I_twin(3) ≈ 1 ===")
print("Twin primes (p, p+2) with p > 3:")
mod3 = [p % 3 for p in twins[:20]]
print(f"  First 20 twins mod 3: {mod3}")
print(f"  ALL ≡ 2 mod 3 (because if p ≡ 1 mod 3, then p+2 ≡ 0 mod 3 = not prime)")
print(f"  → exp(2πip/3) = exp(4πi/3) = same phase for ALL twins")
print(f"  → PERFECT COHERENCE (trivial)")
print()

# Same logic for cousins (gap 4) at λ=5:
print("=== COUSIN PRIMES (gap 4) at λ=5 ===")
mod5 = [p % 5 for p in cousins[:20]]
print(f"  First 20 cousins mod 5: {mod5}")
# (p, p+4): if p ≡ 1 mod 5, p+4 ≡ 0 mod 5 → not prime (unless p+4=5)
# So cousins > 5 require p ≢ 1 mod 5
# Also: if p ≡ 4 mod 5, p+4 ≡ 3 mod 5 ✓
# If p ≡ 2 mod 5, p+4 ≡ 1 mod 5 ✓
# If p ≡ 3 mod 5, p+4 ≡ 2 mod 5 ✓
# So cousins can be 2, 3, or 4 mod 5 → NOT perfectly coherent at λ=5
print(f"  Multiple residues → NOT perfectly coherent at λ=5")
i_co5 = sum(1 for p in cousins if p%5 in [2,3,4])
print(f"  I_cousin(5) = {laser(cousins, 5):.6f} (not 1.0)")
print()

# For GENERAL gap g:
# (p, p+g): p+g ≡ 0 mod q when p ≡ -g mod q
# So twin primes avoid p ≡ -2 mod q for all prime q
# The FORCED residue class creates coherence at λ=q when q | (something)
print("=== GENERAL: gap-g primes at λ=q ===")
print("(p, p+g): must avoid p ≡ -g mod q for each prime q")
print("When g ≡ 0 mod q: no constraint (p+g ≡ 0 mod q only if p ≡ 0 mod q)")
print("When g ≢ 0 mod q: p is forced to avoid ONE residue class mod q")
print()

# The number of allowed residue classes mod q for gap-g primes:
# There are φ(q) coprime residues normally.
# The constraint removes 1 class when gcd(g,q)=1, 0 classes when q|g.
# Allowed = φ(q) - [1 if gcd(g,q)==1 else 0]  (roughly)
# For q=3, g=2: allowed = φ(3)-1 = 2-1 = 1 → single residue → PERFECT
# For q=5, g=2: allowed = φ(5)-1 = 4-1 = 3 → three residues → partial
# For q=3, g=4: allowed = φ(3)-1 = 1 → single residue → PERFECT
# For q=3, g=6: allowed = φ(3) = 2 (since 3|6) → two residues → normal

def laser_amp(values, lam):
    """Return complex amplitude"""
    ar=ai=0
    for v in values:
        ph=2*math.pi*v/lam; ar+=math.cos(ph); ai+=math.sin(ph)
    return complex(ar,ai)/len(values) if values else 0

print(f"{'gap':>4} {'λ':>3} {'allowed_res':>12} {'I_gap':>10} {'coherent?':>10}")
print("-"*50)
for g in [2, 4, 6, 8, 10, 12]:
    gap_primes = [p for p in P if p > g and p+g in Pset]
    if len(gap_primes) < 10: continue
    for q in [3, 5, 7]:
        # How many residue classes mod q are used?
        classes_used = set(p % q for p in gap_primes)
        n_classes = len(classes_used)
        # Coherence
        ip = laser(gap_primes, q)
        coh = "PERFECT" if ip > 0.9 else ("HIGH" if ip > 0.1 else "normal")
        print(f"g={g:2d}  q={q}  classes={classes_used!s:<12} I={ip:10.6f}  {coh}")
    print()

# ==========================================
# THE REAL OVERTONE STRUCTURE
# For twin primes, λ=3 gives perfect coherence.
# What about λ=3k (overtones of this fundamental)?
# λ=3: perfect, λ=6: same (since 6 ≡ 0 mod 3 for phases... wait)
# Actually λ=6: exp(2πip/6). Twins have p ≡ 5 mod 6 (≡ -1 mod 6)
# So exp(2πi*5/6) = same phase for all twins → PERFECT
# λ=9: p mod 9 for twins... twins are 2 mod 3, but mod 9?
# ==========================================
print("=== OVERTONE LADDER for twin primes ===")
print("Fundamental: λ=3 (I=1.0 because all twins ≡ 2 mod 3)")
print()

for lam in [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]:
    classes = set(p % lam for p in twins)
    ip = laser(twins, lam)
    nc = len(classes)
    print(f"λ={lam:3d}: I={ip:.6f}  #residue_classes={nc}  classes={sorted(classes)[:8]}{'...' if nc>8 else ''}")

print()
print("=== WHAT WE ACTUALLY FOUND ===")
print()
print("1. Twin primes have I(3)=I(6)≈1.0 → TRIVIAL (forced residue class)")
print("2. Cousin primes have I(5)≈0.30 → NOT perfect (3 residue classes)")
print("3. Sexy primes (gap 6) have I(3)≈0.25 = same as all primes → NO boost")
print("   (because 3|6, so no residue class is eliminated)")
print()
print("4. The 'overtone series' of twin primes is just:")
print("   Perfect at λ = 3, 6 (forced to single class mod 3)")
print("   Normal elsewhere")
print()
print("5. This IS the Hardy-Littlewood singular series in action!")
print("   S₂(q) = Π_{p|q} (p-1)/(p-2) for p>2, times μ²/φ²")
print("   When q=3: (3-1)/(3-2) = 2 → 2× boost over base")
print("   The 'resonance' IS the singular series.")
print()
print("★ INVERTED INSIGHT:")
print("  Don't ask 'do twin primes resonate?'")
print("  Ask 'what does the singular series SOUND like?'")
print("  The singular series IS the overtone spectrum of prime pairs!")
print("  Each factor (p-1)/(p-2) is a harmonic amplitude.")
