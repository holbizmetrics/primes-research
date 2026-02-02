# Inverse Spectral Learning for Primes

Research project exploring what L-function zero statistics reveal about arithmetic structure.

## Key Results

1. **Cross-correlation ratios**: Zeta correlates 50% more strongly with Dirichlet than Dirichlet pairs with each other. Explained by Euler product overlap (50% vs 33% matching primes).

2. **Galois induction coupling**: Non-abelian Dedekind zetas (e.g., Q(∛2)) have lower variance than abelian ones (e.g., Q(√2)) due to arithmetic entanglement from the induction relation `Ind₁^{S₃}(1) = 1 ⊕ ρ₂`.

3. **Dedekind variance verifier**: Working tool to predict and verify spacing variance from Galois structure.

## Structure

```
primes-research/
├── README.md
├── dedekind_verification_note.md   # Summary of verification approach
├── state/
│   └── state.md                    # Full project state (Sessions 1-6)
├── tools/
│   ├── verify.gp                   # PARI/GP variance verifier
│   ├── dedekind_verifier.py        # Python wrapper
│   ├── dedekind.gp                 # Dedekind zero computation
│   ├── cross_repulsion.py          # Cross-family analysis
│   ├── ml_zeros.py                 # ML feature extraction
│   ├── var_conv.py                 # Variance convergence
│   └── artin_variance.py           # Artin L-function analysis
└── sessions/                       # Session logs (future)
```

## Quick Start

```bash
# Verify a Dedekind zeta's spacing variance
gp -q tools/verify.gp

# Or manually:
gp -q -f << 'EOF'
v(z)={my(s,m,n);s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}
K=nfinit(x^3-2);z=lfunzeros(lfuncreate(K),100);print("Variance: ",v(z))
EOF
```

## Status

- Sessions 1-4: Empirical exploration
- Session 5: Dedekind anomaly explained (cross-family repulsion)
- Session 6: Artin claim corrected, Galois coupling discovered, verifier built

## Requirements

- PARI/GP 2.15+ (with lfun package)
- Python 3.10+ (for wrapper scripts)
