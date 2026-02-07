\\ All 4 experiments in PARI/GP
\\ Using CORRECT fine_scan.py physics: r=n/N, R=0.5, k=2*Pi*lam

R_inv = 0.5;

bs(v, N, t, lam, mode) = {
  my(k=2*Pi*lam, ar=0., ai=0., c=0);
  for(i=1, #v,
    my(n=v[i], r=n*1.0/N);
    if(r < 0.01, next);
    c++;
    my(rn);
    if(mode == 0,
      rn = r^(1-2*t) * R_inv^(2*t),     \\ geometric (standard)
    mode == 1,
      rn = (1-t)*r + t*R_inv,             \\ arithmetic
    mode == 2,
      rn = 1.0/((1-t)/r + t/R_inv),       \\ harmonic
    mode == 3,
      rn = sqrt((1-t)*r^2 + t*R_inv^2),   \\ quadratic
    mode == 4,
      rn = r^(1+2*t) * R_inv^(-2*t);      \\ repulsive
      rn = max(0.001, min(rn, 10))
    );
    my(z = 1 - 2*rn, ph = 2*k*z);
    ar += cos(ph); ai += sin(ph)
  );
  if(c > 0, (ar^2 + ai^2)/c^2, 0)
};

N = 1000;
pr = select(isprime, vector(N-1, i, i+1));
co = select(n -> !isprime(n) && n > 3, vector(N-1, i, i+1));
\\ Random baseline: every 6th number starting at 7 (rough density match)
rr = select(n -> n%6==1 || n%13==3, vector(N-1, i, i+1));
rr = vecextract(rr, vector(min(#rr, #pr), i, i));

print("=== EXP 1: REPULSIVE BRENNPUNKT (mode=4) ===");
print("lam   t     P          C          Rand       P/R    P/C");
for(li = 1, 5,
  my(lam = [6,10,30,35,59][li]);
  my(bt=0, bpe=0);
  for(ti = 1, 80,
    my(t = ti/1000.0);
    my(bp = bs(pr, N, t, lam, 4));
    my(br = bs(rr, N, t, lam, 4));
    my(pe = if(br > 1e-12, bp/br, 0));
    if(pe > bpe && pe < 1e6, bpe = pe; bt = t)
  );
  my(bp = bs(pr, N, bt, lam, 4));
  my(bc = bs(co, N, bt, lam, 4));
  my(br = bs(rr, N, bt, lam, 4));
  my(pc = if(bc > 1e-12, bp/bc, 0));
  printf("L=%2d t=%.3f P=%.6f C=%.6f R=%.6f P/R=%5.1fx P/C=%5.1fx\n", lam, bt, bp, bc, br, bpe, pc)
);

print("");
print("=== EXP 2: POWER MEAN FAMILY ===");
print("mode      lam   t     P/Rand    P/C");
my(modes = ["geo","arith","harm","quad","repuls"]);
for(mi = 0, 4,
  for(li = 1, 4,
    my(lam = [6,10,30,35][li]);
    my(bt=0, bpe=0);
    for(ti = 1, 200,
      my(t = ti/250.0);
      my(bp = bs(pr, N, t, lam, mi));
      my(br = bs(rr, N, t, lam, mi));
      my(pe = if(br > 1e-12, bp/br, 0));
      if(pe > bpe && pe < 1e6, bpe = pe; bt = t)
    );
    my(bp = bs(pr, N, bt, lam, mi));
    my(bc = bs(co, N, bt, lam, mi));
    my(pc = if(bc > 1e-12, bp/bc, 0));
    printf("%7s L=%2d t=%.3f P/R=%7.1fx P/C=%7.1fx\n", modes[mi+1], lam, bt, bpe, pc)
  );
  print("")
);

print("=== EXP 3 (partial): RESIDUE VOTING ===");
\\ For each n, count coprime residues across moduli
my(moduli = [2,3,5,6,7,11,13,30]);
my(scores = vector(N));
for(n = 2, N,
  my(s = 0);
  for(j = 1, #moduli, if(gcd(n, moduli[j]) == 1, s++));
  scores[n] = s
);
\\ Sort and check precision
my(idx = vecsort(vector(N-1, i, [scores[i+1], i+1]), , 4));  \\ descending
for(ki = 1, 5,
  my(k = [50,100,168,200,300][ki]);
  my(pcount = 0);
  for(j = 1, min(k, #idx),
    if(isprime(idx[j][2]), pcount++)
  );
  printf("  Top %3d: %3d primes (precision=%.3f)\n", k, pcount, pcount*1.0/k)
);

print("");
print("=== N-STABILITY: best modes across N ===");
for(ni = 1, 3,
  my(N2 = [500, 2000, 5000][ni]);
  my(pr2 = select(isprime, vector(N2-1, i, i+1)));
  my(co2 = select(n -> !isprime(n) && n > 3, vector(N2-1, i, i+1)));
  \\ harmonic mean, lam=6
  my(bt=0, bpc=0);
  for(ti = 5, 200,
    my(t = ti/250.0);
    my(bp = bs(pr2, N2, t, 6, 2));
    my(bc = bs(co2, N2, t, 6, 2));
    my(pc = if(bc > 1e-12, bp/bc, 0));
    if(pc > bpc && pc < 1e8, bpc = pc; bt = t)
  );
  printf("N=%5d harm L=6: t=%.3f P/C=%.1fx (#P=%d)\n", N2, bt, bpc, #pr2);
  \\ geometric, lam=6
  bt=0; bpc=0;
  for(ti = 5, 200,
    my(t = ti/250.0);
    my(bp = bs(pr2, N2, t, 6, 0));
    my(bc = bs(co2, N2, t, 6, 0));
    my(pc = if(bc > 1e-12, bp/bc, 0));
    if(pc > bpc && pc < 1e8, bpc = pc; bt = t)
  );
  printf("N=%5d geo  L=6: t=%.3f P/C=%.1fx\n", N2, bt, bpc);
  \\ repulsive, lam=6
  bt=0; bpc=0;
  for(ti = 1, 80,
    my(t = ti/1000.0);
    my(bp = bs(pr2, N2, t, 6, 4));
    my(bc = bs(co2, N2, t, 6, 4));
    my(pc = if(bc > 1e-12, bp/bc, 0));
    if(pc > bpc && pc < 1e8, bpc = pc; bt = t)
  );
  printf("N=%5d rep  L=6: t=%.3f P/C=%.1fx\n", N2, bt, bpc)
);
