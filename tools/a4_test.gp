\\ A4 Galois group variance test
\\ A4 has irreps: 1, 1, 1 (from A4/V4 = C3) and one 3-dim
\\ So 4 factors with dimensions 1, 1, 1, 3

svar(z) = {
  my(s, m, n);
  if(#z < 5, return(-1));
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  n = vector(#s, i, s[i]/m);
  vecsum(vector(#n, i, (n[i]-1)^2)) / #n
}

\\ Known A4 polynomials (discriminant is a perfect square)
\\ x^4 + 8x + 12 -> disc = 2^12 * 3^2 = perfect square? Let's check

print("=== A4 Galois Group Test ===");
print("");

\\ Test candidates - A4 requires disc to be a perfect square
polys = [
  x^4 + 8*x + 12,
  x^4 - 2*x + 2,
  x^4 + x + 1,
  x^4 - x^2 + 1,
  x^4 + 4*x^2 + 2,
  x^4 - 4*x^2 + 2
];

for(i = 1, #polys,
  p = polys[i];
  d = poldisc(p);
  if(issquare(d),
    print("Candidate A4: ", p, " disc=", d, " sqrt=", sqrtint(abs(d)));
    K = nfinit(p);
    gal = polgalois(p);
    print("  Galois: ", gal);
    if(gal[1] == 12 && gal[2] == -1,
      print("  Confirmed A4!");
      z = lfunzeros(lfuncreate(K), 50);
      print("  Zeros: ", #z, " Variance: ", svar(z));
    );
    print("");
  )
)

\\ More systematic: find A4 quartics
print("=== Searching for A4 quartics ===");
found = 0;
for(a = -5, 5,
  for(b = -5, 5,
    if(found < 5,
      p = x^4 + a*x + b;
      if(polisirreducible(p),
        d = poldisc(p);
        if(issquare(abs(d)) && d != 0,
          gal = polgalois(p);
          if(gal[1] == 12 && gal[2] == -1,
            found++;
            print("A4 #", found, ": x^4 + ", a, "*x + ", b);
            K = nfinit(p);
            z = lfunzeros(lfuncreate(K), 50);
            print("  Zeros: ", #z, " Variance: ", svar(z));
          )
        )
      )
    )
  )
)
