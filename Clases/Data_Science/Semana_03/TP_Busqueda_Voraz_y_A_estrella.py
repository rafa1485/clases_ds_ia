"""
================================================================================
TRABAJO PRACTICO: BUSQUEDA VORAZ Y A* SOBRE UN GRAFO DIRIGIDO
Curso: Inteligencia Artificial / Data Science
Semana 3, Clase 3
Modalidad: Individual
Entregable: Script ejecutable con trazas, metricas y analisis conceptual
================================================================================
"""

import heapq
from typing import Dict, List, Tuple, Any, Optional

# ==============================================================================
# 1. MODELADO DEL GRAFO Y LA HEURISTICA
# ==============================================================================
GRAFO: Dict[str, List[Tuple[str, int]]] = {
    'S': [('A', 2), ('B', 2)],
    'A': [('C', 2), ('D', 5)],
    'B': [('D', 2)],
    'C': [('G', 3)],
    'D': [('G', 6)],
    'G': []
}

HEURISTICA: Dict[str, int] = {
    'S': 7,
    'A': 5,
    'B': 7,
    'C': 3,
    'D': 6,
    'G': 0
}

ESTADO_INICIAL = 'S'
ESTADO_OBJETIVO = 'G'

# ==============================================================================
# 2. ESTRUCTURA DE DATOS Y ESQUEMA COMUN
# ==============================================================================
def crear_nodo(estado: str, padre: Optional[Dict[str, Any]] = None, 
               accion: Optional[str] = None, g: float = 0, h: float = 0, f: float = 0) -> Dict[str, Any]:
    return {
        'estado': estado,
        'padre': padre,
        'accion': accion,
        'g': g,
        'h': h,
        'f': f
    }

def reconstruir_camino(nodo_meta: Dict[str, Any]) -> List[str]:
    camino = []
    actual = nodo_meta
    while actual is not None:
        camino.append(actual['estado'])
        actual = actual['padre']
    return camino[::-1]

