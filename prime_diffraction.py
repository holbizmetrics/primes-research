#!/usr/bin/env python3
"""
PRIME DIFFRACTION PATTERN

What happens when a plane wave hits the prime-decorated sphere?
Treat primes as scatterers - compute the diffraction pattern.

This is the "prime metamaterial" as an optical/acoustic element.
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

def golden_spiral_3d(n, N):
    """Map n to 3D point on unit sphere."""
    theta = GOLDEN_ANGLE * n
    z = 1 - (2 * n) / N
    z = max(-1, min(1, z))
    r_xy = math.sqrt(max(0, 1 - z*z))
    x = r_xy * math.cos(theta)
    y = r_xy * math.sin(theta)
    return (x, y, z)

def compute_diffraction(primes, N, k_vec, num_angles=180):
    """
    Compute diffraction pattern from prime scatterers.
    
    Incoming plane wave with wavevector k_vec.
    Each prime at position r_p scatters spherically.
    
    Far-field amplitude in direction (theta, phi):
    A(theta, phi) = sum_p exp(i * k * (r_p . (k_hat - s_hat)))
    
    where s_hat is the scattering direction.
    """
    k_mag = math.sqrt(sum(ki**2 for ki in k_vec))
    k_hat = tuple(ki/k_mag for ki in k_vec)
    
    # Get prime positions
    prime_positions = [golden_spiral_3d(p, N) for p in primes if p <= N]
    
    # Scan scattering angles in the plane containing k_vec
    # Use theta from 0 to 180 degrees (forward to backward)
    
    pattern = []
    
    for i in range(num_angles + 1):
        theta = math.pi * i / num_angles  # 0 to pi
        
        # Scattering direction in xz plane (assuming k along z)
        s_hat = (math.sin(theta), 0, math.cos(theta))
        
        # Momentum transfer
        q = tuple(k_mag * (k_hat[j] - s_hat[j]) for j in range(3))
        
        # Sum over all prime scatterers
        amp_real = 0
        amp_imag = 0
        
        for pos in prime_positions:
            # Phase = q . r
            phase = sum(q[j] * pos[j] for j in range(3))
            amp_real += math.cos(phase)
            amp_imag += math.sin(phase)
        
        intensity = amp_real**2 + amp_imag**2
        pattern.append((math.degrees(theta), intensity, amp_real, amp_imag))
    
    return pattern

def analyze_diffraction():
    print("=" * 70)
    print("PRIME DIFFRACTION PATTERN")
    print("=" * 70)
    
    N = 500
    primes = sieve_primes(N)
    
    print(f"\nScatterers: {len(primes)} primes on golden-spiral sphere")
    print(f"N = {N}")
    
    # Incoming wave along z-axis
    k_mag = 2 * math.pi  # wavelength = 1 (in units of sphere radius)
    k_vec = (0, 0, k_mag)
    
    print(f"\nIncoming wave: k = (0, 0, {k_mag:.2f})")
    print(f"Wavelength: lambda = 1.0")
    
    pattern = compute_diffraction(primes, N, k_vec)
    
    # Find peaks
    print("\n" + "=" * 70)
    print("DIFFRACTION PATTERN (forward = 0°, backward = 180°)")
    print("=" * 70)
    
    # Normalize
    max_intensity = max(p[1] for p in pattern)
    
    print(f"\n{'Angle':<10}{'Intensity':<15}{'Normalized':<15}")
    print("-" * 40)
    
    for angle, intensity, _, _ in pattern[::10]:  # Every 10 degrees
        norm = intensity / max_intensity
        bar = "#" * int(norm * 30)
        print(f"{angle:>6.0f}°    {intensity:>10.1f}    {norm:>6.3f}  {bar}")
    
    # Find peaks (local maxima)
    print("\n" + "=" * 70)
    print("DIFFRACTION PEAKS")
    print("=" * 70)
    
    peaks = []
    for i in range(1, len(pattern) - 1):
        if pattern[i][1] > pattern[i-1][1] and pattern[i][1] > pattern[i+1][1]:
            if pattern[i][1] > max_intensity * 0.1:  # Significant peaks
                peaks.append(pattern[i])
    
    peaks.sort(key=lambda x: -x[1])
    
    print(f"\n{'Angle':<10}{'Intensity':<15}{'Rel. Intensity':<15}")
    print("-" * 40)
    
    for angle, intensity, _, _ in peaks[:15]:
        norm = intensity / max_intensity
        print(f"{angle:>6.1f}°    {intensity:>10.1f}    {norm:>6.3f}")
    
    # Check if peak angles relate to golden angle or Fibonacci
    print("\n" + "=" * 70)
    print("PEAK ANGLES vs SPECIAL NUMBERS")
    print("=" * 70)
    
    golden_angle_deg = math.degrees(GOLDEN_ANGLE)
    print(f"\nGolden angle: {golden_angle_deg:.2f}°")
    print(f"360/phi: {360/PHI:.2f}°")
    print(f"360/phi^2: {360/(PHI**2):.2f}°")
    
    for angle, intensity, _, _ in peaks[:10]:
        # Check ratios
        ratio_golden = angle / golden_angle_deg
        ratio_fib = None
        
        # Check if angle is near a Fibonacci multiple of something
        fibs = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        for f in fibs:
            if abs(angle - f * 10) < 5:  # Within 5 degrees of F*10
                ratio_fib = f
                break
            if abs(angle - f) < 2:
                ratio_fib = f
                break
        
        fib_note = f"near {ratio_fib}×10°" if ratio_fib else ""
        print(f"  {angle:>6.1f}°: angle/golden = {ratio_golden:.2f}  {fib_note}")
    
    # Wavelength scan
    print("\n" + "=" * 70)
    print("WAVELENGTH SCAN - RESONANCES")
    print("=" * 70)
    
    print("\nScanning wavelengths for forward scattering intensity...")
    print(f"\n{'Lambda':<10}{'Forward I':<15}{'Backward I':<15}{'Ratio':<10}")
    print("-" * 50)
    
    resonances = []
    
    for lam_inv in range(1, 21):  # lambda from 1 to 0.05
        lam = 1.0 / (lam_inv * 0.5)  # wavelength
        k_mag = 2 * math.pi / lam
        k_vec = (0, 0, k_mag)
        
        pattern = compute_diffraction(primes, N, k_vec, num_angles=36)
        
        forward = pattern[0][1]   # theta = 0
        backward = pattern[-1][1]  # theta = 180
        ratio = forward / backward if backward > 0 else float('inf')
        
        resonances.append((lam, forward, backward, ratio))
        print(f"{lam:>8.3f}    {forward:>10.1f}    {backward:>10.1f}    {ratio:>8.2f}")
    
    # Find resonance peaks
    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print("""
