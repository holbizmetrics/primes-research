# SPARK: Primes as Information — CAPTURE

## Session: Information theory of prime gaps
**Date:** 2026-02-06

## SPRAY (7 ideas)
1. Shannon entropy of prime gap distribution
2. Mutual information between consecutive gaps
3. Lempel-Ziv complexity of prime bitmap
4. Entropy in different bases
5. Conditional entropy ladder (history depth)
6. KL divergence from geometric (max entropy) distribution
7. Relative entropy of primes mod q vs uniform

## STRIKE Results

### Strike 1: Shannon entropy
- **H = 3.59 bits per gap** (at N=100,000)
- Geometric distribution (max entropy for same mean): 3.68 bits
- Efficiency: **97.6%** — primes are nearly maximum entropy
- Gap=6 is the dominant gap (20.2%), carrying only 2.31 bits (most predictable)

### Strike 2: Mutual information
- **MI(g_n; g_{n+1}) = 0.37 bits = 10%** of total entropy
- Miller-Madow corrected: 0.37 bits (correction small: 0.01 bits)
- Cramer model predicts MI=0 → measured MI is a DEVIATION from random
- **Most attracted pairs**: (28,2), (4,26), (2,28) — all sum to 30!
- **Most repelled pairs**: (20,12), (24,8), (18,18) — avoid same-size pairs

### Strike 3: Lempel-Ziv complexity
- Prime bitmap: **23% more compressible than random** (same density)
- LZ(primes) = 532 vs LZ(random) = 689 (bitmap length 20,000)

### Strike 4: Base entropy
- **Perfect efficiency (1.000) in EVERY base** for coprime residue classes
- This IS Dirichlet's theorem: primes equidistribute among coprime residues
- Base doesn't matter — primes look equally random in all bases

### Strike 5: Conditional entropy ladder
- k=1 history: 11% reduction (trustworthy, 16 contexts)
- k=2 history: 16% reduction (borderline, 177 contexts)
- k≥3: OVERFIT due to sparsity (6750+ contexts, 50%+ singletons)
- True entropy rate bounded by k=1 result: ~3.3 bits/gap

### Strike 6: KL divergence
- **KL(primes || geometric) = 0.088 bits**
- Dominated by gap=6 excess (+0.14 bits contribution)
- Gaps divisible by 6 are systematically over-represented
- This is the mod-6 structure: primes >3 are ≡ ±1 mod 6

### Strike 7: Relative entropy mod q
- Primes are **most random** mod small q (D_KL → 0 for q=3,5,6)
- **Least random** mod large primes (D_KL peaks at q=53, 59)
- This is trivial: more residue classes → more room for fluctuations

## DEEP STRIKES

### Lemke Oliver-Soundararajan Bias
The transition matrix of consecutive prime residues mod q reveals:
- **Mod 3**: diagonal ratio 0.80 (20% suppression of same-class repetition)
- **Mod 7**: diagonal ratio 0.38 (62% suppression)
- **Mod 30**: diagonal ratio **0.12** (88% suppression!)

Primes act like a ratchet — they strongly prefer advancing to the NEXT coprime residue class rather than staying in the same one. This is the Lemke Oliver-Soundararajan (2016) effect.

### Mod-30 Decomposition
- Knowing the residue pair (r1, r2) mod 30 determines g mod 30
- **96.8%** of gaps are the minimum possible for their residue pair
- Conditional entropy H(gap | residue_pair_mod_30) = **0.21 bits** (from 3.69)
- The 0.21 remaining bits = "how many multiples of 30 to skip" (almost always 0)

### The Killer Result: Residual Correlation
After stripping mod-30 effects (looking at gap // 30):
- **MI of reduced gaps = 0.0009 bits ≈ 0**
- ALL gap-to-gap correlation comes from residue class dynamics
- The non-periodic part of prime gaps is **truly independent**

## DIAMOND

**Prime gaps have a clean two-layer information structure:**

| Layer | Content | Bits | % of total |
|-------|---------|------|-----------|
| Residue dynamics | Which coprime class mod 30 comes next | 3.49 | 94% |
| Random remainder | How many 30-periods to skip | 0.21 | 6% |
| **Total** | | **3.69** | **100%** |

The 10% gap-to-gap mutual information (0.37 bits) is **entirely** from the residue layer. Once you remove mod-30 effects, the residual MI drops to 0.001 bits — effectively zero.

**Interpretation**: Primes are a nearly deterministic residue-class ratchet (mod 30) plus a thin layer of genuine randomness (which multiple of 30 to advance by). The "randomness of primes" is 94% structural and only 6% truly random.

This is the information-theoretic restatement of:
- Dirichlet's theorem (equidistribution → max entropy within each layer)
- Lemke Oliver-Soundararajan (residue ratchet → sequential correlations)
- Cramér model (the 6% random part behaves like independent geometric draws)

## Connection to previous SPARKs
- **Laser SPARK**: The Ramanujan coherence I_P(q) = μ²/φ² measures the same mod-q structure in Fourier space. The laser sees the 94% structural part.
- **Inside-out SPARK**: The Legendre symbol at 50% inversion maximally amplifies the residue structure.
- **Audio SPARK**: The 0.96 consonance correlation reflects that musical intervals probe the same residue layers.

## Scripts
- `spark_info.py` — Strikes 1-3 (entropy, MI, LZ)
- Inline computations for Strikes 4-7 and deep analysis

