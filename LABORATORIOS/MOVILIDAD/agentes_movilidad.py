"""Plantilla para el trabajo practico de agentes de movilidad.

Complete las funciones marcadas con TODO sin consultar datos de h+1.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

import math 


ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85


def decidir_reactivo_simple(percepcion: dict[str, Any]) -> tuple[str, str]:
    """Devuelve (accion, motivo) usando solo la percepcion actual."""
    if not isinstance(percepcion, dict) or "presion" not in percepcion or "capacidad_x" not in percepcion:
        return "ABSTENERSE", "faltan_datos_requeridos"

    presion = percepcion["presion"]
    capacidad = percepcion["capacidad_x"]

    if not isinstance(presion, (int, float)):
        return "ABSTENERSE", "presion_invalida"
    
    if not isinstance(capacidad, (int, float)):
        return "ABSTENERSE", "capacidad_invalida"

    if math.isnan(presion) or math.isinf(presion):
        return "ABSTENERSE", "presion_no_numerica"

    if presion < 0:
        return "ABSTENERSE", f"presion_negativa (presion={presion:.2f})"

    if capacidad == 0:
        return "ABSTENERSE", "capacidad_desconocida (capacidad_x=0)"

    if presion >= UMBRAL_PRESION:
        return "RECOMENDAR_REFUERZO", f"presion={presion:.2f} >= umbral={UMBRAL_PRESION}"
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

    """valida la percepcion"""
    accion_simple, _ = decidir_reactivo_simple(percepcion)

    """si la percepcion es invalida, no se actualiza el estado"""
    if accion_simple == "ABSTENERSE":
        return {
            "percepcion_valida": False,
            "racha_presion_alta": 0,
            "presion_anterior": None,
            "ultima_accion": estado_anterior["ultima_accion"],
        }

    """si la presion es alta, se incrementa la racha, sino se reinicia a 0"""
    presion_actual = percepcion["presion"]

    if presion_actual >= UMBRAL_PRESION:
        nueva_racha = estado_anterior["racha_presion_alta"] + 1
    else:
        nueva_racha = 0

    return {
        "percepcion_valida": True,
        "racha_presion_alta": nueva_racha,
        "presion_anterior": presion_actual,
        "ultima_accion": estado_anterior["ultima_accion"],
    }


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""

    if not estado_actual["percepcion_valida"]:
        return "ABSTENERSE", "percepcion_invalida"

    racha = estado_actual["racha_presion_alta"]

    if racha >= 2:
        return "RECOMENDAR_REFUERZO", f"Se registraron {racha} horas consecutivas con presión alta."

    return "NO_REFORZAR", f"Racha de presión alta: {racha} horas consecutivas."


def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes y construye la bitacora comparativa."""

    estado = crear_estado_inicial()
    registros = []

    # Procesar las percepciones en orden temporal.
    percepciones_ordenadas = percepciones.sort_values("hora")

    for _, fila in percepciones_ordenadas.iterrows():
        percepcion = fila.to_dict()

        # Decisión del agente reactivo simple.
        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)

        # Actualización y decisión del agente basado en modelo.
        estado = actualizar_estado(estado, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)

        # Conservar la última acción del agente basado en modelo.
        estado["ultima_accion"] = accion_modelo

        # Agregar una fila a la bitácora.
        registros.append(
            {
                "hora": percepcion["hora"],
                "presion": percepcion["presion"],
                "racha_presion_alta": estado["racha_presion_alta"],
                "accion_simple": accion_simple,
                "motivo_simple": motivo_simple,
                "accion_modelo": accion_modelo,
                "motivo_modelo": motivo_modelo,
            }
        )

    return pd.DataFrame(registros)

if __name__ == "__main__":
    percepciones = pd.read_csv("escenario_agente/percepciones.csv")

    bitacora = procesar_secuencia(percepciones)

    print(bitacora.to_string(index=False))

    bitacora.to_csv(
        "LABORATORIOS/MOVILIDAD/bitacora_agentes.csv",
        index=False,
    )

    print("\nBitácora guardada correctamente.")