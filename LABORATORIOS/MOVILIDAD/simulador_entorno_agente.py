#!/usr/bin/env python3
"""Entorno didactico para agentes de refuerzo de taxis.

Reutiliza el simulador de viajes y divide su demanda entre una empresa
ficticia X y un conjunto sintetico de otras empresas. La salida visible llega
hasta la hora h; el resultado de h+1 se guarda por separado para evaluacion.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd

if __package__:
    from .simulador_movilidad import (
        cargar_centros_zonas,
        construir_url_tlc,
        estimar_modelo_demanda,
        simular_viajes,
    )
else:
    from simulador_movilidad import (
        cargar_centros_zonas,
        construir_url_tlc,
        estimar_modelo_demanda,
        simular_viajes,
    )


Q_OTRAS_MIN = 0.15
Q_OTRAS_MAX = 0.75
TAXIS_REFERENCIA = 10.0
SIGMA_OTRAS = 0.05

COLUMNAS_PERCEPCION = [
    "zona_id",
    "zona",
    "hora",
    "taxis_x",
    "demanda_total",
    "tasa_otras_simulada",
    "viajes_otras",
    "demanda_x",
    "capacidad_x",
    "viajes_atendibles_x",
    "demanda_no_cubierta_x",
    "presion",
]


def _validar_entero_no_negativo(valor: int, nombre: str) -> int:
    if isinstance(valor, bool) or not isinstance(valor, (int, np.integer)):
        raise TypeError(f"{nombre} debe ser un entero")
    if valor < 0:
        raise ValueError(f"{nombre} no puede ser negativo")
    return int(valor)


def tasa_otras_esperada(
    taxis_x: int,
    q_min: float = Q_OTRAS_MIN,
    q_max: float = Q_OTRAS_MAX,
    taxis_referencia: float = TAXIS_REFERENCIA,
) -> float:
    """Calcula la cuota base de otras empresas, inversa a la flota de X."""
    taxis_x = _validar_entero_no_negativo(taxis_x, "taxis_x")
    if not 0 <= q_min < q_max <= 1:
        raise ValueError("Se requiere 0 <= q_min < q_max <= 1")
    if taxis_referencia <= 0:
        raise ValueError("taxis_referencia debe ser positiva")

    return q_min + (q_max - q_min) / (1 + taxis_x / taxis_referencia)


def sortear_tasa_otras(
    taxis_x: int,
    generador: np.random.Generator,
    q_min: float = Q_OTRAS_MIN,
    q_max: float = Q_OTRAS_MAX,
    taxis_referencia: float = TAXIS_REFERENCIA,
    sigma: float = SIGMA_OTRAS,
) -> float:
    """Agrega ruido normal a la cuota base y la mantiene entre sus limites."""
    if sigma < 0:
        raise ValueError("sigma no puede ser negativa")
    base = tasa_otras_esperada(taxis_x, q_min, q_max, taxis_referencia)
    return float(np.clip(base + generador.normal(0, sigma), q_min, q_max))


def construir_percepcion(
    viajes_simulados: pd.DataFrame,
    centros: pd.DataFrame,
    zona_id: int,
    hora: int,
    taxis_x: int,
    generador: np.random.Generator,
    viajes_por_taxi: int = 1,
) -> dict[str, object]:
    """Resume una hora simulada como percepcion de una zona para el agente."""
    zona_id = _validar_entero_no_negativo(zona_id, "zona_id")
    hora = _validar_entero_no_negativo(hora, "hora")
    taxis_x = _validar_entero_no_negativo(taxis_x, "taxis_x")
    viajes_por_taxi = _validar_entero_no_negativo(
        viajes_por_taxi, "viajes_por_taxi"
    )
    if viajes_por_taxi == 0:
        raise ValueError("viajes_por_taxi debe ser mayor que cero")
    if not 0 <= hora <= 23:
        raise ValueError("hora debe estar entre 0 y 23")
    if "PULocationID" not in viajes_simulados:
        raise ValueError("Los viajes simulados no contienen PULocationID")

    zonas = centros.loc[centros["LocationID"].eq(zona_id), "zona"]
    if zonas.empty:
        raise ValueError(f"No existe geometria para la zona {zona_id}")

    demanda_total = int(viajes_simulados["PULocationID"].eq(zona_id).sum())
    tasa_otras = sortear_tasa_otras(taxis_x, generador)
    viajes_otras = int(generador.binomial(demanda_total, tasa_otras))
    demanda_x = demanda_total - viajes_otras
    capacidad_x = taxis_x * viajes_por_taxi
    viajes_atendibles = min(demanda_x, capacidad_x)
    demanda_no_cubierta = demanda_x - viajes_atendibles
    if capacidad_x:
        presion = demanda_x / capacidad_x
    else:
        presion = float("inf") if demanda_x else 0.0

    return {
        "zona_id": zona_id,
        "zona": str(zonas.iloc[0]),
        "hora": hora,
        "taxis_x": taxis_x,
        "demanda_total": demanda_total,
        "tasa_otras_simulada": tasa_otras,
        "viajes_otras": viajes_otras,
        "demanda_x": demanda_x,
        "capacidad_x": capacidad_x,
        "viajes_atendibles_x": viajes_atendibles,
        "demanda_no_cubierta_x": demanda_no_cubierta,
        "presion": presion,
    }


def simular_escenario(
    viajes_historicos: pd.DataFrame,
    centros: pd.DataFrame,
    zona_id: int,
    hora_decision: int,
    taxis_x: int,
    anio: int,
    mes: int,
    horas_historia: int = 3,
    viajes_por_taxi: int = 1,
    semilla: int | None = None,
) -> pd.DataFrame:
    """Simula la historia visible y una hora futura reservada para evaluar."""
    zona_id = _validar_entero_no_negativo(zona_id, "zona_id")
    hora_decision = _validar_entero_no_negativo(hora_decision, "hora_decision")
    taxis_x = _validar_entero_no_negativo(taxis_x, "taxis_x")
    horas_historia = _validar_entero_no_negativo(
        horas_historia, "horas_historia"
    )
    if horas_historia == 0:
        raise ValueError("horas_historia debe ser mayor que cero")
    if not 0 <= hora_decision <= 22:
        raise ValueError("hora_decision debe estar entre 0 y 22")
    if horas_historia > hora_decision + 1:
        raise ValueError(
            "horas_historia no puede retroceder antes del comienzo del lunes"
        )

    generador = np.random.default_rng(semilla)
    hora_inicial = hora_decision - horas_historia + 1
    percepciones = []
    for hora in range(hora_inicial, hora_decision + 2):
        tasa, distribucion_od = estimar_modelo_demanda(
            viajes_historicos, centros, hora, anio, mes
        )
        semilla_viajes = int(
            generador.integers(0, np.iinfo(np.int64).max, dtype=np.int64)
        )
        viajes_simulados = simular_viajes(
            tasa,
            distribucion_od,
            centros,
            hora,
            semilla=semilla_viajes,
        )
        percepciones.append(
            construir_percepcion(
                viajes_simulados,
                centros,
                zona_id,
                hora,
                taxis_x,
                generador,
                viajes_por_taxi,
            )
        )

    return pd.DataFrame(percepciones, columns=COLUMNAS_PERCEPCION)


def separar_escenario(
    escenario: pd.DataFrame,
    hora_decision: int,
    viajes_por_taxi: int = 1,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa percepciones permitidas y resultado futuro de evaluacion."""
    viajes_por_taxi = _validar_entero_no_negativo(
        viajes_por_taxi, "viajes_por_taxi"
    )
    if viajes_por_taxi == 0:
        raise ValueError("viajes_por_taxi debe ser mayor que cero")
    visible = escenario.loc[escenario["hora"].le(hora_decision)].copy()
    futuro = escenario.loc[escenario["hora"].eq(hora_decision + 1)].copy()
    if futuro.empty:
        raise ValueError("El escenario no contiene la hora h+1")

    futuro["necesita_refuerzo"] = futuro["demanda_x"].gt(futuro["capacidad_x"])
    futuro["taxis_adicionales_sugeridos"] = futuro[
        "demanda_no_cubierta_x"
    ].map(lambda faltante: math.ceil(faltante / viajes_por_taxi))
    return visible.reset_index(drop=True), futuro.reset_index(drop=True)


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Genera percepciones para un agente didactico de taxis."
    )
    parser.add_argument("--zona", type=int, required=True, help="LocationID de TLC")
    parser.add_argument(
        "--hora", type=int, required=True, help="Hora h de decision, entre 0 y 22"
    )
    parser.add_argument(
        "--taxis-x", type=int, required=True, help="Taxis de la empresa X en la zona"
    )
    parser.add_argument("--anio", type=int, default=2024)
    parser.add_argument("--mes", type=int, default=1)
    parser.add_argument("--horas-historia", type=int, default=3)
    parser.add_argument("--viajes-por-taxi", type=int, default=1)
    parser.add_argument("--semilla", type=int)
    parser.add_argument("--datos", help="Parquet local o URL de viajes TLC")
    parser.add_argument(
        "--salida-dir",
        type=Path,
        default=Path("escenario_agente"),
        help="Directorio para percepciones.csv y resultado_h_mas_1.csv",
    )
    return parser


