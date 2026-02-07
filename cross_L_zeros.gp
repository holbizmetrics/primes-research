\\ Zeros of Dirichlet L-functions for cross-SFF analysis
default(realprecision, 28);

\\ q=3: 2 characters
G3 = znstar(3, 1);
for(a = 0, 1, \
  L = lfuncreate([G3, [a]]); \
  z = lfunzeros(L, 120); \
  printf("Q3_CHAR_%d: ", a); \
  for(j = 1, #z, printf("%.10f ", z[j])); \
  printf("\n"); \
);

\\ q=5: 4 characters
G5 = znstar(5, 1);
for(a = 0, 3, \
  L = lfuncreate([G5, [a]]); \
  z = lfunzeros(L, 100); \
  printf("Q5_CHAR_%d: ", a); \
  for(j = 1, #z, printf("%.10f ", z[j])); \
  printf("\n"); \
);

\\ q=7: 6 characters
G7 = znstar(7, 1);
for(a = 0, 5, \
  L = lfuncreate([G7, [a]]); \
  z = lfunzeros(L, 80); \
  printf("Q7_CHAR_%d: ", a); \
  for(j = 1, #z, printf("%.10f ", z[j])); \
  printf("\n"); \
);
