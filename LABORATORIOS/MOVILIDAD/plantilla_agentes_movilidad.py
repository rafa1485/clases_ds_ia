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
    # TODO: validar la percepción y aplicar las reglas de la consigna.
    raise NotImplementedError


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
