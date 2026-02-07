#!/usr/bin/env python3
"""N-hedron sweep: Strikes 1-4 (additive laser)"""
import math, sys
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
def mobius(n):
    if n==1: return 1
    d=2;t=n;nf=0
    while d*d<=t:
        if t%d==0:
            nf+=1;t//=d
            if t%d==0: return 0
        d+=1
    if t>1: nf+=1
    return (-1)**nf
def euler_phi(n):
    r=n;d=2;t=n
    while d*d<=t:
        if t%d==0:
            while t%d==0: t//=d
            r-=r//d
        d+=1
    if t>1: r-=r//t
    return r

N=3000; P=sieve(N); NP=len(P)
LAM=[0.0]*(N+1)
for n in range(2,N+1): LAM[n]=mangoldt(n)
TL=sum(LAM)

results=[]
best_ip=0;best_iq=0;best_il=0;best_lq=0
print("=== N-HEDRON SWEEP q=2..200, N=%d ===" % N)
print("%4s %3s %4s %10s %10s %8s" % ("q","mu","phi","I_prime","I_Lambda","Lam/Pri"))
print("-"*50)
for q in range(2,201):
    ar=ai=0.0
    for p in P: ph=2*math.pi*p/q; ar+=math.cos(ph); ai+=math.sin(ph)
    ip=(ar**2+ai**2)/NP**2
    ar=ai=0.0
    for n in range(2,N+1):
        l=LAM[n]
        if l==0: continue
        ph=2*math.pi*n/q; ar+=l*math.cos(ph); ai+=l*math.sin(ph)
    il=(ar**2+ai**2)/TL**2
    mu=mobius(q);phi=euler_phi(q)
    ratio=il/ip if ip>1e-12 else 0
    results.append((q,mu,phi,ip,il,ratio))
    if ip>best_ip: best_ip=ip;best_iq=q
    if il>best_il: best_il=il;best_lq=q
    if ip>0.005 or q<=30:
        print("%4d %3d %4d %10.6f %10.6f %8.4f" % (q,mu,phi,ip,il,ratio))
sys.stdout.flush()
print()
print("PEAK I_P: q=%d (%.6f)" % (best_iq,best_ip))
print("PEAK I_L: q=%d (%.6f)" % (best_lq,best_il))
print()
# Top 10 each
print("--- Top 10 by I_Prime ---")
by_ip=sorted(results,key=lambda x:-x[3])
for q,mu,phi,ip,il,r in by_ip[:10]:
    print("  q=%3d I_P=%.6f I_L=%.6f mu=%+d" % (q,ip,il,mu))
print()
print("--- Top 10 by I_Lambda ---")
by_il=sorted(results,key=lambda x:-x[4])
for q,mu,phi,ip,il,r in by_il[:10]:
    print("  q=%3d I_L=%.6f I_P=%.6f mu=%+d" % (q,il,ip,mu))
print()
# Bright/dark classification
thresh=0.0005
bs=bn=ds=dn=0
for q,mu,phi,ip,il,r in results:
    sf=(mu!=0);bright=(il>thresh)
    if bright and sf: bs+=1
    elif bright and not sf: bn+=1
    elif not bright and sf: ds+=1
    else: dn+=1
print("Lambda bright/dark vs squarefree:")
print("              Sqfree  Not-sqfree")
print("  Bright:     %5d   %5d" % (bs,bn))
print("  Dark:       %5d   %5d" % (ds,dn))
print()
# Ratio analysis at bright wavelengths
rats=[(q,r) for q,mu,phi,ip,il,r in results if ip>0.005 and mu!=0]
if rats:
    mean_r=sum(r for _,r in rats)/len(rats)
    print("Mean Lambda/Prime ratio at bright q: %.4f" % mean_r)
    print("Lambda is ALWAYS %s in additive geometry" % ("WEAKER" if mean_r<1 else "STRONGER"))
print()
# Envelope decay
print("--- Signal envelope (max in windows of 10) ---")
print("%10s %10s %10s" % ("range","max_I_P","max_I_L"))
for s in range(2,201,10):
    e=min(s+9,200)
    mip=max(r[3] for r in results if s<=r[0]<=e)
    mil=max(r[4] for r in results if s<=r[0]<=e)
    print("%4d - %3d %10.6f %10.6f" % (s,e,mip,mil))
