"""Trabajo práctico de búsqueda voraz y A* sobre un grafo dirigido.

Estudiante: Uriel Paul
Inteligencia Artificial — Semana 3, Clase 3

Ejecutar con Python 3. El programa usa solamente la biblioteca estándar.
"""

from __future__ import annotations

from heapq import heappop, heappush
from itertools import count
from math import inf
from typing import Any


GRAFO: dict[str, list[tuple[str, int]]] = {
    "S": [("A", 2), ("B", 2)],
    "A": [("C", 2), ("D", 5)],
    "B": [("D", 2)],
    "C": [("G", 3)],
    "D": [("G", 6)],
    "G": [],
}

HEURISTICA: dict[str, int] = {
    "S": 7,
    "A": 5,
    "B": 7,
    "C": 3,
    "D": 6,
    "G": 0,
}

INICIAL = "S"
OBJETIVO = "G"
ALGORITMOS = ("UCS", "Voraz", "A*")


def crear_nodo(
    estado: str,
    padre: dict[str, Any] | None = None,
    accion: str | None = None,
    g: int = 0,
    h: int = 0,
) -> dict[str, Any]:
    """Crea el nodo con la información común a las tres búsquedas."""
    return {
        "estado": estado,
        "padre": padre,
        "accion": accion,
        "g": g,
        "h": h,
        "f": g + h,
    }


def reconstruir_camino(nodo: dict[str, Any]) -> list[str]:
    """Reconstruye el camino recorriendo los padres desde la meta."""
    camino: list[str] = []
    actual: dict[str, Any] | None = nodo
    while actual is not None:
        camino.append(actual["estado"])
        actual = actual["padre"]
    camino.reverse()
    return camino


def calcular_prioridad(algoritmo: str, nodo: dict[str, Any]) -> int:
    """Devuelve g para UCS, h para voraz y g+h para A*."""
    if algoritmo == "UCS":
        return nodo["g"]
    if algoritmo == "Voraz":
        return nodo["h"]
    if algoritmo == "A*":
        return nodo["f"]
    raise ValueError(f"Algoritmo desconocido: {algoritmo}")


def describir_frontera(
    frontera: list[tuple[int, int, dict[str, Any]]],
    mejor_g: dict[str, int],
) -> str:
    """Muestra la cola ordenada y marca las entradas que ya son obsoletas."""
    if not frontera:
        return "(vacía)"

    partes: list[str] = []
    for prioridad, _, nodo in sorted(frontera, key=lambda entrada: (entrada[0], entrada[1])):
        obsoleto = nodo["g"] != mejor_g.get(nodo["estado"], inf)
        marca = ", obsoleto" if obsoleto else ""
        partes.append(f"{nodo['estado']}(p={prioridad}, g={nodo['g']}{marca})")
    return "; ".join(partes)


