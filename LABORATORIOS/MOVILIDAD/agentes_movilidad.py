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
     # 1. Comprobar que existan los datos necesarios
    #    presion y capacidad_x

    presion = percepcion.get("presion")
    capacidad_x = percepcion.get("capacidad_x")

    # 2. Comprobar que esos datos sean válidos
    #    si no → ABSTENERSE
    if presion is None or capacidad_x is None:
        return "ABSTENERSE", "datos invalidos"

    # 3. Comprobar presión
    if presion >= UMBRAL_PRESION:
        return "RECOMENDAR_REFUERZO", "presion alta"

    # 4. Si no alcanza el umbral
    return "NO_REFORZAR", "presion normal"

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
    """Actualiza la memoria a partir del estado anterior y la percepción."""

    estado_nuevo = estado_anterior.copy()

    presion = percepcion.get("presion")
    capacidad_x = percepcion.get("capacidad_x")

    # Percepción inválida
    if presion is None or capacidad_x is None:
        estado_nuevo["percepcion_valida"] = False
        estado_nuevo["racha_presion_alta"] = 0
        estado_nuevo["presion_anterior"] = presion
        return estado_nuevo

    # Percepción válida
    estado_nuevo["percepcion_valida"] = True
    estado_nuevo["presion_anterior"] = presion

    # Actualizar racha
    if presion >= UMBRAL_PRESION:
        estado_nuevo["racha_presion_alta"] += 1
    else:
        estado_nuevo["racha_presion_alta"] = 0

    return estado_nuevo


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""

    if not estado_actual.get("percepcion_valida", False):
        return "ABSTENERSE", "percepcion invalida"

    racha = estado_actual.get("racha_presion_alta", 0)

    if racha >= 2:
        return "RECOMENDAR_REFUERZO", "dos horas consecutivas con presion alta"

    return "NO_REFORZAR", "no hay dos horas consecutivas con presion alta"

def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes y construye la bitácora comparativa."""

    estado = crear_estado_inicial()
    bitacora = []

    percepciones_ordenadas = percepciones.sort_values("hora")

    for _, fila in percepciones_ordenadas.iterrows():

        percepcion = fila.to_dict()

        # Agente reactivo simple
        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)

        # Agente reactivo basado en modelo
        estado = actualizar_estado(estado, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)

        # Registrar resultados
        bitacora.append({
            "hora": percepcion.get("hora"),
            "presion": percepcion.get("presion"),
            "racha_presion_alta": estado.get("racha_presion_alta"),
            "accion_simple": accion_simple,
            "motivo_simple": motivo_simple,
            "accion_modelo": accion_modelo,
            "motivo_modelo": motivo_modelo,
        })

    return pd.DataFrame(bitacora)