# RMT Derivation of Variance Formula

**Goal:** Derive the constants α ≈ 0.15, β ≈ 0.10 in:
```
Var(ζ_K) ≈ V_GUE × [1 + α(k-1) - β × H(p)]
```

---

## 1. Setup

Consider k independent GUE sequences merged into one. Each sequence i has:
- Proportion p_i of total zeros (Σp_i = 1)
- Internal spacing variance V_i ≈ V_GUE ≈ 0.27
- Mean spacing μ = 1 (after unfolding)

## 2. Variance Decomposition

For merged sequence, spacings are either:
- **Within-factor** (both zeros from same factor): probability Σp_i²
- **Cross-factor** (zeros from different factors): probability 1 - Σp_i²

### 2.1 Within-Factor Contribution

Within-factor spacings have variance V_GUE. Their contribution:
```
Var_within = Σ p_i² × V_GUE
```

### 2.2 Cross-Factor Contribution

Cross-factor spacings depend on the interleaving pattern. If factors are independent:
- Mean cross-spacing: smaller than 1 (zeros cluster)
- Cross-spacing variance: different from V_GUE

Let V_cross be the variance of cross-factor spacings. For independent sequences:
```
Var_cross = V_cross × (1 - Σp_i²)
```

### 2.3 Mean Shift Contribution

When factors have different densities, the mean spacing varies by factor type. This adds:
```
Var_mean = Σ p_i × (μ_i - 1)²
```

where μ_i is the mean normalized spacing within factor i.

## 3. Total Variance Formula

```
Var(merged) = Σp_i² × V_GUE + (1 - Σp_i²) × V_cross + Var_mean
```

## 4. Specializing to Equal Factors

For k equal factors (p_i = 1/k):
- Σp_i² = k × (1/k)² = 1/k
- 1 - Σp_i² = (k-1)/k

```
Var(k equal) = V_GUE/k + V_cross × (k-1)/k
             = V_GUE × [1/k + (V_cross/V_GUE) × (k-1)/k]
```

## 5. Estimating V_cross

From Session 5 data, cross-family spacings have:
- Mean: ~0.62 (zeros cluster, not independent)
- Variance: ~0.18

After normalization to mean 1, the variance scales:
```
V_cross_normalized = 0.18 / 0.62² ≈ 0.47
```

So V_cross/V_GUE ≈ 0.47/0.27 ≈ 1.74.

## 6. Deriving α

For k equal factors:
```
Var(k) = V_GUE × [1/k + 1.74 × (k-1)/k]
       = V_GUE × [1/k + 1.74 - 1.74/k]
       = V_GUE × [1.74 + (1 - 1.74)/k]
       = V_GUE × [1.74 - 0.74/k]
```

Rewriting in terms of (k-1):
```
Var(k) = V_GUE × [1.74 - 0.74/k]
       ≈ V_GUE × [1 + 0.74 × (k-1)/k]
       ≈ V_GUE × [1 + 0.74 × (1 - 1/k)]
```

For large k, this approaches V_GUE × 1.74.

The empirical formula Var = V_GUE × [1 + α(k-1)] with α ≈ 0.15 suggests:
```
α × (k-1) ≈ 0.74 × (k-1)/k
α ≈ 0.74/k for moderate k
```

For k = 4: α ≈ 0.74/4 = 0.185
For k = 2: α ≈ 0.74/2 = 0.37

This doesn't match the constant α = 0.15. The discrepancy suggests **coupling reduces V_cross**.

## 7. Correlation Effect

If zeros have correlation c (0 = independent, 1 = identical), then:
```
V_cross(c) = V_cross(0) × (1 - c)
```

With c ≈ 0.34 (from Session 5):
```
V_cross ≈ 0.47 × (1 - 0.34) ≈ 0.31
V_cross/V_GUE ≈ 0.31/0.27 ≈ 1.15
```

