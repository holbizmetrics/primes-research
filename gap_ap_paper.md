# Arithmetic Progressions in Prime Gaps

**Abstract.** We investigate sequences of consecutive primes where the gaps between them form an arithmetic progression. The longest example found is **11 consecutive primes** starting at 245333213, with gaps [20, 18, 16, 14, 12, 10, 8, 6, 4, 2] ending at twin primes. We prove there is no covering obstruction to arbitrarily long such sequences, and conjecture that they exist for any length k.

---

## 1. Definition

**Definition.** A *gap arithmetic progression* of length n is a sequence of n consecutive primes p₁ < p₂ < ... < pₙ such that the gaps gᵢ = pᵢ₊₁ - pᵢ form an arithmetic progression.

**Example.** The 8 consecutive primes starting at 128981:
```
Primes: 128981, 128983, 128987, 128993, 129001, 129011, 129023, 129037
Gaps:   [2, 4, 6, 8, 10, 12, 14]
```
The gaps form an AP with first term a = 2 and common difference d = 2.

---

## 2. Structural Analysis

### 2.1 Offset Pattern

For a gap AP with first term a and common difference d, the offsets from the starting prime are:
```
0, a, 2a+d, 3a+3d, 4a+6d, 5a+10d, ...
```
For the standard case (a = 2, d = 2), offsets are:
```
0, 2, 6, 12, 20, 30, 42, 56, 72, ...
```
These are n(n+1) for n = 0, 1, 2, ...

### 2.2 Covering Congruence Analysis

**Key question:** Can small primes create an obstruction?

For a covering obstruction to exist, the residues n(n+1) mod p would need to cover all residue classes for some prime p.

**Theorem (No Covering Obstruction).** For any odd prime p, the set {n(n+1) mod p : n ∈ ℤ} does not cover all residue classes.

*Proof.* The function f(n) = n(n+1) = n² + n satisfies f(n) = f(-n-1), so it takes at most (p+1)/2 distinct values mod p. Since (p+1)/2 < p for p > 1, not all residues are covered. □

**Data:**

| p | Residues of n(n+1) | Coverage |
|---|-------------------|----------|
| 3 | {0, 2} | 2/3 |
| 5 | {0, 1, 2} | 3/5 |
| 7 | {0, 2, 5, 6} | 4/7 |
| 11 | {0, 1, 2, 6, 8, 9} | 6/11 |
| 13 | {0, 1, 2, 3, 6, 9, 10, 12} | 8/13 |

**Corollary.** There is no finite set of primes that obstructs gap APs of arbitrary length.

---

## 3. Admissibility

### 3.1 Admissibility mod 210

For the pattern with d = 2, we check admissibility mod 210 = 2·3·5·7.

| Length | Valid starting residues mod 210 |
|--------|--------------------------------|
| 3 | 6 residues |
| 5 | 6 residues |
| 7 | 6 residues |
| 9 | 6 residues |

**Observation.** The count of valid residues stays constant at 6 regardless of length.

This means: approximately 6/210 ≈ 2.86% of primes are candidates to start a gap AP of any length (from the mod-210 perspective alone).

### 3.2 Verification

128981 mod 210 = 41, which is one of the 6 valid residues. ✓

---

## 4. Search Results

### 4.1 Longest Found (Length 11)

| Start | Length | Gaps | First term | Common diff |
|-------|--------|------|------------|-------------|
| 245333213 | **11** | [20,18,16,14,12,10,8,6,4,2] | 20 | -2 |

**11 consecutive primes:** 245333213, 245333233, 245333251, 245333267, 245333281, 245333293, 245333303, 245333311, 245333317, 245333321, 245333323

The sequence ends with twin primes (245333321, 245333323). The gaps form a perfect descending AP from 20 to 2.

### 4.2 Length-9 Examples

| Start | Length | Gaps | First term | Common diff |
|-------|--------|------|------------|-------------|
| 19641263 | 9 | [20,18,16,14,12,10,8,6] | 20 | -2 |
| 32465047 | 9 | [16,14,12,10,8,6,4,2] | 16 | -2 |
| 37091581 | 9 | [16,14,12,10,8,6,4,2] | 16 | -2 |

All three length-9 examples have common difference d = -2 (decreasing AP).

### 4.2 Length-8 Examples

| Start | Length | Gaps | First term | Common diff |
|-------|--------|------|------------|-------------|
| 128981 | 8 | [2,4,6,8,10,12,14] | 2 | +2 |

This is the only length-8 example with d = +2 found up to 500,000.

### 4.3 Other Notable Examples

| Start | Length | Gaps | Pattern |
|-------|--------|------|---------|
| 15373 | 7 | [4,6,8,10,12,14] | a=4, d=+2 |
| 64919 | 6 | [2,6,10,14,18] | a=2, d=+4 |
| 41203 | 6 | [10,8,6,4,2] | a=10, d=-2 |

