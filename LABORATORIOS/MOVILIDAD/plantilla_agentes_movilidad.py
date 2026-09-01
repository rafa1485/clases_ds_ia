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
    
    # Validar si faltan datos o si la capacidad es desconocida (menor o igual a cero o no existe)
    if (
        "presion" not in percepcion 
        or percepcion["presion"] is None 
        or "capacidad_x" not in percepcion 
        or percepcion["capacidad_x"] is None
        or percepcion["capacidad_x"] <= 0
    ):
        return ("ABSTENERSE", "Faltan datos requeridos o capacidad inválida/desconocida")
    
    # Aplicar las reglas basadas en el umbral de presión
    presion = percepcion["presion"]
    if presion >= UMBRAL_PRESION:
        return ("RECOMENDAR_REFUERZO", f"La presión ({presion:.2f}) supera el umbral de {UMBRAL_PRESION}")
    else:
        return ("NO_REFORZAR", f"La presión ({presion:.2f}) es baja")


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
    nuevo_estado = estado_anterior.copy()
    
    # Validar si faltan datos o si la capacidad es desconocida
    if (
        "presion" not in percepcion 
        or percepcion["presion"] is None 
        or "capacidad_x" not in percepcion 
        or percepcion["capacidad_x"] is None
        or percepcion["capacidad_x"] <= 0
    ):
        nuevo_estado["percepcion_valida"] = False
        nuevo_estado["racha_presion_alta"] = 0
        nuevo_estado["presion_anterior"] = None
        return nuevo_estado
        
    nuevo_estado["percepcion_valida"] = True
    presion = percepcion["presion"]
    nuevo_estado["presion_anterior"] = presion
    
    # Actualizar la racha de presión alta
    if presion >= UMBRAL_PRESION:
        nuevo_estado["racha_presion_alta"] += 1
    else:
        nuevo_estado["racha_presion_alta"] = 0
        
    return nuevo_estado

def decidir_reactivo_modelo(
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""
    
    if not estado_actual.get("percepcion_valida", False):
        accion = "ABSTENERSE"
        motivo = "Percepción inválida o datos insuficientes"
    elif estado_actual.get("racha_presion_alta", 0) >= 2:
        accion = "RECOMENDAR_REFUERZO"
        motivo = f"Racha de presión alta mantenida por {estado_actual['racha_presion_alta']} horas"
    else:
        accion = "NO_REFORZAR"
        if estado_actual.get("racha_presion_alta", 0) == 1:
            motivo = "Presión alta por primera vez (esperando confirmación en la siguiente hora)"
        else:
            motivo = "Presión baja o normal"
            
    estado_actual["ultima_accion"] = accion
    return (accion, motivo)





def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes y construye la bitacora comparativa."""
    
    estado_modelo = crear_estado_inicial()
    bitacora = []
    
    # Recorrer las filas del DataFrame en orden (cada fila es una hora)
    for _, fila in percepciones.iterrows():
        percepcion = fila.to_dict()
        hora_actual = percepcion.get("hora")
        presion_actual = percepcion.get("presion")
        
        # 1. Ejecutar el Agente Simple
        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)
        
        # 2. Ejecutar el Agente Basado en Modelo
        estado_modelo = actualizar_estado(estado_modelo, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado_modelo)
        
        # 3. Guardar los resultados de esta hora en la bitácora
        registro = {
            "hora": hora_actual,
            "presion": presion_actual,
            "racha_presion_alta": estado_modelo["racha_presion_alta"],
            "accion_simple": accion_simple,
            "motivo_simple": motivo_simple,
            "accion_modelo": accion_modelo,
            "motivo_modelo": motivo_modelo,
        }
        bitacora.append(registro)
        
    # Convertir la lista de resultados en un nuevo DataFrame (tabla)
    return pd.DataFrame(bitacora)
