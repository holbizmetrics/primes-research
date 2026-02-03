svar(z) = {
  my(s, m);
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  vecsum(vector(#s, i, (s[i]/m - 1)^2)) / #s
}

print("=== Pure Artin L-function Variance ===");
print("");

\\ Splitting field of Q(cbrt(2))
P = polcompositum(x^3-2, polcyclo(3))[1];
print("Splitting field: ", P);

nf = nfinit(P);
gal = galoisinit(P);
print("Galois group: ", galoisidentify(gal));

\\ 2-dim irrep of S3: character [2, 0, -1] on classes [e, (123), (12)]
rho = [2, 0, -1];
print("Character: ", rho);

L = lfunartin(nf, gal, rho, 1);
print("Artin L-function created");

z = lfunzeros(L, 80);
print("");
print("Pure Artin L(s, rho_2) results:");
print("  Zeros computed: ", #z);
print("  Variance: ", svar(z));

\\ Compare with Dedekind and zeta
print("");
print("Comparison:");

K = nfinit(x^3-2);
zd = lfunzeros(lfuncreate(K), 80);
print("  Dedekind Q(cbrt2): n=", #zd, ", var=", svar(zd));

zz = lfunzeros(lfuncreate(1), 80);
print("  Riemann zeta: n=", #zz, ", var=", svar(zz));

print("");
print("=== Summary ===");
print("Pure Artin L(rho_2): var = ", svar(z));
print("Dedekind (merged):   var = ", svar(zd));
print("Riemann zeta:        var = ", svar(zz));
print("");
print("If pure Artin ~ GUE (~0.27), Dedekind lower variance");
print("comes from cross-factor coupling, not intrinsic Artin.");

quit
