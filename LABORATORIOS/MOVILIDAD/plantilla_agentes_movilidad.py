"""Agentes reactivos para el refuerzo de taxis de la empresa X.

Contiene un agente reactivo simple (usa solo la percepcion actual) y un agente
reactivo basado en modelo (mantiene un resumen de la historia observada).
Ninguna funcion de decision consulta datos de h+1.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

import pandas as pd


ACCIONES = {"NO_REFORZAR", "RECOMENDAR_REFUERZO", "ABSTENERSE"}
UMBRAL_PRESION = 0.85

# Campos que la regla condicion-accion necesita para decidir.
CAMPOS_REQUERIDOS = ("demanda_x", "capacidad_x", "presion")

# Campos que pertenecen a la evaluacion posterior (h+1) y nunca deben leerse.
CAMPOS_PROHIBIDOS = ("necesita_refuerzo", "taxis_adicionales_sugeridos")


def _numero(percepcion: dict[str, Any], campo: str) -> float | None:
    """Devuelve el campo como float o None si falta o no es numerico."""
    if campo not in percepcion:
        return None
    valor = percepcion[campo]
    if isinstance(valor, (bool, str)):
        return None
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return None
    if math.isnan(numero) or math.isinf(numero):
        return None
    return numero


def decidir_reactivo_simple(percepcion: dict[str, Any]) -> tuple[str, str]:
    """Devuelve (accion, motivo) usando solo la percepcion actual."""
    if not isinstance(percepcion, dict):
        return "ABSTENERSE", "La percepcion no es un registro valido."

    valores = {campo: _numero(percepcion, campo) for campo in CAMPOS_REQUERIDOS}
    invalidos = [campo for campo, valor in valores.items() if valor is None]
    if invalidos:
        return (
            "ABSTENERSE",
            f"Faltan datos requeridos o son invalidos: {', '.join(invalidos)}.",
        )

    if valores["demanda_x"] < 0 or valores["presion"] < 0:
        return "ABSTENERSE", "La percepcion contiene valores negativos."

    if valores["capacidad_x"] <= 0:
        return "ABSTENERSE", "La capacidad de X es desconocida o nula."

    presion = valores["presion"]
    if presion >= UMBRAL_PRESION:
        return (
            "RECOMENDAR_REFUERZO",
            f"presion={presion:.2f} >= umbral={UMBRAL_PRESION}",
        )
    return "NO_REFORZAR", f"presion={presion:.2f} < umbral={UMBRAL_PRESION}"


def crear_estado_inicial() -> dict[str, Any]:
    """Crea el estado persistente del agente reactivo basado en modelo."""
    return {
        "percepcion_valida": False,
        "racha_presion_alta": 0,
        "presion_anterior": None,
        "ultima_accion": None,
    }


def actualizar_estado(
    estado_anterior: dict[str, Any],
    percepcion: dict[str, Any],
) -> dict[str, Any]:
    """Actualiza la memoria a partir del estado anterior y la percepcion."""
    #si la percepcion no es valida resetea todo
    if not isinstance(percepcion, dict): 
        return {
            "percepcion_valida": False,
            "racha_presion_alta": 0,
            "presion_anterior": None,
            "ultima_accion": estado_anterior.get("ultima_accion"),
        }
    #valida los cmapos requeridos y sus valores
    valores = {campo: _numero(percepcion, campo) for campo in CAMPOS_REQUERIDOS}
    invalidos = [campo for campo, valor in valores.items() if valor is None]
    datos_invalidos = (
        bool(invalidos)
        or valores["demanda_x"] < 0
        or valores["presion"] < 0
        or valores["capacidad_x"] <= 0
    )
    #tamb, si datos estan mal entonces racha en 0 (resetear)
    if datos_invalidos:
        return {
            "percepcion_valida": False,
            "racha_presion_alta": 0,
            "presion_anterior": None,
            "ultima_accion": estado_anterior.get("ultima_accion"),
        }
    
    #aca es donde actualizo la racha:si la presion de esa hora es alta suma 1 a la racha q traia. si es baja vuelve a 0
    presion = valores["presion"]
    racha_anterior = estado_anterior.get("racha_presion_alta", 0)
    racha_nueva = racha_anterior + 1 if presion >= UMBRAL_PRESION else 0
    #devuelve el diccionario nuevo del estado c la racha updateada
    return {
        "percepcion_valida": True,
        "racha_presion_alta": racha_nueva,
        "presion_anterior": presion,
        "ultima_accion": estado_anterior.get("ultima_accion"),
    }


def decidir_reactivo_modelo(
    #no mira la percecpion directamente sino el estado (la memoria) en las 3 posibilidades
    estado_actual: dict[str, Any],
) -> tuple[str, str]:
    #estado intvalido -> abstenerse
    """Devuelve (accion, motivo) a partir del estado interno actualizado."""
    if not estado_actual.get("percepcion_valida", False):
        return "ABSTENERSE", "Estado invalido: la ultima percepcion no es confiable."
    #si la racha es 2 o + (o sea 2+ hs seguidas de presion alta)->refuerzo
    racha = estado_actual.get("racha_presion_alta", 0)
    if racha >= 2:
        return (
            "RECOMENDAR_REFUERZO",
            f"racha_presion_alta={racha} (2 o mas horas consecutivas con presion alta).",
        )
        #y si no, entonces refuerza
    return "NO_REFORZAR", f"racha_presion_alta={racha} (aun no persiste la presion alta)."


def procesar_secuencia(percepciones: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta ambos agentes y construye la bitacora comparativa."""
    ordenadas = percepciones.sort_values("hora").reset_index(drop=True) #ordena las filas x hora
    estado = crear_estado_inicial() #arranca c estado inicial vacio
    filas: list[dict[str, Any]] = [] #lista p ir guardadno resultados de cada hora

    #este se va a repetir por cada hora que haya
    for _, fila in ordenadas.iterrows():
        percepcion = fila.to_dict() #lo convierte a un diccionario

        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion) #pasa al agente 1
        estado = actualizar_estado(estado, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado) #pasa el estado al agente 2
        estado["ultima_accion"] = accion_modelo #guarda lo que decidio
        #tuarda en la lista un diccionario c todo lo d esa hora
        filas.append(
            {
                "hora": percepcion.get("hora"),
                "presion": percepcion.get("presion"),
                "racha_presion_alta": estado["racha_presion_alta"],
                "accion_simple": accion_simple,
                "motivo_simple": motivo_simple,
                "accion_modelo": accion_modelo,
                "motivo_modelo": motivo_modelo,
            }
        )

    return pd.DataFrame(filas)


def cargar_percepciones(ruta: Path) -> pd.DataFrame:
    """Lee percepciones.csv y rechaza cualquier columna de evaluacion futura."""
    datos = pd.read_csv(ruta)
    prohibidas = [c for c in CAMPOS_PROHIBIDOS if c in datos.columns]
    if prohibidas:
        raise ValueError(
            "percepciones.csv contiene columnas de h+1: " + ", ".join(prohibidas)
        )
    return datos


def main() -> None:
    """Ejecuta los agentes sobre el escenario y guarda la bitacora."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--percepciones",
        type=Path,
        default=Path(__file__).parent / "escenario_agente" / "percepciones.csv",
        help="Ruta a percepciones.csv (solo informacion hasta h).",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=Path(__file__).parent / "bitacora_agentes.csv",
        help="Ruta del CSV de bitacora comparativa.",
    )
    args = parser.parse_args()

    percepciones = cargar_percepciones(args.percepciones)
    bitacora = procesar_secuencia(percepciones)
    bitacora.to_csv(args.salida, index=False)
    print(bitacora.to_string(index=False))
    print(f"\nBitacora escrita en: {args.salida}")


if __name__ == "__main__":
    main()