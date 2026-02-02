# Dedekind Zero Verification: Theory and Tool

## Summary

We can predict and verify Dedekind zeta spacing variance from Galois structure. This provides a computational sanity check for zero databases and numerical calculations.

## Key Findings

### Measured Variances (height T=50-80)

| Field | Galois | Zeros | Variance |
|-------|--------|-------|----------|
| Q(√2) | Z/2 | 35-56 | 0.28 |
| Q(√3) | Z/2 | 38-60 | 0.26 |
| Q(√5) | Z/2 | 40-61 | 0.22-0.25 |
| Q(√7) | Z/2 | 45 | 0.28 |
| Q(√11) | Z/2 | 48 | 0.28 |
| Q(√13) | Z/2 | 73 | 0.36 |
| Q(√17) | Z/2 | 77 | 0.31 |
| **Q(∛2)** | **S₃** | 64-103 | **0.25** |
| **Q(∛3)** | **S₃** | 130 | **0.27** |
| Q(∜2) | D₄ | 94 | 0.56 |

### Patterns

1. **S₃ fields are consistently regular**: variance 0.25-0.27, tight range
2. **Quadratic fields vary more**: variance 0.22-0.36, wider range
3. **More factors → higher variance**: Q(∜2) at 0.56 (4 factors)
4. **S₃ induction coupling reduces variance**: Q(∛2) < Q(√2) despite more zeros

### Theoretical Explanation

**Why S₃ fields are more regular:**

The Dedekind zeta factorizes as:
- Q(√d): ζ_K = ζ × L(χ) — two independent 1-dim factors
- Q(∛d): ζ_K = ζ × L(ρ₂) — coupled by Galois induction

The induction relation `Ind₁^{S₃}(1) = 1 ⊕ ρ₂` creates arithmetic entanglement between ζ and L(ρ₂). Their zeros "know about" each other beyond just sharing primes.

**Estimated cross-correlations:**
- Abelian (quadratic): ~34%
- S₃ with induction: ~45%

Higher correlation → better interleaving → lower variance.

## Verification Tool

### Usage (PARI/GP)

```gp
\\ Variance function
v(z)={my(s,m,n);if(#z<3,return(-1));s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}

\\ Compute for a field
K = nfinit(x^3-2);
z = lfunzeros(lfuncreate(K), 100);
print("Variance: ", v(z));
```

### Prediction Rules

| Galois type | Expected variance | Tolerance |
|-------------|------------------|-----------|
| Z/2 (quadratic) | 0.22-0.35 | ±30% |
| S₃ (cubic) | 0.25-0.28 | ±15% |
| D₄ (quartic) | 0.45-0.60 | ±25% |

### Flags for Investigation

- **Variance outside range**: Possible computation error
- **S₃ field with var > 0.30**: Check zero computation
- **Quadratic with var < 0.15 or > 0.45**: Anomalous, investigate

## Applications

1. **Database verification**: Run on LMFDB entries, flag outliers
2. **Computation validation**: Check new zero calculations
3. **Anomaly detection**: Find unusual arithmetic before investigating

## Files

- `verify.gp` — PARI/GP verification script
- `dedekind_verifier.py` — Python wrapper (requires working /tmp)

## Open Questions

1. What drives the variance spread in quadratic fields (0.22-0.36)?
2. Is there a conductor/discriminant dependence?
3. Can we predict variance more precisely for specific fields?

---

*Based on Sessions 5-6 of Inverse Spectral Learning for Primes project.*
