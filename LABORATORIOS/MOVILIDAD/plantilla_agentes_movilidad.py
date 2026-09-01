"""Plantilla para el trabajo practico de agentes de movilidad.

Complete las funciones marcadas con TODO sin consultar datos de h+1.
"""

from __future__ import annotations

from contextlib import aclosing
from typing import Any

import pandas as pd


ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85


def decidir_reactivo_simple(percepcion: dict[str, Any]) -> tuple[str, str]:
    if not percepcion or "presion" not in percepcion:
      return("ABSTENERSE", "Faltan datos requeridos")

    presion = percepcion.get("presion")
    capacidad = percepcion.get("capacidad_x")

    if presion is None or capacidad is None or capacidad == "desconocida":
        return ("ABSTENERSE", "Faltan datos requeridos o capacidad desconocida.")

    if presion >= UMBRAL_PRESION:
        return ("RECOMENDAR_REFUERZO", f"Umbral de presión muy alto ({presion:.2f} >= {UMBRAL_PRESION}).")
    else:
        return ("NO_REFORZAR", f"Umbral de presión controlado ({presion:.2f} < {UMBRAL_PRESION}).")


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
    presion = percepcion.get("presion")
    capacidad = percepcion.get("capacidad_x")
    
    datos_validos = (presion is not None) and (capacidad is not None) and (capacidad != "desconocida")    
    if datos_validos:
      if presion >= UMBRAL_PRESION:
        nueva_racha = estado_anterior["racha_presion_alta"] + 1
      else:
        nueva_racha = 0
    else:
        nueva_racha = 0

    return {
        "percepcion_valida": datos_validos,
        "racha_presion_alta": nueva_racha,
        "presion_anterior": presion,
        "ultima_accion": estado_anterior["ultima_accion"]
    }


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""
    
    # 1. Si la percepción no fue válida o faltan datos
    if not estado_actual.get("percepcion_valida", False):
        return ("ABSTENERSE", "Percepción inválida o datos faltantes.")

    racha = estado_actual.get("racha_presion_alta", 0)

    # 2. Solo recomienda refuerzo si hay 2 o más horas consecutivas con presión alta
    if racha >= 2:
        return ("RECOMENDAR_REFUERZO", f"Presión alta persistente durante {racha} horas consecutivas.")
    else:
        return ("NO_REFORZAR", f"Presión normal o primera hora alta (racha = {racha}).")
    
  

def procesar_secuencia(percepciones: list[dict[str, Any]]) -> pd.DataFrame:
    """Ejecuta la secuencia de percepciones en ambos agentes y retorna la bitácora comparativa."""
    estado_modelo = crear_estado_inicial()
    bitacora = []

    for percepcion in percepciones:
        hora = percepcion.get("hora") if percepcion else None
        presion = percepcion.get("presion") if percepcion else None

        # Agente Reactivo Simple
        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)

        # Agente Reactivo Basado en Modelo
        estado_modelo = actualizar_estado(estado_modelo, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado_modelo)
        estado_modelo["ultima_accion"] = accion_modelo

        fila = {
            "hora": hora,
            "presion": presion,
            "racha_presion_alta": estado_modelo.get("racha_presion_alta", 0),
            "accion_simple": accion_simple,
            "motivo_simple": motivo_simple,
            "accion_modelo": accion_modelo,
            "motivo_modelo": motivo_modelo,
        }
        bitacora.append(fila)

    return pd.DataFrame(bitacora)