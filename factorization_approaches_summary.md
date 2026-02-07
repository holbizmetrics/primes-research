# Factorization via onesFromPP: Four Approaches Summary

## Overview

Given N = p × q and the onesFromPP sequence (partial products sum at each position),
these four approaches attempt to recover the factors p and q.

**onesFromPP[k]** = Σᵢ p[i] × q[k-i] = count of 1×1 bit products at position k

## Approach 1: MAX-SAT Encoding

**Idea**: Formulate as constraint satisfaction. Find (p, q) satisfying:
- p × q = N (hard constraint)
- onesFromPP(p, q) = observed values (soft constraints)

**Results**:
| Bits | Exact | Noisy (10%) |
|------|-------|-------------|
| 6    | 100%  | 100%        |
| 8    | 100%  | 100%        |
| 10   | 100%  | 100%        |

**Key insight**: Even with 10% noise in onesFromPP, MAX-SAT finds correct factorization.

## Approach 2: Gröbner Bases / Bilinear System

**Idea**: The equations Σᵢ p[i]×q[k-i] = c[k] form a bilinear polynomial system.
Solve using:
- Alternating substitution (fix p, solve for q; fix q, solve for p)
- Linearization (introduce y[i][j] = p[i]×q[j], solve linear system)

**Results**:
| Bits | Substitution | Linearization |
|------|--------------|---------------|
| 4    | ~50%         | 100%          |
| 5    | ~35%         | 100%          |
| 6    | ~20%         | 100%          |

**Key insight**: Pure alternating substitution struggles, but linearization works perfectly.

## Approach 3: Error Distribution Analysis

**Idea**: Understand WHERE errors occur in ML-predicted onesFromPP.

**Simulated accuracy** (based on reported ML results):
- Interior positions (middle 80%): 98.8% accuracy
- Edge positions (first/last 10%): 64% accuracy

**Findings**:
| Bits | Interior Acc | Edge Acc | Avg Errors/Sample |
|------|--------------|----------|-------------------|
| 8    | 98.7%        | 65.6%    | 0.86              |
| 12   | 98.7%        | 62.4%    | 1.76              |
| 16   | 98.8%        | 65.0%    | 2.40              |

**Key insight**: Interior is essentially solved. Edge positions are unreliable but few in number.

## Approach 4: Lattice Formulation (CVP)

**Idea**: Linearize y[i][j] = p[i]×q[j], creating n² variables.
onesFromPP constraints become: Σ_{i+j=k} y[i][j] = c[k]

**Lattice geometry**:
| Bits | Variables | Constraints | Underdetermined by |
|------|-----------|-------------|-------------------|
| 4    | 16        | 7           | 9                 |
| 6    | 36        | 11          | 25                |
| 8    | 64        | 15          | 49                |

**Key insight**: The system is massively underdetermined (n² - O(n) degrees of freedom).
BUT: The rank-1 constraint (Y = p⊗q is an outer product) adds n² - 2n constraints!

**Results** (CVP enumeration):
| Bits | Exact | Noisy (ML sim) | Weighted CVP |
|------|-------|----------------|--------------|
| 6    | 100%  | 100%           | 100%         |
| 8    | 100%  | 100%           | 100%         |
| 10   | 100%  | 100%           | 100%         |

## Unified Understanding

The factorization problem via onesFromPP can be viewed as:

**"Find a rank-1 binary matrix Y with prescribed anti-diagonal sums"**

Where:
- Y[i][j] = p[i] × q[j] (binary outer product)
- Anti-diagonal k: Σ_{i+j=k} Y[i][j] = onesFromPP[k]

### Why this is tractable:

1. **N = p × q** already constrains the search space to O(√N) candidates
2. **onesFromPP** provides 2n-1 additional constraints
3. **Rank-1** structure means we're really solving for 2n bits, not n²
4. **Interior positions** have high accuracy (98.8%)
5. **Errors are additive** (±1), allowing robust optimization

### Why this may not break RSA:

1. We only tested up to 10 bits (RSA uses 1024-2048)
2. CVP on full lattice is NP-hard in general
3. ML prediction accuracy at 64+ bits remains to be demonstrated at scale
4. Edge positions become proportionally smaller but carry prediction remains key

## Files

- `factoring_maxsat.py` - MAX-SAT approach
- `factoring_groebner.py` - Bilinear system / Gröbner approach
- `error_analysis.py` - Error distribution simulation
- `factoring_lattice_fast.py` - Lattice / CVP approach

## Conclusion

At small scale (≤10 bits), all approaches achieve 100% success rate, even with
realistic noise levels. The key insight is the **rank-1 structure** of the
linearized problem, which dramatically constrains the solution space.

The remaining challenge is scaling ML prediction to cryptographic bit sizes
(512-4096 bits) with sufficient accuracy on interior positions.
