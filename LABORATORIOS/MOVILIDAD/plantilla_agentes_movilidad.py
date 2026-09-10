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

    if not isinstance(percepcion, dict):
        return ("ABSTENERSE", "La percepción no es válida.")

    presion = percepcion.get("presion")
    capacidad = percepcion.get("capacidad_x")

    if presion is None or capacidad is None:
        return ("ABSTENERSE", "Faltan datos requeridos.")

    if not isinstance(presion, (int, float)) or not isinstance(
        capacidad, (int, float)
    ):
        return ("ABSTENERSE", "La presión o la capacidad no son válidas.")

    if pd.isna(presion) or pd.isna(capacidad):
        return ("ABSTENERSE", "La presión o la capacidad contienen valores inválidos.")

    if capacidad <= 0:
        return ("ABSTENERSE", "La capacidad debe ser mayor que cero.")

    if presion >= UMBRAL_PRESION:
        return (
            "RECOMENDAR_REFUERZO",
            f"La presión ({presion:.2f}) es mayor o igual al umbral ({UMBRAL_PRESION:.2f}).",
        )

    return (
        "NO_REFORZAR",
        f"La presión ({presion:.2f}) es menor al umbral ({UMBRAL_PRESION:.2f}).",
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

    estado = crear_estado_inicial()

    if not isinstance(percepcion, dict):
        return estado

    presion = percepcion.get("presion")
    capacidad = percepcion.get("capacidad_x")

    if presion is None or capacidad is None:
        return estado

    if not isinstance(presion, (int, float)) or not isinstance(
        capacidad, (int, float)
    ):
        return estado

    if pd.isna(presion) or pd.isna(capacidad):
        return estado

    if capacidad <= 0:
        return estado

    estado["percepcion_valida"] = True
    estado["presion_anterior"] = presion

    racha_anterior = estado_anterior.get("racha_presion_alta", 0)

    if presion >= UMBRAL_PRESION:
        estado["racha_presion_alta"] = racha_anterior + 1
    else:
        estado["racha_presion_alta"] = 0

    return estado


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""

    if not isinstance(estado_actual, dict):
        return ("ABSTENERSE", "El estado interno no es válido.")

    if not estado_actual.get("percepcion_valida", False):
        return ("ABSTENERSE", "La percepción actual es inválida.")

    racha = estado_actual.get("racha_presion_alta", 0)

    if not isinstance(racha, int) or racha < 0:
        return ("ABSTENERSE", "La racha de presión alta no es válida.")

    if racha >= 2:
        return (
            "RECOMENDAR_REFUERZO",
            f"Se acumularon {racha} horas consecutivas con presión alta.",
        )

    return (
        "NO_REFORZAR",
        f"La racha de presión alta es de {racha} hora(s), menos de 2.",
    )


def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes y construye la bitacora comparativa."""

    if not isinstance(percepciones, pd.DataFrame):
        raise TypeError("percepciones debe ser un DataFrame de pandas.")

    if percepciones.empty:
        return pd.DataFrame(
            columns=[
                "hora",
                "presion",
                "racha_presion_alta",
                "accion_simple",
                "motivo_simple",
                "accion_modelo",
                "motivo_modelo",
            ]
        )

    percepciones_ordenadas = percepciones.sort_values("hora")

    estado = crear_estado_inicial()
    registros = []

    for _, fila in percepciones_ordenadas.iterrows():
        percepcion = fila.to_dict()

        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)

        estado = actualizar_estado(estado, percepcion)

        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)

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

        estado["ultima_accion"] = accion_modelo

    return pd.DataFrame(registros)
