from mpmath import zetazero

def variance(zeros):
    n = len(zeros)
    spacings = [zeros[i+1] - zeros[i] for i in range(n-1)]
    mean_s = sum(spacings) / len(spacings)
    norm_s = [s / mean_s for s in spacings]
    return sum((s - 1)**2 for s in norm_s) / len(norm_s)

# Compute zeros once, then slice
print("Computing 300 zeta zeros...")
zeros = [float(zetazero(i).imag) for i in range(1, 301)]

for n_zeros in [50, 100, 150, 200, 250, 300]:
    z = zeros[:n_zeros]
    v = variance(z)
    print(f"n={n_zeros}, T≈{z[-1]:.0f}, var={v:.4f}")
