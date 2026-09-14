"""
main.py

Se ejecuta UCS, Voraz y A* sobre el mismo grafo,
muestra la traza de cada uno y una tabla comparativa final.

Ejecutar con: python main.py
"""

from grafo import grafo, heuristica, INICIO, OBJETIVO
from busqueda import ucs, voraz, a_estrella
from reportes import imprimir_traza, imprimir_tabla_comparativa

# --- Identificación  ---
# Nombre : AGUSTIN BEADE

print("Estudiante: <AGUSTIN BEADE>")

# --- Ejecutar los tres algoritmos sobre el mismo problema ---
resultado_ucs = ucs(grafo, heuristica, INICIO, OBJETIVO)
resultado_voraz = voraz(grafo, heuristica, INICIO, OBJETIVO)
resultado_a_estrella = a_estrella(grafo, heuristica, INICIO, OBJETIVO)

# --- Mostrar la traza de cada uno ---
imprimir_traza("UCS", resultado_ucs)
imprimir_traza("Voraz", resultado_voraz)
imprimir_traza("A*", resultado_a_estrella)

# --- Tabla comparativa final ---
resultados = {
    "UCS": resultado_ucs,
    "Voraz": resultado_voraz,
    "A*": resultado_a_estrella,
}
imprimir_tabla_comparativa(resultados)