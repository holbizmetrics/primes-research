v(z)={my(g,ng);g=vector(#z-1,i,z[i+1]-z[i]);ng=vector(#g,i,g[i]*log(z[i]/(2*Pi))/(2*Pi));vecsum(vector(#ng,i,(ng[i]-1)^2))/#ng}
K=nfinit(x^2-2)
z=lfunzeros(lfuncreate(K),150)
print("Q(sqrt2) T=150: ",#z," zeros, var=",precision(v(z),4))
