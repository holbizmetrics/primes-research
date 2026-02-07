default(realprecision, 28);
G3 = znstar(3, 1);
for(a = 0, 1, L = lfuncreate([G3, [a]]); z = lfunzeros(L, 80); printf("Q3_%d: ", a); for(j = 1, #z, printf("%.8f ", z[j])); printf("\n"));
