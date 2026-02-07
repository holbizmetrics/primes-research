\\ Pure Artin L-function variance test
\\ Goal: Test if Var decreases with dimension

svar(z) = {
  my(s, m, n);
  if(#z < 5, return(-1));
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  n = vector(#s, i, s[i]/m);
  vecsum(vector(#n, i, (n[i]-1)^2)) / #n
}

print("=== Pure Artin L-function Variance ===");
print("");

\\ Riemann zeta (dim 1)
print("1. Riemann zeta (dim 1):");
z1 = lfunzeros(lfuncreate(1), 200);
print("   Zeros: ", #z1, ", Var: ", svar(z1));

\\ S3 splitting field - extract dim-2 Artin component
print("2. S3 dim-2 Artin via Dedekind/zeta quotient:");
K3 = nfinit(x^3 - 2);
L3 = lfuncreate(K3);
z_ded = lfunzeros(L3, 200);
print("   Dedekind zeros: ", #z_ded, ", Var: ", svar(z_ded));

\\ For the actual pure Artin, we need the splitting field
\\ Q(cbrt(2), omega) where omega = exp(2*pi*i/3)
print("3. Full S3 splitting field (degree 6):");
K6 = nfinit(x^6 + 3*x^5 + 6*x^4 + 3*x^3 + 9*x + 9);
L6 = lfuncreate(K6);
z6 = lfunzeros(L6, 100);
print("   Zeros: ", #z6, ", Var: ", svar(z6));

\\ A4 extension
print("4. A4 extension (has dim-3 irrep):");
KA4 = nfinit(x^4 + 8*x + 12);
LA4 = lfuncreate(KA4);
zA4 = lfunzeros(LA4, 100);
print("   Zeros: ", #zA4, ", Var: ", svar(zA4));

\\ S4 extension
print("5. S4 extension (has dim-3 irrep):");
KS4 = nfinit(x^4 - x - 1);
LS4 = lfuncreate(KS4);
zS4 = lfunzeros(LS4, 100);
print("   Zeros: ", #zS4, ", Var: ", svar(zS4));

print("");
print("Note: To isolate pure Artin, need Artin representations directly.");
print("The above uses Dedekind zetas which mix factors.");
