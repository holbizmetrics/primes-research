\\ Cancellation test - simplified
z=lfunzeros(lfuncreate(1),100);
K=nfinit(x^3-2);
L=lfuncreate(K);
d=lfunzeros(L,100);

\\ Compute variance of oscillatory sum for each
\\ Using N=1000
N=1000;

\\ Zeta
sz=0.0;sz2=0.0;
for(i=1,100,x=2+i*9.8;v=0.0;for(j=1,min(#z,30),g=z[j];v+=-2*sqrt(x)/sqrt(0.25+g^2)*cos(g*log(x)));sz+=v;sz2+=v^2);
vz=(sz2-sz^2/100)/100;

\\ Dedekind
sd=0.0;sd2=0.0;
for(i=1,100,x=2+i*9.8;v=0.0;for(j=1,min(#d,30),g=d[j];v+=-2*sqrt(x)/sqrt(0.25+g^2)*cos(g*log(x)));sd+=v;sd2+=v^2);
vd=(sd2-sd^2/100)/100;

print("Var(zeta): ",vz);
print("Var(Dedekind): ",vd);
print("Ratio Ded/Zeta: ",vd/vz);
print("Prediction: Ratio > 1 means Dedekind has WORSE cancellation");
