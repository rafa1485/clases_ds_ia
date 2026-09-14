"""
busqueda.py

Implementa el esqueleto común de búsqueda que comparten UCS, Voraz y A*,
y las tres funciones públicas que lo especializan.

Los tres algoritmos comparten:
- misma cola de prioridad con desempate FIFO
- mismo diccionario mejor_g[estado] = mejor costo conocido para llegar a estado
- descarte de nodos obsoletos (cuando se extrae un nodo cuyo g ya fue superado)
- prueba de objetivo AL EXTRAER, no al generar
- reconstrucción del camino siguiendo los padres

Lo único que cambia entre ellos es qué valor se usa como prioridad de la
cola: g (UCS), h (Voraz), o g+h (A*).
"""

from estructuras import crear_nodo, ColaPrioridad


def _calcular_prioridad(modo, g, h):
    """
    Devuelve la prioridad de un nodo según el algoritmo:
        - "ucs":        prioridad = g      (costo recorrido: privilegia lo más barato)
        - "voraz":      prioridad = h      (heurística: privilegia lo que parece más cerca)
        - "a_estrella": prioridad = g + h  (costo total estimado de la solución)
    """
    if modo == "ucs":
        return g
    elif modo == "voraz":
        return h
    elif modo == "a_estrella":
        return g + h
    else:
        raise ValueError(f"Modo desconocido: {modo}")


def _reconstruir_camino(nodo):
    """
    Sigue la cadena de 'padre' desde el nodo objetivo hasta la raíz,
    y devuelve la lista de estados en orden desde el inicio hasta el objetivo.
    """
    camino = []
    actual = nodo
    while actual is not None:
        camino.append(actual["estado"])
        actual = actual["padre"]
    camino.reverse()
    return camino


def buscar(modo, grafo, heuristica, inicio, objetivo):
    """
    Esqueleto común de búsqueda, especializado según 'modo'.

    Parámetros:
        modo:       "ucs" | "voraz" | "a_estrella"
        grafo:      dict de adyacencia {estado: [(vecino, costo), ...]}
        heuristica: dict {estado: h(estado)}
        inicio:     estado inicial
        objetivo:   estado objetivo

    Devuelve un diccionario con:
        camino:              lista de estados desde inicio hasta objetivo (o None si falla)
        costo:                costo total del camino encontrado (g del nodo objetivo)
        estados_generados:   cantidad de nodos creados (insertados en la frontera)
        estados_expandidos:  cantidad de nodos extraídos y procesados (pasaron la prueba de obsoleto)
        frontera_maxima:     tamaño máximo que alcanzó la frontera durante la ejecución
        reaperturas:         veces que se mejoró mejor_g de un estado ya conocido
        traza:               lista de eventos, uno por cada expansión, con el estado
                              extraído y el contenido de la frontera en ese momento
    """
    contador_generados = 0
    contador_expandidos = 0
    frontera_maxima = 0
    reaperturas = 0
    traza = []

    mejor_g = {}  # mejor_g[estado] = mejor costo g conocido hasta ahora para llegar a ese estado
    frontera = ColaPrioridad()

    # --- insertar nodo inicial en la frontera ---
    h_inicio = heuristica[inicio]
    raiz = crear_nodo(inicio, padre=None, accion=None, g=0, h=h_inicio)
    raiz["f"] = _calcular_prioridad(modo, raiz["g"], raiz["h"])
    mejor_g[inicio] = 0
    frontera.insertar(raiz["f"], raiz)
    contador_generados += 1

    # --- mientras la frontera no esté vacía ---
    while not frontera.esta_vacia():
        frontera_maxima = max(frontera_maxima, len(frontera))

        nodo = frontera.extraer()
        estado = nodo["estado"]

        # descartar si su g es obsoleto frente a mejor_g
        # (puede haber quedado una copia vieja en la cola si luego encontramos
        # un camino mejor hacia el mismo estado)
        if nodo["g"] > mejor_g.get(estado, float("inf")):
            continue

        contador_expandidos += 1

        # registrar la traza de esta expansión: qué se extrajo y cómo queda la frontera
        traza.append({
            "expandido": estado,
            "g": nodo["g"],
            "h": nodo["h"],
            "f": nodo["f"],
            "frontera_restante": frontera.contenido(),
        })

        # el objetivo se comprueba AL EXTRAER
        if estado == objetivo:
            return {
                "camino": _reconstruir_camino(nodo),
                "costo": nodo["g"],
                "estados_generados": contador_generados,
                "estados_expandidos": contador_expandidos,
                "frontera_maxima": frontera_maxima,
                "reaperturas": reaperturas,
                "traza": traza,
            }

        # relajar cada transición legal y actualizar mejor_g
        for vecino, costo in grafo[estado]:
            nuevo_g = nodo["g"] + costo
            if nuevo_g < mejor_g.get(vecino, float("inf")):
                if vecino in mejor_g:
                    reaperturas += 1  # ya conocíamos 'vecino' y ahora lo mejoramos
                mejor_g[vecino] = nuevo_g

                h_vecino = heuristica[vecino]
                hijo = crear_nodo(
                    vecino,
                    padre=nodo,
                    accion=f"{estado} -> {vecino}",
                    g=nuevo_g,
                    h=h_vecino,
                )
                hijo["f"] = _calcular_prioridad(modo, nuevo_g, h_vecino)
                frontera.insertar(hijo["f"], hijo)
                contador_generados += 1

    # frontera vacía sin encontrar el objetivo
    return {
        "camino": None,
        "costo": None,
        "estados_generados": contador_generados,
        "estados_expandidos": contador_expandidos,
        "frontera_maxima": frontera_maxima,
        "reaperturas": reaperturas,
        "traza": traza,
    }


def ucs(grafo, heuristica, inicio, objetivo):
    """Búsqueda de costo uniforme: prioridad = g (el camino más barato recorrido)."""
    return buscar("ucs", grafo, heuristica, inicio, objetivo)


def voraz(grafo, heuristica, inicio, objetivo):
    """Búsqueda voraz (greedy best-first): prioridad = h (lo que parece más cerca del objetivo)."""
    return buscar("voraz", grafo, heuristica, inicio, objetivo)


def a_estrella(grafo, heuristica, inicio, objetivo):
    """Búsqueda A*: prioridad = g + h (costo total estimado de la solución)."""
    return buscar("a_estrella", grafo, heuristica, inicio, objetivo)