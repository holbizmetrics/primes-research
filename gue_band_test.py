"""
Rigorous GUE vs Zeta Band-Covariance Test

Tests whether the band structure (B1↔B3 negative, B1↔B2 positive)
is a GUE property or zeta-specific.
"""
import math
import cmath
import random

# Zeta zeros (first 100 for clean comparison)
ZETA = [
    14.134725, 21.022039, 25.010857, 30.424876, 32.935061, 37.586178,
    40.918719, 43.327073, 48.005150, 49.773832, 52.970321, 56.446247,
    59.347044, 60.831778, 65.112544, 67.079810, 69.546401, 72.067157,
    75.704690, 77.144840, 79.337375, 82.910380, 84.735492, 87.425274,
    88.809111, 92.491899, 94.651344, 95.870634, 98.831194, 101.31785,
    103.72553, 105.44662, 107.16861, 111.02953, 111.87465, 114.32022,
    116.22668, 118.79078, 121.37012, 122.94682, 124.25681, 127.51668,
    129.57870, 131.08768, 133.49773, 134.75650, 138.11604, 139.73620,
    141.12370, 143.11184, 146.00098, 147.42276, 150.05352, 150.92525,
    153.02469, 156.11290, 157.59759, 158.84998, 161.18896, 163.03070,
    165.53706, 167.18443, 169.09451, 169.91197, 173.41153, 174.75419,
    176.44143, 178.37740, 179.91648, 182.20707, 184.87446, 185.59878,
    187.22892, 189.41615, 192.02665, 193.07972, 195.26539, 196.87648,
    198.01530, 201.26475, 202.49359, 204.18967, 205.39469, 207.90625,
    209.57650, 211.69086, 213.34791, 214.54704, 216.16953, 219.06759,
    220.71491, 221.43070, 224.00700, 224.98332, 227.42144, 229.33741,
    231.25018, 231.98723, 233.69340, 236.52422,
]

def sample_gue_spacing():
    """Sample from GUE spacing distribution using rejection sampling.
    GUE: p(s) = (32/π²) s² exp(-4s²/π)
    """
    while True:
        # Proposal: exponential with rate 0.8
        s = random.expovariate(0.8)
        # GUE density (unnormalized)
        p_gue = s * s * math.exp(-4 * s * s / math.pi)
        # Proposal density
        p_prop = 0.8 * math.exp(-0.8 * s)
        # Acceptance ratio (with safety factor)
        if random.random() < p_gue / (2.5 * p_prop):
            return s

def generate_gue_eigenvalues(n, start=14.0, mean_spacing=2.2):
    """Generate n eigenvalues with GUE spacing distribution."""
    eigs = [start]
    for _ in range(n - 1):
        spacing = sample_gue_spacing() * mean_spacing
        eigs.append(eigs[-1] + spacing)
    return eigs

def E_contribution(x, gamma):
    """Single zero's contribution to E(x)."""
    sqrt_x = math.sqrt(x)
    log_x = math.log(x)
    phase = cmath.exp(1j * gamma * log_x)
    denom = complex(0.5, gamma)
    return -2 * (sqrt_x * phase / denom).real

def E_with_phase(x, gamma, extra_phase):
    """Single zero's contribution with extra phase."""
    sqrt_x = math.sqrt(x)
    log_x = math.log(x)
    phase = cmath.exp(1j * (gamma * log_x + extra_phase))
    denom = complex(0.5, gamma)
    return -2 * (sqrt_x * phase / denom).real

def compute_covariance(zeros_i, zeros_j, N, samples=60):
    """Compute covariance between contributions from two sets of zeros."""
    xs = [10**(math.log10(2) + k * (math.log10(N) - math.log10(2)) / (samples-1))
          for k in range(samples)]

    # Contributions from each set
    E_i = [sum(E_contribution(x, g) for g in zeros_i) for x in xs]
    E_j = [sum(E_contribution(x, g) for g in zeros_j) for x in xs]

    # Means
    mean_i = sum(E_i) / len(E_i)
    mean_j = sum(E_j) / len(E_j)

    # Covariance
    cov = sum((E_i[k] - mean_i) * (E_j[k] - mean_j) for k in range(len(xs))) / len(xs)

    return cov

