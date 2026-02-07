default(realprecision, 28);
G7 = znstar(7, 1);
for(a = 0, 5, L = lfuncreate([G7, [a]]); z = lfunzeros(L, 50); printf("Q7_%d: ", a); for(j = 1, #z, printf("%.8f ", z[j])); printf("\n"));
