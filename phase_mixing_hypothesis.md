# The Phase-Mixing Hypothesis

## A Standalone Formalization

---

## 1. Motivation

Lemma 1 (Random-Zero Lemma) relies on the assumption that for random zero ensembles, the phases of spectral contributions from different zeros are "effectively independent."

This section formalizes that assumption as a standalone, testable hypothesis.

---

## 2. Setup

### 2.1 Phase of a Spectral Contribution

For a zero at $\gamma$, the contribution to $E(x)$ has the form:
$$f_\gamma(x) = A(\gamma) \cos(\theta_\gamma(x))$$

where:
- **Amplitude:** $A(\gamma) = \frac{2\sqrt{x}}{|\frac{1}{2} + i\gamma|}$
- **Phase:** $\theta_\gamma(x) = \gamma \log x - \arg(\frac{1}{2} + i\gamma)$

### 2.2 Phase Difference

For two zeros $\gamma_1, \gamma_2$, the phase difference at point $x$ is:
$$\Delta\theta(x) = \theta_{\gamma_1}(x) - \theta_{\gamma_2}(x) = (\gamma_1 - \gamma_2)\log x - [\arg(\rho_1) - \arg(\rho_2)]$$

The key quantity is the **accumulated phase difference** over the window $[2, N]$:
$$\Phi_{12}(N) := (\gamma_1 - \gamma_2) \cdot (\log N - \log 2) = (\gamma_1 - \gamma_2) \log(N/2)$$

---

## 3. The Phase-Mixing Hypothesis

### 3.1 Statement (Informal)

**Phase-Mixing Hypothesis:** For a random zero ensemble, the phases $\theta_{\gamma_i}(x)$ for different zeros $\gamma_i$ behave as if they are uniformly distributed over $[0, 2\pi)$, independently of each other, when averaged over realizations.

### 3.2 Statement (Formal)

**Hypothesis (PM):** Let $\{\tilde{\gamma}_n\}$ be a random point process on $\mathbb{R}^+$ satisfying:
- (PM1) **Stationarity:** The process is stationary (or asymptotically stationary) under shifts.
- (PM2) **Finite correlations:** The $k$-point correlation functions decay sufficiently fast.
- (PM3) **No arithmetic constraint:** The points do not satisfy a global linear constraint of the form $\sum_n c_n f_{\tilde{\gamma}_n}(x) = g(x)$ for a fixed function $g$.

Then for any two bands $B_1, B_2$ defined by fixed cutoffs:
$$\mathbb{E}\left[\int_2^N \cos(\theta_{\gamma_1}(x) - \theta_{\gamma_2}(x)) \, d\mu(x)\right] = 0$$
for $\gamma_1 \in B_1$, $\gamma_2 \in B_2$ drawn independently from the ensemble.

### 3.3 Consequence

Under Hypothesis (PM):
$$\mathbb{E}[C(B_1, B_2; N)] = 0$$

This is precisely Lemma 1.

---

## 4. What Makes PM True for Random Ensembles

### 4.1 Poisson Process

For Poisson:
- Zeros are placed independently
- The position of $\gamma_1$ tells you nothing about $\gamma_2$
- The phase difference $\Delta\theta(x)$ is effectively uniform over realizations

**PM holds trivially.**

### 4.2 GUE Process

For GUE:
- Zeros have local repulsion (no close pairs)
- But repulsion only constrains **relative spacing**, not **absolute position**
- The absolute phases are still "randomized" across realizations

**PM holds despite repulsion** because:
- Repulsion affects the *variance* of $C(B_1, B_2; N)$
- It does not affect the *mean* (which depends on absolute phase alignment)

### 4.3 Key Insight

**Repulsion is a local constraint; phase-mixing is about global structure.**

GUE says: "zeros don't cluster."
PM says: "there's no global alignment of phases."

These are independent properties.

---

## 5. What Falsifies PM

### 5.1 Arithmetic Constraint (Explicit Formula)

The zeta zeros satisfy:
$$\sum_n f_{\gamma_n}(x) = \psi(x) - x + O(1)$$

This is a **global linear constraint** on the sum of all contributions.

For this sum to equal a specific function $\psi(x) - x$ at every $x$:
- The phases cannot be independent
- The phases must be **precisely aligned** to produce the required value

**This violates (PM3).**

### 5.2 Consequence

For zeta zeros, the phase-mixing hypothesis fails, and therefore:
$$\mathbb{E}[C(B_1, B_2; N)] \neq 0$$

In fact, $C(B_1, B_2; N)$ is a specific deterministic value (not a random variable at all).

---

## 6. Testable Predictions

### 6.1 For Ensembles Satisfying PM

| Quantity | Prediction |
|----------|------------|
| $\mathbb{E}[C(B_1, B_2; N)]$ | $= 0$ |
| $\text{Var}[C(B_1, B_2; N)]$ | $> 0$ (fluctuates) |
| Sign of $C$ over realizations | 50% positive, 50% negative |

### 6.2 For Spectra Violating PM (e.g., Zeta)

| Quantity | Prediction |
|----------|------------|
| $C(B_1, B_2; N)$ | Deterministic, non-zero |
| Sign | Stable (empirically negative) |

### 6.3 Test Protocol

To test whether a spectrum $\{\lambda_n\}$ satisfies PM:

1. Compute $C(B_1, B_2; N)$ for the actual spectrum
2. Generate many realizations of a matched-density random process (Poisson or GUE)
3. Compute $C(B_1, B_2; N)$ for each realization
4. Compare:
   - Is the actual value within the random distribution? → PM holds
   - Is the actual value an outlier (e.g., >3σ from mean)? → PM fails

---

## 7. Relation to Existing Concepts

### 7.1 Spectral Rigidity

The PM hypothesis is related to (but distinct from) **spectral rigidity**.

- **Spectral rigidity:** How much do eigenvalues fluctuate from their expected positions?
- **Phase-mixing:** Do the phases of different eigenvalues align globally?

High rigidity (GUE) does not prevent phase-mixing.
The explicit formula creates a different kind of constraint — **phase coherence**, not rigidity.

### 7.2 Number Variance

The PM hypothesis is also related to **number variance** $\Sigma^2(L)$.

- Number variance measures fluctuations in the count of zeros in an interval.
- PM measures fluctuations in the **phase relationships** between zeros.

Both probe "how structured" a spectrum is, but at different levels.

---

## 8. Summary

### The Hypothesis

**(PM) Phase-Mixing:** For a random spectrum with no global constraint, the cross-band covariance has zero expectation because phases are effectively independent.

### The Dichotomy

| Spectrum | PM Status | $\mathbb{E}[C(B_1,B_2;N)]$ |
|----------|-----------|---------------------------|
| Poisson | Satisfies PM | $= 0$ |
| GUE | Satisfies PM | $= 0$ |
| Zeta zeros | Violates PM (explicit formula) | $\neq 0$ (deterministic) |
| L-function zeros | Violates PM? | To be tested |

### The Test

PM is falsifiable: if a spectrum has non-zero mean cross-band covariance, PM fails for that spectrum.

---

## 9. Open Question

**Question:** Do all L-functions satisfying a functional equation and having an Euler product violate PM?

**Conjecture:** Yes. The explicit formula (which exists for all such L-functions) forces phase coherence, violating PM.

**Test:** Compute cross-band covariance for Dirichlet L-function zeros and compare to GUE.

---

*Formalized 2026-01-30 | PROMETHEUS v5.0*
