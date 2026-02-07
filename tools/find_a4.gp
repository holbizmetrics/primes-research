/* Find A4 polynomials */
ct=0
for(a=1,100, for(b=1,100, if(ct<10, p=x^4+a*x+b; if(polisirreducible(p), g=polgalois(p); if(g[4]=="A4", ct=ct+1; print(ct,": x^4+",a,"x+",b))))))
quit
