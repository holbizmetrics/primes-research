import math
import subprocess

def K(x):
    if abs(x) < 1e-14:
        return 1.0
    return math.sin(math.pi * x) / (math.pi * x)

# Get zeta zeros
result = subprocess.run(
    ['gp', '-q'],
    input='Z=lfunzeros(1,300);for(i=1,#Z,printf("%.10f\\n",Z[i]))\n',
    capture_output=True, text=True, timeout=30
)
zeros = [float(x) for x in result.stdout.strip().split('\n') if x.strip()]
nz = len(zeros)
print(f"Got {nz} zeros up to T=300")

# Unfolding
def Nsmooth(t):
    return t / (2*math.pi) * math.log(t / (2*math.pi*math.e)) + 7.0/8.0

U = [Nsmooth(z) for z in zeros]

# Check unfolding quality: spacings should have mean 1
spacings = [U[i+1] - U[i] for i in range(nz-1)]
mean_sp = sum(spacings) / len(spacings)
var_sp = sum((s - mean_sp)**2 for s in spacings) / len(spacings)
print(f"Unfolded spacings: mean={mean_sp:.4f} var={var_sp:.4f}")
print(f"GUE spacing var should be ~ 0.286")
print(f"Unfolded range: [{U[0]:.2f}, {U[-1]:.2f}]")
print()

# The issue: for counting N([x,x+L]), we should use DISJOINT intervals
# to get independent samples
# With 138 zeros over ~138 units, for L=5 we get ~27 independent windows

print("=== NON-OVERLAPPING windows ===")
print(f"{'L':>5} {'nwin':>5} {'mean':>7} {'var':>8} {'mu3':>10} {'skew':>7}")

for L in [0.5, 1.0, 2.0, 3.0, 5.0, 10.0]:
    # Place disjoint windows
    vals = []
    x = U[0]
    while x + L <= U[-1]:
        cnt = sum(1 for u in U if x <= u < x + L)
        vals.append(float(cnt))
        x += L

    nw = len(vals)
    if nw < 5:
        print(f"L={L:4.1f} {nw:5d}  (too few windows)")
        continue

    mu = sum(vals) / nw
    d = [v - mu for v in vals]
    v2 = sum(x**2 for x in d) / nw
    v3 = sum(x**3 for x in d) / nw
    skew = v3 / v2**1.5 if v2 > 1e-6 else 0.0
    print(f"L={L:4.1f} {nw:5d} {mu:7.3f} {v2:8.4f} {v3:+10.5f} {skew:+7.3f}")

# Now the REAL question: use SLIDING windows but correct for correlation
# Actually, let's think about this differently.
# The GUE prediction for kappa3 should be compared to
# the THIRD CUMULANT of the counting function.
#
# For N([0,L]) in GUE:
#   kappa_1 = L
#   kappa_2 = Sigma_2(L) = L - int K^2
#   kappa_3 = 2 * int K K K  (the connected 3-point function integrated)
#
# Wait - the 3rd cumulant formula for determinantal processes is:
# kappa_3 = 2 * int_{[0,L]^3} K(x1-x2)*K(x2-x3)*K(x3-x1) dx1 dx2 dx3
#
# But actually for GUE, the CLUSTER functions are:
# T_1(x) = K(x,x) = 1 (density)
# T_2(x,y) = -K(x,y)^2 (pair correlation connected part is -K^2)
# T_3(x,y,z) = 2*K(x,y)*K(y,z)*K(z,x) (3-point connected)
#
# And kappa_n = integral of T_n over [0,L]^n
# So kappa_2 = -int K^2 (note the minus sign!) => Sigma2 = L + kappa_2 = L - int K^2  ✓
# And kappa_3 = 2*int K*K*K  ✓
#
# For the variance, GUE gives ~0.28-0.50 depending on L
# But we measured var ~ 0.25 for the zeta data!
# This is actually LESS than Poisson (var=L for Poisson) and LESS than GUE
#
# Wait, that means zeta zeros are MORE rigid than GUE? That's wrong.
# Actually for L small (L<1), the count is 0 or 1, so var = p(1-p) where p ~ L
# For L=0.5: mean~1.06 (so ~1 zero per half-unit), var=0.055 is plausible
# For L=1.0: mean~1.54, can be 1 or 2, var=0.248 ~ 0.25 = p(1-p) for p=0.5
#
# Actually I think the unfolded variance IS matching GUE for small L.
# Let me check: GUE Sigma2(L) for small L:
# Sigma2(L) = L - int_0^L int_0^L sinc(x-y)^2 dx dy

print("\n=== Careful GUE vs Zeta comparison ===")
print("Using OVERLAPPING windows but computing properly")
print()

# Let's compute with more zeros. Get up to T=1000
result2 = subprocess.run(
    ['gp', '-q'],
    input='Z=lfunzeros(1,600);for(i=1,#Z,printf("%.10f\\n",Z[i]))\n',
    capture_output=True, text=True, timeout=60
)
zeros2 = [float(x) for x in result2.stdout.strip().split('\n') if x.strip()]
nz2 = len(zeros2)
print(f"Got {nz2} zeros up to T=600")

U2 = [Nsmooth(z) for z in zeros2]
spacings2 = [U2[i+1] - U2[i] for i in range(nz2-1)]
mean_sp2 = sum(spacings2) / len(spacings2)
print(f"Unfolded spacings mean = {mean_sp2:.4f}")
print()

# NON-OVERLAPPING for better statistics
print(f"{'L':>5} {'nwin':>5} {'mean':>7} {'var_z':>8} {'mu3_z':>10} {'skew_z':>7} | {'var_G':>8} {'k3_G':>10}")
for L in [0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0]:
    # GUE predictions
    nn = min(30, max(10, int(5*L)))
    dx = L / nn
    s2g = 0.0
    for a in range(nn):
        xa = (a + 0.5) * dx
        for b in range(nn):
            xb = (b + 0.5) * dx
            s2g += K(xa - xb)**2 * dx**2
    k2g = L - s2g

    # kappa3 only for small L (triple integral too expensive for large L)
    if L <= 5:
        nn3 = min(20, max(8, int(4*L)))
        dx3 = L / nn3
        s3g = 0.0
        for a in range(nn3):
            xa = (a + 0.5) * dx3
            for b in range(nn3):
                xb = (b + 0.5) * dx3
                kab = K(xa - xb)
                for c in range(nn3):
                    xc = (c + 0.5) * dx3
                    s3g += 2 * kab * K(xb - xc) * K(xa - xc) * dx3**3
        k3g = s3g
    else:
        k3g = float('nan')

    # Zeta: non-overlapping
    vals = []
    x = U2[0]
    while x + L <= U2[-1]:
        cnt = sum(1 for u in U2 if x <= u < x + L)
        vals.append(float(cnt))
        x += L

    nw = len(vals)
    if nw < 5:
        continue

    mu = sum(vals) / nw
    d = [v - mu for v in vals]
    v2 = sum(x**2 for x in d) / nw
    v3 = sum(x**3 for x in d) / nw
    skew = v3 / v2**1.5 if v2 > 1e-6 else 0.0

    k3s = f"{k3g:+10.4f}" if not math.isnan(k3g) else "    N/A   "
    print(f"L={L:4.1f} {nw:5d} {mu:7.3f} {v2:8.4f} {v3:+10.5f} {skew:+7.3f} | {k2g:8.4f} {k3s}")
