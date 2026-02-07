import math, subprocess, sys

def K(x):
    return 1.0 if abs(x)<1e-14 else math.sin(math.pi*x)/(math.pi*x)

r = subprocess.run(['gp','-q'],
    input='Z=lfunzeros(1,600);for(i=1,#Z,printf("%.10f\\n",Z[i]))\n',
    capture_output=True, text=True, timeout=60)
zeros = [float(x) for x in r.stdout.strip().split('\n') if x.strip()]
nz = len(zeros)
print(f"{nz} zeros"); sys.stdout.flush()

def Ns(t): return t/(2*math.pi)*math.log(t/(2*math.pi*math.e))+7/8
U = [Ns(z) for z in zeros]

# Non-overlapping for independence
for L in [1.0, 2.0, 3.0, 5.0, 10.0, 15.0, 20.0]:
    nn=min(30,max(15,int(8*L))); dx=L/nn
    p2=0
    for a in range(nn):
        for b in range(nn):
            p2 += K((a-b)*dx)**2*dx**2
    k2g = L-p2

    vals=[]
    x=U[0]
    while x+L<=U[-1]:
        cnt=sum(1 for u in U if x<=u<x+L)
        vals.append(float(cnt)); x+=L
    nw=len(vals)
    if nw<5: continue
    mu=sum(vals)/nw
    d=[v-mu for v in vals]
    v2=sum(x**2 for x in d)/nw
    v3=sum(x**3 for x in d)/nw
    sk=v3/v2**1.5 if v2>1e-6 else 0
    print(f"L={L:5.1f} nw={nw:4d} var_z={v2:.4f} var_G={k2g:.4f} excess={v2-k2g:+.4f} mu3={v3:+.5f} skew={sk:+.3f}")
    sys.stdout.flush()

print("\nDone")
