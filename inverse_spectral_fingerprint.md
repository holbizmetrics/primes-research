# Inverse Spectral Fingerprint

## Recovering Arithmetic from Zeros Alone

**Date:** 2026-01-30
**Status:** ~~Confirmed~~ **REJECTED** (N-stability test failed)

---

## 1. The Original Claim

**Claim:** The sign of cross-band covariance recovers whether a Dirichlet character is real or complex, using only the zeros of its L-function.

```
Sign(Cov(B₁, B₂)) < 0  →  Real character (order ≤ 2)
Sign(Cov(B₁, B₂)) > 0  →  Complex character (order > 2)
```

**Status: REJECTED** — See Section 10 for details.

---

## 2. Blind Test (at N=10⁴)

### Protocol

1. Load 8 L-functions (4 real, 4 complex characters)
2. Assign random labels A-H (blind)
3. Compute covariance from zeros only
4. Predict character type from sign
5. Unblind and check accuracy

### Results

| ID | Cov(B₁,B₂) | Prediction | Actual | Result |
|----|------------|------------|--------|--------|
| A | -0.4598 | real | real (ζ) | ✓ |
| B | -1.4830 | real | real (χ₄) | ✓ |
| C | -0.3342 | real | real (χ₃) | ✓ |
| D | -5.3496 | real | real (χ₈) | ✓ |
| E | +0.1212 | complex | complex (χ₅) | ✓ |
| F | +0.1132 | complex | complex (χ₇ ord 3) | ✓ |
| G | +4.2514 | complex | complex (χ₇ ord 6) | ✓ |
| H | +3.0679 | complex | complex (χ₁₃) | ✓ |

**Accuracy: 8/8 = 100%** *(at fixed N=10⁴)*

---

## 3. Band Robustness Analysis

### Concern
Is the result an artifact of the specific band split (15/35)?

### Test
Repeat with 6 different band configurations.

### Results

| Band Split | Real→NEG | Complex→POS | Accuracy |
|------------|----------|-------------|----------|
| B1=[1:10], B2=[11:50] | 4/4 | 4/4 | **100%** |
| B1=[1:12], B2=[13:50] | 4/4 | 4/4 | **100%** |
| B1=[1:15], B2=[16:50] | 4/4 | 4/4 | **100%** |
| B1=[1:18], B2=[19:50] | 4/4 | 4/4 | **100%** |
| B1=[1:20], B2=[21:50] | 4/4 | 4/4 | **100%** |
| B1=[1:25], B2=[26:50] | 4/4 | 3/4 | 88% |

### Summary
- **Real characters:** 24/24 negative across ALL splits
- **Complex characters:** 23/24 positive (one flip at extreme 50/50)
- **Pattern appeared robust to band choice** *(but see Section 10)*

---

## 4. Initial Council Deliberation

The result was stress-tested via PROMETHEUS v6.2 COUNCIL protocol.

### Advocate Position
- 8/8 perfect classification
- Clear theoretical mechanism (phase interference)
- Diverse sample (moduli 3,4,5,7,8,13; orders 2,3,4,6)

### Critic Concerns
- Small sample size (n=8)
- Band choice could be cherry-picked
- Some values barely positive (+0.11)

### Resolution
Robustness test addressed Critic's main concern. Pattern holds across multiple band configurations.

**Initial Council Verdict: CONFIRMED**

---

## 5. Mechanism (Proposed)

### Why Real → Negative?

Real characters satisfy χ(n) = χ̄(n):
- L-function is real on the critical line
- Zeros produce real oscillations
- **Destructive interference** between bands
- Cross-band covariance negative

### Why Complex → Positive?

Complex characters satisfy χ(n) ≠ χ̄(n):
- L-function has complex values
- Zeros have complex phase relationships
- **Constructive interference** between bands
- Cross-band covariance positive

**Note:** This mechanism was proposed but NOT rigorously derived. The N-instability suggests it may be incorrect or incomplete.

---

## 6. Original Significance Claims

### What This Would Have Meant

1. **Spectral fingerprint exists:** Zeros encode arithmetic information
2. **Inverse problem solvable:** Can recover character type from spectrum
3. **New invariant:** Cross-band covariance sign is a spectral invariant

### Implications for Hilbert-Pólya (if true)

Any operator with L-function zeros as eigenvalues must:
- Produce deterministic cross-band covariance
- Have sign determined by character type
- Encode arithmetic (real vs complex) in spectral structure

**Status:** These claims are now in doubt pending resolution of N-stability.

---

## 7. L-Functions Tested

| L-function | Modulus | Order | Type | Zeros | Cov Sign (N=10⁴) |
|------------|---------|-------|------|-------|------------------|
| ζ(s) | - | - | real | 510 | **−** |
| L(s, χ₄) | 4 | 2 | real | 122 | **−** |
| L(s, χ₃) | 3 | 2 | real | 114 | **−** |
| L(s, χ₈) | 8 | 2 | real | 60 | **−** |
| L(s, χ₅) | 5 | 4 | complex | 129 | **+** |
| L(s, χ₇) | 7 | 3 | complex | 140 | **+** |
| L(s, χ₇) | 7 | 6 | complex | 99 | **+** |
| L(s, χ₁₃) | 13 | 4 | complex | 86 | **+** |

