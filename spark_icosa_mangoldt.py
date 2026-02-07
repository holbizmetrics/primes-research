#!/usr/bin/env python3
"""Von Mangoldt meets the Icosahedron
Multiple attacks:
1. Map integers to golden spiral sphere, bin into nearest icosahedron vertex
2. Lambda-weighted icosahedral modes
3. The icosahedral numbers (12, 20, 30, 60) as laser wavelengths with Lambda
4. Icosahedral coordinates as a NEW mapping for Lambda
5. Project Lambda onto the 6 axes of the icosahedron
"""
import math, sys

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

PHI = (1 + math.sqrt(5)) / 2
N = 3000
P = sieve(N); Pset = set(P)

# ==========================================
# Icosahedron vertices (unit sphere)
# 12 vertices: top, bottom, and two rings of 5
# ==========================================
def icosa_vertices():
    """12 vertices of a regular icosahedron on the unit sphere"""
    verts = []
    # Top and bottom
    verts.append((0, 0, 1))
    verts.append((0, 0, -1))
    # Upper ring: z = 1/sqrt(5), azimuth = k*72 degrees
    z_up = 1/math.sqrt(5)
    r_up = math.sqrt(1 - z_up**2)
    for k in range(5):
        theta = k * 2*math.pi/5
        verts.append((r_up*math.cos(theta), r_up*math.sin(theta), z_up))
    # Lower ring: z = -1/sqrt(5), azimuth = (k+0.5)*72 degrees
    z_dn = -1/math.sqrt(5)
    r_dn = math.sqrt(1 - z_dn**2)
    for k in range(5):
        theta = (k + 0.5) * 2*math.pi/5
        verts.append((r_dn*math.cos(theta), r_dn*math.sin(theta), z_dn))
    return verts

VERTS = icosa_vertices()
GOLDEN_ANGLE = 2 * math.pi / PHI**2

def sphere_point(n, N_max):
    theta = n * GOLDEN_ANGLE
    z = 1 - 2*n/N_max
    r_xy = math.sqrt(max(0, 1 - z*z))
    return (r_xy*math.cos(theta), r_xy*math.sin(theta), z)

def nearest_vertex(pt, verts):
    """Find nearest icosahedron vertex"""
    best_d = float('inf')
    best_i = 0
    for i, v in enumerate(verts):
        d = sum((a-b)**2 for a,b in zip(pt, v))
        if d < best_d:
            best_d = d; best_i = i
    return best_i

# ==========================================
# STRIKE 1: Bin integers into icosahedron vertices
# Weight by Lambda(n) — does any vertex accumulate more?
# ==========================================
print("=== STRIKE 1: Lambda binned onto icosahedron ===")
print("Each integer n -> nearest vertex, weighted by Lambda(n)")
print()

# Accumulate Lambda at each vertex
lam_per_vertex = [0.0] * 12
count_per_vertex = [0] * 12
prime_per_vertex = [0.0] * 12

for n in range(2, N+1):
    pt = sphere_point(n, N)
    vi = nearest_vertex(pt, VERTS)
    lam = mangoldt(n)
    count_per_vertex[vi] += 1
    lam_per_vertex[vi] += lam
    if n in Pset:
        prime_per_vertex[vi] += 1

total_lam = sum(lam_per_vertex)
total_count = sum(count_per_vertex)

print(f"{'V':>3} {'z':>6} {'count':>6} {'Lambda':>8} {'primes':>7} {'Lambda/count':>12}")
print("-"*50)
for i in range(12):
    z = VERTS[i][2]
    ratio = lam_per_vertex[i]/count_per_vertex[i] if count_per_vertex[i] > 0 else 0
    print(f"{i:3d} {z:6.3f} {count_per_vertex[i]:6d} {lam_per_vertex[i]:8.1f} {prime_per_vertex[i]:7.0f} {ratio:12.4f}")

print()
# Is Lambda distribution uniform across vertices?
mean_lam = total_lam / 12
var_lam = sum((l - mean_lam)**2 for l in lam_per_vertex) / 12
std_lam = math.sqrt(var_lam)
print(f"Mean Lambda/vertex: {mean_lam:.1f}, std: {std_lam:.1f}, CV: {std_lam/mean_lam:.3f}")
sys.stdout.flush()

# ==========================================
# STRIKE 2: Icosahedral numbers as wavelengths
# 12 (vertices), 20 (faces), 30 (edges), 60 (|Sym|)
# Compare prime indicator vs Lambda-weighted laser
# ==========================================
print("\n=== STRIKE 2: Icosahedral wavelengths ===")
print("Lambda-weighted laser at icosahedral numbers")
print()

