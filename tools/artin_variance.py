#!/usr/bin/env python3
"""
Compute spacing variance for higher-dimensional Artin L-functions.
Uses LMFDB API to fetch zeros.
"""

import urllib.request
import json
import math

def fetch_lmfdb_zeros(label, limit=500):
    """Fetch zeros from LMFDB API."""
    url = f"https://www.lmfdb.org/api/lfunc_zeros/?label={label}&_format=json&_limit={limit}"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            if data and 'data' in data:
                # Extract imaginary parts of zeros
                zeros = []
                for record in data['data']:
                    if 'zeros' in record:
                        zeros.extend(record['zeros'])
                return sorted(zeros)
    except Exception as e:
        print(f"Error fetching {label}: {e}")
    return None

def fetch_artin_zeros(dim, limit=200):
    """Fetch zeros of Artin L-functions of given dimension from LMFDB."""
    # LMFDB Artin rep labels by dimension
    # Format: conductor.galois_label.rep_label

    # Some known Artin L-function labels by dimension:
    artin_labels = {
        2: [
            "2.2.3.1",      # S3, 2-dim
            "2.2.4.1",      # D4, 2-dim
            "2.2.5.1",      # D5, 2-dim
        ],
        3: [
            "3.3.4.1",      # S4, 3-dim standard rep
            "3.3.5.1",      # A5, 3-dim
        ],
        4: [
            "4.4.5.1",      # S5/A5, 4-dim
        ]
    }

    if dim not in artin_labels:
        return None

    for label in artin_labels[dim]:
        zeros = fetch_lmfdb_zeros(f"ArtinRepresentation/{label}")
        if zeros and len(zeros) >= 50:
            return zeros, label

    return None, None

def compute_spacings(zeros):
    """Compute normalized nearest-neighbor spacings."""
    if len(zeros) < 10:
        return []

    # Compute raw spacings
    spacings = [zeros[i+1] - zeros[i] for i in range(len(zeros)-1)]

    # Normalize to mean 1
    mean_spacing = sum(spacings) / len(spacings)
    if mean_spacing <= 0:
        return []

    normalized = [s / mean_spacing for s in spacings]
    return normalized

def variance(data):
    """Compute variance."""
    if len(data) < 2:
        return 0
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean)**2 for x in data) / (n - 1)

def skewness(data):
    """Compute skewness."""
    if len(data) < 3:
        return 0
    n = len(data)
    mean = sum(data) / n
    var = sum((x - mean)**2 for x in data) / n
    if var <= 0:
        return 0
    std = math.sqrt(var)
    return sum((x - mean)**3 for x in data) / (n * std**3)

# Alternative: Use explicit formulas to compute zeros numerically
# For now, let's try the LMFDB route

def main():
    print("Testing Artin L-function spacing variance by dimension")
    print("=" * 60)
    print()
    print("Prediction: Var(dim-d) ≈ 0.27 / d²")
    print()
    print("| Dim | Predicted | Label | N zeros | Observed Var | Skewness |")
    print("|-----|-----------|-------|---------|--------------|----------|")

    for dim in [2, 3, 4]:
        predicted = 0.27 / (dim ** 2)

        # Try fetching from LMFDB
        zeros, label = fetch_artin_zeros(dim)

        if zeros and len(zeros) >= 20:
            spacings = compute_spacings(zeros)
            if spacings:
                var = variance(spacings)
                skew = skewness(spacings)
                print(f"| {dim}   | {predicted:.3f}     | {label} | {len(zeros):>7} | {var:.3f}        | {skew:.3f}    |")
            else:
                print(f"| {dim}   | {predicted:.3f}     | {label} | {len(zeros):>7} | (bad data)     |          |")
        else:
            print(f"| {dim}   | {predicted:.3f}     | (no data) |       - | -              | -        |")

if __name__ == "__main__":
    main()
