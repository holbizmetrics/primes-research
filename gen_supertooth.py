#!/usr/bin/env python3
"""Generate audio of the super tooth — the merged frequency comb"""
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
    print(f"  {path} ({len(samples)/rate:.1f}s)")
    sys.stdout.flush()

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

def c_q(n, q):
    """Ramanujan sum c_q(n)"""
    g = math.gcd(n, q)
    qg = q // g
    mu_qg = mobius(qg)
    phi_q = euler_phi(q)
    phi_qg = euler_phi(qg)
    return mu_qg * phi_q // phi_qg if phi_qg > 0 else 0

# Precompute mu and phi
MU = {}; PHI = {}
for q in range(1, 101):
    MU[q] = mobius(q)
    PHI[q] = euler_phi(q)

def supertooth(n, Q_max):
    """Compute f(n) = -sum_{q=1}^{Q} mu(q)/phi(q) * c_q(n)"""
    f = 0
    for q in range(1, Q_max+1):
        if MU[q] == 0: continue
        f -= MU[q] / PHI[q] * c_q(n, q)
    return f

which = sys.argv[1] if len(sys.argv) > 1 else "all"

# ==========================================
# 1. BUILDUP: Add teeth one by one
# Each segment adds one more q to the sum
# You hear the super tooth forming from noise to signal
# ==========================================
if which in ("1", "all"):
    print("1. Super tooth buildup (teeth added one by one)")
    smp = []
    Q_list = [q for q in range(2, 31) if MU.get(q, 0) != 0]
    
    seg_dur = 0.8  # seconds per added tooth
    ns_seg = int(seg_dur * RATE)
    
    for idx, Q_add in enumerate(Q_list):
        Q_current = Q_list[:idx+1]
        # Play the current partial sum as a pulse train
        # Each "n" gets a short tone whose amplitude = f(n)
        tone_dur = int(0.015 * RATE)  # 15ms per integer
        for n in range(2, int(ns_seg / tone_dur) + 2):
            f_n = 0
            for q in Q_current:
                f_n -= MU[q] / PHI[q] * c_q(n, q)
            
            # Tone with amplitude proportional to f_n
            freq = 440
            for t in range(tone_dur):
                env = math.exp(-5 * t / tone_dur)
                smp.append(f_n * env * math.sin(2 * math.pi * freq * t / RATE))
        
        # Small gap between segments
        smp.extend([0] * int(0.05 * RATE))
    
    write_wav("08_supertooth_buildup.wav", smp)

# ==========================================
# 2. PULSE TRAIN: f(n) as click amplitude
# Loud clicks at primes, silence at composites
# ==========================================
if which in ("2", "all"):
    print("2. Super tooth pulse train (Q=30)")
    smp = []
    Q = 30
    click_dur = int(0.04 * RATE)  # 40ms per number
    
    for n in range(2, 301):
        f_n = supertooth(n, Q)
        freq = 600
        for t in range(click_dur):
            env = math.exp(-8 * t / click_dur)
            smp.append(f_n * env * math.sin(2 * math.pi * freq * t / RATE))
    
    write_wav("09_supertooth_pulse.wav", smp)

# ==========================================
# 3. CARRIER MODULATION: f(n) modulates pitch
# High pitch at primes, low pitch at composites
# ==========================================
if which in ("3", "all"):
    print("3. Super tooth melody (pitch = f(n))")
    smp = []
    Q = 30
    note_dur = int(0.06 * RATE)
    
    for n in range(2, 201):
        f_n = supertooth(n, Q)
        # Map f_n to frequency: composites ~200Hz, primes ~800-1200Hz
        freq = 300 + max(0, f_n) * 150
        amp = 0.3 + 0.7 * max(0, min(1, f_n / 5))
        for t in range(note_dur):
            env = math.exp(-3 * t / note_dur)
            smp.append(amp * env * math.sin(2 * math.pi * freq * t / RATE))
    
    write_wav("10_supertooth_melody.wav", smp)

# ==========================================
# 4. INDIVIDUAL TEETH as audio harmonics
# Each tooth q plays as harmonic q of a base frequency
# Amplitude = mu(q)/phi(q), building up the comb
# ==========================================
if which in ("4", "all"):
    print("4. Frequency comb as literal harmonics")
    base = 55  # A1
    dur = 6.0
    ns = int(dur * RATE)
    
    # Build up: first 2 seconds = q=2 only
    # next 1s add q=3, then q=5, etc.
    Q_list = [q for q in range(2, 51) if MU.get(q, 0) != 0]
    
    smp = [0.0] * ns
    for idx, q in enumerate(Q_list):
        # Fade in this tooth
        start_t = int(idx * dur / len(Q_list) * RATE)
        amp = abs(MU[q]) / PHI[q]
        freq = base * q
        if freq > RATE / 2: continue  # Nyquist
        
        dphi = 2 * math.pi * freq / RATE
        phi = 0
        for t in range(start_t, ns):
            fade = min(1.0, (t - start_t) / (0.3 * RATE))
            smp[t] += amp * fade * math.sin(phi)
            phi += dphi
    
    write_wav("11_comb_harmonics.wav", smp)

# ==========================================
# 5. THE SUPER TOOTH vs LAMBDA: comparison
# Play Lambda(n) = log(p) at primes, 0 at composites
# vs the Q=30 approximation, side by side
# ==========================================
if which in ("5", "all"):
    print("5. Super tooth vs true Lambda(n)")
    
    def true_lambda(n):
        """von Mangoldt function"""
        if n < 2: return 0
        t = n
        for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71]:
            if t == 1: break
            k = 0
            while t % p == 0:
                t //= p; k += 1
            if k > 0 and t == 1:
                return math.log(p)
        if t > 1:  # n itself is prime
            return math.log(n)
        return 0
    
    smp = []
    click_dur = int(0.04 * RATE)
    
    # First half: true Lambda(n)
    for n in range(2, 151):
        lam = true_lambda(n)
        freq = 600
        for t in range(click_dur):
            env = math.exp(-8 * t / click_dur)
            smp.append(lam * env * math.sin(2 * math.pi * freq * t / RATE))
    
    # Gap
    smp.extend([0] * int(0.5 * RATE))
    
    # Second half: super tooth Q=30
    Q = 30
    for n in range(2, 151):
        f_n = supertooth(n, Q)
        freq = 600
        for t in range(click_dur):
            env = math.exp(-8 * t / click_dur)
            smp.append(f_n * env * math.sin(2 * math.pi * freq * t / RATE))
    
    write_wav("12_lambda_vs_supertooth.wav", smp)

print("\nDone!")
