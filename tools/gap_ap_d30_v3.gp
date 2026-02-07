\\ Gap AP search for d=30 - minimal memory version

{
  my(target_d, min_len, maxprime, g1, g2, g3, g4, g5, prev, p2, p3, p4, p5, cnt, found);

  target_d = 30;
  min_len = 5;
  maxprime = prime(10^7);  \\ 10 millionth prime

  print("Gap AP Search: d=30");
  print("Searching primes up to ", maxprime);
  print("Looking for L5+ with |d|=30");
  print();

  g1=0; g2=0; g3=0; g4=0; g5=0;
  prev=2; p2=0; p3=0; p4=0; p5=0;
  cnt=0; found=0;

  forprime(p = 3, maxprime,
    \\ Shift gaps
    g5=g4; g4=g3; g3=g2; g2=g1;
    g1 = p - prev;

    \\ Shift primes for reporting
    p5=p4; p4=p3; p3=p2; p2=prev;

    cnt++;
    if(cnt % 10^6 == 0, print("  checked ", cnt, " primes..."));

    \\ Check L5 ascending: g2-g1=g3-g2=g4-g3=g5-g4=target_d
    if(g5 > 0,
      if(g2-g1==target_d && g3-g2==target_d && g4-g3==target_d && g5-g4==target_d,
        found++;
        print("FOUND L5 (d=+30) at p=", p5);
        print("  gaps: [", g1, ", ", g2, ", ", g3, ", ", g4, ", ", g5, "]");
        print("  p mod 30 = ", p5 % 30);
        print();
      );
      \\ Check L5 descending
      if(g2-g1==-target_d && g3-g2==-target_d && g4-g3==-target_d && g5-g4==-target_d,
        found++;
        print("FOUND L5 (d=-30) at p=", p5);
        print("  gaps: [", g1, ", ", g2, ", ", g3, ", ", g4, ", ", g5, "]");
        print("  p mod 30 = ", p5 % 30);
        print();
      );
    );

    prev = p;
  );

  print();
  print("Total L5+ gap APs with |d|=30: ", found);
  print("Primes checked: ", cnt);
}
