"""Agentes reactivos para el refuerzo de taxis.

Implementa un agente reactivo simple y un agente reactivo basado en modelo
que recomiendan si conviene reforzar la flota de una empresa ficticia X en
la hora siguiente, usando exclusivamente informacion hasta la hora actual.
"""

from __future__ import annotations

import math
from typing import Any

import pandas as pd


ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85

# Campos que deben estar presentes y ser numericos validos para poder decidir.
CAMPOS_REQUERIDOS = ("presion", "capacidad_x")


def _es_numero_valido(valor: Any) -> bool:
    if valor is None:
        return False
    if isinstance(valor, bool):
        return False
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return False
    return math.isfinite(numero)


def _percepcion_valida(percepcion: dict[str, Any]) -> bool:
    """Valida que la percepcion tenga los campos requeridos y sean usables.

    Se considera invalida cuando falta un campo, cuando el valor no es un
    numero finito (incluye NaN e infinitos, que surgen cuando la capacidad
    es cero y por lo tanto la presion queda indefinida) o cuando la
    capacidad reportada no es positiva, es decir, la capacidad de X es
    desconocida o nula.
    """
    for campo in CAMPOS_REQUERIDOS:
        if campo not in percepcion or not _es_numero_valido(percepcion[campo]):
            return False

    if float(percepcion["capacidad_x"]) <= 0:
        return False
    if float(percepcion["presion"]) < 0:
        return False

    return True


def decidir_reactivo_simple(percepcion: dict[str, Any]) -> tuple[str, str]:
    """Devuelve (accion, motivo) usando solo la percepcion actual."""
    if not _percepcion_valida(percepcion):
        return (
            "ABSTENERSE",
            "Percepcion invalida, incompleta o con capacidad desconocida.",
        )

    presion = float(percepcion["presion"])
    if presion >= UMBRAL_PRESION:
        return (
            "RECOMENDAR_REFUERZO",
            f"Presion actual {presion:.2f} >= umbral {UMBRAL_PRESION:.2f}.",
        )
    return (
        "NO_REFORZAR",
        f"Presion actual {presion:.2f} < umbral {UMBRAL_PRESION:.2f}.",
    )


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
    """Actualiza la memoria a partir del estado anterior y la percepcion."""
    if not _percepcion_valida(percepcion):
        return {
            "percepcion_valida": False,
            "racha_presion_alta": 0,
            "presion_anterior": None,
            "ultima_accion": estado_anterior.get("ultima_accion"),
        }

    presion = float(percepcion["presion"])
    racha_anterior = estado_anterior.get("racha_presion_alta", 0) or 0
    racha_actual = racha_anterior + 1 if presion >= UMBRAL_PRESION else 0

    return {
        "percepcion_valida": True,
        "racha_presion_alta": racha_actual,
        "presion_anterior": presion,
        "ultima_accion": estado_anterior.get("ultima_accion"),
    }


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""
    if not estado_actual.get("percepcion_valida", False):
        return (
            "ABSTENERSE",
            "El estado actual proviene de una percepcion invalida.",
        )

    racha = estado_actual.get("racha_presion_alta", 0)
    if racha >= 2:
        return (
            "RECOMENDAR_REFUERZO",
            f"Presion alta sostenida durante {racha} horas consecutivas.",
        )
    return (
        "NO_REFORZAR",
        f"Racha de presion alta de {racha} hora(s); no alcanza la persistencia minima.",
    )


def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes y construye la bitacora comparativa."""
    filas: list[dict[str, Any]] = []
    estado = crear_estado_inicial()

    for _, fila in percepciones.sort_values("hora").iterrows():
        percepcion = fila.to_dict()

        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)
        estado = actualizar_estado(estado, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)
        estado["ultima_accion"] = accion_modelo

        filas.append(
            {
                "hora": percepcion.get("hora"),
                "presion": percepcion.get("presion"),
                "racha_presion_alta": estado["racha_presion_alta"],
                "accion_simple": accion_simple,
                "motivo_simple": motivo_simple,
                "accion_modelo": accion_modelo,
                "motivo_modelo": motivo_modelo,
            }
        )

    return pd.DataFrame(
        filas,
        columns=[
            "hora",
            "presion",
            "racha_presion_alta",
            "accion_simple",
            "motivo_simple",
            "accion_modelo",
            "motivo_modelo",
        ],
    )
