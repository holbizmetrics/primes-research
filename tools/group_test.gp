default(parisize, 100000000)

svar(z) = {
  my(s, m, n);
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  n = vector(#s, i, s[i]/m);
  vecsum(vector(#n, i, (n[i]-1)^2)) / #n
}

print("=== Galois Group vs Variance Test ===");
print("");

\\ A4 test
print("Testing A4...");
K = nfinit(x^4 + 8*x + 12);
G = polgalois(x^4 + 8*x + 12);
z = lfunzeros(lfuncreate(K), 50);
printf("A4: %s, var=%.3f, n=%d\n", G, svar(z), #z);

\\ Another S4
print("Testing more S4...");
K = nfinit(x^4 - 2*x + 2);
G = polgalois(x^4 - 2*x + 2);
z = lfunzeros(lfuncreate(K), 50);
printf("S4: %s, var=%.3f, n=%d\n", G, svar(z), #z);

\\ D4 variants
print("Testing D4...");
K = nfinit(x^4 - 6);
z = lfunzeros(lfuncreate(K), 50);
printf("D4 (x^4-6): var=%.3f, n=%d\n", svar(z), #z);

print("");
print("Done.");
quit
