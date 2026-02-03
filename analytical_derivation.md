# Analytical Derivation: Why ZETA Has Deterministic Cross-Band Covariance

## The Observation

| System | Cov(B1,B2) | Variance |
|--------|------------|----------|
| ZETA | -0.071 | 0 (deterministic) |
| GUE | ~0 | 0.44 (fluctuates) |
| Poisson | ~0 | 0.91 (fluctuates) |

**Key finding**: ZETA has a specific, deterministic value. Random models have zero mean with high variance.

---

## Why Random Models Have Zero Mean

### Setup

Define the contribution from zero γ to E(x):
$$f_\gamma(x) = -2 \cdot \text{Re}\left[\frac{x^{1/2} e^{i\gamma \log x}}{1/2 + i\gamma}\right]$$

The cross-band covariance between bands B1 and B2:
$$\text{Cov}(B1, B2) = \int \left(\sum_{\gamma \in B1} f_\gamma(x)\right) \left(\sum_{\gamma' \in B2} f_{\gamma'}(x)\right) d\mu(x) - \mu_1 \mu_2$$

where $\mu$ is our sampling measure.

### For Random Zeros

If zeros are placed randomly (Poisson or GUE), then for any fixed bands B1, B2:
- The phase relationships between zeros in B1 and zeros in B2 are **random**
- Over different realizations, these phases average out
- Therefore: $\mathbb{E}[\text{Cov}(B1, B2)] = 0$

The variance comes from the fluctuations around this zero mean.

**GUE has smaller variance than Poisson** because the repulsion constrains the phase relationships somewhat, but the mean is still zero.

---

## Why ZETA Has a Specific Non-Zero Value

### The Explicit Formula Constraint

ZETA zeros satisfy:
$$\psi(x) - x = -\sum_\rho \frac{x^\rho}{\rho} + O(1)$$

This is not just any function — it equals the **prime counting error**.

### The Prime Error Has Structure

The function $\psi(x) - x$ has specific properties:
1. **Jumps** at prime powers: $\psi(p^k) - \psi(p^k - \epsilon) = \log p$
2. **Bounded oscillation**: $|\psi(x) - x| = O(x^{1/2 + \epsilon})$
3. **Multiplicative structure**: tied to the prime factorization of integers

### This Forces Phase Relationships

For the sum $\sum_\rho x^\rho/\rho$ to equal $\psi(x) - x$ at **every** x:
- The zeros cannot have arbitrary phases
- The phases must be **precisely tuned** to produce the jumps at prime powers
- This tuning is **deterministic** — the same for every realization (there's only one set of zeta zeros)

### Consequence for Cross-Band Covariance

The phase tuning required by the explicit formula creates **specific correlations** between zeros in different bands.

Let $\gamma_1 \in B1$ and $\gamma_2 \in B2$. Their contributions to E(x):
$$f_{\gamma_1}(x) \cdot f_{\gamma_2}(x) \propto \cos((\gamma_1 - \gamma_2) \log x + \phi)$$

For random zeros, the phase $\phi$ is random, so the average is zero.

For ZETA zeros, the phases are **fixed** by the requirement that:
$$\sum_\gamma f_\gamma(x) = \psi(x) - x$$

This constraint determines $\phi$, making the covariance deterministic and (empirically) negative.

---

## The Sign of the Covariance

### Why Negative?

The explicit formula requires that:
1. E(x) = ψ(x) - x has **bounded oscillation** (no runaway growth)
2. The oscillations **cancel** on average to give $O(x^{1/2})$ growth

For this to happen:
- When low-frequency contributions (B1) are positive, higher-frequency contributions must tend to be negative
- This creates **destructive interference** across the spectrum
- Destructive interference = negative covariance

### Formal Argument

Consider the variance of E(x):
$$\text{Var}[E] = \sum_{j,k} \text{Cov}(f_{\gamma_j}, f_{\gamma_k})$$

If Var[E] is **minimized** (tight bound on oscillation), then:
- Off-diagonal covariances must be **as negative as possible**
- This includes cross-band covariances

The explicit formula effectively **minimizes** the error variance, forcing negative cross-band covariances.

---

## Summary

### Random Models (GUE, Poisson)
- No constraint on the sum
- Phase relationships are random
- Cross-band covariance averages to zero
- High variance across realizations

### ZETA Zeros
- Explicit formula constrains the sum to equal ψ(x) - x
- Phase relationships are determined by this constraint
- Cross-band covariance has a specific, deterministic value
- The value is negative because the constraint minimizes oscillation variance

---

## Mathematical Formulation

**Theorem (informal)**: Let {γ_n} be the imaginary parts of zeta zeros. Define bands B1 = {γ : γ < c1} and B2 = {γ : c1 ≤ γ < c2}. Then:

$$\text{Cov}\left(\sum_{\gamma \in B1} f_\gamma, \sum_{\gamma \in B2} f_\gamma\right) = C_{12}$$

where $C_{12}$ is a **specific constant** (not zero, not random) determined by:
1. The positions of the zeros (which satisfy RH and the explicit formula)
2. The requirement that the sum equals ψ(x) - x

For random zeros (GUE or Poisson) with the same density:
$$\mathbb{E}[\text{Cov}(\cdot, \cdot)] = 0$$

**The non-zero value of $C_{12}$ for zeta zeros is the signature of the explicit formula constraint.**

---

## Implications

1. **This is not about repulsion** — GUE has repulsion but zero mean covariance
2. **This is not about density** — Poisson has matching density but zero mean
3. **This is about the arithmetic constraint** — the explicit formula forces specific phase relationships

Any Hilbert-Pólya operator must:
- Have eigenvalues that satisfy the explicit formula
- Therefore have the same deterministic cross-band covariances
- Therefore NOT be a generic GUE or Poisson model

---

*Derived 2026-01-30 | PROMETHEUS v5.0*
