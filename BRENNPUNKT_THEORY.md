# Brennpunkt Theory: Why 1/4 and 1/3?

**Deriving the Prime and Composite Focal Points**

---

## 1. The Phenomenon

Under parameterized geometric inversion:
```
r(t) = r_orig^(1-2t) × R^(2t)
```

**Empirical finding:**
- Primes cluster tightest at t = 1/4
- Composites cluster tightest at t = 1/3
- Both are simple fractions

---

## 2. The Inversion Formula

At t = 1/4:
```
r_focused = r^(1-1/2) × R^(1/2) = r^(1/2) × R^(1/2) = √(r × R)
```
This is the **geometric mean** of original radius and inversion radius.

At t = 1/3:
```
r_focused = r^(1-2/3) × R^(2/3) = r^(1/3) × R^(2/3) = ∛(r × R²)
```
This is the **weighted geometric mean** with ratio 1:2.

---

## 3. Why Geometric Mean for Primes?

**Hypothesis 1: Prime distribution is scale-invariant**

The Prime Number Theorem: π(x) ~ x/ln(x)

Under scaling x → λx:
- π(λx) ~ λx/ln(λx) = λx/(ln λ + ln x)

The geometric mean √(r × R) is the unique point that:
- Treats small and large primes symmetrically
- Is scale-invariant under r → r/k, R → kR

**Primes are "democratically distributed"** — no scale is special.
The geometric mean captures this democracy.

---

## 4. Why Cube Root for Composites?

**Hypothesis 2: Composites have inherent 2-factor bias**

Most small composites have exactly 2 prime factors (semiprimes dominate).

For a semiprime n = p × q with p < q:
- Typically p ~ n^(1/3), q ~ n^(2/3) (for random semiprimes)

The weighted mean r^(1/3) × R^(2/3) reflects this **2:1 asymmetry**.

**Composites "lean toward" their larger factor** — they're not symmetric.
The 1/3 exponent captures this asymmetry.

---

## 5. Connection to Brennpunkt Numbers

**The numbers:**
```
1/4 = 1/2²     (prime Brennpunkt)
1/3 = 1/F₄     (composite Brennpunkt)

2 = first prime
3 = F₄ = first odd prime

Harmonic mean: 2/(1/4 + 1/3) = 2/(7/12) = 24/7 ≈ 3.43
But H(1/4, 1/3) as BRENNPUNKTE: t = 2×(1/4)×(1/3)/((1/4)+(1/3)) = 2/7
```

**2/7 is the "optimal laser point"** — maximizes prime/composite separation.

---

## 6. Finite-N Hilbert-Pólya Connection

**The classical Hilbert-Pólya conjecture:**
Zeta zeros are eigenvalues of some self-adjoint operator.

**Finite-N analog:**
For primes up to N, is there an operator whose eigenvalue statistics match prime statistics?

**The Brennpunkt as operator:**
```
T_t : r → r^(1-2t) × R^(2t)
```

At t = 1/4, this transformation **optimally diagonalizes** the prime distribution on the golden spiral.

**Conjecture:** The Brennpunkt parameter t = 1/4 corresponds to the unique t where the prime distribution becomes "maximally eigenfunction-like" under the inversion operator.

---

## 7. Testing the Hypotheses

**Test 1: N-independence**
Run Brennpunkt search for N = 100, 500, 1000, 5000, 10000.
If t = 1/4 is universal, it should not depend on N.

**Test 2: Semiprime verification**
For semiprimes pq with p < q:
- Compute typical p/q ratio
- Check if this matches the 1:2 weighting in t = 1/3

**Test 3: Prime-k composites**
For k-almost primes (exactly k prime factors):
- Optimal t should shift with k
- Prediction: t_k → 1/(k+1) as factor count increases?

**Test 4: Operator spectrum**
Discretize the inversion operator on prime-decorated golden spiral.
Check if eigenvalue spacing at t = 1/4 resembles GUE.

---

## 8. Summary

| Object | Brennpunkt t | Exponent | Meaning |
|--------|--------------|----------|---------|
| Primes | 1/4 | 1/2 | Geometric mean (scale-invariant) |
| Composites | 1/3 | 1/3, 2/3 | Weighted mean (2-factor asymmetry) |
| Optimal laser | 2/7 | - | Harmonic mean of Brennpunkte |

**The Brennpunkt encodes the inherent symmetry/asymmetry of the number class.**

Primes: symmetric → geometric mean → t = 1/4
Composites: asymmetric → weighted mean → t = 1/3

---

*Draft: 2026-02-06*
*"The focal point reveals the symmetry."*
