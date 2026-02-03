# Prime Gap Arithmetic Progressions

**Date:** 2026-01-25
**Status:** Novel framing, possibly not in literature

---

## Discovery

Sequences of consecutive primes where the **gaps form an arithmetic progression**.

### Best Example Found

**8 primes starting at 128981:**
```
Primes: 128981, 128983, 128987, 128993, 129001, 129011, 129023, 129037
Gaps:   [2, 4, 6, 8, 10, 12, 14]
```

The gaps form an AP with first term 2 and common difference 2.

---

## Structure

For gaps [2, 4, 6, 8, ..., 2k], the offsets from the starting prime are:
```
0, 2, 6, 12, 20, 30, 42, 56, ...
```
These are **n(n+1)** for n = 0, 1, 2, 3, ...

---

## Covering Congruence Analysis

**Key finding:** n(n+1) mod p never covers all residues for any odd prime p.

| p | Residues covered | Uncovered |
|---|------------------|-----------|
| 3 | {0, 2} | {1} |
| 5 | {0, 1, 2} | {3, 4} |
| 7 | {0, 2, 5, 6} | {1, 3, 4} |
| 11 | {0, 1, 2, 6, 8, 9} | {3, 4, 5, 7, 10} |

**Implication:** No hard theoretical limit from small prime covering!

For any length k, there exist starting residues that avoid all small prime divisibility constraints.

---

## Constraints on Starting Prime

For 8 primes with gaps [2, 4, 6, 8, 10, 12, 14]:
- Starting prime ≡ 2 (mod 3)
- Starting prime ≡ 1 or 2 (mod 5)
- Starting prime ≡ 3, 4, or 6 (mod 7)

Verify: 128981 mod 3 = 2 ✓, mod 5 = 1 ✓, mod 7 = 6 ✓

---

## Why 128981 Can't Extend to 9 Primes

128981 + 72 = 129053 = 23 × 5611 (composite)

A different starting prime might work for 9 primes, but none found up to 3 million.

---

## Conjecture

**Gap AP Conjecture:** For any k, there exist k consecutive primes whose gaps form an arithmetic progression with common difference 2.

**Evidence:**
1. No covering obstruction (n(n+1) never covers all residues mod p)
2. By probabilistic heuristics (similar to Green-Tao), arbitrarily long sequences should exist
3. Finding them becomes exponentially harder as k increases

**Open question:** What is the largest such k for primes below 10^12?

---

## Other Patterns Found

| Starting Prime | Length | Gaps |
|---------------|--------|------|
| 128981 | 7 | [2, 4, 6, 8, 10, 12, 14] |
| 15373 | 6 | [4, 6, 8, 10, 12, 14] |
| 64919 | 5 | [2, 6, 10, 14, 18] (diff=4!) |
| 41203 | 5 | [10, 8, 6, 4, 2] (decreasing) |

---

## Relation to Known Results

- Related to **prime k-tuples** and **admissible patterns**
- The pattern [2, 4, 6, 8, 10, 12, 14] is admissible (checked)
- Different framing: gaps forming AP vs. primes forming AP

---

## Admissibility Analysis

### Valid Residues mod 210

For gap AP with diff=+2, there are exactly **6 valid starting residues mod 210** for any length:

| First Gap | Valid Residues mod 210 |
|-----------|----------------------|
| 2 | {11, 17, 41, 101, 137, 167} |
| 4 | {13, 19, 43, 103, 139, 169} |
| 6 | {17, 23, 47, 107, 143, 173} |

The count stays at 6 regardless of target length!

### Examples by Different Starting Gaps

| First Gap | Best Length Found | Example |
|-----------|-------------------|---------|
| 2 | 7 | 128981: [2,4,6,8,10,12,14] |
| 4 | 6 | 15373: [4,6,8,10,12,14] |
| 6 | 5 | Found in search |

### Different Common Differences

| Diff | Max Length | Example |
|------|------------|---------|
| +2 | 7 | [2,4,6,8,10,12,14] |
| +4 | 6 | [2,6,10,14,18,22] |
| -2 | 6 | [12,10,8,6,4,2] |
| +6 | 5 | [6,12,18,24,30] |
| +8 | 5 | [2,10,18,26,34] |

---

## Literature Status

- **A333253** (OEIS, 2020): Tracks strictly increasing gap runs
- Our specific "gap AP" constraint is more restrictive
- The covering analysis (6 residues mod 210) is standard admissibility theory

---

## Further Investigation

1. Search larger range for length 8+ examples
2. Prove/disprove the Gap AP Conjecture
3. Find connection to existing prime tuple theory
4. Check if this specific framing exists in literature

---

*Research note from prime exploration session*
