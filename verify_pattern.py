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
print("VERIFY: L=12 at exact t=1/6")
for t,name in[(1/6,'1/6'),(0.170,'peak'),(1/4,'1/4'),(1/3,'1/3')]:
    p=bs(P,t,12);c=bs(C,t,12);r=p/c if c>1e-9 else 0
    print(f"L=12 at t={name}: {r:.0f}x")
print()
print("VERIFY: L=9 at exact t=1/4")
for t,name in[(1/4,'1/4'),(0.250,'peak'),(1/3,'1/3'),(2/9,'2/9')]:
    p=bs(P,t,9);c=bs(C,t,9);r=p/c if c>1e-9 else 0
    print(f"L=9 at t={name}: {r:.0f}x")
print()
print("PATTERN CHECK:")
print("="*50)
tests=[(9,'3^2',1/4,'1/4'),(12,'4x3',1/6,'1/6'),(21,'3x7',2/7,'2/7'),
       (35,'5x7',3/7,'3/7'),(33,'3x11',2/5,'2/5')]
for wl,fact,t,tname in tests:
    p=bs(P,t,wl);c=bs(C,t,wl);r=p/c if c>1e-9 else 0
    print(f"L={wl:>2} ({fact:>4}) at t={tname}: {r:>6.0f}x")
