import math
def primes(n):
    s=[True]*(n+1);s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i):s[j]=False
    return set(i for i,v in enumerate(s) if v)
N=1000;ps=primes(N)
def bs(nums,t,wl):
    R,k,ar,ai=0.5,2*math.pi*wl,0,0
    for n in nums:
        r=n/N
        if r<0.01:continue
        rn=(r**(1-2*t))*(R**(2*t));z=1-2*rn
        ar+=math.cos(2*k*z);ai+=math.sin(2*k*z)
    c=len(nums)
    return(ar*ar+ai*ai)/(c*c)if c else 0
P=[n for n in range(2,N+1)if n in ps]
C=[n for n in range(2,N+1)if n not in ps]
print("ALL KEY WAVELENGTHS (including 11, 13, 17, 19):")
print("="*60)
for wl in[3,5,7,8,9,11,12,13,17,19,21,33,35,49]:
    bt,br=0,0
    for ti in range(5,495,2):
        t=ti/1000;p=bs(P,t,wl);c=bs(C,t,wl);r=p/c if c>1e-9 else 0
        if r>br:br,bt=r,t
    frac=""
    for d in range(2,20):
        for n in range(1,d):
            if abs(bt-n/d)<0.008:frac=f"~{n}/{d}"
    prime="P" if wl in ps else " "
    fib="F" if wl in[3,5,8,13,21,34,55,89] else " "
    print(f"L={wl:>2}{prime}{fib}: t={bt:.3f} {frac:>7} {br:>7.0f}x")
