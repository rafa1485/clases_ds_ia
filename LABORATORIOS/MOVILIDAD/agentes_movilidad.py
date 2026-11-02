"""Trabajo practico de agentes de movilidad.

Autor: Ezequiel Zunino.

Las funciones de decision reciben solo la percepcion actual o el estado
interno. Ninguna consulta datos de h+1.

Uso: python agentes_movilidad.py [percepciones.csv] [bitacora.csv]
"""

from __future__ import annotations

import math
import sys
from collections.abc import Mapping
from numbers import Real
from typing import Any

import pandas as pd


ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85
HORAS_PRESION_PERSISTENTE = 2

CAMPOS_REQUERIDOS = ("presion", "capacidad_x")
CAMPOS_NO_NEGATIVOS = (
    "taxis_x",
    "demanda_total",
    "viajes_otras",
    "demanda_x",
    "viajes_atendibles_x",
    "demanda_no_cubierta_x",
)
COLUMNAS_BITACORA = [
    "hora",
    "presion",
    "racha_presion_alta",
    "accion_simple",
    "motivo_simple",
    "accion_modelo",
    "motivo_modelo",
]


def _es_numero(valor: Any) -> bool:
    """Indica si el valor es numerico, excluyendo booleanos y NaN."""
    return (
        isinstance(valor, Real)
        and not isinstance(valor, bool)
        and not math.isnan(valor)
    )


def _problema_percepcion(percepcion: Any) -> str | None:
    """Devuelve el problema de la percepcion, o None si es valida."""
    if not isinstance(percepcion, Mapping):
        return "la percepcion no es un registro de campos"

    for campo in CAMPOS_REQUERIDOS:
        if percepcion.get(campo) is None:
            return f"falta el dato requerido {campo}"
        if not _es_numero(percepcion[campo]):
            return f"{campo} no es un numero valido"

    capacidad = percepcion["capacidad_x"]
    presion = percepcion["presion"]
    if capacidad < 0 or math.isinf(capacidad):
        return "capacidad_x debe ser finita y no negativa"
    if presion < 0:
        return "presion no puede ser negativa"
    # El simulador informa presion infinita solo si hay demanda sin capacidad.
    if math.isinf(presion) and capacidad != 0:
        return "presion infinita con capacidad positiva"

    for campo in CAMPOS_NO_NEGATIVOS:
        if campo not in percepcion:
            continue
        valor = percepcion[campo]
        if not _es_numero(valor) or valor < 0 or math.isinf(valor):
            return f"{campo} no es un valor valido"

    if "tasa_otras_simulada" in percepcion:
        tasa = percepcion["tasa_otras_simulada"]
        if not _es_numero(tasa) or not 0 <= tasa <= 1:
            return "tasa_otras_simulada debe estar entre 0 y 1"

    return None


def decidir_reactivo_simple(percepcion: dict[str, Any]) -> tuple[str, str]:
    """Devuelve (accion, motivo) usando solo la percepcion actual."""
    problema = _problema_percepcion(percepcion)
    if problema is not None:
        return "ABSTENERSE", f"percepcion invalida: {problema}"

    presion = percepcion["presion"]
    if presion >= UMBRAL_PRESION:
        return (
            "RECOMENDAR_REFUERZO",
            f"presion {presion:.3f} >= umbral {UMBRAL_PRESION}",
        )
    return "NO_REFORZAR", f"presion {presion:.3f} < umbral {UMBRAL_PRESION}"


def crear_estado_inicial() -> dict[str, Any]:
    """Crea el estado persistente del agente reactivo basado en modelo."""
    return {
        "percepcion_valida": False,
        "racha_presion_alta": 0,
        "presion_anterior": None,
        "ultima_accion": None,
    }


def actualizar_estado(
    estado_anterior: dict[str, Any],
    percepcion: dict[str, Any],
) -> dict[str, Any]:
    """Actualiza la memoria a partir del estado anterior y la percepcion.

    Devuelve un estado nuevo. presion_anterior guarda la ultima presion
    valida, que sera la presion anterior en la proxima actualizacion. Un dato
    invalido corta la racha: no se puede afirmar que las horas sean seguidas.
    """
    estado = dict(estado_anterior)

    if _problema_percepcion(percepcion) is not None:
        estado["percepcion_valida"] = False
        estado["racha_presion_alta"] = 0
        estado["presion_anterior"] = None
        return estado

    presion = percepcion["presion"]
    estado["percepcion_valida"] = True
    if presion >= UMBRAL_PRESION:
        estado["racha_presion_alta"] = estado_anterior["racha_presion_alta"] + 1
    else:
        estado["racha_presion_alta"] = 0
    estado["presion_anterior"] = presion
    return estado


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""
    if not estado_actual["percepcion_valida"]:
        return "ABSTENERSE", "percepcion invalida: la racha queda en cero"

    racha = estado_actual["racha_presion_alta"]
    if racha >= HORAS_PRESION_PERSISTENTE:
        return "RECOMENDAR_REFUERZO", f"racha de {racha} horas con presion alta"
    if racha == 1:
        return "NO_REFORZAR", "primera hora con presion alta: falta persistencia"
    return "NO_REFORZAR", "presion por debajo del umbral: racha en cero"


def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes y construye la bitacora comparativa.

    Ordena por hora y supone que las horas son contiguas, como las que genera
    el simulador. Cada decision usa solo las filas ya recorridas.
    """
    estado = crear_estado_inicial()
    filas = []

    ordenadas = percepciones.sort_values("hora", kind="stable")
    for percepcion in ordenadas.to_dict("records"):
        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)

        estado = actualizar_estado(estado, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)
        estado["ultima_accion"] = accion_modelo

        filas.append(
            {
                "hora": percepcion["hora"],
                "presion": percepcion.get("presion"),
                "racha_presion_alta": estado["racha_presion_alta"],
                "accion_simple": accion_simple,
                "motivo_simple": motivo_simple,
                "accion_modelo": accion_modelo,
                "motivo_modelo": motivo_modelo,
            }
        )

    return pd.DataFrame(filas, columns=COLUMNAS_BITACORA)


def main() -> None:
    entrada = sys.argv[1] if len(sys.argv) > 1 else "escenario_agente/percepciones.csv"
    salida = sys.argv[2] if len(sys.argv) > 2 else "bitacora_agentes.csv"

    bitacora = procesar_secuencia(pd.read_csv(entrada))
    bitacora.to_csv(salida, index=False)
    print(bitacora.to_string(index=False))
    print(f"Bitacora guardada en {salida}")


if __name__ == "__main__":
    main()
