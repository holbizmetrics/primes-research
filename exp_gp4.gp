R_inv=0.5;
bs(v,NN,t,lam,mode)={my(k=2*Pi*lam,ar=0.,ai=0.,c=0,rn=0.);for(i=1,#v,my(n=v[i],r=n*1.0/NN);if(r<0.01,next);c++;if(mode==0,rn=r^(1-2*t)*R_inv^(2*t));if(mode==1,rn=(1-t)*r+t*R_inv);if(mode==2,rn=1.0/((1-t)/r+t/R_inv));if(mode==3,rn=sqrt((1-t)*r^2+t*R_inv^2));if(mode==4,rn=abs(r^(1+2*t)*R_inv^(-2*t));if(rn>10,rn=10));my(z=1-2*rn,ph=2*k*z);ar+=cos(ph);ai+=sin(ph));if(c>0,(ar^2+ai^2)/c^2,0)}
scanmode(pr,co,NN,lam,mi)={my(bt=0.,bpc=0.);forstep(ti,5,400,2,my(t=ti/500.0,bp=bs(pr,NN,t,lam,mi),bc=bs(co,NN,t,lam,mi),pc=if(bc>1e-12,bp/bc,0.));if(pc>bpc&&pc<1e8,bpc=pc;bt=t));[bt,bpc]}
NN=1000;pr=select(isprime,vector(NN-1,i,i+1));co=select(n->!isprime(n)&&n>3,vector(NN-1,i,i+1));
print("#P=",#pr," #C=",#co);
