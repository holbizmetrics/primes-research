best = 6;
forprime(p = 10^9, 10^9 + 10^6,
  pr = [p];
  for(i = 1, 15, pr = concat(pr, nextprime(pr[#pr] + 1)));
  g = vector(#pr - 1, i, pr[i+1] - pr[i]);
  d = g[2] - g[1];
  if(d,
    len = 1;
    for(j = 2, #g - 1, if(g[j+1] - g[j] == d, len++, break));
    if(len > best,
      best = len;
      print("NEW: len ", len+1, " at p=", p, ": ", vector(len+1, k, g[k]))
    )
  )
);
print("Best found: ", best + 1);
