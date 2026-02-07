/* A4 batch test - multiple polynomials */
svar(z) = {my(s,m,n); if(#z<5,return(-1)); s=vector(#z-1,i,z[i+1]-z[i]); m=vecsum(s)/#s; n=vector(#s,i,s[i]/m); vecsum(vector(#n,i,(n[i]-1)^2))/#n}

print("=== A4 Batch Test ===");

/* Test multiple A4 polynomials */
/* A4 requires disc to be a perfect square and group order 12 */

vars = [];

/* x^4 - 5x^2 + 5 - known A4 */
p = x^4 - 5*x^2 + 5;
g = polgalois(p);
print("Testing: ", p, " Galois: ", g);
if(g[1] == 12,
  K = nfinit(p);
  z = lfunzeros(lfuncreate(K), 40);
  v = svar(z);
  vars = concat(vars, [v]);
  print("  A4: zeros=", #z, " var=", v);
);

/* x^4 + x^2 + 1 */
p = x^4 + x^2 + 1;
g = polgalois(p);
print("Testing: ", p, " Galois: ", g);
if(g[1] == 12,
  K = nfinit(p);
  z = lfunzeros(lfuncreate(K), 40);
  v = svar(z);
  vars = concat(vars, [v]);
  print("  A4: zeros=", #z, " var=", v);
);

/* x^4 - 2 is D4, not A4 - skip */

/* x^4 + 3x^2 + 3 */
p = x^4 + 3*x^2 + 3;
g = polgalois(p);
print("Testing: ", p, " Galois: ", g);
if(g[1] == 12,
  K = nfinit(p);
  z = lfunzeros(lfuncreate(K), 40);
  v = svar(z);
  vars = concat(vars, [v]);
  print("  A4: zeros=", #z, " var=", v);
);

/* x^4 + 2x^2 + 4 */
p = x^4 + 2*x^2 + 4;
g = polgalois(p);
print("Testing: ", p, " Galois: ", g);
if(g[1] == 12,
  K = nfinit(p);
  z = lfunzeros(lfuncreate(K), 40);
  v = svar(z);
  vars = concat(vars, [v]);
  print("  A4: zeros=", #z, " var=", v);
);

print("");
print("=== Summary ===");
print("A4 samples: ", #vars);
if(#vars > 0, print("Mean variance: ", vecsum(vars)/#vars));

quit
