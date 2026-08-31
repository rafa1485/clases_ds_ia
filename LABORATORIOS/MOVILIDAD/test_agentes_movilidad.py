"""Pruebas de los agentes reactivos de movilidad."""

from __future__ import annotations

import unittest

import pandas as pd

from agentes_movilidad import (
    actualizar_estado,
    crear_estado_inicial,
    decidir_reactivo_modelo,
    decidir_reactivo_simple,
    procesar_secuencia,
)


def percepcion(hora: int, presion: float) -> dict[str, float | int]:
    """Construye una percepcion minima valida para las pruebas."""
    return {"hora": hora, "capacidad_x": 20, "presion": presion}


class PercepcionVigilada(dict):
    """Falla si una funcion intenta consultar el resultado futuro."""

    def get(self, clave, predeterminado=None):
        if clave == "resultado_h_mas_1":
            raise AssertionError("Se intento consultar informacion de h+1")
        return super().get(clave, predeterminado)

    def __getitem__(self, clave):
        if clave == "resultado_h_mas_1":
            raise AssertionError("Se intento consultar informacion de h+1")
        return super().__getitem__(clave)


class TestAgentesMovilidad(unittest.TestCase):
    def test_presion_baja(self):
        actual = percepcion(6, 0.50)
        self.assertEqual(decidir_reactivo_simple(actual)[0], "NO_REFORZAR")

        estado = actualizar_estado(crear_estado_inicial(), actual)
        self.assertEqual(decidir_reactivo_modelo(estado)[0], "NO_REFORZAR")
        self.assertEqual(estado["racha_presion_alta"], 0)

    def test_primera_hora_con_presion_alta(self):
        actual = percepcion(7, 0.85)
        self.assertEqual(
            decidir_reactivo_simple(actual)[0], "RECOMENDAR_REFUERZO"
        )

        estado = actualizar_estado(crear_estado_inicial(), actual)
        self.assertEqual(decidir_reactivo_modelo(estado)[0], "NO_REFORZAR")
        self.assertEqual(estado["racha_presion_alta"], 1)

    def test_segunda_hora_consecutiva_con_presion_alta(self):
        estado = actualizar_estado(crear_estado_inicial(), percepcion(7, 0.90))
        estado = actualizar_estado(estado, percepcion(8, 1.10))

        self.assertEqual(
            decidir_reactivo_simple(percepcion(8, 1.10))[0],
            "RECOMENDAR_REFUERZO",
        )
        self.assertEqual(
            decidir_reactivo_modelo(estado)[0], "RECOMENDAR_REFUERZO"
        )
        self.assertEqual(estado["racha_presion_alta"], 2)

    def test_misma_percepcion_dos_historias_distintas(self):
        percepcion_final = percepcion(8, 0.90)

        estado_tras_baja = actualizar_estado(
            crear_estado_inicial(), percepcion(7, 0.40)
        )
        estado_tras_alta = actualizar_estado(
            crear_estado_inicial(), percepcion(7, 0.95)
        )
        estado_historia_baja = actualizar_estado(
            estado_tras_baja, percepcion_final
        )
        estado_historia_alta = actualizar_estado(
            estado_tras_alta, percepcion_final
        )

        accion_simple_1 = decidir_reactivo_simple(percepcion_final)[0]
        accion_simple_2 = decidir_reactivo_simple(dict(percepcion_final))[0]
        self.assertEqual(accion_simple_1, accion_simple_2)
        self.assertEqual(accion_simple_1, "RECOMENDAR_REFUERZO")
        self.assertEqual(
            decidir_reactivo_modelo(estado_historia_baja)[0], "NO_REFORZAR"
        )
        self.assertEqual(
            decidir_reactivo_modelo(estado_historia_alta)[0],
            "RECOMENDAR_REFUERZO",
        )

    def test_datos_invalidos_producen_abstencion_y_cortan_la_racha(self):
        invalidas = [
            {"capacidad_x": 20},
            {"presion": 0.9},
            {"capacidad_x": 0, "presion": 0.9},
            {"capacidad_x": 20, "presion": float("nan")},
            {"capacidad_x": 20, "presion": -0.1},
        ]
        estado_alto = actualizar_estado(
            crear_estado_inicial(), percepcion(6, 0.90)
        )

        for invalida in invalidas:
            with self.subTest(invalida=invalida):
                self.assertEqual(decidir_reactivo_simple(invalida)[0], "ABSTENERSE")
                estado = actualizar_estado(estado_alto, invalida)
                self.assertEqual(decidir_reactivo_modelo(estado)[0], "ABSTENERSE")
                self.assertEqual(estado["racha_presion_alta"], 0)

    def test_decisiones_no_consultan_h_mas_1(self):
        actual = PercepcionVigilada(
            hora=8,
            capacidad_x=20,
            presion=0.90,
            resultado_h_mas_1="dato_prohibido",
        )
        decidir_reactivo_simple(actual)
        actualizar_estado(crear_estado_inicial(), actual)

    def test_procesar_secuencia_ordena_y_genera_bitacora(self):
        datos = pd.DataFrame(
            [percepcion(8, 0.90), percepcion(6, 0.40), percepcion(7, 0.95)]
        )
        bitacora = procesar_secuencia(datos)

        self.assertEqual(bitacora["hora"].tolist(), [6, 7, 8])
        self.assertEqual(bitacora["racha_presion_alta"].tolist(), [0, 1, 2])
        self.assertEqual(
            bitacora["accion_modelo"].tolist(),
            ["NO_REFORZAR", "NO_REFORZAR", "RECOMENDAR_REFUERZO"],
        )


if __name__ == "__main__":
    unittest.main()
