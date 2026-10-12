"""Agentes reactivos para el trabajo práctico de movilidad.

Las decisiones utilizan únicamente las percepciones disponibles hasta
la hora actual. No se consultan datos de h+1.
"""

from __future__ import annotations

from numbers import Real
from typing import Any

import pandas as pd


ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85


def percepcion_es_valida(percepcion: dict[str, Any]) -> bool:
    """Comprueba que presión y capacidad sean datos utilizables."""

    if not isinstance(percepcion, dict):
        return False

    campos_requeridos = {"presion", "capacidad_x"}

    if not campos_requeridos.issubset(percepcion):
        return False

    presion = percepcion["presion"]
    capacidad = percepcion["capacidad_x"]

    if isinstance(presion, bool) or not isinstance(presion, Real):
        return False

    if isinstance(capacidad, bool) or not isinstance(capacidad, Real):
        return False

    if pd.isna(presion) or pd.isna(capacidad):
        return False

    if presion < 0 or capacidad <= 0:
        return False

    return True


def decidir_reactivo_simple(
    percepcion: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve una acción usando solamente la percepción actual."""

    if not percepcion_es_valida(percepcion):
        return (
            "ABSTENERSE",
            "La percepción es inválida o la capacidad es desconocida.",
        )

    presion = float(percepcion["presion"])

    if presion >= UMBRAL_PRESION:
        return (
            "RECOMENDAR_REFUERZO",
            f"La presión {presion:.2f} es mayor o igual al umbral "
            f"{UMBRAL_PRESION:.2f}.",
        )

    return (
        "NO_REFORZAR",
        f"La presión {presion:.2f} es menor al umbral "
        f"{UMBRAL_PRESION:.2f}.",
    )


def crear_estado_inicial() -> dict[str, Any]:
    """Crea el estado persistente del agente basado en modelo."""

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
    """Actualiza la memoria usando el estado anterior y la percepción."""

    estado_actual = estado_anterior.copy()

    if not percepcion_es_valida(percepcion):
        estado_actual["percepcion_valida"] = False
        estado_actual["racha_presion_alta"] = 0
        estado_actual["presion_anterior"] = None
        return estado_actual

    presion = float(percepcion["presion"])

    estado_actual["percepcion_valida"] = True
    estado_actual["presion_anterior"] = presion

    if presion >= UMBRAL_PRESION:
        estado_actual["racha_presion_alta"] = (
            estado_anterior.get("racha_presion_alta", 0) + 1
        )
    else:
        estado_actual["racha_presion_alta"] = 0

    return estado_actual


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Decide usando el estado interno ya actualizado."""

    if not estado_actual.get("percepcion_valida", False):
        return (
            "ABSTENERSE",
            "La percepción actual es inválida.",
        )

    racha = estado_actual.get("racha_presion_alta", 0)

    if racha >= 2:
        return (
            "RECOMENDAR_REFUERZO",
            f"Se observaron {racha} horas consecutivas con presión alta.",
        )

    return (
        "NO_REFORZAR",
        "Todavía no hay dos horas consecutivas con presión alta.",
    )


def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta los agentes en orden temporal y construye la bitácora."""

    estado = crear_estado_inicial()
    registros = []

    percepciones_ordenadas = percepciones.sort_values("hora")

    for _, fila in percepciones_ordenadas.iterrows():
        percepcion = fila.to_dict()

        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)

        estado = actualizar_estado(estado, percepcion)

        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)
        estado["ultima_accion"] = accion_modelo

        registros.append(
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

    return pd.DataFrame(registros)