import math
PHI = (1 + math.sqrt(5)) / 2
GA = 2 * math.pi / (PHI * PHI)

def sieve(n):
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            for j in range(i*i, n + 1, i): s[j] = False
    return set(i for i in range(n + 1) if s[i])

def bs(nums, N, t, lam, R=0.5):
    k = 2 * math.pi * lam
    ar, ai = 0.0, 0.0
    for n in nums:
        r_o = max(n/N, 1e-10)
        r_t = r_o**(1-2*t) * R**(2*t)
        z_u = max(-1, min(1, 1 - 2*n/N))
        phase = 2 * k * r_t * z_u
        ar += math.cos(phase)
        ai += math.sin(phase)
    c = len(nums)
    return (ar*ar + ai*ai) / (c*c) if c > 0 else 0

N = 500
pset = sieve(N)
P = sorted(pset)
C = [n for n in range(4, N+1) if n not in pset]

print('=== Optimal t per wavelength (max P/C ratio) ===')
for lam in [3,5,8,9,12,13,21,33,35]:
    bt, br = 0, 0
    for i in range(400):
        t = 0.01 + 0.48*i/399
        bp = bs(P, N, t, lam)
        bc = bs(C, N, t, lam)
        r = bp/bc if bc > 1e-10 else 0
        if r > br and r < 1e6:
            br, bt = r, t
    near = ''
    for nm, v in [('1/4',.25),('1/3',1/3),('2/7',2/7),('3/8',.375),('2/5',.4),('2/9',2/9),('1/6',1/6)]:
        if abs(bt - v) < 0.015:
            near = nm
    print(f'lam={lam:>3}: t={bt:.3f} {near:>6}  ratio={br:.1f}x')

print()
print('=== lambda=8 detail ===')
for i in range(31):
    t = 0.15 + 0.01*i
    bp = bs(P, N, t, 8)
    bc = bs(C, N, t, 8)
    r = bp/bc if bc > 1e-10 else 0
    m = ' <-1/4' if abs(t-.25) < .006 else (' <-1/3' if abs(t-1/3) < .006 else '')
    print(f'  t={t:.2f} P/C={r:>7.1f}{m}')

print()
print('=== lambda=21 detail ===')
for i in range(31):
    t = 0.15 + 0.01*i
    bp = bs(P, N, t, 21)
    bc = bs(C, N, t, 21)
    r = bp/bc if bc > 1e-10 else 0
    m = ' <-1/4' if abs(t-.25) < .006 else (' <-1/3' if abs(t-1/3) < .006 else (' <-2/9' if abs(t-2/9) < .006 else ''))
    print(f'  t={t:.2f} P/C={r:>7.1f}{m}')

print()
print('=== PRIME-ONLY backscatter peak (not P/C ratio) ===')
for lam in [8, 21]:
    bt, bv = 0, 0
    for i in range(400):
        t = 0.01 + 0.48*i/399
        bp = bs(P, N, t, lam)
        if bp > bv:
            bv, bt = bp, t
    near = ''
    for nm, v in [('1/4',.25),('1/3',1/3),('2/7',2/7),('3/8',.375),('2/5',.4)]:
        if abs(bt - v) < 0.015:
            near = nm
    print(f'lam={lam}: prime peak at t={bt:.3f} {near:>6} val={bv:.5f}')

    bt2, bv2 = 0, 0
    for i in range(400):
        t = 0.01 + 0.48*i/399
        bc = bs(C, N, t, lam)
        if bc > bv2:
            bv2, bt2 = bc, t
    near2 = ''
    for nm, v in [('1/4',.25),('1/3',1/3),('2/7',2/7),('3/8',.375),('2/5',.4)]:
        if abs(bt2 - v) < 0.015:
            near2 = nm
    print(f'lam={lam}: comp peak at t={bt2:.3f} {near2:>6} val={bv2:.5f}')
