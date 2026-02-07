# SPARK CAPTURE: Partial Inversion of Multiplicative Geometry

## SPRAY (7 ideas)
1. Power-map zeros: gamma_k -> gamma_k^alpha
2. Power-map geometry: log(n) -> log(n)^beta
3. Joint (alpha, beta) optimization
4. Does the Legendre half-inversion work here?
5. Peak sharpness Q as quality measure
6. Convergence: does optimal (alpha, beta) stabilize?
7. Mathematical meaning of optimal alpha

## KEY RESULTS

### The Investigation

We swept (alpha, beta) looking for a partial inversion that maximizes
the multiplicative laser signal at zeta zeros.

**Three quality measures tested:**
1. Raw signal F — diverges as alpha->0 (DC artifact). USELESS.
2. Signal/background contrast — noisy, depends on random samples.
3. Peak sharpness Q = F(at zero)/F(nearby) — BEST measure.

### What Happened

Peak sharpness Q showed maximum around alpha~1.9, beta~0.7 (Q=19).
But the definitive test revealed: **the peak is NOT reliably at gamma^alpha.**

At standard (alpha=1, beta=1) with N=800:
- The ACTUAL peak in F(t) is at t~9-11, NOT at gamma_1=14.13
- F(gamma_1) is only 48-65% of the max
- The "high Q" at (1.9, 0.7) was accidental — gamma^1.9 happened to
  land on a noise fluctuation

### The Convergence Test

```
N= 300: peak at t=10.0 (gamma_1=14.13), F(g1)/F(peak)=0.56
N= 700: peak at t=10.9,                  F(g1)/F(peak)=0.65
N=1500: peak at t=10.5,                  F(g1)/F(peak)=0.48
```

The peak does NOT converge to gamma_1 as N grows (with N this small).
The false peak at t~10 is from low-frequency buildup.

### The Mathematical Meaning of alpha=2

The one real insight: alpha=2 has special meaning.

Under n^(-s) -> n^(-alpha*s):
- alpha=1: sigma = 1/2 (critical line) — standard
- alpha=2: sigma = 1.0 (convergence boundary)
- alpha=0: sigma = 0 (trivial)

At alpha=2, we probe the BOUNDARY of absolute convergence of the
Dirichlet series. Terms barely converge, so zero fluctuations
become relatively larger. This explains the apparent "sharpening"
at alpha~2: not better signal, but less damping.

Also: gamma_k^2 is the diagonal of the pair correlation matrix
(the self-pair term in Selberg's trace formula).

## DIAMOND

**Partial inversion of the multiplicative geometry does NOT produce
a Legendre-style optimal point.**

The additive world has a clean answer: the Legendre symbol at
k=(q-1)/2 maximally amplifies the Ramanujan signal. 100% hit rate.

The multiplicative world does NOT have this. The reasons:
1. With finite N, the multiplicative laser doesn't cleanly resolve zeros
2. The "optimal" (alpha, beta) is noise-dependent, not convergent
3. Alpha=2 has mathematical meaning (convergence boundary) but
   doesn't actually improve signal quality
4. The zeros are GUE-correlated, so there's no multiplicative analog
   of the clean factorization that makes Legendre work

**The inside-out symmetry is an ADDITIVE phenomenon.**
It works because primes distribute evenly in (Z/qZ)* and the
Legendre symbol is the natural 2-to-1 fold of that group.
There is no analogous group structure on the zeta zeros.

## What Survived
- Alpha=2 connects to convergence boundary (sigma=1.0)
- Inversion preserves zero consonance (just reverses order)
- The multiplicative laser needs N >> 1000 to resolve zeros
- Half-inversion compresses intervals (audible)

## What Fell Off
- (alpha=1.9, beta=0.7) as optimal — noise fitting
- "Q=19" peak sharpness — accidental alignment
- Convergence of optimal (alpha, beta) — doesn't converge
- Legendre-style half-inversion for zeros — doesn't exist

## Audio Files
- 13_zero_tones.wav — individual zero pitches
- 14_zero_consonance.wav — consonant pairs (near-rational ratios)
- 15_zero_chord.wav — all 10 zeros as chord
- 16_explicit_formula.wav — psi(x)-x as waveform
- 17_inverted_zeros.wav — 1/gamma_k pitches (reversed)
- 18_normal_vs_inverted.wav — side by side comparison
- 19_destructive_vs_constructive.wav — interference patterns
- 20_zero_inversion_sweep.wav — alpha from 1 to -1
