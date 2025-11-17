# В файле в первой строке- грузоподьемность самолета, во второй строке веса грузов через пробел .
# Распечатать номера грузов из заданного списка, полностью загружающих самолет
# (суммарный вес груза должен равняться грузоподьемности самолета)

with open('input.txt', 'r') as f:
    gruzzpod = int(f.readline().strip())
    weights = list(map(int, f.readline().split()))

n = len(weights)
results = []

def backtrack(start, current_sum, nom_in_sp):
    #сумма равна грузоподъёмности -подходит
    if current_sum == gruzzpod:
        results.append(nom_in_sp[:])  # сохраняем копию списка
        return
    if current_sum > gruzzpod:
        return
    # пробуем добавлять грузы
    for i in range(start, n):
        nom_in_sp.append(i + 1)               # добавляем номер груза (с 1)
        backtrack(i + 1, current_sum + weights[i], nom_in_sp)
        nom_in_sp.pop()

#  перебор
backtrack(0, 0, [])

# результаты
for combo in results:
    print(' '.join(map(str, combo)))