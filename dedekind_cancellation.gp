\\ Dedekind Cancellation Test
\\ Prediction: C(Dedekind) > C(Zeta) because merging weakens selection

\\ Compute cancellation ratio for a set of zeros
\\ C(N) = Var(actual) / Var(null) where null = independent phases

cancellation_ratio(zeros, N) = {
  my(n, E_vals, x_vals, var_actual, var_null, diag);

  n = #zeros;
  if(n < 5, return(-1));

  \\ Sample E(x) at log-spaced points
  x_vals = vector(100, i, exp(log(2) + (i-1)*(log(N)-log(2))/99));

  \\ Compute E(x) = sum of zero contributions
  E_vals = vector(100, i,
    my(x = x_vals[i], s = 0.0);
    for(j = 1, min(n, 50),  \\ use first 50 zeros
      my(g = zeros[j]);
      s += -2 * sqrt(x) / sqrt(0.25 + g^2) * cos(g * log(x) - atan(2*g));
    );
    s
  );

  \\ Actual variance
  my(mean_E = vecsum(E_vals) / 100);
  var_actual = vecsum(vector(100, i, (E_vals[i] - mean_E)^2)) / 100;

  \\ Null variance (diagonal only, independent phases)
  diag = 0.0;
  for(j = 1, min(n, 50),
    my(g = zeros[j]);
    diag += N / (0.25 + g^2);  \\ ~ integral of |f_gamma|^2
  );
  var_null = diag / 100;  \\ normalized

  \\ Cancellation ratio
  if(var_null > 0, var_actual / var_null, -1)
}

\\ Main test
print("=== Dedekind Cancellation Test ===");
print("Prediction: C(Dedekind) > C(Zeta)");
print("");

\\ Riemann zeta zeros
print("Computing Riemann zeta zeros...");
z_zeta = lfunzeros(lfuncreate(1), 100);
print("  Found ", #z_zeta, " zeros up to T=100");

\\ Q(cbrt(2)) Dedekind zeta zeros
print("Computing Dedekind zeta zeros for Q(cbrt(2))...");
K = nfinit(x^3 - 2);
L_K = lfuncreate(K);
z_ded = lfunzeros(L_K, 100);
print("  Found ", #z_ded, " zeros up to T=100");

\\ Compute cancellation at various N
print("");
print("Cancellation ratios (lower = better cancellation):");
print("N\t\tC(zeta)\t\tC(Dedekind)\tRatio");
print("-" * 60);

for(logN = 3, 6,
  my(N = 10^logN);
  my(C_z = cancellation_ratio(z_zeta, N));
  my(C_d = cancellation_ratio(z_ded, N));
  if(C_z > 0 && C_d > 0,
    printf("10^%d\t\t%.4f\t\t%.4f\t\t%.3f\n", logN, C_z, C_d, C_d/C_z);
  );
);

print("");
print("If Ratio > 1, Dedekind has WORSE cancellation (confirms prediction)");
print("If Ratio < 1, Dedekind has BETTER cancellation (contradicts prediction)");
