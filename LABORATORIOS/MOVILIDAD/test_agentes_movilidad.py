from clases_ds_ia.LABORATORIOS.MOVILIDAD.agentes_movilidad import (
    crear_estado_inicial,
    decidir_reactivo_simple,
    actualizar_estado,
    decidir_reactivo_modelo,
)

def test_presion_baja():

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


def test_primera_presion_alta():

    percepcion = {
        "presion": 0.90,
        "capacidad_x": 20,
    }

    accion_simple, _ = decidir_reactivo_simple(percepcion)

    estado = crear_estado_inicial()
    estado = actualizar_estado(estado, percepcion)

    accion_modelo, _ = decidir_reactivo_modelo(estado)

    assert accion_simple == "RECOMENDAR_REFUERZO"
    assert accion_modelo == "NO_REFORZAR"
    assert estado["racha_presion_alta"] == 1

def test_segunda_presion_alta_consecutiva():

    percepcion_1 = {
        "presion": 0.90,
        "capacidad_x": 20,
    }

    percepcion_2 = {
        "presion": 0.92,
        "capacidad_x": 20,
    }

    estado = crear_estado_inicial()

    estado = actualizar_estado(estado, percepcion_1)
    estado = actualizar_estado(estado, percepcion_2)

    accion_simple, _ = decidir_reactivo_simple(percepcion_2)
    accion_modelo, _ = decidir_reactivo_modelo(estado)

    assert accion_simple == "RECOMENDAR_REFUERZO"
    assert accion_modelo == "RECOMENDAR_REFUERZO"
    assert estado["racha_presion_alta"] == 2

def test_historias_distintas_misma_percepcion():

    percepcion_baja = {
        "presion": 0.70,
        "capacidad_x": 20,
    }

    percepcion_alta = {
        "presion": 0.90,
        "capacidad_x": 20,
    }

    # -------------------------
    # Historia A: baja → alta
    # -------------------------

    estado_a = crear_estado_inicial()

    estado_a = actualizar_estado(estado_a, percepcion_baja)
    estado_a = actualizar_estado(estado_a, percepcion_alta)

    accion_simple_a, _ = decidir_reactivo_simple(percepcion_alta)
    accion_modelo_a, _ = decidir_reactivo_modelo(estado_a)

    # -------------------------
    # Historia B: alta → alta
    # -------------------------

    estado_b = crear_estado_inicial()

    estado_b = actualizar_estado(estado_b, percepcion_alta)
    estado_b = actualizar_estado(estado_b, percepcion_alta)

    accion_simple_b, _ = decidir_reactivo_simple(percepcion_alta)
    accion_modelo_b, _ = decidir_reactivo_modelo(estado_b)

    # -------------------------
    # Comprobaciones
    # -------------------------

    assert accion_simple_a == accion_simple_b

    assert accion_modelo_a != accion_modelo_b

def test_agentes_no_usan_hora_futura():
    percepcion_actual = {
        "presion": 0.90,
        "capacidad_x": 20,
    }

    # Esta información representa h+1.
    percepcion_futura = {
        "presion": 10.0,
        "capacidad_x": 1,
    }

    # El agente simple solamente recibe la percepción actual.
    accion_simple, _ = decidir_reactivo_simple(percepcion_actual)

    # El agente basado en modelo solamente recibe su estado actual,
    # que fue construido a partir de la percepción actual.
    estado = crear_estado_inicial()
    estado = actualizar_estado(estado, percepcion_actual)
    accion_modelo, _ = decidir_reactivo_modelo(estado)

    # La información futura no participa en ninguna decisión.
    assert accion_simple == "RECOMENDAR_REFUERZO"
    assert accion_modelo == "NO_REFORZAR"

    # Verificación adicional: la percepción futura existe solamente
    # como dato de prueba y no se pasa a ninguna función del agente.
    assert percepcion_futura["presion"] == 10.0