"""Agentes de movilidad para recomendación de refuerso de taxis."""

from __future__ import annotations

import math
from typing import Any
import pandas as pd

ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85

def _validar_percepcion(percepcion: dict[str, Any]) -> bool:
    """Verifica si la percepción contiene datos válidos para decidir."""
    if not isinstance(percepcion, dict):
        return False
    # Deben existir los campos requeridos
    if "presion" not in percepcion or "capacidad_x" not in percepcion:
        return False
    capacidad = percepcion["capacidad_x"]
    presion = percepcion["presion"]
    # Validar tipos (excluyendo booleanos explícitamente)
    if isinstance(capacidad, bool) or isinstance(presion, bool):
        return False
    if not isinstance(capacidad, (int, float)) or not isinstance(presion, (int, float)):
        return False
    # Validar rangos numéricos y ausencia de NaNs/Infs
    if math.isnan(presion) or math.isinf(presion) or presion < 0:
        return False
    if math.isnan(capacidad) or math.isinf(capacidad) or capacidad <= 0:
        return False
    return True

# --- PARTE 1: AGENTE REACTIVO SIMPLE ---
# Lo que se encarga de hacer esta función es revisar la percepción que recibe 
# del entorno en un momento determinado y tomar una acción en base a ella.
# El agente no tiene memoria, por lo que no recuerda percepciones pasadas.
# La percepción es generada por el simulador y es un diccionario con los datos
# de UNA hora.
# Ejemplo: {"capacidad_x": 20, "presion": 1.15}


"""Recibe un diccionario con los datos de UNA hora, ejemplo {"capacidad_x": 20, "presion": 1.15}"""
def decidir_reactivo_simple(percepcion: dict[str, Any]) -> tuple[str, str]:
    """Devuelve (accion, motivo) usando solo la percepción actual."""
    
    # Valida la percepción (verifica que los datos sean correctos)
    # Si no son correctos, devuelve una accion de abstenerse.
    if not _validar_percepcion(percepcion): 
        return ("ABSTENERSE", "Percepción inválida o datos faltantes")

    presion = percepcion["presion"]

    # Si la presión es mayor o igual al umbral, se recomienda refuerzo.
    if presion >= UMBRAL_PRESION: 
        return (
            "RECOMENDAR_REFUERZO", 
            f"Presion alta observada ({presion:.2f} >= {UMBRAL_PRESION})"
        )
    
    return (
        "NO_REFORZAR",
        f"Presión dentro de limites normales ({presion:.2f} < {UMBRAL_PRESION})"
    )

# --- PARTE 2: AGENTE REACTIVO BASADO EN MODELO ---
def crear_estado_inicial() -> dict[str, Any]:
    """Crea el estado persistente inicial del agente basado en modelo."""

    return {
        "percepcion_valida": False,  # ¿El último dato era válido?
        "racha_presion_alta": 0,     # ¿Cuántas horas SEGUIDAS con presión alta?
        "presion_anterior": None,    # ¿Cuál fue la presión de la hora anterior?
        "ultima_accion": None,       # ¿Qué acción decidió la últiama vez?
    }



# Actualiza la memoria del agente con lo que acaba de percibir.
# Recibe el estado anterior y la nueva percepción, y devuelve el estado actualizado.
#
# Ejemplo visual de cómo evoluciona el estado:
# Hora 6: presion=1.15 → racha_presion_alta = 0+1 = 1
# Hora 7: presion=1.95 → racha_presion_alta = 1+1 = 2
# Hora 8: presion=3.10 → racha_presion_alta = 2+1 = 3
#
# Si en hora 7 la presion fuera 0.50 → racha_presion_alta = 0 (se RESETEA)
def actualizar_estado(estado_anterior: dict[str, Any], percepcion: dict[str, Any]) -> dict[str, Any]:
    """Actualiza el estado interno del agente."""
    nuevo_estado = estado_anterior.copy()

    # Si la percepción no es válida, reiniciamos el estado. 
    if not _validar_percepcion(percepcion):
        nuevo_estado["percepcion_valida"] = False
        nuevo_estado["racha_presion_alta"] = 0
        nuevo_estado["presion_anterior"] = None
        return nuevo_estado
    
    # Lo que se hace es guardar la percepcion actual en el estado.
    presion_actual = percepcion["presion"]
    nuevo_estado["percepcion_valida"] = True

    # Si la presión supero el umbral, incrementa la recha acumulada
    if presion_actual >= UMBRAL_PRESION:
        nuevo_estado["racha_presion_alta"] = estado_anterior.get("racha_presion_alta", 0) + 1
    else:
        # SI la presion baja, la racha vuelve a 0
        nuevo_estado["racha_presion_alta"] = 0
    
    nuevo_estado["presion_anterior"] = presion_actual
    return nuevo_estado


# Ahora, en base al estado actualizado, el agente toma una decisión.
# Esta función devuelve (accion, motivo) a partir del estado interno actualizado.
def decidir_reactivo_modelo (estado_actual: dict[str, Any]) -> tuple[str, str]:
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""
    
    # Si la percepción no es válida, reiniciamos el estado.
    if not estado_actual.get("percepcion_valida", False): 
        return ("ABSTENERSE", "Percepción invalida o datos faltantes en el estado.")
    
    # Obtenemos la racha de presión alta
    racha = estado_actual.get("racha_presion_alta", 0)

    # Regla: Recomendar solo tras 2 o más horas consecutivas de presión alta
    if racha >= 2: return("RECOMENDAR_REFUERZO", f"Presión alta persistente durante {racha} horas consecutivas.")

    # Regla: No hacer nada si la racha es baja
    return ("NO_REFORZAR", f"Presión alta durante {racha} hora(s); se requieren al menos 2 horas consecutivas.")


# --- PARTE 3: BITÁCORA Y COMPARACIÖN ---

# Esta función corre ambos agentes sobre todas las horas delescenario y guarda los resultads en CSV para comparar.
#
# Ejemplo:
# hora | presion | racha | accion_simple       | accion_modelo
#   6  |  1.15   |   1   | RECOMENDAR_REFUERZO | NO_REFORZAR      ← divergen
#   7  |  1.95   |   2   | RECOMENDAR_REFUERZO | RECOMENDAR_REFUERZO ← coinciden
#   8  |  3.10   |   3   | RECOMENDAR_REFUERZO | RECOMENDAR_REFUERZO ← coinciden
#
def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes en orden temporal y construye la bitácora comparativa."""
    
    estado_modelo = crear_estado_inicial()
    registros = []
    
    for _, fila in percepciones.iterrows():
        percepcion_dict = fila.to_dict()
        
        # 1. Agente Simple
        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion_dict)
        
        # 2. Agente Basado en Modelo
        estado_modelo = actualizar_estado(estado_modelo, percepcion_dict)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado_modelo)
        
        # Actualizamos la última acción en el estado interno
        estado_modelo["ultima_accion"] = accion_modelo
        
        # 3. Guardar fila en la bitácora
        registros.append({
            "hora": percepcion_dict.get("hora"),
            "presion": percepcion_dict.get("presion"),
            "racha_presion_alta": estado_modelo.get("racha_presion_alta"),
            "accion_simple": accion_simple,
            "motivo_simple": motivo_simple,
            "accion_modelo": accion_modelo,
            "motivo_modelo": motivo_modelo,
        })
    return pd.DataFrame(registros)