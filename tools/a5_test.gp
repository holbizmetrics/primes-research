svar(z)={my(s,m,n);s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}
print("=== A5 Galois Group Test ===")
print("A5 has 5 irreps: 1, 3, 3', 4, 5 (dims)")
print("Factor count = 5")
p=x^5-5*x+12
g=polgalois(p)
print("Testing: ", p)
print("Galois: ", g)
K=nfinit(p)
z=lfunzeros(lfuncreate(K),40)
print("A5: zeros=",#z," var=",svar(z))
quit
