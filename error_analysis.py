#!/usr/bin/env python3
"""
Error Distribution Analysis for onesFromPP Prediction
Key question: Do errors cluster? Are some positions more reliable?
"""

import random
from collections import defaultdict

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

def simulate_prediction_errors(bits, samples=500):
    """
    Simulate ML prediction errors.
    Based on reported results: interior ~98.8%, edges ~64%
    """
    errors_by_position = defaultdict(list)
    total_positions = 2 * bits - 1

    for _ in range(samples):
        p = rand_prime(bits)
        q = rand_prime(bits)
        true_ones = compute_ones_from_pp(p, q, bits)

        # Simulate predictions with position-dependent accuracy
        for k in range(total_positions):
            true_val = true_ones[k]

            # Interior positions (middle 80%) have 98.8% accuracy
            # Edge positions (first/last 10%) have 64% accuracy
            edge_threshold = int(0.1 * total_positions)
            is_edge = k < edge_threshold or k >= total_positions - edge_threshold

            if is_edge:
                accuracy = 0.64
            else:
                accuracy = 0.988

            # Simulate prediction
            if random.random() < accuracy:
                pred_val = true_val
                error = 0
            else:
                # Error: usually ±1
                error = random.choice([-1, 1])
                pred_val = max(0, true_val + error)

            errors_by_position[k].append({
                'true': true_val,
                'pred': pred_val,
                'error': error,
                'is_edge': is_edge
            })

    return errors_by_position

def analyze_error_structure(errors_by_position, bits):
    """Analyze where errors cluster and their characteristics"""
    total_positions = 2 * bits - 1

    print(f"--- Error Distribution for {bits}-bit factors ---")
    print()

    # Compute accuracy by position
    print("Position | Type    | Accuracy | Avg Error | Max onesFromPP")
    print("-" * 60)

    interior_correct = 0
    interior_total = 0
    edge_correct = 0
    edge_total = 0

    for k in range(total_positions):
        data = errors_by_position[k]
        correct = sum(1 for d in data if d['error'] == 0)
        total = len(data)
        accuracy = correct / total if total > 0 else 0
        avg_error = sum(abs(d['error']) for d in data) / total if total > 0 else 0
        max_ones = max(d['true'] for d in data)

        is_edge = data[0]['is_edge'] if data else False
        pos_type = "EDGE" if is_edge else "INTERIOR"

        if is_edge:
            edge_correct += correct
            edge_total += total
        else:
            interior_correct += correct
            interior_total += total

        # Only print some positions
        if k < 3 or k >= total_positions - 3 or k == total_positions // 2:
            print(f"  {k:3d}     | {pos_type:7s} | {accuracy:6.1%}   | {avg_error:5.3f}     | {max_ones}")

    print("  ...")
    print()
    print(f"Interior accuracy: {interior_correct}/{interior_total} = {interior_correct/interior_total:.1%}")
    print(f"Edge accuracy:     {edge_correct}/{edge_total} = {edge_correct/edge_total:.1%}")

    return {
        'interior_acc': interior_correct/interior_total,
        'edge_acc': edge_correct/edge_total,
    }

def analyze_error_correlation(errors_by_position, bits):
    """Check if errors are correlated across positions"""
    total_positions = 2 * bits - 1
    samples = len(errors_by_position[0])

    # For each sample, count total errors
    errors_per_sample = []
    for s in range(samples):
        errs = sum(1 for k in range(total_positions) if errors_by_position[k][s]['error'] != 0)
        errors_per_sample.append(errs)

    avg_errors = sum(errors_per_sample) / samples
    max_errors = max(errors_per_sample)
    zero_error_samples = sum(1 for e in errors_per_sample if e == 0)

    print()
    print("Error correlation analysis:")
    print(f"  Avg errors per sample: {avg_errors:.2f} / {total_positions} positions")
    print(f"  Max errors in one sample: {max_errors}")
    print(f"  Samples with zero errors: {zero_error_samples}/{samples} ({100*zero_error_samples/samples:.1f}%)")

    # Distribution of error counts
    from collections import Counter
    dist = Counter(errors_per_sample)
    print(f"  Error count distribution: {dict(sorted(dist.items())[:10])}")

def test_error_analysis():
    print("=" * 60)
    print("Error Distribution Analysis")
    print("=" * 60)
    print()

    for bits in [8, 12, 16]:
        errors = simulate_prediction_errors(bits, samples=500)
        stats = analyze_error_structure(errors, bits)
        analyze_error_correlation(errors, bits)
        print()
        print("=" * 60)
        print()

if __name__ == "__main__":
    test_error_analysis()
