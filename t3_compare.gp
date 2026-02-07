\\ 3-point analysis: zeta mu3 vs GUE kappa3
\\ Step 1: Zeta zero counting function moments
{
my(Z=lfunzeros(1,300), nz=#Z);
my(Nsmooth(t)=t/(2*Pi)*log(t/(2*Pi*exp(1)))+7/8);
my(U=vector(nz,i,Nsmooth(Z[i])));
printf("zeros=%d\n\n",nz);
printf("L     | mu2_zeta  mu3_zeta\n");
printf("------|-------------------\n");
my(Lv=[0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 10.0]);
for(li=1,#Lv,
  my(L=Lv[li], nw=0, s1=0., s2=0., s3=0.);
  for(j=1,nz,
    my(x0=U[j]);
    if(x0+L > U[nz], next);
    my(cnt=0);
    for(k=j,nz,
      if(U[k] >= x0 && U[k] < x0+L, cnt++);
      if(U[k] >= x0+L, break)
    );
    my(d=1.0*cnt - L);
    nw++; s1 += d; s2 += d^2; s3 += d^3
  );
  if(nw < 10, next);
  my(m1=s1/nw, v2=s2/nw - m1^2, m3c=s3/nw - 3*m1*(s2/nw) + 2*m1^3);
  printf("L=%4.1f  nw=%3d  mu2=%+7.3f  mu3=%+8.3f  (raw_m3=%+8.3f)\n", L, nw, v2, m3c, s3/nw)
)
}
