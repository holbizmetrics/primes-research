#!/usr/bin/env python3
"""SPARK Cross-L SFF: Strikes 3-7

Strike 3: Connected cross-SFF (subtract smooth part)
Strike 4: Pair correlation between zeros of DIFFERENT L-functions
Strike 5: Nearest-neighbor spacing: inter vs intra L-function
Strike 6: GUE vs Poisson for cross-statistics
Strike 7: Does chi_1 * bar(chi_2) matter?
"""
import math

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

# Load zeros
all_zeros = {}
for fname in ['clz5_all.txt', 'clz3_out.txt']:
    all_zeros.update(parse_file(fname))

# Also parse Q3 from inline data
z3_raw = """Q3_0: 14.13472514 21.02203964 25.01085758 30.42487613 32.93506159 37.58617816 40.91871901 43.32707328 48.00515088 49.77383248 52.97032148 56.44624770 59.34704400 60.83177852 65.11254405 67.07981053 69.54640171 72.06715767 75.70469070 77.14484007 79.33737502
Q3_1: 8.03973716 11.24920621 15.70461918 18.26199750 20.45577081 24.05941486 26.57786874 28.21816451 30.74504026 33.89738893 35.60841265 37.55179656 39.48520726 42.61637923 44.12057291 46.27411802 47.51410451 50.37513865 52.49674960 54.19384310 55.64255870 57.58405636 60.02685746 62.20607812 63.17699277 65.29492554 66.62313463 69.51302299 70.81979870 72.65614907 74.00542852 75.62240696 78.21748127 79.63797575"""
for line in z3_raw.strip().split('\n'):
    label, nums = line.split(':', 1)
    all_zeros[label.strip()] = [float(x) for x in nums.split()]

print("Loaded:")
for k in sorted(all_zeros):
    print("  %s: %d zeros" % (k, len(all_zeros[k])))
print()

# Focus on Q5 characters (best data)
q5 = {k: v for k, v in all_zeros.items() if k.startswith('Q5')}

# ============================================
# STRIKE 3: Pair correlation R2(s) between zeros
# For a SINGLE L-function: R2(s) = 1 - (sin(pi*s)/(pi*s))^2  (GUE)
# For DIFFERENT L-functions: R2(s) = 1  (Poisson, if independent)
# We measure: for pairs (g_i^(1), g_j^(2)), what's the distribution of |g_i - g_j|?
# ============================================
print("=== STRIKE 3: Pair correlation — same vs different L-function ===")
print()

def pair_correlation(zeros, bins, max_s):
    """Pair correlation histogram in unfolded units"""
    N = len(zeros)
    # Simple unfolding: normalize spacings by mean spacing
    ms = (zeros[-1] - zeros[0]) / (N - 1)
    counts = [0] * bins
    bin_width = max_s / bins
    npairs = 0
    for i in range(N):
        for j in range(i+1, N):
            s = abs(zeros[i] - zeros[j]) / ms
            if s < max_s:
                b = int(s / bin_width)
                if b < bins:
                    counts[b] += 1
                    npairs += 1
    # Normalize: density should be 1 for Poisson
    norm = npairs * bin_width if npairs > 0 else 1
    return [c / (norm / bins) for c in counts], bin_width

def cross_pair_correlation(z1, z2, bins, max_s):
    """Pair correlation between zeros of DIFFERENT L-functions"""
    # Use combined mean spacing
    ms1 = (z1[-1] - z1[0]) / (len(z1) - 1) if len(z1) > 1 else 1
    ms2 = (z2[-1] - z2[0]) / (len(z2) - 1) if len(z2) > 1 else 1
    ms = (ms1 + ms2) / 2
    counts = [0] * bins
    bin_width = max_s / bins
    npairs = 0
    for g1 in z1:
        for g2 in z2:
            s = abs(g1 - g2) / ms
            if s < max_s:
                b = int(s / bin_width)
                if b < bins:
                    counts[b] += 1
                    npairs += 1
    norm = npairs * bin_width if npairs > 0 else 1
    return [c / (norm / bins) for c in counts], bin_width

BINS = 20; MAX_S = 4.0

# Self pair correlation for Q5_1
z1 = q5['Q5_1']
self_pc, bw = pair_correlation(z1, BINS, MAX_S)

# Cross pair correlation: Q5_1 x Q5_2
z2 = q5['Q5_2']
cross_pc, _ = cross_pair_correlation(z1, z2, BINS, MAX_S)

