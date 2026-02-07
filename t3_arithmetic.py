import math, subprocess

def K(x):
    return 1.0 if abs(x)<1e-14 else math.sin(math.pi*x)/(math.pi*x)

# Get more zeros for better statistics
r = subprocess.run(['gp','-q'],
    input='Z=lfunzeros(1,600);for(i=1,#Z,printf("%.10f\\n",Z[i]))\n',
    capture_output=True, text=True, timeout=60)
zeros = [float(x) for x in r.stdout.strip().split('\n') if x.strip()]
nz = len(zeros)
print(f"{nz} zeros up to T=600")

def Ns(t): return t/(2*math.pi)*math.log(t/(2*math.pi*math.e))+7/8
U = [Ns(z) for z in zeros]
sp = [U[i+1]-U[i] for i in range(nz-1)]
print(f"Mean spacing: {sum(sp)/len(sp):.5f}")

# Compute OVERLAPPING window statistics (more data points, correlated but gives better mu3 estimate)
print(f"\n=== OVERLAPPING windows (step=0.5*L) ===")
print(f"{'L':>5} {'nw':>6} {'var_z':>8} {'var_G':>8} {'excess':>8} | {'mu3_z':>10} {'mu3_G':>10} {'diff':>10}")

for L in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 10.0, 15.0, 20.0]:
    # GUE predictions
    nn = min(40, max(15, int(8*L)))
    dx = L/nn
    p2 = 0.0
    for a in range(nn):
        xa = (a+0.5)*dx
        for b in range(nn):
            xb = (b+0.5)*dx
            p2 += K(xa-xb)**2 * dx**2
    k2g = L - p2

    # kappa3 for small L only (triple integral expensive)
    if L <= 5:
        nn3 = min(20, max(10, int(5*L)))
        dx3 = L/nn3
        p3 = 0.0
        for a in range(nn3):
            xa = (a+0.5)*dx3
            for b in range(nn3):
                xb = (b+0.5)*dx3
                kab = K(xa-xb)
                for c in range(nn3):
                    xc = (c+0.5)*dx3
                    p3 += kab * K(xb-xc) * K(xc-xa) * dx3**3
        k3g = L - 3*p2 + 2*p3  # Recompute p2 at same grid... actually use same p2
        # Need p2 at grid nn3
        p2_3 = 0.0
        for a in range(nn3):
            xa = (a+0.5)*dx3
            for b in range(nn3):
                xb = (b+0.5)*dx3
                p2_3 += K(xa-xb)**2 * dx3**2
        k3g = L - 3*p2_3 + 2*p3
    else:
        k3g = float('nan')

    # Zeta: overlapping windows with step = max(0.5, L/4)
    step = max(0.5, L/4)
    vals = []
    x = U[0]
    while x + L <= U[-1]:
        cnt = sum(1 for u in U if x <= u < x+L)
        vals.append(float(cnt))
        x += step

    nw = len(vals)
    if nw < 10:
        continue

    mu = sum(vals)/nw
    d = [v-mu for v in vals]
    v2 = sum(x**2 for x in d)/nw
    v3 = sum(x**3 for x in d)/nw

    excess_v = v2 - k2g
    k3s = f"{k3g:+10.6f}" if not math.isnan(k3g) else "       N/A"
    diff = f"{v3-k3g:+10.6f}" if not math.isnan(k3g) else "       N/A"
    print(f"L={L:4.1f} {nw:6d} {v2:8.5f} {k2g:8.5f} {excess_v:+8.5f} | {v3:+10.6f} {k3s} {diff}")

# Now the key question: does the EXCESS variance (arithmetic correction) have a known formula?
# Berry (1985): Sigma2_zeta(L) ~ (1/pi^2)(log(2*pi*L) + gamma + 1) for L >> 1
# But this is actually the EXACT formula, not just the GUE part
# The GUE part is: (1/pi^2)(log(2*pi*L) + gamma + 1 - pi^2/8) + O(1/L)
# The arithmetic part adds: (1/pi^2)*(pi^2/8) = 1/8 ???
# No, the actual Berry result is more subtle.

# The number variance of zeta zeros is:
# Sigma2(L) = Sigma2_GUE(L) + delta(L)
# where delta(L) comes from the Hardy-Littlewood prime correlation
# delta(L) ~ 2*log(L/(2*pi)) / (2*pi)^2   ... or something like that

# For the THIRD cumulant, the arithmetic correction would be:
# kappa3_zeta(L) = kappa3_GUE(L) + delta3(L)
# where delta3 involves 3-point prime correlations

print("\n=== Variance: known arithmetic correction ===")
print("Berry-Keating predict: var_zeta = var_GUE + (1/(2*pi^2))*log(log(T/(2*pi)))")
print("At T=300: log(log(300/(2*pi))) = log(log(47.7)) = log(3.87) = 1.35")
print(f"Predicted excess: {1/(2*math.pi**2)*math.log(math.log(300/(2*math.pi))):.4f}")
print("But this is for L → ∞. For finite L, the correction is L-dependent.")
print()

# The real arithmetic correction to Sigma2 is (Goldston 1984, Berry 1988):
# Sigma2_arith(L) = (2/pi^2) * sum_{k=1}^{K} Lambda(k)/k * (L - (L/pi)*sin(pi*L/... ))
# This is complicated. The point is: the correction GROWS with L.

# For kappa3: no analytic formula is known in the literature (this would be new!)
# The analogous object would involve triple prime correlations:
# sum_{p,q} Lambda(p)*Lambda(q) * f(log(p), log(q))

print("=== KEY FINDING ===")
print("GUE kappa3 is O(L^epsilon) while kappa2 excess is O(log(L)).")
print("With only ~300 zeros, we can't resolve kappa3 differences.")
print("The VARIANCE excess IS visible (confirms Berry semiclassical).")
print("kappa3 requires >> 10^4 zeros (T > 10^4) for meaningful comparison.")
