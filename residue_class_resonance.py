#!/usr/bin/env python3
"""
Residue Class Resonance Analysis
Do primes ≡ 1 (mod 6) and primes ≡ 5 (mod 6) have different Brennpunkts?
"""

import math

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi / (PHI * PHI)

def sieve_primes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

def golden_sphere_position(n, N):
    theta = GOLDEN_ANGLE * n
    z = 1 - (2 * n) / N
    z = max(-1, min(1, z))
    r_xy = math.sqrt(max(0, 1 - z*z))
    x = r_xy * math.cos(theta)
    y = r_xy * math.sin(theta)
    return (x, y, z)

def apply_brennpunkt(pos, t, R=0.5):
    x, y, z = pos
    r_orig = math.sqrt(x*x + y*y + z*z)
    if r_orig < 1e-10:
        return pos
    r_focused = (r_orig ** (1 - 2*t)) * (R ** (2*t))
    scale = r_focused / r_orig
    return (x * scale, y * scale, z * scale)

def measure_clustering(positions):
    if len(positions) < 2:
        return float('inf')
    cx = sum(p[0] for p in positions) / len(positions)
    cy = sum(p[1] for p in positions) / len(positions)
    cz = sum(p[2] for p in positions) / len(positions)
    msd = sum((p[0]-cx)**2 + (p[1]-cy)**2 + (p[2]-cz)**2 for p in positions) / len(positions)
    return msd

def find_brennpunkt(numbers, N, t_range=(0.0, 0.5), steps=100):
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
    return (amp_real**2 + amp_imag**2) / (count**2)

# Main analysis
print("=" * 70)
print("RESIDUE CLASS RESONANCE ANALYSIS")
print("=" * 70)

N = 2000
primes = sieve_primes(N)

# Classify primes by residue mod 6
# All primes > 3 are either ≡ 1 or ≡ 5 (mod 6)
primes_mod6_1 = [p for p in primes if p > 3 and p % 6 == 1]
primes_mod6_5 = [p for p in primes if p > 3 and p % 6 == 5]
special = [p for p in primes if p <= 3]  # 2 and 3

print(f"\nN = {N}")
print(f"Total primes: {len(primes)}")
print(f"Primes ≡ 1 (mod 6): {len(primes_mod6_1)}  (e.g., 7, 13, 19, 31, 37...)")
print(f"Primes ≡ 5 (mod 6): {len(primes_mod6_5)}  (e.g., 5, 11, 17, 23, 29...)")
print(f"Special (2, 3): {len(special)}")

print(f"\nFirst 10 primes ≡ 1 (mod 6): {primes_mod6_1[:10]}")
print(f"First 10 primes ≡ 5 (mod 6): {primes_mod6_5[:10]}")

# Check: do these classes have same density?
print(f"\nDensity check: {len(primes_mod6_1)} vs {len(primes_mod6_5)}")
print(f"Ratio: {len(primes_mod6_1)/len(primes_mod6_5):.4f} (should be ~1 by Dirichlet)")

# Find Brennpunkt for each class
print("\n" + "-" * 70)
print("BRENNPUNKT SEARCH")
print("-" * 70)

t_all, c_all = find_brennpunkt(primes, N)
t_mod1, c_mod1 = find_brennpunkt(primes_mod6_1, N)
t_mod5, c_mod5 = find_brennpunkt(primes_mod6_5, N)

print(f"\nAll primes:        t = {t_all:.4f}  (expected ~0.25)")
print(f"Primes ≡ 1 (mod 6): t = {t_mod1:.4f}")
print(f"Primes ≡ 5 (mod 6): t = {t_mod5:.4f}")

# Refined search
print("\n" + "-" * 70)
print("REFINED BRENNPUNKT")
print("-" * 70)

for name, numbers, t_approx in [("mod 6 ≡ 1", primes_mod6_1, t_mod1),
                                 ("mod 6 ≡ 5", primes_mod6_5, t_mod5)]:
    t_refined, c_refined = find_brennpunkt(numbers, N,
                                            t_range=(max(0, t_approx-0.1), min(0.5, t_approx+0.1)),
                                            steps=200)
    print(f"{name:12s}: t = {t_refined:.6f}")

    # Check against simple fractions
    for frac_name, frac_val in [("1/4", 0.25), ("1/3", 1/3), ("1/5", 0.2), ("1/6", 1/6),
                                 ("2/7", 2/7), ("3/10", 0.3), ("2/9", 2/9), ("5/21", 5/21)]:
        if abs(t_refined - frac_val) < 0.015:
            print(f"             Close to {frac_name} = {frac_val:.6f}")

# Wavelength resonance
print("\n" + "-" * 70)
print("WAVELENGTH RESONANCE (at t = 0.25)")
print("-" * 70)

print(f"\n{'Wavelength':<12} {'All':<10} {'mod6≡1':<10} {'mod6≡5':<10} {'1/5 ratio':<10}")
print("-" * 52)

