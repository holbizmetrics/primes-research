#!/usr/bin/env python3
"""
Ramanujan Sum Bridge - Validation Script
Tests the formula: Prime coherence = μ(λ)² / φ(λ)² for squarefree λ

2026-02-06
"""

import math
from functools import lru_cache

def sieve_primes(n):
    """Generate primes up to n"""
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return [i for i in range(n + 1) if sieve[i]]

@lru_cache(maxsize=1000)
def mobius(n):
    """Möbius function μ(n)"""
    if n == 1:
        return 1
    factors = []
    temp = n
    for p in range(2, int(n**0.5) + 1):
        if temp % p == 0:
            count = 0
            while temp % p == 0:
                temp //= p
                count += 1
            if count > 1:
                return 0  # not squarefree
            factors.append(p)
    if temp > 1:
        factors.append(temp)
    return (-1) ** len(factors)

@lru_cache(maxsize=1000)
def euler_totient(n):
    """Euler's totient function φ(n)"""
    result = n
    temp = n
    for p in range(2, int(n**0.5) + 1):
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
    if temp > 1:
        result -= result // temp
    return result

def theoretical_coherence(lam):
    """Ramanujan formula: μ(λ)² / φ(λ)²"""
    mu = mobius(lam)
    if mu == 0:
        return 0.0
    phi = euler_totient(lam)
    return (mu * mu) / (phi * phi)

def measured_coherence(primes, lam):
    """Measure actual prime coherence at wavelength λ"""
    ar, ai = 0.0, 0.0
    count = 0
    for p in primes:
        phase = 2 * math.pi * p / lam
        ar += math.cos(phase)
        ai += math.sin(phase)
        count += 1
    if count == 0:
        return 0.0
    # Coherence = |amplitude|² / N²
    return (ar*ar + ai*ai) / (count * count)

def main():
    print("=" * 60)
    print("RAMANUJAN SUM BRIDGE - Validation")
    print("=" * 60)
    print()
    
    N = 1000
    primes = sieve_primes(N)
    print(f"Testing with {len(primes)} primes up to {N}")
    print()
    
    print(f"{'λ':>4} {'μ(λ)':>5} {'φ(λ)':>5} {'Sqfree':>7} {'Theory':>10} {'Measured':>10} {'Ratio':>8}")
    print("-" * 60)
    
    results = []
    for lam in range(2, 31):
        mu = mobius(lam)
        phi = euler_totient(lam)
        sqfree = "YES" if mu != 0 else "no"
        theory = theoretical_coherence(lam)
        measured = measured_coherence(primes, lam)
        
        if theory > 0:
            ratio = measured / theory
        else:
            ratio = float('inf') if measured > 0 else 0
        
        results.append((lam, mu, phi, sqfree, theory, measured, ratio))
        
        print(f"{lam:>4} {mu:>5} {phi:>5} {sqfree:>7} {theory:>10.6f} {measured:>10.6f} {ratio:>8.3f}")
    
    print()
    print("=" * 60)
    print("ANALYSIS")
    print("=" * 60)
    
    # Check squarefree vs non-squarefree
    sqfree_measured = [r[5] for r in results if r[3] == "YES"]
    nonsqfree_measured = [r[5] for r in results if r[3] == "no"]
    
    print(f"\nSquarefree λ (primes GLOW):")
    print(f"  Mean coherence: {sum(sqfree_measured)/len(sqfree_measured):.6f}")
    print(f"  Max coherence: {max(sqfree_measured):.6f}")
    
    print(f"\nNon-squarefree λ (primes DARK):")
    print(f"  Mean coherence: {sum(nonsqfree_measured)/len(nonsqfree_measured):.6f}")
    print(f"  Max coherence: {max(nonsqfree_measured):.6f}")
    
    print(f"\nGlow/Dark ratio: {sum(sqfree_measured)/len(sqfree_measured) / (sum(nonsqfree_measured)/len(nonsqfree_measured) + 1e-10):.2f}×")
    
    # Theory vs measured correlation for squarefree
    sqfree_theory = [r[4] for r in results if r[3] == "YES"]
    sqfree_ratios = [r[6] for r in results if r[3] == "YES" and r[4] > 0]
    
    print(f"\nTheory/Measured correlation (squarefree only):")
    print(f"  Mean ratio: {sum(sqfree_ratios)/len(sqfree_ratios):.3f}")
    print(f"  Std dev: {(sum((r - sum(sqfree_ratios)/len(sqfree_ratios))**2 for r in sqfree_ratios)/len(sqfree_ratios))**0.5:.3f}")
    
    print()
    print("KEY FINDING:")
    print("  μ(λ) = 0 → primes go DARK (near-zero coherence)")
    print("  μ(λ) ≠ 0 → primes GLOW (positive coherence)")
    print("  This is the RAMANUJAN SUM CONNECTION.")
    print()

if __name__ == "__main__":
    main()
