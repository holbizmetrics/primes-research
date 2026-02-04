svar(z)={my(s,m,n);s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}
print("A4 #1: x^4+8x+12")
K1=nfinit(x^4+8*x+12)
z1=lfunzeros(lfuncreate(K1),50)
print("zeros=",#z1," var=",svar(z1))
print("A4 #2: x^4+24x+36")
K2=nfinit(x^4+24*x+36)
z2=lfunzeros(lfuncreate(K2),50)
print("zeros=",#z2," var=",svar(z2))
print("Mean: ",(svar(z1)+svar(z2))/2)
quit
