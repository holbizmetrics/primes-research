ps=0;pc=0;cs=0;cc=0;
for(n=2,100000,g=prime(n+1)-prime(n);if(isprime(n),ps+=g;pc++,cs+=g;cc++));
print("Prime indices: count=",pc," avg_gap=",1.0*ps/pc);
print("Composite idx: count=",cc," avg_gap=",1.0*cs/cc);
print("Ratio prime/comp: ",(1.0*ps/pc)/(1.0*cs/cc));
quit;
