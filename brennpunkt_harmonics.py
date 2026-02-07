#!/usr/bin/env python3
"""
GRAND SYNTHESIS: Spherical Harmonics at the Brennpunkt

Combine everything:
1. Golden spiral projection
2. Partial inversion to Brennpunkt (t = 1/3)
3. Spherical harmonic decomposition
4. Compare to original configuration

What happens to the spectrum when primes are FOCUSED?
"""

import math

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi / (PHI * PHI)
BRENNPUNKT_T = 1/3  # The focal parameter

def sieve_primes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return set(i for i in range(limit + 1) if is_prime[i])

def golden_spiral_angles(n, N):
    """Return (theta, phi) for point n on golden spiral."""
    theta = (GOLDEN_ANGLE * n) % (2 * math.pi)
    z = 1 - (2 * n) / N
    z = max(-1, min(1, z))
    phi = math.acos(z)
    return theta, phi

def partial_inversion_radius(n, N, t, R=0.5):
    """Compute radius under partial log-inversion."""
    r_orig = n / N
    if r_orig < 1e-10:
        r_orig = 1e-10
    r_t = (r_orig ** (1 - 2*t)) * (R ** (2*t))
    return r_t

def legendre_p(l, m, x):
    """Associated Legendre polynomial P_l^m(x)."""
    if m < 0:
        m = -m

    pmm = 1.0
    if m > 0:
        somx2 = math.sqrt(max(0, 1 - x*x))
        fact = 1.0
        for i in range(1, m + 1):
            pmm *= -fact * somx2
            fact += 2.0

    if l == m:
        return pmm

    pmmp1 = x * (2*m + 1) * pmm
    if l == m + 1:
        return pmmp1

    pll = 0.0
    for ll in range(m + 2, l + 1):
        pll = (x * (2*ll - 1) * pmmp1 - (ll + m - 1) * pmm) / (ll - m)
        pmm = pmmp1
        pmmp1 = pll

    return pll

def spherical_harmonic_real(l, m, theta, phi):
    """Real spherical harmonic Y_l^m(theta, phi)."""
    abs_m = abs(m)

    num = 1
    den = 1
    for i in range(l - abs_m + 1, l + abs_m + 1):
        den *= i

    norm = math.sqrt((2*l + 1) / (4 * math.pi) * num / den)
    x = math.cos(phi)
    plm = legendre_p(l, abs_m, x)

    if m > 0:
        return math.sqrt(2) * norm * plm * math.cos(m * theta)
    elif m < 0:
        return math.sqrt(2) * norm * plm * math.sin(abs_m * theta)
    else:
        return norm * plm

def compute_power_spectrum(indicator_func, N, l_max):
    """Compute angular power spectrum C_l for a function on sphere."""
    coefficients = {}

    # Sample points
    points = []
    for n in range(1, N + 1):
        theta, phi = golden_spiral_angles(n, N)
        val = indicator_func(n)
        weight = 4 * math.pi / N
        points.append((theta, phi, val, weight))

    # Compute coefficients
    for l in range(l_max + 1):
        for m in range(-l, l + 1):
            total = 0.0
            for theta, phi, val, weight in points:
                ylm = spherical_harmonic_real(l, m, theta, phi)
                total += val * ylm * weight
            coefficients[(l, m)] = total

    # Power spectrum
    spectrum = []
    for l in range(l_max + 1):
        power = sum(coefficients.get((l, m), 0)**2 for m in range(-l, l + 1)) / (2*l + 1)
        spectrum.append(power)

    return spectrum, coefficients

def compute_radial_weighted_spectrum(indicator_func, radius_func, N, l_max):
    """
    Power spectrum weighted by radius.
    Points closer to origin contribute more.
    """
    coefficients = {}

    points = []
    total_weight = 0
    for n in range(1, N + 1):
        theta, phi = golden_spiral_angles(n, N)
        val = indicator_func(n)
        r = radius_func(n)
        # Weight inversely by radius (closer = stronger)
        w = 1.0 / (r + 0.1)  # Avoid division by zero
        total_weight += w
        points.append((theta, phi, val, w))

    # Normalize weights
    points = [(t, p, v, w/total_weight * 4 * math.pi) for t, p, v, w in points]

    for l in range(l_max + 1):
        for m in range(-l, l + 1):
            total = 0.0
            for theta, phi, val, weight in points:
                ylm = spherical_harmonic_real(l, m, theta, phi)
                total += val * ylm * weight
            coefficients[(l, m)] = total

    spectrum = []
    for l in range(l_max + 1):
        power = sum(coefficients.get((l, m), 0)**2 for m in range(-l, l + 1)) / (2*l + 1)
        spectrum.append(power)

    return spectrum, coefficients

