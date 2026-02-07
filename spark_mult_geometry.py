#!/usr/bin/env python3
"""SPARK: Multiplicative Geometry + Zeta Zero Overtones
Lambda(n) lives in multiplicative space. The critical strip is its home.
Zeta zeros are its resonances. What happens when we probe with OVERTONES?
"""
import math, sys

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

N = 2000
LAM = {}
LN = {}
for n in range(2, N+1):
    l = mangoldt(n)
    if l > 0:
        LAM[n] = l
        LN[n] = math.log(n)

# Load zeta zeros
zeros = []
try:
    with open('z.txt') as f:
        for line in f:
            line = line.strip()
            if line:
                zeros.append(float(line))
except:
    # First 30 zeros hardcoded
    zeros = [14.1347,21.0220,25.0109,30.4249,32.9351,37.5862,40.9187,
             43.3271,48.0052,49.7738,52.9703,56.4462,59.3470,60.8318,
             65.1125,67.0798,69.5464,72.0672,75.7047,77.1448,79.3374,
             82.9104,84.7355,87.4253,88.8091,92.4919,94.6514,95.8706,
             98.8312,101.318]

print("Loaded %d zeta zeros" % len(zeros))
print()

# ==========================================
# STRIKE 1: The multiplicative laser spectrum
# F(t) = |sum Lambda(n) n^{-1/2 - it}|^2
# Fine scan near first 10 zeros
# ==========================================
print("=== STRIKE 1: Multiplicative resonance spectrum ===")
print("F(t) near each zeta zero")
print()

def F_mult(t):
    ar = ai = 0.0
    for n, l in LAM.items():
        phase = -t * LN[n]
        w = l / math.sqrt(n)
        ar += w * math.cos(phase)
        ai += w * math.sin(phase)
    return ar**2 + ai**2

# Measure F at and near each zero
print("%5s %10s %10s %10s %10s" % ("k", "gamma_k", "F(gamma)", "F(gamma-1)", "Q_est"))
print("-" * 50)
for k in range(min(20, len(zeros))):
    g = zeros[k]
    Fg = F_mult(g)
    # Estimate width: find half-max
    Fm1 = F_mult(g - 1.0)
    Fp1 = F_mult(g + 1.0)
    # Rough Q = gamma / delta_t where delta_t is half-width
    # Use F at +/- 0.5 to estimate
    Fhalf_m = F_mult(g - 0.5)
    Fhalf_p = F_mult(g + 0.5)
    half_max = Fg / 2
    # Q ~ gamma / width
    if Fm1 < half_max and Fp1 < half_max:
        Q_est = g  # width ~ 1, so Q ~ gamma
    elif Fhalf_m < half_max and Fhalf_p < half_max:
        Q_est = g / 0.5
    else:
        Q_est = g / 2  # width > 2
    print("%5d %10.4f %10.1f %10.1f %10.1f" % (k+1, g, Fg, Fm1, Q_est))

sys.stdout.flush()

# ==========================================
# STRIKE 2: Harmonic echoes of gamma_1
# Does F(t) peak at 2*gamma_1, 3*gamma_1, etc.?
# ==========================================
print()
print("=== STRIKE 2: Harmonic echoes of gamma_1 = 14.135 ===")
print("Does F(t) peak at multiples of gamma_1?")
print()

g1 = zeros[0]
print("%5s %10s %10s %10s %s" % ("mult", "t", "F(t)", "F_nearby_max", ""))
print("-" * 55)
for m in range(1, 8):
    t_harm = m * g1
    if t_harm > 100: break
    Fh = F_mult(t_harm)
    # Scan nearby for actual peak
    best_F = 0; best_t = t_harm
    for dt in range(-20, 21):
        t_try = t_harm + dt * 0.1
        if t_try < 1: continue
        Ft = F_mult(t_try)
        if Ft > best_F:
            best_F = Ft; best_t = t_try
    # Is the nearby peak a known zero?
    near_zero = ""
    for k, g in enumerate(zeros):
        if abs(best_t - g) < 0.5:
            near_zero = "gamma_%d=%.2f" % (k+1, g)
            break
    print("%5d %10.4f %10.1f %10.1f  peak@%.2f %s" % (
        m, t_harm, Fh, best_F, best_t, near_zero))

