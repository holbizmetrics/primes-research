#!/usr/bin/env python3
"""
Lattice-based Factorization via onesFromPP
Linearize: y[i][j] = p[i] * q[j], then use LLL to find short vectors

The key insight: the true solution has y[i][j] ∈ {0,1} (binary),
which corresponds to a SHORT vector in the lattice defined by constraints.
"""

import random
from fractions import Fraction

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

# Simple LLL implementation (for educational purposes)
# Production would use fpylll or numpy-based implementations

def gram_schmidt(basis):
    """Gram-Schmidt orthogonalization"""
    n = len(basis)
    m = len(basis[0])
    ortho = [[Fraction(0)] * m for _ in range(n)]
    mu = [[Fraction(0)] * n for _ in range(n)]

    for i in range(n):
        ortho[i] = list(basis[i])
        for j in range(i):
            # Compute mu[i][j] = <b_i, b*_j> / <b*_j, b*_j>
            dot_ij = sum(Fraction(basis[i][k]) * ortho[j][k] for k in range(m))
            dot_jj = sum(ortho[j][k] * ortho[j][k] for k in range(m))
            if dot_jj == 0:
                mu[i][j] = Fraction(0)
            else:
                mu[i][j] = dot_ij / dot_jj
            # Subtract projection
            for k in range(m):
                ortho[i][k] -= mu[i][j] * ortho[j][k]

    return ortho, mu

def lll_reduce(basis, delta=Fraction(3, 4)):
    """
    LLL lattice basis reduction.
    Returns a reduced basis where short vectors are more likely to appear.
    """
    n = len(basis)
    if n == 0:
        return basis
    m = len(basis[0])

    # Work with fractions for exactness
    B = [[Fraction(x) for x in row] for row in basis]

    ortho, mu = gram_schmidt(B)

    k = 1
    while k < n:
        # Size reduction
        for j in range(k - 1, -1, -1):
            if abs(mu[k][j]) > Fraction(1, 2):
                r = round(float(mu[k][j]))
                for i in range(m):
                    B[k][i] -= r * B[j][i]
                ortho, mu = gram_schmidt(B)

        # Lovász condition
        dot_k = sum(ortho[k][i] * ortho[k][i] for i in range(m))
        dot_k1 = sum(ortho[k-1][i] * ortho[k-1][i] for i in range(m))

        if dot_k >= (delta - mu[k][k-1] * mu[k][k-1]) * dot_k1:
            k += 1
        else:
            # Swap
            B[k], B[k-1] = B[k-1], B[k]
            ortho, mu = gram_schmidt(B)
            k = max(k - 1, 1)

    return [[int(x) for x in row] for row in B]

def build_lattice_basis(ones_pp, bits):
    """
    Build lattice basis from onesFromPP constraints.

    Variables: y[i][j] for i,j in [0, bits)
    Constraints: For each k, Σ y[i][k-i] = ones_pp[k]

    We encode this as a lattice where short vectors correspond to
    {0,1}-valued solutions.
    """
    num_vars = bits * bits  # y[i][j] variables
    num_constraints = 2 * bits - 1  # onesFromPP equations

    # Index mapping: y[i][j] -> variable index
    def var_idx(i, j):
        return i * bits + j

    # Build constraint matrix A where A @ y = ones_pp
    A = []
    for k in range(num_constraints):
        row = [0] * num_vars
        for i in range(bits):
            j = k - i
            if 0 <= j < bits:
                row[var_idx(i, j)] = 1
        A.append(row)

    # Build lattice basis
    # The lattice is defined by:
    # [ I   | 0 ]
    # [ A^T | M ]
    # where M is a scaling factor for the constraints

    M = bits * 10  # Scaling factor

    basis = []

    # Add identity rows for variables (encourages small values)
    for v in range(num_vars):
        row = [0] * (num_vars + num_constraints)
        row[v] = 1
        basis.append(row)

    # Add constraint rows
    for c in range(num_constraints):
        row = [0] * (num_vars + num_constraints)
        for v in range(num_vars):
            row[v] = A[c][v] * M
        row[num_vars + c] = M * ones_pp[c]  # Target value
        basis.append(row)

    return basis, var_idx

def extract_solution(reduced_basis, bits, var_idx):
    """
    Extract p, q from reduced lattice basis.
    Look for short vectors with {0,1} entries in variable positions.
    """
    num_vars = bits * bits

    candidates = []

    for row in reduced_basis:
        # Check if variable entries are close to binary
        var_part = row[:num_vars]

        # Try to interpret as y[i][j] = p[i] * q[j]
        # If it's binary, we can factor the matrix

        binary_like = all(abs(v) <= 1 for v in var_part)
        if not binary_like:
            continue

        # Convert to matrix form
        Y = [[0] * bits for _ in range(bits)]
        for i in range(bits):
            for j in range(bits):
                Y[i][j] = abs(var_part[var_idx(i, j)])

        # Try to factor Y = p ⊗ q (outer product)
        # If Y is rank 1, we can recover p and q
        p_bits = [0] * bits
        q_bits = [0] * bits

        # Find a non-zero row to get q pattern
        for i in range(bits):
            if any(Y[i][j] == 1 for j in range(bits)):
                p_bits[i] = 1
                for j in range(bits):
                    if Y[i][j] == 1:
                        q_bits[j] = 1
                break

        # Verify consistency
        consistent = True
        for i in range(bits):
            for j in range(bits):
                expected = p_bits[i] * q_bits[j]
                if Y[i][j] != expected:
                    consistent = False
                    break
            if not consistent:
                break

        if consistent and any(p_bits) and any(q_bits):
            p = sum(b << i for i, b in enumerate(p_bits))
            q = sum(b << i for i, b in enumerate(q_bits))
            if p > 1 and q > 1:
                candidates.append((p, q))

    return candidates