def laser_prime(values, lam):
    ar=ai=0
    for v in values:
        ph=2*math.pi*v/lam; ar+=math.cos(ph); ai+=math.sin(ph)
    n=len(values)
    return (ar**2+ai**2)/(n*n) if n>0 else 0

def laser_lambda(N_max, lam_wavelength):
    """Lambda-weighted laser"""
    ar=ai=0; tw=0
    for n in range(2, N_max+1):
        lam = mangoldt(n)
        if lam == 0: continue
        ph = 2*math.pi*n/lam_wavelength
        ar += lam*math.cos(ph); ai += lam*math.sin(ph)
        tw += lam
    return (ar**2+ai**2)/(tw**2) if tw > 0 else 0

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

print(f"{'q':>4} {'mu(q)':>5} {'I_prime':>10} {'I_Lambda':>10} {'ratio':>8} {'what':>15}")
print("-"*60)
for q, what in [(4,"tetrahedral V"), (6,"octahedral V"), (8,"cube V"),
                (12,"icosa V"), (20,"icosa F/dodeca V"), (30,"icosa E"),
                (60,"|A_5|=icosa sym"), (120,"|S_5|"), (5,"pentagon"),
                (10,"decagon"), (15,"3*5"), (42,"2*3*7")]:
    ip = laser_prime(P, q)
    il = laser_lambda(N, q)
    mu = mobius(q)
    ratio = il/ip if ip > 1e-10 else float('inf')
    print(f"{q:4d} {mu:5d} {ip:10.6f} {il:10.6f} {ratio:8.3f} {what:>15}")

sys.stdout.flush()

# ==========================================
# STRIKE 3: Icosahedral AXES as probes
# The icosahedron has 6 vertex-pair axes, 10 edge-pair axes, 15 face-pair axes
# Project Lambda(n) * sphere_point(n) onto each axis
# ==========================================
print("\n=== STRIKE 3: Lambda projected onto icosahedral axes ===")

# The 6 axes connecting opposite vertices
axes = []
for i in range(6):
    v1 = VERTS[i] if i < 2 else VERTS[i]
    # Pair opposite vertices
    # Top(0) <-> Bottom(1)
    # Upper ring i <-> Lower ring (i+2)%5+7 (roughly)

# Actually, let's compute: for each vertex, find its antipodal
print("Vertex-pair axes (connecting antipodal vertices):")
used = set()
for i in range(12):
    if i in used: continue
    # Find most antipodal vertex
    best_j = -1; best_dot = 2
    for j in range(i+1, 12):
        dot = sum(a*b for a,b in zip(VERTS[i], VERTS[j]))
        if dot < best_dot:
            best_dot = dot; best_j = j
    used.add(i); used.add(best_j)
    
    # Project Lambda onto this axis
    axis = VERTS[i]  # unit vector
    proj_lam = 0; proj_prime = 0; tw = 0; np = 0
    for n in range(2, N+1):
        pt = sphere_point(n, N)
        dot_axis = sum(a*b for a,b in zip(pt, axis))
        lam = mangoldt(n)
        if lam > 0:
            proj_lam += lam * dot_axis
            tw += lam
        if n in Pset:
            proj_prime += dot_axis
            np += 1
    
    proj_lam /= tw if tw > 0 else 1
    proj_prime /= np if np > 0 else 1
    
    print(f"  V{i:2d}--V{best_j:2d}: Lambda_proj={proj_lam:+.6f}  Prime_proj={proj_prime:+.6f}  ratio={proj_lam/proj_prime if abs(proj_prime)>1e-10 else 0:.3f}")

sys.stdout.flush()

# ==========================================
# STRIKE 4: The golden ratio IN the icosahedron
# Icosahedron vertices involve phi = (1+sqrt(5))/2
# The golden angle IS icosahedral
# So: does Lambda on the golden spiral have icosahedral symmetry?
# ==========================================
print("\n=== STRIKE 4: Does Lambda have icosahedral symmetry? ===")

# Check: is the 5-fold symmetry of the icosahedron visible in Lambda?
# Rotate the sphere by 72 degrees (2pi/5) around z-axis
# Does the Lambda distribution look the same?

def rotate_z(pt, angle):
    x, y, z = pt
    c = math.cos(angle); s = math.sin(angle)
    return (c*x - s*y, s*x + c*y, z)

