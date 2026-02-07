K=nfinit(x^4+8*x+12)
L=lfuncreate(K)
z=lfunzeros(L,40)
s=vector(#z-1,i,z[i+1]-z[i])
m=vecsum(s)/#s
n=vector(#s,i,s[i]/m)
v=vecsum(vector(#n,i,(n[i]-1)^2))/#n
print("A4 x^4+8x+12: zeros=",#z," var=",v)
quit
