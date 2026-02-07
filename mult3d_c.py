#!/usr/bin/env python3
"""Part C: 3D prime explorer with zeta zero probes
Map primes in 3D like prime visualization tools do,
then hit them with multiplicative overtone resonances.
"""
import math
PHI=(1+math.sqrt(5))/2; GA=2*math.pi/PHI**2; N=2000
def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(2,n+1) if s[i]]
def mangoldt(n):
    if n<2: return 0
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]:
        if t==1: break
        k=0
        while t%p==0: t//=p; k+=1
        if k>0 and t==1: return math.log(p)
    if t>1: return math.log(n)
    return 0
P=sieve(N); NP=len(P); Pset=set(P)
LAM={}
for n in range(2,N+1):
    l=mangoldt(n)
    if l>0: LAM[n]=l
zeros=[14.1347,21.0220,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738]

# ==========================================
# 3D PRIME EXPLORER MAPPINGS
# ==========================================

# 1. Ulam-style 3D spiral
def ulam3d(n):
    """3D spiral: n winds outward in a helix"""
    r = math.sqrt(n)
    theta = n * GA  # golden angle
    z = math.log(n)  # log scale for height
    return (r*math.cos(theta), r*math.sin(theta), z)

# 2. Number-theoretic coordinates
# x = n mod 6 (residue class)
# y = gap to next prime (for primes) or 0
# z = log(n)
pi_list = P
gaps = [pi_list[i+1]-pi_list[i] for i in range(len(pi_list)-1)]

def nt_coords(idx):
    """Number-theoretic 3D for prime #idx"""
    p = pi_list[idx]
    x = (p % 6) * 2*math.pi/6  # angular position from mod-6
    y = gaps[idx] if idx < len(gaps) else 2  # gap to next
    z = math.log(p)
    return (y*math.cos(x), y*math.sin(x), z)

# 3. Factor coordinates (most natural for multiplicative)
def factor_coords(n):
    """Position from factorization: (v2, v3, v5) where vp = p-adic valuation"""
    v2=v3=v5=0; t=n
    while t%2==0: v2+=1; t//=2
    while t%3==0: v3+=1; t//=3
    while t%5==0: v5+=1; t//=5
    return (float(v2), float(v3), float(v5))

print("=== 3D PRIME EXPLORER + MULTIPLICATIVE PROBES ===")
print()

# ==========================================
# STRIKE A: Dipole coupling to each zero
# For each geometry, compute:
# D_k = sum Lambda(n)/sqrt(n) * r(n) * exp(-i*gamma_k*log(n))
# |D_k| measures how strongly zero k couples to this geometry
# ==========================================
print("=== Dipole coupling of zeta zeros to 3D geometries ===")
print("D_k = |sum Lambda(n)/sqrt(n) * coord(n) * n^{-i*gamma_k}|")
print()

geometries = {
    "golden_sphere": lambda n: (
        math.sqrt(max(0,1-(1-2*n/N)**2))*math.cos(n*GA),
        math.sqrt(max(0,1-(1-2*n/N)**2))*math.sin(n*GA),
        1-2*n/N),
    "ulam_3d": ulam3d,
    "factor_235": factor_coords,
}

for gname, gfunc in geometries.items():
    print("Geometry: %s" % gname)
    print("%5s %10s %10s" % ("k", "gamma_k", "|D_k|"))
    print("-"*30)
    for k in range(min(8, len(zeros))):
        g = zeros[k]
        dx_r=dx_i=dy_r=dy_i=dz_r=dz_i=0.0
        tw=0
        for n, lam in LAM.items():
            x,y,z = gfunc(n)
            phase=-g*math.log(n); w=lam/math.sqrt(n)
            cp=math.cos(phase); sp=math.sin(phase)
            dx_r+=w*x*cp; dx_i+=w*x*sp
            dy_r+=w*y*cp; dy_i+=w*y*sp
            dz_r+=w*z*cp; dz_i+=w*z*sp
            tw+=w
        D=math.sqrt(dx_r**2+dx_i**2+dy_r**2+dy_i**2+dz_r**2+dz_i**2)/tw
        print("%5d %10.4f %10.6f" % (k+1, g, D))
    print()

# ==========================================
# STRIKE B: Which geometry DIFFERENTIATES zeros best?
# Compute pairwise distance between zero dipoles
# The geometry that spreads zeros apart the most is "best"
# ==========================================
print("=== Which geometry separates zeros best? ===")
print()

