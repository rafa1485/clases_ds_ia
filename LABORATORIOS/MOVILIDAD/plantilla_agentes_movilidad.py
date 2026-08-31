"""Plantilla para el trabajo practico de agentes de movilidad.

Complete las funciones marcadas con TODO sin consultar datos de h+1.
"""

from __future__ import annotations

import math
from typing import Any

import pandas as pd


ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85

# Campos que la regla condicion-accion necesita para decidir.
CAMPOS_REQUERIDOS = ("demanda_x", "capacidad_x", "presion")


def _numero(percepcion: dict[str, Any], campo: str) -> float | None:
    """Devuelve el campo como float o None si falta o no es numerico."""
    if campo not in percepcion:
        return None
    valor = percepcion[campo]
    if isinstance(valor, (bool, str)):
        return None
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return None
    if math.isnan(numero) or math.isinf(numero):
        return None
    return numero


def decidir_reactivo_simple(percepcion: dict[str, Any]) -> tuple[str, str]:
    """Devuelve (accion, motivo) usando solo la percepcion actual."""
    if not isinstance(percepcion, dict):
        return "ABSTENERSE", "La percepcion no es un registro valido."

    valores = {campo: _numero(percepcion, campo) for campo in CAMPOS_REQUERIDOS}
    invalidos = [campo for campo, valor in valores.items() if valor is None]
    if invalidos:
        return (
            "ABSTENERSE",
            f"Faltan datos requeridos o son invalidos: {', '.join(invalidos)}.",
        )

    if valores["demanda_x"] < 0 or valores["presion"] < 0:
        return "ABSTENERSE", "La percepcion contiene valores negativos."

    if valores["capacidad_x"] <= 0:
        return "ABSTENERSE", "La capacidad de X es desconocida o nula."

    presion = valores["presion"]
    if presion >= UMBRAL_PRESION:
        return (
            "RECOMENDAR_REFUERZO",
            f"presion={presion:.2f} >= umbral={UMBRAL_PRESION}",
        )
    return "NO_REFORZAR", f"presion={presion:.2f} < umbral={UMBRAL_PRESION}"


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
    # TODO: actualizar la racha y conservar la información necesaria.
    raise NotImplementedError


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""
    # TODO: aplicar las reglas para presión alta persistente.
    raise NotImplementedError


def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes y construye la bitacora comparativa."""
    # TODO: recorrer las filas en orden temporal sin acceder a h+1.
    raise NotImplementedError
