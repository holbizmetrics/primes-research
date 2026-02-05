# PRIME EXPLORER v4 SPECIFICATION
## Complete Feature List from 2026-02-05 Session + ADEIS Audit

---

## CORE IDENTITY

**The Prime Explorer is not a toy. It's a spectrometer.**

A computational laboratory for:
- Discrete Mellin analysis of prime distribution
- Finite-N investigation of Hilbert-Pólya conjecture
- Interactive experimental analytic number theory

---

## EXISTING FEATURES (v3, ~12,700 lines)

### Geometry Engine
- [x] 14+ surface types (sphere, torus, icosahedron, critical strip, etc.)
- [x] Golden spiral mapping
- [x] Multiple coordinate systems

### GPF Resonance (from tonight)
- [x] Brennpunkt slider (t ∈ [0, 0.5])
- [x] Wavelength scanner (λ = 2-100)
- [x] Fibonacci wavelength presets
- [x] Coherent backscatter calculation (correct physics)
- [x] Geometry × wavelength matrix
- [x] 21-Mode button
- [x] Semiprime presets with coupled Brennpunkt
- [x] Auto-tune (find optimal t for current λ)
- [x] Semiprime search
- [x] Coupled scan (λ sweep with auto-tune)

### Visualization
- [x] 3D WebGL rendering
- [x] Log-scale amplification display
- [x] ×-factor labels
- [x] Color coding (prime/composite)

---

## NEW FEATURES TO ADD

### A. MATHEMATICAL FOUNDATIONS

#### A1. Mellin Transform Basis
```javascript
// Current: integer wavelength λ ∈ ℕ
// Add: complex frequency s = ½ + it ∈ ℂ

// Basis switch toggle
basisMode: 'integer' | 'complex'

// When complex: λ maps to imaginary part of zeta zeros
// This connects the Explorer to Riemann's explicit formula
```

#### A2. Inverse Mellin Transform
```javascript
// Forward: primes → frequency amplitudes (current)
// Inverse: frequency amplitudes → reconstructed prime positions

// "Close the loop" — show source from shadow
function inverseMellin(amplitudes, targetN) {
    // Reconstruct π(x) from spectral decomposition
    // Compare to actual prime counting
    // Residual = contribution from unknown zeros
}
```

#### A3. Ramanujan Coherence Calculator
```javascript
// The formula we discovered:
// Prime coherence = μ(λ)² / φ(λ)² for squarefree λ

function ramanujanCoherence(lambda) {
    const mu = mobius(lambda);
    if (mu === 0) return 0;  // non-squarefree → dark
    const phi = eulerTotient(lambda);
    return (mu * mu) / (phi * phi);
}

// Display: theoretical vs measured coherence
// Highlight: squarefree λ (primes glow) vs non-squarefree (primes dark)
```

#### A4. GRH Residual Analyzer
```javascript
// The R² = 0.996 fit leaves 0.4% residual
// That residual encodes GRH information

function analyzeResiduals(measuredCoherence, theoreticalCoherence) {
    const residuals = measured.map((m, i) => m - theoretical[i]);

    // Plot residuals vs:
    // - λ (wavelength)
    // - conductor of Dirichlet character
    // - class number

    // Look for: correlation with L-function zeros
}
```

### B. BRENNPUNKT EXTENSIONS

#### B1. Anti-Brennpunkt Search
```javascript
// Conservation law: if composites cancel somewhere,
// they must constructively reinforce elsewhere

function findAntiBrenpunkt(lambda) {
    // Search for (λ, t) where COMPOSITES maximize
    // (opposite of current search)
    // Map the "composite glow" points
}

// Display: Dual map showing prime peaks AND composite peaks
```

#### B2. Brennpunkt Closed Form Predictor
```javascript
// The Hilbert-Pólya connection:
// If Brennpunkt has a closed form, it implies an operator

function theoreticalBrennpunkt(lambda) {
    // Attempt: predict optimal t from λ alone
    // Using: factorization, φ(λ), μ(λ), etc.

    // If successful: we've found the finite-N Hilbert-Pólya operator
}

// Display: predicted vs measured optimal t
// Residual: where does theory fail?
```

#### B3. Dual Brennpunkt Display
```javascript
// Show BOTH focal points simultaneously:
// - t_prime = where primes focus
// - t_composite = where composites focus

// Animate: sweep t and show both populations focusing/defocusing
```

### C. SPECTRAL ANALYSIS

#### C1. Tensor Product Visualization
```javascript
// Axis 1: Ramanujan (modular) — μ(λ), φ(λ)
// Axis 2: Brennpunkt (radial) — optimal t

// 2D heatmap: λ on x-axis, t on y-axis
// Color: combined discriminant D(λ, t)

// Highlight: primorials as eigenstates (max on BOTH axes)
```

#### C2. Primorial Eigenstate Tester
```javascript
const primorials = [2, 6, 30, 210, 2310, 30030];

function testEigenstate(p) {
    const axis1 = ramanujanCoherence(p);
    const axis2 = brennpunktRatio(p, optimalT(p));
    const joint = axis1 * axis2;

    // Compare: is joint optimization > product of individual?
    // If yes: primorials are true eigenstates
}
```

