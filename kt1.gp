\\ Part 1: just counts and coarse scan
phi=(1+sqrt(5))/2; ga=2*Pi/phi^2; R=0.5;
coh(v,t,l)={my(N=#v,re=0.,im=0.,k=2*Pi/l,Nm=v[N]); for(i=1,N, my(n=v[i],r=R*sqrt(n/Nm),z=r*cos(n*ga*.3),rf=r^(1-2*t)*R^(2*t)); re+=cos(k*z*rf/(r+1e-4)); im+=sin(k*z*rf/(r+1e-4))); (re^2+im^2)/N^2}
ka(b,k)=select(n->bigomega(n)==k,vector(b-1,i,i+1));
pr=select(isprime,vector(999,i,i+1)); s2=ka(1000,2); s3=ka(1000,3);
print("#P=",#pr," #2ap=",#s2," #3ap=",#s3);
for(ti=1,9, my(t=ti*0.05); printf("t=%.2f  P=%.4f  2ap=%.4f  3ap=%.4f\n",t,coh(pr,t,21),coh(s2,t,21),coh(s3,t,21)));