def main() -> None:
    args = crear_parser().parse_args()
    if not 1 <= args.mes <= 12:
        raise SystemExit("El mes debe estar entre 1 y 12")

    fuente = args.datos or construir_url_tlc(args.anio, args.mes)
    print(f"Cargando viajes desde {fuente}...")
    viajes = pd.read_parquet(
        fuente,
        columns=["tpep_pickup_datetime", "PULocationID", "DOLocationID"],
    )
    print("Cargando geometrías de zonas TLC...")
    centros = cargar_centros_zonas()
    print("Simulando historia y resultado futuro...")
    escenario = simular_escenario(
        viajes,
        centros,
        args.zona,
        args.hora,
        args.taxis_x,
        args.anio,
        args.mes,
        args.horas_historia,
        args.viajes_por_taxi,
        args.semilla,
    )
    visible, futuro = separar_escenario(
        escenario, args.hora, args.viajes_por_taxi
    )

    args.salida_dir.mkdir(parents=True, exist_ok=True)
    ruta_visible = args.salida_dir / "percepciones.csv"
    ruta_futuro = args.salida_dir / "resultado_h_mas_1.csv"
    visible.to_csv(ruta_visible, index=False)
    futuro.to_csv(ruta_futuro, index=False)

    print(visible.to_string(index=False))
    print(f"Percepciones guardadas en {ruta_visible.resolve()}")
    print(f"Evaluación futura guardada en {ruta_futuro.resolve()}")


if __name__ == "__main__":
    main()
