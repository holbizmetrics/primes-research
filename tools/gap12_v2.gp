print("Gap AP 12 search from 10^9")
chk(p)={local(v,g,d,ok); v=vector(12); v[1]=p; for(i=2,12,v[i]=nextprime(v[i-1]+1)); g=vector(11,i,v[i+1]-v[i]); d=g[2]-g[1]; ok=1; for(i=2,10,if(g[i+1]-g[i]!=d,ok=0)); ok}
p=nextprime(10^9); found=0; for(i=1,500000, if(chk(p), found=found+1; print("FOUND at p=",p)); p=nextprime(p+1); if(i%100000==0,print("Checked ",i)))
print("Done. Found=",found)
quit
