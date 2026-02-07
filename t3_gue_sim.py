import math, random
random.seed(42)

def randn():
    u1 = random.random()
    u2 = random.random()
    return math.sqrt(-2*math.log(u1+1e-15))*math.cos(2*math.pi*u2)

def gue_eigenvalues_2x2():
    """2x2 GUE: eigenvalues of [[a,c],[c*,b]] where a,b~N(0,1), c~N(0,1/2)+iN(0,1/2)"""
    a = randn()
    b = randn()
    c_re = randn()/math.sqrt(2)
    c_im = randn()/math.sqrt(2)
    c2 = c_re**2 + c_im**2
    tr = a+b
    det = a*b - c2
    disc = tr**2 - 4*det
    if disc < 0: disc = 0
    sq = math.sqrt(disc)
    return [(tr-sq)/2, (tr+sq)/2]

def gue_eigenvalues_NxN(N):
    """NxN GOE (real symmetric for simplicity) eigenvalues"""
    # Build real symmetric matrix with N(0,1) diagonal and N(0,1/sqrt(2)) off-diag
    H = [[0.0]*N for _ in range(N)]
    for i in range(N):
        H[i][i] = randn()
        for j in range(i+1, N):
            v = randn()/math.sqrt(2)
            H[i][j] = v
            H[j][i] = v

    # Power iteration for eigenvalues... too slow. Use Jacobi for small N.
    # Actually let's use the tridiagonal reduction via Householder
    # For N<=10, can use direct characteristic polynomial or QR
    # Simplest: use numpy-like eigenvalue via iterative method
    # But we don't have numpy. Let's use the beta-ensemble trick:
    # GUE eigenvalues via tridiagonal model (Dumitriu-Edelman):
    # diagonal: N(0, sqrt(2)) entries
    # sub-diagonal: chi_{beta*(N-1)}, chi_{beta*(N-2)}, ..., chi_{beta*1}  with beta=2 for GUE
    # chi_k has density x^{k-1}*exp(-x^2/2)*2/Gamma(k/2)
    # chi_k = sqrt(sum of k standard normals squared)

    # Actually that gives a tridiagonal matrix whose eigenvalues = GUE eigenvalues
    # Let's implement this for GUE (beta=2)
    pass

def chi(k):
    """Sample from chi distribution with k degrees of freedom"""
    return math.sqrt(sum(randn()**2 for _ in range(k)))

def gue_tridiag(N, beta=2):
    """Tridiagonal beta-ensemble (Dumitriu-Edelman 2002)
    Returns eigenvalues of tridiag matrix with:
      diagonal: N(0, sqrt(2))
      subdiagonal: chi_{beta*(N-1)}/sqrt(2), chi_{beta*(N-2)}/sqrt(2), ...
    Eigenvalues have joint density proportional to prod|ei-ej|^beta * exp(-sum ei^2/4)
    """
    diag = [randn()*math.sqrt(2) for _ in range(N)]
    subdiag = [chi(beta*(N-i))/math.sqrt(2) for i in range(1, N)]

    # QR algorithm for tridiagonal symmetric matrix eigenvalues
    # Use implicit QR shifts
    return tridiag_eigenvalues(diag, subdiag)

def tridiag_eigenvalues(d, e, max_iter=100):
    """Eigenvalues of symmetric tridiagonal matrix.
    d = diagonal, e = sub/super-diagonal.
    Uses QL algorithm with implicit shifts."""
    n = len(d)
    d = [float(x) for x in d]
    e = [float(x) for x in e] + [0.0]

    for l in range(n):
        itr = 0
        while True:
            m = l
            while m < n-1:
                dd = abs(d[m]) + abs(d[m+1])
                if abs(e[m]) + dd == dd:
                    break
                m += 1
            if m == l:
                break
            itr += 1
            if itr > max_iter:
                break

            g = (d[l+1] - d[l]) / (2*e[l])
            r = math.sqrt(g*g + 1)
            g = d[m] - d[l] + e[l] / (g + (r if g >= 0 else -r))
            s = 1.0
            c = 1.0
            p = 0.0

            for i in range(m-1, l-1, -1):
                f = s * e[i]
                b = c * e[i]
                if abs(f) >= abs(g):
                    c = g / f
                    r = math.sqrt(c*c + 1)
                    e[i+1] = f * r
                    s = 1.0 / r
                    c *= s
                else:
                    s = f / g
                    r = math.sqrt(s*s + 1)
                    e[i+1] = g * r
                    c = 1.0 / r
                    s *= c

                g = d[i+1] - p
                r = (d[i] - g) * s + 2 * c * b
                p = s * r
                d[i+1] = g + p
                g = c * r - b

            d[l] -= p
            e[l] = g
            e[m] = 0.0

    return sorted(d)

# Test: GUE 10x10, 5000 trials, collect spacings and count statistics
print("=== GUE simulation via tridiagonal model ===")
N = 10
trials = 3000
all_spacings = []
count_L1 = []
count_L2 = []

for trial in range(trials):
    evals = gue_tridiag(N, beta=2)
    # Rescale: bulk density at 0 is rho = sqrt(2N)/(2*pi) * sqrt(1 - (x/2sqrt(N))^2)
    # At center: rho(0) = sqrt(2N)/(2*pi) = sqrt(20)/(2*pi) = 4.47/6.28 = 0.712
    # Mean spacing at center = 1/rho = 1.405
    # Unfold by multiplying by rho to get unit mean spacing
    rho0 = math.sqrt(2*N)/(2*math.pi)

    # Take middle eigenvalues only (bulk statistics)
    mid = N//2
    bulk = evals[mid-3:mid+4]  # 7 central eigenvalues
    # Unfold
    u = [x * rho0 for x in bulk]
    sp = [u[i+1]-u[i] for i in range(len(u)-1)]
    all_spacings.extend(sp)

    # Count in windows of length 1/rho0 (which maps to L=1 after unfolding)
    # Actually: after unfolding, place windows at unfolded positions
    # The unfolded positions have mean spacing 1
    for i in range(len(u)-1):
        x0 = u[i]
        cnt = sum(1 for ux in u if x0 <= ux < x0+1.0)
        count_L1.append(cnt)

# Spacing statistics
mean_sp = sum(all_spacings)/len(all_spacings)
var_sp = sum((s-mean_sp)**2 for s in all_spacings)/len(all_spacings)
print(f"Spacings: n={len(all_spacings)} mean={mean_sp:.4f} var={var_sp:.4f}")

# Count statistics L=1
mean_c = sum(count_L1)/len(count_L1)
d_c = [c-mean_c for c in count_L1]
var_c = sum(x**2 for x in d_c)/len(d_c)
mu3_c = sum(x**3 for x in d_c)/len(d_c)
skew_c = mu3_c/var_c**1.5 if var_c > 1e-6 else 0
print(f"\nCount(L=1): n={len(count_L1)} mean={mean_c:.4f} var={var_c:.4f} mu3={mu3_c:.5f} skew={skew_c:.4f}")

from collections import Counter
cc = Counter(count_L1)
total = sum(cc.values())
print("Distribution:")
for k in sorted(cc.keys()):
    print(f"  N=={k}: {cc[k]} ({100*cc[k]/total:.1f}%)")

# Compare to zeta
print(f"\nGUE theory: kappa2(L=1) = 0.344, kappa3(L=1) = 0.979, skewness = 4.85")
print(f"GUE simulation: var = {var_c:.4f}, mu3 = {mu3_c:.5f}, skewness = {skew_c:.4f}")
print(f"Zeta data: var = 0.628, mu3 ~ 0, skewness ~ 0")
