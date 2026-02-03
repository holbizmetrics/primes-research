\\ Test: Does discriminant predict variance within quadratic family?
\\ If no correlation, discriminant is not the driver

svar(z) = {
  my(s, m, n);
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  n = vector(#s, i, s[i]/m);
  vecsum(vector(#n, i, (n[i]-1)^2)) / #n
}

print("Quadratic fields: discriminant vs variance");
print("d    |disc|    variance    zeros");
print("----------------------------------");

test(dd) = {
  my(K, z, v, disc);
  K = nfinit(x^2-dd);
  disc = abs(K.disc);
  z = lfunzeros(lfuncreate(K), 60);
  v = svar(z);
  printf("%d    %d       %.3f       %d\n", dd, disc, v, #z);
  [disc, v]
}

data = [];
data = concat(data, [test(2)]);
data = concat(data, [test(3)]);
data = concat(data, [test(5)]);
data = concat(data, [test(7)]);
data = concat(data, [test(11)]);
data = concat(data, [test(13)]);
data = concat(data, [test(17)]);
data = concat(data, [test(19)]);
data = concat(data, [test(23)]);
data = concat(data, [test(29)]);
data = concat(data, [test(31)]);
data = concat(data, [test(37)]);
data = concat(data, [test(41)]);
data = concat(data, [test(43)]);

\\ Compute correlation
print("");
nn = #data;
sx = sum(i=1,nn,data[i][1]);
sy = sum(i=1,nn,data[i][2]);
sxx = sum(i=1,nn,data[i][1]^2);
syy = sum(i=1,nn,data[i][2]^2);
sxy = sum(i=1,nn,data[i][1]*data[i][2]);
r = (nn*sxy - sx*sy) / sqrt((nn*sxx - sx^2) * (nn*syy - sy^2));
printf("Correlation(|disc|, variance) = %.3f\n", r);
print("If |r| < 0.3, discriminant is not the main driver");
quit
