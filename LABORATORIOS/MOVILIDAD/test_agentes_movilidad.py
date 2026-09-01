"""Pruebas obligatorias para los agentes de refuerzo de taxis.

Cada prueba está comentada con la sección de la consigna
(`consigna_agentes_movilidad.md`) que intenta demostrar.
"""

from __future__ import annotations

import inspect
from typing import Any

import pandas as pd

from agentes_movilidad import (
    actualizar_estado,
    crear_estado_inicial,
    decidir_reactivo_modelo,
    decidir_reactivo_simple,
    procesar_secuencia,
)


def _percepcion(
    hora: int,
    presion: float,
    capacidad_x: float = 10,
    demanda_x: float | None = None,
    taxis_x: int = 10,
) -> dict[str, Any]:
    """Arma una percepcion de ejemplo con la misma forma que produce el
    simulador (`COLUMNAS_PERCEPCION` en simulador_entorno_agente.py)."""
    if demanda_x is None:
        demanda_x = round(presion * capacidad_x)
    return {
        "zona_id": 161,
        "zona": "Zona de prueba",
        "hora": hora,
        "taxis_x": taxis_x,
        "demanda_total": demanda_x + 5,
        "tasa_otras_simulada": 0.3,
        "viajes_otras": 5,
        "demanda_x": demanda_x,
        "capacidad_x": capacidad_x,
        "viajes_atendibles_x": min(demanda_x, capacidad_x),
        "demanda_no_cubierta_x": max(demanda_x - capacidad_x, 0),
        "presion": presion,
    }


# --- Caso 1: presión baja -> ambos agentes NO_REFORZAR ---------------------


def test_presion_baja_ambos_no_refuerzan():
    percepcion = _percepcion(hora=8, presion=0.5)

    accion_simple, _ = decidir_reactivo_simple(percepcion)
    estado = actualizar_estado(crear_estado_inicial(), percepcion)
    accion_modelo, _ = decidir_reactivo_modelo(estado)

    assert accion_simple == "NO_REFORZAR"
    assert accion_modelo == "NO_REFORZAR"


# --- Caso 2: primera hora con presión alta ----------------------------------


def test_primera_hora_presion_alta_solo_simple_recomienda():
    percepcion = _percepcion(hora=8, presion=0.9)

    accion_simple, _ = decidir_reactivo_simple(percepcion)
    estado = actualizar_estado(crear_estado_inicial(), percepcion)
    accion_modelo, _ = decidir_reactivo_modelo(estado)

    assert accion_simple == "RECOMENDAR_REFUERZO"
    assert accion_modelo == "NO_REFORZAR"
    assert estado["racha_presion_alta"] == 1


# --- Caso 3: segunda hora consecutiva con presión alta ----------------------


def test_segunda_hora_consecutiva_ambos_recomiendan():
    estado = crear_estado_inicial()
    estado = actualizar_estado(estado, _percepcion(hora=8, presion=0.9))

    percepcion_2 = _percepcion(hora=9, presion=0.95)
    accion_simple, _ = decidir_reactivo_simple(percepcion_2)
    estado = actualizar_estado(estado, percepcion_2)
    accion_modelo, _ = decidir_reactivo_modelo(estado)

    assert accion_simple == "RECOMENDAR_REFUERZO"
    assert accion_modelo == "RECOMENDAR_REFUERZO"
    assert estado["racha_presion_alta"] == 2


# --- Prueba decisiva: misma percepción final, historias distintas ----------


def test_misma_percepcion_final_con_historias_distintas():
    percepcion_final = _percepcion(hora=8, presion=0.9)

    # Historia A: hora 7 con presión baja, hora 8 con presión alta (racha=1).
    estado_a = actualizar_estado(crear_estado_inicial(), _percepcion(hora=7, presion=0.2))
    estado_a = actualizar_estado(estado_a, percepcion_final)

    # Historia B: hora 7 YA con presión alta, hora 8 repite (racha=2).
    estado_b = actualizar_estado(crear_estado_inicial(), _percepcion(hora=7, presion=0.9))
    estado_b = actualizar_estado(estado_b, percepcion_final)

    accion_simple_a, _ = decidir_reactivo_simple(percepcion_final)
    accion_simple_b, _ = decidir_reactivo_simple(percepcion_final)
    accion_modelo_a, _ = decidir_reactivo_modelo(estado_a)
    accion_modelo_b, _ = decidir_reactivo_modelo(estado_b)

    # El agente simple no tiene memoria: misma percepción -> misma acción.
    assert accion_simple_a == accion_simple_b == "RECOMENDAR_REFUERZO"

    # El agente con memoria sí distingue el historial previo.
    assert accion_modelo_a == "NO_REFORZAR"
    assert accion_modelo_b == "RECOMENDAR_REFUERZO"
    assert accion_modelo_a != accion_modelo_b


# --- Percepciones inválidas -> ABSTENERSE -----------------------------------


def test_capacidad_desconocida_abstiene():
    # capacidad_x=0 hace que la presión quede indefinida (infinita).
    percepcion = _percepcion(hora=8, presion=float("inf"), capacidad_x=0, demanda_x=5)

    accion_simple, _ = decidir_reactivo_simple(percepcion)
    estado = actualizar_estado(crear_estado_inicial(), percepcion)
    accion_modelo, _ = decidir_reactivo_modelo(estado)

    assert accion_simple == "ABSTENERSE"
    assert accion_modelo == "ABSTENERSE"


def test_campo_faltante_abstiene():
    percepcion = _percepcion(hora=8, presion=0.9)
    del percepcion["capacidad_x"]

    accion_simple, _ = decidir_reactivo_simple(percepcion)

    assert accion_simple == "ABSTENERSE"


# --- Causalidad temporal: nada de h+1 -------------------------------------


def test_funciones_de_decision_no_reciben_datos_futuros():
    # Las firmas solo aceptan la percepción/estado actual: no hay forma de
    # pasarles el archivo resultado_h_mas_1.csv aunque se quisiera.
    assert list(inspect.signature(decidir_reactivo_simple).parameters) == ["percepcion"]
    assert list(inspect.signature(decidir_reactivo_modelo).parameters) == ["estado_actual"]


def test_procesar_secuencia_ignora_cambios_futuros():
    percepciones = pd.DataFrame(
        [
            _percepcion(hora=7, presion=0.3),
            _percepcion(hora=8, presion=0.9),
            _percepcion(hora=9, presion=0.9),
        ]
    )
    bitacora_original = procesar_secuencia(percepciones)

    # Alteramos solo la última hora (la más "futura" de la secuencia).
    percepciones_alteradas = percepciones.copy()
    percepciones_alteradas.loc[percepciones_alteradas["hora"] == 9, "presion"] = 0.0
    bitacora_alterada = procesar_secuencia(percepciones_alteradas)

    pasado_original = bitacora_original.loc[bitacora_original["hora"] < 9].reset_index(drop=True)
    pasado_alterado = bitacora_alterada.loc[bitacora_alterada["hora"] < 9].reset_index(drop=True)

    pd.testing.assert_frame_equal(pasado_original, pasado_alterado)
