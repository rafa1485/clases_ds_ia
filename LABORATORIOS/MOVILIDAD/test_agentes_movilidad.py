"""Pruebas del trabajo practico de agentes de movilidad.

Autor: Ezequiel Zunino.

Ejecutar con: python -m pytest test_agentes_movilidad.py
"""

from __future__ import annotations

import inspect
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import agentes_movilidad
from agentes_movilidad import (
    ACCIONES,
    actualizar_estado,
    crear_estado_inicial,
    decidir_reactivo_modelo,
    decidir_reactivo_simple,
    procesar_secuencia,
)


BAJA = 0.50
ALTA = 1.20


def percepcion(presion: float, hora: int = 8, capacidad: float = 20) -> dict:
    return {
        "zona_id": 161,
        "zona": "Midtown Center",
        "hora": hora,
        "taxis_x": capacidad,
        "demanda_x": presion * capacidad,
        "capacidad_x": capacidad,
        "presion": presion,
    }


def correr_modelo(presiones: list[float]) -> tuple[str, dict]:
    """Pasa una historia por el agente y devuelve la ultima accion y el estado."""
    estado = crear_estado_inicial()
    accion = None
    for hora, presion in enumerate(presiones):
        estado = actualizar_estado(estado, percepcion(presion, hora))
        accion, _ = decidir_reactivo_modelo(estado)
    return accion, estado


# Casos obligatorios


def test_presion_baja_ambos_no_refuerzan():
    assert decidir_reactivo_simple(percepcion(BAJA))[0] == "NO_REFORZAR"
    assert correr_modelo([BAJA])[0] == "NO_REFORZAR"


def test_primera_hora_alta_solo_el_simple_recomienda():
    assert decidir_reactivo_simple(percepcion(ALTA))[0] == "RECOMENDAR_REFUERZO"
    assert correr_modelo([ALTA])[0] == "NO_REFORZAR"


def test_segunda_hora_alta_ambos_recomiendan():
    assert decidir_reactivo_simple(percepcion(ALTA))[0] == "RECOMENDAR_REFUERZO"
    assert correr_modelo([ALTA, ALTA])[0] == "RECOMENDAR_REFUERZO"


def test_prueba_decisiva_misma_percepcion_con_historias_distintas():
    historia_baja = [BAJA, ALTA]
    historia_alta = [ALTA, ALTA]
    ultima = percepcion(ALTA, hora=1)

    # Mismo ultimo dato: el simple no puede distinguir las historias.
    acciones_simple = {decidir_reactivo_simple(ultima) for _ in range(2)}
    assert len(acciones_simple) == 1

    assert correr_modelo(historia_baja)[0] == "NO_REFORZAR"
    assert correr_modelo(historia_alta)[0] == "RECOMENDAR_REFUERZO"


# Reglas y bordes


def test_el_umbral_cuenta_como_presion_alta():
    assert decidir_reactivo_simple(percepcion(0.85))[0] == "RECOMENDAR_REFUERZO"
    assert decidir_reactivo_simple(percepcion(0.8499))[0] == "NO_REFORZAR"
    assert correr_modelo([0.85, 0.85])[0] == "RECOMENDAR_REFUERZO"


@pytest.mark.parametrize(
    "cambios",
    [
        {"presion": None},
        {"presion": float("nan")},
        {"presion": "alta"},
        {"presion": True},
        {"presion": -0.1},
        {"presion": float("inf")},
        {"capacidad_x": None},
        {"capacidad_x": float("nan")},
        {"capacidad_x": -1},
        {"capacidad_x": float("inf")},
        {"demanda_x": -3},
        {"taxis_x": "veinte"},
        {"tasa_otras_simulada": 1.5},
    ],
)
def test_datos_invalidos_producen_abstencion(cambios):
    invalida = {**percepcion(ALTA), **cambios}

    assert decidir_reactivo_simple(invalida)[0] == "ABSTENERSE"
    estado = actualizar_estado(crear_estado_inicial(), invalida)
    assert decidir_reactivo_modelo(estado)[0] == "ABSTENERSE"


@pytest.mark.parametrize("campo", ["presion", "capacidad_x"])
def test_campo_requerido_ausente_produce_abstencion(campo):
    incompleta = percepcion(ALTA)
    del incompleta[campo]

    assert decidir_reactivo_simple(incompleta)[0] == "ABSTENERSE"
    estado = actualizar_estado(crear_estado_inicial(), incompleta)
    assert decidir_reactivo_modelo(estado)[0] == "ABSTENERSE"


def test_percepcion_que_no_es_registro_produce_abstencion():
    assert decidir_reactivo_simple(None)[0] == "ABSTENERSE"


def test_flota_cero_del_simulador():
    con_demanda = {"capacidad_x": 0, "presion": float("inf")}
    sin_demanda = {"capacidad_x": 0, "presion": 0.0}

    assert decidir_reactivo_simple(con_demanda)[0] == "RECOMENDAR_REFUERZO"
    assert decidir_reactivo_simple(sin_demanda)[0] == "NO_REFORZAR"


def test_acepta_tipos_de_numpy():
    registro = {"capacidad_x": np.int64(20), "presion": np.float64(ALTA)}
    assert decidir_reactivo_simple(registro)[0] == "RECOMENDAR_REFUERZO"


