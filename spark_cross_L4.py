#!/usr/bin/env python3
"""SPARK Cross-L: Strikes 7-10

The key question: when we mix zeros of DIFFERENT L-functions,
do they repel (GUE) or ignore each other (Poisson)?

The expected answer (from random matrix theory):
- Within one L-function: GUE repulsion (proven for low-order stats)
- Between different primitive L-functions: Poisson (independent)
- BUT: between L(s,chi) and L(s,bar(chi)): SAME zeros (for complex chi)

When we MIX all phi(q) sets of zeros for characters mod q:
the mean spacing shrinks by factor phi(q), and the repulsion
pattern should be: GUE for within, Poisson for between.
This gives a MIXED distribution.

Strike 7: Properly normalize cross-statistics
Strike 8: The "superposition" SFF
Strike 9: Connected cross-SFF (the real test)
Strike 10: Compare q=3, q=5, q=7
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

# Q7 data
all_zeros.update(parse_file('clz3_out.txt'))

# ============================================
# STRIKE 7: Check which characters are conjugate
# For q=5: generator g=2, order 4.
# Character [a] means chi(2) = e^{2pi*i*a/4}
# [0]: trivial, [1]: chi(2)=i, [2]: chi(2)=-1 (Legendre), [3]: chi(2)=-i
# [1] and [3] are conjugate (chi and bar(chi)).
# L(s, chi) and L(s, bar(chi)) have the same nontrivial zeros
# (since L(s,bar(chi)) = conj(L(conj(s),chi)) and zeros are on Re(s)=1/2)
# ============================================
print("=== STRIKE 7: Character conjugacy check ===")
print()

# For complex characters: zeros should be identical
z1 = all_zeros.get('Q5_1', [])
z3 = all_zeros.get('Q5_3', [])
if z1 and z3:
    # Sort both
    z1s, z3s = sorted(z1), sorted(z3)
    # Match nearest
    diffs = []
    for g in z1s[:20]:
        nearest = min(z3s, key=lambda x: abs(x-g))
        diffs.append(abs(g - nearest))
    print("Q5_1 vs Q5_3 (should be conjugate):")
    print("  First 20 nearest-match diffs:", ["%.4f"%d for d in diffs[:10]])
    print("  Max diff: %.6f" % max(diffs))
    if max(diffs) > 0.1:
        print("  NOT conjugate! PARI labels characters differently.")
        # Let me check: which pairs of Q5 chars have matching zeros?
        for l1 in ['Q5_0','Q5_1','Q5_2','Q5_3']:
            for l2 in ['Q5_0','Q5_1','Q5_2','Q5_3']:
                if l2 <= l1: continue
                z_a = sorted(all_zeros.get(l1, []))
                z_b = sorted(all_zeros.get(l2, []))
                if not z_a or not z_b: continue
                max_d = 0
                for g in z_a[:min(10,len(z_a))]:
                    nearest = min(z_b, key=lambda x: abs(x-g))
                    max_d = max(max_d, abs(g-nearest))
                print("  %s vs %s: max nearest diff = %.4f %s" % (
                    l1, l2, max_d, "SAME?" if max_d < 0.01 else ""))
    print()

# ============================================
# STRIKE 8: Superposition SFF
# Mix all zeros from all non-conjugate characters of same q.
# The SFF of the mixed set tells us about cross-correlations.
# ============================================
print("=== STRIKE 8: Superposition SFF ===")
print("Mix zeros of independent L-functions, measure SFF")
print()

def sff_values(zeros, taus):
    N = len(zeros)
    result = []
    for tau in taus:
        sr = si = 0.0
        for g in zeros:
            phase = 2 * math.pi * g * tau
            sr += math.cos(phase); si += math.sin(phase)
        K = (sr*sr + si*si) / N
        result.append(K)
    return result

# For q=5: independent characters are Q5_0, Q5_1, Q5_2, Q5_3
# (since Q5_1 and Q5_3 are NOT identical, they're all independent)
T_max = 50.0
indep_q5 = {}
for k in ['Q5_0', 'Q5_1', 'Q5_2', 'Q5_3']:
    indep_q5[k] = [g for g in all_zeros.get(k, []) if g <= T_max]

# Individual SFFs
taus = [0.01 * i for i in range(1, 51)]
for k in sorted(indep_q5):
    z = indep_q5[k]
    if len(z) < 5: continue
    vals = sff_values(z, taus)
    mean_sff = sum(vals) / len(vals)
    print("  %s: %d zeros, mean SFF = %.3f" % (k, len(z), mean_sff))

# Mixed
all_mixed = sorted(sum(indep_q5.values(), []))
mixed_vals = sff_values(all_mixed, taus)
mean_mixed = sum(mixed_vals) / len(mixed_vals)
print("  MIXED: %d zeros, mean SFF = %.3f" % (len(all_mixed), mean_mixed))
print()

# If independent: mixed SFF = sum of individual SFFs (since phases are random)
# K_mix(tau) = |sum_chi A_chi(tau)|^2 / N_total
# = sum_chi |A_chi|^2 / N_total + sum_{chi!=chi'} A_chi * conj(A_chi') / N_total
# The cross terms average to zero if independent.
# So K_mix ≈ sum of individual K_chi * (N_chi / N_total)

# ============================================
# STRIKE 9: Connected cross-SFF
# K_connected(tau) = K_mix(tau) - sum_chi (N_chi/N_total) * K_chi(tau)
# If zero: zeros are independent across L-functions.
# If positive: there's a cross-correlation.
# ============================================
print("=== STRIKE 9: Connected cross-SFF ===")
print("K_connected = K_mix - sum(weight * K_individual)")
print("Should be ~0 if zeros are independent.")
print()

N_total = len(all_mixed)
connected = []
for idx, tau in enumerate(taus):
    k_mix = mixed_vals[idx]
    k_sum = 0.0
    for k in indep_q5:
        z = indep_q5[k]
        if len(z) < 2: continue
        n_chi = len(z)
        k_ind = sff_values(z, [tau])[0]
        k_sum += (n_chi / N_total) * k_ind
    connected.append(k_mix - k_sum)

# Print connected SFF at selected tau values
print("%8s %8s %8s %8s" % ("tau", "K_mix", "K_ind", "K_conn"))
print("-" * 36)
for idx in range(0, len(taus), 5):
    tau = taus[idx]
    k_mix = mixed_vals[idx]
    k_ind_sum = k_mix - connected[idx]
    print("%8.3f %8.3f %8.3f %8.3f" % (tau, k_mix, k_ind_sum, connected[idx]))

print()
mean_conn = sum(connected) / len(connected)
std_conn = (sum((c-mean_conn)**2 for c in connected)/len(connected))**0.5
mean_ind = sum(mixed_vals[i] - connected[i] for i in range(len(taus))) / len(taus)
print("Mean connected SFF: %.4f" % mean_conn)
print("Std connected SFF:  %.4f" % std_conn)
print("Mean individual SFF: %.4f" % mean_ind)
print("Ratio connected/individual: %.4f" % (mean_conn/mean_ind if mean_ind else 0))
print()
print("If ratio << 1: zeros are approximately independent.")
print("If ratio ~ 1: zeros are strongly correlated across L-functions.")

# ============================================
# STRIKE 10: Compare across q values
# q=3 (2 chars), q=5 (4 chars), q=7 (6 chars)
# ============================================
print()
print("=== STRIKE 10: Cross-correlation strength vs modulus q ===")
print()

for q, prefix, T_cut in [(3, 'Q3', 70), (5, 'Q5', 50), (7, 'Q7', 40)]:
    chars = {k: [g for g in v if g <= T_cut] for k, v in all_zeros.items() if k.startswith(prefix)}
    chars = {k: v for k, v in chars.items() if len(v) >= 5}

    if len(chars) < 2:
        print("q=%d: not enough data" % q)
        continue

    all_mix = sorted(sum(chars.values(), []))
    N_tot = len(all_mix)
    if N_tot < 10: continue

    # Compute connected SFF
    test_taus = [0.01 * i for i in range(1, 31)]
    mix_sff = sff_values(all_mix, test_taus)
    conn = []
    for idx, tau in enumerate(test_taus):
        k_sum = 0
        for k, z in chars.items():
            k_sum += (len(z)/N_tot) * sff_values(z, [tau])[0]
        conn.append(mix_sff[idx] - k_sum)

    mean_c = sum(conn) / len(conn)
    mean_i = sum(mix_sff[i] - conn[i] for i in range(len(conn))) / len(conn)
    ratio = mean_c / mean_i if mean_i else 0

    print("q=%d: %d chars, %d total zeros, connected/individual = %.4f" % (
        q, len(chars), N_tot, ratio))
