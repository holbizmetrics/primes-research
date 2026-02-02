"""
ML Classification of L-function zeros (no numpy)
"""

import subprocess
import math

def get_zeros_gp(cmd):
    """Run GP command and parse zeros"""
    result = subprocess.run(['gp', '-q', '-f'], input=cmd.encode(),
                          capture_output=True, timeout=120)
    output = result.stdout.decode().strip()
    if not output:
        return []
    # Parse GP vector output
    output = output.replace('[','').replace(']','').replace('\n',' ')
    zeros = []
    for x in output.split(','):
        x = x.strip()
        if x:
            try:
                zeros.append(float(x))
            except:
                pass
    return sorted(zeros)

def mean(lst):
    return sum(lst) / len(lst) if lst else 0

def variance(lst):
    if len(lst) < 2:
        return 0
    m = mean(lst)
    return sum((x - m)**2 for x in lst) / len(lst)

def compute_features(zeros):
    """Extract statistical features from zero sequence"""
    if len(zeros) < 10:
        return None

    # Spacings
    spacings = [zeros[i+1] - zeros[i] for i in range(len(zeros)-1)]
    mean_s = mean(spacings)
    norm_spacings = [s / mean_s for s in spacings]

    # Variance
    var_s = variance(norm_spacings)

    # Skewness and kurtosis (simplified)
    std_s = math.sqrt(var_s) if var_s > 0 else 1
    skew = mean([(s - 1)**3 for s in norm_spacings]) / std_s**3 if std_s > 0 else 0
    kurt = mean([(s - 1)**4 for s in norm_spacings]) / std_s**4 if std_s > 0 else 0

    features = {
        'n_zeros': len(zeros),
        'variance': var_s,
        'skewness': skew,
        'kurtosis': kurt,
        'min_norm': min(norm_spacings),
        'max_norm': max(norm_spacings),
        'first_zero': zeros[0],
    }
    return features

# Get zeros
print("Fetching zeros...")

zeta_cmd = "z=lfunzeros(1,[0.1,300]);for(i=1,#z,print1(z[i],\",\"));"
print("  zeta...", end=" ", flush=True)
zeta_zeros = get_zeros_gp(zeta_cmd)
print(f"{len(zeta_zeros)} zeros")

chi7_cmd = "G=znstar(7,1);c=znconreychar(G,6);L=lfuncreate([G,c]);z=lfunzeros(L,[0.1,300]);for(i=1,#z,print1(z[i],\",\"));"
print("  chi7...", end=" ", flush=True)
chi7_zeros = get_zeros_gp(chi7_cmd)
print(f"{len(chi7_zeros)} zeros")

chi3_cmd = "G=znstar(3,1);c=znconreychar(G,2);L=lfuncreate([G,c]);z=lfunzeros(L,[0.1,300]);for(i=1,#z,print1(z[i],\",\"));"
print("  chi3...", end=" ", flush=True)
chi3_zeros = get_zeros_gp(chi3_cmd)
print(f"{len(chi3_zeros)} zeros")

print("\n=== FEATURE COMPARISON ===")
print(f"{'Feature':<12} {'zeta':>10} {'chi7':>10} {'chi3':>10}")
print("-" * 44)

fz = compute_features(zeta_zeros)
f7 = compute_features(chi7_zeros)
f3 = compute_features(chi3_zeros)

for key in ['n_zeros', 'variance', 'skewness', 'kurtosis', 'min_norm', 'max_norm', 'first_zero']:
    print(f"{key:<12} {fz[key]:>10.4f} {f7[key]:>10.4f} {f3[key]:>10.4f}")

print("\n=== CLASSIFICATION POTENTIAL ===")
# Check which features separate well
print("Features that distinguish zeta from Dirichlet:")
for key in ['variance', 'skewness', 'kurtosis']:
    zeta_val = fz[key]
    dirichlet_avg = (f7[key] + f3[key]) / 2
    gap = abs(zeta_val - dirichlet_avg)
    print(f"  {key}: zeta={zeta_val:.4f}, Dirichlet_avg={dirichlet_avg:.4f}, gap={gap:.4f}")
