/* A4 Galois Group Variance Test */
print("=== A4 Galois Group Variance Test ===");

svar(z) = {
  my(s, m, n);
  if(#z < 5, return(-1));
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  n = vector(#s, i, s[i]/m);
  vecsum(vector(#n, i, (n[i]-1)^2)) / #n
}

/* A4 requires discriminant to be a perfect square */
p = x^4 + 8*x + 12;
print("Testing: ", p);
d = poldisc(p);
print("Disc: ", d, " sqrt: ", if(issquare(d), sqrtint(d), "not square"));
g = polgalois(p);
print("Galois: ", g);

K = nfinit(p);
z = lfunzeros(lfuncreate(K), 50);
print("A4 #1: zeros=", #z, " var=", svar(z));

/* More A4 examples */
p2 = x^4 - 5*x^2 + 5;
g2 = polgalois(p2);
print("Testing: ", p2, " Galois: ", g2);
if(g2[1] == 12,
  K2 = nfinit(p2);
  z2 = lfunzeros(lfuncreate(K2), 50);
  print("A4 #2: zeros=", #z2, " var=", svar(z2));
);

/* Try x^4 + x^2 - 1 */
p3 = x^4 + x^2 - 1;
g3 = polgalois(p3);
print("Testing: ", p3, " Galois: ", g3);
if(g3[1] == 12,
  K3 = nfinit(p3);
  z3 = lfunzeros(lfuncreate(K3), 50);
  print("A4 #3: zeros=", #z3, " var=", svar(z3));
);

quit
