\\ k-almost: P/C ratio approach at lambda=8 (where signal was clearest)
phi=(1+sqrt(5))/2; ga=2*Pi/phi^2; R=0.5;
coh(v,t,l)={my(N=#v,re=0.,im=0.,k=2*Pi/l,Nm=2000); for(i=1,N, my(n=v[i],r=R*sqrt(n*1.0/Nm),z=r*cos(n*ga*.3),rf=r^(1-2*t)*R^(2*t)); re+=cos(k*z*rf/(r+1e-4)); im+=sin(k*z*rf/(r+1e-4))); (re^2+im^2)/N^2}
ka(b,k)=select(n->bigomega(n)==k,vector(b-1,i,i+1));
pr=select(isprime,vector(1999,i,i+1)); s2=ka(2000,2); s3=ka(2000,3); s4=ka(2000,4);
print("#P=",#pr," #2ap=",#s2," #3ap=",#s3," #4ap=",#s4);
\\ For each class, find where it MOST differs from "all composites"
comp=select(n->!isprime(n)&&n>1,vector(1999,i,i+1));
print("=== P/Comp ratio, lambda=8 ===");
for(ti=1,19, my(t=ti*0.025,cp=coh(pr,t,8),cc=coh(comp,t,8)); printf("t=%.3f  P=%.6f  C=%.6f  P/C=%.2f\n",t,cp,cc,cp/cc));
