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
    presion = percepcion.get("presion")
    capacidad_x = percepcion.get("capacidad_x")
    if (not (isinstance(presion, (int, float)) and 0 <= presion and not pd.isna(presion))) or (not (isinstance(capacidad_x, (int, float)) and 0 < capacidad_x and not pd.isna(capacidad_x))):
        return "ABSTENERSE", "Presión o capacidad disponible inválida o incompleta"
    if presion >= UMBRAL_PRESION:
        return "RECOMENDAR_REFUERZO", f"Presión alta ({presion})"
    else:
        return "NO_REFORZAR", f"Presión normal ({presion})"


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
    presion = percepcion.get("presion")
    capacidad_x = percepcion.get("capacidad_x")
    percepcion_valida = isinstance(presion, (int, float)) and 0 <= presion and not pd.isna(presion) and isinstance(capacidad_x, (int, float)) and 0 < capacidad_x and not pd.isna(capacidad_x)

    if not percepcion_valida:
        return {
            "percepcion_valida": False,
            "racha_presion_alta": 0,
            "presion_anterior": None,
            "ultima_accion": None,
        }

    racha_presion_alta = estado_anterior.get("racha_presion_alta", 0) + 1 if presion >= UMBRAL_PRESION else 0
    presion_anterior = presion
    ultima_accion = estado_anterior.get("ultima_accion")

    return {
        "percepcion_valida": percepcion_valida,
        "racha_presion_alta": racha_presion_alta,
        "presion_anterior": presion_anterior,
        "ultima_accion": ultima_accion,
    }


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""
    if not estado_actual.get("percepcion_valida"):
        return "ABSTENERSE", "Percepción inválida"
    if estado_actual.get("racha_presion_alta", 0) >= 2:
        return "RECOMENDAR_REFUERZO", f"racha_presion_alta={estado_actual.get('racha_presion_alta')} >= 2"
    return "NO_REFORZAR", f"racha_presion_alta={estado_actual.get('racha_presion_alta')} < 2"


def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes y construye la bitacora comparativa."""
    bitacora = []
    estado_actual = crear_estado_inicial()
    for _, fila in percepciones.iterrows():
        percepcion = fila.to_dict()
        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)
        estado_actual = actualizar_estado(estado_actual, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado_actual)
        estado_actual["ultima_accion"] = accion_modelo
        registro = percepcion.copy()
        registro.update({
            "accion_simple": accion_simple,
            "motivo_simple": motivo_simple,
            "accion_modelo": accion_modelo,
            "motivo_modelo": motivo_modelo,
            "racha_presion_alta": estado_actual["racha_presion_alta"],
        })
        bitacora.append(registro)
    return pd.DataFrame(bitacora)


if __name__ == "__main__":
    print("--- Prueba agente reactivo simple ---")
    print(decidir_reactivo_simple({"presion": 0.90, "capacidad_x": 20}))
    print(decidir_reactivo_simple({"presion": 0.50, "capacidad_x": 20}))
    print(decidir_reactivo_simple({"presion": None, "capacidad_x": 20}))