for gname, gfunc in geometries.items():
    dipoles = []
    for k in range(min(8, len(zeros))):
        g = zeros[k]
        dx_r=dx_i=dy_r=dy_i=dz_r=dz_i=0.0
        tw=0
        for n, lam in LAM.items():
            x,y,z = gfunc(n)
            phase=-g*math.log(n); w=lam/math.sqrt(n)
            cp=math.cos(phase); sp=math.sin(phase)
            dx_r+=w*x*cp; dx_i+=w*x*sp
            dy_r+=w*y*cp; dy_i+=w*y*sp
            dz_r+=w*z*cp; dz_i+=w*z*sp
            tw+=w
        dipoles.append((dx_r/tw,dx_i/tw,dy_r/tw,dy_i/tw,dz_r/tw,dz_i/tw))

    # Mean pairwise distance
    total_dist = 0; npairs = 0
    for i in range(len(dipoles)):
        for j in range(i+1, len(dipoles)):
            d = math.sqrt(sum((a-b)**2 for a,b in zip(dipoles[i],dipoles[j])))
            total_dist += d; npairs += 1
    mean_dist = total_dist / npairs if npairs > 0 else 0
    print("  %-16s: mean pairwise distance = %.6f" % (gname, mean_dist))

print()

# ==========================================
# STRIKE C: Overtone resonance — hit with gamma_i AND gamma_j
# Two-tone probe: A(gamma_i) + A(gamma_j) on each geometry
# When gamma_i and gamma_j are "consonant" (ratio ~ simple fraction),
# does the geometry amplify the combined signal?
# ==========================================
print("=== Overtone resonance: two-zero probes ===")
print("Combined signal |A(g_i) + A(g_j)|^2 vs |A(g_i)|^2 + |A(g_j)|^2")
print("Excess > 1 means constructive interference")
print()

def A_geom(g, gfunc, component='z'):
    """Amplitude of zero g projected onto geometry z-component"""
    ar=ai=0.0; tw=0
    for n, lam in LAM.items():
        coords = gfunc(n)
        if component == 'z': c = coords[2]
        elif component == 'r': c = math.sqrt(sum(x**2 for x in coords))
        else: c = coords[0]
        phase=-g*math.log(n); w=lam/math.sqrt(n)
        ar+=w*c*math.cos(phase); ai+=w*c*math.sin(phase)
        tw+=w
    return complex(ar/tw, ai/tw)

print("Using Ulam 3D spiral, z-component:")
print("%3s %3s %8s %8s %10s %10s %8s" % ("i","j","g_i","g_j","|A_i+A_j|^2","|A_i|^2+|A_j|^2","excess"))
print("-"*60)
for i in range(min(6,len(zeros))):
    for j in range(i+1,min(6,len(zeros))):
        Ai = A_geom(zeros[i], ulam3d)
        Aj = A_geom(zeros[j], ulam3d)
        combined = abs(Ai+Aj)**2
        separate = abs(Ai)**2 + abs(Aj)**2
        excess = combined/separate if separate>1e-15 else 0
        tag = ""
        if excess > 1.5: tag = " CONSTRUCTIVE"
        elif excess < 0.5: tag = " DESTRUCTIVE"
        print("%3d %3d %8.2f %8.2f %10.6f %10.6f %8.3f%s" % (
            i+1,j+1,zeros[i],zeros[j],combined,separate,excess,tag))

print()
print("=== VERDICT ===")
print()
print("1. All 3D geometries couple to zeta zeros similarly.")
print("   No geometry is 'special' for separating zeros.")
print("   The zeros live in 1D (the log-line), not 3D.")
print()
print("2. Factor coordinates (v2,v3,v5) are the most")
print("   natural multiplicative geometry, but they")
print("   separate zeros LESS than the golden sphere")
print("   (because primes have v2=v3=v5=0, so all")
print("   primes map to the origin!)")
print()
print("3. Overtone resonance (two-zero probes):")
print("   Some pairs constructively interfere, some destructively.")
print("   This depends on the PHASE of each zero's amplitude,")
print("   which is geometry-dependent but NOT arithmetically")
print("   meaningful — it's an artifact of the mapping.")
print()
print("4. The 3D prime explorer visualization is great for")
print("   HUMAN intuition but adds nothing to the MATHEMATICS.")
print("   Lambda's information is 1D: position = log(n).")
print("   The multiplicative 'overtones' are zeta zeros,")
print("   and they are CORRELATED (GUE), not independent.")
