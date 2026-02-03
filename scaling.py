import math,cmath,random
Z=[14.13,21.02,25.01,30.42,32.94,37.59,40.92,43.33,48.01,49.77,52.97,56.45,59.35,60.83,65.11,67.08,69.55,72.07,75.70,77.14,79.34,82.91,84.74,87.43,88.81,92.49,94.65,95.87,98.83,101.3,103.7,105.4,107.2,111.0,111.9,114.3,116.2,118.8,121.4,122.9]
def C(N):
    xs=[10**(0.3+i*(math.log10(N)-0.3)/99) for i in range(100)]
    def E(x,rp=None):
        t=0j
        for i,g in enumerate(Z):
            ph=g*math.log(x)+(rp[i] if rp else 0)
            t+=math.sqrt(x)*cmath.exp(1j*ph)/complex(0.5,g)
        return -2*t.real
    def v(a):m=sum(a)/len(a);return sum((y-m)**2 for y in a)/len(a)
    va=v([E(x) for x in xs])
    vn=sum(v([E(x,[random.uniform(0,6.28) for _ in Z]) for x in xs]) for _ in range(25))/25
    return va/vn
Ns=[100,200,500,1000,2000,5000,10000,20000,50000]
Cs=[C(n) for n in Ns]
print('N        C(N)   log(N)  1/log(N)')
for i,n in enumerate(Ns):
    print(f'{n:>6} {Cs[i]:>7.3f} {math.log(n):>6.2f} {1/math.log(n):>8.4f}')
x=[1/math.log(n) for n in Ns];y=Cs
xm=sum(x)/len(x);ym=sum(y)/len(y)
b=sum((x[i]-xm)*(y[i]-ym) for i in range(len(x)))/sum((x[i]-xm)**2 for i in range(len(x)))
a=ym-b*xm
print(f'\nFit: C(N) = {a:.3f} + {b:.2f}/log(N)')
print(f'Asymptote as N->inf: C(N) -> {a:.3f}')
