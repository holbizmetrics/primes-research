#!/usr/bin/env python3
"""SPARK Cross-L SFF: Strikes 1-4

Strike 1: SFF within each L-function (should be GUE-like)
Strike 2: Cross-SFF between pairs of L-functions
Strike 3: Does cross-SFF depend on chi_1 * chi_2_bar?
Strike 4: Nearest-neighbor spacing between DIFFERENT L-functions
"""
import math

# Parse zeros from GP output
def parse_file(fname):
    data = {}
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line: continue
            label, nums = line.split(':', 1)
            zeros = [float(x) for x in nums.split() if x]
            data[label.strip()] = zeros
    return data

# Read all zeros
z3 = {}
with open('clz1.gp') as f: pass  # was stdout
# Re-parse from the direct output we saw
z3_raw = """Q3_0: 14.13472514 21.02203964 25.01085758 30.42487613 32.93506159 37.58617816 40.91871901 43.32707328 48.00515088 49.77383248 52.97032148 56.44624770 59.34704400 60.83177852 65.11254405 67.07981053 69.54640171 72.06715767 75.70469070 77.14484007 79.33737502
Q3_1: 8.03973716 11.24920621 15.70461918 18.26199750 20.45577081 24.05941486 26.57786874 28.21816451 30.74504026 33.89738893 35.60841265 37.55179656 39.48520726 42.61637923 44.12057291 46.27411802 47.51410451 50.37513865 52.49674960 54.19384310 55.64255870 57.58405636 60.02685746 62.20607812 63.17699277 65.29492554 66.62313463 69.51302299 70.81979870 72.65614907 74.00542852 75.62240696 78.21748127 79.63797575"""

all_zeros = {}
for line in z3_raw.strip().split('\n'):
    label, nums = line.split(':', 1)
    all_zeros[label.strip()] = [float(x) for x in nums.split()]

for fname in ['clz2_out.txt', 'clz3_out.txt']:
    d = parse_file(fname)
    all_zeros.update(d)

print("Loaded zeros:")
for k, v in sorted(all_zeros.items()):
    print("  %s: %d zeros, range [%.1f, %.1f]" % (k, len(v), v[0], v[-1]))
print()

# ============================================
# STRIKE 1: SFF within each L-function
# K(tau) = |sum_j exp(2*pi*i * gamma_j * tau)|^2 / N
# For GUE: K(tau) ~ tau for tau < 1, ~ 1 for tau > 1
# (in unfolded units where mean spacing = 1)
# ============================================
print("=== STRIKE 1: Self-SFF of each L-function ===")
print()

def sff(zeros, tau_values):
    """Spectral Form Factor"""
    N = len(zeros)
    result = []
    for tau in tau_values:
        sr = si = 0.0
        for g in zeros:
            phase = 2 * math.pi * g * tau
            sr += math.cos(phase)
            si += math.sin(phase)
        K = (sr*sr + si*si) / N
        result.append(K)
    return result

# Unfold: for zeta zeros, mean spacing at height T ~ 2*pi/ln(T/(2*pi))
# For L(s,chi) mod q, mean spacing ~ 2*pi/ln(qT/(2*pi))
# Simple approach: use the actual spacings to estimate mean spacing

def mean_spacing(zeros):
    spacings = [zeros[i+1]-zeros[i] for i in range(len(zeros)-1)]
    return sum(spacings)/len(spacings)

# tau values in units of 1/mean_spacing
tau_raw = [0.001 * i for i in range(1, 200)]

for label in sorted(all_zeros.keys()):
    zeros = all_zeros[label]
    if len(zeros) < 10: continue
    ms = mean_spacing(zeros)
    # Compute SFF at a few key tau values
    taus = [0.5/ms, 1.0/ms, 2.0/ms, 5.0/ms]
    K_vals = sff(zeros, taus)
    tau_unfolded = [0.5, 1.0, 2.0, 5.0]
    print("  %s (%d zeros, mean_sp=%.3f):" % (label, len(zeros), ms))
    for t, k in zip(tau_unfolded, K_vals):
        gue = min(t, 1.0) * len(zeros)  # GUE prediction (unnormalized)
        print("    tau=%.1f: K=%.2f (GUE~%.1f)" % (t, k, min(t, 1.0)))
    print()

# ============================================
# STRIKE 2: Cross-SFF between pairs
# K_cross(tau) = sum_i exp(2*pi*i*g_i^(1)*tau) * conj(sum_j exp(2*pi*i*g_j^(2)*tau)) / sqrt(N1*N2)
# If uncorrelated: K_cross ~ 0 (random phases cancel)
# If correlated: K_cross > 0
# ============================================
print("=== STRIKE 2: Cross-SFF between L-functions ===")
print()

def cross_sff(zeros1, zeros2, tau_values):
    """Cross spectral form factor"""
    N = math.sqrt(len(zeros1) * len(zeros2))
    result = []
    for tau in tau_values:
        r1 = i1 = r2 = i2 = 0.0
        for g in zeros1:
            phase = 2 * math.pi * g * tau
            r1 += math.cos(phase); i1 += math.sin(phase)
        for g in zeros2:
            phase = 2 * math.pi * g * tau
            r2 += math.cos(phase); i2 += math.sin(phase)
        # cross = A1 * conj(A2) = (r1+i*i1)(r2-i*i2) = (r1*r2+i1*i2) + i(i1*r2-r1*i2)
        cross_re = r1*r2 + i1*i2
        cross_im = i1*r2 - r1*i2
        cross_abs = math.sqrt(cross_re**2 + cross_im**2) / N
        result.append((cross_abs, cross_re/N, cross_im/N))
    return result

# Compare self vs cross for q=5
labels_q5 = [k for k in sorted(all_zeros.keys()) if k.startswith('Q5')]
print("Q5 characters:", labels_q5)
print()

# Use a range of tau values
tau_test = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5]

print("Self-SFF (diagonal):")
for label in labels_q5:
    z = all_zeros[label]
    if len(z) < 5: continue
    vals = sff(z, tau_test)
    print("  %s: " % label + " ".join("%.2f" % v for v in vals))

print()
print("Cross-SFF (off-diagonal):")
for i, l1 in enumerate(labels_q5):
    for j, l2 in enumerate(labels_q5):
        if j <= i: continue
        z1, z2 = all_zeros[l1], all_zeros[l2]
        if len(z1) < 5 or len(z2) < 5: continue
        vals = cross_sff(z1, z2, tau_test)
        abs_vals = [v[0] for v in vals]
        print("  %s x %s: " % (l1, l2) + " ".join("%.2f" % v for v in abs_vals))

print()
print("If cross ~ self: zeros are correlated.")
print("If cross << self: zeros are independent (expected).")
