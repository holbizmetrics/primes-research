\\ k-almost prime Brennpunkt - compact version
phi=(1+sqrt(5))/2; ga=2*Pi/phi^2; R=0.5;
coh(nums,t,lam)={my(N=#nums,re=0.0,im=0.0,k2=2*Pi/lam); for(i=1,N, my(n=nums[i],r=R*sqrt(n/1000.0),z); z=r*cos(n*ga*0.3); my(rf=r^(1-2*t)*R^(2*t),zf=z*rf/(r+1e-4)); re+=cos(k2*zf); im+=sin(k2*zf)); (re^2+im^2)/N^2}
ka(b,k)=select(n->bigomega(n)==k,vector(b-1,i,i+1));
N=2000; lam=21;
pr=select(n->isprime(n),vector(N-1,i,i+1));
s2=ka(N,2); s3=ka(N,3); s4=ka(N,4);
print("Counts: P=",#pr," 2ap=",#s2," 3ap=",#s3," 4ap=",#s4);
for(c=1,4, my(nums,nm); if(c==1,nums=pr;nm="Primes  "); if(c==2,nums=s2;nm="Semi    "); if(c==3,nums=s3;nm="3-almost"); if(c==4,nums=s4;nm="4-almost"); my(bt=0,bc=0); for(ti=1,95, my(t=ti*0.005,v=coh(nums,t,lam)); if(v>bc,bc=v;bt=t)); printf("%s: peak t=%.3f  coh=%.6f\n",nm,bt,bc));