sys.stdout.flush()

# ==========================================
# STRIKE 3: Two-probe multiplicative cross-coherence
# Hit Lambda with TWO multiplicative probes at t1 and t2
# A(t) = sum Lambda(n) n^{-1/2-it} / sqrt(sum Lambda^2/n)
# cross(t1,t2) = Re(A(t1) * conj(A(t2)))
# ==========================================
print()
print("=== STRIKE 3: Cross-coherence between zeta zeros ===")
print("A(t) = sum Lambda(n) n^{-1/2-it}")
print("cross(t1,t2) = Re(A(t1)*conj(A(t2))) / |A(t1)||A(t2)|")
print()

def amplitude_mult(t):
    ar = ai = 0.0
    for n, l in LAM.items():
        phase = -t * LN[n]
        w = l / math.sqrt(n)
        ar += w * math.cos(phase)
        ai += w * math.sin(phase)
    return complex(ar, ai)

# Compute A at first 10 zeros
A_zeros = []
for k in range(min(10, len(zeros))):
    A_zeros.append(amplitude_mult(zeros[k]))

print("Amplitudes at zeros:")
for k in range(len(A_zeros)):
    a = A_zeros[k]
    print("  gamma_%d = %.4f: |A| = %.2f, phase = %.4f" % (
        k+1, zeros[k], abs(a), math.atan2(a.imag, a.real)))

print()
print("Cross-coherence matrix (normalized):")
nz = len(A_zeros)
print("     ", end="")
for j in range(nz):
    print("  g_%d  " % (j+1), end="")
print()

for i in range(nz):
    print("g_%d " % (i+1), end="")
    for j in range(nz):
        cross = (A_zeros[i] * A_zeros[j].conjugate()).real
        norm = abs(A_zeros[i]) * abs(A_zeros[j])
        c = cross / norm if norm > 1e-10 else 0
        print(" %+.3f" % c, end="")
    print()

sys.stdout.flush()

# ==========================================
# STRIKE 4: Pair correlation of zeta zeros
# R_2(s) = density of zero pairs with spacing s
# Montgomery: R_2(s) = 1 - (sin(pi*s)/(pi*s))^2
# Compute the Fourier transform (overtone spectrum)
# ==========================================
print()
print("=== STRIKE 4: Zero pair correlation (overtone spectrum) ===")
print("Spacing distribution of consecutive + all zero pairs")
print()

# Normalize spacings by mean spacing
nz_all = min(len(zeros), 200)
mean_spacing = (zeros[nz_all-1] - zeros[0]) / (nz_all - 1)
# More precise: use Riemann-von Mangoldt for mean spacing
# N(T) ~ T/(2pi) * log(T/(2*pi*e)), so mean spacing ~ 2pi/log(T/(2pi))
T_avg = sum(zeros[:nz_all]) / nz_all
mean_sp_rvM = 2 * math.pi / math.log(T_avg / (2 * math.pi))

print("Mean spacing (empirical): %.4f" % mean_spacing)
print("Mean spacing (R-vM formula): %.4f" % mean_sp_rvM)
print()

# All spacings (not just consecutive)
spacings = []
for i in range(nz_all):
    for j in range(i+1, min(i+20, nz_all)):  # up to 20th neighbor
        s = (zeros[j] - zeros[i]) / mean_sp_rvM  # normalized
        spacings.append(s)

# Histogram
print("Normalized spacing distribution (all pairs up to 20th neighbor):")
bins = 20
hist = [0] * bins
for s in spacings:
    b = int(s / 0.5)
    if 0 <= b < bins:
        hist[b] += 1

print("%8s %6s %10s %10s" % ("s_range", "count", "density", "GUE_pred"))
total_sp = len(spacings)
for b in range(bins):
    s_lo = b * 0.5
    s_hi = (b + 1) * 0.5
    s_mid = (s_lo + s_hi) / 2
    density = hist[b] / (total_sp * 0.5) if total_sp > 0 else 0
    # Montgomery pair correlation: 1 - (sin(pi*s)/(pi*s))^2
    if s_mid > 0.01:
        gue = 1 - (math.sin(math.pi * s_mid) / (math.pi * s_mid))**2
    else:
        gue = 0
    print("%4.1f-%3.1f %6d %10.4f %10.4f" % (s_lo, s_hi, hist[b], density, gue))

