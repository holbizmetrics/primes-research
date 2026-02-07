#!/usr/bin/env python3
"""STRIKE 30-31: Why odd k gives residual ~0.7 (rotation HURTS).

For k-bit prime p: rotate(p,1,k) = 2(p - 2^{k-1}) + 1 = 2p - 2^k + 1.

For even k: 2^k ≡ 0 mod 4, so 2p - 2^k + 1 ≡ 2p + 1 mod 4.
  If p ≡ 1 mod 4: rotated ≡ 3 mod 4.
  If p ≡ 3 mod 4: rotated ≡ 3 mod 4. Wait: 2*3 + 1 = 7 ≡ 3 mod 4. Hmm.
  Actually 2p + 1 mod 4: p odd, so p=2j+1, 2p+1=4j+3 ≡ 3 mod 4. Always!

For odd k: 2^k ≡ 2 mod 4 (since k odd means 2^k = 2 * 2^{k-1}, k-1 even).
  Wait: 2^k for any k >= 2 is ≡ 0 mod 4. Let me reconsider.
  2^k ≡ 0 mod 4 for k >= 2. So 2p - 2^k + 1 ≡ 2p + 1 mod 4 regardless of k.
  Both even and odd k give same mod 4 residue!

So the difference isn't mod 4. Let me check mod 3 and mod other smalls.
"""
import math

def sieve(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return s

N=131072; is_p=sieve(N)

def bit_rotate(n, d, w):
    d = d % w
    return ((n << d) | (n >> (w - d))) & ((1 << w) - 1)

# STRIKE 30: Distribution of rotated values in number line
# For k-bit prime p, r = rotate(p,1,k) = 2p mod (2^k-1).
# Where does r fall within [2^{k-1}, 2^k-1]?
print("=== STRIKE 30: Where do rotated values land? ===")
print()

for k in [11, 12, 13, 14]:
    lo = 1<<(k-1); hi = (1<<k)-1
    Mk = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    rotated_in_range = []
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi:
            rotated_in_range.append(r)

    if not rotated_in_range: continue

    # Split range into quartiles and check prime density in each
    range_size = hi - lo
    q_size = range_size // 4

    print("k=%d (%s):" % (k, "even" if k%2==0 else "ODD"))
    for q in range(4):
        q_lo = lo + q * q_size
        q_hi = lo + (q+1) * q_size if q < 3 else hi
        in_q = [r for r in rotated_in_range if q_lo <= r <= q_hi]
        primes_in_q = sum(1 for r in in_q if is_p[r])
        n_in_q = len(in_q)
        # Actual prime density in this quartile
        all_primes_q = sum(1 for n in range(q_lo, q_hi+1) if is_p[n])
        actual_density = all_primes_q / (q_hi - q_lo + 1)
        rot_rate = primes_in_q / n_in_q if n_in_q else 0
        print("  Q%d [%d-%d]: %d rotated, %d prime (rate=%.3f), local density=%.3f, ratio=%.3f" % (
            q, q_lo, q_hi, n_in_q, primes_in_q, rot_rate, actual_density,
            rot_rate / actual_density if actual_density else 0))
    print()

# STRIKE 31: The key — for ODD k, is the map p -> 2p mod M_k biased
# toward regions where primes are sparser?
# Check: mod 6 residue of rotated value
print("=== STRIKE 31: Mod-6 residue of rotated values ===")
print("Primes > 3 are ≡ 1 or 5 mod 6")
print()

for k in range(9, 18):
    lo = 1<<(k-1); hi = (1<<k)-1
    if hi > N: break
    Mk = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    rotated = []
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi:
            rotated.append(r)

    if not rotated: continue

    mod6 = [0]*6
    for r in rotated:
        mod6[r % 6] += 1

    total = len(rotated)
    # Primes must be ≡ 1 or 5 mod 6. What fraction of rotated values are?
    prime_eligible = mod6[1] + mod6[5]
    print("k=%2d (%s): rotated mod 6: %s  eligible=%.1f%%" % (
        k, "even" if k%2==0 else "ODD",
        " ".join("%d:%.0f%%" % (i, 100*mod6[i]/total) for i in range(6)),
        100*prime_eligible/total))

print()

# STRIKE 31b: The analytic answer
# rotate(p,1,k) = 2p - M_k when p >= M_k/2 (which is always true for k-bit p).
# So r = 2p - (2^k - 1).
# r mod 3: 2p mod 3 - (2^k - 1) mod 3.
# For even k: 2^k ≡ 1 mod 3, so M_k = 2^k-1 ≡ 0 mod 3.
#   r mod 3 = 2p mod 3. Since p ≢ 0 mod 3, 2p ≢ 0 mod 3. Good!
# For odd k: 2^k ≡ 2 mod 3, so M_k = 2^k-1 ≡ 1 mod 3.
#   r mod 3 = (2p - 1) mod 3. If p ≡ 1 mod 3: r ≡ 1 mod 3. OK.
#   If p ≡ 2 mod 3: r ≡ 0 mod 3! DIVISIBLE BY 3!

print("=== ANALYTIC EXPLANATION ===")
print()
print("For even k: M_k ≡ 0 mod 3, so rotation preserves coprimality to 3.")
print("For odd k: M_k ≡ 1 mod 3.")
print("  If p ≡ 2 mod 3: rotated ≡ (2*2 - 1) ≡ 0 mod 3. DIVISIBLE BY 3!")
print("  Half of primes have p ≡ 2 mod 3, and their rotation is div by 3.")
print("  These can NEVER be prime (unless = 3 itself).")
print()

# Verify
print("Verification:")
for k in [9, 11, 13, 15, 17]:
    lo = 1<<(k-1); hi = (1<<k)-1
    if hi > N: break
    Mk = (1<<k)-1
    prm = [p for p in range(lo, hi+1) if is_p[p]]

    rot_div3 = 0; p_mod3_2 = 0
    for p in prm:
        r = bit_rotate(p, 1, k)
        if lo <= r <= hi:
            if r % 3 == 0:
                rot_div3 += 1
            if p % 3 == 2:
                p_mod3_2 += 1

    in_range = sum(1 for p in prm if lo <= bit_rotate(p,1,k) <= hi)
    print("  k=%2d: primes≡2 mod 3: %d/%d (%.1f%%), rotated div by 3: %d/%d (%.1f%%)" % (
        k, p_mod3_2, len(prm), 100*p_mod3_2/len(prm),
        rot_div3, in_range, 100*rot_div3/in_range if in_range else 0))

print()
print("For odd k: ~50% of in-range rotated values are div by 3 -> can't be prime.")
print("This explains the ~0.7 residual: half the candidates are killed by 3.")
print("Expected residual for odd k ≈ 0.5 * sieve + 0.5 * enhanced_sieve...")
print("More precisely: the sieve prediction overcounts by including the 3-factor")
print("which only works for even k.")
