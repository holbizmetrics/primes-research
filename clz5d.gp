default(realprecision, 28);
G5 = znstar(5, 1);
L = lfuncreate([G5, [3]]); z = lfunzeros(L, 200);
printf("Q5_3: "); for(j = 1, #z, printf("%.8f ", z[j])); printf("\n");
