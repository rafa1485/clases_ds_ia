"""Plantilla para el trabajo practico de agentes de movilidad.

Complete las funciones marcadas con TODO sin consultar datos de h+1.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85


def decidir_reactivo_simple(percepcion: dict[str, Any]) -> tuple[str, str]:
    """Devuelve (accion, motivo) usando solo la percepcion actual."""

    capacidad = percepcion.get("capacidad_x")
    presion = percepcion.get("presion")

    if capacidad is None:
        return "ABSTENERSE", "La capacidad de X es desconocida."

    if not isinstance(capacidad, (int, float)) or capacidad <= 0:
        return "ABSTENERSE", "La capacidad de X es inválida."

    if presion is None:
        return "ABSTENERSE", "La presión no está disponible."

    if not isinstance(presion, (int, float)):
        return "ABSTENERSE", "La presión no es un valor numérico."

    if presion >= UMBRAL_PRESION:
        return (
            "RECOMENDAR_REFUERZO",
            f"La presión ({presion:.2f}) es mayor o igual al umbral de {UMBRAL_PRESION:.2f}."
        )

    return (
        "NO_REFORZAR",
        f"La presión ({presion:.2f}) es menor al umbral de {UMBRAL_PRESION:.2f}."
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
    estado = estado_anterior.copy()

    capacidad = percepcion.get("capacidad_x")
    presion = percepcion.get("presion")

    if (
        capacidad is None
        or not isinstance(capacidad, (int, float))
        or capacidad <= 0
    ):
        estado["percepcion_valida"] = False
        estado["racha_presion_alta"] = 0
        estado["presion_anterior"] = None
        return estado

    if presion is None or not isinstance(presion, (int, float)):
        estado["percepcion_valida"] = False
        estado["racha_presion_alta"] = 0
        estado["presion_anterior"] = None
        return estado

    estado["percepcion_valida"] = True
    estado["presion_anterior"] = presion

    if presion >= UMBRAL_PRESION:
        estado["racha_presion_alta"] += 1
    else:
        estado["racha_presion_alta"] = 0

    return estado


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""

    if not estado_actual.get("percepcion_valida", False):
        return (
            "ABSTENERSE",
            "La percepción actual no es válida."
        )

    racha = estado_actual.get("racha_presion_alta", 0)

    if racha >= 2:
        return (
            "RECOMENDAR_REFUERZO",
            f"La presión alta se mantiene durante {racha} horas consecutivas."
        )

    return (
        "NO_REFORZAR",
        f"La presión alta todavía no se mantiene durante 2 horas consecutivas (racha actual: {racha})."
    )


def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes y construye la bitacora comparativa."""

    estado = crear_estado_inicial()
    bitacora = []

    percepciones_ordenadas = percepciones.sort_values("hora")

    for _, fila in percepciones_ordenadas.iterrows():
        percepcion = fila.to_dict()

        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)

        estado = actualizar_estado(estado, percepcion)

        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)

        bitacora.append({
            "hora": percepcion["hora"],
            "presion": percepcion.get("presion"),
            "racha_presion_alta": estado["racha_presion_alta"],
            "accion_simple": accion_simple,
            "motivo_simple": motivo_simple,
            "accion_modelo": accion_modelo,
            "motivo_modelo": motivo_modelo,
        })

        estado["ultima_accion"] = accion_modelo

    return pd.DataFrame(bitacora)
