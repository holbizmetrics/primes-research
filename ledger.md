# World Model — Primes Research

## KNOWN
- Primes are infinite (Euclid)
- Prime Number Theorem: π(n) ~ n/ln(n)
- Bounded gaps between primes proven (Zhang 2013, Polymath)
- Primes in arithmetic progressions (Dirichlet)
- Green-Tao: arbitrarily long arithmetic progressions in primes
- Mod 6 constraint: gaps can only be ≡ 0, 2, 4 (mod 6) for p > 3
- Forbidden gap pairs: (2,2), (4,4) mod 6 — i.e., gaps ≡ 2 cannot follow gaps ≡ 2
- Lemke Oliver-Soundararajan: prime last-digit transitions are biased

## DISCOVERED (This Session)

### Gap Arithmetic Progressions [POTENTIALLY NOVEL]
- Found 8 consecutive primes (128981 to 129037) with gaps [2,4,6,8,10,12,14]
- Gaps form AP with first term 2, common difference 2
- No covering obstruction: n(n+1) mod p never covers all residues
- Conjecture: arbitrarily long such sequences exist

### Other Findings
- Hypercube clustering: Hamming distance between consecutive primes ≈ 2.5 (vs 4 expected random)
- Digit sum +6 spike: 13.5% of gap changes are +6, caused by sexy primes (gap 6) with no carry
- Even-digit primes: n + reverse(n) always divisible by 11

## ASSUMED
- Gap AP pattern probably not in mainstream literature (needs verification)
- Longer gap APs (9+ primes) exist but computationally hard to find

## UNCERTAIN
- Exact density of gap AP sequences
- Whether there's a named theorem for n(n+1) residue coverage

## CHANGED
- Initial assumption that patterns are "all known" → some novel framings possible

---

## Verification Ledger

| Claim | Status | Evidence |
|-------|--------|----------|
| 128981 starts 8-prime gap AP | VERIFIED | Computed, all primes checked |
| No covering obstruction | VERIFIED | n(n+1) residues computed mod p for p ≤ 19 |
| 129053 = 23 × 5611 | VERIFIED | Division check |

---

## Epistemic Debt

| Claim | Level | What Would Verify |
|-------|-------|-------------------|
| Gap AP conjecture | SPECULATION | Proof or large-scale search |
| Pattern is novel | MEDIUM | Literature search |
