\\ Gap AP search for d=30 - streaming version (low memory)
\\ Prediction: d=30 gap APs appear around 10^7 primes

allocatemem(256*10^6);  \\ 256MB stack

{
gap_ap_stream(maxN, target_d, min_len) =
  my(p, prev, gaps, window, found, g, L, ok);

  print("Streaming search through ", maxN, " primes...");
  print("Looking for L", min_len, "+ gap APs with |d|=", target_d);
  print();

  \\ Use a sliding window approach
  window = min_len + 5;  \\ keep last few gaps
  gaps = vector(window);
  found = 0;

  p = 2; prev = 2;
  forprime(q = 3, prime(maxN),
    g = q - prev;

    \\ Shift window
    for(i = 1, window-1, gaps[i] = gaps[i+1]);
    gaps[window] = g;

    \\ Check for AP in last min_len gaps (ascending d)
    if(gaps[window - min_len + 1] > 0,
      L = 1;
      ok = 1;
      for(j = 1, min_len - 1,
        if(gaps[window - min_len + 1 + j] - gaps[window - min_len + j] != target_d,
          ok = 0; break
        );
        L++;
      );
      if(ok && L >= min_len,
        found++;
        print("FOUND L", L, " (ascending d=", target_d, ") ending at p=", q);
        print("  gaps: ", vector(min_len, k, gaps[window - min_len + k]));
        print("  end prime mod 30 = ", q % 30);
        print();
      );

      \\ Check descending d
      L = 1;
      ok = 1;
      for(j = 1, min_len - 1,
        if(gaps[window - min_len + 1 + j] - gaps[window - min_len + j] != -target_d,
          ok = 0; break
        );
        L++;
      );
      if(ok && L >= min_len,
        found++;
        print("FOUND L", L, " (descending d=-", target_d, ") ending at p=", q);
        print("  gaps: ", vector(min_len, k, gaps[window - min_len + k]));
        print("  end prime mod 30 = ", q % 30);
        print();
      );
    );

    prev = q;
  );

  print("Search complete. Found: ", found);
  found;
}

print("=== Gap AP Search: d=30 (Primorial Hierarchy Test) ===");
print();

\\ Run search
print("Searching 10^7 primes for L5+ gap APs with d=30...");
gap_ap_stream(10^7, 30, 5);

print();
print("Now searching for L4...");
gap_ap_stream(10^7, 30, 4);

print();
print("=== Done ===");
