import math
phi = (1+math.sqrt(5))/2; ga = 2*math.pi/phi**2; R = 1.0

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
        r=math.sqrt(n); th=n*ga
        lat=math.asin(((n*phi)%1)*2-1)
        z=r*math.sin(lat)
        rf=r**(1-2*t)*R**(2*t)
        sc=rf/r if r>1e-6 else 1
        re+=math.cos(k*z*sc); im+=math.sin(k*z*sc)
    return (re**2+im**2)/N**2

primes=[n for n in range(2,2001) if is_prime(n)]
s2=[n for n in range(4,2001) if bigomega(n)==2]
s3=[n for n in range(8,2001) if bigomega(n)==3]
s4=[n for n in range(16,2001) if bigomega(n)==4]
allnums=list(range(2,2001))

print(f"#P={len(primes)} #2ap={len(s2)} #3ap={len(s3)} #4ap={len(s4)}")

# For each class, find t where class/all ratio is maximized
# This is the "Brennpunkt" for that class
for lam in [8, 13, 21, 34]:
    print(f"\n=== lambda={lam} ===")
    for nm,v in [("Primes",primes),("2-almost",s2),("3-almost",s3),("4-almost",s4)]:
        best_t, best_ratio = 0, 0
        for ti in range(5, 190):
            t = ti/400.
            cv = bc(v, t, lam)
            ca = bc(allnums, t, lam)
            ratio = cv/ca if ca > 1e-10 else 0
            if ratio > best_ratio:
                best_ratio = ratio
                best_t = t
        print(f"  {nm:10s}: best t={best_t:.4f} (1/{1/best_t:.1f})  ratio={best_ratio:.3f}")
