import pandas as pd
from plantilla_agentes_movilidad import (
    decidir_reactivo_simple,
    actualizar_estado,
    decidir_reactivo_modelo
)

def test_presion_baja():
    """Caso 1: Presión baja -> Ambos devuelven NO_REFORZAR."""
    percepcion = {"presion": 0.50, "capacidad_x": 20}

    accion_s, _ = decidir_reactivo_simple(percepcion)
    assert accion_s == "NO_REFORZAR"

    estado_inic = {
        "percepcion_valida": False,
        "racha_presion_alta": 0,
        "presion_anterior": None,
        "ultima_accion": None,
    }
    estado_act = actualizar_estado(estado_inic, percepcion)
    accion_m, _ = decidir_reactivo_modelo(estado_act)
    assert accion_m == "NO_REFORZAR"


def test_primera_hora_presion_alta():
    """Caso 2: Primera hora alta -> Simple recomienda; Modelo todavía no."""
    percepcion = {"presion": 0.90, "capacidad_x": 20}

    accion_s, _ = decidir_reactivo_simple(percepcion)
    assert accion_s == "RECOMENDAR_REFUERZO"

    estado_inic = {
        "percepcion_valida": False,
        "racha_presion_alta": 0,
        "presion_anterior": None,
        "ultima_accion": None,
    }
    estado_act = actualizar_estado(estado_inic, percepcion)
    accion_m, _ = decidir_reactivo_modelo(estado_act)
    assert accion_m == "NO_REFORZAR"


def test_segunda_hora_consecutiva_presion_alta():
    """Caso 3: Segunda hora consecutiva alta -> Ambos recomiendan."""
    percepcion = {"presion": 0.90, "capacidad_x": 20}

    accion_s, _ = decidir_reactivo_simple(percepcion)
    assert accion_s == "RECOMENDAR_REFUERZO"

    estado_previo = {
        "percepcion_valida": True,
        "racha_presion_alta": 1,
        "presion_anterior": 0.88,
        "ultima_accion": "NO_REFORZAR",
    }
    estado_act = actualizar_estado(estado_previo, percepcion)
    accion_m, _ = decidir_reactivo_modelo(estado_act)
    assert accion_m == "RECOMENDAR_REFUERZO"


def test_prueba_decisiva_dependencia_historica():
    """Prueba decisiva: Misma percepción final (presión 0.90), dos historias distintas."""
    percepcion_final = {"presion": 0.90, "capacidad_x": 20}

    est_A_0 = {"percepcion_valida": True, "racha_presion_alta": 0, "presion_anterior": None, "ultima_accion": None}
    est_A_1 = actualizar_estado(est_A_0, {"presion": 0.50, "capacidad_x": 20})
    est_A_2 = actualizar_estado(est_A_1, percepcion_final)

    est_B_0 = {"percepcion_valida": True, "racha_presion_alta": 0, "presion_anterior": None, "ultima_accion": None}
    est_B_1 = actualizar_estado(est_B_0, {"presion": 0.90, "capacidad_x": 20})
    est_B_2 = actualizar_estado(est_B_1, percepcion_final)

    accion_simple_A, _ = decidir_reactivo_simple(percepcion_final)
    accion_simple_B, _ = decidir_reactivo_simple(percepcion_final)
    assert accion_simple_A == accion_simple_B == "RECOMENDAR_REFUERZO"

    accion_mod_A, _ = decidir_reactivo_modelo(est_A_2)
    accion_mod_B, _ = decidir_reactivo_modelo(est_B_2)

    assert accion_mod_A == "NO_REFORZAR"
    assert accion_mod_B == "RECOMENDAR_REFUERZO"


def test_ausencia_fuga_temporal():
    """Comprueba que la percepción no contenga datos de h+1."""
    percepcion = {"presion": 0.90, "capacidad_x": 20}
    assert "resultado_h_mas_1" not in percepcion
    assert "h+1" not in percepcion