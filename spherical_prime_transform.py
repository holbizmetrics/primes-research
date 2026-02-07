#!/usr/bin/env python3
"""
Spherical Harmonic Transform of Prime Distribution

"What's the Fourier transform of primes on a sphere?"

Spherical harmonics Y_l^m are the Fourier basis on S².
Decompose prime indicator function into these modes.

Like CMB analysis - but for primes!
"""

import math

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi / (PHI * PHI)

def sieve_primes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return set(i for i in range(limit + 1) if is_prime[i])

def golden_spiral_angles(n, total):
    """
    Return (theta, phi) spherical coordinates for integer n.
    theta = azimuthal angle [0, 2π]
    phi = polar angle [0, π]
    """
    theta = (GOLDEN_ANGLE * n) % (2 * math.pi)
    # z = cos(phi) goes from 1 to -1
    z = 1 - (2 * n) / total
    z = max(-1, min(1, z))
    phi = math.acos(z)
    return theta, phi

def legendre_p(l, m, x):
    """
    Associated Legendre polynomial P_l^m(x).
    Simplified implementation for small l, m.
    """
    # P_0^0 = 1
    if l == 0 and m == 0:
        return 1.0

    # Use recurrence relations
    # Start with P_m^m
    if m < 0:
        m = -m

    # P_m^m = (-1)^m (2m-1)!! (1-x²)^(m/2)
    pmm = 1.0
    if m > 0:
        somx2 = math.sqrt(max(0, 1 - x*x))
        fact = 1.0
        for i in range(1, m + 1):
            pmm *= -fact * somx2
            fact += 2.0

    if l == m:
        return pmm

    # P_{m+1}^m = x(2m+1)P_m^m
    pmmp1 = x * (2*m + 1) * pmm
    if l == m + 1:
        return pmmp1

    # Use recurrence: (l-m)P_l^m = x(2l-1)P_{l-1}^m - (l+m-1)P_{l-2}^m
    pll = 0.0
    for ll in range(m + 2, l + 1):
        pll = (x * (2*ll - 1) * pmmp1 - (ll + m - 1) * pmm) / (ll - m)
        pmm = pmmp1
        pmmp1 = pll

    return pll

def spherical_harmonic_real(l, m, theta, phi):
    """
    Real spherical harmonic Y_l^m(theta, phi).

    For m > 0: Y_l^m = sqrt(2) * N * P_l^m(cos(phi)) * cos(m*theta)
    For m < 0: Y_l^m = sqrt(2) * N * P_l^|m|(cos(phi)) * sin(|m|*theta)
    For m = 0: Y_l^0 = N * P_l^0(cos(phi))

    N = normalization factor
    """
    # Normalization
    abs_m = abs(m)

    # (l - |m|)! / (l + |m|)!
    num = 1
    den = 1
    for i in range(l - abs_m + 1, l + abs_m + 1):
        den *= i

    norm = math.sqrt((2*l + 1) / (4 * math.pi) * num / den)

    # Legendre polynomial
    x = math.cos(phi)
    plm = legendre_p(l, abs_m, x)

    if m > 0:
        return math.sqrt(2) * norm * plm * math.cos(m * theta)
    elif m < 0:
        return math.sqrt(2) * norm * plm * math.sin(abs_m * theta)
    else:
        return norm * plm

def compute_spherical_coefficients(signal_func, N_points, l_max):
    """
    Compute spherical harmonic coefficients of a function on the sphere.

    a_lm = ∫ f(θ,φ) Y_lm(θ,φ) dΩ

    Approximated by sum over sample points.
    """
    coefficients = {}

    # Sample points on sphere (golden spiral)
    points = []
    for n in range(1, N_points + 1):
        theta, phi = golden_spiral_angles(n, N_points)
        val = signal_func(n)
        # Weight by solid angle element (approximately uniform for golden spiral)
        weight = 4 * math.pi / N_points
        points.append((theta, phi, val, weight))

    # Compute coefficients
    for l in range(l_max + 1):
        for m in range(-l, l + 1):
            total = 0.0
            for theta, phi, val, weight in points:
                ylm = spherical_harmonic_real(l, m, theta, phi)
                total += val * ylm * weight
            coefficients[(l, m)] = total

    return coefficients

def power_spectrum(coefficients, l_max):
    """
    Compute angular power spectrum C_l = (1/(2l+1)) Σ_m |a_lm|²
    """
    spectrum = []
    for l in range(l_max + 1):
        power = 0.0
        for m in range(-l, l + 1):
            alm = coefficients.get((l, m), 0)
            power += alm * alm
        power /= (2*l + 1)
        spectrum.append(power)
    return spectrum

