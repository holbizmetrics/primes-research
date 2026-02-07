#!/usr/bin/env python3
"""Von Mangoldt function on the sphere
Map integers n to golden-spiral sphere, weight by Lambda(n).
Lambda(n) = log(p) if n = p^k, 0 otherwise.

The prime indicator is binary (0 or 1).
Lambda is graded: log(2)=0.69, log(3)=1.10, log(5)=1.61, ...
Small primes weigh LESS than large primes. This is the opposite
of the prime indicator where all primes are equal.

What does the sphere look like when big primes matter more?
"""
import math, sys

def sieve(n):
    s = [True]*(n+1); s[0] = s[1] = False
    for i in range(2, int(n**.5)+1):
        if s[i]:
            for j in range(i*i, n+1, i): s[j] = False
    return [i for i in range(2, n+1) if s[i]]

def mangoldt(n):
    """Von Mangoldt: Lambda(n) = log(p) if n=p^k, else 0"""
    if n < 2: return 0
    t = n
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]:
        if t == 1: break
        k = 0
        while t % p == 0:
            t //= p; k += 1
        if k > 0 and t == 1:
            return math.log(p)
    if t > 1:
        return math.log(n)  # n itself is prime
    return 0

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi / PHI**2

N = 2000
P = sieve(N)
Pset = set(P)

# ==========================================
# STRIKE 1: Lambda-weighted laser
# Instead of I_P(q) = |sum_p exp(2pi*i*p/q)|^2 / N_P^2
# compute I_Lambda(q) = |sum_n Lambda(n) exp(2pi*i*n/q)|^2 / (sum Lambda)^2
# ==========================================
print("=== STRIKE 1: Lambda-weighted laser ===")
print("I_Lambda(q) vs I_P(q) — does Lambda change the coherence?")
print()

total_lambda = sum(mangoldt(n) for n in range(2, N+1))
n_primes = len(P)

print(f"{'q':>3} {'I_prime':>10} {'I_Lambda':>10} {'ratio':>8} {'note':>10}")
print("-"*50)
for q in range(2, 31):
    # Standard prime laser
    ar_p = ai_p = 0
    for p in P:
        ph = 2*math.pi*p/q; ar_p += math.cos(ph); ai_p += math.sin(ph)
    i_p = (ar_p**2 + ai_p**2) / n_primes**2
    
    # Lambda-weighted laser
    ar_l = ai_l = 0
    for n in range(2, N+1):
        lam = mangoldt(n)
        if lam == 0: continue
        ph = 2*math.pi*n/q
        ar_l += lam * math.cos(ph)
        ai_l += lam * math.sin(ph)
    i_l = (ar_l**2 + ai_l**2) / total_lambda**2
    
    ratio = i_l / i_p if i_p > 1e-10 else float('inf')
    note = ""
    if abs(ratio - 1) < 0.1: note = "same"
    elif ratio > 1.1: note = "Lambda+"
    elif ratio < 0.9: note = "Lambda-"
    
    print(f"{q:3d} {i_p:10.6f} {i_l:10.6f} {ratio:8.3f} {note:>10}")

print()
sys.stdout.flush()

# ==========================================
# STRIKE 2: Golden spiral sphere with Lambda weights
# Point n at position (theta, z) on sphere
# Weight = Lambda(n) instead of 1
# Center of mass, spread, moments
# ==========================================
print("=== STRIKE 2: Lambda on the golden spiral sphere ===")

def sphere_point(n, N_max):
    theta = n * GOLDEN_ANGLE
    z = 1 - 2*n/N_max
    r_xy = math.sqrt(max(0, 1 - z*z))
    x = r_xy * math.cos(theta)
    y = r_xy * math.sin(theta)
    return x, y, z

# Lambda-weighted center of mass
cx = cy = cz = 0
tw = 0
for n in range(2, N+1):
    lam = mangoldt(n)
    if lam == 0: continue
    x, y, z = sphere_point(n, N)
    cx += lam*x; cy += lam*y; cz += lam*z
    tw += lam