def analyze_brennpunkt_harmonics():
    print("=" * 70)
    print("GRAND SYNTHESIS: Spherical Harmonics at the Brennpunkt")
    print("=" * 70)

    N = 500
    L_MAX = 20
    primes = sieve_primes(N)

    print(f"\nPoints: {N}, Primes: {len(primes)}")
    print(f"Brennpunkt: t = {BRENNPUNKT_T:.4f}")
    print(f"Computing harmonics up to l = {L_MAX}")

    def prime_indicator(n):
        return 1.0 if n in primes else 0.0

    # Original configuration (t=0)
    print("\n" + "=" * 70)
    print("CONFIGURATION 1: Original (t = 0)")
    print("=" * 70)

    spectrum_orig, coeffs_orig = compute_power_spectrum(prime_indicator, N, L_MAX)

    # At Brennpunkt (t=1/3)
    print("\n" + "=" * 70)
    print(f"CONFIGURATION 2: Brennpunkt (t = {BRENNPUNKT_T:.4f})")
    print("=" * 70)

    def radius_at_brennpunkt(n):
        return partial_inversion_radius(n, N, BRENNPUNKT_T)

    spectrum_brenn, coeffs_brenn = compute_radial_weighted_spectrum(
        prime_indicator, radius_at_brennpunkt, N, L_MAX
    )

    # Fully inverted (t=1)
    print("\n" + "=" * 70)
    print("CONFIGURATION 3: Fully Inverted (t = 1)")
    print("=" * 70)

    def radius_inverted(n):
        return partial_inversion_radius(n, N, 1.0)

    spectrum_inv, coeffs_inv = compute_radial_weighted_spectrum(
        prime_indicator, radius_inverted, N, L_MAX
    )

    # Comparison
    print("\n" + "=" * 70)
    print("POWER SPECTRUM COMPARISON")
    print("=" * 70)

    print(f"\n{'l':<6}{'Original':<14}{'Brennpunkt':<14}{'Inverted':<14}{'B/O Ratio':<12}")
    print("-" * 60)

    fibs = {1, 2, 3, 5, 8, 13}

    for l in range(L_MAX + 1):
        orig = spectrum_orig[l]
        brenn = spectrum_brenn[l]
        inv = spectrum_inv[l]
        ratio = brenn / orig if orig > 0 else 0

        fib_marker = " ← FIB" if l in fibs else ""
        peak_marker = " ***" if ratio > 2 or ratio < 0.5 else ""

        if l == 0:
            print(f"{l:<6}{orig:<14.6f}{brenn:<14.6f}{inv:<14.6f}{'(DC)':<12}")
        else:
            print(f"{l:<6}{orig:<14.6f}{brenn:<14.6f}{inv:<14.6f}{ratio:<12.2f}{peak_marker}{fib_marker}")

    # What changes most?
    print("\n" + "=" * 70)
    print("LARGEST CHANGES AT BRENNPUNKT")
    print("=" * 70)

    changes = []
    for l in range(1, L_MAX + 1):
        ratio = spectrum_brenn[l] / spectrum_orig[l] if spectrum_orig[l] > 0 else 1
        changes.append((ratio, l, spectrum_orig[l], spectrum_brenn[l]))

    print("\nModes AMPLIFIED at Brennpunkt (ratio > 1):")
    for ratio, l, orig, brenn in sorted(changes, reverse=True)[:10]:
        if ratio > 1:
            fib = "FIBONACCI" if l in fibs else ""
            print(f"  l={l}: {ratio:.2f}x amplified ({orig:.6f} → {brenn:.6f}) {fib}")

    print("\nModes SUPPRESSED at Brennpunkt (ratio < 1):")
    for ratio, l, orig, brenn in sorted(changes)[:10]:
        if ratio < 1:
            fib = "FIBONACCI" if l in fibs else ""
            print(f"  l={l}: {ratio:.2f}x suppressed ({orig:.6f} → {brenn:.6f}) {fib}")

    # Fibonacci analysis
    print("\n" + "=" * 70)
    print("FIBONACCI MODES BEHAVIOR")
    print("=" * 70)

    print(f"\n{'l (Fib)':<10}{'Original':<14}{'Brennpunkt':<14}{'Ratio':<10}")
    print("-" * 48)

    for l in [1, 2, 3, 5, 8, 13]:
        if l <= L_MAX:
            orig = spectrum_orig[l]
            brenn = spectrum_brenn[l]
            ratio = brenn / orig if orig > 0 else 0
            print(f"{l:<10}{orig:<14.6f}{brenn:<14.6f}{ratio:<10.2f}")

    fib_power_orig = sum(spectrum_orig[l] for l in [1,2,3,5,8,13] if l <= L_MAX)
    fib_power_brenn = sum(spectrum_brenn[l] for l in [1,2,3,5,8,13] if l <= L_MAX)

    print(f"\nTotal Fibonacci power: {fib_power_orig:.6f} → {fib_power_brenn:.6f}")
    print(f"Ratio: {fib_power_brenn/fib_power_orig:.2f}x")

    # The l=3 mode (related to Brennpunkt t=1/3?)
    print("\n" + "=" * 70)
    print("THE l=3 MODE (related to Brennpunkt t=1/3?)")
    print("=" * 70)

    print(f"\nl=3 at original: {spectrum_orig[3]:.6f}")
    print(f"l=3 at Brennpunkt: {spectrum_brenn[3]:.6f}")
    print(f"l=3 at inverted: {spectrum_inv[3]:.6f}")

    ratio_3 = spectrum_brenn[3] / spectrum_orig[3] if spectrum_orig[3] > 0 else 0
    print(f"\nBrennpunkt/Original ratio for l=3: {ratio_3:.2f}")

    # Is l=3 special because Brennpunkt = 1/3?
    print("\nIs l=3 special because Brennpunkt = 1/3?")
    print("The connection: 3 is both the Brennpunkt denominator AND a Fibonacci number")

    # Strongest individual coefficients at Brennpunkt
    print("\n" + "=" * 70)
    print("STRONGEST MODES AT BRENNPUNKT")
    print("=" * 70)

    sorted_coeffs = sorted([(abs(v), (l,m), v) for (l,m), v in coeffs_brenn.items() if l > 0],
                          reverse=True)

    print(f"\n{'(l,m)':<12}{'|a_lm|':<14}{'At Original':<14}")
    print("-" * 40)

    for absv, (l,m), v in sorted_coeffs[:15]:
        orig_v = coeffs_orig.get((l,m), 0)
        ratio = absv / abs(orig_v) if abs(orig_v) > 0.001 else 0
        print(f"({l},{m:+d}){'':<5}{absv:<14.4f}{abs(orig_v):<14.4f}")

    # Synthesis
    print("\n" + "=" * 70)
    print("GRAND SYNTHESIS")
    print("=" * 70)
    print(f"""
SPHERICAL HARMONICS AT THE BRENNPUNKT reveal:

1. FOCUSING changes the spectrum
   - Some modes amplified, others suppressed
   - The angular structure SHIFTS when primes are focused

2. FIBONACCI MODES at Brennpunkt:
   - Total Fibonacci power changes by {fib_power_brenn/fib_power_orig:.2f}x

3. THE l=3 CONNECTION:
   - Brennpunkt is at t = 1/3
   - l=3 is both Fibonacci AND related to the focal parameter
   - Ratio for l=3: {ratio_3:.2f}x

4. PHYSICAL INTERPRETATION:
   - Original: primes spread on sphere, certain angular scales dominate
   - Brennpunkt: primes FOCUSED, angular structure changes
   - Like changing the aperture of a telescope - different scales come into focus

The combination of:
- Golden spiral (φ)
- Brennpunkt (1/3)
- Spherical harmonics (angular decomposition)
- Prime distribution

creates a unified picture where NUMBER THEORY and GEOMETRY
interact through WAVE-LIKE decomposition.

This is the "grand unified" view of prime structure in 3D.
""")

if __name__ == "__main__":
    analyze_brennpunkt_harmonics()
