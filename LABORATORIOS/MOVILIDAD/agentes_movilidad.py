import pandas as pd
import numpy as np

# Acciones permitidas
NO_REFORZAR = "NO_REFORZAR"
RECOMENDAR_REFUERZO = "RECOMENDAR_REFUERZO"
ABSTENERSE = "ABSTENERSE"

# -------------------------------------------------------------
# PARTE 1: Agente Reactivo Simple
# -------------------------------------------------------------
def decidir_reactivo_simple(percepcion):
    """
    Decide únicamente con la percepción actual.
    Retorna: (accion, motivo)
    """
    if percepcion is None:
        return ABSTENERSE, "Percepción nula"
    
    presion = percepcion.get("presion")
    capacidad = percepcion.get("capacidad_x")
    
    # Validaciones de entrada
    if presion is None or capacidad is None or capacidad <= 0 or pd.isna(presion):
        return ABSTENERSE, "Datos inválidos o capacidad desconocida"
    
    # Reglas condición-acción
    if presion >= 0.85:
        return RECOMENDAR_REFUERZO, f"Presión alta detectada en hora actual ({presion:.2f} >= 0.85)"
    else:
        return NO_REFORZAR, f"Presión dentro de límites normales ({presion:.2f} < 0.85)"


# -------------------------------------------------------------
# PARTE 2: Agente Reactivo Basado en Modelo
# -------------------------------------------------------------
def inicializar_estado():
    return {
        "percepcion_valida": False,
        "racha_presion_alta": 0,
        "presion_anterior": None,
        "ultima_accion": None,
    }

def actualizar_estado(estado_anterior, percepcion):
    """
    Actualiza el estado interno agregando la historia reciente.
    """
    if estado_anterior is None:
        estado_anterior = inicializar_estado()
        
    if percepcion is None:
        return {
            "percepcion_valida": False,
            "racha_presion_alta": 0,
            "presion_anterior": estado_anterior.get("presion_anterior"),
            "ultima_accion": estado_anterior.get("ultima_accion")
        }
        
    presion = percepcion.get("presion")
    capacidad = percepcion.get("capacidad_x")
    
    # Validación
    if presion is None or capacidad is None or capacidad <= 0 or pd.isna(presion):
        return {
            "percepcion_valida": False,
            "racha_presion_alta": 0,
            "presion_anterior": estado_anterior.get("presion_anterior"),
            "ultima_accion": estado_anterior.get("ultima_accion")
        }
    
    # Actualización de racha
    racha_actual = estado_anterior.get("racha_presion_alta", 0)
    if presion >= 0.85:
        nueva_racha = racha_actual + 1
    else:
        nueva_racha = 0
        
    return {
        "percepcion_valida": True,
        "racha_presion_alta": nueva_racha,
        "presion_anterior": presion,
        "ultima_accion": estado_anterior.get("ultima_accion")
    }

def decidir_reactivo_modelo(estado_actual):
    """
    Decide en función del estado interno acumulado.
    Retorna: (accion, motivo)
    """
    if not estado_actual or not estado_actual.get("percepcion_valida", False):
        return ABSTENERSE, "Estado inválido o percepción corrupta"
    
    racha = estado_actual.get("racha_presion_alta", 0)
    presion = estado_actual.get("presion_anterior")
    
    if racha >= 2:
        return RECOMENDAR_REFUERZO, f"Presión alta sostenida por {racha} horas consecutivas"
    else:
        return NO_REFORZAR, f"Presión alta no sostenida (racha: {racha} hora/s, presion: {presion:.2f})"


# -------------------------------------------------------------
# PARTE 3: Procesamiento de Secuencia (Bitácora)
# -------------------------------------------------------------
def procesar_secuencia(percepciones_df):
    """
    Recorre cronológicamente las percepciones y compara ambos agentes.
    """
    bitacora = []
    estado = inicializar_estado()
    
    for _, fila in percepciones_df.iterrows():
        percepcion = fila.to_dict()
        hora = percepcion.get("hora")
        presion = percepcion.get("presion")
        
        # 1. Agente Reactivo Simple
        acc_simple, mot_simple = decidir_reactivo_simple(percepcion)
        
        # 2. Agente Reactivo Basado en Modelo
        estado = actualizar_estado(estado, percepcion)
        acc_modelo, mot_modelo = decidir_reactivo_modelo(estado)
        estado["ultima_accion"] = acc_modelo
        
        bitacora.append({
            "hora": hora,
            "presion": presion,
            "racha_presion_alta": estado["racha_presion_alta"],
            "accion_simple": acc_simple,
            "motivo_simple": mot_simple,
            "accion_modelo": acc_modelo,
            "motivo_modelo": mot_modelo
        })
        
    return pd.DataFrame(bitacora)
