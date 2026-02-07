N=1000;
R=0.5;
bs(wl,t,isp)={my(k=2*Pi*wl,ar=0.0,ai=0.0,c=0);for(n=2,N,if(isp&&!isprime(n),next());if(!isp&&isprime(n),next());my(r=n*1.0/N);if(r<0.01,next());my(rn=r^(1-2*t)*R^(2*t),z=1-2*rn);ar=ar+cos(2*k*z);ai=ai+sin(2*k*z);c=c+1);if(c==0,return(0.0));return((ar^2+ai^2)/(c^2))};
print("Testing:");
for(wl=3,21,my(bt=0.0,br=0.0);for(ti=1,49,my(t=ti*1.0/100,p=bs(wl,t,1),cc=bs(wl,t,0),r=if(cc>0.000001,p/cc,0.0));if(r>br,br=r;bt=t));printf("%d: t=%.2f r=%.0f\n",wl,bt,br))
