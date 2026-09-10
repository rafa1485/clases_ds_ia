import pandas as pd

from plantilla_agentes_movilidad import (
    crear_estado_inicial,
    decidir_reactivo_modelo,
    decidir_reactivo_simple,
    actualizar_estado,
)


def test_presion_baja_ambos_no_refuerzan():
    percepcion = {
        "presion": 0.70,
        "capacidad_x": 20,
    }

    accion_simple, _ = decidir_reactivo_simple(percepcion)

    estado = crear_estado_inicial()
    estado = actualizar_estado(estado, percepcion)
    accion_modelo, _ = decidir_reactivo_modelo(estado)

    assert accion_simple == "NO_REFORZAR"
    assert accion_modelo == "NO_REFORZAR"


def test_primera_hora_presion_alta():
    percepcion = {
        "presion": 1.15,
        "capacidad_x": 20,
    }

    accion_simple, _ = decidir_reactivo_simple(percepcion)

    estado = crear_estado_inicial()
    estado = actualizar_estado(estado, percepcion)
    accion_modelo, _ = decidir_reactivo_modelo(estado)

    assert accion_simple == "RECOMENDAR_REFUERZO"
    assert accion_modelo == "NO_REFORZAR"


def test_segunda_hora_consecutiva_presion_alta():
    percepcion_1 = {
        "presion": 1.15,
        "capacidad_x": 20,
    }

    percepcion_2 = {
        "presion": 1.95,
        "capacidad_x": 20,
    }

    estado = crear_estado_inicial()

    estado = actualizar_estado(estado, percepcion_1)
    estado = actualizar_estado(estado, percepcion_2)

    accion_simple, _ = decidir_reactivo_simple(percepcion_2)
    accion_modelo, _ = decidir_reactivo_modelo(estado)

    assert accion_simple == "RECOMENDAR_REFUERZO"
    assert accion_modelo == "RECOMENDAR_REFUERZO"
    
def test_dependencia_historica():
    percepcion_final = {
        "presion": 0.90,
        "capacidad_x": 20,
    }

    # Historia A: dos horas anteriores con presión alta.
    estado_a = crear_estado_inicial()

    estado_a = actualizar_estado(
        estado_a,
        {"presion": 1.20, "capacidad_x": 20},
    )

    estado_a = actualizar_estado(
        estado_a,
        {"presion": 1.10, "capacidad_x": 20},
    )

    estado_a = actualizar_estado(
        estado_a,
        percepcion_final,
    )

    # Historia B: dos horas anteriores con presión baja.
    estado_b = crear_estado_inicial()

    estado_b = actualizar_estado(
        estado_b,
        {"presion": 0.60, "capacidad_x": 20},
    )

    estado_b = actualizar_estado(
        estado_b,
        {"presion": 0.70, "capacidad_x": 20},
    )

    estado_b = actualizar_estado(
        estado_b,
        percepcion_final,
    )

    # El agente simple solo mira la percepción actual.
    accion_simple_a, _ = decidir_reactivo_simple(percepcion_final)
    accion_simple_b, _ = decidir_reactivo_simple(percepcion_final)

    # El modelo sí depende de la historia.
    accion_modelo_a, _ = decidir_reactivo_modelo(estado_a)
    accion_modelo_b, _ = decidir_reactivo_modelo(estado_b)

    assert accion_simple_a == accion_simple_b
    assert accion_simple_a == "RECOMENDAR_REFUERZO"

    assert accion_modelo_a == "RECOMENDAR_REFUERZO"
    assert accion_modelo_b == "NO_REFORZAR"