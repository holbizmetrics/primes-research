#!/usr/bin/env python3
"""
Brennpunkt Stability Test
Check if t=1/4 (primes) and t=1/3 (composites) are N-independent

2026-02-06
"""

import math

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi / (PHI * PHI)

def sieve_primes(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return [i for i in range(n + 1) if sieve[i]]

def compute_spread(numbers, N, t, R=0.5):
    """Compute spread (variance of focused radii) for given t"""
    focused_radii = []
    for n in numbers:
        r_orig = n / N
        r_focused = (r_orig ** (1 - 2*t)) * (R ** (2*t))
        focused_radii.append(r_focused)
    
    if len(focused_radii) < 2:
        return float('inf')
    
    mean = sum(focused_radii) / len(focused_radii)
    variance = sum((r - mean)**2 for r in focused_radii) / len(focused_radii)
    return variance

def find_optimal_t(numbers, N, t_min=0.0, t_max=0.5, steps=100):
    """Find t that minimizes spread"""
    best_t = 0
    best_spread = float('inf')
    
    for i in range(steps + 1):
        t = t_min + (t_max - t_min) * i / steps
        spread = compute_spread(numbers, N, t)
        if spread < best_spread:
            best_spread = spread
            best_t = t
    
    return best_t, best_spread

def main():
    print("=" * 60)
    print("BRENNPUNKT STABILITY TEST")
    print("=" * 60)
    print()
    print("Testing if optimal t is N-independent...")
    print()
    
    print(f"{'N':>6} {'Prime t':>10} {'Comp t':>10} {'1/Prime':>10} {'1/Comp':>10}")
    print("-" * 60)
    
    prime_ts = []
    comp_ts = []
    
    for N in [100, 200, 500, 1000, 2000, 5000]:
        primes = sieve_primes(N)
        composites = [n for n in range(4, N+1) if n not in set(primes) and n > 1]
        
        t_prime, _ = find_optimal_t(primes, N, steps=200)
        t_comp, _ = find_optimal_t(composites, N, steps=200)
        
        prime_ts.append(t_prime)
        comp_ts.append(t_comp)
        
        inv_prime = 1/t_prime if t_prime > 0 else 0
        inv_comp = 1/t_comp if t_comp > 0 else 0
        
        print(f"{N:>6} {t_prime:>10.4f} {t_comp:>10.4f} {inv_prime:>10.2f} {inv_comp:>10.2f}")
    
    print()
    print("=" * 60)
    print("ANALYSIS")
    print("=" * 60)
    
    mean_prime_t = sum(prime_ts) / len(prime_ts)
    mean_comp_t = sum(comp_ts) / len(comp_ts)
    
    std_prime = (sum((t - mean_prime_t)**2 for t in prime_ts) / len(prime_ts)) ** 0.5
    std_comp = (sum((t - mean_comp_t)**2 for t in comp_ts) / len(comp_ts)) ** 0.5
    
    print(f"\nPrime Brennpunkt:")
    print(f"  Mean t = {mean_prime_t:.4f} (theory: 0.2500 = 1/4)")
    print(f"  Std dev = {std_prime:.4f}")
    print(f"  1/t = {1/mean_prime_t:.2f} (theory: 4)")
    
    print(f"\nComposite Brennpunkt:")
    print(f"  Mean t = {mean_comp_t:.4f} (theory: 0.3333 = 1/3)")
    print(f"  Std dev = {std_comp:.4f}")
    print(f"  1/t = {1/mean_comp_t:.2f} (theory: 3)")
    
    print(f"\nConclusion:")
    if std_prime < 0.02 and std_comp < 0.02:
        print("  ✓ Brennpunkt is N-INDEPENDENT (stable across N)")
    else:
        print("  ? Brennpunkt shows N-dependence (needs investigation)")
    
    print()

if __name__ == "__main__":
    main()
