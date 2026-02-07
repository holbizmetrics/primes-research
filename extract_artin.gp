\\ Extract pure Artin zeros via Dedekind/zeta quotient
\\ For S3: ζ_K = ζ × L(ρ₂), so L(ρ₂) zeros = ζ_K zeros - ζ zeros

svar(z) = {
  my(s, m, n);
  if(#z < 5, return(-1));
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  n = vector(#s, i, s[i]/m);
  vecsum(vector(#n, i, (n[i]-1)^2)) / #n
}

\\ Get zeros
print("Computing zeros...");
z_zeta = lfunzeros(lfuncreate(1), 100);
K = nfinit(x^3 - 2);
z_ded = lfunzeros(lfuncreate(K), 100);

print("Zeta zeros: ", #z_zeta);
print("Dedekind zeros: ", #z_ded);

\\ Extract Artin zeros by removing zeta zeros from Dedekind
\\ A zero γ is a zeta zero if there exists a zeta zero within 0.01
tol = 0.01;
z_artin = [];
for(i = 1, #z_ded,
  g = z_ded[i];
  is_zeta = 0;
  for(j = 1, #z_zeta,
    if(abs(g - z_zeta[j]) < tol, is_zeta = 1; break);
  );
  if(!is_zeta, z_artin = concat(z_artin, [g]));
);
z_artin = Vec(z_artin);

print("Pure Artin zeros (after removing zeta): ", #z_artin);
print("");
print("=== Variance Results ===");
print("Riemann zeta: ", svar(z_zeta));
print("Dedekind S3: ", svar(z_ded));
print("Pure Artin dim-2: ", svar(z_artin));
