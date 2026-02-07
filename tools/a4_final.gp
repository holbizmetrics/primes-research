/* A4 variance - all found polynomials */
svar(z)={my(s,m,n);if(#z<5,return(-1));s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}

print("=== A4 Variance Test ===")

polys = [x^4+8*x+12, x^4+24*x+36]
vars = []

for(i=1,#polys,
  p = polys[i]
  g = polgalois(p)
  print(i, ": ", p, " Galois=", g[4])
  K = nfinit(p)
  z = lfunzeros(lfuncreate(K), 50)
  v = svar(z)
  vars = concat(vars, [v])
  print("   zeros=", #z, " var=", v)
)

print("")
print("A4 mean variance: ", vecsum(vars)/#vars)
print("Compare: S3=0.25, S4=0.26, D4=0.47, C4=0.53")
quit
