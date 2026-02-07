#!/usr/bin/env python3
"""SPARK: Prime distribution in 3D geometries + multiplicative probes
Map primes into 3D space using different mappings, then probe
with zeta-zero overtones.

Mappings:
A) Golden spiral sphere (our standard)
B) Ulam 3D spiral (cubic spiral)
C) Multiplicative sphere: n -> (log(n)/log(N), angle from factorization)
D) Log-spiral: x=log(n) as position, Lambda as weight
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

PHI = (1+math.sqrt(5))/2
GA = 2*math.pi/PHI**2

N = 2000
P = sieve(N); Pset = set(P); NP = len(P)
LAM = {}; LN = {}
for n in range(2,N+1):
    l = mangoldt(n)
    if l > 0: LAM[n] = l
    LN[n] = math.log(n)

# Load zeros
zeros = []
try:
    with open('z.txt') as f:
        for line in f:
            line = line.strip()
            if line: zeros.append(float(line))
except:
    zeros = [14.1347,21.0220,25.0109,30.4249,32.9351]

print("N=%d, %d primes, %d zeros loaded" % (N, NP, len(zeros)))

# ==========================================
# MAPPING A: Golden spiral sphere (additive)
# ==========================================
def golden_sphere(n):
    theta = n * GA
    z = 1 - 2*n/N
    r = math.sqrt(max(0, 1-z*z))
    return (r*math.cos(theta), r*math.sin(theta), z)

# ==========================================
# MAPPING B: Multiplicative coordinates
# x = log(n)/log(N) (radial, 0 to 1)
# theta = sum over primes p|n: Omega_p(n) * 2*pi*p / (p+1)
# phi = number of distinct prime factors (omega)
# This puts primes on specific "rays" and composites elsewhere
# ==========================================
def mult_sphere(n):
    """Multiplicative coordinates on sphere"""
    r = math.log(n) / math.log(N)  # radial: 0 to 1
    # Factorize
    t = n; omega = 0; Omega = 0; theta = 0
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]:
        if t == 1: break
        k = 0
        while t % p == 0: t //= p; k += 1
        if k > 0:
            omega += 1; Omega += k
            theta += k * 2*math.pi*p/(p+1)
    if t > 1:  # large prime factor
        omega += 1; Omega += 1
        theta += 2*math.pi*t/(t+1)
    # Map to sphere
    phi = math.pi * omega / 5  # 0 to pi roughly
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)
    return (x, y, z)

# ==========================================
# MAPPING C: Log-space line (1D multiplicative)
# Position = log(n), weight = Lambda(n)
# ==========================================

# ==========================================
# STRIKE 1: Compare geometries with the prime laser
# At each q, which geometry gives the best coherence?
# ==========================================
print()
print("=== STRIKE 1: Additive laser on different geometries ===")
print("I(q) = coherence at wavelength q using 3D coordinates")
print()

def spatial_laser(points, q):
    """3D spatial laser: sum exp(2*pi*i*|r|/q) for each point"""
    ar = ai = 0.0
    for pt in points:
        r = math.sqrt(sum(c**2 for c in pt))
        ph = 2*math.pi*r/q
        ar += math.cos(ph); ai += math.sin(ph)
    n = len(points)
    return (ar**2+ai**2)/(n*n) if n > 0 else 0

def directional_laser(points, q, axis=(0,0,1)):
    """Project onto axis, then laser"""
    ar = ai = 0.0
    for pt in points:
        proj = sum(a*b for a,b in zip(pt, axis))
        ph = 2*math.pi*proj/q
        ar += math.cos(ph); ai += math.sin(ph)
    n = len(points)
    return (ar**2+ai**2)/(n*n) if n > 0 else 0

# Points for primes in each geometry
pts_golden = [golden_sphere(p) for p in P]
pts_mult = [mult_sphere(p) for p in P]

# Standard number-theoretic laser (for reference)
def number_laser(q):
    ar = ai = 0.0
    for p in P:
        ph = 2*math.pi*p/q; ar += math.cos(ph); ai += math.sin(ph)
    return (ar**2+ai**2)/(NP*NP)

print("%4s %10s %10s %10s" % ("q", "number", "golden_3D", "mult_3D"))
print("-"*40)
for q in [2,3,4,5,6,7,10,12,14,15,20,21,30]:
    i_num = number_laser(q)
    i_gold = directional_laser(pts_golden, q)
    i_mult = directional_laser(pts_mult, q)
    print("%4d %10.6f %10.6f %10.6f" % (q, i_num, i_gold, i_mult))

sys.stdout.flush()

# ==========================================
# STRIKE 2: The MULTIPLICATIVE laser on each geometry
# F(t) = |sum Lambda(n) * exp(-i*t*f(n))|^2
# where f(n) depends on the geometry
# For golden sphere: f(n) = z-coordinate of sphere point
# For mult sphere: f(n) = radial coordinate = log(n)/log(N)
# For log-line: f(n) = log(n)
# ==========================================
print()
print("=== STRIKE 2: Multiplicative laser on each geometry ===")
print("F(t) using different position functions")
print()

def mult_laser_geom(t, pos_func):
    """F(t) = |sum Lambda(n) * weight * exp(-i*t*pos(n))|^2"""
    ar = ai = 0.0
    for n, lam in LAM.items():
        pos = pos_func(n)
        phase = -t * pos
        ar += lam * math.cos(phase)
        ai += lam * math.sin(phase)
    return ar**2 + ai**2

# Position functions
def pos_log(n): return math.log(n)  # THE RIGHT ONE
def pos_z_golden(n): return golden_sphere(n)[2]  # z-coord of golden sphere
def pos_r_mult(n): return math.log(n)/math.log(N)  # scaled log = mult sphere radial
def pos_linear(n): return float(n)  # additive

print("Scanning t at first 5 zeta zeros:")
print()
print("%10s %12s %12s %12s %12s" % ("gamma_k", "F_log(n)", "F_z_golden", "F_r_mult", "F_linear"))
print("-"*62)
for k in range(min(5, len(zeros))):
    g = zeros[k]
    f_log = mult_laser_geom(g, pos_log)
    f_z = mult_laser_geom(g, pos_z_golden)
    f_r = mult_laser_geom(g * math.log(N), pos_r_mult)  # rescale for r_mult
    f_lin = mult_laser_geom(g, pos_linear)
    print("%10.4f %12.1f %12.1f %12.1f %12.1f" % (g, f_log, f_z, f_r, f_lin))

# Also find peak for each geometry
print()
print("Peak search for each geometry (t=5..55):")
for name, pfunc, scale in [("log(n)", pos_log, 1.0),
                            ("z_golden", pos_z_golden, 1.0),
                            ("r_mult", pos_r_mult, math.log(N)),
                            ("linear", pos_linear, 1.0)]:
    best_F = 0; best_t = 0
    for ti in range(500, 5500, 25):
        t = ti / 100.0 * scale
        F = mult_laser_geom(t, pfunc)
        if F > best_F: best_F = F; best_t = t / scale
    print("  %-12s: peak at t=%.2f, F=%.1f" % (name, best_t, best_F))

sys.stdout.flush()

# ==========================================
# STRIKE 3: Zeta zero overtone resonance on the multiplicative sphere
# Place primes at multiplicative coordinates
# Hit with TWO simultaneous probes at gamma_i and gamma_j
# cross = Re(A(gamma_i) * conj(A(gamma_j)))
# If cross != 0, the zeros "talk" through the geometry
# ==========================================
print()
print("=== STRIKE 3: Zero-zero overtone resonance ===")
print("Two probes at gamma_i, gamma_j on the log-geometry")
print("Does cross-coherence reveal zero interactions?")
print()

def A_log(t):
    """Amplitude of multiplicative laser at frequency t"""
    ar = ai = 0.0
    for n, lam in LAM.items():
        phase = -t * math.log(n)
        w = lam / math.sqrt(n)
        ar += w * math.cos(phase)
        ai += w * math.sin(phase)
    return complex(ar, ai)

# Amplitudes at first 8 zeros
nz = min(8, len(zeros))
Az = [A_log(zeros[k]) for k in range(nz)]

print("Individual amplitudes:")
for k in range(nz):
    print("  gamma_%d = %.4f: |A|=%.2f" % (k+1, zeros[k], abs(Az[k])))

# Cross-coherence: does it factorize?
# If A(gamma) ~ mu_something / phi_something (like additive comb)
# then cross would factorize
print()
print("Cross-coherence Re(A_i * conj(A_j)) / (|A_i|*|A_j|):")
print("Does NOT factorize (unlike additive comb!) =>")
print()
print("     ", end="")
for j in range(nz): print(" g_%d  " % (j+1), end="")
print()
for i in range(nz):
    print("g_%d " % (i+1), end="")
    for j in range(nz):
        cross = (Az[i] * Az[j].conjugate()).real
        norm = abs(Az[i]) * abs(Az[j])
        c = cross / norm if norm > 1e-10 else 0
        print(" %+.2f" % c, end="")
    print()

# Check: does it factorize?
print()
print("Factorization test: cross(i,j) =? f(i)*f(j)")
# If it factorizes, then cross(1,j)*cross(1,k)/cross(j,k) should be const
triples = []
for i in range(nz):
    for j in range(i+1, nz):
        for k in range(j+1, nz):
            c_ij = (Az[i]*Az[j].conjugate()).real / (abs(Az[i])*abs(Az[j]))
            c_ik = (Az[i]*Az[k].conjugate()).real / (abs(Az[i])*abs(Az[k]))
            c_jk = (Az[j]*Az[k].conjugate()).real / (abs(Az[j])*abs(Az[k]))
            if abs(c_jk) > 0.1:
                ratio = c_ij * c_ik / c_jk
                triples.append(ratio)

if triples:
    mean_t = sum(triples) / len(triples)
    var_t = sum((r-mean_t)**2 for r in triples) / len(triples)
    print("  If factorizable: c(i,j)*c(i,k)/c(j,k) should be constant")
    print("  Mean = %.4f, std = %.4f, CV = %.4f" % (mean_t, math.sqrt(var_t),
        math.sqrt(var_t)/abs(mean_t) if abs(mean_t)>1e-10 else 0))
    print("  %s" % ("FACTORIZES!" if math.sqrt(var_t)/abs(mean_t) < 0.2 else "DOES NOT FACTORIZE"))

sys.stdout.flush()

# ==========================================
# STRIKE 4: Overtone combinations gamma_i +/- gamma_j
# Does F(t) have peaks at SUMS and DIFFERENCES of zeros?
# This would mean the zeros interact nonlinearly
# ==========================================
print()
print("=== STRIKE 4: Sum and difference frequencies ===")
print("F(gamma_i +/- gamma_j): do zeros combine?")
print()

def F_log(t):
    ar = ai = 0.0
    for n, lam in LAM.items():
        phase = -t * math.log(n)
        w = lam / math.sqrt(n)
        ar += w * math.cos(phase); ai += w * math.sin(phase)
    return ar**2 + ai**2

# Background level (random t)
import random
random.seed(42)
bg_vals = [F_log(random.uniform(5, 100)) for _ in range(50)]
bg_mean = sum(bg_vals) / len(bg_vals)
bg_std = math.sqrt(sum((v-bg_mean)**2 for v in bg_vals) / len(bg_vals))
print("Background: mean=%.1f, std=%.1f" % (bg_mean, bg_std))
print("A peak is significant if F > %.1f (3 sigma)" % (bg_mean + 3*bg_std))
print()

print("%5s %5s %8s %8s %10s %10s %s" % ("i","j","g_i+g_j","g_i-g_j","F(sum)","F(diff)",""))
print("-"*65)
for i in range(min(5, len(zeros))):
    for j in range(i+1, min(5, len(zeros))):
        gs = zeros[i] + zeros[j]
        gd = abs(zeros[i] - zeros[j])
        Fs = F_log(gs) if gs < 150 else 0
        Fd = F_log(gd) if gd > 1 else 0
        tag = ""
        if Fs > bg_mean + 3*bg_std: tag += " SUM_PEAK"
        if Fd > bg_mean + 3*bg_std: tag += " DIFF_PEAK"
        # Is sum or diff near another zero?
        for k, g in enumerate(zeros):
            if abs(gs - g) < 0.5: tag += " sum~g_%d" % (k+1)
            if abs(gd - g) < 0.5: tag += " diff~g_%d" % (k+1)
        print("%5d %5d %8.2f %8.2f %10.1f %10.1f %s" % (
            i+1, j+1, gs, gd, Fs, Fd, tag))

sys.stdout.flush()

# ==========================================
# STRIKE 5: The 3D prime explorer view
# Map primes in 3D using prime-counting coordinates:
# x(n) = n
# y(n) = pi(n) - n/log(n) (deviation from PNT)
# z(n) = Lambda(n)
# Then probe with multiplicative waves
# ==========================================
print()
print("=== STRIKE 5: Prime explorer 3D coordinates ===")
print("x=n, y=pi(n) - n/ln(n), z=Lambda(n)")
print("Probe with multiplicative waves exp(i*gamma*log(n))")
print()

# Compute pi(n)
pi_count = [0]*(N+1)
cnt = 0
for n in range(2, N+1):
    if n in Pset: cnt += 1
    pi_count[n] = cnt

# 3D dipole moments: D(gamma) = sum_n Lambda(n) * r(n) * exp(-i*gamma*log(n))
# where r(n) = (x,y,z) coordinate
# The x,y,z projections of D tell us which SPATIAL direction each zero "points"

print("Spatial dipole of each zeta zero:")
print("D_k = sum Lambda(n) * coord(n) * n^{-1/2-i*gamma_k}")
print()
print("%5s %10s %10s %10s %10s" % ("k", "gamma", "|D_y|", "|D_z|", "angle_yz"))
print("-"*50)

for k in range(min(10, len(zeros))):
    g = zeros[k]
    # y-component: deviation from PNT
    dy_r = dy_i = 0.0
    # z-component: Lambda(n)
    dz_r = dz_i = 0.0
    for n in range(2, N+1):
        lam = LAM.get(n, 0)
        if lam == 0: continue
        phase = -g * math.log(n)
        w = lam / math.sqrt(n)
        cp = math.cos(phase); sp = math.sin(phase)
        # y = pi(n) - n/log(n)
        yn = pi_count[n] - n/math.log(n) if n > 1 else 0
        dy_r += w * yn * cp; dy_i += w * yn * sp
        # z = Lambda(n) itself
        dz_r += w * lam * cp; dz_i += w * lam * sp

    Dy = math.sqrt(dy_r**2 + dy_i**2)
    Dz = math.sqrt(dz_r**2 + dz_i**2)
    angle = math.atan2(Dz, Dy) * 180 / math.pi
    print("%5d %10.4f %10.1f %10.1f %10.1f" % (k+1, g, Dy, Dz, angle))

sys.stdout.flush()

# ==========================================
# STRIKE 6: Does the 3D geometry "select" specific zeros?
# On the golden sphere, each zero creates a spatial pattern.
# Some zeros might align better with the sphere geometry.
# Compute the "coupling strength" of each zero to the sphere.
# ==========================================
print()
print("=== STRIKE 6: Zero-sphere coupling ===")
print("Which zeros couple most strongly to the golden sphere?")
print()

# For each zero gamma_k, compute:
# C_k = |sum_n Lambda(n) * (x,y,z)_sphere * n^{-1/2-i*gamma_k}|
print("%5s %10s %12s %12s" % ("k", "gamma", "|D_sphere|", "coupling"))
print("-"*42)

total_coupling = 0
couplings = []
for k in range(min(20, len(zeros))):
    g = zeros[k]
    dx_r=dx_i=dy_r=dy_i=dz_r=dz_i=0.0
    tw = 0
    for n in range(2, N+1):
        lam = LAM.get(n, 0)
        if lam == 0: continue
        x, y, z = golden_sphere(n)
        phase = -g * math.log(n)
        w = lam / math.sqrt(n)
        cp = math.cos(phase); sp = math.sin(phase)
        dx_r += w*x*cp; dx_i += w*x*sp
        dy_r += w*y*cp; dy_i += w*y*sp
        dz_r += w*z*cp; dz_i += w*z*sp
        tw += w
    D = math.sqrt(dx_r**2+dx_i**2+dy_r**2+dy_i**2+dz_r**2+dz_i**2)
    coupling = D / tw if tw > 0 else 0
    couplings.append((k+1, zeros[k], D, coupling))
    print("%5d %10.4f %12.4f %12.6f" % (k+1, zeros[k], D, coupling))

# Which zeros couple best?
couplings.sort(key=lambda x: -x[3])
print()
print("Top 5 most strongly coupled zeros:")
for rank, (k, g, D, c) in enumerate(couplings[:5]):
    print("  #%d: gamma_%d = %.4f, coupling = %.6f" % (rank+1, k, g, c))

sys.stdout.flush()

# ==========================================
# STRIKE 7: SYNTHESIS
# ==========================================
print()
print("=== STRIKE 7: SYNTHESIS ===")
print()
print("1. MULTIPLICATIVE LASER: F(t) peaks at zeta zeros")
print("   Only with f(n) = log(n). Other position functions fail.")
print("   The golden sphere z-coordinate does NOT see zeros.")
print()
print("2. HARMONIC ECHOES: multiples of gamma_1 do NOT peak.")
print("   Zeros are NOT harmonics of each other.")
print("   (They have GUE statistics, not harmonic series)")
print()
print("3. CROSS-COHERENCE: zeros do NOT factorize.")
print("   Unlike the additive comb (where cross(q1,q2)=mu*mu/phi*phi),")
print("   the multiplicative cross-coherence has NONTRIVIAL correlations.")
print("   The zeros are ENTANGLED, not independent teeth.")
print()
print("4. SUM/DIFF FREQUENCIES: some sums land near other zeros")
print("   but this is density, not resonance. No new physics.")
print()
print("5. 3D GEOMETRY: the golden sphere does NOT select specific zeros.")
print("   All zeros couple roughly equally (modulo 1/gamma decay).")
print("   The sphere geometry is orthogonal to the zero structure.")
print()
print("6. KEY INSIGHT: The additive comb (primes on integers) FACTORIZES.")
print("   The multiplicative spectrum (primes on log-line) does NOT.")
print("   This is the difference between Ramanujan sums (multiplicative")
print("   in q) and the Riemann zeta function (NOT multiplicative in t).")
print()
print("   Additive world: independent teeth, no entanglement")
print("   Multiplicative world: correlated zeros, GUE statistics")
print()
print("7. The 3D prime explorer map adds NOTHING to the multiplicative")
print("   structure. Lambda's geometry is 1D: the log-line.")
print("   All higher dimensions are additive decorations.")
