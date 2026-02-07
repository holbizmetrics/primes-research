/* Search for length 12 gap AP */
/* Record: length 11 at 245333213 with gaps [20,18,16,14,12,10,8,6,4,2] */

is_ap(v) = {
  if(#v < 2, return(0));
  d = v[2] - v[1];
  for(i=2, #v-1, if(v[i+1]-v[i] != d, return(0)));
  return(1)
}

check_gap_ap(p, len) = {
  primes = vector(len);
  primes[1] = p;
  for(i=2, len, primes[i] = nextprime(primes[i-1]+1));
  gaps = vector(len-1, i, primes[i+1] - primes[i]);
  return(is_ap(gaps))
}

print("Searching for length 12 gap AP starting from 10^10...")
print("This may take a long time.")

found = 0
p = nextprime(10^10)
ct = 0
while(found < 1 && ct < 10^7,
  ct = ct + 1;
  if(ct % 10^6 == 0, print("Checked ", ct, " primes, at p=", p));
  if(check_gap_ap(p, 12),
    found = found + 1;
    print("FOUND length 12 at p=", p);
    primes = vector(12);
    primes[1] = p;
    for(i=2, 12, primes[i] = nextprime(primes[i-1]+1));
    gaps = vector(11, i, primes[i+1] - primes[i]);
    print("Gaps: ", gaps);
  );
  p = nextprime(p+1)
)

print("Search complete. Found: ", found)
quit
