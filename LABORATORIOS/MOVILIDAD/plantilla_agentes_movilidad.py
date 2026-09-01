"""Plantilla para el trabajo practico de agentes de movilidad.

Complete las funciones marcadas con TODO sin consultar datos de h+1.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85


def decidir_reactivo_simple(percepcion):
    if "presion" not in percepcion or pd.isna(percepcion.get("presion")):
        return "ABSTENERSE", "Falta dato de presion o es nulo"
    
    if "capacidad_x" not in percepcion or pd.isna(percepcion.get("capacidad_x")):
        return "ABSTENERSE", "Capacidad desconocida"

    presion = percepcion["presion"]

    # Aplicamos las reglas reactivas
    if presion >= 0.85:
        return "RECOMENDAR_REFUERZO", "Presion >= 0.85"
    else:
        return "NO_REFORZAR", "Presion < 0.85"


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

        # BUENA PRÁCTICA: Evitar mutar el estado anterior. Creamos uno nuevo.
        # Así garantizamos trazabilidad y evitamos efectos secundarios extraños en la simulación temporal.
        nuevo_estado = estado_anterior.copy()

        presion = percepcion.get("presion")
        capacidad = percepcion.get("capacidad_x")

        # 1. Validamos la percepción (mismo criterio que el agente simple)
        es_invalida = presion is None or capacidad is None or pd.isna(presion) or pd.isna(capacidad)

        if es_invalida:
            nuevo_estado["percepcion_valida"] = False
            nuevo_estado["racha_presion_alta"] = 0  # Si nos quedamos ciegos, se corta la racha
            nuevo_estado["presion_anterior"] = None
        else:
            nuevo_estado["percepcion_valida"] = True
            nuevo_estado["presion_anterior"] = presion

            # 2. Actualizamos la memoria histórica
            if presion >= 0.85:
                nuevo_estado["racha_presion_alta"] += 1
            else:
                nuevo_estado["racha_presion_alta"] = 0

        return nuevo_estado


def decidir_reactivo_modelo(
        estado_actual: dict[str, Any],
    ) -> tuple[str, str]:
        """Devuelve (accion, motivo) a partir del estado interno actualizado."""

        # Fijate que acá NO HAY PERCEPCIÓN. Solo leemos el modelo mental.

        if not estado_actual["percepcion_valida"]:
            return ("ABSTENERSE", "El estado interno indica que la última percepción fue inválida.")

        if estado_actual["racha_presion_alta"] >= 2:
            return ("RECOMENDAR_REFUERZO", f"¡Alerta! Presión alta sostenida durante {estado_actual['racha_presion_alta']} horas.")

        return ("NO_REFORZAR", f"La racha de presión alta actual es {estado_actual['racha_presion_alta']}, insuficiente para actuar.")


def procesar_secuencia(df_percepciones):
    """
    Ejecuta ambos agentes sobre la secuencia temporal de percepciones.csv
    y devuelve un DataFrame para guardar como bitacora_agentes.csv.
    """
    filas = []
    
    # Estado inicial del agente basado en modelo
    estado_modelo = {
        "percepcion_valida": False,
        "racha_presion_alta": 0,
        "presion_anterior": None,
        "ultima_accion": None,
    }

    for _, fila in df_percepciones.iterrows():
        percepcion = fila.to_dict()
        hora = percepcion.get("hora")
        presion = percepcion.get("presion")

        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)

        estado_modelo = actualizar_estado(estado_modelo, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado_modelo)
        
        estado_modelo["ultima_accion"] = accion_modelo

        filas.append({
            "hora": hora,
            "presion": presion,
            "racha_presion_alta": estado_modelo["racha_presion_alta"],
            "accion_simple": accion_simple,
            "motivo_simple": motivo_simple,
            "accion_modelo": accion_modelo,
            "motivo_modelo": motivo_modelo,
        })

    return pd.DataFrame(filas)
