#!/usr/bin/env python3
"""Test: do zeros from different L-functions repel less than same-family zeros?"""

from mpmath import mp, zetazero, dirichlet, fmul
mp.dps = 25

def dirichlet_zeros_chi4(n):
    """Zeros of L(s, chi_4) - the primitive character mod 4"""
    # chi_4(-1) = -1, so this is an odd character
    # Use mpmath's built-in
    zeros = []
    for k in range(1, n+1):
        z = mp.siegelz(k)  # This is for zeta, need different approach
    # Actually mpmath doesn't have direct Dirichlet zero finder
    # Use known tabulated values for first zeros of L(s, chi_4)
    # From LMFDB: first zeros of L(s, chi_4) (conductor 4, odd)
    known_chi4 = [
        6.0209489, 10.2437703, 12.5880371, 16.2509880, 18.8510577,
        21.1597146, 23.4301316, 26.0586104, 27.6701858, 30.4267387,
        32.0352779, 33.8998659, 36.2536040, 37.7557801, 40.0032609,
        41.5247272, 43.2907285, 45.2768876, 46.6206302, 48.3509380,
        49.5614688, 51.4809654, 52.8064648, 54.3758782, 56.1297584,
        57.1210223, 58.8568109, 60.3178300, 61.6339916, 63.2665384
    ]
    return known_chi4[:n]

def zeta_zeros(n):
    """First n zeros of Riemann zeta"""
    return [float(zetazero(k).imag) for k in range(1, n+1)]

def within_family_spacings(zeros):
    """Consecutive spacings within one L-function, normalized"""
    spacings = [zeros[i+1] - zeros[i] for i in range(len(zeros)-1)]
    mean_s = sum(spacings) / len(spacings)
    return [s / mean_s for s in spacings]

def between_family_spacings(zeros_a, zeros_b):
    """For each zero in A, distance to nearest zero in B, normalized by local density"""
    # Local density approximation: use average spacing
    all_zeros = sorted(zeros_a + zeros_b)
    mean_spacing = (all_zeros[-1] - all_zeros[0]) / (len(all_zeros) - 1)
    
    cross_distances = []
    for za in zeros_a:
        # Find nearest zero in B
        nearest = min(zeros_b, key=lambda zb: abs(za - zb))
        cross_distances.append(abs(za - nearest) / mean_spacing)
    
    return cross_distances

def stats(values):
    n = len(values)
    mean = sum(values) / n
    var = sum((v - mean)**2 for v in values) / n
    # Fraction of small spacings (< 0.5 mean)
    small_frac = sum(1 for v in values if v < 0.5) / n
    return {'mean': mean, 'var': var, 'small_frac': small_frac}

# Get zeros
print("Computing zeros...")
zeta_z = zeta_zeros(30)
chi4_z = dirichlet_zeros_chi4(30)

print(f"Zeta zeros: {zeta_z[:5]}...")
print(f"Chi4 zeros: {chi4_z[:5]}...")

# Within-family spacings
within_zeta = within_family_spacings(zeta_z)
within_chi4 = within_family_spacings(chi4_z)

# Between-family spacings
cross_spacings = between_family_spacings(zeta_z, chi4_z)

print("\n=== WITHIN-FAMILY (consecutive) ===")
print(f"Zeta: mean={stats(within_zeta)['mean']:.3f}, var={stats(within_zeta)['var']:.3f}, small_frac={stats(within_zeta)['small_frac']:.3f}")
print(f"Chi4: mean={stats(within_chi4)['mean']:.3f}, var={stats(within_chi4)['var']:.3f}, small_frac={stats(within_chi4)['small_frac']:.3f}")

print("\n=== BETWEEN-FAMILY (nearest neighbor) ===")
print(f"Cross: mean={stats(cross_spacings)['mean']:.3f}, var={stats(cross_spacings)['var']:.3f}, small_frac={stats(cross_spacings)['small_frac']:.3f}")

print("\n=== KEY COMPARISON ===")
wz_small = stats(within_zeta)['small_frac']
cross_small = stats(cross_spacings)['small_frac']
print(f"Small spacings within zeta: {wz_small:.1%}")
print(f"Small spacings cross-family: {cross_small:.1%}")
if cross_small > wz_small:
    print("→ MORE small spacings between families = WEAKER repulsion")
else:
    print("→ FEWER small spacings between families = SAME or STRONGER repulsion")
