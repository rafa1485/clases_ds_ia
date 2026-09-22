"""
Trabajo práctico: búsqueda voraz y A* sobre un grafo dirigido
Curso: Inteligencia Artificial · Semana 3, clase 3 · Modalidad: individual

Estudiante: Milagros Idiarte

Implementa UCS (costo uniforme), Voraz (mejor primero) y A* sobre el mismo
grafo de 6 estados (S, A, B, C, D, G), comparando camino, costo y estados
expandidos, y respondiendo las 5 preguntas de análisis de la consigna.
"""

import heapq


# 1. Representación del problema: P = (S, A, T, s0, G, c)


# Grafo dirigido: estado -> lista de (sucesor, costo de la arista)
GRAFO = {
    "S": [("A", 2), ("B", 2)],
    "A": [("C", 2), ("D", 5)],
    "B": [("D", 2)],
    "C": [("G", 3)],
    "D": [("G", 6)],
    "G": [],
}

# Heurística h(n): estimación del costo restante hasta G
H = {"S": 7, "A": 5, "B": 7, "C": 3, "D": 6, "G": 0}

INICIO = "S"
OBJETIVOS = {"G"}



# 2. Estructura de nodo y reconstrucción de camino


def crear_nodo(estado, padre=None, accion=None, g=0, h=0):
    return {
        "estado": estado,
        "padre": padre,
        "accion": accion,
        "g": g,
        "h": h,
        "f": g + h,
    }


def reconstruir_camino(nodo):
    camino = []
    actual = nodo
    while actual is not None:
        camino.append(actual["estado"])
        actual = actual["padre"]
    camino.reverse()
    return camino



# 3. Esqueleto de búsqueda común (UCS / Voraz / A*)
#    Cambia únicamente la clave de prioridad de la frontera.


def buscar(modo, verbose=True):
    """
    modo: 'ucs'        -> prioridad = g
          'voraz'      -> prioridad = h
          'a_estrella' -> prioridad = g + h

    Devuelve un diccionario con camino, costo, estados generados,
    estados expandidos, frontera máxima, reaperturas y traza completa.
    """
    assert modo in ("ucs", "voraz", "a_estrella")

    def prioridad(nodo):
        if modo == "ucs":
            return nodo["g"]
        elif modo == "voraz":
            return nodo["h"]
        else:  # a_estrella
            return nodo["g"] + nodo["h"]

    contador = 0  # orden de inserción -> desempate FIFO estable ante empates
    frontera = []
    raiz = crear_nodo(INICIO, g=0, h=H[INICIO])
    heapq.heappush(frontera, (prioridad(raiz), contador, raiz))
    contador += 1

    mejor_g = {INICIO: 0}
    generados = 1
    expandidos = 0
    frontera_maxima = 1
    reaperturas = 0
    traza = []

    while frontera:
        frontera_maxima = max(frontera_maxima, len(frontera))
        _, _, nodo = heapq.heappop(frontera)
        estado = nodo["estado"]

        # Control de obsolescencia: solo UCS y A* lo aplican (según pseudocódigo
        # de la consigna, Voraz comprueba el objetivo directamente al extraer).
        if modo in ("ucs", "a_estrella") and nodo["g"] > mejor_g.get(estado, float("inf")):
            continue

        expandidos += 1
        contenido_frontera = sorted(
            [(round(p, 2), n["estado"]) for p, _, n in frontera]
        )
        traza.append({
            "expandido": estado,
            "g": nodo["g"], "h": nodo["h"], "f": nodo["f"],
            "frontera": contenido_frontera,
        })

        if estado in OBJETIVOS:
            resultado = {
                "modo": modo,
                "camino": reconstruir_camino(nodo),
                "costo": nodo["g"],
                "generados": generados,
                "expandidos": expandidos,
                "frontera_maxima": frontera_maxima,
                "reaperturas": reaperturas,
                "traza": traza,
            }
            if verbose:
                imprimir_traza(modo, traza)
            return resultado

        for vecino, costo in GRAFO[estado]:
            nuevo_g = nodo["g"] + costo
            if nuevo_g < mejor_g.get(vecino, float("inf")):
                if vecino in mejor_g:
                    reaperturas += 1
                mejor_g[vecino] = nuevo_g
                hijo = crear_nodo(vecino, padre=nodo, accion=f"{estado} -> {vecino}",
                                   g=nuevo_g, h=H[vecino])
                heapq.heappush(frontera, (prioridad(hijo), contador, hijo))
                contador += 1
                generados += 1

    if verbose:
        imprimir_traza(modo, traza)
    return None  # fracaso (no debería ocurrir en este grafo)



# 4. Impresión de traza


NOMBRES = {"ucs": "COSTO UNIFORME (UCS)", "voraz": "VORAZ", "a_estrella": "A*"}