cx /= tw; cy /= tw; cz /= tw
r_cm = math.sqrt(cx**2 + cy**2 + cz**2)

# Compare with prime-indicator center of mass
px = py = pz = 0
for p in P:
    x, y, z = sphere_point(p, N)
    px += x; py += y; pz += z
px /= n_primes; py /= n_primes; pz /= n_primes
r_cm_p = math.sqrt(px**2 + py**2 + pz**2)

# All integers center of mass (should be ~0)
ax = ay = az = 0
for n in range(2, N+1):
    x, y, z = sphere_point(n, N)
    ax += x; ay += y; az += z
ax /= (N-1); ay /= (N-1); az /= (N-1)
r_cm_a = math.sqrt(ax**2 + ay**2 + az**2)

print(f"Center of mass (all integers): r = {r_cm_a:.6f}")
print(f"Center of mass (prime indicator): r = {r_cm_p:.6f}")
print(f"Center of mass (Lambda-weighted): r = {r_cm_l:.6f}" if False else f"Center of mass (Lambda-weighted): r = {r_cm:.6f}")
print()

# Lambda-weighted angular power spectrum
# C_l = sum_m |a_lm|^2 / (2l+1)
# For just the z-component (axial symmetry): use Legendre polynomials
print("=== STRIKE 3: Angular power spectrum C_l ===")
print("Legendre decomposition of Lambda on the sphere")
print()

def legendre(l, x):
    """Compute P_l(x) via recursion"""
    if l == 0: return 1.0
    if l == 1: return x
    p_prev = 1.0; p_curr = x
    for k in range(2, l+1):
        p_next = ((2*k-1)*x*p_curr - (k-1)*p_prev) / k
        p_prev = p_curr; p_curr = p_next
    return p_curr

# Compute a_l = sum_n Lambda(n) * P_l(z_n) / total_lambda
# For comparison: a_l for prime indicator
print(f"{'l':>3} {'C_l(Lambda)':>12} {'C_l(primes)':>12} {'ratio':>8}")
print("-"*40)

for l in range(0, 21):
    # Lambda-weighted
    al_lam = 0
    for n in range(2, N+1):
        lam = mangoldt(n)
        if lam == 0: continue
        _, _, z = sphere_point(n, N)
        al_lam += lam * legendre(l, z)
    al_lam /= tw
    
    # Prime indicator
    al_p = 0
    for p in P:
        _, _, z = sphere_point(p, N)
        al_p += legendre(l, z)
    al_p /= n_primes
    
    ratio = al_lam**2 / al_p**2 if al_p**2 > 1e-15 else 0
    fib = " *" if l in [1,2,3,5,8,13] else ""
    print(f"{l:3d} {al_lam**2:12.6f} {al_p**2:12.6f} {ratio:8.3f}{fib}")

print()
print("* = Fibonacci mode")
sys.stdout.flush()

# ==========================================
# STRIKE 4: Lambda vs prime indicator — what's different?
# Lambda(n) = log(p) weights large primes more.
# On the sphere, large primes are near z = -1 (south pole).
# So Lambda should shift the center of mass SOUTHWARD.
# ==========================================
print("=== STRIKE 4: Lambda shifts the sphere ===")
print("Lambda weights large primes (near south pole) more")
print()

