import datetime
import math
import matplotlib.pyplot as plt
#рекурсия
def F_rec(n):
    if n==1: return 1
    else :
        G_n=G_rec(n-1)
        return (-1)**n * (F_rec(n-1) - 2*G_n)
def G_rec(n):
    if n==1: return 1
    else:
        F_n=F_rec(n-1)
        return (-1)* F_n + math.factorial(2*n-1)
#итеративное
def F_it(n):
    F_v=[0]*(n+1)
    G_v=[0]*(n+1)
    F_v[1]=1
    G_v[1]=1

    for i in range(2,n+1):
        G_v[i]=(-1)*F_v[i-1]+math.factorial(2*i-1)
        F_v[i]=(-1)**i*(F_v[i-1]-2*G_v[i-1])
    return G_v[n],F_v[n]
#время
n_vr=range(1,21)
rec_time=[]
it_time=[]
for n in n_vr:
    start_time=datetime.datetime.now()
    F_rec(n)
    rec_time.append((datetime.datetime.now()-start_time).total_seconds())
    start_time = datetime.datetime.now()
    F_it(n)
    it_time.append((datetime.datetime.now() - start_time).total_seconds())
#таблица
print(f"{'n':<10} {'время рекурсии (сек)':<20} {'время итерации (сек)':<20}")
for n, r_time, i_time in zip(n_vr, rec_time, it_time):
    print(f"{n:<5} {r_time:<20.6f} {i_time:<20.6f}")

#график
plt.plot(n_vr, rec_time, label='recursive', marker='o')
plt.plot(n_vr, it_time, label='iterative', marker='x')
plt.title('время сравнения итерации и рекурсии')
plt.xlabel('n')
plt.ylabel('время')
plt.legend()
plt.grid(True)
plt.show()