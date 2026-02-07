\\ SPARK Berry Conjecture — Computation 1: Gap autocorrelation
{
for(ni=1,5,
  my(N2=[200,500,1000,2000,5000][ni]);
  my(P2=primes([2,N2]));
  my(n2=#P2);
  if(n2<5,next);
  my(u2=vector(n2,i,if(P2[i]>2, intnum(x=2,P2[i],1/log(x)), 0)));
  my(g2=vector(n2-1,i,u2[i+1]-u2[i]));
  my(m2=vecsum(g2)/(n2-1));
  my(gn=vector(n2-1,i,g2[i]/m2));
  my(vv=sum(i=1,n2-1,(gn[i]-1)^2)/(n2-1));
  my(cc=sum(i=1,n2-2,(gn[i]-1)*(gn[i+1]-1))/(n2-2));
  printf("N=%5d #P=%4d lag1=%+.4f\n",N2,n2,cc/vv)
)
}
