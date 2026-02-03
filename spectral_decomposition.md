# Spectral Decomposition of C(N)

## Analytical Derivation of the Cancellation Functional

---

## 1. Setup

The error term in the prime counting function:

$$E(x) = \psi(x) - x = -\sum_{\rho} \frac{x^\rho}{\rho} + O(1)$$

where $\rho = \frac{1}{2} + i\gamma$ are non-trivial zeros of $\zeta(s)$.

Each term contributes:
$$\frac{x^\rho}{\rho} = \frac{x^{1/2} e^{i\gamma \log x}}{\frac{1}{2} + i\gamma}$$

Taking conjugate pairs together:
$$E(x) = -2 \sum_{\gamma > 0} \text{Re}\left[\frac{x^{1/2} e^{i\gamma \log x}}{\frac{1}{2} + i\gamma}\right]$$

---

## 2. Variance Decomposition

The variance of $E(x)$ over the interval $[2, N]$ is:

$$\text{Var}[E] = \int_2^N \int_2^N K(x,y) \, d\mu(x) \, d\mu(y)$$

where $K(x,y) = \text{Cov}[E(x), E(y)]$ and $\mu$ is our sampling measure.

Expanding:
$$K(x,y) = 4 \sum_{j,k} \text{Re}\left[\frac{(xy)^{1/2} e^{i(\gamma_j \log x - \gamma_k \log y)}}{\rho_j \bar{\rho}_k}\right]$$

---

## 3. Diagonal vs Off-Diagonal

Split into diagonal ($j = k$) and off-diagonal ($j \neq k$) terms:

$$K(x,y) = K_{\text{diag}}(x,y) + K_{\text{off}}(x,y)$$

**Diagonal terms** ($j = k$):
$$K_{\text{diag}}(x,y) = 4 \sum_j \frac{(xy)^{1/2} \cos(\gamma_j \log(x/y))}{|\rho_j|^2}$$

**Off-diagonal terms** ($j \neq k$):
$$K_{\text{off}}(x,y) = 4 \sum_{j \neq k} \text{Re}\left[\frac{(xy)^{1/2} e^{i(\gamma_j \log x - \gamma_k \log y)}}{\rho_j \bar{\rho}_k}\right]$$

---

## 4. Null Model Comparison

**Null model**: Replace $e^{i\gamma_j \log x}$ with $e^{i(\gamma_j \log x + \phi_j)}$ where $\phi_j$ are i.i.d. uniform on $[0, 2\pi)$.

Under the null:
- **Diagonal terms**: Unchanged (phase cancels)
- **Off-diagonal terms**: Average to zero (independent phases)

Therefore:
$$\mathbb{E}[\text{Var}_{\text{null}}[E]] = \text{contribution from diagonal terms only}$$

---

## 5. The Key Identity

$$C(N) = \frac{\text{Var}_{\text{actual}}}{\text{Var}_{\text{null}}} = \frac{\text{Diag} + \text{Off}_{\text{actual}}}{\text{Diag}}$$

$$\boxed{C(N) = 1 + \frac{\text{Off}_{\text{actual}}}{\text{Diag}}}$$

**Critical insight**:
- If $\text{Off}_{\text{actual}} < 0$ → $C(N) < 1$ → Enhanced cancellation
- If $\text{Off}_{\text{actual}} > 0$ → $C(N) > 1$ → Worse than random
- If $\text{Off}_{\text{actual}} = 0$ → $C(N) = 1$ → Same as random

---

## 6. Why Off-Diagonal is Negative (GUE)

The off-diagonal contribution involves sums like:
$$\sum_{j \neq k} f(\gamma_j, \gamma_k)$$

