#!/usr/bin/env python3
"""Better measure: peak sharpness Q at the first zero
Q = F(gamma^a) / F(gamma^a +/- delta)
Sweep alpha and beta, measure Q for gamma_1
"""
import math
N=800
def mg(n):
    if n<2:return 0
    t=n
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]:
        if t==1:break
        k=0
        while t%p==0:t//=p;k+=1
        if k>0 and t==1:return math.log(p)
    if t>1:return math.log(n)
    return 0
L={};LN={}
for n in range(2,N+1):
    l=mg(n)
    if l>0:L[n]=l;LN[n]=math.log(n)

g1=14.1347

def F(t,beta):
    ar=ai=0.0
    for n,l in L.items():
        pos=LN[n]**beta; w=l/math.sqrt(n)
        ar+=w*math.cos(-t*pos); ai+=w*math.sin(-t*pos)
    return ar*ar+ai*ai

# For each (alpha, beta), compute the probe frequency
# t_probe = gamma_1^alpha
# Then measure Q = F(t_probe)/mean(F(t_probe +/- offsets))
print("=== Peak sharpness Q at gamma_1 ===")
print("Q = F(peak)/F(nearby). Higher = sharper resonance")
print()
print("%5s %5s %8s %8s %8s" % ("alpha","beta","F_peak","F_wing","Q"))
print("-"*40)
best_Q=0;ba=1;bb=1
for ai in range(5,22):
    a=ai*0.1
    for bi in range(3,16):
        b=bi*0.1
        t0=g1**a
        fp=F(t0,b)
        # Wings: +/- 10%
        delta=t0*0.1
        fw=0
        for d in [-2*delta,-delta,delta,2*delta]:
            fw+=F(t0+d,b)
        fw/=4
        Q=fp/fw if fw>0.1 else 0
        if Q>best_Q: best_Q=Q;ba=a;bb=b
        if Q>2.0 or (abs(a-1)<0.05 and abs(b-1)<0.05):
            print("%5.1f %5.1f %8.1f %8.1f %8.2f%s" % (a,b,fp,fw,Q,
                " **" if Q>3 else ""))
print()
print("BEST: alpha=%.1f beta=%.1f Q=%.2f" % (ba,bb,best_Q))
print("Standard (1,1): ", end="")
t0=g1; fp=F(t0,1.0)
fw=sum(F(t0+d,1.0) for d in [-t0*0.2,-t0*0.1,t0*0.1,t0*0.2])/4
print("Q=%.2f" % (fp/fw if fw>0.1 else 0))
print()

# Does alpha=0.5 (half-inversion) do anything special?
print("=== Half-inversion check ===")
for a in [0.5, 1.0, 1.5, 2.0]:
    t0=g1**a; fp=F(t0,1.0)
    fw=sum(F(t0+d,1.0) for d in [-t0*0.15,-t0*0.08,t0*0.08,t0*0.15])/4
    Q=fp/fw if fw>0.1 else 0
    # Also check all 5 zeros
    Qs=[]
    for g in [14.1347,21.022,25.0109,30.4249,32.9351]:
        t0=g**a; fp2=F(t0,1.0)
        fw2=sum(F(t0+d,1.0) for d in [-t0*0.15,-t0*0.08,t0*0.08,t0*0.15])/4
        Qs.append(fp2/fw2 if fw2>0.1 else 0)
    print("  alpha=%.1f: Q(g1)=%.2f, mean_Q=%.2f" % (a, Q, sum(Qs)/len(Qs)))
