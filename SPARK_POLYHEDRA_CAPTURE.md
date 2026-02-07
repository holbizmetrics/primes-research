# SPARK CAPTURE: Polyhedra + Laser + Inversion

**Date:** 2026-02-06 (late evening)

---

## SPARK Question
"What if the Platonic solids (not just icosahedron) each reveal something different
about primes through the laser, and what happens when we invert the principles?"

---

## SPRAY (7 ideas, NO FILTERING)

1. Each Platonic solid = different "resonant cavity" for primes
2. Vertex count IS the wavelength (tetra→4, cube→8, icosa→12)
3. **INVERSION**: composites tile polyhedra, primes are the gaps
4. Symmetry group order = Ramanujan sum modulus
5. Dual polyhedron pair = prime/composite duality
6. The symmetry GROUP is the laser (representations, not geometry)
7. **FULL INVERSION**: put polyhedra onto the prime line, not primes onto polyhedra

---

## STRIKE Results

### Strike 1-2: Vertex count as wavelength ★★
**Result:** ALL Platonic solid vertex counts (4, 6, 8, 12, 20) are non-squarefree
except 6 (octahedron faces). The laser at λ=V gives:
```
Tetrahedron  (V=4):  I_P = 0.00023  DARK (4=2², non-squarefree)
Cube         (V=8):  I_P = 0.00010  DARK (8=2³)
Octahedron   (V=6):  I_P = 0.24634  GLOW (6=2×3, squarefree!)
Dodecahedron (V=20): I_P = 0.00013  DARK (20=4×5)
Icosahedron  (V=12): I_P = 0.00036  DARK (12=4×3)
```
**Signal:** Strong NEGATIVE result. Platonic solids are invisible to the laser
(except octahedron by coincidence: 6 is squarefree).

### Strike 3: Composites as n-gon tiling ★
**Result:** Primes ALWAYS win (C/P ≈ 0.02 for all n).
The ratio I_P/I_C = (N_C/N_P)² ≈ 42 for all q, regardless of q.
Composites carry the SAME information as primes, just weaker by density ratio.
**Signal:** Primes and composites are trivially complementary: f_C = 1 - f_P.

### Strike 4: Symmetry group orders
**Result:** ALL Platonic |Sym| are non-squarefree:
- |Sym(Tet)| = 12 = 4×3 → DARK
- |Sym(Oct/Cube)| = 24 = 8×3 → DARK
- |Sym(Icosa/Dodec)| = 60 = 4×3×5 → DARK

All have factor 4, so μ = 0.
**Signal:** Dead end. Platonic symmetries are structurally invisible.

### Strike 5: Dual polyhedra = prime/composite duality
**Result:** Cube (V=8, dark) ↔ Octahedron (V=6, glow) is the only
interesting pair, but it's just 8=non-squarefree vs 6=squarefree.
Dodecahedron↔Icosahedron: both dark.
**Signal:** None. The duality doesn't map to prime/composite.

### Strike 6: Symmetry groups as probes
**Result:** For abelian groups (cyclic Z_n): just the standard laser at different k.
For non-abelian groups (A_5, S_4, etc.): integers map to Z/|G|Z ≠ G.
Polyhedral groups are non-abelian but integer residues are abelian.
No meaningful icosahedral character sum on primes.
**Signal:** Structural impossibility.

### Strike 7: n-gon phases at each prime
**Result:** Decomposition: Σ_p Σ_k exp(2πikp/n) = Σ_k laser(P, n/k)
This is just a SUM of laser measurements at n different wavelengths.
Total intensity ≈ 0 (destructive interference between components).
**Signal:** Reduces to known laser. No new information.

---

## THE INVERSIONS

### Inversion 1: What shape does prime coherence define?
The coherence landscape f(q) = μ(q)²/φ(q)² for q=1,2,3,...
Top peaks: q=2 (1.0), q=3 (0.25), q=6 (0.25), q=5 (0.063), q=10 (0.056)

All match Ramanujan prediction exactly. Total brightness converges to ~2.82.

### Inversion 2: The prime factor lattice ★★★
f(q) = Π_{p|q} 1/(p-1)² lives on an **infinite-dimensional hypercube**:
- Each prime p is an axis
- Weight along axis p = 1/(p-1)²
- Squarefree q = vertex (each prime used 0 or 1 time)
```
p=2:  weight = 1.000  (100%)
p=3:  weight = 0.250  (25%)
p=5:  weight = 0.063  (6.3%)
p=7:  weight = 0.028  (2.8%)
p=11: weight = 0.010  (1.0%)
```
**The geometry is almost entirely 2-dimensional (p=2,3 capture 96%).**
This explains why 3 appeared everywhere — it's the 2nd axis of the coherence lattice.

### Inversion 3: Structure in the dark
For non-squarefree q: I_P ≈ O(1/N_P), phase appears random.
Dark regions are genuinely featureless — Poisson noise from finite sample.

