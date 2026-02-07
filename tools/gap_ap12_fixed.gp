/* Gap AP length 12 search - fixed syntax */
print("Gap AP length 12 search")
print("Starting from 10^9")

found=0
p=nextprime(10^9)
ct=0

/* Check if gaps form AP */
check(p,len)={
  local(primes,gaps,d,ok);
  primes=vector(len);
  primes[1]=p;
  for(i=2,len,primes[i]=nextprime(primes[i-1]+1));
  gaps=vector(len-1,i,primes[i+1]-primes[i]);
  d=gaps[2]-gaps[1];
  ok=1;
  for(i=2,#gaps-1,if(gaps[i+1]-gaps[i]!=d,ok=0));
  if(ok,print("FOUND at ",p,": gaps=",gaps));
  ok
}

/* Search */
for(i=1,10^6,
  if(check(p,12),found=found+1);
  p=nextprime(p+1);
  if(i%100000==0,print("Checked ",i," primes, at p=",p))
)

print("Done. Found: ",found)
quit
