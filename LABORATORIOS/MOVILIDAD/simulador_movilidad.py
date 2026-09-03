#!/usr/bin/env python3
"""Simulador de viajes Yellow Taxi para un lunes y una hora dada.

La demanda simulada representa pickups realizados y reportados por TLC. No
representa solicitudes no atendidas ni la demanda total de movilidad.
"""

from __future__ import annotations

import argparse
import calendar
import tempfile
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd


ZONAS_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip"
COLUMNAS_SALIDA = [
    "viaje_id",
    "dia_semana",
    "hora",
    "minuto",
    "PULocationID",
    "zona_pickup",
    "latitud_pickup",
    "longitud_pickup",
    "DOLocationID",
    "zona_dropoff",
    "latitud_dropoff",
    "longitud_dropoff",
    "distancia_centros_km",
]


def construir_url_tlc(anio: int, mes: int) -> str:
    """Construye la URL del parquet mensual de Yellow Taxi."""
    return (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/"
        f"yellow_tripdata_{anio}-{mes:02d}.parquet"
    )


def cargar_centros_zonas(zonas_url: str = ZONAS_URL) -> pd.DataFrame:
    """Descarga las zonas TLC y devuelve sus centroides geograficos."""
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise RuntimeError(
            "Se necesita geopandas para leer las zonas TLC. "
            "Instale las dependencias con: pip install -r requirements.txt"
        ) from exc

    with tempfile.NamedTemporaryFile(suffix=".zip") as archivo_zip:
        urllib.request.urlretrieve(zonas_url, archivo_zip.name)
        zonas = gpd.read_file(
            f"zip://{archivo_zip.name}!taxi_zones/taxi_zones.shp"
        )

    if zonas.crs is None:
        raise ValueError("Las geometrías de las zonas TLC no tienen un CRS definido")

    # EPSG:2263 permite calcular el centro sobre un plano adecuado para NYC.
    zonas_proyectadas = zonas.to_crs(epsg=2263)
    centroides = zonas_proyectadas.geometry.centroid.to_crs(epsg=4326)

    return pd.DataFrame(
        {
            "LocationID": pd.to_numeric(zonas["LocationID"], errors="raise").astype(int),
            "zona": zonas["zone"].astype(str),
            "longitud": centroides.x.to_numpy(),
            "latitud": centroides.y.to_numpy(),
        }
    )


def cantidad_lunes(anio: int, mes: int) -> int:
    """Devuelve la cantidad de lunes calendario de un mes."""
    return sum(
        calendar.weekday(anio, mes, dia) == calendar.MONDAY
        for dia in range(1, calendar.monthrange(anio, mes)[1] + 1)
    )


