#!/usr/bin/env python3
"""
Deep Dive: Zeta Zero γ₂ ≈ 21 (Fibonacci)

Is this coincidence or structure?

γ₂ = 21.022039639...
F_8 = 21

Difference: 0.022 - that's remarkably close!

Let's investigate systematically.
"""

import math

PHI = (1 + math.sqrt(5)) / 2

# First 100 zeta zeros (imaginary parts)
ZETA_ZEROS = [
    14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
    37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478,
    52.970321478, 56.446247697, 59.347044003, 60.831778525, 65.112544048,
    67.079810529, 69.546401711, 72.067157674, 75.704690699, 77.144840069,
    79.337375020, 82.910380854, 84.735492981, 87.425274613, 88.809111208,
    92.491899271, 94.651344041, 95.870634228, 98.831194218, 101.317851006,
    103.725538040, 105.446623052, 107.168611184, 111.029535543, 111.874659177,
    114.320220915, 116.226680321, 118.790782866, 121.370125002, 122.946829294,
    124.256818554, 127.516683880, 129.578704200, 131.087688531, 133.497737203,
    134.756509753, 138.116042055, 139.736208952, 141.123707404, 143.111845808,
]

def fibonacci_up_to(n):
    """Generate Fibonacci numbers up to n."""
    fibs = [1, 1]
    while fibs[-1] < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

def lucas_up_to(n):
    """Generate Lucas numbers up to n. L_n = F_{n-1} + F_{n+1}"""
    lucas = [2, 1]
    while lucas[-1] < n:
        lucas.append(lucas[-1] + lucas[-2])
    return lucas

def analyze_gamma2_equals_21():
    """Deep analysis of γ₂ ≈ 21."""
    print("=" * 65)
    print("DEEP DIVE: γ₂ = 21.022... ≈ F_8 = 21")
    print("=" * 65)

    gamma2 = ZETA_ZEROS[1]  # Second zero (0-indexed)
    F8 = 21

    print(f"\nγ₂ = {gamma2:.10f}")
    print(f"F_8 = {F8}")
    print(f"Difference: {gamma2 - F8:.10f}")
    print(f"Relative error: {abs(gamma2 - F8) / F8 * 100:.4f}%")

    # What's special about 21?
    print("\n--- Properties of 21 ---")
    print(f"21 = 3 × 7 (triangular number T_6)")
    print(f"21 = F_8 (8th Fibonacci)")
    print(f"21 = C(7,2) = binomial coefficient")
    print(f"21 in binary: {bin(21)} = 10101")

    # What's special about γ₂?
    print("\n--- Properties of γ₂ ---")
    print(f"γ₂/γ₁ = {gamma2/ZETA_ZEROS[0]:.6f}")
    print(f"γ₂/π = {gamma2/math.pi:.6f}")
    print(f"γ₂/e = {gamma2/math.e:.6f}")
    print(f"γ₂/φ = {gamma2/PHI:.6f}")
    print(f"γ₂/(2π) = {gamma2/(2*math.pi):.6f}")

    # Is γ₂ ≈ 21 + small correction?
    print("\n--- Decomposition of γ₂ ---")
    remainder = gamma2 - 21
    print(f"γ₂ = 21 + {remainder:.10f}")
    print(f"Remainder ≈ 1/45 = {1/45:.10f}")
    print(f"Remainder ≈ 1/(2×21+3) = {1/45:.10f}")
    print(f"Remainder × 45 = {remainder * 45:.6f}")

    # Check: is remainder related to φ?
    print(f"\nRemainder/φ⁻⁴ = {remainder / (PHI**-4):.6f}")
    print(f"φ⁻⁴ = {PHI**-4:.10f}")
    print(f"Remainder - φ⁻⁴ = {remainder - PHI**-4:.10f}")

