import math

# CORRECT implementation from the original JS
# Key: z = 1 - 2*rNew, phase = 2*k*z, k = 2*pi*wavelength
phi = (1+math.sqrt(5))/2
ga = 2*math.pi/phi**2

def is_prime(n):
    if n<2: return False
    if n<4: return True
    if n%2==0 or n%3==0: return False
    i=5
    while i*i<=n:
        if n%i==0 or n%(i+2)==0: return False
        i+=6
    return True

def bigomega(n):
    c=0;d=2
    while d*d<=n:
        while n%d==0: c+=1;n//=d
        d+=1
    if n>1: c+=1
    return c

def backscatter(nums, t, wavelength, R=0.5):
    """Correct backscatter from original JS"""
    k = 2 * math.pi * wavelength  # NOTE: k = 2pi*lam, not 2pi/lam
    ar = 0.; ai = 0.; N = len(nums)
    for n in nums:
        # Golden spiral 3D mapping
        r_orig = R * math.sqrt(n / 1000.0)  # radius
        # Apply Brennpunkt focusing
        rNew = r_orig**(1-2*t) * R**(2*t)
        # z from focused radius
        z = 1 - 2*rNew
        # Backscatter phase (factor 2 for round-trip)
        phase = 2 * k * z
        ar += math.cos(phase)
        ai += math.sin(phase)
    return (ar*ar + ai*ai) / (N*N) if N > 0 else 0

# Build number classes
primes = [n for n in range(2, 1001) if is_prime(n)]
comps = [n for n in range(4, 1001) if not is_prime(n)]
s2 = [n for n in range(4, 1001) if bigomega(n)==2]
s3 = [n for n in range(8, 1001) if bigomega(n)==3]
s4 = [n for n in range(16, 1001) if bigomega(n)==4]

print(f"#P={len(primes)} #C={len(comps)} #2ap={len(s2)} #3ap={len(s3)} #4ap={len(s4)}")

# Test at the documented champion wavelengths
for lam in [9, 21, 33, 35]:
    print(f"\nlam={lam}: t-scan P/C ratio")
    best_t, best_ratio = 0, 0
    for ti in range(5, 96):
        t = ti / 200.
        bp = backscatter(primes, t, lam)
        bc = backscatter(comps, t, lam)
        ratio = bp/bc if bc > 1e-12 else 0
        if ratio > best_ratio:
            best_ratio = ratio
            best_t = t
        if ti % 10 == 0:
            print(f"  t={t:.3f} P={bp:.6f} C={bc:.6f} P/C={ratio:.1f}")
    print(f"  ** PEAK: t={best_t:.3f} P/C={best_ratio:.1f}")

# Now test k-almost primes at lam=35 (champion)
print("\n=== k-Almost Primes at lam=35 ===")
for nm, v in [("Primes", primes), ("Semi", s2), ("3-almo", s3), ("4-almo", s4), ("Comps", comps)]:
    bt, br = 0, 0
    for ti in range(5, 96):
        t = ti/200.
        bv = backscatter(v, t, 35)
        ba = backscatter(comps, t, 35)
        rat = bv/ba if ba > 1e-12 else 0
        if rat > br: br = rat; bt = t
    print(f"  {nm:7s}: peak t={bt:.3f} ratio_vs_C={br:.2f}")
