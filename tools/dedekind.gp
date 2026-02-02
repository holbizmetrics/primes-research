v(z)={my(s,m,n);if(#z<3,return(-1));s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}
z1=lfunzeros(lfuncreate(1),50);print("deg1: n=",#z1," v=",precision(v(z1),3))
K2=nfinit(x^2-2);z2=lfunzeros(lfuncreate(K2),50);print("deg2: n=",#z2," v=",precision(v(z2),3))
K3=nfinit(x^3-2);z3=lfunzeros(lfuncreate(K3),50);print("deg3: n=",#z3," v=",precision(v(z3),3))
K4=nfinit(x^4-2);z4=lfunzeros(lfuncreate(K4),50);print("deg4: n=",#z4," v=",precision(v(z4),3))
quit
