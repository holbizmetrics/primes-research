\\ Anomaly Scanner for Elliptic Curves
\\ Finds curves with unusual L-function zero statistics
\\
\\ Usage: gp anomaly_scan.gp

\\ Spacing variance
svar(z) = {
  my(s, m, n);
  if(#z < 5, return(-1));
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  n = vector(#s, i, s[i]/m);
  vecsum(vector(#n, i, (n[i]-1)^2)) / #n
}

\\ Skewness of spacings
sskew(z) = {
  my(s, m, std, n);
  if(#z < 5, return(0));
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  n = vector(#s, i, s[i]/m);
  std = sqrt(vecsum(vector(#n, i, (n[i]-1)^2)) / #n);
  if(std < 0.001, return(0));
  vecsum(vector(#n, i, ((n[i]-1)/std)^3)) / #n
}

\\ Scan a single curve
scan_curve(coeffs, label) = {
  my(E, c, r, z, v, sk, z1);
  E = ellinit(coeffs);
  if(E == 0, return(0));
  c = ellglobalred(E)[1];
  r = ellrank(E)[1];
  z = lfunzeros(lfuncreate(E), 80);
  if(#z < 5, return(0));
  v = svar(z);
  sk = sskew(z);
  z1 = z[1];
  [label, c, r, z1, v, sk, #z]
}

\\ Main scan
anomaly_scan() = {
  my(results, vars, skews, mean_v, std_v, mean_sk, std_sk);

  print("============================================================");
  print("ANOMALY SCANNER: Elliptic Curve Zero Statistics");
  print("============================================================");
  print("");

  \\ Test set: various curve types
  results = [];

  \\ Small conductors
  results = concat(results, [scan_curve([0,-1,1,-10,-20], "11a1")]);
  results = concat(results, [scan_curve([0,0,1,0,0], "19a1")]);
  results = concat(results, [scan_curve([0,0,0,0,1], "27a1")]);
  results = concat(results, [scan_curve([0,0,0,-1,0], "32a1")]);
  results = concat(results, [scan_curve([0,0,1,-1,0], "37a1")]);
  results = concat(results, [scan_curve([1,0,1,-2,-1], "46a1")]);
  results = concat(results, [scan_curve([1,-1,0,-1,0], "52a1")]);

  \\ Medium conductors
  results = concat(results, [scan_curve([0,0,1,-7,6], "91b1")]);
  results = concat(results, [scan_curve([1,1,0,-10,-10], "120a1")]);
  results = concat(results, [scan_curve([0,1,1,-2,0], "389a1")]);

  \\ Larger conductors
  results = concat(results, [scan_curve([0,1,0,-1,1], "704h1")]);
  results = concat(results, [scan_curve([1,0,0,-1,0], "65a1")]);
  results = concat(results, [scan_curve([0,0,1,1,0], "43a1")]);

  print("Curve      Cond    Rank  z[1]     Var      Skew     #zeros");
  print("------------------------------------------------------------");

  for(i = 1, #results,
    if(results[i] != 0,
      printf("%-10s %6d  %d     %7.4f  %7.4f  %7.4f  %d\n",
        results[i][1], results[i][2], results[i][3],
        results[i][4], results[i][5], results[i][6], results[i][7])
    )
  );

  \\ Filter valid results
  results = select(x -> x != 0, results);

  print("");
  print("=== STATISTICAL ANALYSIS ===");

  vars = vector(#results, i, results[i][5]);
  skews = vector(#results, i, results[i][6]);

  mean_v = vecsum(vars) / #vars;
  std_v = sqrt(vecsum(vector(#vars, i, (vars[i] - mean_v)^2)) / #vars);
  mean_sk = vecsum(skews) / #skews;
  std_sk = sqrt(vecsum(vector(#skews, i, (skews[i] - mean_sk)^2)) / #skews);

  printf("Variance:  mean=%.4f, std=%.4f (GUE expected ~0.27)\n", mean_v, std_v);
  printf("Skewness:  mean=%.4f, std=%.4f (GUE expected ~0.35)\n", mean_sk, std_sk);

  print("");
  print("=== ANOMALIES (>1.5 std from mean) ===");

  my(found);
  found = 0;
  for(i = 1, #results,
    my(v_score, sk_score, anomaly);
    v_score = if(std_v > 0.001, abs(results[i][5] - mean_v) / std_v, 0);
    sk_score = if(std_sk > 0.001, abs(results[i][6] - mean_sk) / std_sk, 0);
    anomaly = "";
    if(v_score > 1.5, anomaly = concat(anomaly, Str(" var=", v_score)));
    if(sk_score > 1.5, anomaly = concat(anomaly, Str(" skew=", sk_score)));
    if(anomaly != "",
      printf("%s (cond=%d, rank=%d): %s\n", results[i][1], results[i][2], results[i][3], anomaly);
      found++
    )
  );
  if(found == 0, print("  None detected in this sample."));

  print("");
  results
}

print("Anomaly Scanner loaded.");
print("  anomaly_scan() - run full scan");
print("  scan_curve([a1,a2,a3,a4,a6], \"label\") - test single curve");
print("");
anomaly_scan()
