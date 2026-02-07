\\ Test zeta zeros against Fibonacci numbers
fib(n) = fibonacci(n);
gamma = [14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588, 37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478];

print("Fibonacci: ", vector(15, i, fib(i)));
print("\n=== Testing γ_n against nearest Fibonacci ===\n");

for(n=1, 10,
    g = gamma[n];
    print("γ_", n, " = ", precision(g, 12));
    best_fib = 0; best_k = 0;
    for(k=1, 20, if(abs(fib(k) - g) < abs(best_fib - g), best_fib = fib(k); best_k = k));
    print("  Nearest F_", best_k, " = ", best_fib);
    diff = g - best_fib;
    print("  Diff: ", precision(diff, 10));
    if(abs(diff) > 0.001,
        ba = bestappr(diff, 10000);
        print("  Best rational: ", ba);
        d = denominator(ba);
        if(d > 1, print("    Factors of ", d, ": ", factor(d)));
    );
    print("");
);

print("=== γ₂ Formula Check ===");
print("γ₂ - 21 = ", precision(gamma[2] - 21, 12));
print("8/363   = ", precision(8/363, 12));
print("Error   = ", precision(gamma[2] - 21 - 8/363, 12));

print("\n=== Searching Fibonacci formulas F_k ± F_j/(3*m²) ===\n");
for(n=1, 10,
    g = gamma[n];
    best_err = 1.0; best_f = "";
    for(k=5, 13,
        base = fib(k);
        if(abs(g - base) < 10,
            for(j=2, 10,
                num = fib(j);
                for(m=1, 60,
                    denom = 3 * m^2;
                    err1 = abs(g - base - num/denom);
                    err2 = abs(g - base + num/denom);
                    if(err1 < best_err, best_err = err1; best_f = Str("F_",k," + F_",j,"/(3*",m,"²)"));
                    if(err2 < best_err, best_err = err2; best_f = Str("F_",k," - F_",j,"/(3*",m,"²)"));
                )
            )
        )
    );
    if(best_err < 0.01, print("γ_", n, " ≈ ", best_f, " [err ", precision(best_err, 6), "]"),
                        print("γ_", n, ": no formula [err ", precision(best_err, 3), "]"));
);