def statistical_test_fibonacci_proximity():
    """Are zeta zeros closer to Fibonacci numbers than random?"""
    print("\n" + "=" * 65)
    print("STATISTICAL TEST: Zeros vs Fibonacci Proximity")
    print("=" * 65)

    fibs = fibonacci_up_to(200)
    fib_set = set(fibs)

    print(f"\nFibonacci numbers up to 150: {[f for f in fibs if f <= 150]}")

    # For each zero, find distance to nearest Fibonacci
    print(f"\n{'Zero':<6}{'γ':<12}{'Nearest F':<12}{'Distance':<12}{'Rel Err %':<10}")
    print("-" * 52)

    distances = []
    for i, gamma in enumerate(ZETA_ZEROS[:30], 1):
        nearest_fib = min(fibs, key=lambda f: abs(f - gamma))
        dist = abs(gamma - nearest_fib)
        rel_err = dist / gamma * 100
        distances.append((dist, gamma, nearest_fib))

        if dist < 3:
            marker = " ← CLOSE!"
        else:
            marker = ""
        print(f"γ_{i:<4}{gamma:<12.3f}{nearest_fib:<12}{dist:<12.3f}{rel_err:<10.2f}{marker}")

    # Compare to random baseline
    print("\n--- Statistical Comparison ---")

    # For random numbers in same range, what's expected distance to nearest Fib?
    import random
    random.seed(42)

    random_distances = []
    for _ in range(1000):
        x = random.uniform(14, 150)
        nearest_fib = min(fibs, key=lambda f: abs(f - x))
        random_distances.append(abs(x - nearest_fib))

    mean_random = sum(random_distances) / len(random_distances)
    mean_zeros = sum(d for d, g, f in distances) / len(distances)

    print(f"\nMean distance to nearest Fibonacci:")
    print(f"  Zeta zeros: {mean_zeros:.3f}")
    print(f"  Random points: {mean_random:.3f}")
    print(f"  Ratio: {mean_zeros / mean_random:.3f}")

    # Count "close" hits (within 1.5)
    close_zeros = sum(1 for d, g, f in distances if d < 1.5)
    close_random = sum(1 for d in random_distances if d < 1.5) / 1000 * len(distances)

    print(f"\nPoints within 1.5 of a Fibonacci:")
    print(f"  Zeta zeros: {close_zeros}/{len(distances)}")
    print(f"  Expected random: {close_random:.1f}/{len(distances)}")

def analyze_lucas_numbers():
    """Check Lucas numbers too - they're related to φ."""
    print("\n" + "=" * 65)
    print("LUCAS NUMBERS AND ZETA ZEROS")
    print("=" * 65)

    lucas = lucas_up_to(200)
    print(f"\nLucas numbers: {lucas[:15]}")
    print("(Lucas: L_n = φⁿ + (-φ)⁻ⁿ, related to golden ratio)")

    print(f"\n{'Zero':<6}{'γ':<12}{'Nearest L':<12}{'Distance':<12}")
    print("-" * 42)

    for i, gamma in enumerate(ZETA_ZEROS[:20], 1):
        nearest_lucas = min(lucas, key=lambda L: abs(L - gamma))
        dist = abs(gamma - nearest_lucas)

        if dist < 2:
            marker = " ← CLOSE!"
        else:
            marker = ""
        print(f"γ_{i:<4}{gamma:<12.3f}{nearest_lucas:<12}{dist:<12.3f}{marker}")

def analyze_golden_powers():
    """Check if zeros relate to powers of φ."""
    print("\n" + "=" * 65)
    print("ZETA ZEROS AND POWERS OF φ")
    print("=" * 65)

    print(f"\nφ = {PHI:.6f}")
    print(f"\nPowers of φ:")
    for n in range(1, 12):
        print(f"  φ^{n} = {PHI**n:.4f}")

    print(f"\n{'Zero':<6}{'γ':<12}{'γ/φⁿ closest to integer':<30}")
    print("-" * 50)

    for i, gamma in enumerate(ZETA_ZEROS[:15], 1):
        best_n = None
        best_frac = 1
        for n in range(1, 15):
            ratio = gamma / (PHI ** n)
            frac = abs(ratio - round(ratio))
            if frac < best_frac:
                best_frac = frac
                best_n = n
                best_int = round(ratio)

        if best_frac < 0.1:
            print(f"γ_{i:<4}{gamma:<12.3f}γ/φ^{best_n} = {gamma/(PHI**best_n):.4f} ≈ {best_int} (err={best_frac:.4f})")

