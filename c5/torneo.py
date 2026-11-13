import random
import time

# 1. Algoritmo Cuadrático: Inserción
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# 2. Algoritmo n log n: MergeSort
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        
        merge_sort(L)
        merge_sort(R)
        
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

# 3. Algoritmo n log n: QuickSort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# 4. Cuarto Competidor: Timsort (sort nativo de Python)
def python_sort(arr):
    arr.sort()

algoritmos = [
    ("Inserción", insertion_sort),
    ("MergeSort", merge_sort),
    ("QuickSort", quick_sort),
    ("Timsort (Python)", python_sort)
]

tamanos = [10000, 20000, 40000, 80000]

print(f"{'n':<10} | {'Algoritmo':<18} | {'Promedio (3 corridas)':<20}")
print("-" * 55)

for n in tamanos:
    base_data = [random.randint(1, 1000000) for _ in range(n)]
    
    for nombre, func in algoritmos:
        calentamiento = list(base_data)
        if nombre == "QuickSort":
            calentamiento = func(calentamiento)
        else:
            func(calentamiento)
            
        assert calentamiento == sorted(base_data), f"Error: {nombre} no ordenó correctamente."

        tiempos = []
        for _ in range(3):
            copia = list(base_data)
            inicio = time.perf_counter()
            if nombre == "QuickSort":
                copia = func(copia)
            else:
                func(copia)
            fin = time.perf_counter()
            tiempos.append((fin - inicio) * 1000)
            
        promedio = sum(tiempos) / len(tiempos)
        print(f"{n:<10} | {nombre:<18} | {promedio:.2f} ms")
    print("-" * 55)