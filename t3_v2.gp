\\ 3-point: careful centered cumulants + GUE prediction
\\ For determinantal point process, kappa_3 = 2 * int_0^L int_0^L int_0^L K(a-b)*K(b-c)*K(a-c) da db dc
\\ where K(x) = sin(pi*x)/(pi*x)

\\ GUE kappa3 via numerical integration
{
my(KK(x) = if(abs(x) < 1e-12, 1.0, sin(Pi*x)/(Pi*x)));
printf("=== GUE kappa3 prediction ===\n");
my(Lv=[0.5, 1.0, 1.5, 2.0, 3.0, 5.0]);
for(li=1, #Lv,
  my(L=Lv[li], nn=20, dx=L/nn, s=0.);
  for(a=0, nn-1,
    my(xa = (a+0.5)*dx);
    for(b=0, nn-1,
      my(xb = (b+0.5)*dx);
      for(c=0, nn-1,
        my(xc = (c+0.5)*dx);
        s += 2 * KK(xa-xb) * KK(xb-xc) * KK(xa-xc) * dx^3
      )
    )
  );
  printf("L=%4.1f  kappa3_GUE = %+.4f\n", L, s)
)
}

\\ Now: zeta zeros with VERY careful cumulant computation
\\ kappa3 = E[(X-mu)^3] = E[X^3] - 3*mu*E[X^2] + 2*mu^3
{
my(Z=lfunzeros(1,300), nz=#Z);
my(Nsmooth(t) = t/(2*Pi)*log(t/(2*Pi*exp(1))) + 7/8);
my(U=vector(nz, i, Nsmooth(Z[i])));
printf("\n=== Zeta zero counting cumulants (N=%d zeros) ===\n", nz);
printf("Expected: N([x,x+L]) has mean L, so delta = count - L has mean ~0\n\n");
my(Lv=[0.5, 1.0, 1.5, 2.0, 3.0, 5.0]);
for(li=1, #Lv,
  my(L=Lv[li], vals=List());
  for(j=1, nz,
    my(x0=U[j]);
    if(x0 + L > U[nz], break);
    my(cnt=0);
    for(k=j, nz,
      if(U[k] < x0, next);
      if(U[k] >= x0+L, break);
      cnt++
    );
    listput(vals, 1.0*cnt)
  );
  my(nw=#vals);
  if(nw < 20, next);
  my(mu = vecsum(Vec(vals))/nw);
  my(d = vector(nw, i, vals[i] - mu));
  my(v2 = vecsum(vector(nw, i, d[i]^2))/nw);
  my(v3 = vecsum(vector(nw, i, d[i]^3))/nw);
  my(skew = if(v2 > 0.001, v3/v2^1.5, 0));
  printf("L=%4.1f  nw=%d  mean=%.3f  var=%.4f  mu3=%.5f  skewness=%.3f\n", L, nw, mu, v2, v3, skew)
)
}
