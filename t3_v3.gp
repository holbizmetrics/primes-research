\\ Verify: compute GUE kappa2 (= Sigma2 = number variance) via kernel integral
\\ kappa2 = L - int_0^L int_0^L K(x-y)^2 dx dy
\\ kappa3 = 2 * int_0^L int_0^L int_0^L K(x-y)*K(y-z)*K(x-z) dx dy dz
{
my(KK(x) = if(abs(x) < 1e-12, 1.0, sin(Pi*x)/(Pi*x)));
printf("=== GUE cumulants via kernel integration ===\n");
printf("L     kappa2_num  kappa2_formula  kappa3\n");
my(Lv=[0.5, 1.0, 1.5, 2.0, 3.0, 5.0]);
for(li=1, #Lv,
  my(L=Lv[li], nn=30, dx=L/nn);

  \\ kappa2 = L - int int K^2
  my(s2=0.);
  for(a=0, nn-1,
    my(xa=(a+0.5)*dx);
    for(b=0, nn-1,
      my(xb=(b+0.5)*dx);
      s2 += KK(xa-xb)^2 * dx^2
    )
  );
  my(k2 = L - s2);

  \\ Known formula: Sigma2(L) ~ (1/pi^2)(log(2*pi*L) + gamma + 1 - pi^2/8) for large L
  my(k2f = if(L > 1, (log(2*Pi*L) + Euler + 1 - Pi^2/8)/Pi^2, k2));

  \\ kappa3
  my(s3=0.);
  for(a=0, nn-1,
    my(xa=(a+0.5)*dx);
    for(b=0, nn-1,
      my(xb=(b+0.5)*dx);
      for(c=0, nn-1,
        my(xc=(c+0.5)*dx);
        s3 += 2*KK(xa-xb)*KK(xb-xc)*KK(xa-xc) * dx^3
      )
    )
  );

  printf("L=%4.1f  k2=%7.4f  k2f=%7.4f  k3=%+8.4f\n", L, k2, k2f, s3)
)
}
