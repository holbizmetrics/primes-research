v(z)={my(g,ng);if(#z<3,return(-1));g=vector(#z-1,i,z[i+1]-z[i]);ng=vector(#g,i,g[i]*log(z[i]/(2*Pi))/(2*Pi));vecsum(vector(#ng,i,(ng[i]-1)^2))/#ng};

K2=nfinit(x^2-2); z2=lfunzeros(lfuncreate(K2),60); print("Q(sqrt2): ",#z2," var=",precision(v(z2),3));
K3=nfinit(x^3-2); z3=lfunzeros(lfuncreate(K3),60); print("Q(cbrt2): ",#z3," var=",precision(v(z3),3));
K4=nfinit(x^4+1); z4=lfunzeros(lfuncreate(K4),60); print("Q(zeta8): ",#z4," var=",precision(v(z4),3));
