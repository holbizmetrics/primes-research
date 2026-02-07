/* Test elliptic curve L-function variance by rank */
svar(z)={my(s,m,n);if(#z<5,return(-1));s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}

print("=== EC Rank-Variance Test ===")
print("")

/* Rank 0 curves */
print("RANK 0:")
curves0 = [[0,-1,1,-10,-20], [1,-1,1,-1,0], [0,0,0,-1,0], [0,1,1,0,0], [1,0,1,1,0]]
vars0 = []
for(i=1,#curves0,
  E = ellinit(curves0[i]);
  L = lfuncreate(E);
  val = lfun(L, 1);
  if(abs(val) > 0.01,
    z = lfunzeros(L, 60);
    if(#z > 5,
      v = svar(z);
      vars0 = concat(vars0, [v]);
      print(curves0[i], " L(1)=", val, " var=", v)
    )
  )
)
print("Rank 0 mean: ", if(#vars0>0, vecsum(vars0)/#vars0, "N/A"))

print("")
print("RANK 1+:")
/* Rank 1+ curves (L(1) = 0) */
curves1 = [[0,0,1,-1,0], [1,0,0,-1,0], [0,1,1,-2,0], [1,-1,0,-1,0], [0,0,1,0,-1]]
vars1 = []
for(i=1,#curves1,
  E = ellinit(curves1[i]);
  L = lfuncreate(E);
  val = lfun(L, 1);
  if(abs(val) < 0.01,
    z = lfunzeros(L, 60);
    if(#z > 5,
      v = svar(z);
      vars1 = concat(vars1, [v]);
      print(curves1[i], " L(1)=", val, " var=", v)
    )
  )
)
print("Rank 1+ mean: ", if(#vars1>0, vecsum(vars1)/#vars1, "N/A"))

print("")
print("Ratio (rank1/rank0): ", if(#vars0>0 && #vars1>0, (vecsum(vars1)/#vars1)/(vecsum(vars0)/#vars0), "N/A"))
quit