def imprimir_traza(modo, traza):
    print(f"\n--- Traza de {NOMBRES[modo]} ---")
    for paso in traza:
        print(f"  Expandido: {paso['expandido']:<2} "
              f"(g={paso['g']}, h={paso['h']}, f={paso['f']}) "
              f"| Frontera tras extraer: {paso['frontera']}")



# 5. Ejecución de los tres algoritmos y tabla comparativa


def tabla_comparativa(resultados):
    prioridad_txt = {"ucs": "g", "voraz": "h", "a_estrella": "g + h"}
    print("\n" + "=" * 72)
    print("TABLA COMPARATIVA")
    print("=" * 72)
    encabezado = f"{'':<28}{'UCS':<15}{'Voraz':<15}{'A*':<15}"
    print(encabezado)
    print("-" * 72)

    def fila(nombre, clave, transform=lambda x: x, ancho=15):
        vals = [transform(resultados[m][clave]) for m in ("ucs", "voraz", "a_estrella")]
        print(f"{nombre:<28}{vals[0]!s:<{ancho}}{vals[1]!s:<{ancho}}{vals[2]!s:<{ancho}}")

    fila("Camino", "camino", lambda c: " -> ".join(c), ancho=18)
    fila("Costo", "costo")
    print(f"{'Prioridad':<28}{prioridad_txt['ucs']:<15}{prioridad_txt['voraz']:<15}{prioridad_txt['a_estrella']:<15}")
    fila("Expandidos hasta extraer G", "expandidos")
    fila("Estados generados", "generados")
    fila("Frontera máxima", "frontera_maxima")
    fila("Reaperturas", "reaperturas")


def main():
    resultados = {}
    for modo in ("ucs", "voraz", "a_estrella"):
        resultados[modo] = buscar(modo)

    tabla_comparativa(resultados)

    print("\n" + "=" * 72)
    print("PREGUNTAS DE ANÁLISIS")
    print("=" * 72)

    print("""
1) ¿Por qué voraz y A* coinciden en este grafo?
   Porque la heurística usada baja de forma consistente en el camino
   S -> A -> C -> G (7, 5, 3, 0) y ese descenso de h coincide, en este
   grafo puntual, con el camino de menor costo real. Voraz elige en cada
   paso el sucesor de menor h sin mirar g, y aquí esa elección "miope"
   resulta ser también la óptima, por lo que ambos algoritmos expanden
   la misma secuencia de estados y devuelven el mismo camino. Esto no es
   una propiedad general del algoritmo voraz, sino una particularidad de
   este grafo y esta heurística.

2) ¿Garantiza voraz el camino de menor costo en general?
   No. La prioridad de voraz es únicamente h(n): ignora por completo el
   costo ya recorrido (g). Esto significa que puede seguir un camino cuya
   h decrece rápido pero cuyas aristas reales son costosas, dejando de
   lado otro camino con h algo mayor pero de costo total menor. A
   diferencia de A* (que sí es óptimo cuando h es admisible, porque su
   prioridad incluye g), voraz no tiene ninguna garantía de optimalidad.

3) ¿Qué ocurre si se usa h = 0 en A*?
   La prioridad f = g + h se reduce a f = g, que es exactamente el
   criterio de UCS. Es decir, A* con h = 0 se comporta idénticamente a
   costo uniforme: UCS puede verse como un caso particular de A* con la
   heurística trivial h(n) = 0 para todo n.

4) ¿Hubo reaperturas en UCS? ¿Y en A* y voraz? ¿Por qué?
   En UCS sí hubo una reapertura: el estado D se alcanza primero vía
   A (g=7) y luego, al expandir B, se encuentra un camino más barato
   S -> B -> D (g=4), que mejora mejor_g[D] y reabre ese nodo. En voraz
   y en A*, en cambio, no hubo reaperturas en esta ejecución, porque en
   ambos casos el objetivo G se alcanza (vía S -> A -> C -> G) antes de
   que B llegue a expandirse; como B nunca se expande, D solo se inserta
   una vez (vía A) y nunca se vuelve a relajar.

5) ¿"Expandir menos estados" significa "camino más barato"?
   No. La cantidad de estados expandidos mide la eficiencia/rapidez de
   la búsqueda, no la calidad de la solución encontrada. En este grafo,
   voraz expandió menos estados que UCS (4 contra 6) pero llegó al mismo
   costo óptimo (7); eso fue posible porque la heurística lo guió bien,
   no porque "expandir menos" garantice nada. En general, voraz podría
   expandir pocos estados y aun así devolver un camino subóptimo,
   mientras que UCS garantiza el camino de menor costo aunque para ello
   necesite expandir más estados.
""")


if __name__ == "__main__":
    main()
