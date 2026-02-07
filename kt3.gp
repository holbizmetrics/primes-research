\\ Correct 3D golden spiral + backscatter from original JS
\\ r = sqrt(n), theta = n*golden_angle, z = r*cos(asin(frac(n*phi)))
\\ Focus: r_f = r^(1-2t)*R^(2t), preserve angles, scale z proportionally
phi=(1+sqrt(5))/2; ga=2*Pi/phi^2; R=1.0;
bc(v,t,lam)={
  my(N=#v,re=0.,im=0.,k=2*Pi/lam);
  for(i=1,N,
    my(n=v[i], r=sqrt(n*1.0), th=n*ga);
    my(lat=asin(frac(n*phi)*2-1));
    my(x=r*cos(th)*cos(lat), y=r*sin(th)*cos(lat), z=r*sin(lat));
    my(rf=r^(1-2*t)*R^(2*t));
    my(sc=rf/r);
    my(zf=z*sc);
    re+=cos(k*zf); im+=sin(k*zf)
  );
  (re^2+im^2)/N^2
}
pr=select(isprime,vector(999,i,i+1));
comp=select(n->!isprime(n)&&n>1,vector(999,i,i+1));
ka(b,k)=select(n->bigomega(n)==k,vector(b-1,i,i+1));
s2=ka(1000,2); s3=ka(1000,3);
print("#P=",#pr," #C=",#comp," #2ap=",#s2," #3ap=",#s3);
print("=== lambda=8 P/C scan ===");
for(ti=2,19, my(t=ti*0.025, bp=bc(pr,t,8), bcomp=bc(comp,t,8)); printf("t=%.3f P=%.6f C=%.6f P/C=%.3f\n",t,bp,bcomp,bp/bcomp));
print("\n=== lambda=21 P/C scan ===");
for(ti=2,19, my(t=ti*0.025, bp=bc(pr,t,21), bcomp=bc(comp,t,21)); printf("t=%.3f P=%.6f C=%.6f P/C=%.3f\n",t,bp,bcomp,bp/bcomp));
