from itertools import product
from datetime import datetime

def recurs(K, N):
    def track(tres, ost, res):
        if len(tres) == N:
            if ost == 0:
                res.append(tuple(tres))
            return
        for i in range(ost + 1):
            track(tres + [i], ost - i, res)

    res = []
    track([], K, res)
    return res

def funs_dist(K, N): return [p for p in product(range(K + 1), repeat=N) if sum(p) == K]

def optimal(K, N, max_l=11, min_l=1):# оптимальное распределение
    if min_l * N > K or max_l * N < K:
        return None

    def target(dist):
        avg = sum(dist) / N
        return (max(dist) - min(dist), sum(x > avg for x in dist))

    distributions = [p for p in product(range(min_l, max_l + 1), repeat=N) if sum(p) == K]
    return min(distributions, key=target) if distributions else None

def time_work(label, start, end):
    print(f"{label}: время выполнения = {(end - start).total_seconds():.6f} сек")

# Тестирование
K, N = 3, 3
print("Часть 1: сравнение подходов")
start = datetime.now()
a_dist = recurs(K, N)
time_work("Рекурсивный метод", start, datetime.now())
print(f"Количество вариантов: {len(a_dist)}\nВарианты:\n" + '\n'.join(map(str, a_dist)))

start = datetime.now()
f_dist = funs_dist(K, N)
time_work("Функциональный метод", start, datetime.now())
print(f"Количество вариантов: {len(f_dist)}\nВарианты:\n" + '\n'.join(map(str, f_dist)))

# Сравнение времени
print("\nЧасть 2: оптимизированное распределение")
K, N = 6, 2
start = datetime.now()
all_distributions = [p for p in product(range(1, 11), repeat=N) if sum(p) == K]  # генерация всех вариантов
opt = optimal(K, N)
time_work("Оптимальное распределение", start, datetime.now())
print(f"Оптимальное распределение: {opt}\nНагрузка: макс {max(opt)}, мин {min(opt)}\nКоличество вариантов всех: {len(all_distributions)}\nВарианты:\n" + '\n'.join(map(str, all_distributions)))
