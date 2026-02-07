# SPARK CAPTURE: Multiplicative Geometry + Zeta Zero Overtones

## SPRAY (7 ideas)
1. Zero harmonics — peaks at multiples of gamma_1?
2. Zero-zero cross-coherence — factorizable like additive comb?
3. Pair correlation — GUE overtone spectrum of zero spacings
4. Explicit formula as overtones — each zero = one tone
5. Multiplicative sphere — map via log(n), not n
6. Resonance Q-factors — how sharp is each zero's peak?
7. Zero triplets — do overtone triads resonate?

## KEY RESULTS

### The Two Worlds of Primes

**Additive World (Ramanujan):**
- Frequency comb with independent teeth at squarefree q
- Cross-coherence **FACTORIZES** perfectly (CV ~ 0)
- Phase: binary (0 or pi), encodes Mobius function
- Intensities: 1/phi(q)^2 — closed form
- Position function: n (integers)
- Probe: exp(2*pi*i*n/q)

**Multiplicative World (Riemann):**
- Resonance spectrum with peaks at zeta zeros gamma_k
- Cross-coherence **DOES NOT FACTORIZE** (CV = 2.74)
- Phase: continuous, varies per zero
- Amplitudes: |A| ~ 17, 12, 9, 10... — NO closed form per zero
- Position function: log(n)
- Probe: n^{-s} = exp(-s*log(n))

### Overtone Findings

1. **Zeros are NOT harmonics.** 2*gamma_1 = 28.27 is NOT near any zero.

2. **Zero ratios near simple fractions** = "consonance":
   - gamma_1/gamma_2 ~ 2/3 (quality 55)
   - gamma_1/gamma_5 ~ 3/7 (quality 193)
   - gamma_3/gamma_6 ~ 2/3 (quality 212)
   These create periodic alignment of oscillations.

3. **Two-zero probes** show constructive/destructive interference:
   - (g4, g5) strongly constructive (excess 1.97)
   - (g3, g4) almost perfectly destructive (excess 0.04!)
   - Pattern encodes pair correlation function

4. **Sum frequencies** (gamma_i + gamma_j): no significant peaks
5. **Difference frequencies**: huge but artifact (DC leakage for small t)
6. **SFF shows GUE linear ramp** at small tau (K ~ tau), confirming GUE

### 3D Geometry Findings

7. **Golden sphere z-coordinate is a disguised additive laser:**
   z(n) = 1 - 2n/N is linear in n, so F(t) with f(n)=z(n) is really
   the additive laser at wavelength q = N/(2t). NOT multiplicative.

8. **Ulam 3D spiral** separates zeros 10x better than golden sphere
   or factor coordinates (mean distance 0.42 vs 0.04)

9. **Factor coordinates (v2, v3, v5)** map ALL primes to the origin!
   Primes have no factors of 2, 3, or 5 (except the primes themselves).
   So the natural multiplicative geometry collapses for primes.

10. **No 3D geometry adds to the multiplicative structure.**
    Lambda lives on a 1D manifold: the log-line.
    All 3D mappings are additive decorations.

## DIAMOND

The additive prime comb and multiplicative zero spectrum are connected
by the explicit formula, but they have fundamentally different structure:

- **Additive**: independent, factorizable, binary phase, closed form
- **Multiplicative**: entangled, non-factorizable, continuous phase, no closed form

The "overtone consonance" between zeta zeros (their near-rational ratios)
is the multiplicative analog of musical consonance. It creates patterns
of constructive and destructive interference that encode GUE statistics.

**No 3D geometry enhances either structure.** The additive world is integers,
the multiplicative world is log-integers. Both are 1D.

## What Survived
- Cross-coherence non-factorization (verified, CV=2.74)
- Near-rational zero ratios creating overtone resonance
- Constructive interference at x~299 (but 299=13*23, not special)
- GUE linear ramp in SFF
- Explicit formula as bridge between worlds

## What Fell Off
- z_golden as multiplicative probe (it's additive in disguise)
- 3D prime explorer as mathematically meaningful (just visualization)
- Factor coordinates for primes (all primes at origin)
- DIFF frequency peaks (DC leakage, not resonance)
- Sum frequency resonances (no significant peaks)

## Files
- spark_mult_geometry.py — Main 7-strike analysis
- mult3d_a.py — Geometry comparison + cross-coherence
- mult3d_b.py — Overtone combinations + interference hotspots
- mult3d_c.py — 3D explorer + zero coupling + two-zero probes
