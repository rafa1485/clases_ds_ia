"""Pruebas unitarias para agentes de movilidad.

Valida el comportamiento del agente reactivo simple, el agente basado en modelo,
la persistencia del estado interno, la causalidad temporal y la prueba decisiva.
"""

from __future__ import annotations

import unittest
import pandas as pd
import numpy as np

from agentes_movilidad import (
    validar_percepcion,
    decidir_reactivo_simple,
    crear_estado_inicial,
    actualizar_estado,
    decidir_reactivo_modelo,
    procesar_secuencia,
)


class TestAgentesMovilidad(unittest.TestCase):

    def test_presion_baja(self):
        """Caso 1: Presión baja -> Ambos agentes devuelven NO_REFORZAR."""
        percepcion = {"hora": 8, "presion": 0.50, "capacidad_x": 20}
        
        # Agente reactivo simple
        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)
        self.assertEqual(accion_simple, "NO_REFORZAR")
        self.assertIn("< 0.85", motivo_simple)

        # Agente basado en modelo (estado inicial)
        estado = crear_estado_inicial()
        estado = actualizar_estado(estado, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)
        self.assertEqual(accion_modelo, "NO_REFORZAR")
        self.assertEqual(estado["racha_presion_alta"], 0)

    def test_primera_hora_presion_alta(self):
        """Caso 2: Primera hora con presión alta -> Simple: RECOMENDAR_REFUERZO, Modelo: NO_REFORZAR."""
        percepcion = {"hora": 8, "presion": 0.90, "capacidad_x": 20}
        
        # Agente reactivo simple
        accion_simple, motivo_simple = decidir_reactivo_simple(percepcion)
        self.assertEqual(accion_simple, "RECOMENDAR_REFUERZO")
        self.assertIn(">= 0.85", motivo_simple)

        # Agente basado en modelo (primera hora alta, racha = 1)
        estado = crear_estado_inicial()
        estado = actualizar_estado(estado, percepcion)
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)
        self.assertEqual(accion_modelo, "NO_REFORZAR")
        self.assertEqual(estado["racha_presion_alta"], 1)

    def test_segunda_hora_consecutiva_presion_alta(self):
        """Caso 3: Segunda hora consecutiva con presión alta -> Ambos recomiendan refuerzo."""
        percepcion_h1 = {"hora": 7, "presion": 0.90, "capacidad_x": 20}
        percepcion_h2 = {"hora": 8, "presion": 0.95, "capacidad_x": 20}

        # Agente simple en h2
        accion_simple, _ = decidir_reactivo_simple(percepcion_h2)
        self.assertEqual(accion_simple, "RECOMENDAR_REFUERZO")

        # Agente basado en modelo tras dos horas consecutivas de presión alta
        estado = crear_estado_inicial()
        estado = actualizar_estado(estado, percepcion_h1)
        self.assertEqual(estado["racha_presion_alta"], 1)

        estado = actualizar_estado(estado, percepcion_h2)
        self.assertEqual(estado["racha_presion_alta"], 2)
        
        accion_modelo, motivo_modelo = decidir_reactivo_modelo(estado)
        self.assertEqual(accion_modelo, "RECOMENDAR_REFUERZO")
        self.assertIn("persistente", motivo_modelo.lower())

    def test_prueba_decisiva_dependencia_historica(self):
        """Prueba decisiva: Dos historias distintas que culminan en la MISMA percepción final.

        Historia 1: [h=7: presion=0.40 (baja)] -> [h=8: presion=0.90 (alta)]
        Historia 2: [h=7: presion=0.90 (alta)] -> [h=8: presion=0.90 (alta)]

        El agente reactivo simple produce la MISMA acción en ambas (RECOMENDAR_REFUERZO).
        El agente basado en modelo produce acciones DISTINTAS (NO_REFORZAR vs RECOMENDAR_REFUERZO).
        """
        percepcion_final_identica = {"hora": 8, "presion": 0.90, "capacidad_x": 20}

        # Ejecución Historia 1
        estado_h1 = crear_estado_inicial()
        estado_h1 = actualizar_estado(estado_h1, {"hora": 7, "presion": 0.40, "capacidad_x": 20})
        estado_h1 = actualizar_estado(estado_h1, percepcion_final_identica)
        accion_modelo_h1, _ = decidir_reactivo_modelo(estado_h1)
        accion_simple_h1, _ = decidir_reactivo_simple(percepcion_final_identica)

        # Ejecución Historia 2
        estado_h2 = crear_estado_inicial()
        estado_h2 = actualizar_estado(estado_h2, {"hora": 7, "presion": 0.90, "capacidad_x": 20})
        estado_h2 = actualizar_estado(estado_h2, percepcion_final_identica)
        accion_modelo_h2, _ = decidir_reactivo_modelo(estado_h2)
        accion_simple_h2, _ = decidir_reactivo_simple(percepcion_final_identica)

        # Comprobaciones
        # 1. El agente simple actúa igual en ambos casos porque sólo ve la percepción de h=8
        self.assertEqual(accion_simple_h1, accion_simple_h2)
        self.assertEqual(accion_simple_h1, "RECOMENDAR_REFUERZO")

        # 2. El agente basado en modelo actúa diferente debido a la historia
        self.assertNotEqual(accion_modelo_h1, accion_modelo_h2)
        self.assertEqual(accion_modelo_h1, "NO_REFORZAR")
        self.assertEqual(accion_modelo_h2, "RECOMENDAR_REFUERZO")

    def test_no_fuga_temporal_h_mas_1(self):
        """Comprueba que ninguna función de decisión depende de datos de h+1."""
        percepcion_presente = {
            "hora": 8,
            "presion": 0.70,
            "capacidad_x": 20,
        }
        # Inyectar deliberadamente datos futuros como si viniesen de resultado_h_mas_1.csv
        percepcion_con_futuro = {
            **percepcion_presente,
            "demanda_h_mas_1": 500,
            "presion_h_mas_1": 5.0,
            "resultado_futuro": "CRISIS",
        }

        # La decisión del reactivo simple debe depender exclusivamente de presion actual
        accion1, _ = decidir_reactivo_simple(percepcion_presente)
        accion2, _ = decidir_reactivo_simple(percepcion_con_futuro)
        self.assertEqual(accion1, "NO_REFORZAR")
        self.assertEqual(accion2, "NO_REFORZAR")

        # La decisión del modelo debe basarse únicamente en el estado acumulado hasta h
        estado1 = actualizar_estado(crear_estado_inicial(), percepcion_presente)
        estado2 = actualizar_estado(crear_estado_inicial(), percepcion_con_futuro)
        self.assertEqual(decidir_reactivo_modelo(estado1)[0], "NO_REFORZAR")
        self.assertEqual(decidir_reactivo_modelo(estado2)[0], "NO_REFORZAR")

    def test_validacion_percepciones_invalidas(self):
        """Valida que entradas incompletas o corruptas devuelvan ABSTENERSE."""
        casos_invalidos = [
            {},                                     # Vacío
            {"hora": 8},                            # Sin presión
            {"hora": 8, "presion": None},           # Presión None
            {"hora": 8, "presion": np.nan},         # Presión NaN
            {"hora": 8, "presion": "alta"},         # Presión string
            {"hora": 8, "presion": True},           # Presión booleana
            {"hora": 8, "presion": -0.5},           # Presión negativa
            {"hora": 8, "presion": 0.9, "capacidad_x": 0},   # Capacidad 0
            {"hora": 8, "presion": 0.9, "capacidad_x": -5},  # Capacidad negativa
            None,                                   # No es dict
            "percepcion_string",                    # No es dict
        ]

        for caso in casos_invalidos:
            with self.subTest(caso=caso):
                self.assertFalse(validar_percepcion(caso))
                accion_simple, _ = decidir_reactivo_simple(caso)
                self.assertEqual(accion_simple, "ABSTENERSE")

                estado = actualizar_estado(crear_estado_inicial(), caso)
                accion_modelo, _ = decidir_reactivo_modelo(estado)
                self.assertEqual(accion_modelo, "ABSTENERSE")

    def test_reinicio_de_racha(self):
        """Verifica que una hora con presión baja reinicie la racha a cero."""
        estado = crear_estado_inicial()

        # Hora 1: alta -> racha 1
        estado = actualizar_estado(estado, {"hora": 6, "presion": 0.90})
        self.assertEqual(estado["racha_presion_alta"], 1)
        self.assertEqual(decidir_reactivo_modelo(estado)[0], "NO_REFORZAR")

        # Hora 2: alta -> racha 2 (refuerzo)
        estado = actualizar_estado(estado, {"hora": 7, "presion": 0.95})
        self.assertEqual(estado["racha_presion_alta"], 2)
        self.assertEqual(decidir_reactivo_modelo(estado)[0], "RECOMENDAR_REFUERZO")

        # Hora 3: baja -> racha vuelve a 0
        estado = actualizar_estado(estado, {"hora": 8, "presion": 0.50})
        self.assertEqual(estado["racha_presion_alta"], 0)
        self.assertEqual(decidir_reactivo_modelo(estado)[0], "NO_REFORZAR")

        # Hora 4: alta -> racha es 1 (no refuerza aún)
        estado = actualizar_estado(estado, {"hora": 9, "presion": 0.88})
        self.assertEqual(estado["racha_presion_alta"], 1)
        self.assertEqual(decidir_reactivo_modelo(estado)[0], "NO_REFORZAR")

    def test_procesar_secuencia_completa(self):
        """Verifica la generación de la bitácora comparativa sobre un DataFrame."""
        df_in = pd.DataFrame([
            {"hora": 6, "zona": "Midtown Center", "presion": 0.70, "capacidad_x": 20},
            {"hora": 7, "zona": "Midtown Center", "presion": 0.90, "capacidad_x": 20},
            {"hora": 8, "zona": "Midtown Center", "presion": 0.95, "capacidad_x": 20},
        ])

        bitacora = procesar_secuencia(df_in)

        # Columnas mínimas requeridas por consigna
        columnas_esperadas = [
            "hora",
            "presion",
            "racha_presion_alta",
            "accion_simple",
            "motivo_simple",
            "accion_modelo",
            "motivo_modelo",
        ]
        for col in columnas_esperadas:
            self.assertIn(col, bitacora.columns)

        self.assertEqual(len(bitacora), 3)
        self.assertEqual(list(bitacora["accion_simple"]), ["NO_REFORZAR", "RECOMENDAR_REFUERZO", "RECOMENDAR_REFUERZO"])
        self.assertEqual(list(bitacora["accion_modelo"]), ["NO_REFORZAR", "NO_REFORZAR", "RECOMENDAR_REFUERZO"])
        self.assertEqual(list(bitacora["racha_presion_alta"]), [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
