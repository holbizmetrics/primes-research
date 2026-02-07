#!/usr/bin/env python3
"""SPARK: Cross-L-function SFF

SPRAY:
1. Compute zeros of L(s,chi) for Dirichlet characters chi mod q
2. SFF within each L-function (should be GUE)
3. Cross-SFF between pairs: K(tau) = |sum_i exp(2*pi*i*gamma_i^(1)*tau) * sum_j exp(-2*pi*i*gamma_j^(2)*tau)|
4. Does cross-SFF depend on relationship between chi_1 and chi_2?
5. Joint pair correlation: how do zeros of different L-functions interleave?
6. Sweep q: does cross-correlation change with modulus?
7. What happens when we mix zeta zeros with Dirichlet L zeros?

We need zeros of Dirichlet L-functions.
PARI/GP has lfunzeros(). Let's generate them.
"""
# First: generate zeros using PARI/GP
# Characters mod q: for q=5, there are phi(5)=4 characters
# chi_0 (principal), chi_1, chi_2, chi_3
# chi_0 gives zeta zeros (up to finitely many)

import subprocess, os

# Generate zeros of L(s, chi) for chi mod 5
# q=5 has characters of orders 1, 2, 4, 4
gp_script = r"""
\\ Zeros of Dirichlet L-functions mod 5
\\ Characters mod 5: orders 1(principal), 2, 4, 4

\\ Use lfuncreate for Dirichlet characters
default(realprecision, 28);

\\ chi mod 5, using Conrey labeling
\\ G = znstar(5,1) gives generators
\\ Characters: chi_0 (trivial), chi_1 (order 2), chi_2 (order 4), chi_3 (order 4)

\\ Method: lfuncreate with a Dirichlet character
\\ In PARI: lfuncreate([G, chi]) where G=znstar(q,1), chi=character vector

G = znstar(5, 1);

\\ Get all characters
chars = chargalois(G);  \\ or use specific characters

\\ Actually, let's use the direct approach
\\ For q=5: the characters are determined by chi(2) since 2 generates (Z/5Z)*
\\ chi_0: 2->1    (trivial)
\\ chi_1: 2->-1   (order 2, Legendre symbol mod 5)
\\ chi_2: 2->i    (order 4)
\\ chi_3: 2->-i   (order 4)

\\ In PARI, we specify character as a vector on generators of (Z/qZ)*
\\ For q=5, generator is 2, order 4
\\ Character [a] means chi(2) = e^{2*pi*i*a/4}
\\ a=0: trivial, a=1: order 4, a=2: order 2 (Legendre), a=3: order 4

for(a = 0, 3, \
  L = lfuncreate([G, [a]]); \
  z = lfunzeros(L, 100); \
  printf("CHAR_%d: ", a); \
  for(j = 1, #z, printf("%.10f ", z[j])); \
  printf("\n"); \
);

\\ Also do q=7 (6 characters, orders 1,2,3,3,6,6)
G7 = znstar(7, 1);
for(a = 0, 5, \
  L = lfuncreate([G7, [a]]); \
  z = lfunzeros(L, 80); \
  printf("Q7_CHAR_%d: ", a); \
  for(j = 1, #z, printf("%.10f ", z[j])); \
  printf("\n"); \
);

\\ And q=3 (2 characters)
G3 = znstar(3, 1);
for(a = 0, 1, \
  L = lfuncreate([G3, [a]]); \
  z = lfunzeros(L, 120); \
  printf("Q3_CHAR_%d: ", a); \
  for(j = 1, #z, printf("%.10f ", z[j])); \
  printf("\n"); \
);
"""

with open('/data/data/com.termux/files/home/primes-research/cross_L_zeros.gp', 'w') as f:
    f.write(gp_script)

print("GP script written. Run with: gp -q cross_L_zeros.gp > cross_L_zeros.txt")
print("Then run spark_cross_L2.py to analyze.")
