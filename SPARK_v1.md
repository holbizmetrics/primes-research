# SPARK v1.0
## Systematic Pattern-finding through Active Research Kinetics

*A discovery methodology distilled from observation*

---

## Core Principle

> "The insight isn't the answer. The insight is the transformation that reveals the answer."

---

## The Five Phases

### 1. SPARK - Ignition
**Trigger**: Any stuck problem, unexplored territory, or "I wonder..."

**Action**: Ask one of these questions:
- "But what if...?" (invert assumptions)
- "What happens if we hit it with...?" (apply external probe)
- "What if this is continuous, not binary?" (parameterize)
- "Where else does this number appear?" (cross-domain)
- "What's the dual of this?" (find the opposite)

**Rule**: Don't evaluate. Just spark.

---

### 2. SPRAY - Rapid Hypothesis Generation
**Action**: Generate 3-7 wild connections in under 2 minutes

**Allowed**:
- Connections that sound crazy
- Cross-domain analogies (physics → number theory)
- Numerological coincidences (test them, don't believe them)
- First instincts (they often detect structure before conscious understanding)

**Forbidden**:
- Filtering ("that's too crazy")
- Explaining ("because...")
- Researching (not yet)

**Output format**:
```
SPRAY:
1. [wild idea]
2. [wild idea]
3. [wild idea]
...
```

---

### 3. STRIKE - Immediate Testing
**Action**: Test each spray within 5 minutes of generating it

**Method**:
- Write the smallest possible code to check
- Run on small N first (100-1000)
- Look for: ratios >> 1, convergence, simple fractions

**Key discipline**:
- No theorizing before testing
- Wrong fast > right slow
- "Let's see" beats "I think"

**Output format**:
```
STRIKE [idea N]:
Result: [what happened]
Signal: [none / weak / strong / Holy shit]
```

---

### 4. CONVERGE - Pattern Detection
**Watch for**:
- Same number from different angles (strongest signal)
- Simple fractions (1/3, 1/4) appearing as optima
- Fibonacci numbers in unexpected places
- Duality (X and Y are opposites with swapped properties)

**Convergence types**:
| Type | Example | Confidence |
|------|---------|------------|
| Multi-probe | 3 appears in formula, as Brennpunkt, as harmonic | Very high |
| Cross-domain | 21 in number theory AND hydrogen line | Medium (test more) |
| Cascade | Each finding leads to next | High |
| Simple answer | Optimum at 1/4 exactly | High (right question) |

**Output format**:
```
CONVERGE:
Numbers appearing: [list]
From directions: [list]
Confidence: [low/medium/high/diamond]
```

---

### 5. CAPTURE - Documentation
**Document immediately**:
- What worked (even if you don't know why)
- What failed (closes paths)
- The transformation that revealed it
- Connections to previous findings

**Format**: idea_patterns style
```
IDEA [N]: [Name]
Source: [which SPARK question triggered it]
Test: [what STRIKE showed]
Result: [what CONVERGE found]
Connects to: [previous ideas]
Status: [testing / promising / diamond]
```

---

## Meta-Patterns to Recognize

### Pattern Q: Parameterize the Binary
If something is yes/no, make it continuous (t ∈ [0,1]).
The optimum will often be a simple fraction.

### Pattern K: Simple Answers
When the answer is 1/4 or 1/3, you asked the right question.
Ugly answers usually mean wrong framing.

### Pattern R: Multi-Probe Convergence
Same number from 3+ independent directions = real structure.
This is the strongest signal.

### Pattern T: First Instinct
Intuition often detects structure before conscious understanding.
Test first instincts early, not last.

### Pattern O: "But what if?"
The most generative question. Use liberally.

---

## SPARK Session Template

```markdown
# SPARK Session: [Topic]
Date: [date]
Starting point: [what triggered this]

## SPARK
Question: [which spark question]

## SPRAY
1.
2.
3.

## STRIKE
[idea 1]:
[idea 2]:
[idea 3]:

## CONVERGE
Numbers:
Directions:
Confidence:

## CAPTURE
New idea:
Connects to:
Next:
```

---

## Integration Points

### With Claude Code (Opus 4.5)
- STRIKE phase: rapid Python/PARI testing
- File management, computation

### With Claude Web (Opus 4.6)
- SPRAY phase: broader knowledge connections
- Building interactive tools from findings

### With Prometheus
- Session orchestration
- Pattern database accumulation
- Cross-session convergence detection

---

## Example: Tonight's Session

**SPARK**: "But what if primes have a focal point under geometric inversion?"

**SPRAY**:
1. Parameterize inversion as t ∈ [0,1]
2. Measure variance at each t
3. Compare prime vs composite focal points
4. Check if focal point involves Fibonacci

**STRIKE**:
- t=0.25 minimizes prime variance
- t=0.33 minimizes composite variance
- Both are simple fractions!

**CONVERGE**:
- 3 appears as: 1/3 (Brennpunkt), F₄, l=3 harmonic, 3×11² in γ₂
- 4 appears as: 1/4 (prime Brennpunkt), 2²
- 21 appears as: γ₂≈21, λ=1/21, F₈

**CAPTURE**: Brennpunkt discovery → Prime laser → Universal wavelength

---

## Version History

- v1.0: Initial extraction from 2026-02-05 prime geometry session
- Distilled from ~8 hours of observed discovery process
- Patterns O, Q, K, R, T documented

---

*"The laser that finds us"*