def test_las_acciones_pertenecen_al_conjunto_permitido():
    casos = [percepcion(BAJA), percepcion(ALTA), {"presion": None}]
    assert {decidir_reactivo_simple(caso)[0] for caso in casos} == ACCIONES


# Estado interno


def test_la_racha_crece_y_se_reinicia():
    estado = crear_estado_inicial()
    rachas = []
    for presion in [ALTA, ALTA, BAJA, ALTA]:
        estado = actualizar_estado(estado, percepcion(presion))
        rachas.append(estado["racha_presion_alta"])

    assert rachas == [1, 2, 0, 1]
    assert estado["presion_anterior"] == ALTA


def test_un_dato_invalido_corta_la_racha():
    _, estado = correr_modelo([ALTA, ALTA])
    estado = actualizar_estado(estado, {"presion": float("nan")})

    assert estado["percepcion_valida"] is False
    assert estado["racha_presion_alta"] == 0
    assert estado["presion_anterior"] is None

    estado = actualizar_estado(estado, percepcion(ALTA))
    assert decidir_reactivo_modelo(estado)[0] == "NO_REFORZAR"


def test_actualizar_no_modifica_el_estado_anterior():
    anterior = crear_estado_inicial()
    copia = dict(anterior)

    actualizar_estado(anterior, percepcion(ALTA))

    assert anterior == copia


def test_procesar_secuencia_conserva_la_ultima_accion(monkeypatch):
    estados = []
    original = agentes_movilidad.actualizar_estado

    def espiar(estado, registro):
        estados.append(dict(estado))
        return original(estado, registro)

    monkeypatch.setattr(agentes_movilidad, "actualizar_estado", espiar)
    procesar_secuencia(pd.DataFrame([percepcion(ALTA, 6), percepcion(ALTA, 7)]))

    assert estados[1]["ultima_accion"] == "NO_REFORZAR"


# Bitacora


def test_bitacora_tiene_los_campos_pedidos_y_orden_temporal():
    desordenadas = pd.DataFrame(
        [percepcion(ALTA, 7), percepcion(BAJA, 6), percepcion(ALTA, 8)]
    )

    bitacora = procesar_secuencia(desordenadas)

    assert list(bitacora.columns) == [
        "hora",
        "presion",
        "racha_presion_alta",
        "accion_simple",
        "motivo_simple",
        "accion_modelo",
        "motivo_modelo",
    ]
    assert bitacora["hora"].tolist() == [6, 7, 8]
    assert bitacora["racha_presion_alta"].tolist() == [0, 1, 2]
    assert bitacora["accion_simple"].tolist() == [
        "NO_REFORZAR",
        "RECOMENDAR_REFUERZO",
        "RECOMENDAR_REFUERZO",
    ]
    assert bitacora["accion_modelo"].tolist() == [
        "NO_REFORZAR",
        "NO_REFORZAR",
        "RECOMENDAR_REFUERZO",
    ]


def test_bitacora_registra_abstencion_de_una_fila_con_nan():
    filas = pd.DataFrame(
        [percepcion(ALTA, 6), percepcion(float("nan"), 7), percepcion(ALTA, 8)]
    )

    bitacora = procesar_secuencia(filas)

    assert bitacora["accion_simple"].iloc[1] == "ABSTENERSE"
    assert bitacora["accion_modelo"].iloc[1] == "ABSTENERSE"
    assert bitacora["racha_presion_alta"].tolist() == [1, 0, 1]


# Causalidad temporal


def test_las_decisiones_no_reciben_datos_de_h_mas_1():
    firmas = {
        decidir_reactivo_simple: ["percepcion"],
        actualizar_estado: ["estado_anterior", "percepcion"],
        decidir_reactivo_modelo: ["estado_actual"],
    }
    for funcion, parametros in firmas.items():
        assert list(inspect.signature(funcion).parameters) == parametros


def test_un_campo_futuro_agregado_no_cambia_la_decision():
    limpia = percepcion(BAJA)
    con_futuro = {**limpia, "necesita_refuerzo": True, "demanda_x_h_mas_1": 999}

    assert decidir_reactivo_simple(con_futuro) == decidir_reactivo_simple(limpia)
    assert actualizar_estado(crear_estado_inicial(), con_futuro) == (
        actualizar_estado(crear_estado_inicial(), limpia)
    )


def test_el_codigo_no_consulta_el_archivo_de_evaluacion():
    fuente = Path(inspect.getfile(agentes_movilidad)).read_text(encoding="utf-8")

    assert "resultado_h_mas_1" not in fuente
    assert "necesita_refuerzo" not in fuente


def test_el_futuro_no_altera_las_decisiones_pasadas():
    pasado = pd.DataFrame([percepcion(ALTA, 6), percepcion(BAJA, 7)])
    con_futuro_a = pd.concat(
        [pasado, pd.DataFrame([percepcion(ALTA, 8)])], ignore_index=True
    )
    con_futuro_b = pd.concat(
        [pasado, pd.DataFrame([percepcion(BAJA, 8)])], ignore_index=True
    )

    esperado = procesar_secuencia(pasado)

    for completo in (con_futuro_a, con_futuro_b):
        obtenido = procesar_secuencia(completo).iloc[:2]
        pd.testing.assert_frame_equal(obtenido, esperado)
