"""
estructuras.py

Bloques de construcción reutilizados por los tres algoritmos de búsqueda
(UCS, Voraz, A*):

- crear_nodo(): arma un nodo de búsqueda como diccionario, guardando referencia
  al padre para poder reconstruir el camino al final.
- ColaPrioridad: envoltorio sobre heapq que agrega desempate estable por orden
  de inserción (FIFO), tal como exige la consigna cuando dos nodos tienen
  igual prioridad.
"""

import heapq
import itertools


"""
    Crea un nodo de búsqueda.

    Parámetros:
        estado: nombre del estado (ej. "S", "A", ...)
        padre:  nodo (dict) del cual se llegó a este estado, o None si es la raíz
        accion: descripción de la transición usada (ej. "S -> A")
        g:      costo acumulado desde el inicio hasta este nodo
        h:      estimación heurística del costo restante hasta el objetivo

    Devuelve:
        dict con las claves estado, padre, accion, g, h, f.
        'f' se calcula por defecto como g + h, pero cada algoritmo puede
        sobreescribirlo según qué prioridad use (g, h, o g+h).
    """
def crear_nodo(estado, padre=None, accion=None, g=0, h=0):
    return {
        "estado": estado,
        "padre": padre,
        "accion": accion,
        "g": g,
        "h": h,
        "f": g + h,
    }



"""
    Cola de prioridad mínima con desempate estable por orden de inserción.

    Por qué existe: heapq compara tuplas elemento por elemento. Si dos nodos
    tienen la misma prioridad, Python intentaría comparar el siguiente
    elemento de la tupla; si ese elemento es un dict (nuestro nodo), el
    programa falla porque los dicts no son comparables entre sí.

    La solución es insertar un contador incremental como segundo elemento
    de la tupla (prioridad, contador, nodo). Ante prioridades iguales,
    heapq desempata por contador, que refleja el orden de inserción:
    el nodo insertado antes tiene contador menor y sale primero (FIFO).
    """
class ColaPrioridad: 
    def __init__(self):
        self._heap = []
        self._contador = itertools.count() # genera 0, 1, 2, 3, ... sin repetir

    def insertar(self, prioridad, nodo):
        # Inserta nodo en la cola con la prioridad dada.
        contador = next(self._contador)
        heapq.heappush(self._heap, (prioridad, contador, nodo))
    
    def extraer(self):
        #Extrae y devuelve el nodo de menor prioridad (desempatando por FIFO)
        prioridad, contador, nodo = heapq.heappop(self._heap)
        return nodo
    
    def esta_vacia(self):
        # True si no quedan nodos en la frontera.
        return len(self._heap) == 0

    def contenido(self):
        # Devuelve una lista de (prioridad, estado) de todo lo que hay
        # actualmente en la frontera, ordenada por prioridad (y por FIFO
        # en caso de empate). Se usa solo para armar la traza; no afecta
        # el comportamiento de la búsqueda.

        return [(prioridad, nodo["estado"]) for prioridad, _, nodo in sorted(self._heap)]
    
    def __len__(self):
        return len(self._heap)
        