import random
import time


def hay_repetidos_por_pares(carnets):
    for i in range(len(carnets)):
        for j in range(i + 1, len(carnets)):
            if carnets[i] == carnets[j]:
                return True
    return False


def hay_repetidos_curado(carnets):
    vistos = set()

    for carnet in carnets:
        if carnet in vistos:
            return True
        vistos.add(carnet)

    return False


def generar_sin_repetidos(n):
    datos = list(range(n))
    random.shuffle(datos)
    return datos


def medir(funcion, datos):
    inicio = time.perf_counter()
    funcion(datos)
    fin = time.perf_counter()
    return (fin - inicio) * 1000


print(f"{'N':<10}{'O(n²) ms':<15}{'O(n) ms':<15}")
print("-" * 40)

for n in [10000, 50000, 80000]:

    datos = generar_sin_repetidos(n)

    tiempo_lento = medir(
        hay_repetidos_por_pares,
        datos
    )

    tiempo_rapido = medir(
        hay_repetidos_curado,
        datos
    )

    print(
        f"{n:<10}"
        f"{tiempo_lento:<15.2f}"
        f"{tiempo_rapido:<15.2f}"
    )