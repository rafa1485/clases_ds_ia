"""
reportes.py

Funciones de presentación: transforman los resultados que devuelve
busqueda.buscar() en salida legible por consola (traza paso a paso
y tabla comparativa). No contienen lógica de búsqueda, solo formateo.
"""


def imprimir_traza(nombre_algoritmo, resultado):
    """
    Imprime, para un algoritmo dado, cada expansión registrada en la traza:
    qué estado se expandió, sus valores g/h/f, y cómo quedó la frontera
    inmediatamente después de extraerlo.
    """
    print(f"\n{'=' * 60}")
    print(f"TRAZA: {nombre_algoritmo}")
    print(f"{'=' * 60}")

    for i, paso in enumerate(resultado["traza"], start=1):
        print(f"\nPaso {i}: se expande '{paso['expandido']}' "
              f"(g={paso['g']}, h={paso['h']}, f={paso['f']})")
        if paso["frontera_restante"]:
            frontera_str = ", ".join(
                f"{estado}(prio={prioridad})"
                for prioridad, estado in paso["frontera_restante"]
            )
            print(f"  Frontera restante: [{frontera_str}]")
        else:
            print("  Frontera restante: []")

    print(f"\nCamino encontrado: {' -> '.join(resultado['camino']) if resultado['camino'] else 'NO ENCONTRADO'}")
    print(f"Costo total: {resultado['costo']}")


def imprimir_tabla_comparativa(resultados):
    """
    Imprime una tabla comparando los tres algoritmos.

    Parámetros:
        resultados: dict {nombre_algoritmo: resultado_de_buscar}
    """
    encabezado = (
        f"{'Algoritmo':<12} | {'Camino':<18} | {'Costo':<6} | "
        f"{'Prioridad usada':<16} | {'Generados':<10} | "
        f"{'Expandidos':<11} | {'Frontera máx':<13} | {'Reaperturas':<11}"
    )
    print(f"\n{'=' * len(encabezado)}")
    print("TABLA COMPARATIVA")
    print(f"{'=' * len(encabezado)}")
    print(encabezado)
    print("-" * len(encabezado))

    prioridad_por_algoritmo = {
        "UCS": "g",
        "Voraz": "h",
        "A*": "g + h",
    }

    for nombre, resultado in resultados.items():
        camino_str = " -> ".join(resultado["camino"]) if resultado["camino"] else "NO ENCONTRADO"
        print(
            f"{nombre:<12} | {camino_str:<18} | {str(resultado['costo']):<6} | "
            f"{prioridad_por_algoritmo.get(nombre, '?'):<16} | "
            f"{resultado['estados_generados']:<10} | "
            f"{resultado['estados_expandidos']:<11} | "
            f"{resultado['frontera_maxima']:<13} | "
            f"{resultado['reaperturas']:<11}"
        )