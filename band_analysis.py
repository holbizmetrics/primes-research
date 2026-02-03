import math, cmath, random

ZEROS = [14.134725, 21.022039, 25.010857, 30.424876, 32.935061, 37.586178,
         40.918719, 43.327073, 48.005150, 49.773832, 52.970321, 56.446247,
         59.347044, 60.831778, 65.112544, 67.079810, 69.546401, 72.067157,
         75.704690, 77.144840, 79.337375, 82.910380, 84.735492, 87.425274,
         88.809111, 92.491899, 94.651344, 95.870634, 98.831194, 101.31785,
         103.72553, 105.44662, 107.16861, 111.02953, 111.87465, 114.32022,
         116.22668, 118.79078, 121.37012, 122.94682, 124.25681, 127.51668,
         129.57870, 131.08768, 133.49773, 134.75650, 138.11604, 139.73620,
         141.12370, 143.11184, 146.00098, 147.42276, 150.05352, 150.92525,
         153.02469, 156.11290, 157.59759, 158.84998, 161.18896, 163.03070,
         165.53706, 167.18443, 169.09451, 169.91197, 173.41153, 174.75419,
         176.44143, 178.37740, 179.91648, 182.20707, 184.87446, 185.59878,
         187.22892, 189.41615, 192.02665, 193.07972, 195.26539, 196.87648,
         198.01530, 201.26475, 202.49359, 204.18967, 205.39469, 207.90625,
         209.57650, 211.69086, 213.34791, 214.54704, 216.16953, 219.06759,
         220.71491, 221.43070, 224.00700, 224.98332, 227.42144, 229.33741,
         231.25018, 231.98723, 233.69340, 236.52422]

def E(x, zeros):
    s = math.sqrt(x); L = math.log(x); t = 0j
    for g in zeros: t += s * cmath.exp(1j*g*L) / complex(0.5,g)
    return -2*t.real

def En(x, zeros, rp):
    s = math.sqrt(x); L = math.log(x); t = 0j
    for i,g in enumerate(zeros): t += s * cmath.exp(1j*(g*L+rp[i])) / complex(0.5,g)
    return -2*t.real

def v(vals):
    m = sum(vals)/len(vals); return sum((x-m)**2 for x in vals)/len(vals)

def C(N, z, samples=200, trials=15):
    if not z: return float('nan'), 0, 0
    xs = [10**(math.log10(2)+i*(math.log10(N)-math.log10(2))/(samples-1)) for i in range(samples)]
    va = v([E(x,z) for x in xs])
    vn = sum(v([En(x,z,[random.uniform(0,6.28) for _ in z]) for x in xs]) for _ in range(trials))/trials
    return va/vn if vn>0 else 0, va, vn

b1=[g for g in ZEROS if g<50]
b2=[g for g in ZEROS if 50<=g<100]
b3=[g for g in ZEROS if 100<=g<150]
b4=[g for g in ZEROS if 150<=g<200]
b5=[g for g in ZEROS if g>=200]

N = 10000

print('='*60)
print('CROSS-BAND INTERACTION ANALYSIS')
print('='*60)
print()
print('Individual bands:')
for name, zeros in [('B1 (γ<50)',b1),('B2 (50-100)',b2),('B3 (100-150)',b3),('B4 (150-200)',b4),('B5 (>200)',b5)]:
    c,_,_ = C(N, zeros)
    status = 'CANCELS' if c < 1 else 'ANTI-CANCELS'
    print(f'  {name}: C={c:.3f} [{status}]')

print()
print('Cross-band combinations:')
good = sorted(b1+b3+b5)
bad = sorted(b2+b4)
c_good,_,_ = C(N, good)
c_bad,_,_ = C(N, bad)
c_all,_,_ = C(N, ZEROS)
print(f'  Good bands (B1+B3+B5): C = {c_good:.4f}')
print(f'  Bad bands (B2+B4):     C = {c_bad:.4f}')
print(f'  ALL combined:          C = {c_all:.4f}')

print()
print('Adjacent pair combinations:')
for name, zeros in [('B1+B2',b1+b2),('B2+B3',b2+b3),('B3+B4',b3+b4),('B4+B5',b4+b5)]:
    c,_,_ = C(N, sorted(zeros))
    print(f'  {name}: C = {c:.4f}')

print()
print('Non-adjacent pairs:')
for name, zeros in [('B1+B3',b1+b3),('B1+B5',b1+b5),('B2+B4',b2+b4),('B3+B5',b3+b5)]:
    c,_,_ = C(N, sorted(zeros))
    print(f'  {name}: C = {c:.4f}')

print()
print('='*60)
print('INTERPRETATION')
print('='*60)
if c_all < c_good and c_all < c_bad:
    print('Combined ALL is better than either good or bad groups alone!')
    print('=> CONSTRUCTIVE INTERFERENCE between groups')
elif c_all < c_bad:
    print('Good bands dominate when combined with bad bands')
    print('=> Good cancellation survives mixing')