def compute_C(zeros, N, samples=80, trials=15):
    """Compute cancellation functional C(N)."""
    xs = [10**(math.log10(2) + k * (math.log10(N) - math.log10(2)) / (samples-1))
          for k in range(samples)]

    def E_actual(x):
        return sum(E_contribution(x, g) for g in zeros)

    def E_null(x, phases):
        return sum(E_with_phase(x, zeros[i], phases[i]) for i in range(len(zeros)))

    def var(vals):
        m = sum(vals) / len(vals)
        return sum((v - m)**2 for v in vals) / len(vals)

    # Actual variance
    E_vals = [E_actual(x) for x in xs]
    var_actual = var(E_vals)

    # Null variance (average over trials)
    null_vars = []
    for _ in range(trials):
        phases = [random.uniform(0, 2*math.pi) for _ in zeros]
        E_null_vals = [E_null(x, phases) for x in xs]
        null_vars.append(var(E_null_vals))
    var_null = sum(null_vars) / len(null_vars)

    return var_actual / var_null if var_null > 0 else 0

def analyze_band_structure(zeros, label, N=10000):
    """Analyze band structure for a set of zeros."""
    # Define bands based on the range
    min_g, max_g = min(zeros), max(zeros)
    range_g = max_g - min_g

    # Three equal bands
    cut1 = min_g + range_g / 3
    cut2 = min_g + 2 * range_g / 3

    B1 = [g for g in zeros if g < cut1]
    B2 = [g for g in zeros if cut1 <= g < cut2]
    B3 = [g for g in zeros if g >= cut2]

    print(f"\n{'='*60}")
    print(f"BAND ANALYSIS: {label}")
    print(f"{'='*60}")
    print(f"Total zeros: {len(zeros)}, range: [{min_g:.1f}, {max_g:.1f}]")
    print(f"B1: {len(B1)} zeros (γ < {cut1:.1f})")
    print(f"B2: {len(B2)} zeros ({cut1:.1f} ≤ γ < {cut2:.1f})")
    print(f"B3: {len(B3)} zeros (γ ≥ {cut2:.1f})")

    # Band-by-band C(N)
    print(f"\nBand-by-band C(N) at N={N}:")
    if len(B1) > 2:
        c1 = compute_C(B1, N)
        print(f"  C(B1) = {c1:.4f} {'[cancels]' if c1 < 1 else '[anti-cancels]'}")
    if len(B2) > 2:
        c2 = compute_C(B2, N)
        print(f"  C(B2) = {c2:.4f} {'[cancels]' if c2 < 1 else '[anti-cancels]'}")
    if len(B3) > 2:
        c3 = compute_C(B3, N)
        print(f"  C(B3) = {c3:.4f} {'[cancels]' if c3 < 1 else '[anti-cancels]'}")
    c_all = compute_C(zeros, N)
    print(f"  C(ALL) = {c_all:.4f}")

    # Cross-band covariances
    print(f"\nCross-band covariances:")
    if len(B1) > 1 and len(B2) > 1:
        cov_12 = compute_covariance(B1, B2, N)
        print(f"  Cov(B1,B2) = {cov_12:+.4f} {'[positive=bad]' if cov_12 > 0 else '[negative=good]'}")
    if len(B1) > 1 and len(B3) > 1:
        cov_13 = compute_covariance(B1, B3, N)
        print(f"  Cov(B1,B3) = {cov_13:+.4f} {'[positive=bad]' if cov_13 > 0 else '[negative=good]'}")
    if len(B2) > 1 and len(B3) > 1:
        cov_23 = compute_covariance(B2, B3, N)
        print(f"  Cov(B2,B3) = {cov_23:+.4f} {'[positive=bad]' if cov_23 > 0 else '[negative=good]'}")

    return {
        'C_B1': c1 if len(B1) > 2 else None,
        'C_B2': c2 if len(B2) > 2 else None,
        'C_B3': c3 if len(B3) > 2 else None,
        'C_all': c_all,
        'cov_12': cov_12 if len(B1) > 1 and len(B2) > 1 else None,
        'cov_13': cov_13 if len(B1) > 1 and len(B3) > 1 else None,
        'cov_23': cov_23 if len(B2) > 1 and len(B3) > 1 else None,
    }

