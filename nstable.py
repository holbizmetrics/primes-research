import math
def primes(n):
    s=[True]*(n+1);s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i):s[j]=False
    return set(i for i,v in enumerate(s) if v)
def bs(nums,N,t,wl,R=0.5):
    k=2*math.pi*wl;ar=ai=0;c=0
    for n in nums:
        r=n/N
        if r<0.01:continue
        c+=1;rn=r**(1-2*t)*R**(2*t);z=1-2*rn;ph=2*k*z
        ar+=math.cos(ph);ai+=math.sin(ph)
    return(ar*ar+ai*ai)/(c*c)if c else 0

print('=== PRIME coherence peaks across N ===')
for N in[200,500,1000,2000]:
    ps=primes(N);P=[n for n in range(2,N+1)if n in ps]
    for lam in[9,21,35]:
        bt=bv=0
        for ti in range(10,490):
            t=ti/1000;bp=bs(P,N,t,lam)
            if bp>bv:bv=bp;bt=t
        near=''
        for nm,v in[('1/4',.25),('1/3',1/3),('2/7',2/7),('1/6',1/6),('2/9',2/9)]:
            if abs(bt-v)<0.012:near=nm
        print(f'N={N:5d} L={lam:2d}: t={bt:.3f} coh={bv:.6f} {near}')
    print()

print('=== COMPOSITE coherence peaks across N ===')
for N in[200,500,1000,2000]:
    ps=primes(N);C=[n for n in range(4,N+1)if n not in ps]
    for lam in[9,21,35]:
        bt=bv=0
        for ti in range(10,490):
            t=ti/1000;bc=bs(C,N,t,lam)
            if bc>bv:bv=bc;bt=t
        near=''
        for nm,v in[('1/4',.25),('1/3',1/3),('2/7',2/7),('1/6',1/6),('2/9',2/9)]:
            if abs(bt-v)<0.012:near=nm
        print(f'N={N:5d} L={lam:2d}: t={bt:.3f} coh={bv:.6f} {near}')
    print()

# Now: P/C ratio measured at FIXED t values (the claimed Brennpunkts)
print('=== P/C at FIXED t across N (is the ratio N-stable?) ===')
for t_fixed in [0.25, 1/3, 2/7]:
    print(f'\nt = {t_fixed:.4f}:')
    for N in[200,500,1000,2000,5000]:
        ps=primes(N)
        P=[n for n in range(2,N+1)if n in ps]
        C=[n for n in range(4,N+1)if n not in ps]
        for lam in[9,21,35]:
            bp=bs(P,N,t_fixed,lam)
            bc=bs(C,N,t_fixed,lam)
            r=bp/bc if bc>1e-12 else 0
            print(f'  N={N:5d} L={lam:2d}: P={bp:.6f} C={bc:.6f} P/C={r:>8.1f}')
