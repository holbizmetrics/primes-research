"""Experiment 4: Ramanujan residual analysis — what's in the 0.4%?"""
import math
from math import gcd

def sieve(n):
    s=[True]*(n+1);s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i):s[j]=False
    return set(i for i,v in enumerate(s) if v)

def euler_totient(n):
    result = n
    p = 2
    temp = n
    while p*p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

def bs_direct(nums, N, wl):
    """Direct phase backscatter (Ramanujan axis, t=0, no Brennpunkt)"""
    k=2*math.pi*wl; ar=ai=0; c=0
    for n in nums:
        r=n/N
        if r<0.01: continue
        c+=1
        z = 1 - 2*r
        ph = 2*k*z
        ar+=math.cos(ph); ai+=math.sin(ph)
    return (ar*ar+ai*ai)/(c*c) if c else 0

def mobius(n):
    """Mobius function"""
    if n == 1: return 1
    factors = 0; d = 2; temp = n
    while d*d <= temp:
        if temp % d == 0:
            temp //= d
            factors += 1
            if temp % d == 0: return 0  # not squarefree
        d += 1
    if temp > 1: factors += 1
    return (-1)**factors

def omega(n):
    """Number of distinct prime factors"""
    c = 0; d = 2; temp = n
    while d*d <= temp:
        if temp % d == 0:
            c += 1
            while temp % d == 0: temp //= d
        d += 1
    if temp > 1: c += 1
    return c

N = 1000
ps = sieve(N)
P = [n for n in range(2,N+1) if n in ps]
n_primes = len(P)

print('=== Ramanujan Law: pEnh = N_pi / phi(lam)^2 ===')
print(f'N={N}, N_pi={n_primes}')
print()

# Compute pEnh for many wavelengths
results = []
print(f'{"lam":>4} {"phi":>4} {"mu":>3} {"omega":>3} {"pEnh":>8} {"predicted":>10} {"residual":>10} {"rel_err":>8}')
print('-'*65)

for lam in range(2, 100):
    phi_lam = euler_totient(lam)
    mu_lam = mobius(lam)
    om_lam = omega(lam)

    bp = bs_direct(P, N, lam)
    # Random baseline: uniform integers have ~0 coherence at large k
    # Use all integers as baseline
    all_nums = list(range(2, N+1))
    ba = bs_direct(all_nums, N, lam)

    if ba < 1e-15: continue

    penh = bp / ba
    predicted = n_primes / (phi_lam * phi_lam)
    residual = penh - predicted
    rel_err = residual / predicted if predicted > 0 else 0

    results.append((lam, phi_lam, mu_lam, om_lam, penh, predicted, residual, rel_err))

    if lam <= 40 or lam in [42, 60, 66, 70, 78, 90]:
        print(f'{lam:>4} {phi_lam:>4} {mu_lam:>3} {om_lam:>3} {penh:>8.3f} {predicted:>10.3f} {residual:>10.3f} {rel_err:>8.3f}')

print()

# Analyze residuals
residuals = [(lam, res, rel, mu, om) for lam, phi, mu, om, penh, pred, res, rel in results if abs(pred) > 0.01]

# Group by mobius
print('=== Residual by Mobius function ===')
for mu_val in [1, -1, 0]:
    group = [(lam, res, rel) for lam, res, rel, mu, om in residuals if mu == mu_val]
    if group:
        avg_rel = sum(r for _,_,r in group) / len(group)
        print(f'  mu={mu_val:>2}: n={len(group):>2}, avg rel_error={avg_rel:.4f}')

print()

# Group by omega (number of distinct prime factors)
print('=== Residual by omega (distinct prime factors) ===')
for om_val in range(1, 5):
    group = [(lam, res, rel) for lam, res, rel, mu, om in residuals if om == om_val]
    if group:
        avg_rel = sum(r for _,_,r in group) / len(group)
        std_rel = math.sqrt(sum((r-avg_rel)**2 for _,_,r in group)/len(group)) if len(group)>1 else 0
        print(f'  omega={om_val}: n={len(group):>2}, avg rel_error={avg_rel:.4f} +/- {std_rel:.4f}')

print()

# Check if residual correlates with lambda itself
print('=== Residual vs lambda (linear correlation) ===')
lams = [r[0] for r in residuals]
rels = [r[2] for r in residuals]
n_r = len(lams)
mean_l = sum(lams)/n_r
mean_r = sum(rels)/n_r
cov = sum((l-mean_l)*(r-mean_r) for l,r in zip(lams, rels))/n_r
var_l = sum((l-mean_l)**2 for l in lams)/n_r
var_r = sum((r-mean_r)**2 for r in rels)/n_r
corr = cov/math.sqrt(var_l*var_r) if var_l*var_r > 0 else 0
print(f'  Pearson r(lambda, rel_error) = {corr:.4f}')

# Check against 1/lambda
inv_lams = [1/l for l in lams]
mean_il = sum(inv_lams)/n_r
cov2 = sum((il-mean_il)*(r-mean_r) for il,r in zip(inv_lams, rels))/n_r
var_il = sum((il-mean_il)**2 for il in inv_lams)/n_r
corr2 = cov2/math.sqrt(var_il*var_r) if var_il*var_r > 0 else 0
print(f'  Pearson r(1/lambda, rel_error) = {corr2:.4f}')

# Check against log(lambda)
log_lams = [math.log(l) for l in lams]
mean_ll = sum(log_lams)/n_r
cov3 = sum((ll-mean_ll)*(r-mean_r) for ll,r in zip(log_lams, rels))/n_r
var_ll = sum((ll-mean_ll)**2 for ll in log_lams)/n_r
corr3 = cov3/math.sqrt(var_ll*var_r) if var_ll*var_r > 0 else 0
print(f'  Pearson r(ln(lambda), rel_error) = {corr3:.4f}')

print()

# N-stability of the Ramanujan law
print('=== N-stability of Ramanujan law ===')
for N2 in [200, 500, 1000, 2000, 5000]:
    ps2 = sieve(N2)
    P2 = [n for n in range(2,N2+1) if n in ps2]
    n_p = len(P2)
    all2 = list(range(2, N2+1))

    # Compute R^2 for Ramanujan law
    data = []
    for lam in range(2, min(N2//2, 100)):
        phi_l = euler_totient(lam)
        bp = bs_direct(P2, N2, lam)
        ba = bs_direct(all2, N2, lam)
        if ba < 1e-15: continue
        penh = bp/ba
        pred = n_p/(phi_l**2)
        data.append((penh, pred))

    if len(data) > 5:
        mean_obs = sum(d[0] for d in data)/len(data)
        ss_tot = sum((d[0]-mean_obs)**2 for d in data)
        ss_res = sum((d[0]-d[1])**2 for d in data)
        r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
        print(f'  N={N2:>5}: R^2 = {r2:.6f} (n={len(data)} wavelengths, N_pi={n_p})')
