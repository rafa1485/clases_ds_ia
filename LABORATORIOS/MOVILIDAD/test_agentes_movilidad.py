import inspect

import pytest

import agentes_movilidad
from agentes_movilidad import (
    decidir_reactivo_simple,
    actualizar_estado,
    decidir_reactivo_modelo,
    crear_estado_inicial
)

def test_presion_baja():
    # Caso 1: Presión baja. Ambos agentes devuelven NO_REFORZAR.
    percepcion = {"presion": 0.5, "capacidad_x": 20}
    estado = crear_estado_inicial()
    
    accion_s, _ = decidir_reactivo_simple(percepcion)
    assert accion_s == "NO_REFORZAR"
    
    estado = actualizar_estado(estado, percepcion)
    accion_m, _ = decidir_reactivo_modelo(estado)
    assert accion_m == "NO_REFORZAR"

def test_primera_hora_presion_alta():
    # Caso 2: Primera hora con presión alta. El simple recomienda refuerzo y el basado en modelo todavía no.
    percepcion = {"presion": 0.9, "capacidad_x": 20}
    estado = crear_estado_inicial()
    
    accion_s, _ = decidir_reactivo_simple(percepcion)
    assert accion_s == "RECOMENDAR_REFUERZO"
    
    estado = actualizar_estado(estado, percepcion)
    accion_m, _ = decidir_reactivo_modelo(estado)
    assert accion_m == "NO_REFORZAR"

def test_segunda_hora_presion_alta():
    # Caso 3: Segunda hora consecutiva con presión alta. Ambos recomiendan refuerzo.
    percepcion1 = {"presion": 0.9, "capacidad_x": 20}
    percepcion2 = {"presion": 0.95, "capacidad_x": 20}
    estado = crear_estado_inicial()
    
    accion_s, _ = decidir_reactivo_simple(percepcion2)
    assert accion_s == "RECOMENDAR_REFUERZO"
    
    estado = actualizar_estado(estado, percepcion1)
    estado = actualizar_estado(estado, percepcion2)
    accion_m, _ = decidir_reactivo_modelo(estado)
    assert accion_m == "RECOMENDAR_REFUERZO"
    
def test_historias_distintas():
    # Caso 4: Prueba decisiva. Dos historias terminan en la misma percepción.
    percepcion_final = {"presion": 0.9, "capacidad_x": 20}
    
    # Historia 1: venía de presión baja
    estado1 = crear_estado_inicial()
    estado1 = actualizar_estado(estado1, {"presion": 0.5, "capacidad_x": 20})
    estado1 = actualizar_estado(estado1, percepcion_final)
    accion_m1, _ = decidir_reactivo_modelo(estado1)
    
    # Historia 2: venía de presión alta
    estado2 = crear_estado_inicial()
    estado2 = actualizar_estado(estado2, {"presion": 0.9, "capacidad_x": 20})
    estado2 = actualizar_estado(estado2, percepcion_final)
    accion_m2, _ = decidir_reactivo_modelo(estado2)
    
    # Simple da lo mismo en ambas, modelo da distinto
    accion_s1, _ = decidir_reactivo_simple(percepcion_final)
    accion_s2, _ = decidir_reactivo_simple(percepcion_final)
    
    assert accion_s1 == accion_s2 == "RECOMENDAR_REFUERZO"
    assert accion_m1 == "NO_REFORZAR"
    assert accion_m2 == "RECOMENDAR_REFUERZO"


def test_funciones_de_decision_no_usan_h_mas_1():
    # Ninguna función de decisión recibe ni consulta datos de h+1.
    firmas = {
        decidir_reactivo_simple: {"percepcion"},
        actualizar_estado: {"estado_anterior", "percepcion"},
        decidir_reactivo_modelo: {"estado_actual"},
    }
    for funcion, parametros_esperados in firmas.items():
        parametros_reales = set(inspect.signature(funcion).parameters)
        assert parametros_reales == parametros_esperados

    codigo_fuente = inspect.getsource(agentes_movilidad)
    assert "resultado_h_mas_1" not in codigo_fuente
    assert "h_mas_1" not in codigo_fuente