for denom in [3, 5, 6, 7, 8, 13, 21, 34]:
    wl = 1/denom
    i_all = wave_scatter(primes, N, wl, 0.25)
    i_mod1 = wave_scatter(primes_mod6_1, N, wl, 0.25)
    i_mod5 = wave_scatter(primes_mod6_5, N, wl, 0.25)

    ratio = i_mod1 / i_mod5 if i_mod5 > 0 else 0

    marker = ""
    if denom in [3, 5, 8, 13, 21, 34]:
        marker = " Fib"
    if denom == 6:
        marker = " MOD BASE"

    print(f"1/{denom:<10} {i_all:<10.5f} {i_mod1:<10.5f} {i_mod5:<10.5f} {ratio:<10.3f}{marker}")

# Test at their own Brennpunkts
print("\n" + "-" * 70)
print("RESONANCE AT OWN BRENNPUNKTS")
print("-" * 70)

print("\nPrimes ≡ 1 (mod 6) at t = {:.4f}:".format(t_mod1))
for denom in [5, 6, 7, 8, 13, 21]:
    wl = 1/denom
    i_own = wave_scatter(primes_mod6_1, N, wl, t_mod1)
    i_std = wave_scatter(primes_mod6_1, N, wl, 0.25)
    amp = i_own / i_std if i_std > 0 else 0
    print(f"  λ = 1/{denom}: own={i_own:.5f}, std={i_std:.5f}, amplification={amp:.2f}x")

print("\nPrimes ≡ 5 (mod 6) at t = {:.4f}:".format(t_mod5))
for denom in [5, 6, 7, 8, 13, 21]:
    wl = 1/denom
    i_own = wave_scatter(primes_mod6_5, N, wl, t_mod5)
    i_std = wave_scatter(primes_mod6_5, N, wl, 0.25)
    amp = i_own / i_std if i_std > 0 else 0
    print(f"  λ = 1/{denom}: own={i_own:.5f}, std={i_std:.5f}, amplification={amp:.2f}x")

# Scan for DIFFERENT wavelengths for each class
print("\n" + "-" * 70)
print("WAVELENGTH SCAN - LOOKING FOR CLASS-SPECIFIC RESONANCES")
print("-" * 70)

results_mod1 = []
results_mod5 = []

for denom in range(2, 50):
    wl = 1/denom
    i1 = wave_scatter(primes_mod6_1, N, wl, t_mod1)
    i5 = wave_scatter(primes_mod6_5, N, wl, t_mod5)
    results_mod1.append((denom, i1))
    results_mod5.append((denom, i5))

results_mod1.sort(key=lambda x: -x[1])
results_mod5.sort(key=lambda x: -x[1])

print("\nTop 5 wavelengths for primes ≡ 1 (mod 6):")
for denom, intensity in results_mod1[:5]:
    fib = " (Fib)" if denom in [1,2,3,5,8,13,21,34] else ""
    mod6 = " (=6k)" if denom % 6 == 0 else ""
    print(f"  λ = 1/{denom}: {intensity:.5f}{fib}{mod6}")

print("\nTop 5 wavelengths for primes ≡ 5 (mod 6):")
for denom, intensity in results_mod5[:5]:
    fib = " (Fib)" if denom in [1,2,3,5,8,13,21,34] else ""
    mod6 = " (=6k)" if denom % 6 == 0 else ""
    print(f"  λ = 1/{denom}: {intensity:.5f}{fib}{mod6}")

# Now try mod 4 classes
print("\n" + "=" * 70)
print("BONUS: MOD 4 RESIDUE CLASSES")
print("=" * 70)

primes_mod4_1 = [p for p in primes if p > 2 and p % 4 == 1]
primes_mod4_3 = [p for p in primes if p > 2 and p % 4 == 3]

print(f"\nPrimes ≡ 1 (mod 4): {len(primes_mod4_1)} (can be sum of two squares)")
print(f"Primes ≡ 3 (mod 4): {len(primes_mod4_3)} (cannot be sum of two squares)")

t_4mod1, _ = find_brennpunkt(primes_mod4_1, N)
t_4mod3, _ = find_brennpunkt(primes_mod4_3, N)

print(f"\nBrennpunkt for ≡ 1 (mod 4): t = {t_4mod1:.4f}")
print(f"Brennpunkt for ≡ 3 (mod 4): t = {t_4mod3:.4f}")

# Check if the split relates to sum-of-squares property
print("\nNote: Primes ≡ 1 (mod 4) can be written as a² + b²")
print("      This is Fermat's theorem on sums of two squares")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"""
RESIDUE CLASS BRENNPUNKTS:
  All primes:        t ≈ {t_all:.4f} (≈ 1/4)
  Primes ≡ 1 (mod 6): t ≈ {t_mod1:.4f}
  Primes ≡ 5 (mod 6): t ≈ {t_mod5:.4f}
  Primes ≡ 1 (mod 4): t ≈ {t_4mod1:.4f}
  Primes ≡ 3 (mod 4): t ≈ {t_4mod3:.4f}

Do they differ? Let's see the data above...
""")
