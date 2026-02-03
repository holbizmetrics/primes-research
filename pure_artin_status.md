# Pure Artin L-function Variance: Status

**Date:** 2026-02-03
**Status:** ✅ MEASURED — Surprising result!

---

## Result

**Pure Artin L(s, ρ₂) variance = 0.150** (at T=100, n=131 zeros)

This is LOWER than:
- Riemann zeta: 0.186 (same height)
- GUE expectation: ~0.27

## Method

Used splitting field approach:
```gp
P = polcompositum(x^3-2, polcyclo(3))[1];  \\ degree 6 splitting field
nf = nfinit(P);
gal = galoisinit(P);
rho = [2, 0, -1];  \\ character of 2-dim irrep on [e, (123), (12)]
L = lfunartin(nf, gal, rho, 1);
z = lfunzeros(L, 100);  \\ 131 zeros
```

## Data

| L-function | T | Zeros | Variance |
|------------|---|-------|----------|
| Pure Artin L(ρ₂) | 60 | 69 | 0.137 |
| Pure Artin L(ρ₂) | 100 | 131 | **0.150** |
| Riemann ζ | 60 | 13 | 0.134 |
| Riemann ζ | 100 | 29 | 0.186 |
| Dedekind Q(∛2) | 60 | 82 | 0.275 |

## Interpretation

**Overturns previous conjecture!**

Old hypothesis: Pure Artin ~0.27 (GUE), Dedekind lower due to coupling.

**New finding:** Pure Artin has LOWER variance than zeta. The Dedekind (merged) variance is HIGHER than its components.

This suggests:
1. Higher-dim Artin representations have intrinsically more regular zeros
2. Merging zeros (Dedekind = ζ × L(ρ₂)) INCREASES variance toward GUE
3. The "coupling" effect is the opposite of what we thought

---

## Original Analysis (Superseded)

---

## Why This Matters

The Galois coupling paper conjectures that variance depends on factor structure. We have:
- Dedekind ζ_{Q(∛2)} = ζ × L(ρ₂) → var ≈ 0.25

If the conjecture is correct:
- ζ alone → var ≈ 0.27 (GUE)
- L(ρ₂) alone → var ≈ 0.27 (GUE)
- Merged → var < 0.27 (coupling reduces variance)

Measuring L(ρ₂) directly would verify this.

---

## Technical Barriers

### 1. PARI/GP's `lfunartin`

Requires:
- `nf`: nfinit structure for the field
- `gal`: galoisinit structure for splitting field
- `rho`: character values on conjugacy classes
- `n`: cyclotomic field order for character

**Problem:** `galoisinit(x^3-2)` returns 0 because x³-2 doesn't split over Q.

The Galois closure is degree 6 (S₃), but PARI needs the polynomial to split.

### 2. Splitting Field Approach

Could use the degree-6 splitting field polynomial, but:
- Need to identify the correct polynomial
- Then identify the 2-dim representation

This is non-trivial and requires deeper Galois theory computation.

### 3. LMFDB

The LMFDB (L-functions and Modular Forms Database) has Artin L-function data, but:
- Web access from this environment is limited
- Would need API access or downloaded data

---

## Extraction Method (Indirect)

We can estimate by:
1. Compute ζ_{Q(∛2)} zeros
2. Compute ζ zeros
3. "Remove" ζ zeros from merged sequence

**Problem:** This doesn't give the true L(ρ₂) spacing distribution because:
- The zeros interleave in a correlated way
- Removing every other zero changes statistics
- Cross-family repulsion affects both sets

---

## What We Know

From Dedekind measurements:
- ζ_{Q(∛2)} has lower variance than ζ_{Q(√2)}
- This is attributed to Galois induction coupling
- The 2-dim Artin L(ρ₂) contributes 2/3 of the zeros

**Conjecture (unverified):** Pure L(ρ₂) has variance ~0.27 (GUE), same as any single L-function.

---

## Next Steps

1. **LMFDB download:** Get Artin L-function zeros directly
2. **Splitting field approach:** Construct degree-6 polynomial for S₃ closure
3. **Alternative computation:** Use SageMath or Magma which may have better Artin support

---

## Conclusion

Pure Artin variance measurement remains **OPEN** due to technical barriers in PARI/GP. The indirect evidence (Dedekind measurements + theory) suggests pure Artin L-functions should have GUE-like variance (~0.27), with the lower Dedekind variance arising from cross-factor coupling.

---

*Status note 2026-02-03*
