import random
import time

# 1. Preparar los datos
n = 1_000_000
num_busquedas = 1_000

# Arreglo ordenado de 1,000,000 de enteros
arreglo_ordenado = sorted([random.randint(1, 10_000_000) for _ in range(n)])

# 1,000 claves que SÍ existan en el arreglo (para garantizar que la búsqueda sea justa)
claves_a_buscar = [random.choice(arreglo_ordenado) for _ in range(num_busquedas)]

# --- ALGORITMOS DE BÚSQUEDA ---

# Búsqueda Lineal: O(n)
def busqueda_lineal(arr, claves):
    for clave in claves:
        encontrado = False
        for i in range(len(arr)):
            if arr[i] == clave:
                encontrado = True
                break

# Búsqueda Binaria: O(log n)
def busqueda_binaria(arr, claves):
    for clave in claves:
        izquierda, derecha = 0, len(arr) - 1
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if arr[medio] == clave:
                break
            elif arr[medio] < clave:
                izquierda = medio + 1
            else:
                derecha = medio - 1

# --- APLICACIÓN DEL PROTOCOLO (Calentar + 3 Corridas + Promediar) ---

def medir_tiempo(funcion, arr, claves):
    # 1. Calentamiento (Warm-up)
    funcion(arr, claves)
    
    # 3 Corridas medidas
    tiempos = []
    for _ in range(3):
        inicio = time.perf_counter()
        funcion(arr, claves)
        fin = time.perf_counter()
        tiempos.append((fin - inicio) * 1000) # Convertir a milisegundos
        
    return sum(tiempos) / len(tiempos)

# Ejecutar mediciones
tiempo_lineal = medir_tiempo(busqueda_lineal, arreglo_ordenado, claves_a_buscar)
tiempo_binario = medir_tiempo(busqueda_binaria, arreglo_ordenado, claves_a_buscar)

# Calcular el cociente (cuántas veces más lento es el lineal respecto al binario)
cociente = tiempo_lineal / tiempo_binario

# Resultados en consola
print(f"{'Algoritmo':<18} | {'Tiempo Promedio (1000 búsquedas)':<30}")
print("-" * 52)
print(f"Búsqueda Lineal  | {tiempo_lineal:.2f} ms")
print(f"Búsqueda Binaria | {tiempo_binario:.4f} ms")
print("-" * 52)
print(f"Cociente (Lineal / Binaria): {cociente:.2f}x más lento el lineal")



****************** RESULTADO  **********
#conciderar que los datos generados ya estaban organizados/ordenados porque que es requicito para binario 

Algoritmo          | Tiempo Promedio (1000 búsquedas)
----------------------------------------------------
Búsqueda Lineal  | 60473.36 ms
Búsqueda Binaria | 2.4501 ms
----------------------------------------------------
Cociente (Lineal / Binaria): 24681.98x más lento el lineal