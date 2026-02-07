import math
phi = (1+math.sqrt(5))/2
ga = 2*math.pi/phi**2
R = 1.0

def is_prime(n):
    if n<2: return False
    if n<4: return True
    if n%2==0 or n%3==0: return False
    i=5
    while i*i<=n:
        if n%i==0 or n%(i+2)==0: return False
        i+=6
    return True

def bigomega(n):
    c=0; d=2
    while d*d<=n:
        while n%d==0: c+=1; n//=d
        d+=1
    if n>1: c+=1
    return c

def bc(nums, t, lam):
    N=len(nums); re=0.; im=0.; k=2*math.pi/lam
    for n in nums:
        r=math.sqrt(n)
        th=n*ga
        lat=math.asin(((n*phi)%1)*2-1)
        z=r*math.sin(lat)
        rf=r**(1-2*t)*R**(2*t)
        sc=rf/r if r>1e-6 else 1
        zf=z*sc
        re+=math.cos(k*zf); im+=math.sin(k*zf)
    return (re**2+im**2)/N**2

primes=[n for n in range(2,1001) if is_prime(n)]
comps=[n for n in range(4,1001) if not is_prime(n)]
s2=[n for n in range(4,1001) if bigomega(n)==2]
s3=[n for n in range(8,1001) if bigomega(n)==3]
s4=[n for n in range(16,1001) if bigomega(n)==4]
print(f"#P={len(primes)} #C={len(comps)} #2ap={len(s2)} #3ap={len(s3)} #4ap={len(s4)}")

for lam in [8, 21]:
    print(f"\n=== lambda={lam} ===")
    print(f"{'t':>5} {'P':>8} {'2ap':>8} {'3ap':>8} {'4ap':>8} {'P/C':>6}")
    for ti in range(2,20):
        t=ti*0.025
        cp=bc(primes,t,lam)
        cc=bc(comps,t,lam)
        c2=bc(s2,t,lam)
        c3=bc(s3,t,lam)
        c4=bc(s4,t,lam) if len(s4)>5 else 0
        print(f"{t:.3f} {cp:.6f} {c2:.6f} {c3:.6f} {c4:.6f} {cp/cc:.3f}")

# Fine peak search
print("\n=== Peak t for each class ===")
for lam in [8, 21]:
    for nm,v in [("Primes",primes),("2-almo",s2),("3-almo",s3),("4-almo",s4),("Comps",comps)]:
        if len(v)<5: continue
        bt,bv=0,0
        for ti in range(5,96):
            t=ti/200.
            c=bc(v,t,lam)
            if c>bv: bv=c; bt=t
        print(f"lam={lam:2d} {nm:7s}: peak t={bt:.3f} coh={bv:.6f}")
