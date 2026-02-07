#!/usr/bin/env python3
import struct, math, wave
R = 22050
base = 55
ns = int(3.0 * R)

def mu(n):
    if n == 1: return 1
    d = 2; t = n; f = 0
    while d*d <= t:
        if t % d == 0:
            f += 1; t //= d
            if t % d == 0: return 0
        d += 1
    if t > 1: f += 1
    return (-1)**f

def phi(n):
    r = n; d = 2; t = n
    while d*d <= t:
        if t % d == 0:
            while t % d == 0: t //= d
            r -= r // d
        d += 1
    if t > 1: r -= r // t
    return r

ql = [q for q in range(2, 31) if mu(q) != 0]
s = [0.0] * ns
for q in ql:
    a = 1.0 / phi(q)
    freq = base * q
    if freq > R // 2: continue
    dp = 2 * math.pi * freq / R
    ph = 0.0
    for t in range(ns):
        s[t] += a * math.sin(ph)
        ph += dp

with wave.open('audio/11_comb_harmonics.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(R)
    mx = max(abs(x) for x in s) or 1
    w.writeframes(b''.join(struct.pack('<h', int(x/mx*30000)) for x in s))
print('audio/11_comb_harmonics.wav (3.0s)')
