import pytest
from agentes_movilidad import (
    decidir_reactivo_simple,
    actualizar_estado,
    decidir_reactivo_modelo,
    inicializar_estado,
    NO_REFORZAR,
    RECOMENDAR_REFUERZO,
    ABSTENERSE
)

def test_caso_presion_baja():
    """Caso 1: Presión baja -> Ambos devuelven NO_REFORZAR"""
    percepcion = {"hora": 5, "presion": 0.40, "capacidad_x": 20}
    
    # Simple
    acc_simple, _ = decidir_reactivo_simple(percepcion)
    assert acc_simple == NO_REFORZAR
    
    # Modelo
    estado = inicializar_estado()
    estado = actualizar_estado(estado, percepcion)
    acc_modelo, _ = decidir_reactivo_modelo(estado)
    assert acc_modelo == NO_REFORZAR

def test_primera_hora_presion_alta():
    """Caso 2: 1ra hora alta -> Simple refuerza, Modelo todavía no"""
    percepcion = {"hora": 6, "presion": 0.90, "capacidad_x": 20}
    
    # Simple
    acc_simple, _ = decidir_reactivo_simple(percepcion)
    assert acc_simple == RECOMENDAR_REFUERZO
    
    # Modelo
    estado = inicializar_estado()
    estado = actualizar_estado(estado, percepcion)
    acc_modelo, _ = decidir_reactivo_modelo(estado)
    assert acc_modelo == NO_REFORZAR
    assert estado["racha_presion_alta"] == 1

def test_segunda_hora_consecutiva_presion_alta():
    """Caso 3: 2da hora consecutiva alta -> Ambos recomiendan refuerzo"""
    p1 = {"hora": 6, "presion": 0.90, "capacidad_x": 20}
    p2 = {"hora": 7, "presion": 0.95, "capacidad_x": 20}
    
    # Simple en p2
    acc_simple, _ = decidir_reactivo_simple(p2)
    assert acc_simple == RECOMENDAR_REFUERZO
    
    # Modelo a lo largo de las 2 horas
    estado = inicializar_estado()
    estado = actualizar_estado(estado, p1)
    estado = actualizar_estado(estado, p2)
    acc_modelo, _ = decidir_reactivo_modelo(estado)
    assert acc_modelo == RECOMENDAR_REFUERZO
    assert estado["racha_presion_alta"] == 2

def test_prueba_decisiva_dependencia_historica():
    """
    Caso 4 (Decisivo): Misma observación actual (presion=0.90),
    pero historias previas diferentes.
    - Historia A: venía de presión baja (racha 1).
    - Historia B: venía de presión alta (racha 2).
    """
    percepcion_actual = {"hora": 8, "presion": 0.90, "capacidad_x": 20}
    
    # El agente simple actúa igual en ambos casos (no tiene memoria)
    acc_simple_A, _ = decidir_reactivo_simple(percepcion_actual)
    acc_simple_B, _ = decidir_reactivo_simple(percepcion_actual)
    assert acc_simple_A == acc_simple_B == RECOMENDAR_REFUERZO
    
    # Historia A: Hora 7 tuvo presión baja
    estado_A = inicializar_estado()
    estado_A = actualizar_estado(estado_A, {"hora": 7, "presion": 0.50, "capacidad_x": 20})
    estado_A = actualizar_estado(estado_A, percepcion_actual)
    acc_modelo_A, _ = decidir_reactivo_modelo(estado_A)
    
    # Historia B: Hora 7 tuvo presión alta
    estado_B = inicializar_estado()
    estado_B = actualizar_estado(estado_B, {"hora": 7, "presion": 0.95, "capacidad_x": 20})
    estado_B = actualizar_estado(estado_B, percepcion_actual)
    acc_modelo_B, _ = decidir_reactivo_modelo(estado_B)
    
    # Verificación de divergencia por memoria interna
    assert acc_modelo_A == NO_REFORZAR
    assert acc_modelo_B == RECOMENDAR_REFUERZO

def test_datos_invalidos():
    """Verificación de abstención ante corrupción de datos"""
    percepcion_invalida = {"hora": 8, "presion": None, "capacidad_x": 0}
    
    acc_simple, _ = decidir_reactivo_simple(percepcion_invalida)
    assert acc_simple == ABSTENERSE
    
    estado = inicializar_estado()
    estado = actualizar_estado(estado, percepcion_invalida)
    acc_modelo, _ = decidir_reactivo_modelo(estado)
    assert acc_modelo == ABSTENERSE