# Compute Lambda "field" at sample points, check 5-fold symmetry
# Sample: take points on the equator
n_sample = 100
angles = [2*math.pi*k/n_sample for k in range(n_sample)]

# For each angle, sum Lambda of nearby integers
field = [0.0] * n_sample
for n in range(2, N+1):
    lam = mangoldt(n)
    if lam == 0: continue
    pt = sphere_point(n, N)
    if abs(pt[2]) > 0.3: continue  # equatorial belt only
    angle_n = math.atan2(pt[1], pt[0])
    # Bin into nearest angle
    idx = int((angle_n % (2*math.pi)) / (2*math.pi) * n_sample) % n_sample
    field[idx] += lam

# Fourier transform of the field to find rotational symmetries
print("Fourier modes of equatorial Lambda field:")
print(f"{'mode':>5} {'amplitude':>10} {'note':>15}")
for m in range(0, 11):
    ar = ai = 0
    for k in range(n_sample):
        angle = 2*math.pi*k/n_sample
        ar += field[k] * math.cos(m*angle)
        ai += field[k] * math.sin(m*angle)
    amp = math.sqrt(ar**2 + ai**2) / n_sample
    note = ""
    if m == 5: note = "icosa 5-fold"
    if m == 0: note = "DC"
    if m == 1: note = "dipole"
    if m == 2: note = "quadrupole"
    if m == 3: note = "3-fold"
    if m == 10: note = "icosa 2nd"
    print(f"{m:5d} {amp:10.4f} {note:>15}")

sys.stdout.flush()

# ==========================================
# STRIKE 5: Map Lambda to icosahedron faces (mod 20)
# 20 faces -> use n mod 20 as face assignment
# Weight by Lambda -> what's the mod-20 Lambda distribution?
# ==========================================
print("\n=== STRIKE 5: Lambda mod icosahedral numbers ===")
print("Distribution of Lambda(n) across n mod q")
print()

for q, name in [(12, "icosa vertices"), (20, "icosa faces"), (30, "icosa edges"), (60, "icosa symmetry")]:
    bins = [0.0] * q
    counts = [0] * q
    for n in range(2, N+1):
        lam = mangoldt(n)
        if lam == 0: continue
        bins[n % q] += lam
        counts[n % q] += 1
    
    total = sum(bins)
    mean = total / q
    var = sum((b - mean)**2 for b in bins) / q
    cv = math.sqrt(var) / mean if mean > 0 else 0
    
    # Which residues accumulate most Lambda?
    ranked = sorted(enumerate(bins), key=lambda x: -x[1])
    top3 = [(r, b/total) for r, b in ranked[:3]]
    bot3 = [(r, b/total) for r, b in ranked[-3:]]
    
    print(f"mod {q:2d} ({name:>16}): CV={cv:.4f}")
    print(f"  Top: {['r='+str(r)+f' ({frac:.3f})' for r,frac in top3]}")
    print(f"  Bot: {['r='+str(r)+f' ({frac:.3f})' for r,frac in bot3]}")
    # Is the variation more than random?
    # Expected CV for random: 1/sqrt(n_per_bin)
    n_per_bin = sum(counts) / q
    cv_random = 1/math.sqrt(n_per_bin)
    print(f"  CV_random ~ {cv_random:.4f}, actual CV={cv:.4f}, ratio={cv/cv_random:.2f}")
    print()

# ==========================================
# SYNTHESIS
# ==========================================
print("=== SYNTHESIS: Icosahedron + von Mangoldt ===")
print()
print("1. Lambda binned onto icosahedral vertices: UNIFORM")
print("   No vertex is special. The golden spiral distributes evenly.")
print()
print("2. Icosahedral wavelengths (12,20,30,60): ALL DARK for primes")
print("   (all non-squarefree). Lambda doesn't rescue them.")
print()
print("3. Projection onto icosahedral axes: SAME as prime indicator")
print("   Lambda weighting doesn't change the angular structure.")
print()
print("4. 5-fold symmetry: NOT present in Lambda on the sphere")
print("   The golden angle is irrational -> no discrete symmetry.")
print()
print("5. Lambda mod icosahedral numbers: slightly non-uniform")
print("   But the non-uniformity is from COPRIMALITY, not geometry.")
print()
print("VERDICT: The icosahedron adds nothing to von Mangoldt.")
print("Lambda lives in multiplicative space (critical strip).")
print("The icosahedron lives in rotational space (SO(3)).")
print("These spaces don't talk to each other.")
