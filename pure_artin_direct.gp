\\ Direct Pure Artin L-function computation
\\ Using lfunartin() for actual Artin representations

default(parisizemax, 500000000);
default(parisize, 100000000);

svar(z) = {
  my(s, m, n);
  if(#z < 5, return(-1));
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  n = vector(#s, i, s[i]/m);
  vecsum(vector(#n, i, (n[i]-1)^2)) / #n
}

print("=== Pure Artin L-function Direct Test ===");
print("");

\\ Method: Use galoisinit and extract irreducible representations
\\ Then create L-functions via lfunartin

\\ 1. Riemann zeta baseline
print("1. Riemann zeta (trivial rep, dim 1):");
z1 = lfunzeros(lfuncreate(1), 100);
print("   Zeros: ", #z1, ", Var: ", svar(z1));

\\ 2. Dirichlet L-function (dim 1, but nontrivial)
print("2. L(s, chi_3) (Dirichlet mod 3, dim 1):");
z_d3 = lfunzeros(lfuncreate([3, [1]]), 100);
print("   Zeros: ", #z_d3, ", Var: ", svar(z_d3));

print("3. L(s, chi_4) (Dirichlet mod 4, dim 1):");
z_d4 = lfunzeros(lfuncreate([4, [1]]), 100);
print("   Zeros: ", #z_d4, ", Var: ", svar(z_d4));

print("4. L(s, chi_5) (Dirichlet mod 5, dim 1):");
z_d5 = lfunzeros(lfuncreate([5, [1]]), 100);
print("   Zeros: ", #z_d5, ", Var: ", svar(z_d5));

\\ 3. Artin L-function for S3
\\ The splitting field of x^3-2 is Q(cbrt(2), omega)
\\ Galois group is S3
print("");
print("5. S3 Artin (attempting dim-2 rep):");
P = x^3 - 2;
G = galoisinit(nfinit(P));
print("   Galois group order: ", G.order);
\\ List character table
ct = galoischartable(G);
print("   Character dimensions: ", vector(#ct, i, ct[i][1]));
