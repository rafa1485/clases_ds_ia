import heapq

# ============================================================
# TP2 - Busqueda voraz y A* sobre un grafo dirigido
# Alumno: Lucas Manuel
# ============================================================

GRAFO = {
    "S": [("A", 2), ("B", 2)],
    "A": [("C", 2), ("D", 5)],
    "B": [("D", 2)],
    "C": [("G", 3)],
    "D": [("G", 6)],
    "G": [],
}

HEURISTICA = {
    "S": 7,
    "A": 5,
    "B": 7,
    "C": 3,
    "D": 6,
    "G": 0,
}


# ============================================================
# 1. CREACION DE NODOS Y MANEJO DE LA FRONTERA
# ============================================================

def crear_nodo(estado, padre=None, accion=None, g=0):
    h = HEURISTICA[estado]

    return {
        "estado": estado,
        "padre": padre,
        "accion": accion,
        "g": g,
        "h": h,
        "f": g + h,
    }


def insertar_en_frontera(frontera, nodo, prioridad, contador):
    # El contador mantiene el orden FIFO si hay prioridades iguales.
    heapq.heappush(frontera, (prioridad, contador, nodo))
    return contador + 1


def extraer_de_frontera(frontera):
    prioridad, orden, nodo = heapq.heappop(frontera)
    return prioridad, orden, nodo


def reconstruir_camino(nodo):
    camino = []
    actual = nodo

    while actual is not None:
        camino.append(actual["estado"])
        actual = actual["padre"]

    return list(reversed(camino))


def describir_frontera(frontera):
    if not frontera:
        return "[]"

    # Se muestra en el orden en que se extraerian los elementos.
    elementos = []

    for prioridad, orden, nodo in sorted(frontera):
        elementos.append(
            f'{nodo["estado"]}(p={prioridad}, g={nodo["g"]})'
        )

    return "[" + ", ".join(elementos) + "]"


def crear_resultado(
    nodo,
    generados,
    expandidos,
    frontera_maxima,
    mejoras_mejor_g,
    traza,
    tipo_prioridad,
):
    if tipo_prioridad == "g":
        prioridad_objetivo = nodo["g"]
    elif tipo_prioridad == "h":
        prioridad_objetivo = nodo["h"]
    else:
        prioridad_objetivo = nodo["f"]

    return {
        "nodo": nodo,
        "generados": generados,
        "expandidos": expandidos,
        "frontera_maxima": frontera_maxima,
        "mejoras_mejor_g": mejoras_mejor_g,
        "camino": reconstruir_camino(nodo),
        "costo": nodo["g"],
        "prioridad_objetivo": prioridad_objetivo,
        "traza": traza,
    }


# ============================================================
# 2. BUSQUEDA DE COSTO UNIFORME (UCS)
# Prioridad: g(n)
# ============================================================

def busqueda_costo_uniforme():
    frontera = []
    contador = 0

    inicial = crear_nodo("S")
    contador = insertar_en_frontera(
        frontera, inicial, inicial["g"], contador
    )

    mejor_g = {"S": 0}

    generados = 1
    expandidos = 0
    frontera_maxima = 1
    mejoras_mejor_g = 0
    traza = []

    while frontera:
        prioridad, _, nodo = extraer_de_frontera(frontera)
        estado = nodo["estado"]

        # Descarta entradas antiguas que tienen un costo peor.
        if nodo["g"] > mejor_g.get(estado, float("inf")):
            traza.append(
                f"Descarta entrada obsoleta {estado} "
                f"(g={nodo['g']}, prioridad={prioridad})"
            )
            continue

        traza.append(
            f"Extrae {estado} (g={nodo['g']}, prioridad g={prioridad}); "
            f"frontera: {describir_frontera(frontera)}"
        )

        # Se comprueba la meta cuando se extrae de la frontera.
        if estado == "G":
            return crear_resultado(
                nodo,
                generados,
                expandidos,
                frontera_maxima,
                mejoras_mejor_g,
                traza,
                "g",
            )

        expandidos += 1

        for sucesor, costo in GRAFO[estado]:
            nuevo_g = nodo["g"] + costo

            if nuevo_g < mejor_g.get(sucesor, float("inf")):

                # El estado ya era conocido y ahora se encuentra
                # un costo mejor.
                if sucesor in mejor_g:
                    mejoras_mejor_g += 1

                mejor_g[sucesor] = nuevo_g

                hijo = crear_nodo(
                    sucesor,
                    padre=nodo,
                    accion=sucesor,
                    g=nuevo_g,
                )

                contador = insertar_en_frontera(
                    frontera, hijo, hijo["g"], contador
                )

                generados += 1

        frontera_maxima = max(
            frontera_maxima, len(frontera)
        )

    return None


# ============================================================
# 3. BUSQUEDA VORAZ
# Prioridad: h(n)
# ============================================================

