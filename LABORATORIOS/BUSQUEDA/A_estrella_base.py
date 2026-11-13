"""Implementación básica de A* para el trabajo práctico.

El programa utiliza listas y diccionarios para que la lógica del algoritmo
sea visible. No usa heapq ni clases.
"""

from datos_problema import costos, h


def crear_nodo(estado, padre=None, accion=None, g=0):
    """Crea un nodo de búsqueda con el costo acumulado y la heurística."""
    return {
        "estado": estado,
        "padre": padre,
        "accion": accion,
        "g": g,
        "h": h[estado],
        "f": g + h[estado],
    }


def sucesores(estado):
    """Devuelve pares (estado_siguiente, costo_paso) de las aristas salientes."""
    resultado = []
    for (origen, destino), costo in costos.items():
        if origen == estado:
            resultado.append((destino, costo))
    return resultado


def reconstruir_camino(nodo):
    """Sigue los padres desde la meta hasta la raíz."""
    camino = []
    actual = nodo

    while actual is not None:
        camino.append(actual["estado"])
        actual = actual["padre"]

    camino.reverse()
    return camino


def prioridad(nodo, orden):
    """Devuelve la prioridad f y el orden para resolver empates."""
    return (nodo["f"], orden)


def a_estrella(inicial, objetivo):
    """Ejecuta A* y devuelve el resultado junto con una traza."""
    raiz = crear_nodo(inicial, g=0)
    frontera = [{"nodo": raiz, "orden": 0}]
    mejor_g = {inicial: 0}
    expandidos = set()
    traza = []
    orden_siguiente = 1
    generados = 1
    expandidos_total = 0
    reaperturas = 0
    max_frontera = len(frontera)

    while frontera:
        # La lista reemplaza a una cola de prioridad. Es menos eficiente,
        # pero permite observar directamente cómo se selecciona el mínimo.
        entrada = min(
            frontera,
            key=lambda elemento: prioridad(
                elemento["nodo"], elemento["orden"]
            ),
        )
        frontera.remove(entrada)
        nodo = entrada["nodo"]

        if nodo["g"] > mejor_g[nodo["estado"]]:
            continue

        estados_frontera = [
            (elemento["nodo"]["estado"], elemento["nodo"]["f"])
            for elemento in frontera
        ]
        traza.append(
            {
                "extraido": nodo["estado"],
                "g": nodo["g"],
                "h": nodo["h"],
                "f": nodo["f"],
                "frontera": estados_frontera,
            }
        )

        if nodo["estado"] == objetivo:
            return {
                "camino": reconstruir_camino(nodo),
                "costo": nodo["g"],
                "generados": generados,
                "expandidos": expandidos_total,
                "frontera_maxima": max_frontera,
                "reaperturas": reaperturas,
                "traza": traza,
            }

        expandidos.add(nodo["estado"])
        expandidos_total += 1

        for estado_siguiente, costo_paso in sucesores(nodo["estado"]):
            nuevo_g = nodo["g"] + costo_paso

            if estado_siguiente not in mejor_g or nuevo_g < mejor_g[estado_siguiente]:
                if estado_siguiente in expandidos:
                    reaperturas += 1

                mejor_g[estado_siguiente] = nuevo_g
                hijo = crear_nodo(
                    estado_siguiente,
                    padre=nodo,
                    accion=nodo["estado"] + " -> " + estado_siguiente,
                    g=nuevo_g,
                )
                frontera.append({"nodo": hijo, "orden": orden_siguiente})
                orden_siguiente += 1
                generados += 1

        max_frontera = max(max_frontera, len(frontera))

    return {
        "camino": None,
        "costo": None,
        "generados": generados,
        "expandidos": expandidos_total,
        "frontera_maxima": max_frontera,
        "reaperturas": reaperturas,
        "traza": traza,
    }


def mostrar_resultado(resultado):
    """Imprime el resultado y la traza de A*."""
    print("Camino:", resultado["camino"])
    print("Costo:", resultado["costo"])
    print("Estados generados:", resultado["generados"])
    print("Estados expandidos:", resultado["expandidos"])
    print("Frontera máxima:", resultado["frontera_maxima"])
    print("Reaperturas:", resultado["reaperturas"])
    print("\nTraza:")

    for paso, registro in enumerate(resultado["traza"], start=1):
        print(
            paso,
            "extrae",
            registro["extraido"],
            "g=",
            registro["g"],
            "h=",
            registro["h"],
            "f=",
            registro["f"],
            "frontera=",
            registro["frontera"],
        )


if __name__ == "__main__":
    resultado = a_estrella("S", "G")
    mostrar_resultado(resultado)
