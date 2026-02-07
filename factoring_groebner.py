#!/usr/bin/env python3
"""
Gröbner Basis approach to factorization via onesFromPP
The bilinear structure: onesFromPP[k] = Σᵢ pᵢ × qₖ₋ᵢ
"""

import random

def is_prime(n, k=5):
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0: r += 1; d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def rand_prime(bits):
    while True:
        n = random.getrandbits(bits) | (1 << (bits-1)) | 1
        if is_prime(n): return n

def compute_ones_from_pp(p, q, bits):
    ones = []
    for k in range(2 * bits - 1):
        count = 0
        for i in range(bits):
            j = k - i
            if 0 <= j < bits:
                count += ((p >> i) & 1) * ((q >> j) & 1)
        ones.append(count)
    return ones

def build_polynomial_system(ones_pp, bits):
    """
    Build the polynomial system:
    For each k: Σᵢ pᵢ × qₖ₋ᵢ = ones_pp[k]

    Variables: p0, p1, ..., p_{n-1}, q0, q1, ..., q_{n-1}

    Returns list of (coefficients, constant) tuples
    Each equation: sum of products = constant
    """
    equations = []

    for k in range(2 * bits - 1):
        # Equation: Σᵢ pᵢqₖ₋ᵢ = ones_pp[k]
        terms = []  # List of (i, j) pairs where we have pᵢqⱼ
        for i in range(bits):
            j = k - i
            if 0 <= j < bits:
                terms.append((i, j))
        equations.append((terms, ones_pp[k]))

    return equations

def solve_by_substitution(equations, bits, n):
    """
    Solve bilinear system by alternating substitution.
    Fix q, solve for p linearly. Fix p, solve for q linearly. Iterate.
    """
    # Initialize with sqrt(n) approximation
    sqrt_n = int(n ** 0.5)

    # Try multiple initializations
    for init_q in [sqrt_n, sqrt_n + 1, sqrt_n - 1, sqrt_n + 2]:
        q_bits = [(init_q >> i) & 1 for i in range(bits)]

        for iteration in range(20):
            # Given q, solve for p
            # Each equation becomes linear in p: Σᵢ pᵢ × qₖ₋ᵢ = target
            # This is: Σᵢ pᵢ × q[k-i] = target

            p_bits = [0] * bits

            # Use equations to constrain p
            for k, (terms, target) in enumerate(equations):
                # terms are (i, j) pairs
                # Equation: Σ p[i] * q[j] = target
                # If we know q, this is: Σ p[i] * q_bits[j] = target

                known_sum = 0
                unknown_indices = []
                for (i, j) in terms:
                    if q_bits[j] == 1:
                        unknown_indices.append(i)
                    # If q_bits[j] == 0, term contributes 0

                # Simplest case: if only one unknown p[i], we can solve
                if len(unknown_indices) == 1:
                    i = unknown_indices[0]
                    # p[i] * 1 = target (since q[j]=1 for the one term)
                    # So p[i] = target if target ∈ {0, 1}
                    if target in [0, 1]:
                        p_bits[i] = target

            # Reconstruct p
            p_val = sum(b << i for i, b in enumerate(p_bits))

            # Check if p divides n
            if p_val > 1 and n % p_val == 0:
                q_val = n // p_val
                if 1 < q_val < n:
                    return p_val, q_val

            # Given p, solve for q (symmetric)
            for k, (terms, target) in enumerate(equations):
                unknown_indices = []
                for (i, j) in terms:
                    if p_bits[i] == 1:
                        unknown_indices.append(j)

                if len(unknown_indices) == 1:
                    j = unknown_indices[0]
                    if target in [0, 1]:
                        q_bits[j] = target

            q_val = sum(b << i for i, b in enumerate(q_bits))

            if q_val > 1 and n % q_val == 0:
                p_val = n // q_val
                if 1 < p_val < n:
                    return p_val, q_val

    return None, None

def solve_by_linearization(equations, bits, n):
    """
    Linearization: introduce y[i][j] = p[i] * q[j]
    This gives us a linear system in n² variables.
    Plus consistency: y[i][j] * y[k][l] = y[i][l] * y[k][j]

    For small cases, we can enumerate.
    """
    # For very small bits, just enumerate
    if bits <= 6:
        for p in range(3, 1 << bits, 2):
            if n % p == 0:
                q = n // p
                if 1 < q < (1 << bits) and q % 2 == 1:
                    actual = compute_ones_from_pp(p, q, bits)
                    target = [eq[1] for eq in equations]
                    if actual == target:
                        return p, q
    return None, None

def test_groebner_factoring():
    print("=" * 60)
    print("Bilinear System Solving (Gröbner-style)")
    print("=" * 60)
    print()

    for bits in [4, 5, 6]:
        print(f"--- {bits}-bit factors ---")

        successes_sub = 0
        successes_lin = 0
        trials = 20

        for _ in range(trials):
            p = rand_prime(bits)
            q = rand_prime(bits)
            n = p * q

            ones = compute_ones_from_pp(p, q, bits)
            equations = build_polynomial_system(ones, bits)

            # Try substitution method
            fp, fq = solve_by_substitution(equations, bits, n)
            if fp and fq and {fp, fq} == {p, q}:
                successes_sub += 1

            # Try linearization
            fp, fq = solve_by_linearization(equations, bits, n)
            if fp and fq and {fp, fq} == {p, q}:
                successes_lin += 1

        print(f"  Alternating substitution: {successes_sub}/{trials}")
        print(f"  Linearization + enum:     {successes_lin}/{trials}")
        print()

    # Show the polynomial system structure
    print("--- Polynomial System Structure ---")
    p, q = 7, 11
    bits = 4
    ones = compute_ones_from_pp(p, q, bits)
    equations = build_polynomial_system(ones, bits)

    print(f"p={p}, q={q}, bits={bits}")
    print("Equations (Σ pᵢqⱼ = constant):")
    for k, (terms, target) in enumerate(equations):
        term_str = " + ".join(f"p{i}q{j}" for i, j in terms)
        print(f"  k={k}: {term_str} = {target}")

if __name__ == "__main__":
    test_groebner_factoring()
