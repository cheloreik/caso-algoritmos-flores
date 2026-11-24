from dataclasses import dataclass
from typing import List, Tuple
import time
import random


@dataclass
class Paquete:
    codigo: str
    kg: int
    ganancia: int


class IPlanificador:
    def elegir(self, paquetes: List[Paquete], capacidad_kg: int):
        raise NotImplementedError

    def esta_en_el_viaje(self, codigo: str):
        raise NotImplementedError


# -------------------------------------------------
# SOLUCIÓN INGENUA (2^n)
# -------------------------------------------------
class PlanificadorIngenuo(IPlanificador):

    def __init__(self):
        self.elegidos = []

    def elegir(self, paquetes: List[Paquete], capacidad_kg: int):

        n = len(paquetes)
        mejor = 0
        mejor_mascara = 0

        for mascara in range(1 << n):
            kg = 0
            ganancia = 0

            for i in range(n):
                if mascara & (1 << i):
                    kg += paquetes[i].kg
                    ganancia += paquetes[i].ganancia

            if kg <= capacidad_kg and ganancia > mejor:
                mejor = ganancia
                mejor_mascara = mascara

        self.elegidos = []

        for i in range(n):
            if mejor_mascara & (1 << i):
                self.elegidos.append(paquetes[i].codigo)

        return mejor, self.elegidos.copy()

    def esta_en_el_viaje(self, codigo: str):
        return codigo in self.elegidos


# -------------------------------------------------
# SOLUCIÓN MEJORADA (Programación Dinámica)
# Complejidad: O(n * capacidad)
# -------------------------------------------------
class PlanificadorMejorado(IPlanificador):

    def __init__(self):
        self.elegidos = set()

    def elegir(self, paquetes: List[Paquete], capacidad_kg: int):

        n = len(paquetes)

        dp = [[0] * (capacidad_kg + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            peso = paquetes[i - 1].kg
            valor = paquetes[i - 1].ganancia

            for cap in range(capacidad_kg + 1):

                if peso <= cap:
                    dp[i][cap] = max(
                        dp[i - 1][cap],
                        dp[i - 1][cap - peso] + valor
                    )
                else:
                    dp[i][cap] = dp[i - 1][cap]

        # Reconstruir solución
        codigos = []
        cap = capacidad_kg

        self.elegidos.clear()

        for i in range(n, 0, -1):

            if dp[i][cap] != dp[i - 1]paquete = paquetes[i - 1]

                codigos.append(paquete.codigo)
                self.elegidos.add(paquete.codigo)

                cap -= paquete.kg

        return dp[n][capacidad_kg], codigos

    def esta_en_el_viaje(self, codigo: str):
        return codigo in self.elegidos


# -------------------------------------------------
# DATOS DE PRUEBA
# -------------------------------------------------
def lote(*datos):
    return [Paquete(c, kg, g) for c, kg, g in datos]


CASOS = [
    (
        "el voraz se equivoca",
        lote(
            ("P1", 10, 60),
            ("P2", 20, 100),
            ("P3", 30, 120)
        ),
        50,
        220,
        ["P2", "P3"]
    ),

    (
        "cuatro paquetes",
        lote(
            ("P1", 2, 3),
            ("P2", 3, 4),
            ("P3", 4, 5),
            ("P4", 5, 6)
        ),
        8,
        10,
        ["P2", "P4"]
    ),

    (
        "capacidad cero",
        lote(
            ("P1", 5, 10),
            ("P2", 7, 12)
        ),
        0,
        0,
        []
    ),

    (
        "sin paquetes",
        lote(),
        30,
        0,
        []
    ),

    (
        "nada cabe",
        lote(
            ("P1", 40, 90),
            ("P2", 50, 100)
        ),
        30,
        0,
        []
    ),

    (
        "entran todos",
        lote(
            ("P1", 5, 10),
            ("P2", 7, 12),
            ("P3", 3, 4)
        ),
        100,
        26,
        ["P1", "P2", "P3"]
    )
]


# -------------------------------------------------
# PRUEBAS
# -------------------------------------------------
def probar(titulo, fabrica):

    bien = 0
    total = 0

    for que, paquetes, capacidad, esperada, codigos in CASOS:

        plan = fabrica()

        ganancia, elegidos = plan.elegir(paquetes, capacidad)

        total += 1

        ok = (
            ganancia == esperada and
            sorted(elegidos) == sorted(codigos)
        )

        if ok:
            bien += 1
        else:
            print(
                f"MAL en '{que}': "
                f"esperado {esperada} con {codigos}, "
                f"obtuvo {ganancia} con {elegidos}"
            )

    p = fabrica()
    p.elegir(CASOS[0][1], CASOS[0][2])

    total += 2

    if p.esta_en_el_viaje("P2"):
        bien += 1
    else:
        print("MAL en EstaEnElViaje(P2)")

    if not p.esta_en_el_viaje("P1"):
        bien += 1
    else:
        print("MAL en EstaEnElViaje(P1)")

    print(f"{titulo}: {bien} de {total} pruebas correctas")


# -------------------------------------------------
# CARGA
# -------------------------------------------------
def ejecutar_carga(plan, n):

    random.seed(n)

    paquetes = [
        Paquete(
            f"C{i}",
            random.randint(5, 59),
            random.randint(10, 99)
        )
        for i in range(n)
    ]

    capacidad = sum(p.kg for p in paquetes) // 3

    ganancia, _ = plan.elegir(paquetes, capacidad)

    return ganancia


# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":

    probar(
        "PlanificadorIngenuo",
        lambda: PlanificadorIngenuo()
    )

    probar(
        "PlanificadorMejorado",
        lambda: PlanificadorMejorado()
    )

    inicio = time.perf_counter()

    ejecutar_carga(
        PlanificadorIngenuo(),
        18
    )

    fin = time.perf_counter()

    print(
        f"Ingenuo con 18 paquetes: "
        f"{(fin - inicio) * 1000:.2f} ms"
    )