# Prime Investigation Session Notes
## 2026-01-29

### Session Overview
Explored prime structure through multiple lenses: power sums, smooth numbers, spectral metrics, and gap transitions. Goal: find genuine structure beyond known results.

---

## 1. Binary Power Differences: |2^n - 3^m|

### Key Finding
- Differences |2^n - 3^m| can express ~23 primes ≤ 500
- Connected to **continued fraction convergents** of log₂(3) ≈ 1.585
- Convergent (8, 5) gives prime 13: |256 - 243| = 13
- Primes cluster near convergent points

### The Math
```
log₂(3) = [1; 1, 1, 2, 2, 3, 1, ...]
Convergents: (1,1), (2,1), (3,2), (8,5), (19,12), ...
At (8,5): 2^8 - 3^5 = 256 - 243 = 13 (prime!)
```

### Verdict
Known territory (Bezout's identity, Mihailescu theorem). The visual/geometric interpretation is nice but not novel.

---

## 2. Ternary Power Sums: |±3^a ± 5^b ± 7^c|

### Parity Constraint Discovery
With bases (2, 3, 5) — genuine ternary can ONLY produce prime 2:
```
2^a = even, 3^b = odd, 5^c = odd
±even ± odd ± odd = even (always!)
```

### Odd Bases (3, 5, 7)
- All terms odd → odd ± odd ± odd can be odd or even
- **43.7% of primes ≤ 1000 are unreachable**
- Not a residue class issue — it's discrete lattice structure

### Unreachable Primes
```
61, 139, 149, 163, 179, 181, 197, 223, 229, 233, 271, 277,
307, 313, 331, 373, 379, 397, 401, 409, 421, 433, 439, ...
```

### Cross-Base Analysis
```
Unreachable by {3,5,7}:  514 primes < 5000
Unreachable by {3,5,11}: 552 primes < 5000
Unreachable by BOTH:     456 primes (88% overlap!)
```

### Verdict
The specific unreachable set has structure, but likely reduces to known S-unit equation theory.

---

## 3. Smooth Number Distance

### Setup
- 7-smooth numbers: 2^a × 3^b × 5^c × 7^d
- Question: How close is each prime to nearest smooth number?

### Key Statistics
- 52% of primes are distance 1 from a 7-smooth number
- These are primes of form (smooth ± 1)
- Smooth neighbors are 87% reachable by |±3^a ± 5^b ± 7^c| (vs 47% random)

### Explanation
Smooth numbers and power sums share base primes {3,5,7} → correlated, not independent.

### Twin Primes at Smooth Numbers
Found 9 smooth numbers where BOTH n-1 and n+1 are prime AND unreachable:
```
 180 = 2² × 3² × 5     → (179, 181)
 810 = 2  × 3⁴ × 5     → (809, 811)
 882 = 2  × 3² × 7²    → (881, 883)
1152 = 2⁷ × 3²         → (1151, 1153)
...
```

### Statistical Test
- Expected "both unreachable" rate: 59.2% (if independent)
- Twins at smooth: only 33.3% both unreachable
- Ratio: 0.56x — twins at smooth are MORE reachable than random

---

## 4. Spectral Metric (Zeta Zeros)

### The Idea
Define prime "distance" using zeta zero oscillations:
```
signature(p) = [cos(t_k × log(p)) for each zero t_k]
spectral_distance(p, q) = ||signature(p) - signature(q)||
```

### Key Finding
**Spectral distance ≠ log distance** (correlation only 0.355)

### Anomalies Found
- (239, 419) gap 180: spectrally CLOSE despite being far
- (1721, 1847) gap 126: spectrally FAR despite being close

### Resonance Condition
Primes p, q are spectrally close when:
```
t_k × (log(q) - log(p)) ≈ 2π × n_k for multiple zeros
```
This is a **Diophantine condition** on the log ratio.

### Best Resonant Pair
(101, 457): gap 356, spectral distance 1.152
- Works because Δlog aligns with multiple 2π/t_k ratios

---

## 5. Gap Transition Analysis

### Forbidden Transitions
```
(2 → 2): only 1 occurrence (the triple 3,5,7)
(4 → 4): 0 — forbidden!
(8 → 8): 0 — forbidden!
(2 → 8): 0 — forbidden!
(8 → 2): 0 — forbidden!
```

### Explanation: Mod 6 Structure
- Primes > 3 are ≡ 1 or 5 (mod 6)
- Gap 2: alternates residue classes (1→5 or 5→1)
- Gap 6: stays in same class
- Triple prime (p, p+2, p+4) impossible mod 3 for p > 3

### Memory in Gaps
After gap 2: distribution is {4: 0.295, 6: 0.251, 10: 0.266, 12: 0.186}
After gap 4: distribution is {2: 0.324, 6: 0.412, 8: 0.163, 12: 0.101}

**Gaps are NOT memoryless** — but the memory is fully explained by mod 6.

---

## 6. Sonification Attempt

### Pipeline (from ChatGPT)
1. Detrended prime signal: actual - expected (1/log n)
2. FFT → phase scramble → inverse FFT
3. Compare original vs scrambled

### Preliminary Finding
- Local variance ratio: **4.08x** (original vs scrambled)
- Primes have non-uniform "clumping" that phase scrambling destroys
- Top frequencies: periods 6, 3, 10, 5 (modular structure)

### Audio generation blocked by environment issues

---

## Key Takeaways

### What's Known
1. Modular constraints (mod 6, mod 30, etc.) explain most gap structure
2. Spectral properties (zeta zeros) govern fluctuations
3. Power sum representability follows from S-unit theory
4. Smooth number proximity is correlated with power sum bases

### What Might Be Novel
1. The specific set of "unreachable by multiple base triplets" primes
2. The 4x local variance ratio in detrended signal
3. Spectral resonance pairs at non-obvious distances

### The Real Frontier
> "What operator has zeta zeros as eigenvalues — and what metric does that operator induce?"

Everything else reduces to known modular or spectral structure.

---

## Files Created
- `~/primes_orig.wav` (attempted)
- `~/primes_scram.wav` (attempted)
- This notes file

---

## 7. Angular Embeddings (from ChatGPT analysis)

### What Doesn't Work
| Angle choice | Result |
|--------------|--------|
| θ = n (index) | Sunflower pattern, no arithmetic info |
| θ = p (value mod 2π) | Equidistribution, weak mod exclusions |
| θ = gap | Discrete bands, no dynamics |

### What Never Appears
- Spiral arms
- Angular periodicity
- Phase locking
- Attractors
- Local angular rules

### Key Insight
> "Angular embeddings reveal modular constraints and scale effects, but no rotational dynamics or phase structure — reinforcing that prime behavior is spectral and global, not geometric and local."

### The One Worth Trying
**Angle = spectral phase (from zeta zeros), Radius = redshifted position**

This is where genuine "phase" might live — the only angular construction not yet exhausted.

---

## Next Directions
1. Implement proper sonification with working audio
2. Deeper spectral analysis with more zeta zeros
3. Test "unreachable core" primes for special properties
4. Explore gap transition Markov chain in detail
5. **Spectral phase angular embedding** — angle from zeta oscillation phase