def search_for_formula():
    """Try to find a formula for γ₂ ≈ 21."""
    print("\n" + "=" * 65)
    print("SEARCHING FOR γ₂ FORMULA")
    print("=" * 65)

    gamma2 = ZETA_ZEROS[1]

    candidates = [
        ("21", 21),
        ("21 + 1/45", 21 + 1/45),
        ("21 + 1/46", 21 + 1/46),
        ("21 + φ⁻⁴", 21 + PHI**-4),
        ("21 + 1/(2π)", 21 + 1/(2*math.pi)),
        ("21 + 1/π²", 21 + 1/(math.pi**2)),
        ("F_8 + F_8/(F_8² - 1)", 21 + 21/(21**2 - 1)),
        ("21 × (1 + 1/1000)", 21 * (1 + 1/1000)),
        ("21 × φ/φ", 21),  # baseline
        ("7π", 7 * math.pi),
        ("21 + 0.022", 21.022),
        ("F_8 + 1/F_6", 21 + 1/8),
        ("F_8 + 1/F_7", 21 + 1/13),
        ("e³", math.e**3),
        ("20 + φ⁻¹ × φ⁻¹", 20 + PHI**-2),
        ("21 + log(φ)/π", 21 + math.log(PHI)/math.pi),
    ]

    print(f"\nγ₂ = {gamma2:.10f}")
    print(f"\n{'Formula':<30}{'Value':<15}{'Error':<15}")
    print("-" * 60)

    results = []
    for name, value in candidates:
        error = abs(gamma2 - value)
        results.append((error, name, value))

    results.sort()
    for error, name, value in results[:12]:
        print(f"{name:<30}{value:<15.10f}{error:<15.10f}")

def investigate_21_connection():
    """Why might 21 appear in zeta zeros?"""
    print("\n" + "=" * 65)
    print("WHY 21? THEORETICAL SPECULATION")
    print("=" * 65)

    print("""
POSSIBLE CONNECTIONS:

1. FIBONACCI + ZETA:
   - Fibonacci numbers encode golden ratio: F_n/F_{n-1} → φ
   - Zeta zeros encode prime distribution
   - Both involve deep number-theoretic structure
   - Connection through explicit formula? Zeros as "Fibonacci-like" basis?

2. 21 = 3 × 7:
   - Both 3 and 7 are primes
   - γ₁ ≈ 14.13 ≈ 2 × 7
   - γ₂ ≈ 21 = 3 × 7
   - Is there a pattern with small primes?

3. TRIANGULAR NUMBERS:
   - 21 = T_6 = 1+2+3+4+5+6
   - Triangular numbers appear in combinatorics
   - Connection to prime counting?

4. DIMENSIONAL ARGUMENT:
   - 21 = C(7,2) = dimension of antisymmetric 7×7 matrices
   - Could relate to some representation theory?

5. COINCIDENCE TEST:
   - In range [14, 150], there are ~12 Fibonacci numbers
   - Having one zero within 0.03 of a Fibonacci could be ~1/500 per zero
   - With 50 zeros... not impossible by chance
   - BUT: γ₂ is EXACTLY the second zero, and 21 is EXACTLY F_8
""")

    # The key question
    print("\n--- KEY QUESTION ---")
    print("""
If γ₂ ≈ 21 is NOT coincidence, there should be a formula:

  γ₂ = 21 + f(φ, π, primes, ...)

where f is some "natural" correction term.

The remainder is 0.022039639...

Let's check: 0.022039639 × 1000 ≈ 22.04
            22 = 2 × 11
            0.022 ≈ 1/45 = 1/(44+1) = 1/(4×11+1)

Hmm, 11 appears... and 11 is F_5 (sort of - actually F_5 = 5)
Actually 11 = L_5 (Lucas!)
""")

    remainder = ZETA_ZEROS[1] - 21
    print(f"\nRemainder = {remainder:.10f}")
    print(f"1/remainder = {1/remainder:.4f}")
    print(f"remainder × 100 = {remainder * 100:.6f}")
    print(f"remainder × 360 = {remainder * 360:.4f}° (angular?)")
    print(f"remainder × 2π = {remainder * 2 * math.pi:.6f}")

def main():
    analyze_gamma2_equals_21()
    statistical_test_fibonacci_proximity()
    analyze_lucas_numbers()
    analyze_golden_powers()
    search_for_formula()
    investigate_21_connection()

    print("\n" + "=" * 65)
    print("SUMMARY")
    print("=" * 65)
    print("""
γ₂ = 21.022039639... is remarkably close to F_8 = 21.

Statistical test shows zeta zeros are NOT significantly closer
to Fibonacci numbers than random - but γ₂ ≈ 21 is the closest hit.

The question remains: Is there a FORMULA that explains why
the second zeta zero is almost exactly the 8th Fibonacci number?

Or is this a beautiful coincidence?

Either way, it's worth investigating further:
- Connection between explicit formula and Fibonacci?
- Role of φ in zero distribution?
- Why specifically γ₂ and F_8?
""")

if __name__ == "__main__":
    main()