---

## 8. Future Work (Original)

1. ~~More L-functions: Test 20+ to increase confidence~~
2. ~~Theoretical proof: Derive sign from character parity rigorously~~
3. ~~Magnitude analysis: Does |Cov| encode further information?~~
4. ~~Other L-functions: Dedekind zeta, modular forms~~
5. ~~Continuous classifier: Use Cov value for finer classification~~

**Status:** Superseded by N-stability failure.

---

## 9. Original Summary

> ~~From zeros alone, the sign of cross-band covariance perfectly predicts whether a Dirichlet character is real or complex.~~

~~This is a genuine inverse spectral result: arithmetic information recovered from pure spectral data.~~

| Input | Output | Accuracy |
|-------|--------|----------|
| L-function zeros (unlabeled) | Real vs Complex character | ~~100%~~ (8/8 at N=10⁴) |

~~Robustness confirmed across 6 band configurations.~~

---

## 10. N-STABILITY TEST (CRITICAL UPDATE)

### The Fatal Flaw

The original tests used fixed N=10⁴. A proper invariant must be stable across different window sizes.

### N-Stability Test Protocol

For each L-function, compute Cov(B₁, B₂) at N = 10², 10³, 10⁴, 10⁵, 10⁶ and check if sign is consistent.

### Results

| L-function | N=10² | N=10³ | N=10⁴ | N=10⁵ | N=10⁶ | Stable? |
|------------|-------|-------|-------|-------|-------|---------|
| ζ(s) | + | − | − | − | + | NO |
| L(s, χ₄) | − | − | − | + | + | NO |
| L(s, χ₃) | − | − | + | − | + | NO |
| L(s, χ₈) | − | − | + | + | + | NO |
| L(s, χ₅) | + | + | + | + | − | NO |
| L(s, χ₇) ord 3 | − | + | − | + | − | NO |
| L(s, χ₇) ord 6 | + | + | + | − | − | NO |
| L(s, χ₁₃) | + | + | − | + | − | NO |

### Summary

- **Stable:** 0/8
- **Unstable:** 8/8 (ALL sign flip with N)

### Second Council Deliberation

**Advocate:** "Maybe zeta is stable?"

**Critic:** "Re-test shows zeta is ALSO unstable. 0/8 are stable."

**Analyst:** "The evidence is clear: ALL L-functions have N-dependent sign. No exceptions."

**Referee Verdict:**

| Claim | Status |
|-------|--------|
| Cross-band covariance distinguishes L-functions from GUE | ✓ VALID |
| Sign predicts real vs complex | ✗ REJECTED (N-dependent) |
| Inverse spectral fingerprint | ✗ REJECTED (0/8 stable) |

---

## 11. What Survives

Despite the rejection, some findings remain valid:

1. **L-functions have deterministic cross-band covariance** — the value is reproducible for fixed parameters
2. **GUE/Poisson have stochastic covariance** — fluctuates around zero with variance
3. **This distinguishes L-functions from random matrix ensembles**

The *existence* of deterministic covariance is meaningful. The *sign* is not a reliable fingerprint.

---

## 12. Lessons Learned

1. **Test N-dependence early** — any "invariant" must survive parameter variation
2. **8/8 at one parameter is not confirmation** — could be coincidence
3. **Devil's advocate saves wasted effort** — the Critic's concerns were valid
4. **Null results are valuable** — knowing what doesn't work matters

---

## 13. Revised Summary

> **The sign of cross-band covariance is NOT a reliable spectral fingerprint for character type.**
>
> The 8/8 success at N=10⁴ was an artifact of that specific parameter choice. **All 8 L-functions** (including zeta) show sign instability across N values.

| Original Claim | Status |
|----------------|--------|
| Sign predicts character type | **REJECTED** |
| Cross-band covariance distinguishes from GUE | **VALID** |
| Zeta uniquely stable | **REJECTED** (re-test showed 0/8 stable) |

---

*Discovered 2026-01-30 | Rejected 2026-01-30 | Corrected 2026-01-30 | PROMETHEUS v6.2*
*Proper falsification is science. Proper re-verification catches errors.*

---

## 14. Successor: Attraction Strength Fingerprint

The covariance approach failed, but a new approach succeeded.

**See: `attraction_strength_fingerprint.md`**

By inverting the principle (measuring attraction instead of repulsion), a robust fingerprint was found:

| Method | Accuracy | Robust? |
|--------|----------|---------|
| Covariance sign | 8/8 at one point | No |
| **Attraction strength** | **8/8** | **Yes** |

The breakthrough came from Transformation Algebra:
```
P(repulsion) ⊗ T_inv → P(attraction)
```

*Updated 2026-01-31*
