default(parisizemax, 128000000)
svar(z)={my(s,m,n);s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}
print("A5 variance test")
print("A5 has 5 irreps: dims 1,3,3,4,5 -> 5 factors")
K=nfinit(x^5+20*x-16)
print("Field initialized")
L=lfuncreate(K)
print("L-function created")
z=lfunzeros(L,30)
print("A5 x^5+20x-16: zeros=",#z," var=",svar(z))
quit
