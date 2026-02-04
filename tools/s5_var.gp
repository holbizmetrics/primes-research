default(parisizemax, 256000000)
svar(z)={my(s,m,n);s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}
print("S5 variance test")
print("S5 has 7 irreps: dims 1,1,4,4,5,5,6 -> 7 factors")
K=nfinit(x^5-x-1)
print("S5 field initialized")
L=lfuncreate(K)
print("L-function created")
z=lfunzeros(L,25)
print("S5 x^5-x-1: zeros=",#z," var=",svar(z))
quit