def resolver_busqueda(grafo: Dict[str, List[Tuple[str, int]]],
                      heuristica: Dict[str, int],
                      inicio: str,
                      objetivo: str,
                      estrategia: str,
                      verbose: bool = True) -> Dict[str, Any]:
    estrategia = estrategia.upper()
    if estrategia not in ['UCS', 'VORAZ', 'A*']:
        raise ValueError(f"Estrategia desconocida: {estrategia}")

    g_ini = 0
    h_ini = heuristica[inicio]
    if estrategia == 'UCS':
        f_ini = g_ini
    elif estrategia == 'VORAZ':
        f_ini = h_ini
    else:  # A*
        f_ini = g_ini + h_ini

    nodo_raiz = crear_nodo(inicio, padre=None, accion=None, g=g_ini, h=h_ini, f=f_ini)
    contador_insercion = 0
    frontera: List[Tuple[float, int, Dict[str, Any]]] = []
    heapq.heappush(frontera, (nodo_raiz['f'], contador_insercion, nodo_raiz))
    contador_insercion += 1

    mejor_g: Dict[str, float] = {inicio: 0}
    estados_generados = 1
    estados_expandidos = 0
    max_frontera = 1
    reaperturas = 0
    traza = []
    paso = 0

    if verbose:
        print(f"\n{'='*75}")
        print(f" ESTRATEGIA: {estrategia}")
        print(f"{'='*75}")

    while frontera:
        max_frontera = max(max_frontera, len(frontera))
        prio_f, _, nodo_actual = heapq.heappop(frontera)
        estado_actual = nodo_actual['estado']

        # Descarte de nodos obsoletos (Lazy Deletion)
        if estrategia in ['UCS', 'A*'] and nodo_actual['g'] > mejor_g[estado_actual]:
            if verbose:
                print(f"  [Descarte Obsoleto] Estado '{estado_actual}' con g={nodo_actual['g']} superado por mejor_g={mejor_g[estado_actual]}")
            continue

        paso += 1
        items_frontera = [(f, n['estado'], n['g'], n['h']) for f, _, n in sorted(frontera)]
        info_paso = {
            'paso': paso,
            'extrae': estado_actual,
            'g': nodo_actual['g'],
            'h': nodo_actual['h'],
            'f': nodo_actual['f'],
            'frontera_restante': items_frontera
        }
        traza.append(info_paso)

        if verbose:
            str_frontera = ", ".join([f"{e}(f={f}, g={g}, h={h})" for f, e, g, h in items_frontera]) or "vacia"
            print(f"Paso {paso}: Extrae '{estado_actual}' [f={nodo_actual['f']}, g={nodo_actual['g']}, h={nodo_actual['h']}] | Frontera: [{str_frontera}]")

        # Comprobacion de meta AL EXTRAER
        if estado_actual == objetivo:
            camino = reconstruir_camino(nodo_actual)
            costo_total = nodo_actual['g']
            if verbose:
                print(f"\n  -> META ALCANZADA! Camino: {' -> '.join(camino)} | Costo: {costo_total}")
            return {
                'algoritmo': estrategia,
                'camino': camino,
                'costo': costo_total,
                'expandidos': estados_expandidos,
                'generados': estados_generados,
                'max_frontera': max_frontera,
                'reaperturas': reaperturas,
                'traza': traza
            }

        estados_expandidos += 1

        for sucesor, costo_arista in grafo.get(estado_actual, []):
            nuevo_g = nodo_actual['g'] + costo_arista
            nuevo_h = heuristica[sucesor]
            estados_generados += 1

            if estrategia == 'UCS':
                nuevo_f = nuevo_g
            elif estrategia == 'VORAZ':
                nuevo_f = nuevo_h
            else:  # A*
                nuevo_f = nuevo_g + nuevo_h

            if sucesor not in mejor_g or nuevo_g < mejor_g[sucesor]:
                if sucesor in mejor_g:
                    reaperturas += 1
                    if verbose:
                        print(f"    * Reapertura de '{sucesor}': g anterior={mejor_g[sucesor]} -> nuevo g={nuevo_g}")
                mejor_g[sucesor] = nuevo_g
                nuevo_nodo = crear_nodo(
                    estado=sucesor,
                    padre=nodo_actual,
                    accion=f"{estado_actual} -> {sucesor}",
                    g=nuevo_g,
                    h=nuevo_h,
                    f=nuevo_f
                )
                heapq.heappush(frontera, (nuevo_f, contador_insercion, nuevo_nodo))
                contador_insercion += 1
                if verbose:
                    print(f"    + Inserta '{sucesor}' con f={nuevo_f} (g={nuevo_g}, h={nuevo_h})")
            else:
                if verbose:
                    print(f"    - Poda '{sucesor}': nuevo g={nuevo_g} >= mejor_g={mejor_g[sucesor]}")

    raise RuntimeError("Frontera vacia sin alcanzar el objetivo.")

