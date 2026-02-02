# Galois Induction Coupling and Dedekind Zeta Variance

**Date:** 2026-02-03
**Status:** Empirical observation, marginally significant (p ≈ 0.06)

## Abstract

We observe that Dedekind zeta functions of non-abelian cubic extensions Q(∛d) exhibit ~11% lower spacing variance than their abelian quadratic counterparts Q(√d). We propose this arises from "Galois induction coupling" — the shared Riemann zeta factor in the Artin factorization creates correlated zeros that reduce variance.

## 1. Background

### Dedekind Zeta Factorization

For a number field K with Galois closure having group G, the Dedekind zeta function factors as:

```
ζ_K(s) = ∏_ρ L(s, ρ)^{dim(ρ)}
```

where the product runs over irreducible representations of G.

**Abelian case (Q(√d), G = C₂):**
```
ζ_{Q(√d)}(s) = ζ(s) · L(s, χ)
```
where χ is a quadratic Dirichlet character. The factors ζ and L(χ) have **independent** zeros.

**Non-abelian case (Q(∛d), G = S₃):**
```
ζ_{Q(∛d)}(s) = ζ(s) · L(s, ρ₂)
```
where ρ₂ is the 2-dimensional irreducible representation of S₃. Crucially, this arises from the induction relation:

```
Ind₁^{S₃}(1) = 1 ⊕ ρ₂
```

The **same** ζ(s) factor appears, but now its zeros are "entangled" with those of L(ρ₂) through the Galois structure.

## 2. Hypothesis

**Galois Induction Coupling:** When a Dedekind zeta function factors through a non-abelian Galois group, the shared components (particularly the Riemann zeta factor) create correlations between zeros that reduce spacing variance compared to abelian extensions where factors are independent.

### Mechanism

In Random Matrix Theory terms:
- Abelian: zeros from independent GUE matrices → variance adds
- Non-abelian: zeros from coupled/constrained matrices → variance reduced by correlation

## 3. Empirical Evidence

### Test Design

For squarefree d ∈ {2, 3, 5, 6, 7, 10, 11, 13, 15}:
1. Compute zeros of ζ_{Q(√d)} and ζ_{Q(∛d)} up to height T=60
2. Calculate normalized spacing variance for each
3. Compare abelian vs non-abelian

### Results

| d | Q(√d) Abelian | Q(∛d) Non-abelian | Δ (Ab - NonAb) |
|---|---------------|-------------------|----------------|
| 2 | 0.321 | 0.276 | +0.045 |
| 3 | 0.262 | 0.244 | +0.018 |
| 5 | 0.275 | 0.272 | +0.003 |
| 6 | 0.260 | 0.263 | -0.003 |
| 7 | 0.283 | 0.223 | +0.060 |
| 10 | 0.271 | 0.259 | +0.012 |
| 11 | 0.282 | 0.268 | +0.014 |
| 13 | 0.369 | 0.239 | +0.130 |
| 15 | 0.282 | 0.284 | -0.002 |

### Statistical Summary

```
Sample size:           n = 9 field pairs
Non-abelian lower:     7/9 cases (78%)
Mean abelian var:      0.289
Mean non-abelian var:  0.259
Mean difference:       0.031 ± 0.014
Effect size:           ~11% reduction
t-statistic:           2.15
p-value:               ≈ 0.06 (marginally significant)
```

## 4. Discussion

### Why This Might Be New

Literature search (2026-02-03) found no prior work on:
- Spacing variance differences between abelian/non-abelian extensions
- Galois structure affecting zero statistics beyond multiplicity
- "Coupling" effects from shared L-function factors

Related known results:
- Montgomery-Odlyzko: GUE statistics for individual L-functions
- Katz-Sarnak: Symmetry types for L-function families
- Miller (2006): Spacing statistics independent of elliptic curve rank

None address the specific question of how Artin factorization structure affects spacing variance.

### Caveats

1. **Sample size:** n=9 is small; p ≈ 0.06 is marginally significant
2. **Discriminant confound:** Q(∛d) has different discriminant than Q(√d)
3. **Degree effect:** Cubic vs quadratic might matter independently of Galois structure
4. **Finite height:** Effects might vanish as T → ∞

### Predictions

If the hypothesis is correct:
1. Other S₃ extensions should show similar variance reduction
2. A₄ extensions (with more complex factorization) might show even lower variance
3. The effect should persist (or strengthen) with more zeros
4. Matching discriminants should still show the effect

## 5. Future Work

1. **More data:** Test 30+ field pairs for statistical significance
2. **Height dependence:** Check if effect persists at T = 200, 500, 1000
3. **Discriminant matching:** Compare fields with similar discriminants
4. **Other Galois groups:** Test A₄, S₄, D₄ extensions
5. **Theoretical derivation:** Derive variance prediction from RMT + rep theory

## 6. Conclusion

We present empirical evidence for a novel phenomenon: non-abelian Dedekind zeta functions have lower spacing variance than abelian ones, possibly due to correlations induced by shared factors in the Artin factorization. The effect is consistent (7/9 cases) with ~11% magnitude, but requires more data for statistical confirmation.

If confirmed, this would be a new connection between Galois theory and random matrix statistics of L-function zeros.

---

## Appendix: Reproduction

```gp
\\ PARI/GP code to verify
\\ Abelian: Q(sqrt(2))
K2 = nfinit(x^2-2);
z2 = lfunzeros(lfuncreate(K2), 60);
s2 = vector(#z2-1, i, z2[i+1]-z2[i]);
m2 = vecsum(s2)/#s2;
v2 = vecsum(vector(#s2, i, (s2[i]/m2-1)^2))/#s2;
print("Q(sqrt2) variance: ", v2);

\\ Non-abelian: Q(cbrt(2))
K3 = nfinit(x^3-2);
z3 = lfunzeros(lfuncreate(K3), 60);
s3 = vector(#z3-1, i, z3[i+1]-z3[i]);
m3 = vecsum(s3)/#s3;
v3 = vecsum(vector(#s3, i, (s3[i]/m3-1)^2))/#s3;
print("Q(cbrt2) variance: ", v3);
```

## References

1. Montgomery, H. L. (1973). The pair correlation of zeros of the zeta function.
2. Katz, N. M., & Sarnak, P. (1999). Random matrices, Frobenius eigenvalues, and monodromy.
3. Miller, S. J. (2006). Investigations of zeros near the central point of elliptic curve L-functions.
4. Rudnick, Z., & Sarnak, P. (1996). Zeros of principal L-functions and random matrix theory.
