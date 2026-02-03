# Frequency Band Decomposition of C(N)

## Summary of Findings

---

## 1. Band-by-Band C(N) Values

| Band | γ Range | # Zeros | C(N) at N=10⁴ | Effect |
|------|---------|---------|---------------|--------|
| B1 | < 50 | 10 | 0.69 | 31% better |
| B2 | 50-100 | 19 | 1.13 | 13% **worse** |
| B3 | 100-150 | 23 | 0.68 | 32% better |
| B4 | 150-200 | 27 | ~1.2 | ~20% worse |
| B5 | > 200 | 21 | 0.82 | 18% better |

**Pattern**: Alternating good/bad bands (approximately).

---

## 2. Cross-Band Combinations

| Combination | C(N) | Observation |
|-------------|------|-------------|
| B1 alone | 0.69 | Good |
| B3 alone | 0.68 | Good |
| **B1 + B3** | **0.56** | **Better than either!** |
| B2 alone | 1.13 | Bad |
| B1 + B2 | ~0.9 | B2 hurts B1 |
| ALL | 0.80 | Net positive |

**Key finding**: Non-adjacent bands (B1+B3) combine constructively for cancellation.

---

## 3. Covariance Structure

### Within-Band Covariances
| Band | Avg Cov | Interpretation |
|------|---------|----------------|
| B1 | -0.073 | Strong destructive |
| B2 | -0.004 | Weak |
| B3 | -0.001 | Very weak |

### Cross-Band Covariances
| Pair | Avg Cov | Interpretation |
|------|---------|----------------|
| B1↔B2 | **+0.023** | **Constructive** (bad) |
| B1↔B3 | **-0.027** | **Destructive** (good) |
| B2↔B3 | -0.002 | Neutral |

---

## 4. Mechanism

### Why B1+B3 is better than B1 or B3 alone:

The covariance between bands i and j contributes to total variance:
$$\text{Var}[E_{B_i} + E_{B_j}] = \text{Var}[E_{B_i}] + \text{Var}[E_{B_j}] + 2\text{Cov}[E_{B_i}, E_{B_j}]$$

For B1+B3:
- Cov[B1, B3] < 0 (destructive)
- This **reduces** the combined variance
- Result: C(B1+B3) < C(B1), C(B3)

For B1+B2:
- Cov[B1, B2] > 0 (constructive)
- This **increases** the combined variance
- Result: C(B1+B2) > C(B1)

### Physical intuition:

Low-frequency zeros (B1) and high-frequency zeros (B3) oscillate at very different rates. When both are present:
- Their contributions are **anti-correlated** on average
- When B1 is high, B3 tends to be low (and vice versa)
- Net effect: additional cancellation

Mid-frequency zeros (B2) have a **resonance** with low-frequency zeros:
- Their contributions are positively correlated
- When B1 is high, B2 tends to also be high
- Net effect: reduced cancellation

---

## 5. New Operator Constraint

Any Hilbert-Pólya operator must produce:

1. **Band-alternating C(N) pattern**: odd bands cancel well, even bands may not
2. **Negative B1↔B3 cross-covariance**: distant frequency bands must destructively interfere
3. **Near-zero or positive B1↔B2 cross-covariance**: adjacent bands may constructively interfere

This is a **finer constraint** than just requiring C(N) < 1 overall.

---

## 6. Implications for Operator Classes

### GUE Random Matrices
- Should produce similar band structure
- Testable: compute C(N) by bands for GUE eigenvalues

### Quantum Chaotic Hamiltonians
- BGS conjecture: eigenvalues follow GUE
- Should match band structure if conjecture holds

### Generic Self-Adjoint
- Unlikely to have correct cross-band correlations
- Would need fine-tuned spectrum

---

## 7. Next Steps

1. **Verify with more zeros**: Current analysis uses 50-100 zeros
2. **Test GUE prediction**: Generate GUE eigenvalues, compute band structure
3. **Quantify resonance**: Why does B1↔B2 resonate but not B1↔B3?
4. **Scaling**: How does band structure change with N?

---

*Analysis date: 2026-01-30*
*Framework: PROMETHEUS v5.0 Inverse Spectral*
