"""Agentes reactivos para recomendar refuerzo de taxis.

Las funciones de decision trabajan unicamente con percepciones disponibles
hasta la hora observada. El resultado de ``h+1`` queda fuera de este modulo.
"""

from __future__ import annotations

import math
from numbers import Real
from typing import Any

import pandas as pd


ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85


def _numero_finito_no_negativo(valor: Any) -> bool:
    """Indica si ``valor`` es un numero real, finito y no negativo."""
    return (
        not isinstance(valor, bool)
        and isinstance(valor, Real)
        and math.isfinite(float(valor))
        and valor >= 0
    )


def _validar_percepcion(percepcion: Any) -> tuple[bool, str]:
    """Valida los datos estrictamente necesarios para aplicar la politica."""
    if not isinstance(percepcion, dict):
        return False, "La percepcion debe ser un diccionario."

    if "capacidad_x" not in percepcion or "presion" not in percepcion:
        return False, "Faltan capacidad_x o presion en la percepcion."

    capacidad = percepcion.get("capacidad_x")
    if not _numero_finito_no_negativo(capacidad) or capacidad == 0:
        return False, "La capacidad de X es desconocida, invalida o nula."

    presion = percepcion.get("presion")
    if not _numero_finito_no_negativo(presion):
        return False, "La presion es desconocida o invalida."

    return True, "Percepcion valida."


def decidir_reactivo_simple(percepcion: dict[str, Any]) -> tuple[str, str]:
    """Devuelve ``(accion, motivo)`` usando solo la percepcion actual."""
    es_valida, motivo = _validar_percepcion(percepcion)
    if not es_valida:
        return "ABSTENERSE", motivo

    presion = float(percepcion["presion"])
    if presion >= UMBRAL_PRESION:
        return (
            "RECOMENDAR_REFUERZO",
            f"La presion actual ({presion:.2f}) alcanza el umbral de "
            f"{UMBRAL_PRESION:.2f}.",
        )
    return (
        "NO_REFORZAR",
        f"La presion actual ({presion:.2f}) es menor que el umbral de "
        f"{UMBRAL_PRESION:.2f}.",
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
    """Actualiza la memoria sin modificar el estado recibido."""
    es_valida, _ = _validar_percepcion(percepcion)
    ultima_accion = (
        estado_anterior.get("ultima_accion")
        if isinstance(estado_anterior, dict)
        else None
    )

    if not es_valida:
        return {
            "percepcion_valida": False,
            "racha_presion_alta": 0,
            "presion_anterior": None,
            "ultima_accion": ultima_accion,
        }

    presion = float(percepcion["presion"])
    racha_anterior = (
        estado_anterior.get("racha_presion_alta", 0)
        if isinstance(estado_anterior, dict)
        else 0
    )
    if isinstance(racha_anterior, bool) or not isinstance(racha_anterior, int):
        racha_anterior = 0
    if racha_anterior < 0:
        racha_anterior = 0

    racha_actual = racha_anterior + 1 if presion >= UMBRAL_PRESION else 0
    return {
        "percepcion_valida": True,
        "racha_presion_alta": racha_actual,
        "presion_anterior": presion,
        "ultima_accion": ultima_accion,
    }


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve ``(accion, motivo)`` a partir del estado actualizado."""
    if not isinstance(estado_actual, dict) or not estado_actual.get(
        "percepcion_valida", False
    ):
        return "ABSTENERSE", "La percepcion actual es invalida."

    racha = estado_actual.get("racha_presion_alta")
    if isinstance(racha, bool) or not isinstance(racha, int) or racha < 0:
        return "ABSTENERSE", "La racha de presion alta es invalida."

    if racha >= 2:
        return (
            "RECOMENDAR_REFUERZO",
            f"Se observaron {racha} horas consecutivas con presion alta.",
        )
    return (
        "NO_REFORZAR",
        f"La racha de presion alta es {racha}; se requieren al menos 2 horas.",
    )


def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes en orden temporal y crea su bitacora."""
    if not isinstance(percepciones, pd.DataFrame):
        raise TypeError("percepciones debe ser un DataFrame")
    if "hora" not in percepciones.columns:
        raise ValueError("Las percepciones deben incluir la columna hora")

    horas = pd.to_numeric(percepciones["hora"], errors="coerce")
    horas_validas = horas.notna() & horas.map(
        lambda hora: math.isfinite(float(hora)) and float(hora).is_integer()
    )
    if not horas_validas.all():
        raise ValueError("Todas las horas deben ser enteros validos")

    ordenadas = percepciones.assign(_hora_orden=horas).sort_values(
        "_hora_orden", kind="stable"
    )
    estado = crear_estado_inicial()
    registros: list[dict[str, Any]] = []

    for _, fila in ordenadas.drop(columns="_hora_orden").iterrows():
        percepcion = fila.to_dict()
        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)
        estado = actualizar_estado(estado, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)
        estado["ultima_accion"] = accion_modelo

        registros.append(
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

    return pd.DataFrame(
        registros,
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
