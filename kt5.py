import math
phi=(1+math.sqrt(5))/2; ga=2*math.pi/phi**2; R=1.0
def ip(n):
    if n<2: return False
    if n<4: return True
    if n%2==0 or n%3==0: return False
    i=5
    while i*i<=n:
        if n%i==0 or n%(i+2)==0: return False
        i+=6
    return True
def bo(n):
    c=0;d=2
    while d*d<=n:
        while n%d==0: c+=1;n//=d
        d+=1
    if n>1: c+=1
    return c
def bc(v,t,lam):
    N=len(v);re=0.;im=0.;k=2*math.pi/lam
    for n in v:
        r=math.sqrt(n);lat=math.asin(((n*phi)%1)*2-1);z=r*math.sin(lat)
        rf=r**(1-2*t)*R**(2*t);sc=rf/r if r>1e-6 else 1
        re+=math.cos(k*z*sc);im+=math.sin(k*z*sc)
    return(re**2+im**2)/N**2
pr=[n for n in range(2,501) if ip(n)]
co=[n for n in range(4,501) if not ip(n)]
s2=[n for n in range(4,501) if bo(n)==2]
s3=[n for n in range(8,501) if bo(n)==3]
for lam in [8,21]:
    for nm,v in [('P',pr),('2ap',s2),('3ap',s3)]:
        bt=0;br=0
        for ti in range(30,85):
            t=ti/200.;cv=bc(v,t,lam);cc=bc(co,t,lam);rat=cv/cc if cc>1e-10 else 0
            if rat>br: br=rat;bt=t
        print(f'lam={lam} {nm:3s} t={bt:.3f} ratio={br:.1f}')
