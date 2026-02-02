\\ BSD Rank Detector
\\ Predicts elliptic curve rank (0 vs ≥1) from L-function zeros
\\
\\ Method: Central zero detection
\\   z[1] ≈ 0 means rank ≥ 1 (L(E,1) = 0)
\\   z[1] > 1 means rank = 0 (L(E,1) ≠ 0)
\\
\\ Note: Spacing variance was tested but found to correlate with
\\ CONDUCTOR, not rank. See Miller (2006) arXiv:math/0508150.
\\
\\ Usage:
\\   gp rank_detector.gp
\\   ? rank_test([0,-1,1,-10,-20])  \\ test curve 11a1

\\ Main test function
rank_test(coeffs, height=60) = {
  my(E, cond, actual, z, pred);

  E = ellinit(coeffs);
  if(E == 0, print("Invalid curve"); return);

  cond = ellglobalred(E)[1];
  actual = ellrank(E)[1];
  z = lfunzeros(lfuncreate(E), height);

  print("Curve: ", coeffs);
  print("Conductor: ", cond);
  print("Actual rank: ", actual);
  print("Zeros computed: ", #z);
  printf("First zero: %.4f\n", z[1]);
  print("");

  if(z[1] < 0.5,
    pred = 1;
    print("Central zero detected at s=1 => RANK >= 1")
  ,
    pred = 0;
    print("No central zero => RANK = 0")
  );

  print("");
  if((pred == 0 && actual == 0) || (pred >= 1 && actual >= 1),
    print("CORRECT")
  ,
    print("INCORRECT")
  );

  [actual, pred, z[1]]
}

\\ Batch test
batch_test() = {
  my(curves, correct, total);

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
  print("BSD RANK DETECTOR - Validation");
  print("==================================================");
  print("");
  print("Curve     Rank  z[1]      Pred  Status");
  print("--------------------------------------------------");

  correct = 0;
  total = 0;

  for(i = 1, #curves,
    my(E, rank, z, pred, status, label);
    E = ellinit(curves[i][1]);
    if(E == 0, next);

    rank = curves[i][2];
    label = curves[i][3];
    z = lfunzeros(lfuncreate(E), 60);

    pred = if(z[1] < 0.5, 1, 0);

    if((pred == 0 && rank == 0) || (pred >= 1 && rank >= 1),
      status = "OK";
      correct++
    ,
      status = "FAIL"
    );
    total++;

    printf("%-9s %d     %.4f    %d     %s\n", label, rank, z[1], pred, status)
  );

  print("--------------------------------------------------");
  printf("Accuracy: %d/%d\n", correct, total);
  print("");
  print("Method: z[1] < 0.5 => rank >= 1 (central zero)");
  print("        z[1] > 0.5 => rank = 0 (no central zero)");
}

print("BSD Rank Detector loaded.");
print("  rank_test([a1,a2,a3,a4,a6]) - test single curve");
print("  batch_test() - run validation");
print("");
batch_test()
