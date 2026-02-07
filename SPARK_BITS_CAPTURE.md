# SPARK CAPTURE: How Bits Move When You Multiply

## SPRAY (7 ideas)
1. Bit patterns of primes vs composites
2. Hamming weight (popcount) of primes
3. Bit autocorrelation within primes
4. Bit scattering under multiplication (n*k)
5. XOR structure: n XOR (n*k)
6. Carry propagation in multiplication
7. Bit-reversal: reversed(prime) -> prime?

## KEY RESULTS

### Strike 1: Popcount — a DEBUNKED myth

Raw data: primes have +0.6 more 1-bits than composites.
Controlled data: **when you compare primes to odd numbers, the difference is ±0.03.**

The popcount "bias" is entirely because primes are odd (bit 0 = 1, adding 0.5 to expected popcount) and not divisible by 2 (which would force bit 0 = 0 for half of composites).

**There is NO intrinsic bit-level popcount signature of primality.**

### Strike 2: Bit autocorrelation — small but real

Primes have slightly higher bit autocorrelation (0.02-0.05 more than composites). This is from coprimality constraints: not divisible by 3 means certain bit patterns are slightly suppressed, pushing others up.

### Strike 3: Bit scattering under multiplication

When you multiply a prime by k, the Hamming distance H(p, p*k) is 0.4-0.7 MORE than for composites. Primes "scatter more" under multiplication because they have no common factors with k to create shortcuts (cancellation paths through the carry chain).

### Strike 4: Carry chains — no significant difference

Longest carry chain in p+p (= 2p) is essentially the same for primes and composites (diff ~ 0.01-0.17). Carry structure is determined by consecutive 1-bits, which is a random binary string property.

### Strike 5: Bit reversal — REAL signal!

**Primes are 1.5-1.7x more likely to bit-reverse to another prime than random odd numbers are to bit-reverse to a prime.**

```
10 bits: ratio=1.64 (control=1.00)
12 bits: ratio=1.48 (control=1.00)
14 bits: ratio=1.66 (control=1.00)
```

This is NOT just density. The control (random odd numbers) shows ratio=1.00 exactly. Primes have structural similarity to their bit-reversals.

**Why?** Bit reversal preserves:
- MSB = 1 (still in same bit range)
- LSB = 1 (still odd, since primes have MSB=1)
- Popcount (same number of 1-bits)
- NOT divisible by small primes? Partially — bit reversal scrambles the mod structure, but not completely.

The 1.5x enrichment is likely from: primes avoid multiples of small primes, and bit reversal approximately preserves this avoidance for some primes.

### Strike 6: Bit rotation sweep

```
d=0:  8.03x (identity — trivially prime)
d=1:  2.27x (double-and-wrap)
d=11: 2.27x (halve-and-wrap = inverse of d=1)
d=2..10: 1.10-1.26x (near random)
```

Rotation by ±1 is special! This is multiplication/division by 2 modulo 2^k-1 (Mersenne numbers). The 2.27x enrichment at d=±1 means primes are somewhat preserved under "multiplication by 2 mod 2^k-1."

This connects to: **Mersenne prime structure.** In the ring Z/(2^k-1)Z, multiplication by 2 is bit rotation. Primes that survive this rotation are related to the factorization of 2^k-1.

### Strike 7: Twin prime XOR

XOR popcount between consecutive primes follows gap structure:
- Gap 2 (twins): XOR popcount = 1.90 ≈ 2
- Gap 4 (cousins): XOR popcount = 2.04
- Gap 6 (sexy): XOR popcount = 2.96

Twin primes differ in almost exactly 2 bits! The XOR is concentrated in the lowest bits because p+2 only requires carry propagation through trailing 1s.

General pattern: XOR popcount ≈ number of bit positions affected by adding the gap. This is NOT log2(gap)+1 as naively expected — carries cancel many bit flips.

### Strike 8: Multiplication bit correlation matrix

For 8-bit primes multiplied by 3:
- Bit 0 of n*3 strongly correlates with ALL input bits (the constant)
- Diagonal correlation (bit i -> bit i+1) from the shift
- Off-diagonal spread from carries
- The "carry mixing" is where multiplication creates non-trivial bit interactions

## DIAMOND

**Primality has almost no bit-level signature.** The popcount bias is a myth (just oddness). The autocorrelation is just coprimality. The carry structure is random.

**Two real findings:**
1. **Bit reversal preserves primality 1.5x beyond chance** — a real structural property of primes in binary representation
2. **Bit rotation by ±1 preserves primality 2.3x** — connects to Mersenne structure

Both come from the same source: primes avoid small factors, and certain bit transformations approximately preserve this avoidance. The preservation is APPROXIMATE (1.5-2.3x, not exact) because bit operations don't respect the ring structure of multiplication.

**The bit world and the number world are nearly orthogonal.** Multiplication mixes bits chaotically (the carry chain), which is why primality can't be read from bits. The small residual correlations (1.5x, 2.3x) come from the overlap between "not divisible by 2,3,5" and "certain bit patterns."

## Files
- spark_bits.py — 7-strike bit analysis
- spark_bits2.py — Deeper analysis: controls, rotation, XOR
