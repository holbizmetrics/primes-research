#!/usr/bin/env python3
"""Search for length-9 gap APs"""
import sys

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def next_prime(n):
    n += 1
    while not is_prime(n):
        n += 1
    return n

print("Searching for length-9 gap APs up to 10M...", flush=True)
p = 5
cnt = 0
checked = 0
while p < 10000000:
    primes = [p]
    for _ in range(8):
        primes.append(next_prime(primes[-1]))
    gaps = [primes[i+1] - primes[i] for i in range(8)]
    d = gaps[1] - gaps[0]
    if all(gaps[i+1] - gaps[i] == d for i in range(7)):
        cnt += 1
        print(f'FOUND {cnt}: p={p} gaps={gaps}', flush=True)
        if cnt >= 5:
            break
    p = next_prime(p)
    checked += 1
    if checked % 50000 == 0:
        print(f"Progress: checked {checked} primes, now at p={p}", flush=True)
print(f'Total found: {cnt}', flush=True)
