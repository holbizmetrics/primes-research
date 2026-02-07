#!/usr/bin/env python3
"""Definitive test: scan F(t) continuously for different (alpha,beta)
Is there a REAL peak at gamma_1^alpha, or is it noise?"""
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
    r=i=0.0
    for n,l in L.items():
        p=LN[n]**beta;w=l/math.sqrt(n)
        r+=w*math.cos(-t*p);i+=w*math.sin(-t*p)
    return r*r+i*i

# Standard: alpha=1, beta=1 — scan around gamma_1
print("=== alpha=1.0, beta=1.0: scan t around gamma_1=14.13 ===")
t0=g1; print("t0=%.2f" % t0)
for dt in range(-10,11):
    t=t0+dt*0.5; f=F(t,1.0)
    bar="*"*int(f/10); print("  t=%6.2f F=%8.1f %s%s" % (t,f,bar," <-- gamma_1" if abs(dt)<1 else ""))

print()
# alpha=2.0, beta=0.7 — scan around gamma_1^2
print("=== alpha=2.0, beta=0.7: scan t around gamma_1^2=199.8 ===")
t0=g1**2; print("t0=%.2f" % t0)
for dt in range(-10,11):
    t=t0+dt*5; f=F(t,0.7)
    bar="*"*int(f/3); print("  t=%7.1f F=%8.1f %s%s" % (t,f,bar," <-- gamma_1^2" if abs(dt)<1 else ""))

print()
# alpha=1.9, beta=0.7
print("=== alpha=1.9, beta=0.7: scan t around gamma_1^1.9=166.5 ===")
t0=g1**1.9; print("t0=%.2f" % t0)
for dt in range(-10,11):
    t=t0+dt*4; f=F(t,0.7)
    bar="*"*int(f/3); print("  t=%7.1f F=%8.1f %s%s" % (t,f,bar," <-- gamma_1^1.9" if abs(dt)<1 else ""))

print()
# KEY TEST: is the peak AT gamma^alpha or somewhere else?
print("=== Is the peak AT gamma_1^alpha or accidental? ===")
for a,b in [(1.0,1.0),(1.5,1.0),(1.9,0.7),(2.0,0.7),(2.0,0.9)]:
    t0=g1**a
    # Find actual peak in neighborhood
    best_t=t0; best_f=0
    for dt in range(-40,41):
        t=t0*(1+dt*0.01)
        f=F(t,b)
        if f>best_f: best_f=f;best_t=t
    offset=(best_t-t0)/t0*100
    print("  a=%.1f b=%.1f: gamma^a=%.2f, actual_peak=%.2f (offset %+.1f%%), F=%.1f" % (
        a,b,t0,best_t,offset,best_f))
