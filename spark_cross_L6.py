#!/usr/bin/env python3
"""SPARK Cross-L: Strikes 15-18

Confirmed: mixed zeros are Poisson (no cross-repulsion).
Now: is there ANY cross-correlation signal beyond Poisson?

Strike 15: Cross-correlation at SPECIFIC tau values (the additive laser)
Strike 16: Cross number variance (more sensitive than SFF)
Strike 17: What if we weight by the character relationship?
Strike 18: The bridge — does the explicit formula create cross-terms?
"""
import math

def parse_file(fname):
    data = {}
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line: continue
            label, nums = line.split(':', 1)
            zeros = [float(x) for x in nums.split() if x]
            data[label.strip()] = zeros
    return data

all_zeros = {}
for fname in ['clz5_all.txt', 'clz3_out.txt']:
    all_zeros.update(parse_file(fname))
z3_raw = """Q3_0: 14.13472514 21.02203964 25.01085758 30.42487613 32.93506159 37.58617816 40.91871901 43.32707328 48.00515088 49.77383248 52.97032148 56.44624770 59.34704400 60.83177852 65.11254405 67.07981053 69.54640171 72.06715767 75.70469070 77.14484007 79.33737502
Q3_1: 8.03973716 11.24920621 15.70461918 18.26199750 20.45577081 24.05941486 26.57786874 28.21816451 30.74504026 33.89738893 35.60841265 37.55179656 39.48520726 42.61637923 44.12057291 46.27411802 47.51410451 50.37513865 52.49674960 54.19384310 55.64255870 57.58405636 60.02685746 62.20607812 63.17699277 65.29492554 66.62313463 69.51302299 70.81979870 72.65614907 74.00542852 75.62240696 78.21748127 79.63797575"""
for line in z3_raw.strip().split('\n'):
    label, nums = line.split(':', 1)
    all_zeros[label.strip()] = [float(x) for x in nums.split()]

# ============================================
# STRIKE 15: The explicit formula bridge
# psi(x; chi) = sum_{chi(n)} Lambda(n) for n <= x
# Each character has its own psi function.
# Cross-correlation of psi(x;chi_1) and psi(x;chi_2) involves
# sum over zeros of L(s,chi_1) and L(s,chi_2).
# If zeros are independent, the cross-correlation of the oscillating
# parts should vanish.
#
# Test: compute A_chi(t) = sum_n chi(n) Lambda(n) n^{-1/2-it}
# for two different characters, and see if they're correlated.
# ============================================
print("=== STRIKE 15: Explicit formula cross-correlation ===")
print("A_chi(t) = sum Lambda(n) chi(n) n^{-1/2 - it}")
print()

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return s

N = 5000
is_p = sieve(N)

def mangoldt(n):
    """Lambda(n) = log(p) if n is a prime power p^k, else 0"""
    if n < 2: return 0
    if is_p[n]: return math.log(n)
    # Check prime powers
    for p in range(2, int(n**0.5)+1):
        if not is_p[p]: continue
        m = n
        while m > 1:
            if m % p != 0: break
            m //= p
        if m == 1: return math.log(p)
    return 0

# Characters mod 5
# Generator 2, order 4. chi_a(2) = e^{2pi*i*a/4}
# chi_a(n): need n mod 5's discrete log base 2.
# 2^0=1, 2^1=2, 2^2=4, 2^3=3, 2^4=1 mod 5
# So: 1->0, 2->1, 3->3, 4->2 (discrete logs mod 5)
dlog5 = {1:0, 2:1, 3:3, 4:2}

def chi5(a, n):
    """Character chi_a mod 5: chi_a(n) = e^{2pi*i*a*dlog(n)/4}"""
    r = n % 5
    if r == 0: return 0
    dl = dlog5[r]
    theta = 2 * math.pi * a * dl / 4
    return complex(math.cos(theta), math.sin(theta))

# Precompute Lambda
LAM = {}
for n in range(2, N+1):
    l = mangoldt(n)
    if l > 0: LAM[n] = l

def A_chi(a, t, q=5):
    """Amplitude: sum Lambda(n) chi_a(n) n^{-1/2-it}"""
    ar = ai = 0.0
    for n, lam in LAM.items():
        c = chi5(a, n)
        if c == 0: continue
        phase = -t * math.log(n)
        w = lam / math.sqrt(n)
        # c * exp(i*phase) = (cr + i*ci) * (cos(phase) + i*sin(phase))
        cr, ci = c.real, c.imag
        cp, sp = math.cos(phase), math.sin(phase)
        ar += w * (cr*cp - ci*sp)
        ai += w * (cr*sp + ci*cp)
    return complex(ar, ai)

# Test: |A_chi(a, t)|^2 should peak at zeros of L(s, chi_a)
print("Test: |A_chi_0(t)|^2 at first few zeta zeros:")
for g in all_zeros.get('Q5_0', [])[:5]:
    amp = A_chi(0, g)
    print("  t=%.4f: |A|^2 = %.2f" % (g, abs(amp)**2))

print()
print("|A_chi_1(t)|^2 at first few L(s,chi_1) zeros:")
for g in all_zeros.get('Q5_1', [])[:5]:
    amp = A_chi(1, g)
    print("  t=%.4f: |A|^2 = %.2f" % (g, abs(amp)**2))

print()

# ============================================
# STRIKE 16: Cross-amplitude product
# For zeros gamma of L(s,chi_1):
# what is <|A_chi_2(gamma)|^2> ?
# If independent: should equal the smooth background.
# If correlated: should be enhanced/depleted.
# ============================================
print("=== STRIKE 16: Cross-amplitude at zeros ===")
print("|A_chi_b|^2 evaluated at zeros of L(s, chi_a)")
print()

# Compute |A_b(t)|^2 for a grid, then at specific zeros
import random

# Background: average |A_b(t)|^2 at random t
bg = {}
for b in range(4):
    random_ts = [random.uniform(10, 60) for _ in range(20)]
    bg_vals = [abs(A_chi(b, t))**2 for t in random_ts]
    bg[b] = sum(bg_vals) / len(bg_vals)
    print("  Background |A_%d|^2: %.2f" % (b, bg[b]))

print()

# At zeros of each L-function
for a in range(4):
    label = 'Q5_%d' % a
    zeros = [g for g in all_zeros.get(label, []) if 10 <= g <= 60][:15]
    if len(zeros) < 3: continue

    for b in range(4):
        vals = [abs(A_chi(b, g))**2 for g in zeros]
        mean_val = sum(vals) / len(vals)
        ratio = mean_val / bg[b] if bg[b] > 0 else 0
        tag = " <-- SELF" if a == b else ""
        if ratio > 2: tag += " HIGH!"
        print("  |A_%d|^2 at zeros of chi_%d: mean=%.2f, bg=%.2f, ratio=%.2f%s" % (
            b, a, mean_val, bg[b], ratio, tag))
    print()

print("ratio >> 1 at self: confirms zeros are where |A|^2 peaks (by definition)")
print("ratio >> 1 at cross: zeros of chi_a enhance |A_b|^2 (CROSS-CORRELATION)")
print("ratio ~ 1 at cross: independent (expected)")
