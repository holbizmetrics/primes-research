#!/usr/bin/env python3
"""
Dedekind Zero Verifier

Predicts expected spacing variance from Galois structure,
compares to measured variance, flags anomalies.

Usage:
  python3 dedekind_verifier.py          # Run built-in tests
  python3 dedekind_verifier.py check    # Interactive mode
"""

import math
import subprocess
import sys

# =============================================================================
# THEORETICAL PREDICTIONS
# =============================================================================

def predict_variance(galois_type, n_factors, has_induction_coupling=False):
    """
    Predict Dedekind zeta spacing variance from Galois structure.

    Based on:
    - Independent merging: var ~ 0.47
    - Full correlation: var ~ 0.27 (GUE)
    - Cross-correlation reduces variance proportionally

    Parameters:
    - galois_type: "abelian" or "non-abelian"
    - n_factors: number of Artin L-function factors
    - has_induction_coupling: True if factors related by Galois induction
    """

    # Base variances from empirical/theoretical work
    V_GUE = 0.27          # Single L-function (GUE limit)
    V_INDEP = 0.47        # Independent merging of two GUE

    # Cross-correlation estimates
    CORR_ABELIAN = 0.34       # ζ vs Dirichlet (measured)
    CORR_NONABELIAN = 0.45    # ζ vs induced Artin (estimated from Q(∛2))

    if n_factors == 1:
        return V_GUE, "single L-function"

    # Effective correlation
    if has_induction_coupling:
        corr = CORR_NONABELIAN
        reason = f"non-abelian with induction coupling (corr ≈ {corr:.0%})"
    else:
        corr = CORR_ABELIAN
        reason = f"abelian or no induction coupling (corr ≈ {corr:.0%})"

    # Interpolate between independent and fully correlated
    # var = V_INDEP * (1 - corr) + V_GUE * corr
    # But this is for 2 factors. For more factors, variance increases.

    if n_factors == 2:
        var = V_INDEP * (1 - corr) + V_GUE * corr
    else:
        # More factors: start from 2-factor base, add penalty
        base = V_INDEP * (1 - corr) + V_GUE * corr
        # Each additional factor pair adds variance
        # Rough model: var scales with (n_factors - 1) * some_factor
        factor_penalty = 0.08 * (n_factors - 2)
        var = base + factor_penalty
        reason += f" + {n_factors} factors"

    return var, reason


def analyze_field(field_desc):
    """
    Analyze a number field and predict its Dedekind variance.

    field_desc: string like "Q(sqrt(2))", "Q(cbrt(2))", "Q(zeta_8)"

    Returns: (predicted_var, galois_info, factors)
    """

    field_desc = field_desc.lower().replace(" ", "")

    # Quadratic fields: Q(√d)
    if "sqrt" in field_desc or "√" in field_desc:
        return {
            "type": "quadratic",
            "galois": "Z/2 (abelian)",
            "factors": ["ζ(s)", "L(s,χ)"],
            "n_factors": 2,
            "has_induction": False,
            "predicted_var": predict_variance("abelian", 2, False)[0],
            "reason": "Quadratic: ζ_K = ζ × L(χ), abelian correlation"
        }

    # Pure cubic fields: Q(∛d)
    if "cbrt" in field_desc or "∛" in field_desc or "^(1/3)" in field_desc:
        return {
            "type": "cubic (pure)",
            "galois": "S₃ (non-abelian)",
            "factors": ["ζ(s)", "L(s,ρ₂)"],
            "n_factors": 2,
            "has_induction": True,  # Ind(1) = 1 ⊕ ρ₂
            "predicted_var": predict_variance("non-abelian", 2, True)[0],
            "reason": "Cubic S₃: induction coupling Ind(1) = 1 ⊕ ρ₂"
        }

    # Cyclotomic: Q(ζ_n)
    if "zeta_" in field_desc or "ζ_" in field_desc:
        # Extract n
        import re
        match = re.search(r'[ζzeta_]+(\d+)', field_desc)
        if match:
            n = int(match.group(1))
            phi_n = euler_phi(n)
            n_factors = phi_n  # One factor per character
            return {
                "type": f"cyclotomic Q(ζ_{n})",
                "galois": f"(Z/{n}Z)* ≅ Z/{phi_n}Z (abelian)",
                "factors": [f"L(s,χ^k) for k=0..{phi_n-1}"],
                "n_factors": phi_n,
                "has_induction": False,
                "predicted_var": predict_variance("abelian", phi_n, False)[0],
                "reason": f"Cyclotomic: {phi_n} abelian factors, high variance expected"
            }

    # Quartic: Q(∜d)
    if "4thrt" in field_desc or "∜" in field_desc or "^(1/4)" in field_desc:
        return {
            "type": "quartic (pure)",
            "galois": "D₄ (non-abelian)",
            "factors": ["ζ(s)", "L(s,χ)", "L(s,χ')", "L(s,ρ₂)"],
            "n_factors": 4,
            "has_induction": True,
            "predicted_var": predict_variance("non-abelian", 4, True)[0],
            "reason": "Quartic D₄: 4 factors with partial induction coupling"
        }

    return {
        "type": "unknown",
        "galois": "unknown",
        "factors": ["?"],
        "n_factors": None,
        "has_induction": None,
        "predicted_var": None,
        "reason": "Field type not recognized"
    }


def euler_phi(n):
    """Euler's totient function."""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result


# =============================================================================
# MEASUREMENT (via PARI/GP)
# =============================================================================

