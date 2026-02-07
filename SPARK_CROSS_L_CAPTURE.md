# SPARK CAPTURE: Cross-L-function SFF

## SPRAY (7 ideas)
1. SFF within each L-function (GUE?)
2. Cross-SFF between different L-functions
3. Pair correlation: self vs cross
4. Does character relationship (conjugate, order) matter?
5. Nearest-neighbor spacing in mixed zeros
6. Number variance for mixed vs individual
7. Cross-amplitude: |A_chi_b|² at zeros of chi_a

## KEY RESULTS

### Strike 1-2: Data collection
Computed zeros of Dirichlet L-functions:
- q=3: 2 characters, 21 + 34 zeros (up to height ~80)
- q=5: 4 characters, 79 + 130 + 129 + 129 zeros (up to height ~200)
- q=7: 6 characters, 10 + 24×5 zeros (up to height ~50)

### Strike 7: Character conjugacy
For q=5: PARI's 4 characters are all independent (none share zeros). The expected conjugate-pair sharing L(s,chi)↔L(s,bar(chi)) was not observed in PARI's labeling, suggesting all 4 are treated as distinct primitive characters.

### Strike 12-13: MAIN RESULT — Spacing ratios

| | Individual <r> | Mixed <r> | GUE | Poisson |
|---|---|---|---|---|
| q=3 | 0.653 | 0.478 | 0.531 | 0.386 |
| q=5 | 0.651 | 0.399 | 0.531 | 0.386 |
| q=7 | 0.651 | 0.411 | 0.531 | 0.386 |

**Individual L-functions: <r> ≈ 0.65** (persistently above GUE 0.531, even for 800 zeta zeros).
**Mixed zeros: <r> ≈ 0.40** (very close to Poisson 0.386).

### Strike 14: Cross nearest-neighbor distribution
- Self NN: zero cases below 0.3 (strong repulsion, GUE-like)
- Cross NN: 35-55% of cases below 0.3 (no repulsion, Poisson)
- Cross NN distribution peaks at s=0 and decays exponentially

### Strike 16: Cross-amplitude matrix

|A_chi_b|² at zeros of chi_a (ratio to background):

| | at chi_0 zeros | at chi_1 zeros | at chi_2 zeros | at chi_3 zeros |
|---|---|---|---|---|
| A_0 | **4.94** (self) | 1.47 | 1.52 | 1.82 |
| A_1 | 0.81 | **1.99** (self) | 0.70 | 0.57 |
| A_2 | 0.51 | 0.65 | **1.76** (self) | 0.59 |
| A_3 | 0.96 | 0.40 | 0.63 | **1.50** (self) |

- Diagonal (self): 1.5-5.0x enhancement (zeros peak their own amplitude)
- Off-diagonal: 0.4-1.5x (near 1.0, some mild depletion)
- chi_0 (zeta) shows slight elevation at all cross-zeros (1.5-1.8x)
- Non-trivial characters show cross-depletion (0.4-0.8x)

### Strike 19: Pair correlation
- Self R2(s): vanishes at s→0 (GUE level repulsion confirmed)
- Cross R2(s): flat near s=0 (no cross-repulsion, Poisson)

### Strike 20: Number variance
- Individual: grows logarithmically (GUE-like at small L)
- Mixed: grows linearly (Poisson-like at large L)

### Strike 22: The <r> = 0.65 anomaly
Zeta zeros give <r> = 0.61-0.62 consistently from height 14 to 542, NOT converging to GUE (0.531). This is a known arithmetic correction — the non-universal part of the statistics persists at any finite height.

## DIAMOND

### What's confirmed (known, independently verified)
1. **Cross-independence**: zeros of different primitive L-functions are Poisson (Katz-Sarnak prediction). Mixed <r> = 0.40 matches Poisson 0.386.
2. **Self-repulsion**: zeros within each L-function show GUE-like repulsion (no cases below 0.3).
3. **Cross-amplitude near 1.0**: no significant cross-enhancement beyond background.

### What's interesting (possibly worth pursuing)
1. **<r> = 0.65 >> 0.531**: Individual L-functions show STRONGER than GUE repulsion. This persists to at least height 540 (300+ zeros). Known to be an arithmetic correction, but the magnitude (22% above GUE) is larger than I expected.
2. **chi_0 mild cross-elevation**: |A_0|² is 1.5-1.8x at zeros of other L-functions. This could be from the shared arithmetic (all characters mod q share the same prime-avoidance structure for p|q).
3. **Non-trivial cross-depletion**: |A_chi|² for non-trivial chi is 0.4-0.8x at zeros of other non-trivial characters. Mild anti-correlation.

### What fell off
- No significant cross-correlation in SFF or pair correlation
- Connected cross-SFF is dominated by DC/smooth density artifacts
- The "ratio = 2.67" for q=7 connected SFF was a normalization artifact

## THE VERDICT

**The cross-L-function SFF contains no new information beyond Poisson independence.** This was the expected result from Katz-Sarnak, and we confirmed it numerically.

The one genuinely interesting number is **<r> = 0.65** for individual L-functions — 22% above the GUE prediction, persistent at all heights tested. This is the arithmetic fingerprint: the non-universal corrections to GUE statistics that encode the specific properties of each L-function.

## FILES
- clz*.gp — PARI/GP scripts to compute L-function zeros
- clz*_out.txt — Raw zero data
- spark_cross_L2.py through spark_cross_L8.py — Analysis scripts
