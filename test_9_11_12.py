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
print("Testing 9, 11, 12:")
for wl in[9,11,12,33,35,21]:
    bt,br=0,0
    for ti in range(10,490,5):
        t=ti/1000;p=bs(P,t,wl);c=bs(C,t,wl);r=p/c if c>1e-9 else 0
        if r>br:br,bt=r,t
    print(f"L={wl:>2}: peak t={bt:.3f} ratio={br:.0f}x")
