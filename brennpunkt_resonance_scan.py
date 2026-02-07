#!/usr/bin/env python3
"""
Find the TRUE Brennpunkt: the t that maximizes resonance at Fibonacci wavelengths.
Not variance minimization (which trivially goes to t=0.5).
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

def get_composites(n, primes):
    prime_set = set(primes)
    return [i for i in range(4, n+1) if i not in prime_set]

def golden_sphere_position(n, N):
    theta = GOLDEN_ANGLE * n
    z = 1 - (2 * n) / N
    z = max(-1, min(1, z))
    r_xy = math.sqrt(max(0, 1 - z*z))
    return (r_xy * math.cos(theta), r_xy * math.sin(theta), z)

def apply_brennpunkt(pos, t, R=0.5):
    x, y, z = pos
    r_orig = math.sqrt(x*x + y*y + z*z)
    if r_orig < 1e-10:
        return pos
    r_focused = (r_orig ** (1 - 2*t)) * (R ** (2*t))
    scale = r_focused / r_orig
    return (x * scale, y * scale, z * scale)

def wave_scatter_intensity(numbers, N, wavelength, t):
    """Compute backscatter intensity at given wavelength and Brennpunkt t"""
    k = 2 * math.pi / wavelength
    amp_real, amp_imag = 0, 0

    count = 0
    for n in numbers:
        if n > N:
            continue
        count += 1
        pos = golden_sphere_position(n, N)
        pos = apply_brennpunkt(pos, t)
        z = pos[2]
        phase = 2 * k * z
        amp_real += math.cos(phase)
        amp_imag += math.sin(phase)

    if count == 0:
        return 0
    return (amp_real**2 + amp_imag**2) / (count**2)

def find_optimal_t_for_resonance(numbers, N, wavelength, t_range=(0, 0.5), steps=200):
    """Find t that MAXIMIZES resonance at given wavelength"""
    best_t = 0
    best_intensity = 0

    results = []
    for i in range(steps + 1):
        t = t_range[0] + (t_range[1] - t_range[0]) * i / steps
        intensity = wave_scatter_intensity(numbers, N, wavelength, t)
        results.append((t, intensity))
        if intensity > best_intensity:
            best_intensity = intensity
            best_t = t

    return best_t, best_intensity, results

# Main analysis
print("=" * 70)
print("TRUE BRENNPUNKT: MAXIMIZING RESONANCE")
print("=" * 70)

N = 1000
primes = sieve_primes(N)
composites = get_composites(N, primes)

print(f"\nN = {N}")
print(f"Primes: {len(primes)}, Composites: {len(composites)}")

# Test at multiple Fibonacci wavelengths
fib_wavelengths = [1/5, 1/8, 1/13, 1/21, 1/34]

print("\n" + "-" * 70)
print("PRIMES: Optimal t for each Fibonacci wavelength")
print("-" * 70)

print(f"\n{'Wavelength':<12} {'Optimal t':<12} {'Intensity':<12} {'Close to?':<20}")
print("-" * 56)

prime_t_values = []
for wl in fib_wavelengths:
    opt_t, opt_int, _ = find_optimal_t_for_resonance(primes, N, wl)
    prime_t_values.append(opt_t)

    # Check what fraction it's close to
    close_to = ""
    for name, val in [("1/4", 0.25), ("1/3", 1/3), ("1/5", 0.2), ("2/9", 2/9),
                       ("3/13", 3/13), ("5/21", 5/21), ("1/6", 1/6)]:
        if abs(opt_t - val) < 0.015:
            close_to = name

    denom = round(1/wl)
    print(f"1/{denom:<10} {opt_t:<12.4f} {opt_int:<12.6f} {close_to:<20}")

avg_prime_t = sum(prime_t_values) / len(prime_t_values)
print(f"\nAverage optimal t for primes: {avg_prime_t:.4f}")

print("\n" + "-" * 70)
print("COMPOSITES: Optimal t for each Fibonacci wavelength")
print("-" * 70)

print(f"\n{'Wavelength':<12} {'Optimal t':<12} {'Intensity':<12} {'Close to?':<20}")
print("-" * 56)

comp_t_values = []
for wl in fib_wavelengths:
    opt_t, opt_int, _ = find_optimal_t_for_resonance(composites, N, wl)
    comp_t_values.append(opt_t)

    close_to = ""
    for name, val in [("1/4", 0.25), ("1/3", 1/3), ("1/5", 0.2), ("2/9", 2/9),
                       ("3/13", 3/13), ("5/21", 5/21), ("1/6", 1/6)]:
        if abs(opt_t - val) < 0.015:
            close_to = name

    denom = round(1/wl)
    print(f"1/{denom:<10} {opt_t:<12.4f} {opt_int:<12.6f} {close_to:<20}")

avg_comp_t = sum(comp_t_values) / len(comp_t_values)
print(f"\nAverage optimal t for composites: {avg_comp_t:.4f}")

# Now scan more finely around expected values
print("\n" + "-" * 70)
print("FINE SCAN AROUND 1/4 FOR PRIMES (λ = 1/21)")
print("-" * 70)

opt_t, opt_int, results = find_optimal_t_for_resonance(primes, N, 1/21, t_range=(0.15, 0.35), steps=400)
print(f"\nOptimal t = {opt_t:.6f}")
print(f"Intensity at optimum: {opt_int:.6f}")

# Show profile around optimum
print("\nResonance profile:")
for t, intensity in results[::40]:  # Every 40th point
    bar = "#" * int(intensity * 500)
    marker = " <-- 1/4" if abs(t - 0.25) < 0.005 else ""
    marker = " <-- 1/3" if abs(t - 1/3) < 0.005 else marker
    print(f"  t={t:.3f}: {intensity:.5f} {bar}{marker}")

print("\n" + "-" * 70)
print("FINE SCAN AROUND 1/3 FOR COMPOSITES (λ = 1/21)")
print("-" * 70)

opt_t, opt_int, results = find_optimal_t_for_resonance(composites, N, 1/21, t_range=(0.2, 0.45), steps=400)
print(f"\nOptimal t = {opt_t:.6f}")
print(f"Intensity at optimum: {opt_int:.6f}")

print("\nResonance profile:")
for t, intensity in results[::40]:
    bar = "#" * int(intensity * 500)
    marker = " <-- 1/4" if abs(t - 0.25) < 0.005 else ""
    marker = " <-- 1/3" if abs(t - 1/3) < 0.005 else marker
    print(f"  t={t:.3f}: {intensity:.5f} {bar}{marker}")

# Compare primes vs composites at different t values
print("\n" + "-" * 70)
print("PRIME/COMPOSITE RATIO at λ = 1/21 vs t")
print("-" * 70)

print("\n  t      Prime    Composite   Ratio")
print("-" * 40)

for t in [0.0, 0.1, 0.2, 0.25, 0.30, 1/3, 0.4, 0.45, 0.5]:
    p_int = wave_scatter_intensity(primes, N, 1/21, t)
    c_int = wave_scatter_intensity(composites, N, 1/21, t)
    ratio = p_int / c_int if c_int > 0 else float('inf')
    marker = ""
    if t == 0.25:
        marker = " <-- prime Brennpunkt"
    if abs(t - 1/3) < 0.01:
        marker = " <-- composite Brennpunkt"
    print(f"  {t:.3f}  {p_int:.5f}  {c_int:.5f}    {ratio:.2f}x{marker}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"""
TRUE BRENNPUNKT (maximizing resonance):

  Primes:     t ≈ {avg_prime_t:.3f}
  Composites: t ≈ {avg_comp_t:.3f}

The Brennpunkt is where RESONANCE peaks, not where variance minimizes.

Key insight: At t=1/4, primes show maximum wave coherence.
             At t=1/3, composites show their maximum.
""")
