default(realprecision, 28);
G5 = znstar(5, 1);
L = lfuncreate([G5, [0]]); z = lfunzeros(L, 200);
printf("Q5_0: "); for(j = 1, #z, printf("%.8f ", z[j])); printf("\n");