def estimar_modelo_demanda(
    viajes: pd.DataFrame,
    centros: pd.DataFrame,
    hora: int,
    anio: int,
    mes: int,
) -> tuple[float, pd.DataFrame]:
    """Estima la tasa horaria y la distribucion OD conjunta de los lunes."""
    if not 0 <= hora <= 23:
        raise ValueError("La hora debe ser un entero entre 0 y 23")

    columnas_viajes = {
        "tpep_pickup_datetime",
        "PULocationID",
        "DOLocationID",
    }
    faltantes = columnas_viajes.difference(viajes.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas de viajes: {sorted(faltantes)}")

    fechas = pd.to_datetime(viajes["tpep_pickup_datetime"], errors="coerce")
    pickup = pd.to_numeric(viajes["PULocationID"], errors="coerce")
    dropoff = pd.to_numeric(viajes["DOLocationID"], errors="coerce")
    ids_validos = set(pd.to_numeric(centros["LocationID"], errors="coerce").dropna())

    mascara = (
        fechas.notna()
        & (fechas.dt.year == anio)
        & (fechas.dt.month == mes)
        & (fechas.dt.dayofweek == 0)
        & (fechas.dt.hour == hora)
        & pickup.isin(ids_validos)
        & dropoff.isin(ids_validos)
    )
    od = pd.DataFrame(
        {
            "PULocationID": pickup[mascara].astype(int),
            "DOLocationID": dropoff[mascara].astype(int),
        }
    )

    tasa = len(od) / cantidad_lunes(anio, mes)
    frecuencias = (
        od.value_counts(sort=False)
        .rename("frecuencia")
        .reset_index()
    )
    if not frecuencias.empty:
        frecuencias["probabilidad"] = frecuencias["frecuencia"] / len(od)
    else:
        frecuencias["probabilidad"] = pd.Series(dtype=float)

    return tasa, frecuencias


def distancia_haversine_km(
    latitud_origen: pd.Series | np.ndarray,
    longitud_origen: pd.Series | np.ndarray,
    latitud_destino: pd.Series | np.ndarray,
    longitud_destino: pd.Series | np.ndarray,
) -> np.ndarray:
    """Calcula la distancia de circulo maximo entre pares de coordenadas."""
    lat1 = np.radians(np.asarray(latitud_origen, dtype=float))
    lon1 = np.radians(np.asarray(longitud_origen, dtype=float))
    lat2 = np.radians(np.asarray(latitud_destino, dtype=float))
    lon2 = np.radians(np.asarray(longitud_destino, dtype=float))

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = np.sin(delta_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(
        delta_lon / 2
    ) ** 2
    return 2 * 6371.0088 * np.arcsin(np.sqrt(a))


def simular_viajes(
    tasa: float,
    distribucion_od: pd.DataFrame,
    centros: pd.DataFrame,
    hora: int,
    semilla: int | None = None,
) -> pd.DataFrame:
    """Simula viajes de una hora con demanda Poisson y minutos uniformes."""
    if tasa < 0:
        raise ValueError("La tasa de demanda no puede ser negativa")
    if not 0 <= hora <= 23:
        raise ValueError("La hora debe ser un entero entre 0 y 23")

    generador = np.random.default_rng(semilla)
    cantidad = int(generador.poisson(tasa))
    if cantidad == 0:
        return pd.DataFrame(columns=COLUMNAS_SALIDA)
    if distribucion_od.empty:
        raise ValueError("No hay pares pickup-dropoff para simular los viajes")

    probabilidades = distribucion_od["probabilidad"].to_numpy(dtype=float)
    probabilidades = probabilidades / probabilidades.sum()
    indices = generador.choice(
        len(distribucion_od), size=cantidad, replace=True, p=probabilidades
    )
    muestra = distribucion_od.iloc[indices][
        ["PULocationID", "DOLocationID"]
    ].reset_index(drop=True)
    muestra["minuto"] = generador.integers(0, 60, size=cantidad)

    centros_idx = centros.drop_duplicates("LocationID").set_index("LocationID")
    pickup = centros_idx.loc[muestra["PULocationID"]].reset_index(drop=True)
    dropoff = centros_idx.loc[muestra["DOLocationID"]].reset_index(drop=True)

    resultado = pd.DataFrame(
        {
            "dia_semana": "lunes",
            "hora": hora,
            "minuto": muestra["minuto"],
            "PULocationID": muestra["PULocationID"],
            "zona_pickup": pickup["zona"],
            "latitud_pickup": pickup["latitud"],
            "longitud_pickup": pickup["longitud"],
            "DOLocationID": muestra["DOLocationID"],
            "zona_dropoff": dropoff["zona"],
            "latitud_dropoff": dropoff["latitud"],
            "longitud_dropoff": dropoff["longitud"],
        }
    )
    resultado["distancia_centros_km"] = distancia_haversine_km(
        resultado["latitud_pickup"],
        resultado["longitud_pickup"],
        resultado["latitud_dropoff"],
        resultado["longitud_dropoff"],
    )
    resultado = resultado.sort_values("minuto", kind="stable").reset_index(drop=True)
    resultado.insert(0, "viaje_id", np.arange(1, cantidad + 1))
    return resultado[COLUMNAS_SALIDA]


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simula viajes Yellow Taxi para un lunes y una hora."
    )
    parser.add_argument("--hora", type=int, required=True, help="Hora de 0 a 23")
    parser.add_argument("--anio", type=int, default=2024, help="Año histórico")
    parser.add_argument("--mes", type=int, default=1, help="Mes histórico")
    parser.add_argument(
        "--datos",
        help="Parquet local o URL; por defecto se usa el parquet TLC del año y mes",
    )
    parser.add_argument("--semilla", type=int, help="Semilla aleatoria reproducible")
    parser.add_argument("--salida", type=Path, help="Archivo CSV para los viajes")
    return parser


def main() -> None:
    args = crear_parser().parse_args()
    if not 1 <= args.mes <= 12:
        raise SystemExit("El mes debe ser un entero entre 1 y 12")
    if not 0 <= args.hora <= 23:
        raise SystemExit("La hora debe ser un entero entre 0 y 23")

    fuente = args.datos or construir_url_tlc(args.anio, args.mes)
    print(f"Cargando viajes desde {fuente}...")
    viajes = pd.read_parquet(
        fuente,
        columns=["tpep_pickup_datetime", "PULocationID", "DOLocationID"],
    )
    print("Cargando geometrías de zonas TLC...")
    centros = cargar_centros_zonas()

    tasa, distribucion_od = estimar_modelo_demanda(
        viajes, centros, args.hora, args.anio, args.mes
    )
    simulados = simular_viajes(
        tasa, distribucion_od, centros, args.hora, args.semilla
    )

    print(f"Demanda histórica promedio: {tasa:.2f} viajes por hora.")
    print(f"Viajes simulados: {len(simulados)}.")
    if args.salida:
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        simulados.to_csv(args.salida, index=False)
        print(f"Resultado guardado en {args.salida.resolve()}")
    elif simulados.empty:
        print("No se generaron viajes en esta ejecución.")
    else:
        print(simulados.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
