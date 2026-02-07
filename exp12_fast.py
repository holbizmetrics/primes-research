import math, random
random.seed(42)

def sieve(n):
    s=[True]*(n+1);s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i):s[j]=False
    return set(i for i,v in enumerate(s) if v)

N=1000; ps=sieve(N)
P=[n for n in range(2,N+1) if n in ps]
C=[n for n in range(4,N+1) if n not in ps]
R_set=sorted(random.sample(range(2,N+1),len(P)))

def bs(nums,N,t,wl,R=0.5,mode='geo'):
    k=2*math.pi*wl;ar=ai=0;c=0
    for n in nums:
        r=n/N
        if r<0.01:continue
        c+=1
        if mode=='geo':
            rn=r**(1-2*t)*R**(2*t)
        elif mode=='arith':
            rn=(1-t)*r+t*R
        elif mode=='harm':
            rn=1.0/((1-t)/r+t/R) if r>1e-10 else r
        elif mode=='quad':
            rn=math.sqrt((1-t)*r*r+t*R*R)
        elif mode=='repulsive':
            rn=r**(1+2*t)*R**(-2*t)
            rn=max(0.001,min(rn,10))
        else:
            rn=r
        z=1-2*rn;ph=2*k*z
        ar+=math.cos(ph);ai+=math.sin(ph)
    return(ar*ar+ai*ai)/(c*c)if c else 0

print('=== EXP 1: REPULSIVE BRENNPUNKT ===')
print('Small t, genuine prime glow (not composite cancellation)')
print(f'{"lam":>4} {"t":>6} {"P":>10} {"C":>10} {"Rand":>10} {"P/R":>7} {"P/C":>7}')
for lam in [6,10,30,35,59]:
    bt=bpe=0
    for ti in range(1,80):
        t=ti/1000
        bp=bs(P,N,t,lam,mode='repulsive')
        br=bs(R_set,N,t,lam,mode='repulsive')
        pe=bp/br if br>1e-12 else 0
        if pe>bpe and pe<1e6:
            bpe=pe;bt=t
    bp=bs(P,N,bt,lam,mode='repulsive')
    bc=bs(C,N,bt,lam,mode='repulsive')
    br=bs(R_set,N,bt,lam,mode='repulsive')
    pc=bp/bc if bc>1e-12 else 0
    print(f'{lam:>4} {bt:.3f} {bp:>10.6f} {bc:>10.6f} {br:>10.6f} {bpe:>7.1f}x {pc:>7.1f}x')

print()
print('=== EXP 2: POWER MEAN FAMILY ===')
print('Which focusing function gives strongest GENUINE signal?')
print(f'{"mode":>10} {"lam":>4} {"t":>6} {"P/R":>7} {"P/C":>7} {"P":>10} {"C":>10}')
for mode in ['geo','arith','harm','quad','repulsive']:
    for lam in [6,10,30,35]:
        bt=bpe=0
        for ti in range(5,400,2):
            t=ti/500
            bp=bs(P,N,t,lam,mode=mode)
            br=bs(R_set,N,t,lam,mode=mode)
            pe=bp/br if br>1e-12 else 0
            if pe>bpe and pe<1e6:bpe=pe;bt=t
        bp=bs(P,N,bt,lam,mode=mode)
        bc=bs(C,N,bt,lam,mode=mode)
        pc=bp/bc if bc>1e-12 else 0
        print(f'{mode:>10} {lam:>4} {bt:.3f} {bpe:>7.1f}x {pc:>7.1f}x {bp:>10.6f} {bc:>10.6f}')
    print()

# N-stability for the best results
print('=== N-STABILITY of top findings ===')
for N2 in [500,2000]:
    ps2=sieve(N2)
    P2=[n for n in range(2,N2+1) if n in ps2]
    C2=[n for n in range(4,N2+1) if n not in ps2]
    R2=sorted(random.sample(range(2,N2+1),len(P2)))
    for mode in ['harm','quad','repulsive']:
        for lam in [6,10,30]:
            bt=bpe=0
            for ti in range(5,400,3):
                t=ti/500
                bp=bs(P2,N2,t,lam,mode=mode)
                br=bs(R2,N2,t,lam,mode=mode)
                pe=bp/br if br>1e-12 else 0
                if pe>bpe and pe<1e6:bpe=pe;bt=t
            print(f'N={N2:5d} {mode:>10} L={lam:>2} t={bt:.3f} P/R={bpe:.1f}x')
