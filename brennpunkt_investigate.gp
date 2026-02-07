\\ Brennpunkt investigation - which metric gives 1/4?
{
N = 500;
GA = 2*Pi/(((1+sqrt(5))/2)^2);
R = 0.5;

\\ Build prime and composite vectors
pv = List(); cv = List();
for(n=2, N, if(isprime(n), listput(pv, n), if(n>3, listput(cv, n))));
pv = Vec(pv); cv = Vec(cv);
np = #pv; nc = #cv;
print("Primes: ", np, " Composites: ", nc);

\\ 3D spread
sp3d(v, nn, t) = my(cx=0,cy=0,cz=0,pts=vector(nn,j,my(n=v[j],ro=max(n/N,1e-10),rt=ro^(1-2*t)*R^(2*t),zu=max(-1,min(1,1-2.0*n/N)),rxy=sqrt(max(0,1-zu^2)),th=GA*n);[rt*rxy*cos(th),rt*rxy*sin(th),rt*zu])); for(j=1,nn,cx+=pts[j][1];cy+=pts[j][2];cz+=pts[j][3]); cx/=nn;cy/=nn;cz/=nn; my(v2=0); for(j=1,nn,v2+=(pts[j][1]-cx)^2+(pts[j][2]-cy)^2+(pts[j][3]-cz)^2); sqrt(v2/nn);

\\ Backscatter
bsc(v, nn, t, lam) = my(k=2*Pi*lam,ar=0.0,ai=0.0); for(j=1,nn, my(n=v[j],ro=max(n/N,1e-10),rt=ro^(1-2*t)*R^(2*t),zu=max(-1,min(1,1-2.0*n/N)),ph=2*k*rt*zu); ar+=cos(ph);ai+=sin(ph)); (ar^2+ai^2)/nn^2;

print("");
print("=== METRIC A: 3D SPREAD (min = Brennpunkt) ===");
my(bp_t=0,bp_v=99,bc_t=0,bc_v=99);
forstep(t=0.10, 0.48, 0.005, my(sp=sp3d(pv,np,t),sc=sp3d(cv,nc,t)); if(sp<bp_v,bp_v=sp;bp_t=t); if(sc<bc_v,bc_v=sc;bc_t=t); if(round(t*100)%5==0, print("  t=",precision(t,4)," P=",precision(sp,6)," C=",precision(sc,6))));
print("  PRIME minimum: t = ", precision(bp_t,4), " (1/t = ", precision(1/bp_t,3), ")");
print("  COMP  minimum: t = ", precision(bc_t,4), " (1/t = ", precision(1/bc_t,3), ")");

print("");
print("=== METRIC B: P/C BACKSCATTER RATIO ===");
for(lam_idx=1, 4, my(lam=[8,13,21,35][lam_idx], br=0, bt=0); forstep(t=0.05, 0.48, 0.005, my(bp=bsc(pv,np,t,lam),bc=bsc(cv,nc,t,lam),r=if(bc>1e-12,bp/bc,0)); if(r>br&&r<1e6,br=r;bt=t)); print("  lam=",lam,": best t=",precision(bt,4)," ratio=",precision(br,3),"x"));

print("");
print("=== METRIC C: PRIME-ONLY peak ===");
for(lam_idx=1, 4, my(lam=[8,13,21,35][lam_idx], bv=0, bt=0); forstep(t=0.05, 0.48, 0.005, my(bp=bsc(pv,np,t,lam)); if(bp>bv,bv=bp;bt=t)); print("  lam=",lam,": prime peak t=",precision(bt,4)));

print("");
print("=== METRIC D: MAX SEPARATION (P - C) ===");
for(lam_idx=1, 4, my(lam=[8,13,21,35][lam_idx], bd=0, bt=0); forstep(t=0.05, 0.48, 0.005, my(bp=bsc(pv,np,t,lam),bc=bsc(cv,nc,t,lam),d=bp-bc); if(d>bd,bd=d;bt=t)); print("  lam=",lam,": max(P-C) at t=",precision(bt,4)," delta=",precision(bd,5)));
}
