svar(z)={my(s,m,n);s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}
print("=== 3-dim Artin L-function Test ===")
print("Using S4 splitting field of x^4-x-1")
P=x^24-4*x^23+8*x^22-8*x^21-8*x^20+48*x^19-56*x^18-8*x^17+108*x^16-176*x^15+16*x^14+240*x^13-260*x^12-8*x^11+316*x^10-288*x^9-16*x^8+288*x^7-164*x^6-80*x^5+156*x^4-48*x^3-28*x^2+24*x-4
print("Splitting field degree: 24 (S4)")
nf=nfinit(P)
gal=galoisinit(P)
print("Galois initialized")
print("Conjugacy classes: ", #gal.conj)
rho3=[3,1,-1,0,1]
L3=lfunartin(nf,gal,rho3,1)
print("3-dim Artin L-function created")
z3=lfunzeros(L3,60)
print("Pure 3-dim Artin: zeros=",#z3," var=",svar(z3))
quit
