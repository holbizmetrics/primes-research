N=200; R=0.5;
pv=select(isprime,[2..N]);
cv=select(n->n>3 && !isprime(n),[2..N]);
np=#pv; nc=#cv;
print("P=",np," C=",nc);

bsc(v,nn,t,lam)={my(k=2*Pi*lam,ar=0.0,ai=0.0);for(j=1,nn,my(n=v[j],ro=max(n/N,1e-10),rt=ro^(1-2*t)*R^(2*t),zu=1-2.0*n/N,ph=2*k*rt*zu);ar+=cos(ph);ai+=sin(ph));(ar^2+ai^2)/nn^2};

print("--- Scan t for lam=8 (P/C ratio) ---");
forstep(t=0.15,0.45,0.02,my(bp=bsc(pv,np,t,8),bc=bsc(cv,nc,t,8),r=if(bc>1e-12,bp/bc,0));print("  t=",precision(t,2)," P/C=",precision(r,3)));

print("--- Scan t for lam=21 (P/C ratio) ---");
forstep(t=0.15,0.45,0.02,my(bp=bsc(pv,np,t,21),bc=bsc(cv,nc,t,21),r=if(bc>1e-12,bp/bc,0));print("  t=",precision(t,2)," P/C=",precision(r,3)));

print("--- Key comparisons ---");
print("t=0.25 lam=8:  P=",precision(bsc(pv,np,.25,8),5)," C=",precision(bsc(cv,nc,.25,8),5));
print("t=0.33 lam=8:  P=",precision(bsc(pv,np,.33,8),5)," C=",precision(bsc(cv,nc,.33,8),5));
print("t=0.25 lam=21: P=",precision(bsc(pv,np,.25,21),5)," C=",precision(bsc(cv,nc,.25,21),5));
print("t=0.33 lam=21: P=",precision(bsc(pv,np,.33,21),5)," C=",precision(bsc(cv,nc,.33,21),5));

quit;
