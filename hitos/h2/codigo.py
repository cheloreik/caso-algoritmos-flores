import bisect
import time


def busqueda_lineal(lista, objetivo):
    for i, valor in enumerate(lista):
        if valor == objetivo:
            return i
    return -1


def busqueda_binaria(lista, objetivo):
    pos = bisect.bisect_left(lista, objetivo)

    if pos < len(lista) and lista[pos] == objetivo:
        return pos

    return -1


def comparar(n):

    correlativos = list(range(2684000000, 2684000000 + n))

    objetivo = 2684124676

    # Si el correlativo no existe en la lista, lo agregamos
    if objetivo not in correlativos:
        correlativos.append(objetivo)
        correlativos.sort()

    print(f"\nCantidad de correlativos: {len(correlativos):,}")

    # Búsqueda lineal
    inicio = time.perf_counter()

    pos_lineal = busqueda_lineal(correlativos, objetivo)

    fin = time.perf_counter()

    tiempo_lineal = (fin - inicio) * 1000

    # Búsqueda binaria
    inicio = time.perf_counter()

    pos_binaria = busqueda_binaria(correlativos, objetivo)

    fin = time.perf_counter()

    tiempo_binaria = (fin - inicio) * 1000

    print("\nCorrelativo buscado:", objetivo)

    print("\nBúsqueda Lineal")
    print("Posición:", pos_lineal)
    print(f"Tiempo: {tiempo_lineal:.6f} ms")

    print("\nBúsqueda Binaria")
    print("Posición:", pos_binaria)
    print(f"Tiempo: {tiempo_binaria:.6f} ms")


comparar(10000)
comparar(50000)
comparar(80000)