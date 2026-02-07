#!/usr/bin/env python3
"""SPARK Cross-L: Strikes 11-14

The connected SFF is noisy and DC-contaminated.
Need to: (1) unfold properly, (2) strip smooth part, (3) check what's real.

Strike 11: Proper unfolding using Weyl law
Strike 12: Number variance — the cleanest cross-statistic
Strike 13: Level spacing ratio for mixed zeros
Strike 14: The repulsion test — do close zeros from different L avoid each other?
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

all_zeros = {}
for fname in ['clz5_all.txt', 'clz3_out.txt']:
    all_zeros.update(parse_file(fname))
z3_raw = """Q3_0: 14.13472514 21.02203964 25.01085758 30.42487613 32.93506159 37.58617816 40.91871901 43.32707328 48.00515088 49.77383248 52.97032148 56.44624770 59.34704400 60.83177852 65.11254405 67.07981053 69.54640171 72.06715767 75.70469070 77.14484007 79.33737502
Q3_1: 8.03973716 11.24920621 15.70461918 18.26199750 20.45577081 24.05941486 26.57786874 28.21816451 30.74504026 33.89738893 35.60841265 37.55179656 39.48520726 42.61637923 44.12057291 46.27411802 47.51410451 50.37513865 52.49674960 54.19384310 55.64255870 57.58405636 60.02685746 62.20607812 63.17699277 65.29492554 66.62313463 69.51302299 70.81979870 72.65614907 74.00542852 75.62240696 78.21748127 79.63797575"""
for line in z3_raw.strip().split('\n'):
    label, nums = line.split(':', 1)
    all_zeros[label.strip()] = [float(x) for x in nums.split()]

# ============================================
# STRIKE 11: Proper unfolding
# For L(s,chi) mod q: N(T) ~ T/(2*pi) * log(qT/(2*pi*e))
# The unfolded zeros are: theta_j = N(gamma_j) (staircase function)
# In unfolded coords, mean spacing = 1.
# ============================================

def weyl_count(T, q):
    """Approximate N(T) for L(s,chi) mod q"""
    if T <= 0: return 0
    return T / (2 * math.pi) * math.log(q * T / (2 * math.pi * math.e))

def unfold(zeros, q):
    """Unfold zeros using Weyl law"""
    return [weyl_count(g, q) for g in zeros]

# ============================================
# STRIKE 12: r-statistic (spacing ratio)
# r_n = min(s_n, s_{n+1}) / max(s_n, s_{n+1})
# GUE: <r> ≈ 0.5307 (Wigner-Dyson)
# Poisson: <r> = 2*ln(2) - 1 ≈ 0.386
# ============================================
print("=== STRIKE 12: Spacing ratio statistic ===")
print("GUE: <r> = 0.5307,  Poisson: <r> = 0.386")
print()

def spacing_ratios(zeros):
    """Compute r = min(s_n, s_{n+1}) / max(s_n, s_{n+1})"""
    spacings = [zeros[i+1] - zeros[i] for i in range(len(zeros)-1)]
    ratios = []
    for i in range(len(spacings)-1):
        s1, s2 = spacings[i], spacings[i+1]
        if max(s1,s2) > 0:
            ratios.append(min(s1,s2) / max(s1,s2))
    return ratios

# For each L-function individually (should be GUE)
print("Individual L-functions (should be GUE ≈ 0.531):")
for k in sorted(all_zeros):
    if not k.startswith('Q5'): continue
    z = sorted(all_zeros[k])
    if len(z) < 10: continue
    # Unfold
    zz = unfold(z, 5)
    r = spacing_ratios(zz)
    if r:
        print("  %s: <r> = %.4f (%d ratios)" % (k, sum(r)/len(r), len(r)))

# For mixed zeros (all Q5 chars)
print()
print("Mixed zeros (all Q5 characters):")
all_q5 = sorted(sum([v for k,v in all_zeros.items() if k.startswith('Q5')], []))
# Unfold with q=5
zz_mixed = unfold(all_q5, 5)  # NOTE: this uses single-L unfolding, wrong for mixed
r_mixed = spacing_ratios(sorted(all_q5))  # use raw (not unfolded) — ratios are scale-free
print("  <r> = %.4f (%d ratios)" % (sum(r_mixed)/len(r_mixed), len(r_mixed)))
print()
print("  If <r> ~ 0.531: mixed zeros have GUE repulsion (zeros repel across L-functions)")
print("  If <r> ~ 0.386: mixed zeros are Poisson (no cross-repulsion)")
print("  If between: partial cross-correlation")
print()

# ============================================
# STRIKE 13: Same analysis for q=3 and q=7
# ============================================
print("=== STRIKE 13: Spacing ratios across moduli ===")
print()

for q, prefix in [(3, 'Q3'), (5, 'Q5'), (7, 'Q7')]:
    # Individual
    indiv_rs = []
    chars = {k: sorted(v) for k, v in all_zeros.items() if k.startswith(prefix) and len(v) >= 10}
    for k, z in sorted(chars.items()):
        r = spacing_ratios(z)
        if r:
            indiv_rs.extend(r)
    indiv_mean = sum(indiv_rs)/len(indiv_rs) if indiv_rs else 0

    # Mixed
    all_mix = sorted(sum(chars.values(), []))
    r_mix = spacing_ratios(all_mix)
    mix_mean = sum(r_mix)/len(r_mix) if r_mix else 0

    n_chars = len(chars)
    n_zeros = len(all_mix)
    print("q=%d: %d chars, %d mixed zeros" % (q, n_chars, n_zeros))
    print("  Individual <r>: %.4f (expect GUE 0.531)" % indiv_mean)
    print("  Mixed <r>:      %.4f" % mix_mean)
    print("  Poisson:        0.386")
    print()

# ============================================
# STRIKE 14: Direct repulsion test
# For each zero, find the nearest zero from a DIFFERENT L-function.
# Compare the distribution of these distances to:
# (a) Poisson: P(s) = rho * exp(-rho * s) where rho = (phi(q)-1) * local_density
# (b) GUE: suppressed at s=0
# ============================================
print("=== STRIKE 14: Cross nearest-neighbor distribution ===")
print()

for q, prefix in [(3, 'Q3'), (5, 'Q5')]:
    chars = {k: sorted(v) for k, v in all_zeros.items() if k.startswith(prefix) and len(v) >= 8}
    if len(chars) < 2: continue

    # For each zero, find nearest from OTHER L-function
    cross_nn = []
    for k1, z1 in chars.items():
        other_zeros = sorted(sum([v for k2,v in chars.items() if k2 != k1], []))
        for g in z1:
            if other_zeros:
                nearest = min(abs(g - g2) for g2 in other_zeros)
                cross_nn.append(nearest)

    # Self nearest-neighbor
    self_nn = []
    for k1, z1 in chars.items():
        for i in range(len(z1)):
            dists = []
            if i > 0: dists.append(z1[i] - z1[i-1])
            if i < len(z1)-1: dists.append(z1[i+1] - z1[i])
            if dists:
                self_nn.append(min(dists))

    # Normalize by mean spacing
    all_mix = sorted(sum(chars.values(), []))
    mix_ms = (all_mix[-1] - all_mix[0]) / (len(all_mix) - 1)

    cross_norm = [s / mix_ms for s in cross_nn]
    self_norm = [s / mix_ms for s in self_nn]

    # Compute mean self spacing per individual L-function
    indiv_ms_list = []
    for k, z in chars.items():
        if len(z) > 1:
            ms = (z[-1]-z[0])/(len(z)-1)
            indiv_ms_list.append(ms)
    indiv_ms = sum(indiv_ms_list)/len(indiv_ms_list)
    self_norm_proper = [s / indiv_ms for s in self_nn]

    print("q=%d (%d characters):" % (q, len(chars)))
    print("  Self nearest-neighbor (normalized by own L mean spacing):")
    print("    mean = %.3f, frac < 0.3 = %.3f" % (
        sum(self_norm_proper)/len(self_norm_proper),
        sum(1 for s in self_norm_proper if s < 0.3)/len(self_norm_proper)))

    print("  Cross nearest-neighbor (normalized by mixed mean spacing):")
    print("    mean = %.3f, frac < 0.3 = %.3f" % (
        sum(cross_norm)/len(cross_norm),
        sum(1 for s in cross_norm if s < 0.3)/len(cross_norm)))

    # Histogram
    bins = [0]*8
    bw = 0.5
    for s in cross_norm:
        b = min(int(s/bw), 7)
        bins[b] += 1
    total = len(cross_norm)
    print("  Cross NN distribution:")
    for b in range(8):
        s = (b + 0.5) * bw
        frac = bins[b]/total
        # Expected Poisson: exp(-s) * bw (approx)
        poisson = math.exp(-s) * bw * (len(chars)-1) / len(chars)  # rough
        bar = "#" * int(frac * 40)
        print("    [%.1f-%.1f]: %.3f %s" % (b*bw, (b+1)*bw, frac, bar))
    print()
