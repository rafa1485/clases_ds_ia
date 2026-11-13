import grafo

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
    while nodo is not None:
        camino.append(nodo["estado"])
        nodo = nodo["padre"]
    camino.reverse()
    return camino

raiz = crear_nodo("S", g=0, h=grafo.HEURISTICA["S"])

frontera = [raiz]
visitados = set()

while frontera:
    nodo = min(frontera, key=lambda n: n["f"])
    frontera.remove(nodo)

    if nodo["estado"] in visitados:
        continue
    visitados.add(nodo["estado"])

    if nodo["estado"] == "G":
        print("Camino:", " -> ".join(reconstruir_camino(nodo)))
        print("Costo total:", nodo["g"])
        break

    for vecino, costo in grafo.GRAFO[nodo["estado"]]:
        if vecino in visitados:
            continue
        g = nodo["g"] + costo
        h = grafo.HEURISTICA[vecino]
        nodo_vecino = crear_nodo(vecino, padre=nodo, accion=f"{nodo['estado']} -> {vecino}", g=g, h=h)
        frontera.append(nodo_vecino)
else:
    print("No se encontro solucion")
