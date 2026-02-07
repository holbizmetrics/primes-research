\\ Multi-N cancellation test
z=lfunzeros(lfuncreate(1),100);
K=nfinit(x^3-2);
L=lfuncreate(K);
d=lfunzeros(L,100);

print("N\tVar(zeta)\tVar(Ded)\tRatio");

{for(logN=2,5,
  N=10^logN;
  sz=0.0;sz2=0.0;
  for(i=1,100,x=2+(i-1)*(N-2)/99;v=0.0;for(j=1,min(#z,25),g=z[j];v+=-2*sqrt(x)/sqrt(0.25+g^2)*cos(g*log(x)));sz+=v;sz2+=v^2);
  vz=(sz2-sz^2/100)/100;
  sd=0.0;sd2=0.0;
  for(i=1,100,x=2+(i-1)*(N-2)/99;v=0.0;for(j=1,min(#d,25),g=d[j];v+=-2*sqrt(x)/sqrt(0.25+g^2)*cos(g*log(x)));sd+=v;sd2+=v^2);
  vd=(sd2-sd^2/100)/100;
  printf("10^%d\t%.2f\t\t%.2f\t\t%.2f\n",logN,vz,vd,vd/vz);
)}
