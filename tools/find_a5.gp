/* Find A5 polynomial */
print("Searching for A5 quintic...")
ct=0
for(a=-20,20,
  for(b=-20,20,
    if(ct<3,
      p=x^5+a*x+b;
      if(polisirreducible(p),
        g=polgalois(p);
        if(g[1]==60,
          ct=ct+1;
          print(ct,": ",p," Galois=",g[4])
        )
      )
    )
  )
)
print("Found ",ct," A5 polynomials")
quit
