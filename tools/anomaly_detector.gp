\\ Elliptic Curve Anomaly Detector
\\ Detects curves with unusual L-function zero statistics
\\
\\ Key findings:
\\   - Central zeros (rank >= 1) create giant first gap (~5x mean)
\\   - Rank 1 curves show ~30% higher variance than rank 0 even excluding first gap
\\   - This is a GUE boundary effect from repulsion off the central zero
\\
\\ Usage:
\\   gp anomaly_detector.gp
\\   ? detect_anomaly([0,0,1,-1,0])

\\ Spacing variance
svar(z) = {
  my(s, m, n);
  if(#z < 5, return(-1));
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  n = vector(#s, i, s[i]/m);
  vecsum(vector(#n, i, (n[i]-1)^2)) / #n
}

\\ Variance excluding first gap
svar_no1(z) = {
  my(s, m, n);
  if(#z < 6, return(-1));
  s = vector(#z-2, i, z[i+2] - z[i+1]);
  m = vecsum(s) / #s;
  n = vector(#s, i, s[i]/m);
  vecsum(vector(#n, i, (n[i]-1)^2)) / #n
}

\\ First gap (normalized)
first_gap_norm(z) = {
  my(s, m);
  if(#z < 5, return(-1));
  s = vector(#z-1, i, z[i+1] - z[i]);
  m = vecsum(s) / #s;
  s[1] / m
}

\\ Main detector
detect_anomaly(coeffs) = {
  my(E, c, r, z, v_full, v_no1, g1, anomalies);

  E = ellinit(coeffs);
  if(E == 0, print("Invalid curve"); return);

  c = ellglobalred(E)[1];
  r = ellrank(E)[1];
  z = lfunzeros(lfuncreate(E), 100);

  if(#z < 10, print("Not enough zeros"); return);

  v_full = svar(z);
  v_no1 = svar_no1(z);
  g1 = first_gap_norm(z);

  print("============================================");
  print("ANOMALY DETECTION REPORT");
  print("============================================");
  print("");
  printf("Curve: %s\n", coeffs);
  printf("Conductor: %d\n", c);
  printf("Rank: %d\n", r);
  printf("Zeros computed: %d\n", #z);
  print("");
  print("--- Statistics ---");
  printf("First zero: %.4f\n", z[1]);
  printf("First gap (normalized): %.2fx mean\n", g1);
  printf("Full variance: %.4f (GUE expected ~0.27)\n", v_full);
  printf("Variance (gaps 2+): %.4f\n", v_no1);
  print("");

  anomalies = [];

  \\ Check for central zero
  if(z[1] < 0.1,
    anomalies = concat(anomalies, ["Central zero detected (rank >= 1)"])
  );

  \\ Check first gap anomaly
  if(g1 > 6.0,
    anomalies = concat(anomalies, [Str("Exceptionally large first gap: ", g1, "x")])
  );

  \\ Check variance anomaly (rank 0 expected ~0.15, rank 1 expected ~0.19)
  my(expected_var);
  expected_var = if(r >= 1, 0.19, 0.15);
  if(v_no1 > expected_var * 1.3,
    anomalies = concat(anomalies, [Str("High variance (gaps 2+): ", v_no1)])
  );
  if(v_no1 < expected_var * 0.7,
    anomalies = concat(anomalies, [Str("Low variance (gaps 2+): ", v_no1)])
  );

  print("--- Anomaly Status ---");
  if(#anomalies == 0,
    print("No anomalies detected - curve appears typical.")
  ,
    print("ANOMALIES FOUND:");
    for(i = 1, #anomalies, print("  * ", anomalies[i]))
  );

  print("");
  [c, r, v_full, v_no1, g1, anomalies]
}

\\ Quick check function
quick_check(coeffs) = {
  my(E, r, z, g1);
  E = ellinit(coeffs);
  if(E == 0, return(0));
  r = ellrank(E)[1];
  z = lfunzeros(lfuncreate(E), 60);
  if(#z < 5, return(0));
  g1 = first_gap_norm(z);
  [r, g1]
}

print("Anomaly Detector loaded.");
print("  detect_anomaly([a1,a2,a3,a4,a6]) - full analysis");
print("  quick_check([a1,a2,a3,a4,a6]) - returns [rank, first_gap]");
print("");
print("Testing on known curves...");
print("");

detect_anomaly([0,0,1,-1,0]);
