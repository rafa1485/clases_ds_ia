from plantilla_agentes_movilidad import (  # pyright: ignore[reportMissingImports]
    decidir_reactivo_simple,
    crear_estado_inicial,
    actualizar_estado,
    decidir_reactivo_modelo,
    procesar_secuencia,
)


def ejecutar_pruebas():
    print("--- INICIANDO PRUEBAS OBLIGATORIAS ---")

    # -------------------------------------------------------------
    # CASO 1: Presión baja (Ambos deben devolver NO_REFORZAR)
    # -------------------------------------------------------------
    p_baja = {"hora": 8, "presion": 0.50, "capacidad_x": 100}
    estado_1 = crear_estado_inicial()

    acc_simple, _ = decidir_reactivo_simple(p_baja)

    # 1. Actualizar estado y 2. Decidir
    estado_1 = actualizar_estado(estado_1, p_baja)
    acc_modelo, motivo_modelo = decidir_reactivo_modelo(estado_1)

    assert acc_simple == "NO_REFORZAR", f"Error Simple C1: {acc_simple}"
    assert acc_modelo == "NO_REFORZAR", f"Error Modelo C1: {acc_modelo}"
    print("✓ Caso 1 (Presión baja): PASADO")

    # -------------------------------------------------------------
    # CASO 2: Primera hora con presión alta
    # (Simple -> RECOMENDAR_REFUERZO / Modelo -> NO_REFORZAR o ABSTENERSE)
    # -------------------------------------------------------------
    p_alta = {"hora": 9, "presion": 0.90, "capacidad_x": 100}
    estado_2 = crear_estado_inicial()

    acc_simple, _ = decidir_reactivo_simple(p_alta)

    # 1. Actualizar estado y 2. Decidir
    estado_2 = actualizar_estado(estado_2, p_alta)
    acc_modelo, motivo_modelo = decidir_reactivo_modelo(estado_2)

    assert acc_simple == "RECOMENDAR_REFUERZO", f"Error Simple C2: {acc_simple}"
    assert acc_modelo != "RECOMENDAR_REFUERZO", "Error Modelo C2: El modelo no debió recomendar en la 1ra hora"
    print("✓ Caso 2 (Primera hora alta): PASADO")

    # -------------------------------------------------------------
    # CASO 3: Segunda hora consecutiva con presión alta
    # (Ambos recomiendan refuerzo)
    # -------------------------------------------------------------
    acc_simple, _ = decidir_reactivo_simple(p_alta)

    # 1. Actualizar estado sobre el estado_2 acumulado de la hora anterior
    estado_2 = actualizar_estado(estado_2, p_alta)
    acc_modelo, motivo_modelo = decidir_reactivo_modelo(estado_2)

    assert acc_simple == "RECOMENDAR_REFUERZO", f"Error Simple C3: {acc_simple}"
    assert acc_modelo == "RECOMENDAR_REFUERZO", f"Error Modelo C3: {acc_modelo}"
    print("✓ Caso 3 (Segunda hora alta consecutiva): PASADO")

    # -------------------------------------------------------------
    # PRUEBA: Misma percepción final, dos historias distintas
    # -------------------------------------------------------------
    p_objetivo = {"hora": 10, "presion": 0.90, "capacidad_x": 100}

    # Historia A: Venía de presión baja (0.4) -> Recibe p_objetivo (1ra hora alta)
    historia_A = [
        {"hora": 9, "presion": 0.40, "capacidad_x": 100},
        p_objetivo,
    ]

    # Historia B: Venía de presión alta (0.9) -> Recibe p_objetivo (2da hora alta)
    historia_B = [
        {"hora": 9, "presion": 0.90, "capacidad_x": 100},
        p_objetivo,
    ]

    df_A = procesar_secuencia(historia_A)
    df_B = procesar_secuencia(historia_B)

    # 1. El simple responde igual
    assert df_A.iloc[-1]["accion_simple"] == df_B.iloc[-1]["accion_simple"], (
        "El agente simple falló: debió responder igual ante la misma percepción."
    )

    # 2. El basado en modelo diferencia historias
    assert df_A.iloc[-1]["accion_modelo"] != df_B.iloc[-1]["accion_modelo"], (
        "El agente basado en modelo falló: debió diferenciar las historias."
    )

    print("✓ Prueba Decisiva (Misma percepción, distintas historias): PASADO")

    # -------------------------------------------------------------
    # COMPROBACIÓN DE NO CONSULTAR DATOS DE h+1
    # -------------------------------------------------------------
    p_con_futuro = {
        "hora": 8,
        "presion": 0.50,
        "capacidad_x": 100,
        "h+1": {"presion": 0.99, "capacidad_x": 100},
    }
    est_test = crear_estado_inicial()

    res_simple, _ = decidir_reactivo_simple(p_con_futuro)

    est_test = actualizar_estado(est_test, p_con_futuro)
    res_modelo, _ = decidir_reactivo_modelo(est_test)

    # Dado que la presión actual es 0.50, ignorando h+1, ambos deben responder NO_REFORZAR
    assert res_simple == "NO_REFORZAR", "El agente simple consultó datos de h+1"
    assert res_modelo == "NO_REFORZAR", "El agente basado en modelo consultó datos de h+1"
    print("✓ Comprobación de aislamiento h+1: PASADO")

    print("\n¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")

    # -------------------------------------------------------------
    # GENERACIÓN DEL CSV (bitacora_agentes.csv)
    # -------------------------------------------------------------
    escenario = [
        {"hora": 8, "presion": 0.50, "capacidad_x": 100},
        {"hora": 9, "presion": 0.90, "capacidad_x": 100},
        {"hora": 10, "presion": 0.95, "capacidad_x": 100},
        {"hora": 11, "presion": 0.40, "capacidad_x": 100},
    ]
    df_bitacora = procesar_secuencia(escenario)
    df_bitacora.to_csv("bitacora_agentes.csv", index=False, encoding="utf-8")

    print("\n✓ Archivo 'bitacora_agentes.csv' generado exitosamente.")


if __name__ == "__main__":
    ejecutar_pruebas()