# Grafo dirigido: cada estado apunta a una lista de (estado_destino, costo)
grafo = {
    "S": [("A", 2), ("B", 2)],
    "A": [("C", 2), ("D", 5)],
    "B": [("D", 2)],
    "C": [("G", 3)],
    "D": [("G", 6)],
    "G": [],  # G no tiene salidas
}

# Heurística: estimación del costo restante hasta G
h = {
    "S": 7,
    "A": 5,
    "B": 7,
    "C": 3,
    "D": 6,
    "G": 0,
}

INICIO = "S"
OBJETIVO = "G"

import itertools
import heapq

def crear_nodo(estado, padre=None, accion=None, g=0, h_valor=0):
    return {
        "estado": estado,
        "padre": padre,
        "accion": accion,
        "g": g,
        "h": h_valor,
        "f": g + h_valor,
    }

def reconstruir_camino(nodo):
    """Sube por los padres hasta la raíz y devuelve la lista de estados en orden S -> ... -> G"""
    camino = []
    actual = nodo
    while actual is not None:
        camino.append(actual["estado"])
        actual = actual["padre"]
    camino.reverse()
    return camino

class ColaPrioridad:
    """Cola de prioridad con desempate estable por orden de inserción (FIFO)."""
    def __init__(self):
        self._heap = []
        self._contador = itertools.count()

    def insertar(self, prioridad, nodo):
        orden = next(self._contador)  # marca cuándo se insertó
        heapq.heappush(self._heap, (prioridad, orden, nodo))

    def extraer_minimo(self):
        prioridad, orden, nodo = heapq.heappop(self._heap)
        return nodo

    def esta_vacia(self):
        return len(self._heap) == 0

    def contenido_para_traza(self):
        """Devuelve una lista legible (estado, prioridad) para imprimir en la traza,
        sin alterar el heap."""
        return [(nodo["estado"], prioridad) for prioridad, orden, nodo in sorted(self._heap)]
    
def calcular_prioridad(algoritmo, g, h_valor):
    if algoritmo == "ucs":
        return g
    elif algoritmo == "voraz":
        return h_valor
    elif algoritmo == "a*":
        return g + h_valor
    else:
        raise ValueError("Algoritmo no reconocido")


def busqueda(algoritmo):
    frontera = ColaPrioridad()
    mejor_g = {INICIO: 0}
    generados = 1
    expandidos = 0
    reaperturas = 0
    frontera_maxima = 0
    traza = []

    raiz = crear_nodo(INICIO, g=0, h_valor=h[INICIO])
    frontera.insertar(calcular_prioridad(algoritmo, 0, h[INICIO]), raiz)

    while not frontera.esta_vacia():
        frontera_maxima = max(frontera_maxima, len(frontera._heap))
        nodo = frontera.extraer_minimo()
        estado = nodo["estado"]

        # Descarte de obsoletos: solo UCS y A* lo aplican
        if algoritmo in ("ucs", "a*") and nodo["g"] > mejor_g[estado]:
            continue

        expandidos += 1

        if estado == OBJETIVO:
            traza.append(f"Expandido: {estado} (¡objetivo!) | Frontera restante: {frontera.contenido_para_traza()}")
            return {
                "algoritmo": algoritmo,
                "camino": reconstruir_camino(nodo),
                "costo": nodo["g"],
                "generados": generados,
                "expandidos": expandidos,
                "frontera_maxima": frontera_maxima,
                "reaperturas": reaperturas,
                "traza": traza,
            }

        for vecino, costo in grafo[estado]:
            nuevo_g = nodo["g"] + costo
            if vecino not in mejor_g or nuevo_g < mejor_g[vecino]:
                if vecino in mejor_g:
                    reaperturas += 1  # ya conocíamos este estado y encontramos un camino mejor
                mejor_g[vecino] = nuevo_g
                nuevo_nodo = crear_nodo(vecino, padre=nodo, accion=f"{estado} -> {vecino}",
                                         g=nuevo_g, h_valor=h[vecino])
                prioridad = calcular_prioridad(algoritmo, nuevo_g, h[vecino])
                frontera.insertar(prioridad, nuevo_nodo)
                generados += 1

        traza.append(f"Expandido: {estado} | Frontera: {frontera.contenido_para_traza()}")

    return None  # fracaso: no se encontró camino a G

resultados = {}
for algoritmo in ["ucs", "voraz", "a*"]:
    resultados[algoritmo] = busqueda(algoritmo)