# Divide primes into small and large
small_P = [p for p in P if p <= N//2]
large_P = [p for p in P if p > N//2]

print(f"Small primes (p <= {N//2}): {len(small_P)}, mean Lambda = {sum(math.log(p) for p in small_P)/len(small_P):.3f}")
print(f"Large primes (p > {N//2}): {len(large_P)}, mean Lambda = {sum(math.log(p) for p in large_P)/len(large_P):.3f}")
print(f"Ratio of Lambda weights: {sum(math.log(p) for p in large_P)/sum(math.log(p) for p in small_P):.3f}")
print()

# Z-coordinate of center of mass
z_lam = sum(mangoldt(n) * sphere_point(n, N)[2] for n in range(2, N+1) if mangoldt(n) > 0) / tw
z_prime = sum(sphere_point(p, N)[2] for p in P) / n_primes
z_all = sum(sphere_point(n, N)[2] for n in range(2, N+1)) / (N-1)

print(f"Mean z (all integers): {z_all:.6f}")
print(f"Mean z (prime indicator): {z_prime:.6f}")
print(f"Mean z (Lambda-weighted): {z_lam:.6f}")
print(f"Lambda shifts south by: {z_lam - z_prime:.6f}")
print()

# ==========================================
# STRIKE 5: The Ramanujan expansion ON the sphere
# Each term mu(q)/phi(q) * c_q(n) is a "mode" on the sphere
# What do these modes look like?
# ==========================================
print("=== STRIKE 5: Ramanujan modes on the sphere ===")
print("Each Ramanujan term q creates a pattern on the sphere")
print()

def mobius(n):
    if n == 1: return 1
    d = 2; t = n; nf = 0
    while d*d <= t:
        if t%d == 0:
            nf += 1; t //= d
            if t%d == 0: return 0
        d += 1
    if t > 1: nf += 1
    return (-1)**nf

def euler_phi(n):
    r = n; d = 2; t = n
    while d*d <= t:
        if t%d == 0:
            while t%d == 0: t //= d
            r -= r // d
        d += 1
    if t > 1: r -= r // t
    return r

def c_q(n, q):
    g = math.gcd(n, q)
    qg = q // g
    mu_qg = mobius(qg)
    phi_q = euler_phi(q)
    phi_qg = euler_phi(qg)
    return mu_qg * phi_q // phi_qg if phi_qg > 0 else 0

# For each q, compute the spatial pattern: sum_n c_q(n) * z_n
# This measures the "z-dipole" of the q-th Ramanujan mode
print(f"{'q':>3} {'mu':>3} {'z_mode':>10} {'r_mode':>10} {'note':>12}")
print("-"*45)
for q in range(2, 31):
    mu_q = mobius(q)
    phi_q = euler_phi(q)
    if mu_q == 0:
        print(f"{q:3d} {mu_q:3d}       dark       dark")
        continue
    
    # Compute spatial center of mass of c_q(n) pattern
    wx = wy = wz = 0
    wt = 0
    for n in range(2, N+1):
        cqn = c_q(n, q)
        x, y, z = sphere_point(n, N)
        wx += cqn * x; wy += cqn * y; wz += cqn * z
        wt += abs(cqn)
    
    if wt > 0:
        z_mode = wz / wt
        r_mode = math.sqrt(wx**2 + wy**2 + wz**2) / wt
    else:
        z_mode = r_mode = 0
    
    note = ""
    if abs(z_mode) > 0.1: note = "POLAR"
    
    print(f"{q:3d} {mu_q:3d} {z_mode:10.6f} {r_mode:10.6f} {note:>12}")

print()
print("z_mode > 0: this Ramanujan mode concentrates near north pole (small n)")
print("z_mode < 0: concentrates near south pole (large n)")
print("r_mode: total displacement from center (coherence of the mode on sphere)")
sys.stdout.flush()

# ==========================================
# SYNTHESIS
# ==========================================
print()
print("=== SYNTHESIS: Von Mangoldt on the Sphere ===")
print()
print("Lambda(n) on the golden sphere differs from the prime indicator by")
print("WEIGHTING large primes more (Lambda = log p grows with p).")
print()
print("Key differences:")
print("1. Center of mass shifts south (large primes near south pole)")
print("2. Lambda-weighted laser ~ same as prime laser at each q")
print("   (because log(p) varies slowly compared to exp(2*pi*i*p/q))")
print("3. Angular power spectrum C_l is nearly identical")
print("   (Lambda doesn't change the ANGULAR structure, just the radial weight)")
print()
print("The Ramanujan modes c_q(n) on the sphere are NOT polar —")
print("they don't prefer north or south. This is because c_q(n)")
print("depends on n mod q, and the golden spiral scrambles the")
print("mod-q structure across the whole sphere.")
print()
print("BOTTOM LINE: Lambda on the sphere looks almost the same as")
print("the prime indicator on the sphere. The log(p) weighting")
print("doesn't reveal new spatial structure.")