# Cross: Q5_1 x Q5_3
z3 = q5['Q5_3']
cross_pc2, _ = cross_pair_correlation(z1, z3, BINS, MAX_S)

# GUE prediction: 1 - (sin(pi*s)/(pi*s))^2
def gue_r2(s):
    if s < 0.001: return 0
    return 1 - (math.sin(math.pi * s) / (math.pi * s))**2

print("Pair correlation R2(s):")
print("%6s %7s %7s %7s %7s" % ("s", "GUE", "self", "cross12", "cross13"))
print("-" * 42)
for b in range(BINS):
    s = (b + 0.5) * bw
    gue = gue_r2(s)
    print("%6.2f %7.3f %7.3f %7.3f %7.3f" % (s, gue, self_pc[b], cross_pc[b], cross_pc2[b]))

print()
print("GUE: vanishes at s=0 (level repulsion)")
print("Poisson: flat at 1.0 (no correlations)")
print("If cross ~ 1 near s=0: different L-functions DON'T repel")
print("If cross ~ 0 near s=0: different L-functions DO repel")
print()

# ============================================
# STRIKE 4: Nearest-neighbor spacing distribution
# ============================================
print("=== STRIKE 4: Nearest-neighbor spacing ===")
print()

def nn_spacings(zeros):
    """Nearest-neighbor spacings, normalized by mean"""
    spacings = [zeros[i+1]-zeros[i] for i in range(len(zeros)-1)]
    ms = sum(spacings)/len(spacings)
    return [s/ms for s in spacings]

def cross_nn_spacings(z1, z2):
    """For each zero in z1, find nearest zero in z2"""
    spacings = []
    ms1 = (z1[-1]-z1[0])/(len(z1)-1) if len(z1)>1 else 1
    ms2 = (z2[-1]-z2[0])/(len(z2)-1) if len(z2)>1 else 1
    ms = (ms1+ms2)/2
    for g1 in z1:
        nearest = min(abs(g1 - g2) for g2 in z2)
        spacings.append(nearest / ms)
    return spacings

# Self spacings
self_sp = nn_spacings(z1)
cross_sp12 = cross_nn_spacings(z1, z2)
cross_sp13 = cross_nn_spacings(z1, z3)

# Also: ALL zeros mixed together
all_q5_zeros = sorted(z1 + z2 + z3 + q5.get('Q5_0', []))
mixed_sp = nn_spacings(all_q5_zeros)

print("Mean spacing (should be ~1 if normalized):")
print("  self (Q5_1):     %.3f" % (sum(self_sp)/len(self_sp)))
print("  cross Q5_1xQ5_2: %.3f" % (sum(cross_sp12)/len(cross_sp12)))
print("  cross Q5_1xQ5_3: %.3f" % (sum(cross_sp13)/len(cross_sp13)))
print()

# Small spacing fraction
print("Fraction of spacings < 0.3 (measures repulsion):")
f_self = sum(1 for s in self_sp if s < 0.3) / len(self_sp)
f_cross12 = sum(1 for s in cross_sp12 if s < 0.3) / len(cross_sp12)
f_cross13 = sum(1 for s in cross_sp13 if s < 0.3) / len(cross_sp13)
f_mixed = sum(1 for s in mixed_sp if s < 0.3) / len(mixed_sp)

# GUE: P(s<0.3) ~ very small (level repulsion)
# Poisson: P(s<0.3) = 1 - exp(-0.3) ~ 0.26
print("  self:        %.3f" % f_self)
print("  cross 1x2:   %.3f" % f_cross12)
print("  cross 1x3:   %.3f" % f_cross13)
print("  all mixed:   %.3f" % f_mixed)
print("  GUE expect:  ~0.01")
print("  Poisson exp: ~0.26")
print()

# ============================================
# STRIKE 5: Do zeros of chi and chi_bar repel differently
# than zeros of unrelated characters?
# For q=5: chi_1 has order 4, chi_3 = bar(chi_1) (conjugate)
# chi_2 has order 2 (real character, Legendre symbol)
# So: Q5_1 and Q5_3 are conjugate, Q5_2 is self-conjugate
# ============================================
print("=== STRIKE 5: Conjugate vs non-conjugate characters ===")
print("Q5_1 (order 4) and Q5_3 = bar(Q5_1) are conjugate")
print("Q5_2 (order 2) is real (self-conjugate)")
print()