def buscar(algoritmo: str, heuristica: dict[str, int] | None = None) -> dict[str, Any]:
    """Ejecuta una búsqueda y devuelve camino, métricas y traza completa."""
    h = HEURISTICA if heuristica is None else heuristica
    orden = count()
    raiz = crear_nodo(INICIAL, g=0, h=h[INICIAL])
    frontera: list[tuple[int, int, dict[str, Any]]] = []
    heappush(frontera, (calcular_prioridad(algoritmo, raiz), next(orden), raiz))

    mejor_g = {INICIAL: 0}
    generados = 1
    expandidos = 0
    reaperturas = 0
    obsoletos_descartados = 0
    frontera_maxima = 1
    traza: list[dict[str, Any]] = []

    while frontera:
        frontera_antes = describir_frontera(frontera, mejor_g)
        prioridad, _, nodo = heappop(frontera)
        estado = nodo["estado"]

        if nodo["g"] != mejor_g.get(estado, inf):
            obsoletos_descartados += 1
            traza.append(
                {
                    "estado": f"{estado} (g={nodo['g']})",
                    "prioridad": prioridad,
                    "frontera": describir_frontera(frontera, mejor_g),
                    "detalle": "Entrada obsoleta descartada; no se expanden sucesores.",
                    "frontera_antes": frontera_antes,
                }
            )
            continue

        if estado == OBJETIVO:
            traza.append(
                {
                    "estado": estado,
                    "prioridad": prioridad,
                    "frontera": describir_frontera(frontera, mejor_g),
                    "detalle": "Objetivo alcanzado al extraer; no se expande.",
                    "frontera_antes": frontera_antes,
                }
            )
            return {
                "algoritmo": algoritmo,
                "camino": reconstruir_camino(nodo),
                "costo": nodo["g"],
                "generados": generados,
                "expandidos": expandidos,
                "frontera_maxima": frontera_maxima,
                "reaperturas": reaperturas,
                "obsoletos_descartados": obsoletos_descartados,
                "traza": traza,
            }

        expandidos += 1
        cambios: list[str] = []
        for sucesor, costo in GRAFO[estado]:
            nuevo_g = nodo["g"] + costo
            if nuevo_g < mejor_g.get(sucesor, inf):
                if sucesor in mejor_g:
                    anterior = mejor_g[sucesor]
                    reaperturas += 1
                    cambios.append(f"{sucesor}: g mejora de {anterior} a {nuevo_g}")
                else:
                    cambios.append(f"{sucesor}: g={nuevo_g}")

                mejor_g[sucesor] = nuevo_g
                hijo = crear_nodo(
                    sucesor,
                    padre=nodo,
                    accion=f"{estado} -> {sucesor}",
                    g=nuevo_g,
                    h=h[sucesor],
                )
                heappush(
                    frontera,
                    (calcular_prioridad(algoritmo, hijo), next(orden), hijo),
                )
                generados += 1
            else:
                cambios.append(f"{sucesor}: g={nuevo_g}, sin mejora")

        frontera_maxima = max(frontera_maxima, len(frontera))
        traza.append(
            {
                "estado": estado,
                "prioridad": prioridad,
                "frontera": describir_frontera(frontera, mejor_g),
                "detalle": "; ".join(cambios) if cambios else "Sin sucesores.",
                "frontera_antes": frontera_antes,
            }
        )

    return {
        "algoritmo": algoritmo,
        "camino": None,
        "costo": inf,
        "generados": generados,
        "expandidos": expandidos,
        "frontera_maxima": frontera_maxima,
        "reaperturas": reaperturas,
        "obsoletos_descartados": obsoletos_descartados,
        "traza": traza,
    }


def mostrar_grafo_y_heuristica() -> None:
    print("ESTUDIANTE: Uriel Paul")
    print("Trabajo práctico: búsqueda voraz y A* sobre un grafo dirigido")
    print("\nGrafo dirigido y costos:")
    for estado, sucesores in GRAFO.items():
        aristas = ", ".join(f"{estado}->{destino} ({costo})" for destino, costo in sucesores)
        print(f"  {aristas if aristas else estado + ': sin sucesores'}")
    print("\nHeurística h(n):")
    print("  " + ", ".join(f"h({estado})={valor}" for estado, valor in HEURISTICA.items()))
    print("  Desempates: FIFO por orden de inserción.")


def mostrar_traza(resultado: dict[str, Any]) -> None:
    print(f"\n=== {resultado['algoritmo']} ===")
    print("Paso | Extraído (prioridad) | Frontera luego del evento | Resultado")
    print("-" * 110)
    for paso, evento in enumerate(resultado["traza"], start=1):
        print(
            f"{paso:>4} | {evento['estado']} ({evento['prioridad']}) | "
            f"{evento['frontera']} | {evento['detalle']}"
        )
    camino = " -> ".join(resultado["camino"]) if resultado["camino"] else "Sin solución"
    print(f"Camino: {camino}; costo: {resultado['costo']}")
    print(
        f"Generados: {resultado['generados']}; expandidos: {resultado['expandidos']}; "
        f"frontera máxima: {resultado['frontera_maxima']}; "
        f"reaperturas: {resultado['reaperturas']}; "
        f"entradas obsoletas descartadas: {resultado['obsoletos_descartados']}"
    )