DIFFRACTION FROM PRIME SCATTERERS:

1. FORWARD SCATTERING (0°):
   - Constructive interference when primes align with wavefront
   - Maximum intensity at wavelengths matching prime spacing

2. PEAK ANGLES:
   - Diffraction peaks at specific angles
   - May relate to golden angle or Fibonacci structure

3. WAVELENGTH RESONANCES:
   - Certain wavelengths scatter more strongly
   - Resonances could reveal characteristic prime scales

4. PHYSICAL ANALOGY:
   - Primes as atoms in a "number crystal"
   - Diffraction reveals the "lattice structure" of primes
   - Golden spiral creates quasi-periodic arrangement
""")

    # Compare to random scatterers
    print("\n" + "=" * 70)
    print("COMPARISON: PRIMES vs RANDOM SCATTERERS")
    print("=" * 70)
    
    import random
    random.seed(42)
    
    # Random points same density as primes
    num_primes = len([p for p in primes if p <= N])
    random_points = random.sample(range(2, N+1), num_primes)
    
    k_vec = (0, 0, 2 * math.pi)
    
    # Prime pattern
    prime_pattern = compute_diffraction(primes, N, k_vec, num_angles=180)
    prime_max = max(p[1] for p in prime_pattern)
    prime_angles = [p[0] for p in prime_pattern if p[1] > 0.5 * prime_max]
    
    # Random pattern
    random_pattern = compute_diffraction(set(random_points), N, k_vec, num_angles=180)
    random_max = max(p[1] for p in random_pattern)
    random_angles = [p[0] for p in random_pattern if p[1] > 0.5 * random_max]
    
    print(f"\nPrime scatterers: {len(prime_angles)} angles with >50% max intensity")
    print(f"Random scatterers: {len(random_angles)} angles with >50% max intensity")
    
    print(f"\nPrime max intensity: {prime_max:.1f}")
    print(f"Random max intensity: {random_max:.1f}")
    print(f"Ratio (prime/random): {prime_max/random_max:.2f}")
    
    # Variance in pattern
    prime_intensities = [p[1] for p in prime_pattern]
    random_intensities = [p[1] for p in random_pattern]
    
    prime_var = sum((x - sum(prime_intensities)/len(prime_intensities))**2 for x in prime_intensities) / len(prime_intensities)
    random_var = sum((x - sum(random_intensities)/len(random_intensities))**2 for x in random_intensities) / len(random_intensities)
    
    print(f"\nPrime pattern variance: {prime_var:.1f}")
    print(f"Random pattern variance: {random_var:.1f}")
    print(f"Ratio: {prime_var/random_var:.2f}")
    
    if prime_var > random_var:
        print("\n→ Primes create MORE structured diffraction than random!")
    else:
        print("\n→ Prime diffraction similar to random")

if __name__ == "__main__":
    analyze_diffraction()
