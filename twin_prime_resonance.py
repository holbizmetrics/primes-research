#!/usr/bin/env python3
"""
Twin Prime Resonance Analysis
Do twin primes have their own Brennpunkt and resonance wavelength?
"""

import math

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi / (PHI * PHI)

def sieve_primes(n):
    """Simple sieve of Eratosthenes"""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

def get_twin_primes(primes):
    """Extract twin prime pairs (both members)"""
    prime_set = set(primes)
    twins = []
    for p in primes:
        if p + 2 in prime_set:
            twins.append(p)
            twins.append(p + 2)
    return sorted(set(twins))  # Remove duplicates, sort

def get_isolated_primes(primes):
    """Primes that are NOT part of any twin pair"""
    prime_set = set(primes)
    isolated = []
    for p in primes:
        if (p - 2) not in prime_set and (p + 2) not in prime_set:
            isolated.append(p)
    return isolated

def golden_sphere_position(n, N):
    """Map integer to golden spiral sphere"""
    theta = GOLDEN_ANGLE * n
    z = 1 - (2 * n) / N
    z = max(-1, min(1, z))
    r_xy = math.sqrt(max(0, 1 - z*z))
    x = r_xy * math.cos(theta)
    y = r_xy * math.sin(theta)
    return (x, y, z)

def apply_brennpunkt(pos, t, R=0.5):
    """Apply partial geometric inversion"""
    x, y, z = pos
    r_orig = math.sqrt(x*x + y*y + z*z)
    if r_orig < 1e-10:
        return pos
    r_focused = (r_orig ** (1 - 2*t)) * (R ** (2*t))
    scale = r_focused / r_orig
    return (x * scale, y * scale, z * scale)

def measure_clustering(positions):
    """Measure how clustered positions are (lower = more clustered)"""
    if len(positions) < 2:
        return float('inf')

    # Compute centroid
    cx = sum(p[0] for p in positions) / len(positions)
    cy = sum(p[1] for p in positions) / len(positions)
    cz = sum(p[2] for p in positions) / len(positions)

    # Mean squared distance from centroid
    msd = sum((p[0]-cx)**2 + (p[1]-cy)**2 + (p[2]-cz)**2 for p in positions) / len(positions)
    return msd

def find_brennpunkt(numbers, N, t_range=(0.0, 0.5), steps=100):
    """Find optimal t for minimum clustering"""
    positions_orig = [golden_sphere_position(n, N) for n in numbers if n <= N]

    best_t = 0
    best_clustering = float('inf')

    for i in range(steps + 1):
        t = t_range[0] + (t_range[1] - t_range[0]) * i / steps
        positions_focused = [apply_brennpunkt(p, t) for p in positions_orig]
        clustering = measure_clustering(positions_focused)
        if clustering < best_clustering:
            best_clustering = clustering
            best_t = t

    return best_t, best_clustering

def wave_scatter(numbers, N, wavelength, t_brennpunkt):
    """Compute backscatter amplitude at given wavelength"""
    k = 2 * math.pi / wavelength
    amp_real, amp_imag = 0, 0

    for n in numbers:
        if n > N:
            continue
        pos = golden_sphere_position(n, N)
        pos = apply_brennpunkt(pos, t_brennpunkt)
        z = pos[2]
        phase = 2 * k * z
        amp_real += math.cos(phase)
        amp_imag += math.sin(phase)

    count = len([n for n in numbers if n <= N])
    if count == 0:
        return 0

    # Normalize by count
    return (amp_real**2 + amp_imag**2) / (count**2)

def test_wavelengths(numbers, N, t_brennpunkt, wavelengths):
    """Test multiple wavelengths"""
    results = {}
    for wl in wavelengths:
        intensity = wave_scatter(numbers, N, wl, t_brennpunkt)
        results[wl] = intensity
    return results

# Main analysis
print("=" * 60)
print("TWIN PRIME RESONANCE ANALYSIS")
print("=" * 60)

N = 2000
primes = sieve_primes(N)
twins = get_twin_primes(primes)
isolated = get_isolated_primes(primes)

print(f"\nN = {N}")
print(f"Total primes: {len(primes)}")
print(f"Twin primes (members of pairs): {len(twins)}")
print(f"Isolated primes: {len(isolated)}")
print(f"First few twins: {twins[:20]}")
print(f"First few isolated: {isolated[:10]}")