# Fourier transform of spacing distribution = overtone spectrum
print()
print("Overtone spectrum of zero spacings:")
print("(Fourier transform of pair correlation)")
print()
print("%6s %10s %10s" % ("freq", "power", "note"))
print("-" * 35)
for m in range(0, 16):
    freq = m * 0.5
    ar = ai = 0.0
    for s in spacings:
        ph = 2 * math.pi * freq * s
        ar += math.cos(ph); ai += math.sin(ph)
    power = (ar**2 + ai**2) / len(spacings)**2
    note = ""
    if m == 0: note = "DC"
    if m == 1: note = "fundamental"
    if m == 2: note = "2nd harmonic"
    print("%6.1f %10.6f %s" % (freq, power, note))

sys.stdout.flush()

# ==========================================
# STRIKE 5: Explicit formula overtones
# psi(x) = x - sum_rho x^rho/rho - log(2pi) - 1/2*log(1-x^-2)
# Each zero contributes: -x^{1/2+i*gamma}/(1/2+i*gamma) + conjugate
#                       = -2*x^{1/2} * cos(gamma*log(x)) * Re(1/rho)
#                         + sin term
# So each zero creates a wave in x-space with "frequency" gamma/(2pi) in log(x)
# What do these overtones look like?
# ==========================================
print()
print("=== STRIKE 5: Explicit formula as overtone series ===")
print("psi(x) = x - sum 2*Re(x^rho/rho)")
print("Each zero k contributes a wave with freq gamma_k in log-space")
print()

# Compute partial sums of the explicit formula
def psi_partial(x, K):
    """psi(x) using first K zeros"""
    result = x  # main term
    for k in range(K):
        g = zeros[k]
        rho_r = 0.5; rho_i = g
        # x^rho = x^{1/2} * exp(i*gamma*log(x))
        lx = math.log(x)
        xhalf = math.sqrt(x)
        phase = g * lx
        # x^rho / rho = x^{1/2} * exp(i*gamma*ln(x)) / (1/2 + i*gamma)
        # = x^{1/2} * (cos(phase) + i*sin(phase)) * (1/2 - i*gamma) / (1/4 + gamma^2)
        denom = 0.25 + g**2
        re_inv_rho = 0.5 / denom
        im_inv_rho = -g / denom
        re_xrho = xhalf * math.cos(phase)
        im_xrho = xhalf * math.sin(phase)
        # Re(x^rho / rho)
        re_term = re_xrho * re_inv_rho - im_xrho * im_inv_rho
        result -= 2 * re_term  # both rho and conj(rho)
    return result

# True psi(x) = sum_{n<=x} Lambda(n)
def psi_true(x):
    s = 0.0
    for n in range(2, int(x)+1):
        t = n
        for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]:
            if t==1: break
            k=0
            while t%p==0: t//=p; k+=1
            if k>0 and t==1: s+=math.log(p); break
        else:
            if t>1: s+=math.log(n)
    return s

# Compare at x = 100
x = 100.0
true_val = psi_true(x)
print("psi(100) true = %.4f" % true_val)
print("psi(100) main term (=x) = %.4f" % x)
print()
print("%5s %10s %10s %10s" % ("K", "psi_K(100)", "error", "rel_err"))
print("-" * 40)
for K in [1, 2, 3, 5, 10, 20, 30, 50, min(100, len(zeros))]:
    if K > len(zeros): break
    val = psi_partial(x, K)
    err = val - true_val
    rel = err / true_val if true_val > 0 else 0
    print("%5d %10.4f %10.4f %10.4f" % (K, val, err, rel))

sys.stdout.flush()

# ==========================================
# STRIKE 6: Overtone interference
# What if we ADD the contributions of pairs of zeros?
# At x where cos(gamma_i * log(x)) and cos(gamma_j * log(x))
# are BOTH positive, we get constructive interference.
# Where does this happen?
# ==========================================
print()
print("=== STRIKE 6: Overtone interference between zeros ===")
print("When do two zeros constructively interfere?")
print()

