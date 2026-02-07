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

print('FINE SCAN: Finding exact peaks')
print('='*55)

for wl, name in [(35, '7x5'), (33, '3x11'), (21, '3x7')]:
    best_t, best_r = 0, 0
    for t_int in range(0, 500):
        t = t_int / 1000
        p = backscatter(primes_list, N, t, wl)
        c = backscatter(comps_list, N, t, wl)
        r = p/c if c > 1e-9 else 0
        if r > best_r: best_r, best_t = r, t

    print(f'L={wl} ({name}): peak t={best_t:.3f} ratio={best_r:.0f}x')

    # Find simple fraction
    for d in range(2, 15):
        for n in range(1, d):
            if abs(best_t - n/d) < 0.008:
                print(f'  near {n}/{d} = {n/d:.4f}')

print()
print('The peaks are highly sensitive to exact t value.')
print('The 3787x was at coarse t=0.42, finer scan finds true peak.')