def main():
    print("\n" + "#" * 75)
    print(" EJECUTANDO TRAZAS DE UCS, VORAZ Y A* SOBRE EL GRAFO DIDACTICO")
    print("#" * 75)

    res_ucs = resolver_busqueda(GRAFO, HEURISTICA, ESTADO_INICIAL, ESTADO_OBJETIVO, 'UCS')
    res_voraz = resolver_busqueda(GRAFO, HEURISTICA, ESTADO_INICIAL, ESTADO_OBJETIVO, 'VORAZ')
    res_astar = resolver_busqueda(GRAFO, HEURISTICA, ESTADO_INICIAL, ESTADO_OBJETIVO, 'A*')

    print("\n" + "=" * 75)
    print(" TABLA COMPARATIVA (SECCION 5)")
    print("=" * 75)
    header = f"{'Metrica / Propiedad':<38} | {'UCS':<10} | {'Voraz':<10} | {'A*':<10}"
    print(header)
    print("-" * len(header))
    print(f"{'Camino devuelto':<38} | {' -> '.join(res_ucs['camino']):<10} | {' -> '.join(res_voraz['camino']):<10} | {' -> '.join(res_astar['camino']):<10}")
    print(f"{'Costo total':<38} | {res_ucs['costo']:<10} | {res_voraz['costo']:<10} | {res_astar['costo']:<10}")
    print(f"{'Formula de prioridad':<38} | {'g':<10} | {'h':<10} | {'g + h':<10}")
    print(f"{'Expandidos antes de extraer G':<38} | {res_ucs['expandidos']:<10} | {res_voraz['expandidos']:<10} | {res_astar['expandidos']:<10}")
    print(f"{'Estados generados':<38} | {res_ucs['generados']:<10} | {res_voraz['generados']:<10} | {res_astar['generados']:<10}")
    print(f"{'Tamano maximo de frontera':<38} | {res_ucs['max_frontera']:<10} | {res_voraz['max_frontera']:<10} | {res_astar['max_frontera']:<10}")
    print(f"{'Reaperturas':<38} | {res_ucs['reaperturas']:<10} | {res_voraz['reaperturas']:<10} | {res_astar['reaperturas']:<10}")
    print("-" * len(header))

    print("\n" + "=" * 75)
    print(" RESPUESTAS A LAS PREGUNTAS DE ANALISIS (SECCION 6)")
    print("=" * 75)
    
    respuestas = [
        ("1. Por que voraz y A* coinciden en este grafo? Que condicion lo explica?",
         "Coinciden porque la heuristica h(n) es PERFECTA (exacta, h(n) = h*(n)) a lo largo del camino optimo S -> A -> C -> G:\n"
         "  h(S)=7 (real 2+2+3=7), h(A)=5 (real 2+3=5), h(C)=3 (real 3), h(G)=0.\n"
         "Al ser monotona y exacta en esa rama, Voraz se deja guiar directamente por el gradiente sin equivocarse,\n"
         "mientras que A* mantiene f = g + h = 7 en toda la trayectoria optima, superando en prioridad a cualquier rama lateral."),
        
        ("2. Garantiza voraz devolver el camino de menor costo en general?",
         "NO. Voraz minimiza exclusivamente h(n), ignorando por completo el costo acumulado g(n).\n"
         "Un sucesor con h muy bajo pero un g astronomico siempre sera preferido por Voraz frente a un camino\n"
         "con costo g minimo pero heuristica ligeramente mayor. No ofrece garantia formal de admisibilidad."),
        
        ("3. Que ocurre si se usa h = 0 en A*? Con que algoritmo coincide entonces?",
         "Si h(n) = 0 para todo n, la funcion f(n) = g(n) + 0 = g(n).\n"
         "En ese caso, A* se reduce IDENTICAMENTE a Busqueda de Costo Uniforme (UCS / Dijkstra).\n"
         "Las curvas de nivel se vuelven circulos concentricos de isocosto g en lugar de buscar la meta."),
        
        ("4. Hubo reaperturas en UCS? Y en A* y voraz? Por que?",
         "En UCS SI hubo 1 reapertura en el estado D: primero se descubrio via A con g = 2+5 = 7,\n"
         "y luego via B con g = 2+2 = 4 (menor). Al mejorar g, D se volvio a insertar.\n"
         "En A* y Voraz NO hubo reaperturas (0): la heuristica los condujo directamente a G sin llegar a expandir B,\n"
         "por lo que la ruta alternativa a D nunca fue explorada. Ademas, h es consistente en A*."),
        
        ("5. 'Expandir menos estados' significa 'camino mas barato'?",
         "NO. Expandir estados mide esfuerzo computacional (tiempo/espacio), no la calidad de la solucion (costo).\n"
         "Voraz aqui expandio menos nodos (3 vs 5) porque la heuristica fue perfecta. Si la arista C -> G costara 100,\n"
         "Voraz seguiria devolviendo el camino caro (costo 104) en 3 expansiones, mientras que UCS expandiria mas\n"
         "estados para encontrar la ruta barata (S -> B -> D -> G, costo 10).")
    ]

    for titulo, contenido in respuestas:
        print(f"\n[+] {titulo}")
        print(f"    {contenido}")

if __name__ == '__main__':
    main()
