"""Pruebas de los agentes reactivos de movilidad."""

from __future__ import annotations

import inspect
from pathlib import Path

import pandas as pd
import pytest

import plantilla_agentes_movilidad as ag


def percepcion(hora: int, presion: float, **extra) -> dict:
    """Arma una percepcion coherente con la presion pedida."""
    capacidad = 20
    base = {
        "zona_id": 161,
        "zona": "Midtown Center",
        "hora": hora,
        "taxis_x": capacidad,
        "demanda_x": presion * capacidad,
        "capacidad_x": capacidad,
        "presion": presion,
    }
    base.update(extra)
    return base


# --------------------------------------------------------------------------
# Casos obligatorios
# --------------------------------------------------------------------------


def test_presion_baja_ambos_no_refuerzan():
    p = percepcion(6, 0.40)

    accion_simple, _ = ag.decidir_reactivo_simple(p)
    estado = ag.actualizar_estado(ag.crear_estado_inicial(), p)
    accion_modelo, _ = ag.decidir_reactivo_modelo(estado)

    assert accion_simple == "NO_REFORZAR"
    assert accion_modelo == "NO_REFORZAR"
    assert estado["racha_presion_alta"] == 0


def test_primera_hora_presion_alta_solo_el_simple_recomienda():
    p = percepcion(7, 0.95)

    accion_simple, _ = ag.decidir_reactivo_simple(p)
    estado = ag.actualizar_estado(ag.crear_estado_inicial(), p)
    accion_modelo, _ = ag.decidir_reactivo_modelo(estado)

    assert accion_simple == "RECOMENDAR_REFUERZO"
    assert accion_modelo == "NO_REFORZAR"
    assert estado["racha_presion_alta"] == 1


def test_segunda_hora_consecutiva_alta_ambos_recomiendan():
    estado = ag.crear_estado_inicial()
    estado = ag.actualizar_estado(estado, percepcion(7, 0.95))
    p2 = percepcion(8, 1.20)
    estado = ag.actualizar_estado(estado, p2)

    accion_simple, _ = ag.decidir_reactivo_simple(p2)
    accion_modelo, _ = ag.decidir_reactivo_modelo(estado)

    assert accion_simple == "RECOMENDAR_REFUERZO"
    assert accion_modelo == "RECOMENDAR_REFUERZO"
    assert estado["racha_presion_alta"] == 2


# --------------------------------------------------------------------------
# Prueba decisiva: misma percepcion final, historias distintas
# --------------------------------------------------------------------------


def test_misma_percepcion_final_historias_distintas():
    """El simple no distingue historias; el basado en modelo si."""
    final = percepcion(9, 0.90)

    # Historia A: la hora previa ya venia con presion alta.
    estado_a = ag.actualizar_estado(ag.crear_estado_inicial(), percepcion(8, 0.95))
    estado_a = ag.actualizar_estado(estado_a, final)
    accion_a, _ = ag.decidir_reactivo_modelo(estado_a)

    # Historia B: la hora previa estuvo tranquila.
    estado_b = ag.actualizar_estado(ag.crear_estado_inicial(), percepcion(8, 0.30))
    estado_b = ag.actualizar_estado(estado_b, final)
    accion_b, _ = ag.decidir_reactivo_modelo(estado_b)

    # El agente simple ve exactamente lo mismo en los dos casos.
    accion_simple_a, motivo_simple_a = ag.decidir_reactivo_simple(final)
    accion_simple_b, motivo_simple_b = ag.decidir_reactivo_simple(final)
    assert (accion_simple_a, motivo_simple_a) == (accion_simple_b, motivo_simple_b)
    assert accion_simple_a == "RECOMENDAR_REFUERZO"

    # El basado en modelo difiere porque su estado anterior es distinto.
    assert accion_a == "RECOMENDAR_REFUERZO"
    assert accion_b == "NO_REFORZAR"
    assert accion_a != accion_b


# --------------------------------------------------------------------------
# Ausencia de fuga temporal (nada de h+1)
# --------------------------------------------------------------------------


def test_las_decisiones_ignoran_columnas_de_h_mas_1():
    """Inyectar datos de h+1 no cambia ninguna decision."""
    limpia = percepcion(8, 0.50)
    contaminada = percepcion(
        8,
        0.50,
        necesita_refuerzo=True,
        taxis_adicionales_sugeridos=60,
        presion_h_mas_1=4.0,
    )

    assert ag.decidir_reactivo_simple(limpia) == ag.decidir_reactivo_simple(contaminada)

    estado_limpio = ag.actualizar_estado(ag.crear_estado_inicial(), limpia)
    estado_contaminado = ag.actualizar_estado(ag.crear_estado_inicial(), contaminada)
    assert estado_limpio == estado_contaminado
    assert ag.decidir_reactivo_modelo(estado_limpio)[0] == "NO_REFORZAR"


def test_el_codigo_no_menciona_campos_de_evaluacion_futura():
    """Ninguna funcion de decision nombra columnas de h+1."""
    for funcion in (
        ag.decidir_reactivo_simple,
        ag.actualizar_estado,
        ag.decidir_reactivo_modelo,
        ag._numero,
    ):
        fuente = inspect.getsource(funcion)
        for prohibido in ag.CAMPOS_PROHIBIDOS + ("h_mas_1", "resultado_h"):
            assert prohibido not in fuente, f"{funcion.__name__} usa {prohibido}"


def test_percepciones_csv_no_trae_columnas_de_h_mas_1():
    ruta = Path(__file__).parent / "escenario_agente" / "percepciones.csv"
    if not ruta.exists():
        pytest.skip("Escenario no generado.")
    columnas = set(pd.read_csv(ruta).columns)
    assert not columnas.intersection(ag.CAMPOS_PROHIBIDOS)


def test_el_estado_solo_depende_de_horas_ya_observadas():
    """Procesar la secuencia truncada da el mismo prefijo que la completa."""
    filas = [percepcion(6, 0.95), percepcion(7, 0.95), percepcion(8, 0.20)]
    completa = ag.procesar_secuencia(pd.DataFrame(filas))
    truncada = ag.procesar_secuencia(pd.DataFrame(filas[:2]))

    pd.testing.assert_frame_equal(completa.head(2), truncada)

