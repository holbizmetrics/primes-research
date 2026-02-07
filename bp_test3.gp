N=500; R=0.5;
pv=select(isprime,[2..N]);
cv=select(n->n>3 && !isprime(n),[2..N]);
np=#pv; nc=#cv;
print("P=",np," C=",nc);

bsc(v,nn,t,lam)={my(k=2*Pi*lam,ar=0.0,ai=0.0);for(j=1,nn,my(n=v[j],ro=max(n/N,1e-10),rt=ro^(1-2*t)*R^(2*t),zu=1-2.0*n/N,ph=2*k*rt*zu);ar+=cos(ph);ai+=sin(ph));(ar^2+ai^2)/nn^2};

\\ Fine scan near t=0.25 for lam=8
print("=== lam=8: fine scan near 1/4 ===");
forstep(t=0.20,0.35,0.01,my(bp=bsc(pv,np,t,8),bc=bsc(cv,nc,t,8),r=if(bc>1e-12,bp/bc,0));print("  t=",precision(t,3)," P=",precision(bp,4)," C=",precision(bc,4)," P/C=",precision(r,3)));

\\ Fine scan for lam=21
print("=== lam=21: fine scan ===");
forstep(t=0.15,0.40,0.01,my(bp=bsc(pv,np,t,21),bc=bsc(cv,nc,t,21),r=if(bc>1e-12,bp/bc,0));print("  t=",precision(t,3)," P=",precision(bp,4)," C=",precision(bc,4)," P/C=",precision(r,3)));

quit;
