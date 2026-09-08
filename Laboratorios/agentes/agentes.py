"""Módulo de agentes reactivo simple y basado en modelo para refuerzo de taxis.

Trabajo práctico: Agentes reactivos para refuerzo de movilidad.
"""

from __future__ import annotations

from typing import Any
import pandas as pd

ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85


def validar_percepcion(percepcion: dict[str, Any] | Any) -> bool:
    """Verifica si una percepción contiene los datos mínimos y válidos."""
    if not isinstance(percepcion, dict):
        return False
    if "presion" not in percepcion:
        return False
    presion = percepcion.get("presion")
    if presion is None or pd.isna(presion) or isinstance(presion, bool):
        return False
    if not isinstance(presion, (int, float)):
        return False
    if presion < 0:
        return False
    if "capacidad_x" in percepcion:
        capacidad = percepcion.get("capacidad_x")
        if (
            capacidad is None
            or pd.isna(capacidad)
            or isinstance(capacidad, bool)
            or not isinstance(capacidad, (int, float))
            or capacidad <= 0
        ):
            return False
    return True


def decidir_reactivo_simple(percepcion: dict[str, Any]) -> tuple[str, str]:
    """Devuelve (accion, motivo) usando exclusivamente la percepcion actual."""
    if not validar_percepcion(percepcion):
        return ("ABSTENERSE", "Percepción inválida, incompleta o capacidad desconocida.")

    presion = float(percepcion["presion"])
    if presion >= UMBRAL_PRESION:
        return (
            "RECOMENDAR_REFUERZO",
            f"Presión actual ({presion:.2f}) >= {UMBRAL_PRESION:.2f}.",
        )
    return (
        "NO_REFORZAR",
        f"Presión actual ({presion:.2f}) < {UMBRAL_PRESION:.2f}.",
    )


def crear_estado_inicial() -> dict[str, Any]:
    """Crea el estado persistente inicial del agente reactivo basado en modelo."""
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
    """Actualiza la memoria a partir del estado anterior y la percepcion actual."""
    if not validar_percepcion(percepcion):
        return {
            "percepcion_valida": False,
            "racha_presion_alta": 0,
            "presion_anterior": None,
            "ultima_accion": "ABSTENERSE",
        }

    presion = float(percepcion["presion"])
    if presion >= UMBRAL_PRESION:
        racha_actual = estado_anterior.get("racha_presion_alta", 0) + 1
    else:
        racha_actual = 0

    return {
        "percepcion_valida": True,
        "racha_presion_alta": racha_actual,
        "presion_anterior": presion,
        "ultima_accion": estado_anterior.get("ultima_accion"),
    }


def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""
    if not estado_actual.get("percepcion_valida", False):
        return (
            "ABSTENERSE",
            "Percepción inválida o incompleta; no es seguro aplicar la política.",
        )

    racha = estado_actual.get("racha_presion_alta", 0)
    if racha >= 2:
        return (
            "RECOMENDAR_REFUERZO",
            f"Presión alta persistente ({racha} horas consecutivas >= {UMBRAL_PRESION:.2f}).",
        )
    if racha == 1:
        return (
            "NO_REFORZAR",
            f"Presión alta aislada (racha = 1 hora); se requiere persistencia de al menos 2 horas.",
        )
    return (
        "NO_REFORZAR",
        f"Presión normal o baja (< {UMBRAL_PRESION:.2f}); racha de presión alta = 0.",
    )


def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes y construye la bitácora comparativa en orden temporal."""
    estado = crear_estado_inicial()
    resultados = []

    for _, fila in percepciones.iterrows():
        percepcion: dict[str, Any] = dict(fila.items())

        # Agente reactivo simple
        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)

        # Agente reactivo basado en modelo
        estado = actualizar_estado(estado, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)
        estado["ultima_accion"] = accion_modelo

        presion_val = percepcion.get("presion")

        fila_resultado: dict[str, Any] = {
            "hora": percepcion.get("hora"),
            "presion": presion_val,
            "racha_presion_alta": estado["racha_presion_alta"],
            "accion_simple": accion_simple,
            "motivo_simple": motivo_simple,
            "accion_modelo": accion_modelo,
            "motivo_modelo": motivo_modelo,
        }
        resultados.append(fila_resultado)

    columnas_resultado = [
        "hora",
        "presion",
        "racha_presion_alta",
        "accion_simple",
        "motivo_simple",
        "accion_modelo",
        "motivo_modelo",
    ]
    return pd.DataFrame(resultados, columns=columnas_resultado)


if __name__ == "__main__":
    datos_ejemplo = pd.DataFrame([
        {"hora": 6, "zona": "Midtown Center", "presion": 0.70, "capacidad_x": 20},
        {"hora": 7, "zona": "Midtown Center", "presion": 0.90, "capacidad_x": 20},
        {"hora": 8, "zona": "Midtown Center", "presion": 0.88, "capacidad_x": 20},
        {"hora": 9, "zona": "Midtown Center", "presion": 0.60, "capacidad_x": 20},
    ])

    df_resultado = procesar_secuencia(datos_ejemplo)
    print("--- Bitácora de prueba ---")
    print(df_resultado.to_string(index=False))