### 4.5 Search Statistics

| Length | First occurrence | Count | Range searched |
|--------|------------------|-------|----------------|
| 8 | 128981 | 1 | up to 500k |
| 9 | 19641263 | 3 | up to 100M |
| 10 | 245333213 | 2 | up to 1B |
| 11 | 245333213 | 1+ | up to 10B (in progress) |

**Observation:** All examples with length ≥ 9 have d = -2 (decreasing), while length-8 at 128981 has d = +2. The length-11 is a perfect "countdown" from gap 20 to gap 2 (twin primes).

---

## 5. Direction Asymmetry: The Twin Prime Sink Effect

### 5.1 Increasing vs Decreasing Counts

We systematically counted gap APs by direction (d > 0 vs d < 0):

| Length | Range | Increasing (d>0) | Decreasing (d<0) | Ratio dec/inc |
|--------|-------|------------------|------------------|---------------|
| 7 | 10M | 21 | 15 | **0.71** |
| 8 | 100M | 15 | 21 | **1.40** |
| 9 | 500M | 3 | 12 | **4.00** |

**Key observation:** The ratio shifts dramatically toward decreasing as length increases.

### 5.2 Analysis of Termination Patterns

For decreasing length-9 gap APs (12 found), the final gaps are:

| Final gap | Count | Percentage |
|-----------|-------|------------|
| 2 (twins) | 6 | 50% |
| 4 | 3 | 25% |
| 6 | 2 | 17% |
| 8 | 1 | 8% |

**Half of all decreasing length-9 gap APs terminate at twin primes.**

### 5.3 The Twin Prime Sink Effect

**Theorem (Heuristic).** Decreasing gap APs are favored at longer lengths due to the "twin prime sink effect."

**Mechanism:**
- **Decreasing (d < 0):** Gaps shrink toward small values. Twin primes (gap = 2) are relatively abundant and act as natural "sinks" that capture descending sequences.
- **Increasing (d > 0):** Gaps grow toward large values. Large gaps (16, 18, 20, ...) become exponentially rare, making it harder to complete long increasing sequences.

**Quantitative argument:**
- Gap g occurs with probability roughly proportional to 1/log(p) for typical gaps
- Large gaps (g > 20) are significantly rarer than small gaps
- Decreasing sequences "fall" toward the abundant twin primes
- Increasing sequences must "climb" toward rare large gaps

This explains why:
1. At length 7, increasing is slightly favored (sequences are short, large gaps still achievable)
2. At length 8, the ratio crosses 1:1
3. At length 9+, decreasing dominates (4:1 ratio)
4. The length-11 record is decreasing, ending at twins

### 5.4 Increasing Length-9 Examples

Despite being rarer, increasing length-9 gap APs do exist:

| Start | Gaps | First | Last |
|-------|------|-------|------|
| 95285633 | [6,8,10,12,14,16,18,20] | 6 | 20 |
| 113575727 | [2,4,6,8,10,12,14,16] | 2 | 16 |
| 232728647 | [2,4,6,8,10,12,14,16] | 2 | 16 |

Note: 2 of 3 start at twin primes (gap = 2), confirming that starting constraints matter for increasing sequences.

---

## 6. Density Heuristics

### 5.1 Probabilistic Model

Assuming Cramér-like independence, the probability that n consecutive primes near x have gaps forming an AP is roughly:

```
P(gap AP of length n near x) ≈ C · (log x)^{-n}
```

for some constant C depending on the specific AP parameters.

### 5.2 Expected Count

By prime number theorem heuristics:
- Length 7: expect O(1) examples below 10⁶
- Length 8: expect O(1) examples below 10⁷
- Length 9: expect O(1) examples below 10⁸

Finding a length-8 at 128981 is consistent with these estimates.

---

## 7. Conjecture

**Gap AP Conjecture.** For any k ≥ 2, there exist k consecutive primes whose gaps form an arithmetic progression with common difference 2.

**Evidence:**
1. No covering obstruction (proven above)
2. Admissibility count stays constant (6 mod 210)
3. Probabilistic heuristics predict existence
4. Analogous to Green-Tao for primes in AP

**Stronger Conjecture.** There are infinitely many such k-tuples for each k.

---

## 8. Relation to Literature

### 7.1 OEIS

- **A333253:** Primes starting strictly increasing gap sequences
- Our gap AP constraint is more restrictive (exact AP, not just increasing)

### 7.2 Prime Tuples

The pattern is an admissible prime tuple. Hardy-Littlewood conjecture predicts infinitely many, with known asymptotic formula.

### 7.3 Novelty Ass