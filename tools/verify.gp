\\ Dedekind Zero Verifier (PARI/GP)
\\ Computes variance and compares to prediction based on Galois structure

\\ Variance function
v(z)={my(s,m,n);if(#z<3,return(-1));s=vector(#z-1,i,z[i+1]-z[i]);m=vecsum(s)/#s;n=vector(#s,i,s[i]/m);vecsum(vector(#n,i,(n[i]-1)^2))/#n}

\\ Predictions based on our theory:
\\ - Abelian (2 factors): var ~ 0.31 (34% correlation)
\\ - Non-abelian with induction (2 factors): var ~ 0.28 (45% correlation)
\\ - 4 factors: var ~ 0.40-0.55

print("============================================================");
print("DEDEKIND ZERO VERIFIER");
print("============================================================");
print("");
print("Field            | Predicted | Measured | Status");
print("-----------------+-----------+----------+--------");

\\ Q(√2) - abelian, 2 factors
K=nfinit(x^2-2);z=lfunzeros(lfuncreate(K),50);
pred=0.31; meas=v(z); diff=abs(meas-pred)/pred;
status=if(diff<0.15,"PASS","FAIL");
printf("Q(sqrt2)  n=%-3d  |   %.3f   |  %.3f   | %s\n",#z,pred,meas,status);

\\ Q(√3) - abelian, 2 factors
K=nfinit(x^2-3);z=lfunzeros(lfuncreate(K),50);
pred=0.31; meas=v(z); diff=abs(meas-pred)/pred;
status=if(diff<0.15,"PASS","FAIL");
printf("Q(sqrt3)  n=%-3d  |   %.3f   |  %.3f   | %s\n",#z,pred,meas,status);

\\ Q(√5) - abelian, 2 factors
K=nfinit(x^2-5);z=lfunzeros(lfuncreate(K),50);
pred=0.31; meas=v(z); diff=abs(meas-pred)/pred;
status=if(diff<0.15,"PASS","FAIL");
printf("Q(sqrt5)  n=%-3d  |   %.3f   |  %.3f   | %s\n",#z,pred,meas,status);

\\ Q(∛2) - S3, 2 factors with induction coupling
K=nfinit(x^3-2);z=lfunzeros(lfuncreate(K),50);
pred=0.27; meas=v(z); diff=abs(meas-pred)/pred;
status=if(diff<0.15,"PASS","FAIL");
printf("Q(cbrt2)  n=%-3d  |   %.3f   |  %.3f   | %s (S3 induction)\n",#z,pred,meas,status);

\\ Q(∛3) - S3, 2 factors with induction coupling
K=nfinit(x^3-3);z=lfunzeros(lfuncreate(K),50);
pred=0.27; meas=v(z); diff=abs(meas-pred)/pred;
status=if(diff<0.15,"PASS","FAIL");
printf("Q(cbrt3)  n=%-3d  |   %.3f   |  %.3f   | %s (S3 induction)\n",#z,pred,meas,status);

\\ Q(∜2) - D4, 4 factors
K=nfinit(x^4-2);z=lfunzeros(lfuncreate(K),50);
pred=0.50; meas=v(z); diff=abs(meas-pred)/pred;
status=if(diff<0.20,"PASS","FAIL");
printf("Q(4thrt2) n=%-3d  |   %.3f   |  %.3f   | %s (D4, 4 factors)\n",#z,pred,meas,status);

print("");
print("============================================================");
print("Theory: Galois induction coupling reduces variance");
print("  Abelian (no coupling):     predicted ~ 0.31");
print("  Non-abelian (S3 coupling): predicted ~ 0.27");
print("  4+ factors:                predicted ~ 0.50");
print("============================================================");

quit
