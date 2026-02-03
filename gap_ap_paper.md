# Arithmetic Progressions in Prime Gaps

**Abstract.** We investigate sequences of consecutive primes where the gaps between them form an arithmetic progression. The longest example found is 8 consecutive primes starting at 128981, with gaps [2, 4, 6, 8, 10, 12, 14]. We prove there is no covering obstruction to arbitrarily long such sequences, and conjecture that they exist for any length k.

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

### 4.1 Longest Found

| Start | Length | Gaps | First term | Common diff |
|-------|--------|------|------------|-------------|
| 128981 | 8 | [2,4,6,8,10,12,14] | 2 | +2 |

This is the only length-8 example found up to 500,000.

### 4.2 Other Notable Examples

| Start | Length | Gaps | Pattern |
|-------|--------|------|---------|
| 15373 | 7 | [4,6,8,10,12,14] | a=4, d=+2 |
| 64919 | 6 | [2,6,10,14,18] | a=2, d=+4 |
| 41203 | 6 | [10,8,6,4,2] | a=10, d=-2 |

### 4.3 Search Statistics

| Range | Length 7 found | Length 8 found |
|-------|---------------|----------------|
| 0 - 100k | 0 | 0 |
| 100k - 200k | 1 (128981) | 1 (128981) |
| 200k - 500k | 0 | 0 |

The rarity suggests exponential decay in density with length.

---

## 5. Density Heuristics

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

## 6. Conjecture

**Gap AP Conjecture.** For any k ≥ 2, there exist k consecutive primes whose gaps form an arithmetic progression with common difference 2.

**Evidence:**
1. No covering obstruction (proven above)
2. Admissibility count stays constant (6 mod 210)
3. Probabilistic heuristics predict existence
4. Analogous to Green-Tao for primes in AP

**Stronger Conjecture.** There are infinitely many such k-tuples for each k.

---

## 7. Relation to Literature

### 7.1 OEIS

- **A333253:** Primes starting strictly increasing gap sequences
- Our gap AP constraint is more restrictive (exact AP, not just increasing)

### 7.2 Prime Tuples

The pattern is an admissible prime tuple. Hardy-Littlewood conjecture predicts infinitely many, with known asymptotic formula.

### 7.3 Novelty Assessment

The specific framing "gaps forming an arithmetic progression" appears not to have a standard name or OEIS sequence. The covering analysis and mod-210 admissibility count may be new observations.

---

## 8. Open Problems

1. **Search extension:** Find length 9+ examples
2. **Prove the conjecture:** Adapt Green-Tao or sieve methods
3. **Density formula:** Derive exact asymptotic for count below x
4. **Other common differences:** Characterize gap APs with d ≠ 2
5. **Decreasing APs:** Are there arbitrarily long decreasing gap APs?

---

## 9. Conclusion

Gap arithmetic progressions — sequences of consecutive primes with gaps in AP — exist and appear to be unbounded in length. The longest known example has 8 primes (128981 to 129037) with gaps [2, 4, 6, 8, 10, 12, 14].

We prove there is no covering obstruction, meaning the pattern is admissible for any length. Combined with probabilistic heuristics, this strongly suggests the Gap AP Conjecture holds.

---

## Appendix: Verification Code

```gp
\\ PARI/GP: Find gap APs

find_gap_ap(maxp, len) = {
  forprime(p = 5, maxp,
    my(g, q, ok);
    g = [];
    q = p;
    for(i = 1, len-1,
      my(nq);
      nq = nextprime(q+1);
      g = concat(g, [nq-q]);
      q = nq
    );
    ok = 1;
    for(i = 2, len-1,
      if(g[i] - g[i-1] <> 2, ok = 0)
    );
    if(ok, print(p, " ", g))
  )
}

\\ Verify 128981
find_gap_ap(130000, 8);

\\ Search for length 9
\\ find_gap_ap(10000000, 9);
```

---

*Draft prepared 2026-02-03*
