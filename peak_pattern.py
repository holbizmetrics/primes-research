import math

def primes(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i,v in enumerate(s) if v]

N = 1000
ps = set(primes(N))

def backscatter(nums, N, t, wl):
    R = 0.5
    k = 2 * math.pi * wl
    ar, ai = 0, 0
    for n in nums:
        r = n / N
        if r < 0.01: continue
        r_new = (r ** (1-2*t)) * (R ** (2*t))
        z = 1 - 2*r_new
        ar += math.cos(2*k*z)
        ai += math.sin(2*k*z)
    count = len(nums)
    return (ar*ar + ai*ai) / (count * count) if count > 0 else 0

P = [n for n in range(2, N+1) if n in ps]
C = [n for n in range(2, N+1) if n not in ps]

print('PEAK PATTERN SEARCH')
print('='*60)
print()

# Find peaks for many wavelengths
results = []
for wl in range(10, 100, 5):
    best_t, best_r = 0, 0
    for t_int in range(10, 450):
        t = t_int / 1000
        p = backscatter(P, N, t, wl)
        c = backscatter(C, N, t, wl)
        r = p/c if c > 1e-9 else 0
        if r > best_r: best_r, best_t = r, t
    if best_r > 100:
        results.append((wl, best_t, best_r))

print(f'{"L":>4} | {"peak t":>8} | {"ratio":>10} | t*L')
print('-'*45)
for wl, t, r in sorted(results, key=lambda x: -x[2])[:15]:
    product = t * wl
    print(f'{wl:>4} | {t:>8.4f} | {r:>8.0f}x | {product:.2f}')

print()
print('='*60)
print('LOOKING FOR t * L pattern...')
print()

# Check if t * L is constant or follows pattern
products = [t * wl for wl, t, r in results]
if products:
    avg = sum(products) / len(products)
    print(f'Average t * L = {avg:.2f}')
    print(f'Range: {min(products):.2f} to {max(products):.2f}')
