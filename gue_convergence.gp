v(z)={my(g,ng);g=vector(#z-1,i,z[i+1]-z[i]);ng=vector(#g,i,g[i]*log(z[i]/(2*Pi))/(2*Pi));vecsum(vector(#ng,i,(ng[i]-1)^2))/#ng}

print("=== GUE Convergence Test ===")
print("")
print("Riemann zeta:")
for(T=50,300,50, z=lfunzeros(lfuncreate(1),T); print("  T=",T,": ",#z," zeros, var=",precision(v(z),4)))

print("")
print("Q(sqrt(2)):")
K=nfinit(x^2-2)
for(T=50,200,50, z=lfunzeros(lfuncreate(K),T); print("  T=",T,": ",#z," zeros, var=",precision(v(z),4)))

print("")
print("GUE prediction: var -> 0.180")
