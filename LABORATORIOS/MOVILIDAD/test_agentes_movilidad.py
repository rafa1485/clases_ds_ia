"""Pruebas unitarias para validar los agentes de movilidad y su comportamiento histórico."""

from agentes_movilidad import (
    crear_estado_inicial,
    actualizar_estado,
    decidir_reactivo_simple,
    decidir_reactivo_modelo,
)


def test_presion_baja():
    """Caso 1: Presión baja produce NO_REFORZAR en ambos agentes."""
    percepcion = {"capacidad_x": 20, "presion": 0.50}

    # Agente simple
    accion_s, _ = decidir_reactivo_simple(percepcion)
    assert accion_s == "NO_REFORZAR"

    # Agente basado en modelo
    estado = crear_estado_inicial()
    estado = actualizar_estado(estado, percepcion)
    accion_m, _ = decidir_reactivo_modelo(estado)
    assert accion_m == "NO_REFORZAR"


def test_primera_hora_presion_alta():
    """Caso 2: Primera hora con presión alta -> Simple recomienda, Modelo NO."""
    percepcion = {"capacidad_x": 20, "presion": 0.90}

    # Agente simple
    accion_s, _ = decidir_reactivo_simple(percepcion)
    assert accion_s == "RECOMENDAR_REFUERZO"

    # Agente basado en modelo (solo 1 hora alta -> racha = 1)
    estado = crear_estado_inicial()
    estado = actualizar_estado(estado, percepcion)
    accion_m, _ = decidir_reactivo_modelo(estado)
    assert accion_m == "NO_REFORZAR"


def test_segunda_hora_consecutiva_presion_alta():
    """Caso 3: Segunda hora consecutiva -> Ambos recomiendan refuerzo."""
    p1 = {"capacidad_x": 20, "presion": 0.90}
    p2 = {"capacidad_x": 20, "presion": 0.88}

    # Agente basado en modelo procesa 2 horas altas seguidas
    estado = crear_estado_inicial()
    estado = actualizar_estado(estado, p1)
    estado = actualizar_estado(estado, p2)
    accion_m, _ = decidir_reactivo_modelo(estado)

    assert estado["racha_presion_alta"] == 2
    assert accion_m == "RECOMENDAR_REFUERZO"


def test_demostramente_dependencia_historia():
    """Prueba decisiva: Misma percepción final, distintas historias previas.
    
    Historia A: [Baja (0.50), Alta (0.90)]
    Historia B: [Alta (0.90), Alta (0.90)]
    """
    p_baja = {"capacidad_x": 20, "presion": 0.50}
    p_alta = {"capacidad_x": 20, "presion": 0.90}

    # --- HISTORIA A ---
    estado_a = crear_estado_inicial()
    estado_a = actualizar_estado(estado_a, p_baja)
    estado_a = actualizar_estado(estado_a, p_alta)

    accion_simple_a, _ = decidir_reactivo_simple(p_alta)
    accion_modelo_a, _ = decidir_reactivo_modelo(estado_a)

    # --- HISTORIA B ---
    estado_b = crear_estado_inicial()
    estado_b = actualizar_estado(estado_b, p_alta)
    estado_b = actualizar_estado(estado_b, p_alta)

    accion_simple_b, _ = decidir_reactivo_simple(p_alta)
    accion_modelo_b, _ = decidir_reactivo_modelo(estado_b)

    # El agente simple reacciona IGUAL ante la misma percepción final (sin memoria)
    assert accion_simple_a == accion_simple_b == "RECOMENDAR_REFUERZO"

    # El agente basado en modelo reacciona DIFERENTE por su historia previa
    assert accion_modelo_a == "NO_REFORZAR"
    assert accion_modelo_b == "RECOMENDAR_REFUERZO"


def test_percepcion_invalida():
    """Comprueba que ante datos corruptos o incompletos ambos respondan ABSTENERSE."""
    percepcion_invalida = {"capacidad_x": 0, "presion": -1}

    accion_s, _ = decidir_reactivo_simple(percepcion_invalida)
    assert accion_s == "ABSTENERSE"

    estado = crear_estado_inicial()
    estado = actualizar_estado(estado, percepcion_invalida)
    accion_m, _ = decidir_reactivo_modelo(estado)
    assert accion_m == "ABSTENERSE"


if __name__ == "__main__":
    test_presion_baja()
    test_primera_hora_presion_alta()
    test_segunda_hora_consecutiva_presion_alta()
    test_demostramente_dependencia_historia()
    test_percepcion_invalida()
    print("✅ ¡Todos los tests pasaron exitosamente!")

