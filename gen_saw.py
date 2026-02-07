#!/usr/bin/env python3
"""Generate sawtooth comparison — optimized"""
import struct, math, wave, os

RATE = 22050
OUTDIR = "/data/data/com.termux/files/home/primes-research/audio"

def write_wav(filename, samples, rate=RATE):
    path = os.path.join(OUTDIR, filename)
    with wave.open(path, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        mx = max(abs(s) for s in samples) or 1
        data = b''.join(struct.pack('<h', int(s/mx*30000)) for s in samples)
        w.writeframes(data)
    print(f"  {path} ({len(samples)/rate:.1f}s)")

Pset = set([2,3,5,7,11,13,17,19,23,29,31,37,41,43,47])
dur = 2.0; base = 130; mh = 47; ns = int(dur * RATE)

for label, harms in [("full", list(range(1, mh+1))),
                      ("primes", [h for h in range(2, mh+1) if h in Pset]),
                      ("composites", [h for h in range(4, mh+1) if h not in Pset])]:
    # Precompute phase increments
    smp = [0.0] * ns
    for h in harms:
        a = 1.0 / h
        dphi = 2 * math.pi * base * h / RATE
        phi = 0.0
        for t in range(ns):
            smp[t] += a * math.sin(phi)
            phi += dphi
    write_wav(f"03_{label}.wav", smp)
    print(f"  ({label}: {len(harms)} harmonics)")
