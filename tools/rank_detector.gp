\\ BSD Rank Detector v2
\\ Predicts elliptic curve rank (0 vs ≥1) from L-function zeros
\\
\\ Two methods:
\\   1. First zero position (z[1] ≈ 0 means rank ≥ 1) - MORE RELIABLE
\\   2. Spacing variance (higher variance suggests rank ≥ 1) - STATISTICAL
\\
\\ Usage:
\\   gp rank_detector.gp
\\   ? rank_test([0,-1,1,-10,-20])  \\ 11a1

\\ Spacing variance
spacing_var(z) = {
  my(s, m);
  if(#z < 5, return(-1));
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  vecsum(vector(#s, i, (s[i]/m - 1)^2)) / #s
}

\\ Main test function
rank_test(coeffs, height=60) = {
  my(E, cond, actual, z, v, pred1, pred2);

  E = ellinit(coeffs);
  if(E == 0, print("Invalid curve"); return);

  cond = ellglobalred(E)[1];
  actual = ellrank(E)[1];
  z = lfunzeros(lfuncreate(E), height);

  print("Curve: ", coeffs);
  print("Conductor: ", cond);
  print("Actual rank: ", actual);
  print("Zeros: ", #z);
  print("");

  \\ Method 1: First zero position
  print("Method 1 - First zero position:");
  printf("  z[1] = %.4f\n", z[1]);
  if(z[1] < 0.5,
    pred1 = 1;
    print("  => Central zero detected => RANK >= 1")
  ,
    pred1 = 0;
    print("  => No central zero => RANK = 0")
  );

  \\ Method 2: Spacing variance
  print("Method 2 - Spacing variance:");
  v = spacing_var(z);
  printf("  variance = %.4f\n", v);
  if(v < 0.27,
    pred2 = 0;
    print("  => Low variance => suggests RANK = 0")
  ,
    pred2 = 1;
    print("  => High variance => suggests RANK >= 1")
  );

  print("");
  print("Predictions:");
  printf("  Method 1 (first zero): rank %s\n", if(pred1==0,"= 0",">= 1"));
  printf("  Method 2 (variance):   rank %s\n", if(pred2==0,"= 0",">= 1"));
  print("");

  \\ Final verdict (Method 1 is more reliable)
  if((pred1 == 0 && actual == 0) || (pred1 >= 1 && actual >= 1),
    print("VERDICT: CORRECT (using Method 1)")
  ,
    print("VERDICT: INCORRECT")
  );

  [actual, pred1, pred2, z[1], v]
}

\\ Batch test
batch_test() = {
  my(curves, c1, c2);

  curves = [
    [[0,-1,1,-10,-20], 0, "11a1"],
    [[1,-1,1,-1,0], 0, "17a1"],
    [[0,0,0,-1,0], 0, "32a1"],
    [[0,0,1,-1,0], 1, "37a1"],
    [[1,0,0,-1,0], 1, "65a1"],
    [[0,1,1,-2,0], 2, "389a1"],
    [[0,1,0,-1,1], 1, "cond704"]
  ];

  print("==================================================");
  print("BSD RANK DETECTOR v2 - Validation");
  print("==================================================");
  print("");
  print("Curve     Rank  z[1]    Var     M1  M2");
  print("--------------------------------------------------");

  c1 = 0; c2 = 0;

  for(i = 1, #curves,
    my(E, rank, z, v, p1, p2, label);
    E = ellinit(curves[i][1]);
    if(E == 0, next);

    rank = curves[i][2];
    label = curves[i][3];
    z = lfunzeros(lfuncreate(E), 60);
    v = spacing_var(z);

    p1 = if(z[1] < 0.5, 1, 0);
    p2 = if(v < 0.27, 0, 1);

    if((p1 == 0 && rank == 0) || (p1 >= 1 && rank >= 1), c1++);
    if((p2 == 0 && rank == 0) || (p2 >= 1 && rank >= 1), c2++);

    printf("%-9s %d     %.3f   %.3f   %s   %s\n",
      label, rank, z[1], v,
      if((p1==0 && rank==0)||(p1>=1 && rank>=1), "OK", "X"),
      if((p2==0 && rank==0)||(p2>=1 && rank>=1), "OK", "X"))
  );

  print("--------------------------------------------------");
  printf("Method 1 (first zero): %d/%d correct\n", c1, #curves);
  printf("Method 2 (variance):   %d/%d correct\n", c2, #curves);
  print("");
  print("Method 1 is primary (detects central zero directly)");
  print("Method 2 is supplementary (statistical pattern)");
}

print("BSD Rank Detector v2 loaded.");
print("  rank_test([a1,a2,a3,a4,a6]) - test single curve");
print("  batch_test() - run validation");
print("");
batch_test()
