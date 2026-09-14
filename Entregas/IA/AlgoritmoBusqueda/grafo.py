# --- Representación del grafo ---

grafo = {
    "S": [("A", 2), ("B", 2)],
    "A": [("C", 2), ("D", 5)],
    "B": [("D", 2)],
    "C": [("G", 3)],
    "D": [("G", 6)],
    "G": []  # el objetivo no tiene salidas relevantes para este TP
}

# --- Heurística: estimación del costo restante hasta G ---
heuristica = {
    "S": 7,
    "A": 5,
    "B": 7,
    "C": 3,
    "D": 6,
    "G": 0
}

INICIO = "S"
OBJETIVO = "G"