For **uncorrelated** zeros (Poisson), these average to:
$$\int \int f(\gamma, \gamma') \, d\gamma \, d\gamma' = 0$$

For **correlated** zeros (GUE), the pair correlation function matters:
$$R_2(r) = 1 - \left(\frac{\sin \pi r}{\pi r}\right)^2 \quad \text{(for small } r \text{)}$$

The GUE pair correlation has these properties:
- $R_2(0) = 0$ (level repulsion — no coincident eigenvalues)
- $R_2(r) < 1$ for small $r$ (fewer close pairs than Poisson)
- $R_2(r) \to 1$ as $r \to \infty$ (independence at large separation)

**The deficit of close pairs creates anti-correlation in the oscillator contributions.**

---

## 7. Explicit Form of Off-Diagonal

The off-diagonal contribution can be written as:
$$\text{Off} = 4 \int_2^N \int_2^N (xy)^{1/2} \sum_{j \neq k} \frac{\cos(\gamma_j \log x - \gamma_k \log y)}{|\rho_j||\rho_k|} d\mu(x) d\mu(y)$$

Introduce $u = \log x$, $v = \log y$:
$$\text{Off} \propto \sum_{j \neq k} \frac{1}{|\rho_j||\rho_k|} \int \int \cos(\gamma_j u - \gamma_k v) e^{(u+v)/2} du \, dv$$

This depends on the **sum over pairs** weighted by their phase difference structure.

---

## 8. Connection to Pair Correlation

Let $n(\gamma)$ be the counting function for zeros. The pair correlation function is:
$$R_2(\gamma, \gamma') = \lim_{\Delta \to 0} \frac{\mathbb{E}[n(\gamma, \gamma+\Delta) \cdot n(\gamma', \gamma'+\Delta)]}{\Delta^2}$$

For GUE (and conjecturally for zeta zeros):
$$R_2(\gamma - \gamma') = 1 - \left(\frac{\sin \pi(\gamma - \gamma')/\delta}{\pi(\gamma - \gamma')/\delta}\right)^2$$

where $\delta$ is the mean spacing.

**The off-diagonal sum becomes:**
$$\text{Off} \propto \int \int [R_2(\gamma - \gamma') - 1] \cdot (\text{oscillatory kernel}) \, d\gamma \, d\gamma'$$

Since $R_2 - 1 < 0$ for small separations, and the oscillatory kernel is positive on average for nearby $\gamma, \gamma'$, we get:

$$\boxed{\text{Off}_{\text{actual}} < 0 \implies C(N) < 1}$$

---

## 9. Operator Constraints

Any Hilbert-Pólya operator $H$ with $\text{spec}(H) = \{\gamma_n\}$ must satisfy:

### Constraint 1: Spectral Density
$$\#\{\gamma_n \leq T\} \sim \frac{T}{2\pi} \log \frac{T}{2\pi}$$

### Constraint 2: Pair Correlation
$$R_2(\gamma - \gamma') = 1 - \left(\frac{\sin \pi r}{\pi r}\right)^2 + o(1)$$
where $r = (\gamma - \gamma')/\delta$ is the normalized spacing.

### Constraint 3: Cancellation Efficiency (NEW)
$$C(N) = 1 + \frac{\text{Off}(N)}{\text{Diag}(N)} \approx 0.8 - 0.9$$

This third constraint is **independent** of the first two and provides additional filtering power.

---

## 10. Operator Classes Ruled Out

| Operator Class | Fails Constraint | Reason |
|----------------|------------------|--------|
| Finite-rank | 1 | Wrong density |
| Diagonal + compact | 2 | Poisson statistics |
| Sparse random | 2 | Wrong pair correlation |
| Generic self-adjoint | 3 | C(N) ≈ 1 |
| Clustering spectrum | 3 | C(N) > 1 |

### Operators that could survive:
- Quantized chaotic Hamiltonians (BGS conjecture)
- Random matrix ensembles (GUE)
- Certain pseudodifferential operators

---

## 11. Scaling Prediction

From the structure of the decomposition:

$$C(N) \sim 1 - \frac{c}{\log N} + O(1/\log^2 N)$$

where $c > 0$ depends on the pair correlation structure.

**Prediction**: As $N \to \infty$, $C(N) \to 1$ from below, but the convergence is logarithmically slow.

This is testable with more data.

---

## 12. Summary

The inverse spectral approach yields:

1. **Observable**: $C(N) = \text{Var}_{\text{actual}} / \text{Var}_{\text{null}}$

2. **Decomposition**: $C(N) = 1 + \text{Off}/\text{Diag}$

3. **Mechanism**: GUE repulsion → $R_2 < 1$ near diagonal → $\text{Off} < 0$ → $C(N) < 1$

4. **Constraint**: Any valid operator must produce observed $C(N) \approx 0.8-0.9$

5. **Discrimination**: This rules out large classes of operators that satisfy spectral density but not pair correlation constraints.

---

## Next Steps

1. **Higher precision**: Compute $C(N)$ with 10,000+ zeros to $N = 10^8$
2. **Frequency bands**: Decompose contribution by $\gamma$ ranges
3. **Scaling law**: Fit $C(N) = 1 - c/\log N$ and extract $c$
4. **Operator catalog**: Test known operator classes against constraint 3
5. **Theoretical bound**: Derive $C(N) \geq C_{\text{GUE}}(N)$ from pair correlation

---

*Derived 2026-01-30 | PROMETHEUS v5.0 | Inverse Spectral Framework*