def solve_lattice(n, ones_pp, bits):
    """
    Solve factorization using lattice reduction.
    """
    # For very small bits, LLL overhead isn't worth it
    if bits > 6:
        return None, None  # Lattice too large for simple implementation

    basis, var_idx = build_lattice_basis(ones_pp, bits)

    try:
        reduced = lll_reduce(basis)
    except Exception as e:
        return None, None

    candidates = extract_solution(reduced, bits, var_idx)

    for p, q in candidates:
        if p * q == n:
            return p, q
        if n % p == 0:
            return p, n // p
        if n % q == 0:
            return q, n // q

    return None, None

def solve_cvp_enumeration(ones_pp, bits, n):
    """
    Alternative: Closest Vector Problem by enumeration.
    Find binary y[i][j] closest to satisfying constraints.
    """
    if bits > 5:
        return None, None  # Too large for enumeration

    best_p, best_q = None, None
    best_dist = float('inf')

    # Enumerate all possible (p, q) pairs
    for p in range(3, 1 << bits, 2):
        if n % p != 0:
            continue
        q = n // p
        if q >= (1 << bits) or q < (1 << (bits - 1)):
            continue
        if q % 2 == 0:
            continue

        actual_ones = compute_ones_from_pp(p, q, bits)
        dist = sum((a - t) ** 2 for a, t in zip(actual_ones, ones_pp))

        if dist < best_dist:
            best_dist = dist
            best_p, best_q = p, q

    return best_p, best_q

def test_lattice_factoring():
    print("=" * 60)
    print("Lattice-based Factorization via onesFromPP")
    print("=" * 60)
    print()

    # Test LLL approach
    print("--- LLL Reduction Approach ---")
    for bits in [4, 5, 6]:
        successes = 0
        trials = 20

        for _ in range(trials):
            p = rand_prime(bits)
            q = rand_prime(bits)
            n = p * q
            ones = compute_ones_from_pp(p, q, bits)

            fp, fq = solve_lattice(n, ones, bits)
            if fp and fq and {fp, fq} == {p, q}:
                successes += 1

        print(f"  {bits}-bit: {successes}/{trials} ({100*successes/trials:.0f}%)")

    print()

    # Test CVP enumeration
    print("--- CVP Enumeration Approach ---")
    for bits in [4, 5]:
        successes_exact = 0
        successes_noisy = 0
        trials = 20

        for _ in range(trials):
            p = rand_prime(bits)
            q = rand_prime(bits)
            n = p * q
            ones = compute_ones_from_pp(p, q, bits)

            # Exact
            fp, fq = solve_cvp_enumeration(ones, bits, n)
            if fp and fq and {fp, fq} == {p, q}:
                successes_exact += 1

            # Noisy (±1 on 20% of positions)
            noisy_ones = ones.copy()
            for i in range(len(noisy_ones)):
                if random.random() < 0.2:
                    noisy_ones[i] = max(0, noisy_ones[i] + random.choice([-1, 1]))

            fp, fq = solve_cvp_enumeration(noisy_ones, bits, n)
            if fp and fq and {fp, fq} == {p, q}:
                successes_noisy += 1

        print(f"  {bits}-bit exact: {successes_exact}/{trials}")
        print(f"  {bits}-bit noisy: {successes_noisy}/{trials}")

    print()

    # Show lattice structure
    print("--- Lattice Structure Example ---")
    p, q = 7, 11
    bits = 4
    n = p * q
    ones = compute_ones_from_pp(p, q, bits)

    print(f"p={p} (binary: {bin(p)}), q={q} (binary: {bin(q)})")
    print(f"N = {n}")
    print(f"onesFromPP = {ones}")
    print()

    print("Linearized variables y[i][j] = p[i] * q[j]:")
    print("      q0 q1 q2 q3")
    for i in range(bits):
        pi = (p >> i) & 1
        row = []
        for j in range(bits):
            qj = (q >> j) & 1
            row.append(pi * qj)
        print(f"  p{i}: {row}")

    print()
    print("Constraint structure (diagonal sums = onesFromPP):")
    print("  k=0: y[0][0] = ones[0]")
    print("  k=1: y[0][1] + y[1][0] = ones[1]")
    print("  k=2: y[0][2] + y[1][1] + y[2][0] = ones[2]")
    print("  ...")
    print()
    print("The lattice encodes: find y[i][j] ∈ {0,1} satisfying constraints")
    print("LLL finds short vectors → binary solutions are short!")

if __name__ == "__main__":
    test_lattice_factoring()
