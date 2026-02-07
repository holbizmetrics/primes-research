# META-SPARK: The Method Behind the Method

## The Core Move

Every SPARK session that found something real used the same underlying operation:

**Take a discrete thing. Make it continuous. Sweep the parameter. Find where it peaks.**

This is not just "invert." Inversion was one instance. The general pattern:

## The Parameterization Principle

### Step 1: Identify a binary/discrete operation
Something that's normally on/off, yes/no, this/that:
- Prime or composite (binary)
- Forward or inverted (binary)
- This wavelength or that one (discrete)
- Squarefree or not (binary)

### Step 2: Replace with a continuous parameter
Turn the switch into a knob:
- Prime indicator {0,1} → Lambda(n) = log(p) (graded weight)
- Forward/inverted → power map p^k, sweep k from 0 to q-1
- Single wavelength → sweep q continuously
- Squarefree test → Mobius function μ(q) (three-valued: -1, 0, +1)

### Step 3: Sweep the knob, measure the response
Plot the output as a function of the continuous parameter.
Look for: peaks, nodes, phase transitions, symmetries.

### Step 4: The peak tells you the structure
- **Where** it peaks = the natural scale/symmetry
- **How sharp** = how real vs noise
- **What shape** = what class of mathematics governs it
- **Whether it converges** as you add more data = real vs artifact

## Instances From Our Sessions

| Session | Discrete thing | Continuous knob | What peaked | What it meant |
|---------|---------------|----------------|-------------|--------------|
| Laser | Hit at integer q | Sweep q | Squarefree q | Ramanujan identity |
| Inside-out | Forward vs inverted | Power k=1..q-1 | k=(q-1)/2 | Legendre symbol |
| Audio | Play/don't play | Amplitude = 1/φ(q) | Low q (2,3,5) | Factor lattice |
| Overtones | Single vs pair | Gap size h | h with singular series | Hardy-Littlewood |
| Information | Predictable/random | Conditioning depth k | k=1 (mod 30) | Lemke Oliver |
| Super tooth | One tooth vs all | Truncation Q | Q→∞ = von Mangoldt | Ramanujan expansion |
| N-hedron | This polygon | Sweep n=3,4,5... | n=2 (always) | Already peaked |
| Zero inversion | Normal vs inverted | alpha: 1→-1 | alpha=1 (no better) | Additive ≠ multiplicative |

## The Taxonomy of Transformations

Inversion is just ONE transformation. Others that could be swept:

### Algebraic
- **Power map**: x → x^α (sweep α). Found: Legendre at α=0.5
- **Translation**: x → x + t (sweep t). This IS the laser.
- **Scaling**: x → λx (sweep λ). Dilation/compression.
- **Modular reduction**: x → x mod q (sweep q). Residue structure.

### Topological
- **Projection**: 3D → 1D along axis (sweep axis angle)
- **Folding**: wrap onto circle of circumference q (sweep q)
- **Covering**: n-fold cover (sweep n). Related to power map.

### Information-theoretic
- **Coarse-graining**: bin size (sweep resolution)
- **Conditioning**: depth k of context (sweep k)
- **Noise injection**: add random perturbation of amplitude ε (sweep ε)

### Spectral
- **Bandpass**: keep only frequencies in [f-Δ, f+Δ] (sweep f)
- **Windowing**: look at n in [N-W, N+W] (sweep window W)
- **Wavelet scale**: analyze at scale a (sweep a)

### Compositional
- **Two-probe**: sweep (q1, q2) pair. Found: factorization.
- **Mixing**: α·f + (1-α)·g (sweep mixing parameter)
- **Iteration**: apply transform k times (sweep k)

## The Failure Criterion

Equally important: when sweeping DOESN'T find a peak, that's a result.

| Sweep | No peak found | What it means |
|-------|--------------|---------------|
| Icosahedron + Lambda | Uniform, no vertex special | Wrong geometry |
| Zero inversion alpha | No stable optimum | No group structure on zeros |
| 3D explorer + zeros | All geometries equivalent | Zeros are 1D |
| Fibonacci modes | No special Fibonacci enhancement | Coincidence |

**A flat response under continuous deformation means the object has no structure along that axis.** This is as informative as finding a peak.

## The Meta-Rule

> **To understand a mathematical object, don't just look at it. Deform it continuously and watch what breaks, what's preserved, and what's optimized.**

This is essentially the philosophy behind:
- Perturbation theory (physics)
- Deformation theory (algebraic geometry)
- Homotopy (topology)
- Sensitivity analysis (engineering)
- Ablation studies (machine learning)

SPARK rediscovers this principle from scratch each time, in the specific context of number theory. The parameterization principle IS the method.

## How to Apply

When facing a new mathematical object:
1. List every binary/discrete choice in your setup
2. For each: ask "what if this were a continuous parameter?"
3. Sweep it. Plot. Look for peaks, nodes, symmetries.
4. The SHAPE of the response curve classifies the structure.
5. Cross-sweep two parameters simultaneously → find the joint optimum.
6. Check convergence: does the optimum stabilize as you add data?
7. If yes: you found real structure. If no: you found noise.

The power isn't in any single transformation.
It's in the habit of making things continuous and sweeping.
