\\ Gap AP search for d=30 (primorial hierarchy test)
\\ Prediction: d=30 gap APs appear around 10^7 primes

{
gap_ap_search(N, target_d, min_len) =
  my(p, gaps, n, found, start_p, L, g0, ok, seq);

  print("Generating first ", N, " primes...");
  p = primes(N);
  print("Done. Largest prime: ", p[N]);

  \\ Compute gaps
  gaps = vector(N-1, i, p[i+1] - p[i]);

  found = 0;

  \\ Search for APs in gaps with difference +d or -d
  for(d = 1, 1,  \\ just do positive, check both directions
    for(i = 1, N - min_len,
      \\ Check ascending AP (gaps increase by target_d)
      g0 = gaps[i];
      L = 1;
      for(j = i+1, N-1,
        if(gaps[j] == g0 + (j-i)*target_d,
          L++,
          break
        )
      );
      if(L >= min_len,
        found++;
        seq = vector(L, k, gaps[i+k-1]);
        print("FOUND L", L, " at p=", p[i], " (index ", i, ")");
        print("  gaps: ", seq);
        print("  p mod 30 = ", p[i] % 30);
        print("  p mod 6 = ", p[i] % 6);
        print("  primes mod 30: ", vector(L+1, k, p[i+k-1] % 30));
        print();
      );

      \\ Check descending AP (gaps decrease by target_d)
      L = 1;
      for(j = i+1, N-1,
        if(gaps[j] == g0 - (j-i)*target_d,
          L++,
          break
        )
      );
      if(L >= min_len,
        found++;
        seq = vector(L, k, gaps[i+k-1]);
        print("FOUND L", L, " at p=", p[i], " (index ", i, "), d=-", target_d);
        print("  gaps: ", seq);
        print("  p mod 30 = ", p[i] % 30);
        print("  p mod 6 = ", p[i] % 6);
        print("  primes mod 30: ", vector(L+1, k, p[i+k-1] % 30));
        print();
      );
    )
  );

  print("Total L", min_len, "+ gap APs with |d|=", target_d, ": ", found);
  found;
}

print("=== Gap AP Search: d=30 ===");
print("Testing primorial hierarchy prediction");
print();

\\ Stage 1: 10^6 primes
print("--- Stage 1: 10^6 primes ---");
gap_ap_search(10^6, 30, 5);
print();

\\ Stage 2: 10^7 primes (the prediction threshold)
print("--- Stage 2: 10^7 primes ---");
gap_ap_search(10^7, 30, 5);
print();

\\ If nothing found, try L4
print("--- Fallback: L4 search in 10^7 primes ---");
gap_ap_search(10^7, 30, 4);

print();
print("=== Search complete ===");