# For gamma_i and gamma_j, constructive when:
# gamma_i * log(x) = 2*pi*m  AND  gamma_j * log(x) = 2*pi*n
# => log(x) = 2*pi*m/gamma_i = 2*pi*n/gamma_j
# => m/n = gamma_i/gamma_j
# Constructive when gamma_i/gamma_j is nearly rational!

print("Zero frequency ratios gamma_i/gamma_j:")
print("If near a simple fraction -> overtone resonance!")
print()
print("%5s %5s %10s %12s %8s" % ("i", "j", "ratio", "near_frac", "quality"))
print("-" * 48)

def best_rational(x, max_denom=20):
    """Find best rational approximation p/q with q <= max_denom"""
    best_err = 1.0; best_p = 0; best_q = 1
    for q in range(1, max_denom+1):
        p = round(x * q)
        err = abs(x - p/q)
        if err < best_err:
            best_err = err; best_p = p; best_q = q
    return best_p, best_q, best_err

for i in range(min(8, len(zeros))):
    for j in range(i+1, min(8, len(zeros))):
        ratio = zeros[i] / zeros[j]
        p, q, err = best_rational(ratio)
        quality = 1.0 / (err * q + 0.001)
        if quality > 5:  # only show good ones
            print("%5d %5d %10.6f %8d/%-3d %8.1f" % (
                i+1, j+1, ratio, p, q, quality))

# Which x values see maximum constructive interference?
print()
print("Constructive interference hotspots:")
print("x where sum_k cos(gamma_k * log(x)) is maximized")
print()

x_vals = [math.exp(lx/10.0) for lx in range(10, 100)]  # x from e^1 to e^10
print("%8s %10s %10s %10s" % ("x", "sum_cos", "n_zeros", "mean_cos"))
print("-" * 42)
best_sc = -999; best_x = 0
for x in x_vals:
    lx = math.log(x)
    sc = sum(math.cos(g * lx) for g in zeros[:30])
    mean_c = sc / 30
    if sc > best_sc:
        best_sc = sc; best_x = x
    if abs(sc) > 5 or x in [math.e, math.e**2, math.e**5, math.e**10]:
        tag = " ***" if sc > 8 else ""
        print("%8.1f %10.4f %10d %10.4f%s" % (x, sc, 30, mean_c, tag))

print()
print("Maximum constructive interference at x = %.1f" % best_x)
print("  log(x) = %.4f, sum_cos = %.4f" % (math.log(best_x), best_sc))
# Is this near a prime power?
lbx = math.log(best_x)
print("  Nearest integer to x: %d" % round(best_x))
near_n = round(best_x)
l = mangoldt(near_n) if 2 <= near_n <= 10000 else 0
print("  Lambda(%d) = %.4f %s" % (near_n, l, "(prime power!)" if l > 0 else "(composite)"))

sys.stdout.flush()

# ==========================================
# STRIKE 7: The multiplicative SFF
# K(tau) = |sum_k exp(i * gamma_k * tau)|^2 / N_zeros
# This is the spectral form factor of zeta zeros
# For GUE: K(tau) = min(tau, 1) (after normalization)
# ==========================================
print()
print("=== STRIKE 7: Spectral Form Factor of zeta zeros ===")
print("K(tau) = |sum exp(i*gamma_k*tau)|^2 / N")
print("GUE prediction: K(tau) = min(tau, 1)")
print()

nz_sff = min(len(zeros), 100)
# Normalize: tau in units where mean spacing = 1
# tau_phys = tau * 2*pi / mean_spacing
mean_sp = mean_sp_rvM

print("%6s %10s %10s %10s" % ("tau", "K(tau)", "GUE", "ratio"))
print("-" * 40)
for ti in range(1, 41):
    tau = ti * 0.1  # normalized tau
    tau_phys = tau * 2 * math.pi / mean_sp
    ar = ai = 0.0
    for k in range(nz_sff):
        phase = zeros[k] * tau_phys
        ar += math.cos(phase); ai += math.sin(phase)
    K = (ar**2 + ai**2) / nz_sff
    gue = min(tau, 1.0)
    ratio = K / gue if gue > 0.01 else 0
    tag = ""
    if abs(ratio - 1) < 0.15: tag = " match"
    print("%6.1f %10.4f %10.4f %10.4f%s" % (tau, K, gue, ratio, tag))

sys.stdout.flush()