# Find Brennpunkt for each class
print("\n" + "-" * 60)
print("BRENNPUNKT SEARCH")
print("-" * 60)

t_all, c_all = find_brennpunkt(primes, N)
t_twins, c_twins = find_brennpunkt(twins, N)
t_isolated, c_isolated = find_brennpunkt(isolated, N)

print(f"\nAll primes:      t = {t_all:.4f}  (expected ~0.25)")
print(f"Twin primes:     t = {t_twins:.4f}")
print(f"Isolated primes: t = {t_isolated:.4f}")

# Refined search around found values
print("\n" + "-" * 60)
print("REFINED BRENNPUNKT")
print("-" * 60)

for name, numbers, t_approx in [("Twins", twins, t_twins), ("Isolated", isolated, t_isolated)]:
    t_refined, c_refined = find_brennpunkt(numbers, N,
                                            t_range=(max(0, t_approx-0.1), min(0.5, t_approx+0.1)),
                                            steps=200)
    print(f"{name:12s}: t = {t_refined:.6f}")

    # Check against simple fractions
    for frac_name, frac_val in [("1/4", 0.25), ("1/3", 1/3), ("1/5", 0.2), ("1/6", 1/6),
                                 ("2/7", 2/7), ("3/8", 3/8), ("2/9", 2/9)]:
        if abs(t_refined - frac_val) < 0.02:
            print(f"             Close to {frac_name} = {frac_val:.6f}")

# Wavelength resonance test
print("\n" + "-" * 60)
print("WAVELENGTH RESONANCE TEST")
print("-" * 60)

# Fibonacci wavelengths
fibs = [3, 5, 8, 13, 21, 34, 55]
wavelengths = [1/f for f in fibs] + [0.1, 0.15, 0.2, 0.3]
wavelengths = sorted(set(wavelengths), reverse=True)

print(f"\nUsing t = 0.25 (standard prime Brennpunkt) for all:")
print(f"\n{'Wavelength':<12} {'All Primes':<12} {'Twins':<12} {'Isolated':<12} {'Twin/All':<10}")
print("-" * 58)

for wl in wavelengths:
    i_all = wave_scatter(primes, N, wl, 0.25)
    i_twins = wave_scatter(twins, N, wl, 0.25)
    i_isolated = wave_scatter(isolated, N, wl, 0.25)

    ratio = i_twins / i_all if i_all > 0 else 0

    marker = ""
    if wl in [1/8, 1/21]:
        marker = " <-- Fibonacci"

    print(f"1/{1/wl:<10.1f} {i_all:<12.6f} {i_twins:<12.6f} {i_isolated:<12.6f} {ratio:<10.2f}{marker}")

# Now test at their OWN Brennpunkts
print("\n" + "-" * 60)
print("RESONANCE AT OWN BRENNPUNKTS")
print("-" * 60)

print(f"\nTwins at their Brennpunkt (t={t_twins:.4f}):")
for wl in [1/3, 1/5, 1/8, 1/13, 1/21]:
    i_own = wave_scatter(twins, N, wl, t_twins)
    i_std = wave_scatter(twins, N, wl, 0.25)
    ratio = i_own / i_std if i_std > 0 else 0
    print(f"  λ = 1/{1/wl:.0f}: own={i_own:.6f}, std={i_std:.6f}, ratio={ratio:.2f}x")

# Scan for special wavelengths for twins
print("\n" + "-" * 60)
print("WAVELENGTH SCAN FOR TWINS")
print("-" * 60)

best_wl = None
best_intensity = 0
scan_results = []

for denom in range(2, 60):
    wl = 1 / denom
    intensity = wave_scatter(twins, N, wl, t_twins)
    scan_results.append((denom, intensity))
    if intensity > best_intensity:
        best_intensity = intensity
        best_wl = denom

scan_results.sort(key=lambda x: -x[1])
print(f"\nTop 10 wavelengths for twins (at their Brennpunkt):")
for denom, intensity in scan_results[:10]:
    fib_marker = " (Fibonacci)" if denom in [1,2,3,5,8,13,21,34,55] else ""
    print(f"  λ = 1/{denom}: {intensity:.6f}{fib_marker}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"\nTwin primes Brennpunkt:     t ≈ {t_twins:.4f}")
print(f"Isolated primes Brennpunkt: t ≈ {t_isolated:.4f}")
print(f"All primes Brennpunkt:      t ≈ {t_all:.4f}")
print(f"\nBest wavelength for twins: λ = 1/{best_wl}")
