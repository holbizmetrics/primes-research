#!/usr/bin/env python3
"""3D geometry + multiplicative probes, part A"""
import math
PHI=(1+math.sqrt(5))/2; GA=2*math.pi/PHI**2; N=2000
def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(2,n+1) if s[i]]
def mangoldt(n):
    if n<2: return 0
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]:
        if t==1: break
        k=0
        while t%p==0: t//=p; k+=1
        if k>0 and t==1: return math.log(p)
    if t>1: return math.log(n)
    return 0
P=sieve(N); NP=len(P); Pset=set(P)
LAM={}
for n in range(2,N+1):
    l=mangoldt(n)
    if l>0: LAM[n]=l
zeros=[14.1347,21.0220,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738]

def gsphere(n):
    theta=n*GA; z=1-2*n/N; r=math.sqrt(max(0,1-z*z))
    return (r*math.cos(theta),r*math.sin(theta),z)

print("=== STRIKE 1: Multiplicative laser on different position functions ===")
print("F(t) = |sum Lambda(n) n^{-1/2} exp(-i*t*f(n))|^2")
print()
def Fgeom(t, pfunc):
    ar=ai=0.0
    for n,lam in LAM.items():
        phase=-t*pfunc(n); w=lam/math.sqrt(n)
        ar+=w*math.cos(phase); ai+=w*math.sin(phase)
    return ar**2+ai**2

print("At gamma_1=14.13:")
print("  f(n)=log(n):  F=%.1f  (THE RIGHT ONE)" % Fgeom(14.13, lambda n: math.log(n)))
print("  f(n)=z_gold:  F=%.1f  (golden sphere z)" % Fgeom(14.13, lambda n: gsphere(n)[2]))
print("  f(n)=n:       F=%.1f  (linear)" % Fgeom(14.13, lambda n: float(n)))
print("  f(n)=sqrt(n): F=%.1f  (square root)" % Fgeom(14.13, lambda n: math.sqrt(n)))
print()
print("At gamma_2=21.02:")
print("  f(n)=log(n):  F=%.1f" % Fgeom(21.02, lambda n: math.log(n)))
print("  f(n)=z_gold:  F=%.1f" % Fgeom(21.02, lambda n: gsphere(n)[2]))
print("  f(n)=n:       F=%.1f" % Fgeom(21.02, lambda n: float(n)))
print()

print("=== STRIKE 2: Cross-coherence between zeros ===")
def A_log(t):
    ar=ai=0.0
    for n,lam in LAM.items():
        phase=-t*math.log(n); w=lam/math.sqrt(n)
        ar+=w*math.cos(phase); ai+=w*math.sin(phase)
    return complex(ar,ai)

nz=min(8,len(zeros))
Az=[A_log(zeros[k]) for k in range(nz)]
print("Cross-coherence cos(angle) between zero amplitudes:")
print("     ",end="")
for j in range(nz): print(" g%d  " % (j+1),end="")
print()
for i in range(nz):
    print("g%d " % (i+1),end="")
    for j in range(nz):
        cross=(Az[i]*Az[j].conjugate()).real
        norm=abs(Az[i])*abs(Az[j])
        c=cross/norm if norm>1e-10 else 0
        print(" %+.2f" % c,end="")
    print()
# Test factorization
print()
triples=[]
for i in range(nz):
    for j in range(i+1,nz):
        for k in range(j+1,nz):
            c_ij=(Az[i]*Az[j].conjugate()).real/(abs(Az[i])*abs(Az[j]))
            c_ik=(Az[i]*Az[k].conjugate()).real/(abs(Az[i])*abs(Az[k]))
            c_jk=(Az[j]*Az[k].conjugate()).real/(abs(Az[j])*abs(Az[k]))
            if abs(c_jk)>0.1: triples.append(c_ij*c_ik/c_jk)
if triples:
    m=sum(triples)/len(triples)
    v=sum((r-m)**2 for r in triples)/len(triples)
    cv=math.sqrt(v)/abs(m) if abs(m)>1e-10 else 999
    print("Factorization test: CV=%.2f (%s)" % (cv, "FACTORIZES" if cv<0.3 else "DOES NOT FACTORIZE"))
    print("(Additive comb had CV~0 = perfect factorization)")