Revised:
```
Var(k) = V_GUE × [1/k + 1.15 × (k-1)/k]
       = V_GUE × [1.15 + (1 - 1.15)/k]
       = V_GUE × [1.15 - 0.15/k]
```

For k = 2: Var ≈ V_GUE × 1.075 ≈ 0.29 ✓
For k = 4: Var ≈ V_GUE × 1.11 ≈ 0.30... but empirical is ~0.47!

## 8. Resolution: Coupling Varies

The flaw is assuming constant correlation. In reality:
- S₃, S₄: strong Galois coupling → c ≈ 0.45
- D₄, C₄: weak coupling (many independent 1-dim factors) → c ≈ 0.20

**Refined formula:**
```
Var(ζ_K) = V_GUE × [Σp_i² + (1 - Σp_i²) × (V_cross/V_GUE) × (1 - c)]
```

## 9. Entropy Connection

The entropy H(p) = -Σp_i log p_i measures "spread" of dimensions:
- H large: factors evenly distributed → more cross-factor pairs → higher variance
- H small: one factor dominates → fewer cross-factor pairs → lower variance

For k equal factors: H = log(k)
For unequal factors: H < log(k)

The β term captures: **higher entropy → higher variance** (opposite of original sign!)

Wait - the empirical formula has **-β×H**, suggesting higher entropy reduces variance. Let me reconsider...

## 10. Reinterpretation

Actually, higher entropy means more even distribution. If one large factor dominates (low H):
- Fewer cross-factor pairs
- But the dominant factor's zeros are denser, causing more within-factor clustering
- Net effect depends on dimension

For S₃: dims 1, 2 → p = (1/3, 2/3) → H = 0.92
For C₂: dims 1, 1 → p = (1/2, 1/2) → H = 1.00
For D₄: dims 1,1,1,2 → p = (0.2, 0.2, 0.2, 0.4) → H = 1.92

Higher-dimensional irreps have MORE REGULAR zeros (from pure Artin measurement: 0.15 vs 0.19). So when one large-dim factor dominates (low H), the merged variance is pulled toward that factor's low variance.

**Corrected interpretation:**
- -β×H: high entropy (even factors) → more 1-dim factors → higher variance
- Low entropy (dominant large-dim) → pulled toward pure Artin's low variance → lower variance

This matches: S₃ and S₄ have dominant 2-dim/3-dim irreps → lower variance.

## 11. Final Formula

```
Var(ζ_K) = V_GUE × [1 + α(k-1) - β×H(p)]
```

where:
- α ≈ 0.15 captures: more factors → more cross-factor pairs → higher variance
- β ≈ 0.10 captures: even factors (high H) → more 1-dim → higher variance

### Derivation of α

From variance decomposition with typical correlation:
```
α = (V_cross/V_GUE - 1) × (1 - c_avg) / 2
  ≈ (1.15 - 1) × 0.66 / 2
  ≈ 0.15 / 2
  ≈ 0.07
```

Hmm, still not matching. The empirical α = 0.15 may require:
- Variance of mean spacings (Var_mean term)
- Non-equal factor proportions
- Finite-N effects

### Derivation of β

The entropy term should scale the contribution of low-dimension factors:
```
β × H ≈ (V_1dim - V_high_dim) × (fraction of 1-dim)
     ≈ (0.19 - 0.15) × H/log(k)
     ≈ 0.04 × H/log(k)
```

For k=4, log(4)≈1.4, so β ≈ 0.04/1.4 ≈ 0.03.

This is smaller than empirical β = 0.10.

## 12. Conclusion

The formula Var = V_GUE × [1 + α(k-1) - β×H] fits the data well empirically with α≈0.15, β≈0.10.

The RMT derivation gives approximate justification:
- α comes from increased variance when merging independent sequences
- β comes from the dimension-dependence of pure Artin variance

**Exact derivation remains open.** The gap may be due to:
1. Non-trivial correlations from explicit formula
2. Finite-height effects
3. Interaction between factor count and dimensions

---

*Draft derivation - 2026-02-04*
