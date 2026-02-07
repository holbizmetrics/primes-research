#!/usr/bin/env python3
"""Deeper bit analysis: popcount bias, bit reversal primes, carry sweep"""
import math

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return s

N=16384; is_p=sieve(N)
P=[n for n in range(2,N+1) if is_p[n]]

def popcount(n):
    c=0
    while n:c+=n&1;n>>=1
    return c

# ==========================================
# STRIKE A: WHY do primes have higher popcount?
# Primes must be odd (bit 0 = 1) and not divisible by small primes.
# This forces certain bit patterns -> higher popcount?
# Compare: primes vs ODD composites vs all odd numbers
# ==========================================
print("=== WHY higher popcount? ===")
print("Compare: all odd, odd composites, primes")
print()
for blen in [8,10,12,14]:
    lo=1<<(blen-1); hi=(1<<blen)-1
    odd=[n for n in range(lo|1,hi+1,2)]
    odd_comp=[n for n in odd if not is_p[n]]
    prm=[n for n in odd if is_p[n]]
    if not prm: continue
    mo=sum(popcount(n) for n in odd)/len(odd)
    mc=sum(popcount(n) for n in odd_comp)/len(odd_comp)
    mp=sum(popcount(n) for n in prm)/len(prm)
    # Also: numbers coprime to 6 (not div by 2 or 3)
    cop6=[n for n in odd if n%3!=0]
    m6=sum(popcount(n) for n in cop6)/len(cop6)
    print("  %2d bits: odd=%.3f cop6=%.3f odd_comp=%.3f primes=%.3f  prime-odd=%+.3f  prime-cop6=%+.3f" % (
        blen,mo,m6,mc,mp,mp-mo,mp-m6))

print()
print("If prime-odd >> 0 but prime-cop6 ~ 0: popcount bias is from coprimality")
print("If prime-cop6 >> 0: primes have intrinsic bit bias beyond coprimality")
print()

# ==========================================
# STRIKE B: Bit reversal primes — 3x enrichment!
# WHY are bit-reversed primes 3x more likely to be prime?
# Is this just because primes are odd (MSB=1, so reversed has LSB=1)?
# ==========================================
print("=== Bit reversal: controlling for oddness ===")
def bit_rev(n, w):
    r=0
    for i in range(w): r=(r<<1)|(n&1); n>>=1
    return r

for blen in [10,12,14]:
    lo=1<<(blen-1); hi=(1<<blen)-1
    prm=[p for p in P if lo<=p<=hi]
    # All primes have MSB=1 (by construction of range) and LSB=1 (odd)
    # So reversed also has MSB=1 and LSB=1 -> odd and in same bit range
    rev_prime=sum(1 for p in prm if bit_rev(p,blen)<=N and is_p[bit_rev(p,blen)])
    # Control: random odd numbers in range with MSB=1 and LSB=1
    ctrl=[n for n in range(lo|1,hi+1,2) if n&(1<<(blen-1))]
    rev_ctrl=sum(1 for n in ctrl if bit_rev(n,blen)<=N and is_p[bit_rev(n,blen)])
    density_p=len(prm)/len(ctrl) if ctrl else 0
    exp_p=len(prm)*density_p; exp_c=len(ctrl)*density_p
    ratio_p=rev_prime/exp_p if exp_p>0 else 0
    ratio_c=rev_ctrl/exp_c if exp_c>0 else 0
    print("  %2d bits: primes:%d rev_prime:%d (exp %.1f ratio %.2f) | ctrl:%d rev_prime:%d (exp %.1f ratio %.2f)" % (
        blen,len(prm),rev_prime,exp_p,ratio_p,len(ctrl),rev_ctrl,exp_c,ratio_c))

print()
print("If ratio_prime >> ratio_ctrl: bit reversal preserves primality beyond chance")
print("If ratio_prime ~ ratio_ctrl: just density effect")
print()

# ==========================================
# STRIKE C: Sweep the BIT ROTATION
# Not just reversal — rotate bits by d positions.
# Is there an optimal rotation that maximizes prime-to-prime?
# ==========================================
print("=== Bit rotation sweep ===")
print("Rotate bits of prime by d positions. How often still prime?")
print()

blen=12; lo=1<<(blen-1); hi=(1<<blen)-1
prm=[p for p in P if lo<=p<=hi]

def bit_rotate(n, d, w):
    """Rotate n left by d positions in w-bit field"""
    d = d % w
    return ((n << d) | (n >> (w - d))) & ((1 << w) - 1)

print("%3s %6s %6s %8s" % ("d","count","expected","ratio"))
print("-"*28)
best_r=0;best_d=0
for d in range(blen):
    count=0
    for p in prm:
        r=bit_rotate(p, d, blen)
        if lo<=r<=hi and r<=N and is_p[r]:
            count+=1
    density=len(prm)/(hi-lo+1)
    expected=len(prm)*density
    ratio=count/expected if expected>0 else 0
    if ratio>best_r:best_r=ratio;best_d=d
    print("%3d %6d %6.1f %8.3f%s" % (d,count,expected,ratio," *" if ratio>2 else ""))

print()
print("Best rotation: d=%d, ratio=%.3f" % (best_d,best_r))
print("d=0 is identity. d=1 is 'double and wrap'. d=%d is reversal-like." % (blen//2))
print()

# ==========================================
# STRIKE D: XOR with neighbors
# p XOR (p+2): if both prime (twin), what's the XOR?
# p XOR (p-1): always flips trailing 1s (known!)
# p XOR nextprime(p): what pattern?
# ==========================================
print("=== XOR between consecutive primes ===")
print("Popcount of p_n XOR p_{n+1}")
print()

xor_pop = [popcount(P[i] ^ P[i+1]) for i in range(len(P)-1)]
gaps = [P[i+1] - P[i] for i in range(len(P)-1)]

# By gap size
from collections import defaultdict
gap_xor = defaultdict(list)
for i in range(len(gaps)):
    gap_xor[gaps[i]].append(xor_pop[i])

print("%4s %6s %8s %5s" % ("gap","count","mean_xor","note"))
print("-"*30)
for g in sorted(gap_xor.keys())[:15]:
    vals=gap_xor[g]
    mean_x=sum(vals)/len(vals)
    note=""
    if g==2: note="twins"
    elif g==4: note="cousins"
    elif g==6: note="sexy"
    print("%4d %6d %8.3f %s" % (g,len(vals),mean_x,note))

print()
# Is there a formula? gap=2k means the numbers differ in at most
# the lowest bits. XOR popcount ~ number of bit positions that change.
print("XOR popcount ~ log2(gap) + noise from carries")
for g in [2,4,6,8,10,12]:
    if g in gap_xor:
        m=sum(gap_xor[g])/len(gap_xor[g])
        pred=math.log2(g)+1 if g>1 else 1
        print("  gap=%d: mean_xor=%.2f, log2(gap)+1=%.2f" % (g,m,pred))
