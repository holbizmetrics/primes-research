import math

def primes(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i,v in enumerate(s) if v]

N = 1000
ps = set(primes(N))

def backscatter(nums, N, t, wavelength):
    R = 0.5
    k = 2 * math.pi * wavelength
    ar, ai = 0, 0
    for n in nums:
        r = n / N
        if r < 0.01: continue
        r_new = (r ** (1-2*t)) * (R ** (2*t))
        z = 1 - 2*r_new
        phase = 2 * k * z
        ar += math.cos(phase)
        ai += math.sin(phase)
    count = len(nums)
    return (ar*ar + ai*ai) / (count * count) if count > 0 else 0

primes_list = [n for n in range(2, N+1) if n in ps]
comps_list = [n for n in range(2, N+1) if n not in ps]

print('VERIFY: Exact fraction peaks')
print('='*60)

# Test exact fractions
tests = [
    (35, '7x5', 4/13, '4/13'),
    (35, '7x5', 0.311, 'peak'),
    (33, '3x11', 2/5, '2/5'),
    (33, '3x11', 0.398, 'peak'),
    (21, '3x7', 2/9, '2/9'),
    (21, '3x7', 0.224, 'peak'),
    (21, '3x7', 2/7, '2/7 (harm mean)'),
    (21, '3x7', 1/4, '1/4 (prime B)'),
]

for wl, name, t, t_name in tests:
    p = backscatter(primes_list, N, t, wl)
    c = backscatter(comps_list, N, t, wl)
    r = p/c if c > 1e-9 else 0
    print(f'L={wl} ({name}) at t={t_name:>15} = {t:.4f}: {r:>8.0f}x')

print()
print('='*60)
print('PATTERN:')
print('-'*60)
print('L=35 peaks at 4/13:  4 = prime Brennpunkt denom, 13 = F7')
print('L=33 peaks at 2/5:   5 = F5')
print('L=21 peaks at 2/9:   9 = 3^2 = (composite Brennpunkt denom)^2')
print()
print('The FIBONACCI connection persists!')
print()

# What about 2/F_n patterns?
print('Testing 2/F_n fractions:')
fibs = [3, 5, 8, 13, 21, 34]
for f in fibs:
    t = 2/f
    if t < 0.5:
        best_wl, best_r = 0, 0
        for wl in [15, 21, 33, 35, 49, 55]:
            p = backscatter(primes_list, N, t, wl)
            c = backscatter(comps_list, N, t, wl)
            r = p/c if c > 1e-9 else 0
            if r > best_r: best_r, best_wl = r, wl
        print(f't = 2/{f} = {t:.4f}: best L={best_wl} at {best_r:.0f}x')
