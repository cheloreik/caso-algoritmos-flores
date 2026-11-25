marcelo felix flores nina 

// EVALUACIÓN INTEGRADORA · VARIANTE A — "Furgoneta de reparto"
// Caso: una distribuidora tiene una lista de paquetes (cada uno con un peso en kg y una ganancia en Bs) y una furgoneta
// que aguanta una capacidad en kg. Hay que elegir QUÉ paquetes llevar para ganar lo máximo sin pasarse de la capacidad.
// Cada paquete se lleva entero o no se lleva.
// PlanificadorIngenuo es CORRECTO pero LENTO (prueba todas las combinaciones). Tu trabajo: analizarlo, elegir la
// estrategia, APLICARLA en PlanificadorMejorado, medir la diferencia y justificar todo.
// Puedes usar este archivo tal cual (si tienes .NET) o portar todo a TU lenguaje.

no es conveniente utilizar el codigo voraz ya que se elege el paquete con mas ganancia o realizar ganancia X Peso 
NO garantiza una conbinacion OPTIMA 
el algoritmo evalua dos posibilidades no incluirlo / incluirlo si la capacidad es suficiente
la estructura de ingenuo es una list Probando todas las combinaciones posibles de paquetes (voraz) siendo que no siempre puede estar en lo correcto
pero la mejora se usara un hashset ya que se guardan resultado (costo)

- ¿Qué pasaría con tu solución si la capacidad fuera **1.000.000.000 de kg**? Explícalo (1,5)
si la capacidad fuera tan grande la relacion costo beneficio se perderia ya que usar al tener tanta capacidad sera indistito la seleccion de paquetes 
porque se prodran llevar todos, y no importaran si se cargo de manera optima o no 

