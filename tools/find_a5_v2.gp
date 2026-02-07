print("A5 search"); ct=0; for(a=-20,20, for(b=-20,20, p=x^5+a*x+b; if(polisirreducible(p), g=polgalois(p); if(g[1]==60, ct=ct+1; print(p," -> ",g[4]))))); print("Found: ",ct); quit