# Mostrar la traza de cada uno
for algoritmo, resultado in resultados.items():
    print(f"\n===== {algoritmo.upper()} =====")
    for linea in resultado["traza"]:
        print(linea)
    print(f"Camino: {' -> '.join(resultado['camino'])}")
    print(f"Costo total: {resultado['costo']}")
    print(f"Estados generados: {resultado['generados']}")
    print(f"Estados expandidos: {resultado['expandidos']}")
    print(f"Frontera máxima: {resultado['frontera_maxima']}")
    print(f"Reaperturas: {resultado['reaperturas']}")
    
print("\n===== TABLA COMPARATIVA =====")
print(f"{'':20}{'UCS':15}{'Voraz':15}{'A*':15}")
print(f"{'Camino':20}{' -> '.join(resultados['ucs']['camino']):15}"
      f"{' -> '.join(resultados['voraz']['camino']):15}"
      f"{' -> '.join(resultados['a*']['camino']):15}")
print(f"{'Costo':20}{resultados['ucs']['costo']:<15}"
      f"{resultados['voraz']['costo']:<15}"
      f"{resultados['a*']['costo']:<15}")
print(f"{'Prioridad':20}{'g':15}{'h':15}{'g+h':15}")
print(f"{'Expandidos':20}{resultados['ucs']['expandidos']:<15}"
      f"{resultados['voraz']['expandidos']:<15}"
      f"{resultados['a*']['expandidos']:<15}")

"""
PREGUNTAS DE ANÁLISIS

1) ¿Por qué voraz y A* coinciden en este grafo?
Porque la heurística es admisible y consistente para este grafo: en ningún
estado h(n) sobreestima el costo real restante, y en las aristas del camino
óptimo (S->A, A->C, C->G) h es exacta (h(S)=7, h(A)=5, h(C)=3, todas iguales
al costo real restante). Al ser tan precisa en esa rama, el orden de
exploración por h solo (voraz) coincide con el orden por g+h (A*). Esta
coincidencia depende de la calidad de la heurística en este grafo puntual,
no es una propiedad general de voraz.

2) ¿Garantiza voraz devolver el camino de menor costo en general?
No. Voraz prioriza únicamente por h, sin considerar g (lo ya gastado). Puede
lanzarse por un vecino que "parece" cerca del objetivo pero al que se llegó
con costo acumulado alto, ignorando otro camino con mayor h inicial pero
menor g total. Como nunca corrige mirando el costo recorrido, no hay
garantía de optimalidad en general.

3) ¿Qué ocurre si se usa h=0 en A*?
La prioridad queda en g+0=g, que es exactamente la prioridad de UCS. A* se
comporta idénticamente a costo uniforme: ya no usa ninguna estimación para
guiar la búsqueda, solo el costo acumulado real.

4) ¿Hubo reaperturas en UCS? ¿Y en A* y voraz?
En UCS hubo 1 reapertura: al expandir A se generó D con g=7 (por A->D,
costo 5+2). Más tarde, al expandir B, se generó D nuevamente pero con
g=4 (por B->D, costo 2+2), que es menor al g=7 ya registrado. Ese caso
de "mejora un g ya conocido" es la reapertura que cuenta el algoritmo.

En A* y en voraz hubo 0 reaperturas. En A* no llegó a ocurrir porque el
objetivo G se extrajo (vía C, con g+h=7) antes de que D volviera a
generarse por el camino más barato B->D -la búsqueda terminó antes de
que hiciera falta esa mejora. En voraz, directamente no se contempla el
control de mejor_g de la misma manera al no chequear g, por lo que ese
mismo escenario tampoco se refleja como reapertura en su traza.

La diferencia clave es que UCS explora más ampliamente (expande B antes
de llegar a la solución) y por eso "se cruza" con el camino alternativo
hacia D, mientras que A* y voraz, guiados por la heurística, llegan a G
por la rama S->A->C antes de que ese cruce se produzca.

5) ¿"Expandir menos estados" significa "camino más barato"?
No, son propiedades independientes. En esta ejecución, voraz y A* expandieron
menos estados que UCS pero llegaron al mismo costo -expandir menos no
implicó peor camino en este caso, pero tampoco lo garantiza en general. UCS
expande más porque explora sistemáticamente por costo acumulado sin
guiarse por ninguna estimación, lo cual le cuesta más expansiones pero le
da garantía de optimalidad siempre.
"""