def mostrar_comparacion(resultados: dict[str, dict[str, Any]]) -> None:
    print("\nTabla comparativa")
    print("| Resultado | UCS | Voraz | A* |")
    print("|---|---:|---:|---:|")
    filas = (
        ("Camino", lambda r: " -> ".join(r["camino"]) if r["camino"] else "Sin solución"),
        ("Costo", lambda r: str(r["costo"])),
        ("Prioridad", lambda r: {"UCS": "g", "Voraz": "h", "A*": "g+h"}[r["algoritmo"]]),
        ("Expandidos antes de extraer G", lambda r: str(r["expandidos"])),
        ("Generados", lambda r: str(r["generados"])),
        ("Frontera máxima", lambda r: str(r["frontera_maxima"])),
        ("Reaperturas", lambda r: str(r["reaperturas"])),
    )
    for etiqueta, extraer in filas:
        valores = " | ".join(extraer(resultados[nombre]) for nombre in ALGORITMOS)
        print(f"| {etiqueta} | {valores} |")


def mostrar_experimento_heuristica_nula(ucs: dict[str, Any]) -> None:
    """Muestra que A* con h=0 tiene prioridad g, como UCS."""
    h_nula = {estado: 0 for estado in GRAFO}
    a_h0 = buscar("A*", heuristica=h_nula)
    metricas = ("camino", "costo", "generados", "expandidos", "frontera_maxima", "reaperturas")
    print("\nExperimento: A* con h=0 frente a UCS")
    for metrica in metricas:
        print(f"  {metrica}: UCS={ucs[metrica]} | A*(h=0)={a_h0[metrica]}")
    coinciden = all(ucs[metrica] == a_h0[metrica] for metrica in metricas)
    print(f"  Coinciden en las métricas comparadas: {'sí' if coinciden else 'no'}.")


def mostrar_respuestas() -> None:
    print("\nRespuestas de análisis")
    print(
        "1. Voraz y A* coinciden en esta instancia porque ambos prefieren A frente a B "
        "desde S y C frente a D desde A. Sobre el camino óptimo, h coincide con el "
        "costo real restante: h(S)=7, h(A)=5, h(C)=3 y h(G)=0. Esto explica la "
        "coincidencia en este grafo, pero no da optimalidad general a voraz."
    )
    print(
        "2. Voraz no garantiza el camino de menor costo: ordena únicamente por h y "
        "no incorpora g, el costo ya recorrido. Puede elegir una ruta que parece "
        "cercana a la meta aunque su costo acumulado sea alto."
    )
    print(
        "3. Con h=0, A* prioriza f=g+h=g; con el mismo grafo y desempate se comporta "
        "como UCS. El experimento anterior compara sus métricas."
    )
    print(
        "4. UCS registra una reapertura según la definición de la consigna: D mejora "
        "de g=7 a g=4 al descubrirse la ruta por B. D todavía estaba en la frontera. "
        "A* no registra reaperturas porque su heurística es consistente; voraz no "
        "registra ninguna porque alcanza G antes de expandir B y producir una mejora."
    )
    print(
        "5. Expandir menos mide trabajo de búsqueda, no costo de la solución. Aquí "
        "voraz expande menos que UCS y ambos encuentran costo 7, pero solo UCS y A* "
        "garantizan optimalidad bajo las condiciones correspondientes. A* alcanza "
        "el costo 7 con menos expansiones que UCS gracias a la heurística consistente."
    )


def main() -> None:
    mostrar_grafo_y_heuristica()
    resultados = {nombre: buscar(nombre) for nombre in ALGORITMOS}
    for nombre in ALGORITMOS:
        mostrar_traza(resultados[nombre])
    mostrar_comparacion(resultados)
    mostrar_experimento_heuristica_nula(resultados["UCS"])
    mostrar_respuestas()


if __name__ == "__main__":
    main()
