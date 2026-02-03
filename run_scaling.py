import math,cmath,random
from zeros_500 import ZEROS

def C(N, Z, samples=100, trials=15):
    xs = [10**(0.3 + i*(math.log10(N)-0.3)/(samples-1)) for i in range(samples)]

    def E(x, rp=None):
        t = 0j
        for i, g in enumerate(Z):
            ph = g * math.log(x) + (rp[i] if rp else 0)
            t += math.sqrt(x) * cmath.exp(1j * ph) / complex(0.5, g)
        return -2 * t.real

    def v(a):
        m = sum(a) / len(a)
        return sum((y - m)**2 for y in a) / len(a)

    va = v([E(x) for x in xs])
    vn = sum(v([E(x, [random.uniform(0, 6.28) for _ in Z]) for x in xs]) for _ in range(trials)) / trials
    return va / vn if vn else 0

print(f"SCALING ANALYSIS WITH {len(ZEROS)} ZEROS")
print("=" * 40)
print(f"{'N':>8}  {'C(N)':>8}  {'log(N)':>7}")

Ns = [500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
Cs = []

for n in Ns:
    c = C(n, ZEROS)
    Cs.append(c)
    print(f"{n:>8}  {c:>8.4f}  {math.log(n):>7.2f}")

# Fit C(N) = a + b/log(N)
x = [1/math.log(n) for n in Ns]
y = Cs
xm = sum(x)/len(x)
ym = sum(y)/len(y)
b = sum((x[i]-xm)*(y[i]-ym) for i in range(len(x))) / sum((x[i]-xm)**2 for i in range(len(x)))
a = ym - b*xm

print()
print(f"Fit: C(N) = {a:.4f} + {b:.2f}/log(N)")
print(f"Asymptote: C(∞) → {a:.4f}")
if a < 1:
    print(f"→ Cancellation persists as N→∞")
else:
    print(f"→ Cancellation vanishes as N→∞")