def main():
    print("="*60)
    print("RIGOROUS GUE vs ZETA BAND-COVARIANCE TEST")
    print("="*60)

    # Analyze Zeta
    zeta_results = analyze_band_structure(ZETA, "ZETA ZEROS")

    # Generate and analyze multiple GUE samples
    print("\n" + "="*60)
    print("GUE ENSEMBLE (averaging over 5 realizations)")
    print("="*60)

    n_gue_trials = 5
    gue_results_list = []

    for trial in range(n_gue_trials):
        # Generate GUE with same size and density as zeta
        mean_spacing = (ZETA[-1] - ZETA[0]) / (len(ZETA) - 1)
        gue = generate_gue_eigenvalues(len(ZETA), start=ZETA[0], mean_spacing=mean_spacing)

        print(f"\nGUE Trial {trial+1}:")
        results = analyze_band_structure(gue, f"GUE #{trial+1}")
        gue_results_list.append(results)

    # Average GUE results
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)

    def avg(key):
        vals = [r[key] for r in gue_results_list if r[key] is not None]
        return sum(vals) / len(vals) if vals else None

    print(f"\n{'Metric':<20} {'ZETA':>12} {'GUE (avg)':>12} {'Difference':>12}")
    print("-" * 58)

    metrics = [
        ('C(B1)', 'C_B1'),
        ('C(B2)', 'C_B2'),
        ('C(B3)', 'C_B3'),
        ('C(ALL)', 'C_all'),
        ('Cov(B1,B2)', 'cov_12'),
        ('Cov(B1,B3)', 'cov_13'),
        ('Cov(B2,B3)', 'cov_23'),
    ]

    for label, key in metrics:
        zeta_val = zeta_results[key]
        gue_val = avg(key)
        if zeta_val is not None and gue_val is not None:
            diff = zeta_val - gue_val
            print(f"{label:<20} {zeta_val:>12.4f} {gue_val:>12.4f} {diff:>+12.4f}")

    # Key test: covariance sign pattern
    print("\n" + "="*60)
    print("KEY TEST: COVARIANCE SIGN PATTERN")
    print("="*60)

    zeta_pattern = f"B1↔B2: {'+' if zeta_results['cov_12'] > 0 else '-'}, B1↔B3: {'+' if zeta_results['cov_13'] > 0 else '-'}"
    print(f"ZETA pattern: {zeta_pattern}")

    gue_12_positive = sum(1 for r in gue_results_list if r['cov_12'] and r['cov_12'] > 0)
    gue_13_positive = sum(1 for r in gue_results_list if r['cov_13'] and r['cov_13'] > 0)

    print(f"GUE B1↔B2 positive: {gue_12_positive}/{n_gue_trials} trials")
    print(f"GUE B1↔B3 positive: {gue_13_positive}/{n_gue_trials} trials")

    # Verdict
    print("\n" + "="*60)
    print("VERDICT")
    print("="*60)

    zeta_has_pattern = zeta_results['cov_12'] > 0 and zeta_results['cov_13'] < 0
    gue_has_pattern = (gue_12_positive >= n_gue_trials/2) and (gue_13_positive < n_gue_trials/2)

    if zeta_has_pattern and not gue_has_pattern:
        print("✓ ZETA has B1↔B2 positive, B1↔B3 negative")
        print("✗ GUE does NOT consistently show this pattern")
        print("→ BAND STRUCTURE IS ZETA-SPECIFIC, NOT GUE-UNIVERSAL")
        print("→ This is a NEW OBSTRUCTION beyond pair correlation!")
    elif zeta_has_pattern and gue_has_pattern:
        print("✓ Both ZETA and GUE show the same pattern")
        print("→ Band structure is GUE-universal")
        print("→ Still useful as a constraint, but not zeta-specific")
    else:
        print("Pattern unclear - need more data")

if __name__ == "__main__":
    main()