def analyze_prime_harmonics():
    print("=" * 65)
    print("SPHERICAL HARMONIC TRANSFORM OF PRIMES")
    print("The Fourier Transform of Prime Distribution on a Sphere")
    print("=" * 65)

    N = 500  # Number of points
    L_MAX = 20  # Maximum l to compute

    primes = sieve_primes(N)
    print(f"\nPoints on sphere: {N}")
    print(f"Primes: {len(primes)}")
    print(f"Computing harmonics up to l = {L_MAX}")

    # Prime indicator function
    def prime_indicator(n):
        return 1.0 if n in primes else 0.0

    # Compute coefficients
    print("\nComputing spherical harmonic coefficients...")
    coeffs = compute_spherical_coefficients(prime_indicator, N, L_MAX)

    # Power spectrum
    print("Computing power spectrum...")
    spectrum = power_spectrum(coeffs, L_MAX)

    print("\n" + "=" * 65)
    print("ANGULAR POWER SPECTRUM C_l")
    print("(Like CMB power spectrum, but for primes)")
    print("=" * 65)

    print(f"\n{'l':<6}{'C_l':<15}{'√C_l':<12}{'Bar':<30}")
    print("-" * 60)

    max_power = max(spectrum[1:])  # Exclude l=0 (mean)

    for l, cl in enumerate(spectrum):
        sqrt_cl = math.sqrt(cl) if cl > 0 else 0
        bar_len = int(30 * cl / max_power) if max_power > 0 and l > 0 else 0
        bar = "█" * bar_len

        marker = ""
        if l == 0:
            marker = " ← mean (DC component)"
        elif l in [1, 2, 3, 5, 8, 13]:
            marker = f" ← l={l} (Fibonacci!)" if l in [1, 2, 3, 5, 8, 13] else ""

        print(f"{l:<6}{cl:<15.6f}{sqrt_cl:<12.4f}{bar}{marker}")

    # Find dominant modes
    print("\n" + "=" * 65)
    print("DOMINANT MODES (excluding l=0)")
    print("=" * 65)

    sorted_modes = sorted([(spectrum[l], l) for l in range(1, L_MAX + 1)], reverse=True)

    print(f"\nTop 10 l-values by power:")
    for rank, (power, l) in enumerate(sorted_modes[:10], 1):
        fib_marker = "FIBONACCI" if l in [1, 2, 3, 5, 8, 13] else ""
        print(f"  {rank}. l={l}: C_l = {power:.6f} {fib_marker}")

    # Check for peaks at Fibonacci l
    print("\n" + "=" * 65)
    print("FIBONACCI l-VALUES")
    print("=" * 65)

    fibs = [1, 2, 3, 5, 8, 13]
    non_fibs = [l for l in range(1, 14) if l not in fibs]

    fib_power = sum(spectrum[l] for l in fibs if l <= L_MAX)
    non_fib_power = sum(spectrum[l] for l in non_fibs if l <= L_MAX)

    print(f"\nTotal power in Fibonacci l (1,2,3,5,8,13): {fib_power:.6f}")
    print(f"Total power in non-Fibonacci l (4,6,7,9,10,11,12): {non_fib_power:.6f}")
    print(f"Ratio (Fib/non-Fib): {fib_power/non_fib_power:.3f}")

    # Strongest individual coefficients
    print("\n" + "=" * 65)
    print("STRONGEST INDIVIDUAL MODES a_lm")
    print("=" * 65)

    sorted_coeffs = sorted([(abs(v), k, v) for k, v in coeffs.items()], reverse=True)

    print(f"\nTop 15 coefficients:")
    print(f"{'(l,m)':<12}{'|a_lm|':<12}{'a_lm':<15}")
    print("-" * 40)

    for rank, (absv, (l, m), v) in enumerate(sorted_coeffs[:15], 1):
        if l == 0:
            continue  # Skip DC
        print(f"({l},{m:+d})      {absv:<12.4f}{v:<+15.4f}")

    # Compare to random
    print("\n" + "=" * 65)
    print("COMPARISON TO RANDOM")
    print("=" * 65)

    import random
    random.seed(42)

    def random_indicator(n):
        # Same density as primes
        return 1.0 if random.random() < len(primes)/N else 0.0

    random_coeffs = compute_spherical_coefficients(random_indicator, N, L_MAX)
    random_spectrum = power_spectrum(random_coeffs, L_MAX)

    print(f"\n{'l':<6}{'C_l (primes)':<15}{'C_l (random)':<15}{'Ratio':<10}")
    print("-" * 46)

    for l in range(1, min(15, L_MAX + 1)):
        ratio = spectrum[l] / random_spectrum[l] if random_spectrum[l] > 0 else 0
        marker = " ***" if ratio > 2 or ratio < 0.5 else ""
        print(f"{l:<6}{spectrum[l]:<15.6f}{random_spectrum[l]:<15.6f}{ratio:<10.2f}{marker}")

    # Synthesis
    print("\n" + "=" * 65)
    print("SYNTHESIS")
    print("=" * 65)
    print("""
The spherical harmonic decomposition reveals:

1. POWER SPECTRUM: Which angular scales dominate in prime distribution?
   - Low l = large-scale structure (hemispheric)
   - High l = small-scale structure (local clustering)

2. FIBONACCI CHECK: Do l = 1,2,3,5,8,13 have special significance?

3. COMPARISON TO RANDOM: Where does prime distribution differ from noise?

This is the "X-ray crystallography" of primes on a sphere.
The diffraction pattern (power spectrum) encodes the structure.

If primes have non-random angular structure on the golden spiral,
it will show up as excess/deficit power at specific l values.
""")

if __name__ == "__main__":
    analyze_prime_harmonics()