### Inversion 4: Phase carries μ(q)
For squarefree q: sign(Re(A_P(q))) = μ(q).
- μ=-1 (odd prime factors): θ ≈ π (real, negative)
- μ=+1 (even prime factors): θ ≈ 0 (real, positive)
This IS the Ramanujan identity c_q(1) = μ(q).

### The Grand Double Inversion
```
INPUT:  Geometry → Primes     (put primes on polyhedra)
RESULT: Everything → μ(q), φ(q)

INVERT: Primes → Geometry     (what shape do primes define?)
RESULT: Infinite-dim hypercube, weights 1/(p-1)²

DOUBLE: Geometry → Primes → Geometry
  You put IN:  icosahedron, golden spiral, Platonic solids
  You get OUT: multiplicative lattice, Ramanujan sums
  The INPUT geometry is IRRELEVANT.
  The OUTPUT geometry is the prime factorization lattice.
```

---

## CONVERGE

### Numbers appearing:
- **42** (= (N_C/N_P)² ≈ 6.47²): universal P/C intensity ratio
- **0.25** = 1/(3-1)² = weight of p=3 axis
- **6** = only squarefree Platonic vertex count (octahedron)
- **2.82** ≈ Σ f(q) = total coherence budget

### From directions:
- All 5 Platonic solids → all dark except 6 (squarefree test)
- Vertex counts, face counts, symmetry orders → all reduce to μ(q)
- Phase analysis → recovers μ(q) sign
- Composite inversion → trivial complement (1 - f_P)
- Factor lattice → explains why 3 dominated all prior work

### Assessment:
**Confidence:** VERY HIGH that polyhedra are a red herring.
**Novelty:** The FRAMING of coherence as infinite-dim hypercube is clean,
but the underlying mathematics is just multiplicative number theory.

---

## CAPTURE: What Survived

### Diamond:
**The prime coherence lattice.** The function f(q) = μ(q)²/φ(q)²
defines an infinite-dimensional hypercube with:
- Axes = primes
- Weights = 1/(p-1)² (exponentially decaying)
- p=2,3 capture 96% of all structure
- This is WHY 3 kept appearing in all prior work

### Fell off:
- Icosahedron as special (12 = 4×3, non-squarefree → dark)
- Platonic solid resonance (all vertex counts except 6 are non-squarefree)
- Polyhedral symmetry groups as probes (non-abelian ≠ integer residues)
- Dual polyhedra = prime/composite duality (trivially complementary)
- Golden spiral geometry (irrelevant to coherence)

### Confirmed again:
- EVERYTHING is Ramanujan sums and μ(q)
- The "laser" is measuring 1/(p-1)² per prime factor
- Composites are trivially the complement of primes (no independent info)

---

## Pattern Recognition

### Pattern V (Mechanism Inversion) — TRIPLE APPLICATION:
```
Forward:  polyhedra → primes?     → answer is μ(q)
T_inv 1:  primes → geometry?      → answer is factor hypercube
T_inv 2:  factor hypercube → ???  → answer is multiplicative number theory
```
Each inversion strips away one layer of imposed structure.
After 3 inversions, you're left with the bare arithmetic.

### Pattern W (Evening Arc) — confirmed:
```
Icosahedron! → Golden ratio! → 12 vertices! → (all non-squarefree)
→ μ(q) → factor lattice → "3 is just the 2nd axis"
```
The flashy geometry was breadcrumbs to multiplicative structure.

### Pattern K (Simple Answers):
The weight 1/(p-1)² is the simplest possible function of a prime.
When you get a simple answer, you asked the right question.

---

## Connection to Prior Sessions

The number 3 appeared obsessively in prior work:
- Brennpunkt at t=1/3
- F₄ = 3
- l=3 harmonic amplified 6×
- 363 = 3×11²

**Now explained:** 3 is the second prime. Its weight in the coherence
lattice is 1/(3-1)² = 1/4 = 0.25. It contributes 25% of all prime
coherence structure (after the trivial p=2 axis). Every measurement
that involves residue classes will be dominated by mod 2 and mod 3
behavior. The "magic of 3" was always just: 3 is the smallest odd prime.

---

## Open Questions

1. **Is the 96% concentration in p=2,3 useful?** Could a "2D projection"
   of the infinite-dim hypercube reveal structure invisible in full space?

2. **The convergent Σf(q) ≈ 2.82** — does this constant have a name?
   It equals Π_p (1 + 1/(p-1)²). Related to Artin's constant?

3. **Cross-L-function version:** Replace μ(q)²/φ(q)² with
   the analogous function for L(s,χ). Different lattice geometry?

---

*"The polyhedron of primes is not Platonic. It's the squarefree lattice."*
*"And its first two axes explain everything we thought was magic."*