def measure_variance_gp(field_poly, height=50):
    """
    Compute Dedekind zeta zeros and measure spacing variance using PARI/GP.

    field_poly: polynomial defining the field, e.g., "x^2-2" for Q(√2)
    height: compute zeros up to this height

    Returns: (variance, n_zeros, zeros_list) or (None, 0, []) on error
    """

    gp_code = f'''
    v(z)={{my(s,m,n);if(#z<3,return(-1));s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}}
    K=nfinit({field_poly});
    z=lfunzeros(lfuncreate(K),{height});
    print("NZEROS:",#z);
    print("VAR:",precision(v(z),6));
    for(i=1,min(10,#z),print("Z:",precision(z[i],6)));
    '''

    try:
        result = subprocess.run(
            ['gp', '-q', '-f'],
            input=gp_code.encode(),
            capture_output=True,
            timeout=60
        )
        output = result.stdout.decode()

        n_zeros = 0
        variance = None
        zeros = []

        for line in output.strip().split('\n'):
            if line.startswith('NZEROS:'):
                n_zeros = int(line.split(':')[1])
            elif line.startswith('VAR:'):
                variance = float(line.split(':')[1])
            elif line.startswith('Z:'):
                zeros.append(float(line.split(':')[1]))

        return variance, n_zeros, zeros

    except Exception as e:
        print(f"  GP error: {e}")
        return None, 0, []


# =============================================================================
# VERIFICATION
# =============================================================================

def verify_field(field_desc, field_poly, height=50, tolerance=0.15):
    """
    Full verification: predict variance, measure, compare.

    Returns: dict with results and pass/fail status
    """

    print(f"\n{'='*60}")
    print(f"Field: {field_desc}")
    print(f"{'='*60}")

    # Theoretical prediction
    analysis = analyze_field(field_desc)
    predicted = analysis["predicted_var"]

    print(f"\nStructure:")
    print(f"  Galois group: {analysis['galois']}")
    print(f"  Factors: {' × '.join(analysis['factors'])}")
    print(f"  Induction coupling: {analysis['has_induction']}")
    print(f"\nPrediction:")
    print(f"  Expected variance: {predicted:.3f}" if predicted else "  Expected variance: unknown")
    print(f"  Reason: {analysis['reason']}")

    # Measurement
    print(f"\nMeasurement (height={height}):")
    measured, n_zeros, zeros = measure_variance_gp(field_poly, height)

    if measured is None:
        print("  FAILED to compute zeros")
        return {"status": "ERROR", "analysis": analysis}

    print(f"  Zeros found: {n_zeros}")
    print(f"  Measured variance: {measured:.3f}")

    # Comparison
    if predicted is not None:
        diff = abs(measured - predicted)
        rel_diff = diff / predicted

        print(f"\nVerification:")
        print(f"  |measured - predicted| = {diff:.3f}")
        print(f"  Relative difference: {rel_diff:.1%}")

        if rel_diff <= tolerance:
            status = "PASS"
            print(f"  Status: ✓ PASS (within {tolerance:.0%} tolerance)")
        else:
            status = "FAIL"
            print(f"  Status: ✗ FAIL (exceeds {tolerance:.0%} tolerance)")
            print(f"  → Possible computation error or unusual arithmetic")
    else:
        status = "UNKNOWN"
        print(f"\nVerification: Cannot verify (no prediction for this field type)")

    return {
        "status": status,
        "analysis": analysis,
        "predicted": predicted,
        "measured": measured,
        "n_zeros": n_zeros,
        "difference": diff if predicted else None
    }


# =============================================================================
# MAIN
# =============================================================================

def run_builtin_tests():
    """Run verification on known fields."""

    print("\n" + "="*60)
    print("DEDEKIND ZERO VERIFIER - Built-in Test Suite")
    print("="*60)

    test_cases = [
        ("Q(√2)", "x^2-2"),
        ("Q(√3)", "x^2-3"),
        ("Q(√5)", "x^2-5"),
        ("Q(∛2)", "x^3-2"),
        ("Q(∜2)", "x^4-2"),
    ]

    results = []
    for field_desc, field_poly in test_cases:
        result = verify_field(field_desc, field_poly, height=50)
        results.append((field_desc, result))

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"\n{'Field':<12} {'Predicted':>10} {'Measured':>10} {'Status':>8}")
    print("-"*44)

    for field_desc, result in results:
        pred = f"{result['predicted']:.3f}" if result.get('predicted') else "?"
        meas = f"{result['measured']:.3f}" if result.get('measured') else "?"
        status = result['status']
        print(f"{field_desc:<12} {pred:>10} {meas:>10} {status:>8}")

    passes = sum(1 for _, r in results if r['status'] == 'PASS')
    total = len(results)
    print(f"\nPassed: {passes}/{total}")


def interactive_mode():
    """Interactive verification mode."""
    print("\nDedekind Zero Verifier - Interactive Mode")
    print("Enter field polynomial (e.g., 'x^2-5' for Q(√5))")
    print("Type 'quit' to exit\n")

    while True:
        poly = input("Polynomial: ").strip()
        if poly.lower() in ('quit', 'exit', 'q'):
            break

        # Try to guess field description from polynomial
        if 'x^2' in poly:
            desc = f"Q(√?)"
        elif 'x^3' in poly:
            desc = f"Q(∛?)"
        elif 'x^4' in poly:
            desc = f"Q(∜?)"
        else:
            desc = "Custom field"

        verify_field(desc, poly, height=50)
        print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        interactive_mode()
    else:
        run_builtin_tests()
