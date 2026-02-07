print("Gap AP 12 extended search from 2×10^11")
chk(p)={local(v,g,d,ok); v=vector(12); v[1]=p; for(i=2,12,v[i]=nextprime(v[i-1]+1)); g=vector(11,i,v[i+1]-v[i]); d=g[2]-g[1]; ok=1; for(i=2,10,if(g[i+1]-g[i]!=d,ok=0)); if(ok,print("FOUND p=",p," gaps=",g)); ok}
p=nextprime(2*10^11); for(i=1,5000000, chk(p); p=nextprime(p+1); if(i%1000000==0,print("Checked ",i," at p=",p)))
print("Done")
quit
