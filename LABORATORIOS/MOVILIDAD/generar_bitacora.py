"""Genera bitacora_agentes.csv a partir del escenario reproducible de la
consigna (zona 161, hora 8, taxis_x 20, horas_historia 3, semilla 42).

Requiere haber generado antes escenario_agente/percepciones.csv con el
comando de `consigna_agentes_movilidad.md`:

    python simulador_entorno_agente.py --zona 161 --hora 8 --taxis-x 20 \
        --horas-historia 3 --semilla 42 --salida-dir escenario_agente

Este script solo lee percepciones.csv (informacion hasta la hora h) y nunca
abre resultado_h_mas_1.csv, que esta reservado para evaluacion posterior.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from agentes_movilidad import procesar_secuencia

RUTA_PERCEPCIONES = Path("escenario_agente/percepciones.csv")
RUTA_BITACORA = Path("bitacora_agentes.csv")


def main() -> None:
    percepciones = pd.read_csv(RUTA_PERCEPCIONES)
    bitacora = procesar_secuencia(percepciones)
    bitacora.to_csv(RUTA_BITACORA, index=False)
    print(bitacora.to_string(index=False))
    print(f"Bitacora guardada en {RUTA_BITACORA.resolve()}")


if __name__ == "__main__":
    main()
