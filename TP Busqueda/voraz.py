import grafo

def crear_nodo(estado, padre=None, accion=None, g=0, h=0):
    return {
        "estado": estado,
        "padre": padre,
        "accion": accion,
        "g": g,
        "h": h,
        "f": h, #para voraz f=h
    }

def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append(nodo["estado"])
        nodo = nodo["padre"]
    camino.reverse()
    return camino

raiz = crear_nodo("S", g=0, h=grafo.HEURISTICA["S"])
#el algoritmo va a crear solo el grafo en base al archivo grafo
#nodo_a = crear_nodo("A",padre=raiz,accion="S -> A",g=2,h=5)

frontera = [raiz]
nodos_visitados = set()

while frontera:
    nodo = min(frontera, key=lambda n: n["f"])
    frontera.remove(nodo)

    if nodo["estado"] in nodos_visitados:
        continue
    nodos_visitados.add(nodo["estado"])

    if nodo["estado"] == "G":
        print("Camino:", " -> ".join(reconstruir_camino(nodo)))
        print("Costo total:", nodo["g"])
        break

    for vecino, costo in grafo.GRAFO[nodo["estado"]]:
        if vecino in nodos_visitados:
            continue
        nodo_vecino = crear_nodo(vecino, padre=nodo, accion=f"{nodo['estado']} -> {vecino}", g=nodo["g"] + costo, h=grafo.HEURISTICA[vecino])
        frontera.append(nodo_vecino)
else:
    print("No se encontro solucion")