#### C3. Zeta Zero Overlay
```javascript
// Overlay known zeta zeros on wavelength scan
// γ₁ ≈ 14.13, γ₂ ≈ 21.02, γ₃ ≈ 25.01, ...

// Show: do amplitude peaks correlate with zero positions?
// This tests: is λ-space connected to ρ-space?
```

### D. DISCOVERY ENGINE (SPARK Integration)

#### D1. SPARK Mode
```javascript
// Guided discovery workflow
sparkMode: {
    phase: 'SPARK' | 'SPRAY' | 'STRIKE' | 'CONVERGE' | 'CAPTURE',

    // SPARK: suggest questions based on current config
    // SPRAY: generate 5 variations to test
    // STRIKE: auto-test each, show results
    // CONVERGE: highlight patterns (same number, simple fractions)
    // CAPTURE: document finding to session log
}
```

#### D2. Pattern Detector
```javascript
// Auto-flag when:
patterns: {
    sameNumber: [],      // appears 3+ times
    simpleFraction: [],  // ratio is 1/n for small n
    fibonacci: [],       // F_n appears
    squarefree: [],      // μ(λ) ≠ 0 behavior
    convergence: []      // multiple probes agree
}
```

#### D3. T_inv Mode
```javascript
// One-click inversion of current analysis
function invertAnalysis() {
    if (mode === 'maximize P/C') mode = 'minimize P/C';
    if (target === 'primes') target = 'composites';
    if (looking === 'constructive') looking = 'destructive';

    // Re-run analysis with inverted objective
}
```

#### D4. Diamond Sifter
```javascript
// Test robustness of current finding
function siftDiamond(lambda, t) {
    const stability = testAcrossN([200, 500, 1000, 2000, 5000]);
    const sharpness = testNearbyParams(lambda, t, delta=0.01);
    const universality = testAcrossGeometries();

    if (stability && !razorSpike && universality) {
        return 'DIAMOND';
    } else {
        return 'ARTIFACT';
    }
}
```

### E. VISUALIZATION UPGRADES

#### E1. Dual Shadow Display
```javascript
// Side-by-side:
// Left: primes (where they glow)
// Right: composites (where they glow)

// Animation: sweep t, watch both shadows evolve
```

#### E2. Spectral Waterfall
```javascript
// 3D plot: λ on x-axis, N on y-axis, amplitude on z-axis
// Shows: how spectrum evolves with N
// Reveals: stable peaks vs N-dependent artifacts
```

#### E3. Residue Class Coloring
```javascript
// Color primes by residue class (mod 6, mod 10, etc.)
// Visualize: different classes at different positions
// Connect to: Dirichlet characters
```

#### E4. Interactive Explicit Formula
```javascript
// Riemann's explicit formula:
// π(x) = li(x) - Σ li(x^ρ) + ...

// Slider: how many zeros to include
// Watch: reconstruction improve as zeros added
// Gap: what's missing = what we don't know
```

### F. DATA & EXPORT

#### F1. Session Logger
```javascript
// Auto-log all findings in idea_patterns format
sessionLog: [
    { time, config, finding, confidence, connectsTo }
]

// Export: Markdown, JSON, or append to session notes
```

#### F2. Reproducibility Export
```javascript
// Export exact config that produced a finding
// Anyone can load config and verify
exportConfig(finding) → JSON
importConfig(JSON) → restore state
```

#### F3. Paper Figure Mode
```javascript
// High-res export suitable for publication
// Clean labels, proper fonts, no UI chrome
// Multiple formats: SVG, PNG, PDF
```

---

## IMPLEMENTATION PRIORITY

### Phase 1: Mathematical Core
1. Ramanujan coherence calculator (A3)
2. Anti-Brennpunkt search (B1)
3. Tensor product visualization (C1)

### Phase 2: Deep Analysis
4. GRH residual analyzer (A4)
5. Primorial eigenstate tester (C2)
6. Brennpunkt closed form predictor (B2)

### Phase 3: Discovery Engine
7. SPARK mode (D1)
8. Pattern detector (D2)
9. Diamond sifter (D4)

### Phase 4: Research Tools
10. Mellin transform basis switch (A1)
11. Inverse Mellin transform (A2)
12. Zeta zero overlay (C3)

### Phase 5: Publication Ready
13. Paper figure mode (F3)
14. Session logger (F1)
15. Interactive explicit formula (E4)

---

## THE VISION

**Prime Explorer v4 is a computational laboratory for the Hilbert-Pólya conjecture at finite N.**

It bridges:
- Analytic number theory (Dirichlet, Ramanujan, L-functions)
- Mathematical physics (spectroscopy, wave interference)
- Experimental mathematics (interactive exploration)

It enables:
- Visualizing the explicit formula for π(x)
- Testing Brennpunkt as finite-N Hilbert-Pólya
- Discovering structure through SPARK methodology
- Distinguishing diamonds from artifacts

---

*Specification: 2026-02-05*

*"The spectrometer that sees primes"*