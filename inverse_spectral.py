"""
Inverse Spectral Learning: Cancellation Functional C(N)

Computes C(N) = Var_actual[E(x)] / Var_null[E(x)]
where E(x) = ψ(x) - x is the error in the prime counting function.

The null model uses phase-randomized zeros to break correlations
while preserving density.
"""

import numpy as np
from mpmath import mp, zetazero, log, exp, pi
import matplotlib.pyplot as plt
from typing import List, Tuple
import time

# Set precision
mp.dps = 30

class InverseSpectral:
    """Compute cancellation functional for inverse spectral analysis."""

    def __init__(self, num_zeros: int = 1000):
        """Initialize with specified number of zeta zeros."""
        self.num_zeros = num_zeros
        self.zeros = None  # Will hold imaginary parts γ
        self.load_zeros()

    def load_zeros(self):
        """Load/compute the first num_zeros non-trivial zeros of zeta."""
        print(f"Computing {self.num_zeros} zeta zeros...")
        start = time.time()

        # Get imaginary parts of zeros (ρ = 1/2 + iγ)
        self.zeros = []
        for n in range(1, self.num_zeros + 1):
            zero = zetazero(n)
            gamma = float(zero.imag)
            self.zeros.append(gamma)
            if n % 100 == 0:
                print(f"  Computed {n} zeros...")

        self.zeros = np.array(self.zeros)
        elapsed = time.time() - start
        print(f"Done. Computed {len(self.zeros)} zeros in {elapsed:.1f}s")
        print(f"First few γ values: {self.zeros[:5]}")
        print(f"Last few γ values: {self.zeros[-5:]}")

    def E_actual(self, x: float) -> float:
        """
        Compute E(x) = -Σ_ρ (x^ρ / ρ) using actual zeros.

        Each term: x^(1/2 + iγ) / (1/2 + iγ)
                 = x^(1/2) * e^(iγ log x) / (1/2 + iγ)

        We take the real part since E(x) is real.
        """
        sqrt_x = np.sqrt(x)
        log_x = np.log(x)

        total = 0.0
        for gamma in self.zeros:
            # Phase: e^(iγ log x)
            phase = np.exp(1j * gamma * log_x)
            # Denominator: 1/2 + iγ
            denom = 0.5 + 1j * gamma
            # Term contribution
            term = sqrt_x * phase / denom
            total += term

        # E(x) = -Σ (real part, doubled for conjugate pairs)
        # Since zeros come in conjugate pairs ρ, ρ̄, we double the real part
        return -2.0 * total.real

    def E_null(self, x: float, random_phases: np.ndarray) -> float:
        """
        Compute E(x) with randomized phases (null model).

        Same amplitude structure, but phases are randomized to break correlations.
        """
        sqrt_x = np.sqrt(x)
        log_x = np.log(x)

        total = 0.0
        for i, gamma in enumerate(self.zeros):
            # Randomized phase
            phase = np.exp(1j * (gamma * log_x + random_phases[i]))
            denom = 0.5 + 1j * gamma
            term = sqrt_x * phase / denom
            total += term

        return -2.0 * total.real

    def compute_variance(self, x_values: np.ndarray, null: bool = False,
                         random_phases: np.ndarray = None) -> float:
        """Compute variance of E(x) over given x values."""
        if null:
            E_values = np.array([self.E_null(x, random_phases) for x in x_values])
        else:
            E_values = np.array([self.E_actual(x) for x in x_values])

        return np.var(E_values)

    def C(self, N: int, num_samples: int = 500, num_null_trials: int = 20) -> Tuple[float, dict]:
        """
        Compute the cancellation functional C(N).

        C(N) = Var_actual[E(x)] / E[Var_null[E(x)]]

        where the null expectation is over random phase realizations.

        Returns C(N) and diagnostic info.
        """
        # Sample x values in [2, N] (log-spaced for better coverage)
        x_values = np.logspace(np.log10(2), np.log10(N), num_samples)

        # Compute actual variance
        print(f"Computing actual E(x) for {num_samples} points in [2, {N}]...")
        E_actual_values = np.array([self.E_actual(x) for x in x_values])
        var_actual = np.var(E_actual_values)

        # Compute null variance (average over multiple realizations)
        print(f"Computing null variance ({num_null_trials} trials)...")
        null_variances = []
        for trial in range(num_null_trials):
            random_phases = np.random.uniform(0, 2*np.pi, len(self.zeros))
            E_null_values = np.array([self.E_null(x, random_phases) for x in x_values])
            null_variances.append(np.var(E_null_values))

        var_null = np.mean(null_variances)
        var_null_std = np.std(null_variances)

        C_N = var_actual / var_null

        diagnostics = {
            'N': N,
            'var_actual': var_actual,
            'var_null_mean': var_null,
            'var_null_std': var_null_std,
            'C_N': C_N,
            'E_actual_values': E_actual_values,
            'x_values': x_values,
            'num_zeros': len(self.zeros)
        }

        return C_N, diagnostics

    def compute_C_scaling(self, N_values: List[int], **kwargs) -> dict:
        """Compute C(N) for multiple N values to observe scaling."""
        results = {
            'N': [],
            'C_N': [],
            'var_actual': [],
            'var_null': [],
            'diagnostics': []
        }

        for N in N_values:
            print(f"\n{'='*50}")
            print(f"Computing C({N})...")
            C_N, diag = self.C(N, **kwargs)

            results['N'].append(N)
            results['C_N'].append(C_N)
            results['var_actual'].append(diag['var_actual'])
            results['var_null'].append(diag['var_null_mean'])
            results['diagnostics'].append(diag)

            print(f"C({N}) = {C_N:.6f}")
            print(f"  Var_actual = {diag['var_actual']:.2f}")
            print(f"  Var_null   = {diag['var_null_mean']:.2f} ± {diag['var_null_std']:.2f}")

        return results

    def plot_results(self, results: dict, save_path: str = None):
        """Plot C(N) scaling and E(x) behavior."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # Plot 1: C(N) vs N
        ax1 = axes[0, 0]
        ax1.semilogx(results['N'], results['C_N'], 'bo-', markersize=8, linewidth=2)
        ax1.axhline(y=1.0, color='r', linestyle='--', label='Random baseline')
        ax1.set_xlabel('N')
        ax1.set_ylabel('C(N)')
        ax1.set_title('Cancellation Functional C(N) = Var_actual / Var_null')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Variances vs N
        ax2 = axes[0, 1]
        ax2.loglog(results['N'], results['var_actual'], 'g^-', label='Var_actual', markersize=8)
        ax2.loglog(results['N'], results['var_null'], 'rs-', label='Var_null', markersize=8)
        ax2.set_xlabel('N')
        ax2.set_ylabel('Variance')
        ax2.set_title('Variance Scaling')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Plot 3: E(x) for largest N
        ax3 = axes[1, 0]
        last_diag = results['diagnostics'][-1]
        x_vals = last_diag['x_values']
        E_vals = last_diag['E_actual_values']
        ax3.plot(x_vals, E_vals, 'b-', alpha=0.7, linewidth=0.5)
        ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax3.set_xlabel('x')
        ax3.set_ylabel('E(x) = ψ(x) - x')
        ax3.set_title(f'Error Term E(x) up to N={last_diag["N"]}')
        ax3.grid(True, alpha=0.3)

        # Plot 4: E(x) normalized by √x
        ax4 = axes[1, 1]
        E_normalized = E_vals / np.sqrt(x_vals)
        ax4.semilogx(x_vals, E_normalized, 'b-', alpha=0.7, linewidth=0.5)
        ax4.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax4.set_xlabel('x')
        ax4.set_ylabel('E(x) / √x')
        ax4.set_title('Normalized Error (should stay bounded if RH true)')
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Saved plot to {save_path}")

        plt.show()
        return fig


def spectral_decomposition_analysis(zeros: np.ndarray) -> dict:
    """
    Analyze spectral structure of zeros for decomposition.

    The variance of E(x) can be decomposed:
    Var[E] = Σ_j Σ_k Cov[term_j, term_k]
           = Σ_j Var[term_j] + 2 Σ_{j<k} Cov[term_j, term_k]

    The off-diagonal covariances encode the correlations.
    """
    n = len(zeros)

    # Compute nearest-neighbor spacings (normalized)
    spacings = np.diff(zeros)
    mean_spacing = np.mean(spacings)
    normalized_spacings = spacings / mean_spacing

    # GUE prediction: spacing distribution ~ (π/2)s exp(-πs²/4)
    # Poisson prediction: spacing distribution ~ exp(-s)

    # Compute pair correlation proxy
    # R_2(r) measures probability of finding zeros at distance r

    results = {
        'num_zeros': n,
        'gamma_range': (zeros[0], zeros[-1]),
        'mean_spacing': mean_spacing,
        'spacing_variance': np.var(normalized_spacings),
        'normalized_spacings': normalized_spacings,
    }

    # For GUE, Var(spacing) ≈ 0.178
    # For Poisson, Var(spacing) = 1
    print("\n" + "="*50)
    print("SPECTRAL DECOMPOSITION ANALYSIS")
    print("="*50)
    print(f"Number of zeros: {n}")
    print(f"γ range: [{zeros[0]:.2f}, {zeros[-1]:.2f}]")
    print(f"Mean spacing: {mean_spacing:.4f}")
    print(f"Normalized spacing variance: {results['spacing_variance']:.4f}")
    print(f"  (GUE prediction: ~0.178, Poisson: 1.0)")

    if results['spacing_variance'] < 0.3:
        print("  → Spacings are GUE-like (strong repulsion)")
    elif results['spacing_variance'] < 0.6:
        print("  → Spacings show intermediate correlations")
    else:
        print("  → Spacings are Poisson-like (weak correlations)")

    return results


def main():
    """Run the inverse spectral analysis."""
    print("="*60)
    print("INVERSE SPECTRAL LEARNING: CANCELLATION FUNCTIONAL")
    print("="*60)

    # Initialize with zeros
    # Start with fewer zeros for speed, can increase later
    analyzer = InverseSpectral(num_zeros=500)

    # Analyze spectral structure
    spectral_info = spectral_decomposition_analysis(analyzer.zeros)

    # Compute C(N) for increasing N
    N_values = [100, 500, 1000, 5000, 10000]

    print("\n" + "="*60)
    print("COMPUTING CANCELLATION FUNCTIONAL C(N)")
    print("="*60)

    results = analyzer.compute_C_scaling(
        N_values,
        num_samples=300,
        num_null_trials=15
    )

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"{'N':>10} {'C(N)':>12} {'Var_actual':>14} {'Var_null':>14}")
    print("-" * 54)
    for i, N in enumerate(results['N']):
        print(f"{N:>10} {results['C_N'][i]:>12.6f} {results['var_actual'][i]:>14.2f} {results['var_null'][i]:>14.2f}")

    # Interpretation
    print("\n" + "="*60)
    print("INTERPRETATION")
    print("="*60)

    C_values = np.array(results['C_N'])
    if np.all(C_values < 1):
        print("✓ C(N) < 1 for all N tested")
        print("  → Actual zeros cancel MORE efficiently than random")
        print("  → This constrains possible operator classes")

    if np.std(C_values) < 0.1:
        print("✓ C(N) is relatively stable")
        print("  → Cancellation efficiency is scale-invariant")

    # Check if C(N) is decreasing
    if len(C_values) > 2:
        slope = np.polyfit(np.log(results['N']), C_values, 1)[0]
        if slope < 0:
            print(f"✓ C(N) decreasing with N (slope ≈ {slope:.4f} in log scale)")
            print("  → Cancellation strengthens at larger scales")

    # Plot
    analyzer.plot_results(results, save_path='inverse_spectral_results.png')

    return analyzer, results, spectral_info


if __name__ == "__main__":
    analyzer, results, spectral_info = main()
