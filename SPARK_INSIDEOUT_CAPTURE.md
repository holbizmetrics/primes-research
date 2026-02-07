# SPARK: Inside-Out Geometries — CAPTURE

## Session: Turning geometries inside out
**Date:** 2026-02-06

## SPRAY (7 ideas)
1. Full sphere inversion n → N/n
2. Conformal map on prime positions
3. Modular inversion τ → -1/τ
4. Reciprocal primes {1/p}
5. Fourier transform of 1/p
6. Möbius inversion on prime sums
7. Modular inverse primes p → p⁻¹ mod q

## STRIKE Results

### Strike 1: Full inversion n → N/n
- **Result:** Destroys all structure. Inverted primes cluster near small values.
- P/C ratio ≈ 0.8 universally — no Ramanujan structure survives.
- **Verdict:** Additive inversion is destructive.

### Strike 4: Reciprocal primes 1/p
- **Result:** All 1/p cluster near 0 (most primes are large).
- Laser gives near-perfect coherence at all wavelengths — but it's just clustering, not structure.
- **Verdict:** Trivial concentration effect.

### Strike 5: Fourier of 1/p
- **Result:** Smooth monotone decay from ξ=1 to ξ=60.
- No peaks, no structure. Reciprocal map destroys arithmetic information.
- **Verdict:** Dead end.

### Strike 7: Modular inverse p → p⁻¹ mod q → LED TO BREAKTHROUGH
- **Result:** I_orig ≈ I_inv for all q! Primes symmetric under modular inversion.
- This led to the deep analysis below.

## DEEP STRIKES

### Deep A: Phase analysis
- The phase Δ between A_P(q) and A_inv(q) varies — NOT consistently 0 or π.
- The intensity equality is approximate, not exact.

### Deep B: Character theory (PARTIALLY wrong)
- Initial claim: |A|² always preserved under inversion (character conjugation).
- Verification with random subsets showed this is FALSE for arbitrary sets.
- The near-equality for primes reflects their equidistribution mod q (Dirichlet).

### Deep C: Which maps break symmetry?
- **Negation** (p → -p): preserves |A|² exactly (trivial conjugation)
- **Inversion** (p → p⁻¹): preserves approximately
- **Squaring** (p → p²): MASSIVELY amplifies signal (8-30×)
- **Doubling** (p → 2p): preserves approximately

### Deep D: Multiplicative Fourier
- Multiplicative characters give tiny signals (I < 0.001)
- The Legendre character gives the largest multiplicative signal
- Discrete logs of primes are very uniformly distributed (χ² well below expectation)

## THE BREAKTHROUGH: Partial Inside-Out Spectrum

### The power map p → p^k mod q
Sweeping k from 1 to q-2, the laser intensity I(k,q) reveals:

**The optimal exponent is ALWAYS k = (q-1)/2 — exactly 50% of full inversion.**

This is the **Legendre symbol** (p/q).

| q  | Best k | Fraction | I(best) |
|----|--------|----------|---------|
| 7  | 3      | 0.500    | 0.389   |
| 11 | 5      | 0.500    | 0.708   |
| 13 | 6      | 0.500    | 0.784   |
| 17 | 8      | 0.500    | 0.870   |
| 23 | 11     | 0.500    | 0.927   |
| 29 | 14     | 0.500    | 0.954   |
| 37 | 18     | 0.500    | 0.971   |
| 43 | 21     | 0.500    | 0.979   |
| 47 | 23     | 0.500    | 0.982   |

100% hit rate: the Legendre symbol IS the optimal "half inside-out."

### The full spectrum for q=29
```
k=14: I=0.954  ████████████████████████████████████████
k= 4: I=0.168  ███████
k= 8: I=0.175  ███████
k=12: I=0.161  ██████
k=16: I=0.169  ███████
k=20: I=0.167  ██████
k=24: I=0.171  ██████
(all others < 0.03)
```

The secondary peaks at k = 4, 8, 12, 16, 20, 24 correspond to the **quartic residue symbol** (since gcd(4, 28) = 4, these create a 4-fold symmetry).

### Fractional sweep
Sweeping α continuously from 0% to 100% of full inversion:
- α = 0%: I = 1.0 (trivial, all → 1)
- α = 50%: I ≈ 0.95-0.98 (MASSIVE peak = Legendre)
- α = 100%: I = 1.0 (trivial, Fermat)
- Everything else: I < 0.05

## DIAMOND

**The "half inside-out" of prime arithmetic is the Legendre symbol.**

The inside-out spectrum I(k, q) — sweeping the power map p → p^k mod q — has a single dominant non-trivial peak at k = (q-1)/2, which is exactly the Legendre symbol (p/q) = p^((q-1)/2) mod q.

This means:
1. Primes, when "folded" onto the quadratic residues by squaring, concentrate maximally
2. The 50% inversion (not full, not zero) extracts the most information
3. The secondary structure (peaks at k = (q-1)/d) = higher power residue symbols
4. The spectrum I(k,q) over k IS the Fourier decomposition of the prime indicator function on the dual group of (Z/qZ)*

**Why this matters:** It provides a computational/physical interpretation of quadratic reciprocity — the Legendre symbol is the optimal signal amplifier for primes, not because of algebraic convention, but because it's the unique halfway point in the "inside-out" transformation.

## Connection to previous SPARKs
- **Polyhedra SPARK:** The prime factor lattice lives on an infinite-dim hypercube. The inside-out here is along each axis.
- **Audio SPARK:** The consonance-coherence correlation (0.96) reflects that musical intervals are partial foldings of the harmonic series.
- **Twin prime SPARK:** The singular series S₂(q) appears as the overtone spectrum. The inside-out adds power residue structure on top.

## Scripts
- `spark_insideout.py` — Strikes 1, 4, 5, 7
- `spark_insideout2.py` — Deep A-D (character theory, symmetry maps, discrete log)
- `spark_insideout3.py` — Deep E-H (squaring fold, power sweep, fractional)
- `spark_insideout_partial.py` — The breakthrough: partial inside-out spectrum