# Known: L(s, chi) and L(s, bar(chi)) have the SAME zeros (complex conjugate)
# if chi is complex. So Q5_1 and Q5_3 should have IDENTICAL zeros!
print("Checking: are Q5_1 and Q5_3 zeros identical?")
z1_sorted = sorted(q5['Q5_1'])
z3_sorted = sorted(q5['Q5_3'])
min_len = min(len(z1_sorted), len(z3_sorted))
max_diff = max(abs(z1_sorted[i] - z3_sorted[i]) for i in range(min_len))
print("  Max |gamma_i^(1) - gamma_i^(3)|: %.10f" % max_diff)
print("  They are %s" % ("IDENTICAL!" if max_diff < 1e-6 else "DIFFERENT"))
print()

# So for complex characters: L(s,chi) and L(s,bar(chi)) share zeros.
# The interesting cross-correlation is between INDEPENDENT L-functions.
# For q=5: Q5_0 (zeta), Q5_1 (order 4), Q5_2 (order 2) are independent.
# Q5_3 = Q5_1.

# ============================================
# STRIKE 6: Proper cross-correlation of independent L-functions
# ============================================
print("=== STRIKE 6: Cross-correlation of INDEPENDENT L-functions ===")
print("Q5_0 (zeta) vs Q5_1 (order 4) vs Q5_2 (order 2)")
print()

# Restrict to common height range
T_max = 55.0  # all have zeros up to here
indep = {}
for k in ['Q5_0', 'Q5_1', 'Q5_2']:
    indep[k] = [g for g in q5[k] if g <= T_max]
    print("  %s: %d zeros up to T=%.0f" % (k, len(indep[k]), T_max))

print()

# Cross nearest-neighbor for each pair
pairs = [('Q5_0','Q5_1'), ('Q5_0','Q5_2'), ('Q5_1','Q5_2')]
for l1, l2 in pairs:
    sp = cross_nn_spacings(indep[l1], indep[l2])
    ms = sum(sp)/len(sp) if sp else 0
    f_small = sum(1 for s in sp if s < 0.3)/len(sp) if sp else 0
    min_s = min(sp) if sp else 0
    print("  %s x %s: mean_nn=%.3f  frac<0.3=%.3f  min_nn=%.3f" % (
        l1, l2, ms, f_small, min_s))

print()

# Same but for self
for k in indep:
    sp = nn_spacings(sorted(indep[k]))
    ms = sum(sp)/len(sp) if sp else 0
    f_small = sum(1 for s in sp if s < 0.3)/len(sp) if sp else 0
    min_s = min(sp) if sp else 0
    print("  %s self: mean_nn=%.3f  frac<0.3=%.3f  min_nn=%.3f" % (
        k, ms, f_small, min_s))

print()

# ALL independent zeros mixed
all_indep = sorted(sum(indep.values(), []))
sp_mixed = nn_spacings(all_indep)
ms_mixed = sum(sp_mixed)/len(sp_mixed)
f_small_mixed = sum(1 for s in sp_mixed if s < 0.3)/len(sp_mixed)
min_mixed = min(sp_mixed)
print("  ALL mixed: mean_nn=%.3f  frac<0.3=%.3f  min_nn=%.3f" % (
    ms_mixed, f_small_mixed, min_mixed))
print()

# GUE repulsion test for mixed zeros
# If zeros from different L-functions DON'T repel: mixed spacing should be
# Poisson-like (many small spacings, exponential distribution)
# If they DO repel: mixed spacing looks GUE-like (suppressed small spacings)
print("Spacing distribution of ALL mixed zeros:")
bins = [0] * 10
bw = 0.4
for s in sp_mixed:
    b = min(int(s / bw), 9)
    bins[b] += 1
total = len(sp_mixed)
for b in range(10):
    s = (b + 0.5) * bw
    frac = bins[b] / total
    # GUE: ~ pi/2 * s * exp(-pi/4 * s^2)  (Wigner surmise)
    gue_pred = math.pi/2 * s * math.exp(-math.pi/4 * s**2) * bw
    # Poisson: exp(-s) * bw
    poisson_pred = math.exp(-s) * bw
    bar = "#" * int(frac * 50)
    print("  [%.1f-%.1f]: %.3f  GUE=%.3f  Poisson=%.3f  %s" % (
        b*bw, (b+1)*bw, frac, gue_pred, poisson_pred, bar))
