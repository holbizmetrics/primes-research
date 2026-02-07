default(realprecision, 28);
G5 = znstar(5, 1);
L = lfuncreate([G5, [1]]); z = lfunzeros(L, 200);
printf("Q5_1: "); for(j = 1, #z, printf("%.8f ", z[j])); printf("\n");
