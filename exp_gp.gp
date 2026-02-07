\\ Experiments in clean PARI/GP syntax
R_inv = 0.5;

\\ Backscatter: mode 0=geo, 1=arith, 2=harm, 3=quad, 4=repulsive
bs(v, NN, t, lam, mode) = {
  my(k=2*Pi*lam, ar=0., ai=0., c=0, rn=0.);
  for(i=1, #v,
    my(n=v[i], r=n*1.0/NN);
    if(r < 0.01, next);
    c++;
    if(mode == 0,
      rn = r^(1-2*t) * R_inv^(2*t)
    );
    if(mode == 1,
      rn = (1-t)*r + t*R_inv
    );
    if(mode == 2,
      rn = 1.0/((1-t)/r + t/R_inv)
    );
    if(mode == 3,
      rn = sqrt((1-t)*r^2 + t*R_inv^2)
    );
    if(mode == 4,
      rn = r^(1+2*t) * R_inv^(-2*t);
      if(rn > 10, rn = 10);
      if(rn < 0.001, rn = 0.001)
    );
    my(z = 1 - 2*rn, ph = 2*k*z);
    ar += cos(ph); ai += sin(ph)
  );
  if(c > 0, (ar^2 + ai^2)/c^2, 0)
};

NN = 1000;
pr = select(isprime, vector(NN-1, i, i+1));
co = select(n -> !isprime(n) && n > 3, vector(NN-1, i, i+1));
print("#P=", #pr, " #C=", #co);

print("");
print("=== EXP 1: REPULSIVE vs STANDARD at lam=6 ===");
print("t     geo_P    geo_C    geo_P/C  rep_P    rep_C    rep_P/C");
for(ti = 2, 40,
  my(t = ti/1000.0);
  my(gp = bs(pr,NN,t,6,0), gc = bs(co,NN,t,6,0));
  my(rp = bs(pr,NN,t,6,4), rc = bs(co,NN,t,6,4));
  my(gpc = if(gc>1e-12, gp/gc, 0));
  my(rpc = if(rc>1e-12, rp/rc, 0));
  printf("%.3f %.6f %.6f %7.1f  %.6f %.6f %7.1f\n", t, gp, gc, gpc, rp, rc, rpc)
);

print("");
print("=== EXP 2: POWER MEAN COMPARISON at lam=6 ===");
my(mnames = ["geo", "arith", "harm", "quad", "repuls"]);
for(mi = 0, 4,
  my(bt=0., bpc=0.);
  for(ti = 5, 400,
    my(t = ti/500.0);
    my(bp = bs(pr,NN,t,6,mi));
    my(bc = bs(co,NN,t,6,mi));
    my(pc = if(bc>1e-12, bp/bc, 0));
    if(pc > bpc && pc < 1e8, bpc = pc; bt = t)
  );
  my(bp = bs(pr,NN,bt,6,mi), bc = bs(co,NN,bt,6,mi));
  printf("%6s: best t=%.3f P/C=%.1f  P=%.6f C=%.9f\n", mnames[mi+1], bt, bpc, bp, bc)
);

print("");
print("=== EXP 2b: POWER MEAN at lam=10 ===");
for(mi = 0, 4,
  my(bt=0., bpc=0.);
  for(ti = 5, 400,
    my(t = ti/500.0);
    my(bp = bs(pr,NN,t,10,mi));
    my(bc = bs(co,NN,t,10,mi));
    my(pc = if(bc>1e-12, bp/bc, 0));
    if(pc > bpc && pc < 1e8, bpc = pc; bt = t)
  );
  my(bp = bs(pr,NN,bt,10,mi), bc = bs(co,NN,bt,10,mi));
  printf("%6s: best t=%.3f P/C=%.1f  P=%.6f C=%.9f\n", mnames[mi+1], bt, bpc, bp, bc)
);

print("");
print("=== EXP 2c: POWER MEAN at lam=30 ===");
for(mi = 0, 4,
  my(bt=0., bpc=0.);
  for(ti = 5, 400,
    my(t = ti/500.0);
    my(bp = bs(pr,NN,t,30,mi));
    my(bc = bs(co,NN,t,30,mi));
    my(pc = if(bc>1e-12, bp/bc, 0));
    if(pc > bpc && pc < 1e8, bpc = pc; bt = t)
  );
  my(bp = bs(pr,NN,bt,30,mi), bc = bs(co,NN,bt,30,mi));
  printf("%6s: best t=%.3f P/C=%.1f  P=%.6f C=%.9f\n", mnames[mi+1], bt, bpc, bp, bc)
);

print("");
print("=== N-STABILITY ===");
for(NN2 = 1, 4,
  my(N2 = [500, 1000, 2000, 5000][NN2]);
  my(p2 = select(isprime, vector(N2-1, i, i+1)));
  my(c2 = select(n -> !isprime(n) && n > 3, vector(N2-1, i, i+1)));
  for(mi = 0, 4,
    my(bt=0., bpc=0.);
    for(ti = 2, 200,
      my(t = ti/250.0);
      my(bp = bs(p2,N2,t,6,mi));
      my(bc = bs(c2,N2,t,6,mi));
      my(pc = if(bc>1e-12, bp/bc, 0));
      if(pc > bpc && pc < 1e8, bpc = pc; bt = t)
    );
    printf("N=%5d %6s L=6: t=%.3f P/C=%.1f\n", N2, mnames[mi+1], bt, bpc)
  );
  print("")
);