def busqueda_voraz():
    frontera = []
    contador = 0

    inicial = crear_nodo("S")
    contador = insertar_en_frontera(
        frontera, inicial, inicial["h"], contador
    )

    mejor_g = {"S": 0}

    generados = 1
    expandidos = 0
    frontera_maxima = 1
    mejoras_mejor_g = 0
    traza = []

    while frontera:
        prioridad, _, nodo = extraer_de_frontera(frontera)
        estado = nodo["estado"]

        if nodo["g"] > mejor_g.get(estado, float("inf")):
            traza.append(
                f"Descarta entrada obsoleta {estado} "
                f"(g={nodo['g']}, prioridad h={prioridad})"
            )
            continue

        traza.append(
            f"Extrae {estado} (g={nodo['g']}, h={nodo['h']}, "
            f"prioridad h={prioridad}); "
            f"frontera: {describir_frontera(frontera)}"
        )

        if estado == "G":
            return crear_resultado(
                nodo,
                generados,
                expandidos,
                frontera_maxima,
                mejoras_mejor_g,
                traza,
                "h",
            )

        expandidos += 1

        for sucesor, costo in GRAFO[estado]:
            nuevo_g = nodo["g"] + costo

            if nuevo_g < mejor_g.get(sucesor, float("inf")):

                if sucesor in mejor_g:
                    mejoras_mejor_g += 1

                mejor_g[sucesor] = nuevo_g

                hijo = crear_nodo(
                    sucesor,
                    padre=nodo,
                    accion=sucesor,
                    g=nuevo_g,
                )

                contador = insertar_en_frontera(
                    frontera, hijo, hijo["h"], contador
                )

                generados += 1

        frontera_maxima = max(
            frontera_maxima, len(frontera)
        )

    return None


# ============================================================
# 4. BUSQUEDA A*
# Prioridad: f(n) = g(n) + h(n)
# ============================================================

def busqueda_a_estrella():
    frontera = []
    contador = 0

    inicial = crear_nodo("S")
    contador = insertar_en_frontera(
        frontera, inicial, inicial["f"], contador
    )

    mejor_g = {"S": 0}

    generados = 1
    expandidos = 0
    frontera_maxima = 1
    mejoras_mejor_g = 0
    traza = []

    while frontera:
        prioridad, _, nodo = extraer_de_frontera(frontera)
        estado = nodo["estado"]

        if nodo["g"] > mejor_g.get(estado, float("inf")):
            traza.append(
                f"Descarta entrada obsoleta {estado} "
                f"(g={nodo['g']}, prioridad f={prioridad})"
            )
            continue

        traza.append(
            f"Extrae {estado} (g={nodo['g']}, h={nodo['h']}, "
            f"f={nodo['f']}, prioridad f={prioridad}); "
            f"frontera: {describir_frontera(frontera)}"
        )

        if estado == "G":
            return crear_resultado(
                nodo,
                generados,
                expandidos,
                frontera_maxima,
                mejoras_mejor_g,
                traza,
                "f",
            )

        expandidos += 1

        for sucesor, costo in GRAFO[estado]:
            nuevo_g = nodo["g"] + costo

            if nuevo_g < mejor_g.get(sucesor, float("inf")):

                if sucesor in mejor_g:
                    mejoras_mejor_g += 1

                mejor_g[sucesor] = nuevo_g

                hijo = crear_nodo(
                    sucesor,
                    padre=nodo,
                    accion=sucesor,
                    g=nuevo_g,
                )

                contador = insertar_en_frontera(
                    frontera, hijo, hijo["f"], contador
                )

                generados += 1

        frontera_maxima = max(
            frontera_maxima, len(frontera)
        )

    return None


# ============================================================
# 5. IMPRESION DE RESULTADOS Y TRAZAS
# ============================================================

def imprimir_traza(nombre, resultado):
    print(f"\n--- Traza: {nombre} ---")

    for numero, paso in enumerate(
        resultado["traza"], start=1
    ):
        print(f"{numero}. {paso}")


def imprimir_resultado(nombre, resultado):
    print(f"\n{nombre}")
    print(f"  Camino: {' -> '.join(resultado['camino'])}")
    print(f"  Costo: {resultado['costo']}")
    print(
        f"  Nodos generados: {resultado['generados']}"
    )
    print(
        "  Nodos expandidos antes de extraer G: "
        f"{resultado['expandidos']}"
    )
    print(
        f"  Frontera maxima: {resultado['frontera_maxima']}"
    )
    print(
        "  Mejoras de mejor_g en estados conocidos: "
        f"{resultado['mejoras_mejor_g']}"
    )


def mostrar_comparacion(resultados):
    print("\n=== TABLA COMPARATIVA ===")

    encabezado = (
        f"{'Algoritmo':<23}"
        f"{'Camino':<18}"
        f"{'Costo':<8}"
        f"{'Prioridad de G':<16}"
        f"{'Expandidos antes de G':<23}"
        f"{'Generados':<11}"
        f"{'Frontera max.':<15}"
        f"{'Mejoras':<9}"
    )

    print(encabezado)
    print("-" * len(encabezado))

    for nombre, resultado in resultados:
        camino = " -> ".join(resultado["camino"])

        print(
            f"{nombre:<23}"
            f"{camino:<18}"
            f"{resultado['costo']:<8}"
            f"{resultado['prioridad_objetivo']:<16}"
            f"{resultado['expandidos']:<23}"
            f"{resultado['generados']:<11}"
            f"{resultado['frontera_maxima']:<15}"
            f"{resultado['mejoras_mejor_g']:<9}"
        )


# ============================================================
# 6. PROGRAMA PRINCIPAL
# ============================================================

def main():
    print("TP2 - Busqueda voraz y A* sobre un grafo dirigido")
    print("Alumno: Lucas Manuel")

    print("\nGrafo dirigido:")
    for estado, vecinos in GRAFO.items():
        print(f"  {estado}: {vecinos}")

    print("\nHeuristica:")
    for estado, valor in HEURISTICA.items():
        print(f"  h({estado}) = {valor}")

    resultados = [
        ("Costo uniforme (UCS)", busqueda_costo_uniforme()),
        ("Busqueda voraz", busqueda_voraz()),
        ("A*", busqueda_a_estrella()),
    ]

    for nombre, resultado in resultados:
        imprimir_traza(nombre, resultado)
        imprimir_resultado(nombre, resultado)

    mostrar_comparacion(resultados)


if __name__ == "__main__":
    main()