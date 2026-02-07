#!/usr/bin/env python3
"""Sonify zeta zero overtones — hear the consonance between zeros
And inversions: what do inverted zeros sound like?
"""
import struct, math, wave, os, sys

RATE = 22050
OUTDIR = "/data/data/com.termux/files/home/primes-research/audio"
os.makedirs(OUTDIR, exist_ok=True)

def write_wav(filename, samples, rate=RATE):
    path = os.path.join(OUTDIR, filename)
    with wave.open(path, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        mx = max(abs(s) for s in samples) or 1
        data = b''.join(struct.pack('<h', int(s/mx*30000)) for s in samples)
        w.writeframes(data)
    print("  %s (%.1fs)" % (path, len(samples)/rate))
    sys.stdout.flush()

# First 30 zeros
zeros = []
try:
    with open('z.txt') as f:
        for line in f:
            line = line.strip()
            if line: zeros.append(float(line))
    zeros = zeros[:30]
except:
    zeros = [14.1347,21.0220,25.0109,30.4249,32.9351,37.5862,40.9187,
             43.3271,48.0052,49.7738,52.9703,56.4462,59.3470,60.8318,
             65.1125,67.0798,69.5464,72.0672,75.7047,77.1448,79.3374,
             82.9104,84.7355,87.4253,88.8091,92.4919,94.6514,95.8706,
             98.8312,101.318]

which = sys.argv[1] if len(sys.argv) > 1 else "all"

# ==========================================
# 1. INDIVIDUAL ZEROS as tones
# Each gamma_k mapped to a frequency: base * gamma_k / gamma_1
# Hear each zero ring, then fade
# ==========================================
if which in ("1", "all"):
    print("1. Individual zero tones (each gamma_k as a pitch)")
    smp = []
    base = 220.0  # A3
    tone_dur = int(1.0 * RATE)  # 1 second per zero
    gap = int(0.1 * RATE)

    for k in range(min(15, len(zeros))):
        freq = base * zeros[k] / zeros[0]
        # Amplitude decays with k (higher zeros are quieter)
        amp = 1.0 / (1 + k * 0.15)
        for t in range(tone_dur):
            env = math.exp(-2.0 * t / tone_dur)  # decay
            smp.append(amp * env * math.sin(2 * math.pi * freq * t / RATE))
        smp.extend([0] * gap)

    write_wav("13_zero_tones.wav", smp)

# ==========================================
# 2. CONSONANT PAIRS — zeros with near-rational ratios
# Play the two simultaneously to hear the beating/consonance
# ==========================================
if which in ("2", "all"):
    print("2. Consonant zero pairs")
    smp = []
    base = 220.0
    pair_dur = int(2.0 * RATE)
    gap = int(0.3 * RATE)

    # Best consonant pairs (from our analysis)
    pairs = [
        (0, 1, "g1/g2 ~ 2/3 (fifth)"),
        (0, 4, "g1/g5 ~ 3/7"),
        (2, 5, "g3/g6 ~ 2/3 (fifth)"),
        (4, 5, "g5/g6 ~ 7/8"),
        (5, 6, "g6/g7 ~ 11/12"),
        (0, 6, "g1/g7 ~ 1/3"),
        (3, 6, "g4/g7 ~ 3/4 (fourth)"),
    ]

    for i, j, label in pairs:
        if i >= len(zeros) or j >= len(zeros): continue
        f1 = base * zeros[i] / zeros[0]
        f2 = base * zeros[j] / zeros[0]
        for t in range(pair_dur):
            env = math.exp(-1.0 * t / pair_dur)
            s = 0.5 * env * (math.sin(2*math.pi*f1*t/RATE) +
                             math.sin(2*math.pi*f2*t/RATE))
            smp.append(s)
        smp.extend([0] * gap)

    write_wav("14_zero_consonance.wav", smp)

# ==========================================
# 3. THE ZERO CHORD — all zeros sounding simultaneously
# Build up: add one zero at a time
# ==========================================
if which in ("3", "all"):
    print("3. Zero chord buildup (all zeros together)")
    base = 110.0  # lower base for richness
    total_dur = int(8.0 * RATE)
    nz = min(20, len(zeros))
    smp = [0.0] * total_dur

    for k in range(nz):
        freq = base * zeros[k] / zeros[0]
        if freq > RATE / 2: continue  # Nyquist
        amp = 1.0 / (1 + k * 0.2)
        # Fade in at staggered times
        start_t = int(k * total_dur / (nz + 2))
        dphi = 2 * math.pi * freq / RATE
        phi = 0
        for t in range(start_t, total_dur):
            fade_in = min(1.0, (t - start_t) / (0.5 * RATE))
            smp[t] += amp * fade_in * math.sin(phi)
            phi += dphi

    write_wav("15_zero_chord.wav", smp)

# ==========================================
# 4. EXPLICIT FORMULA as audio waveform
# psi(x) = x - sum 2*Re(x^rho/rho)
# Play the OSCILLATION part: -sum 2*Re(x^rho/rho)
# x sweeps from e^1 to e^8, mapped to time
# ==========================================
if which in ("4", "all"):
    print("4. Explicit formula oscillation (psi(x) - x)")
    dur = 6.0
    ns = int(dur * RATE)
    smp = []
    nz_use = min(30, len(zeros))

    for t in range(ns):
        # Map time to log(x)
        lx = 1.0 + 7.0 * t / ns  # log(x) from 1 to 8
        x = math.exp(lx)
        xhalf = math.sqrt(x)

        osc = 0.0
        for k in range(nz_use):
            g = zeros[k]
            denom = 0.25 + g**2
            re_inv_rho = 0.5 / denom
            im_inv_rho = -g / denom
            phase = g * lx
            re_xrho = xhalf * math.cos(phase)
            im_xrho = xhalf * math.sin(phase)
            re_term = re_xrho * re_inv_rho - im_xrho * im_inv_rho
            osc -= 2 * re_term

        # Normalize by x to keep amplitude manageable
        smp.append(osc / x)

    write_wav("16_explicit_formula.wav", smp)

# ==========================================
# 5. INVERTED ZEROS — play 1/gamma_k as frequencies
# If zeros are {14.13, 21.02, ...}, inverted are {1/14.13, 1/21.02, ...}
# Scale to audible range
# ==========================================
if which in ("5", "all"):
    print("5. Inverted zero tones (1/gamma_k)")
    smp = []
    # Inverted zeros: 1/gamma_k, normalized
    inv_zeros = [1.0/g for g in zeros]
    # Scale so largest inverted = gamma_1 frequency
    inv_max = max(inv_zeros)
    base = 220.0

    tone_dur = int(1.0 * RATE)
    gap = int(0.1 * RATE)

    for k in range(min(15, len(inv_zeros))):
        freq = base * inv_zeros[k] / inv_max  # largest = 220 Hz
        amp = 1.0 / (1 + k * 0.15)
        for t in range(tone_dur):
            env = math.exp(-2.0 * t / tone_dur)
            smp.append(amp * env * math.sin(2 * math.pi * freq * t / RATE))
        smp.extend([0] * gap)

    write_wav("17_inverted_zeros.wav", smp)

# ==========================================
# 6. INVERTED CHORD — all inverted zeros together
# Compare with the normal chord
# ==========================================
if which in ("6", "all"):
    print("6. Inverted zero chord")
    inv_zeros = [1.0/g for g in zeros]
    inv_max = max(inv_zeros)
    base = 110.0
    total_dur = int(6.0 * RATE)
    nz = min(20, len(zeros))

    # First half: normal zeros
    smp = [0.0] * total_dur
    for k in range(nz):
        freq = base * zeros[k] / zeros[0]
        if freq > RATE/2: continue
        amp = 1.0 / (1 + k*0.2)
        dphi = 2*math.pi*freq/RATE; phi = 0
        for t in range(total_dur//2):
            fade = min(1.0, t/(0.3*RATE)) * math.exp(-0.5*(t-total_dur//4)**2/(total_dur//8)**2) if t > total_dur//4 else min(1.0, t/(0.3*RATE))
            smp[t] += amp * fade * math.sin(phi); phi += dphi

    # Brief silence

    # Second half: inverted zeros
    for k in range(nz):
        freq = base * inv_zeros[k] / inv_max * (zeros[-1]/zeros[0])  # scale to similar range
        if freq > RATE/2 or freq < 20: continue
        amp = 1.0 / (1 + k*0.2)
        dphi = 2*math.pi*freq/RATE; phi = 0
        start = total_dur//2 + int(0.3*RATE)
        for t in range(start, total_dur):
            fade = min(1.0, (t-start)/(0.3*RATE))
            smp[t] += amp * fade * math.sin(phi); phi += dphi

    write_wav("18_normal_vs_inverted.wav", smp)

# ==========================================
# 7. DESTRUCTIVE pair vs CONSTRUCTIVE pair
# Play the most destructive (g3,g4) and most constructive (g4,g5)
# back to back — hear the difference
# ==========================================
if which in ("7", "all"):
    print("7. Destructive vs constructive zero pairs")
    base = 220.0
    pair_dur = int(2.5 * RATE)
    gap = int(0.5 * RATE)
    smp = []

    demo_pairs = [
        (2, 3, "g3+g4 DESTRUCTIVE (excess 0.04)"),
        (3, 4, "g4+g5 CONSTRUCTIVE (excess 1.97)"),
        (1, 3, "g2+g4 DESTRUCTIVE (excess 0.36)"),
        (1, 5, "g2+g6 CONSTRUCTIVE (excess 1.78)"),
    ]

    for i, j, label in demo_pairs:
        if i >= len(zeros) or j >= len(zeros): continue
        f1 = base * zeros[i] / zeros[0]
        f2 = base * zeros[j] / zeros[0]
        # Play both, with a beat pattern
        for t in range(pair_dur):
            env = 1.0 - 0.3 * (t / pair_dur)  # gentle fade
            # Add overtone interaction
            s = 0.5 * env * (math.sin(2*math.pi*f1*t/RATE) +
                             math.sin(2*math.pi*f2*t/RATE))
            smp.append(s)
        smp.extend([0] * gap)

    write_wav("19_destructive_vs_constructive.wav", smp)

# ==========================================
# 8. THE HALF-INVERSION (Legendre analog)
# Instead of gamma_k, use gamma_k^alpha for alpha from 0 to 2
# alpha=1 is normal, alpha=-1 is inverted
# alpha=0.5 is the "half-inversion" (Legendre analog)
# Play alpha = 1, 0.5, 0, -0.5, -1
# ==========================================
if which in ("8", "all"):
    print("8. Power-map inversion sweep (alpha = 1 to -1)")
    base = 110.0
    seg_dur = int(3.0 * RATE)
    gap = int(0.3 * RATE)
    smp = []
    nz = min(15, len(zeros))

    for alpha in [1.0, 0.5, 0.0, -0.5, -1.0]:
        seg = [0.0] * seg_dur
        if alpha == 0:
            # All zeros collapse to same frequency
            freqs = [base * 2] * nz  # all the same
        else:
            mapped = [g**alpha for g in zeros[:nz]]
            # Normalize to audible range
            m_min = min(mapped); m_max = max(mapped)
            if m_max > m_min:
                freqs = [base + (base*4) * (m - m_min)/(m_max - m_min) for m in mapped]
            else:
                freqs = [base * 2] * nz

        for k in range(nz):
            freq = freqs[k]
            if freq > RATE/2 or freq < 20: continue
            amp = 1.0 / (1 + k*0.3)
            dphi = 2*math.pi*freq/RATE; phi = 0
            for t in range(seg_dur):
                fade = min(1.0, t/(0.2*RATE)) * min(1.0, (seg_dur-t)/(0.2*RATE))
                seg[t] += amp * fade * math.sin(phi)
                phi += dphi

        smp.extend(seg)
        smp.extend([0] * gap)

    write_wav("20_zero_inversion_sweep.wav", smp)

print("\nDone!")
