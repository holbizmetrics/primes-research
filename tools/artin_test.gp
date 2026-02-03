svar(z) = {
  my(s, m);
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  vecsum(vector(#s, i, (s[i]/m - 1)^2)) / #s
}

print("Testing Pure Artin L-function extraction...");
print("");

\\ Dedekind zeta of Q(cbrt(2)) = zeta * L(rho_2)
K = nfinit(x^3-2);
zd = lfunzeros(lfuncreate(K), 80);
print("Dedekind Q(cbrt2) zeros: ", #zd);
print("Dedekind variance: ", svar(zd));

\\ Riemann zeta
zz = lfunzeros(lfuncreate(1), 80);
print("Zeta zeros: ", #zz);
print("Zeta variance: ", svar(zz));

\\ For comparison: Dedekind of Q(sqrt2) = zeta * L(chi)
K2 = nfinit(x^2-2);
z2 = lfunzeros(lfuncreate(K2), 80);
print("Dedekind Q(sqrt2) zeros: ", #z2);
print("Dedekind Q(sqrt2) variance: ", svar(z2));

print("");
print("Summary:");
print("  Q(sqrt2) = zeta * L(chi): var = ", svar(z2));
print("  Q(cbrt2) = zeta * L(rho2): var = ", svar(zd));
print("  Difference: ", svar(z2) - svar(zd));

quit
