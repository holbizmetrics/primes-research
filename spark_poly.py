#!/usr/bin/env python3
"""SPARK: Polyhedra + Laser + Inversion
STRIKE 1-2: Vertex count as wavelength / Platonic solid resonance
"""
import math

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(2,n+1) if s[i]]

def laser(values, lam, N):
    """Coherence |Σ exp(2πi*v/λ)|²/n²"""
    ar=ai=0
    for v in values:
        ph = 2*math.pi*v/lam
        ar += math.cos(ph); ai += math.sin(ph)
    n = len(values)
    return (ar*ar+ai*ai)/(n*n) if n>0 else 0

N = 5000
P = sieve(N)
C = [i for i in range(4, N+1) if not any(i==p for p in P) and i>1]
# faster: use set
Pset = set(P)
C = [i for i in range(2, N+1) if i not in Pset]

print("=== STRIKE 1-2: Platonic solid vertices as laser wavelength ===")
print("Hypothesis: vertex count = natural resonant wavelength")
print()

# Platonic solids: vertices, faces, edges, symmetry group order
platonic = {
    'Tetrahedron':  {'V':4,  'E':6,  'F':4,  'sym':12,  'dual':'Tetrahedron'},
    'Cube':         {'V':8,  'E':12, 'F':6,  'sym':24,  'dual':'Octahedron'},
    'Octahedron':   {'V':6,  'E':12, 'F':8,  'sym':24,  'dual':'Cube'},
    'Dodecahedron': {'V':20, 'E':30, 'F':12, 'sym':60,  'dual':'Icosahedron'},
    'Icosahedron':  {'V':12, 'E':30, 'F':20, 'sym':60,  'dual':'Dodecahedron'},
}

print(f"{'Solid':<15} {'V':>3} {'F':>3} {'|sym|':>5} | {'I_P(V)':>8} {'I_C(V)':>8} {'P/C':>6} | {'I_P(F)':>8} {'I_C(F)':>8} {'P/C':>6} | {'I_P(sym)':>8} {'I_C(sym)':>8} {'P/C':>6}")
print("-"*130)

for name, d in platonic.items():
    # Probe at λ = V (vertices)
    ip_v = laser(P, d['V'], N)
    ic_v = laser(C, d['V'], N)
    pc_v = ip_v/ic_v if ic_v > 1e-10 else float('inf')

    # Probe at λ = F (faces)
    ip_f = laser(P, d['F'], N)
    ic_f = laser(C, d['F'], N)
    pc_f = ip_f/ic_f if ic_f > 1e-10 else float('inf')

    # Probe at λ = |sym| (symmetry group order)
    ip_s = laser(P, d['sym'], N)
    ic_s = laser(C, d['sym'], N)
    pc_s = ip_s/ic_s if ic_s > 1e-10 else float('inf')

    print(f"{name:<15} {d['V']:3d} {d['F']:3d} {d['sym']:5d} | {ip_v:8.5f} {ic_v:8.5f} {pc_v:6.1f} | {ip_f:8.5f} {ic_f:8.5f} {pc_f:6.1f} | {ip_s:8.5f} {ic_s:8.5f} {pc_s:6.1f}")

# Also check: which are squarefree (Ramanujan prediction: glow iff squarefree)
print("\n=== Ramanujan check: squarefree iff glow ===")
def mobius(n):
    if n==1: return 1
    factors = []
    d = 2
    temp = n
    while d*d <= temp:
        if temp%d==0:
            factors.append(d)
            temp//=d
            if temp%d==0: return 0  # squared factor
        d+=1
    if temp>1: factors.append(temp)
    return (-1)**len(factors)

def euler_phi(n):
    result = n
    d = 2
    temp = n
    while d*d <= temp:
        if temp%d==0:
            while temp%d==0: temp//=d
            result -= result//d
        d+=1
    if temp>1: result -= result//temp
    return result

print(f"{'lambda':>6} {'mu(l)':>5} {'phi(l)':>6} {'mu²/phi²':>8} {'I_P':>8} {'I_C':>8} {'P/C':>6} {'predict':>8}")
for lam in [4, 6, 8, 12, 20, 24, 60]:
    mu = mobius(lam)
    phi = euler_phi(lam)
    pred = mu*mu/(phi*phi) if phi > 0 else 0
    ip = laser(P, lam, N)
    ic = laser(C, lam, N)
    pc = ip/ic if ic>1e-10 else float('inf')
    sqfree = "sqfree" if mu != 0 else "NOT_sqf"
    print(f"{lam:6d} {mu:5d} {phi:6d} {pred:8.5f} {ip:8.5f} {ic:8.5f} {pc:6.1f} {sqfree:>8}")
