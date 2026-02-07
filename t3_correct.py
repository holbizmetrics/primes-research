import math, subprocess
from collections import Counter

def K(x):
    return 1.0 if abs(x)<1e-14 else math.sin(math.pi*x)/(math.pi*x)

# Correct formula: kappa_3 = Tr(K_I^3) = int int int K(x-y)*K(y-z)*K(z-x) dx dy dz
# (NO factor of 2)
# kappa_2 = Tr(K_I) - Tr(K_I^2) = L - int int K(x-y)^2 dx dy
print("=== Correct GUE cumulants: kappa_k = (-1)^{k+1} * Tr(K^k) ===")
print("Wait: for determinantal processes, the cumulant-trace relation is:")
print("  kappa_1 = Tr(K) = L")
print("  kappa_2 = Tr(K) - Tr(K^2) = L - int K^2")
print("  kappa_3 = Tr(K) - 3*Tr(K^2) + 2*Tr(K^3)")
print()
print("Actually, for the number of points N_I = sum_i 1_{x_i in I}:")
print("The cumulant generating function log E[exp(s*N_I)] = sum_k kappa_k * s^k/k!")
print("For DPP: log E[exp(s*N_I)] = Tr(log(I + (e^s-1)*K_I))")
print("        = sum_k Tr(K_I^k) * (-1)^{k+1} * (e^s-1)^k / k")
print("This is NOT the same as saying kappa_k = Tr(K^k).")
print()
print("The correct relation via Newton's identity / cumulant-moment:")
print("  kappa_1 = p_1 = L")
print("  kappa_2 = p_1 - p_2  (where p_k = Tr(K^k))")
print("  kappa_3 = p_1 - 3*p_2 + 2*p_3")
print("  kappa_4 = p_1 - 7*p_2 + 12*p_3 - 6*p_4")
print()

# Actually, the correct formula for DPP cumulants is:
# kappa_k = sum over partitions of [k] into cycles...
# For Bernoulli random variables X_i (indicators of points):
# N = sum X_i, and X_i are pairwise NOT independent
# For DPP: cumulants of N_I are given by:
# kappa_k = sum_{j=1}^{k} (-1)^{j-1} * (j-1)! * S(k,j) * Tr(K_I^j) ??? No
#
# Actually the simplest derivation: for DPP with kernel K,
# E[z^{N_I}] = det(I + (z-1)*K_I)
# log E[z^{N_I}] = log det(I + (z-1)*K_I) = Tr log(I + (z-1)*K_I)
#                = sum_{j=1}^inf (-1)^{j-1}/j * (z-1)^j * Tr(K_I^j)
#
# The cumulant generating function is log E[e^{tN}] = Tr log(I + (e^t - 1)*K_I)
# Let w = e^t - 1, then:
# CGF = sum_{j>=1} (-1)^{j+1}/j * w^j * Tr(K^j)
#
# Since w = e^t - 1 = t + t^2/2 + t^3/6 + ...
# w^j = t^j + j*t^{j+1}/2 + ...
#
# kappa_k = coefficient of t^k/k! in CGF
# Let's compute for k=1,2,3:
# CGF = Tr(K)*(e^t-1) - Tr(K^2)/2*(e^t-1)^2 + Tr(K^3)/3*(e^t-1)^3 - ...
#
# (e^t-1) = t + t^2/2 + t^3/6 + ...
# (e^t-1)^2 = t^2 + t^3 + 7t^4/12 + ...
# (e^t-1)^3 = t^3 + 3t^4/2 + ...
#
# Coefficient of t in CGF: Tr(K)*1 = p1
# => kappa_1 = p1 = L  ✓
#
# Coefficient of t^2 in CGF: Tr(K)*1/2 - Tr(K^2)/2*1 = (p1 - p2)/2
# => kappa_2 = (p1 - p2) = L - Tr(K^2)  ✓ (this is Sigma2)
#
# Coefficient of t^3 in CGF: Tr(K)*1/6 - Tr(K^2)/2*1 + Tr(K^3)/3*1
# = p1/6 - p2/2 + p3/3
# => kappa_3 = 3!*(p1/6 - p2/2 + p3/3) = p1 - 3*p2 + 2*p3  ✓

# Now compute:
for L in [0.5, 1.0, 2.0, 3.0, 5.0]:
    nn = 30
    dx = L/nn
    # p1 = Tr(K) = integral of K(x,x) = integral of 1 = L
    p1 = L

    # p2 = Tr(K^2) = int int K(x,y)^2 dx dy
    p2 = 0.0
    for a in range(nn):
        xa = (a+0.5)*dx
        for b in range(nn):
            xb = (b+0.5)*dx
            p2 += K(xa-xb)**2 * dx**2

    # p3 = Tr(K^3) = int int int K(x,y)*K(y,z)*K(z,x) dx dy dz
    nn3 = min(25, nn)
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

    k1 = p1
    k2 = p1 - p2  # = Sigma2(L)
    k3 = p1 - 3*p2 + 2*p3

    sigma = math.sqrt(k2) if k2 > 0 else 0
    skew = k3/k2**1.5 if k2 > 1e-6 else 0

    print(f"L={L:.1f}: p1={p1:.4f} p2={p2:.4f} p3={p3:.4f}")
    print(f"       k2={k2:.5f} k3={k3:+.6f} skew={skew:+.4f}")

# Get zeta zeros and compare
print("\n=== Zeta zero comparison ===")
r = subprocess.run(['gp','-q'], input='Z=lfunzeros(1,300);for(i=1,#Z,printf("%.10f\\n",Z[i]))\n',
                    capture_output=True, text=True, timeout=30)
zeros = [float(x) for x in r.stdout.strip().split('\n') if x.strip()]
nz = len(zeros)
def Ns(t): return t/(2*math.pi)*math.log(t/(2*math.pi*math.e))+7/8
U = [Ns(z) for z in zeros]

for L in [1.0, 2.0, 3.0, 5.0]:
    vals = []
    x = U[0]
    while x+L <= U[-1]:
        cnt = sum(1 for u in U if x<=u<x+L)
        vals.append(float(cnt))
        x += L
    nw = len(vals)
    if nw < 5: continue
    mu = sum(vals)/nw
    d = [v-mu for v in vals]
    v2 = sum(x**2 for x in d)/nw
    v3 = sum(x**3 for x in d)/nw
    sk = v3/v2**1.5 if v2>1e-6 else 0
    print(f"L={L:.0f}: nw={nw} var={v2:.4f} mu3={v3:+.6f} skew={sk:+.4f}")
