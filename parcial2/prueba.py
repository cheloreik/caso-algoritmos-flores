import time
import heapq
from dataclasses import dataclass


# ---------------- INTERFAZ ----------------

class IReceptorPedidos:
    def registrar(self, pedido, plazo_minutos):
        pass

    def preparar_siguiente(self):
        pass

    def esta_pendiente(self, pedido):
        pass

    @property
    def pendientes(self):
        pass


# ---------------- MODELO ----------------

@dataclass
class Pedido:
    nombre: str
    plazo: int
    llegada: int


# ---------- SOLUCIÓN INGENUA ----------

class ReceptorIngenuo(IReceptorPedidos):

    def __init__(self):
        self.lista = []
        self.llegadas = 0

    def registrar(self, pedido, plazo_minutos):
        self.lista.append(
            Pedido(pedido, plazo_minutos, self.llegadas)
        )
        self.llegadas += 1

    def preparar_siguiente(self):
        if len(self.lista) == 0:
            return None

        mejor = 0

        for i in range(1, len(self.lista)):
            p = self.lista[i]
            m = self.lista[mejor]

            if (
                p.plazo < m.plazo
                or
                (p.plazo == m.plazo and p.llegada < m.llegada)
            ):
                mejor = i

        nombre = self.lista[mejor].nombre
        self.lista.pop(mejor)

        return nombre

    def esta_pendiente(self, pedido):
        for p in self.lista:
            if p.nombre == pedido:
                return True

        return False

    @property
    def pendientes(self):
        return len(self.lista)


# ---------- SOLUCIÓN MEJORADA ----------

class ReceptorMejorado(IReceptorPedidos):

    def __init__(self):
        self.cola = []
        self.pendientes_set = set()
        self.llegadas = 0

    def registrar(self, pedido, plazo_minutos):
        heapq.heappush(
            self.cola,
            (plazo_minutos, self.llegadas, pedido)
        )

        self.pendientes_set.add(pedido)
        self.llegadas += 1

    def preparar_siguiente(self):
        if not self.cola:
            return None

        plazo, llegada, pedido = heapq.heappop(self.cola)

        self.pendientes_set.remove(pedido)

        return pedido

    def esta_pendiente(self, pedido):
        return pedido in self.pendientes_set

    @property
    def pendientes(self):
        return len(self.cola)


# ---------------- GUION DE PRUEBAS ----------------

GUION = [
    ("registrar", "Torta", 120, ""),
    ("registrar", "Galletas", 30, ""),
    ("registrar", "Pan", 120, ""),
    ("registrar", "Brazo", 60, ""),
    ("pendientes", "", 0, "4"),
    ("esta", "Galletas", 0, "True"),
    ("esta", "Flan", 0, "False"),
    ("preparar", "", 0, "Galletas"),
    ("esta", "Galletas", 0, "False"),
    ("preparar", "", 0, "Brazo"),
    ("registrar", "Alfajor", 30, ""),
    ("preparar", "", 0, "Alfajor"),
    ("preparar", "", 0, "Torta"),
    ("preparar", "", 0, "Pan"),
    ("preparar", "", 0, "(ninguno)"),
    ("pendientes", "", 0, "0"),
]


def ejecutar(g, op, arg, plazo):

    if op == "registrar":
        g.registrar(arg, plazo)
        return ""

    elif op == "preparar":
        return g.preparar_siguiente() or "(ninguno)"

    elif op == "esta":
        return str(g.esta_pendiente(arg))

    else:
        return str(g.pendientes)


def probar(titulo, g):

    bien = 0
    total = 0

    for op, arg, plazo, esperado in GUION:

        obtenido = ejecutar(g, op, arg, plazo)

        if op == "registrar":
            continue

        total += 1

        if obtenido == esperado:
            bien += 1
        else:
            print(
                f"MAL en '{op} {arg}': "
                f"esperado {esperado}, obtuvo {obtenido}"
            )

    print(f"{titulo}: {bien} de {total} pasos correctos")


# ---------------- CARGA ----------------

def ejecutar_carga(g, n):

    for i in range(n):
        plazo = (((i * 6007) % 6) + 1) * 15
        g.registrar(f"Q{i}", plazo)

    control = 0

    for i in range(n):
        control += len(g.preparar_siguiente())

    return control


# ---------------- MAIN ----------------

if __name__ == "__main__":

    probar("ReceptorIngenuo", ReceptorIngenuo())
    probar("ReceptorMejorado", ReceptorMejorado())

    for n in [10000, 50000, 80000]:

        inicio = time.perf_counter()

        ejecutar_carga(ReceptorIngenuo(), n)

        fin = time.perf_counter()

        print(
            f"Ingenuo con {n:,} pedidos: "
            f"{(fin - inicio) * 1000:.2f} ms"
        )

    print()

    for n in [10000, 50000, 80000]:

        inicio = time.perf_counter()

        ejecutar_carga(ReceptorMejorado(), n)

        fin = time.perf_counter()

        print(
            f"Mejorado con {n:,} pedidos: "
            f"{(fin - inicio) * 1000:.2f} ms"
        )