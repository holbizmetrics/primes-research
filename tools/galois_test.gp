\\ Galois Coupling Variance Test
\\ Tests Q(sqrt(d)) vs Q(cbrt(d)) for squarefree d

svar(z) = {
  my(s, m);
  if(#z < 5, return(-1));
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  vecsum(vector(#s, i, (s[i]/m - 1)^2)) / #s
}

test_pair(d) = {
  my(K2, K3, z2, z3, v2, v3);
  K2 = nfinit(x^2 - d);
  K3 = nfinit(x^3 - d);
  z2 = lfunzeros(lfuncreate(K2), 60);
  z3 = lfunzeros(lfuncreate(K3), 60);
  v2 = svar(z2);
  v3 = svar(z3);
  printf("%d %.4f %.4f %.4f\n", d, v2, v3, v2-v3);
  [v2, v3]
}

print("d ab nonab diff");
