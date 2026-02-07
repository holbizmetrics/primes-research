import math
PHI = (1 + math.sqrt(5)) / 2
GA = 2 * math.pi / (PHI * PHI)

def primes(n):
    s = [True] * (n + 1); s[0] = s[1] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            for j in range(i*i, n + 1, i): s[j] = False
    return [i for i in range(n + 1) if s[i]]

def comps(n, ps): return [i for i in range(4, n+1) if i not in set(ps)]

def verts(nv):
    v = []
    for i in range(nv):
        t = GA * i; z = 1 - (2*i+1)/nv; r = math.sqrt(max(0,1-z*z))
        v.append((r*math.cos(t), r*math.sin(t), z))
    return v

def scatter(nums, N, wl, vs):
    k = 2*math.pi/wl; ar, ai = 0, 0; c = 0
    for n in nums:
        if n > N: continue
        c += 1
        t = GA * n; z = 1 - 2*n/N; z = max(-0.99, min(0.99, z))
        rx = math.sqrt(1-z*z); x, y = rx*math.cos(t), rx*math.sin(t)
        ds = sorted([(x*v[0]+y*v[1]+z*v[2], v) for v in vs], reverse=True)[:3]
        ws = [max(0,d[0])**2 for d in ds]; tot = sum(ws)
        if tot < 0.001: pz = z
        else: pz = sum(w*d[1][2] for w,d in zip(ws,ds))/tot
        ar += math.cos(2*k*pz); ai += math.sin(2*k*pz)
    return (ar*ar+ai*ai)/(c*c) if c else 0

N = 1000; ps = primes(N); cs = comps(N, ps)
print("N-HEDRON: Optimal sphere approximation")
print("="*55)
print()
print("Your insight: It's not the sphere itself,")
print("it's the APPROXIMATION level that matters!")
print()

best = (0, 0, 0)
fibs = [3,5,8,13,21,34,55,89,144]

for nv in [3,4,5,6,7,8,10,12,13,20,21,30,34,42,50,55,89,144,233]:
    vs = verts(nv)
    br, bw = 0, 0
    for d in [3,5,8,13,21,34,55]:
        p = scatter(ps, N, 1/d, vs)
        c = scatter(cs, N, 1/d, vs)
        r = p/c if c > 1e-9 else 0
        if r > br: br, bw = r, d
    if br > best[1]: best = (nv, br, bw)
    f = "*" if nv in fibs else " "
    m = " <<<" if br > 400 else (" <<" if br > 100 else "")
    print(f"n={nv:>3}{f}: {br:>8.1f}x at λ=1/{bw}{m}")

print()
print("="*55)
print(f"BEST: n = {best[0]} vertices → {best[1]:.0f}× at λ=1/{best[2]}")
print()

if best[0] in fibs:
    idx = fibs.index(best[0])
    print(f"n = {best[0]} = F_{idx+4} (Fibonacci!)")
print()
print("Fine scan around optimum:")
print("-"*40)
for nv in range(max(3, best[0]-3), best[0]+4):
    vs = verts(nv)
    br, bw = 0, 0
    for d in [3,5,8,13,21,34,55]:
        p = scatter(ps, N, 1/d, vs)
        c = scatter(cs, N, 1/d, vs)
        r = p/c if c > 1e-9 else 0
        if r > br: br, bw = r, d
    f = "*" if nv in fibs else " "
    print(f"  n={nv:>3}{f}: {br:>8.1f}x")
