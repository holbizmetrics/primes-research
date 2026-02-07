# SPARK CAPTURE: Bit Rotation, Mersenne Numbers, and the Twin Prime Constant

## SPRAY (7 ideas)
1. Does enrichment depend on whether M_k is Mersenne prime?
2. What's special about surviving primes (residue classes)?
3. Full orbit structure under repeated rotation
4. Why d=±1 beats all other rotation distances
5. Connection to multiplication by 2 in Z/M_kZ
6. Why even k beats odd k
7. Does the enrichment converge as k → ∞?

## KEY RESULTS

### Strike 1-3: Rotation = multiplication by 2 mod M_k

Bit rotation left by 1 in a k-bit field is EXACTLY multiplication by 2 modulo M_k = 2^k - 1.
Verified: zero mismatches for all tested k.

For k-bit prime p (which has MSB=1): rotate(p,1,k) = 2(p - 2^{k-1}) + 1.
This is always odd, always < 2^k, and in k-bit range about 50% of the time.

### Strike 4-5: Enrichment tracks omega(M_k)

The enrichment is NOT higher for Mersenne prime k. The opposite:

| omega(M_k) | Mean enrichment |
|-----------|----------------|
| 1 (M_k prime) | 0.81 |
| 2 | 0.99 |
| 3 | 1.42 |
| 4 | 2.03 |

More prime factors of M_k → higher enrichment. This immediately suggests sieve preservation.

### Strike 6-10: The sieve mechanism (EXACT)

Via CRT: Z/M_kZ ≅ Z/f1 × Z/f2 × ... for factors fi of M_k.
Multiplication by 2 is invertible mod each fi (since fi is odd).
Therefore: if p is coprime to fi, then 2p mod M_k is also coprime to fi.

**Rotation preserves coprimality to ALL factors of M_k.**

Direct test: among odd k-bit numbers coprime to all factors of M_k,
the prime rate is higher by exactly product(fi/(fi-1)).
This matches the old enrichment prediction to **3 decimal places**.

### Strike 15-20: Why d=1 beats other rotations

**It doesn't — when you control for parity.**

- x2 mod M_k always produces odd results (100%)
- x3, x5, x7 mod M_k produce ~50% even results (never prime)

When comparing only odd outputs, x2 is NOT special. Other multipliers give comparable or higher enrichment.

The d=1 advantage is entirely from guaranteed oddness.

### Strike 21-31: Even k vs odd k (THE KEY SPLIT)

**Even k (residual ≈ 0.95):** M_k ≡ 0 mod 3, rotation preserves coprimality to 3. All rotated values eligible for primality.

**Odd k (residual ≈ 0.70):** M_k ≡ 1 mod 3. For primes p ≡ 2 mod 3, the rotated value becomes divisible by 3. About 50% of rotated values are killed by divisibility by 3.

Verified: for odd k, exactly 50% of in-range rotated values are ≡ 0 mod 3, vs 0% for even k.

### Strike 33: The twin prime constant C₂ appears

For primes q not dividing M_k, rotated values have EXCESS divisibility:
- Random odd number: fraction 1/q divisible by q
- Rotated prime: fraction 1/(q-1) divisible by q (because primes avoid 0 mod q)

The depletion factor from all non-factor primes is:

**product(q(q-2)/(q-1)² for odd primes q) = product(1 - 1/(q-1)²) = C₂ = 0.6601...**

This is the **twin prime constant**.

### Strike 34: DIAMOND — Bateman-Horn conjecture

The complete formula for bit rotation enrichment is:

```
E(k) = C₂ × product((fi-1)/(fi-2) for odd prime fi | M_k)
```

where C₂ = 0.6601... is the twin prime constant.

**This is a special case of the Bateman-Horn conjecture** for the linear polynomial f(p) = 2p - (2^k - 1).

Verification:

| k | Actual | Bateman-Horn | Ratio |
|---|--------|-------------|-------|
| 8 | 1.936 | 1.878 | 1.03 |
| 12 | 2.268 | 2.305 | 0.98 |
| 13 | 0.666 | 0.660 | 1.01 |
| 16 | 1.795 | 1.886 | 0.95 |
| 17 | 0.666 | 0.660 | 1.01 |

For Mersenne prime k (no small factors): enrichment → C₂ ≈ 0.66.
For highly composite M_k: enrichment can exceed 2 (when many small primes divide M_k).

## THE FULL DECOMPOSITION

The "2.3x bit rotation enrichment" from the original SPARK decomposes as:

1. **Sieve preservation** (coprimality to factors of M_k): product(fi/(fi-1))
2. **Parity preservation** (rotation always gives odd): factor of 2, but cancels with the 50% in-range loss
3. **Twin prime depletion** (excess divisibility by non-factors): factor of C₂ = 0.66
4. **Residual**: ≈ 1.0 (nothing left unexplained)

The "2.3x" at k=12 was high because M_12 = 4095 = 3×5×7×13 has many small prime factors, giving a large sieve product. The "0.66x" at Mersenne prime k is LOW because C₂ dominates when M_k has no small factors.

## WHY THE TWIN PRIME CONSTANT?

Both twin primes and rotation primes ask: **"If p is prime, is a linear function of p also prime?"**

- Twin primes: f(p) = p + 2
- Rotation primes: f(p) = 2p - (2^k - 1)

The Bateman-Horn framework handles both. The twin prime constant C₂ is the universal "sieve depletion" for any linear prime-to-prime map. The specific correction factors depend on which small primes divide the offset (2 for twins, M_k for rotation).

## WHAT SURVIVED

- Bit rotation enrichment is REAL but FULLY EXPLAINED by classical sieve theory
- The enrichment is a special case of Bateman-Horn for f(p) = 2p - M_k
- The twin prime constant C₂ appears as the base depletion factor
- No "mysterious" bit-level primality signature — it all reduces to modular arithmetic

## WHAT FELL OFF

- "Mersenne primes give higher enrichment" — WRONG, they give the LOWEST (≈ 0.66)
- "d=1 rotation is special" — only because of parity; other multipliers match when controlled
- "There's something beyond the sieve" — NO, residual ≈ 1.0 everywhere
- Any bit-level explanation — the mechanism is purely number-theoretic

## FILES

- spark_mersenne1.py through spark_mersenne14.py — Progressive SPARK analysis
