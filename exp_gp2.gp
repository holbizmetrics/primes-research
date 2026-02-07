R_inv=0.5;
bs(v,NN,t,lam,mode)={my(k=2*Pi*lam,ar=0.,ai=0.,c=0,rn=0.);for(i=1,#v,my(n=v[i],r=n*1.0/NN);if(r<0.01,next);c++;if(mode==0,rn=r^(1-2*t)*R_inv^(2*t));if(mode==1,rn=(1-t)*r+t*R_inv);if(mode==2,rn=1.0/((1-t)/r+t/R_inv));if(mode==3,rn=sqrt((1-t)*r^2+t*R_inv^2));if(mode==4,rn=abs(r^(1+2*t)*R_inv^(-2*t));if(rn>10,rn=10));my(z=1-2*rn,ph=2*k*z);ar+=cos(ph);ai+=sin(ph));if(c>0,(ar^2+ai^2)/c^2,0)}
NN=1000;pr=select(isprime,vector(NN-1,i,i+1));co=select(n->!isprime(n)&&n>3,vector(NN-1,i,i+1));
print("#P=",#pr," #C=",#co);
\\ EXP 1+2: Scan all modes at lam=6
print("=== LAM=6: All focusing modes ===");
for(mi=0,4,my(nm=["geo","arith","harm","quad","repul"][mi+1],bt=0.,bpc=0.);forstep(ti,5,400,2,my(t=ti/500.0,bp=bs(pr,NN,t,6,mi),bc=bs(co,NN,t,6,mi),pc=if(bc>1e-12,bp/bc,0.));if(pc>bpc&&pc<1e8,bpc=pc;bt=t));printf("%6s t=%.3f P/C=%.1f P=%.6f C=%.9f\n",nm,bt,bpc,bs(pr,NN,bt,6,mi),bs(co,NN,bt,6,mi)))
\\ lam=10
print("=== LAM=10 ===");
for(mi=0,4,my(nm=["geo","arith","harm","quad","repul"][mi+1],bt=0.,bpc=0.);forstep(ti,5,400,2,my(t=ti/500.0,bp=bs(pr,NN,t,10,mi),bc=bs(co,NN,t,10,mi),pc=if(bc>1e-12,bp/bc,0.));if(pc>bpc&&pc<1e8,bpc=pc;bt=t));printf("%6s t=%.3f P/C=%.1f P=%.6f C=%.9f\n",nm,bt,bpc,bs(pr,NN,bt,10,mi),bs(co,NN,bt,10,mi)))
\\ lam=30
print("=== LAM=30 ===");
for(mi=0,4,my(nm=["geo","arith","harm","quad","repul"][mi+1],bt=0.,bpc=0.);forstep(ti,5,400,2,my(t=ti/500.0,bp=bs(pr,NN,t,30,mi),bc=bs(co,NN,t,30,mi),pc=if(bc>1e-12,bp/bc,0.));if(pc>bpc&&pc<1e8,bpc=pc;bt=t));printf("%6s t=%.3f P/C=%.1f P=%.6f C=%.9f\n",nm,bt,bpc,bs(pr,NN,bt,30,mi),bs(co,NN,bt,30,mi)))
\\ lam=35
print("=== LAM=35 ===");
for(mi=0,4,my(nm=["geo","arith","harm","quad","repul"][mi+1],bt=0.,bpc=0.);forstep(ti,5,400,2,my(t=ti/500.0,bp=bs(pr,NN,t,35,mi),bc=bs(co,NN,t,35,mi),pc=if(bc>1e-12,bp/bc,0.));if(pc>bpc&&pc<1e8,bpc=pc;bt=t));printf("%6s t=%.3f P/C=%.1f P=%.6f C=%.9f\n",nm,bt,bpc,bs(pr,NN,bt,35,mi),bs(co,NN,bt,35,mi)))
\\ N-STABILITY at lam=6
print("=== N-STABILITY lam=6 ===");
for(ni=1,4,my(N2=[500,1000,2000,5000][ni],p2=select(isprime,vector(N2-1,i,i+1)),c2=select(n->!isprime(n)&&n>3,vector(N2-1,i,i+1)));for(mi=0,4,my(nm=["geo","arith","harm","quad","repul"][mi+1],bt=0.,bpc=0.);forstep(ti,5,200,2,my(t=ti/250.0,bp=bs(p2,N2,t,6,mi),bc=bs(c2,N2,t,6,mi),pc=if(bc>1e-12,bp/bc,0.));if(pc>bpc&&pc<1e8,bpc=pc;bt=t));printf("N=%5d %6s t=%.3f P/C=%.1f\n",N2,nm,bt,bpc));print(""))
