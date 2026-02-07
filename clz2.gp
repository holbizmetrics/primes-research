default(realprecision, 28);
G5 = znstar(5, 1);
for(a = 0, 3, L = lfuncreate([G5, [a]]); z = lfunzeros(L, 60); printf("Q5_%d: ", a); for(j = 1, #z, printf("%.8f ", z[j])); printf("\n"));
