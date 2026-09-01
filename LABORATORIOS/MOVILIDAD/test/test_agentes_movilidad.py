"""Pruebas unitarias para los agentes de movilidad."""

import unittest
import sys
import os

# Agregar la carpeta principal para que encuentre la plantilla
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plantilla_agentes_movilidad import (
    decidir_reactivo_simple,
    crear_estado_inicial,
    actualizar_estado,
    decidir_reactivo_modelo,
    UMBRAL_PRESION,
)

class TestAgentesMovilidad(unittest.TestCase):

    def setUp(self):
        # Datos de prueba básicos
        self.percepcion_baja = {"presion": 0.5, "capacidad_x": 10, "hora": 8}
        self.percepcion_alta = {"presion": 0.9, "capacidad_x": 10, "hora": 9}
        self.percepcion_invalida = {"presion": None, "capacidad_x": 10, "hora": 10}

    def test_presion_baja(self):
        """Caso 1: Presión baja. Ambos agentes devuelven NO_REFORZAR."""
        # Agente simple
        accion_simple, _ = decidir_reactivo_simple(self.percepcion_baja)
        self.assertEqual(accion_simple, "NO_REFORZAR")

        # Agente basado en modelo
        estado = crear_estado_inicial()
        estado = actualizar_estado(estado, self.percepcion_baja)
        accion_modelo, _ = decidir_reactivo_modelo(estado)
        self.assertEqual(accion_modelo, "NO_REFORZAR")

    def test_primera_hora_presion_alta(self):
        """Caso 2: Primera hora con presión alta. El simple recomienda, el modelo no."""
        # Agente simple
        accion_simple, _ = decidir_reactivo_simple(self.percepcion_alta)
        self.assertEqual(accion_simple, "RECOMENDAR_REFUERZO")

        # Agente basado en modelo
        estado = crear_estado_inicial()
        estado = actualizar_estado(estado, self.percepcion_alta)
        accion_modelo, _ = decidir_reactivo_modelo(estado)
        self.assertEqual(accion_modelo, "NO_REFORZAR")
        self.assertEqual(estado["racha_presion_alta"], 1)

    def test_segunda_hora_presion_alta(self):
        """Caso 3: Segunda hora consecutiva con presión alta. Ambos recomiendan."""
        # Agente basado en modelo (simulamos que ya pasó una hora alta)
        estado = crear_estado_inicial()
        estado = actualizar_estado(estado, self.percepcion_alta) # Hora 1
        estado = actualizar_estado(estado, self.percepcion_alta) # Hora 2
        
        accion_modelo, _ = decidir_reactivo_modelo(estado)
        self.assertEqual(accion_modelo, "RECOMENDAR_REFUERZO")
        self.assertEqual(estado["racha_presion_alta"], 2)

    def test_historias_distintas_misma_percepcion(self):
        """Prueba decisiva: Dos historias distintas que terminan en la misma percepción alta."""
        # Historia A: Venimos de presión baja, y ahora hay alta.
        estado_a = crear_estado_inicial()
        estado_a = actualizar_estado(estado_a, self.percepcion_baja)
        estado_a = actualizar_estado(estado_a, self.percepcion_alta) # Percepción final
        
        # Historia B: Venimos de presión alta, y ahora hay alta.
        estado_b = crear_estado_inicial()
        estado_b = actualizar_estado(estado_b, self.percepcion_alta)
        estado_b = actualizar_estado(estado_b, self.percepcion_alta) # Percepción final

        # Para el agente simple, la decisión es idéntica en ambos casos porque solo mira el presente
        accion_simple_a, _ = decidir_reactivo_simple(self.percepcion_alta)
        accion_simple_b, _ = decidir_reactivo_simple(self.percepcion_alta)
        self.assertEqual(accion_simple_a, accion_simple_b)
        self.assertEqual(accion_simple_a, "RECOMENDAR_REFUERZO")

        # Para el agente modelo, las decisiones difieren debido a la historia
        accion_modelo_a, _ = decidir_reactivo_modelo(estado_a)
        accion_modelo_b, _ = decidir_reactivo_modelo(estado_b)
        
        self.assertEqual(accion_modelo_a, "NO_REFORZAR") # Racha de 1
        self.assertEqual(accion_modelo_b, "RECOMENDAR_REFUERZO") # Racha de 2
        
        # Comprobamos que son acciones distintas a pesar de tener la misma percepción actual
        self.assertNotEqual(accion_modelo_a, accion_modelo_b)

    def test_datos_futuros_no_consultados(self):
        """Comprueba que no se accede a datos de h+1."""
        # Si la percepción no tiene datos futuros (como h+1), la función no debería quejarse y trabajar normalmente
        try:
            decidir_reactivo_simple(self.percepcion_alta)
        except KeyError as e:
            self.fail(f"La función simple intentó acceder a una llave no permitida: {e}")

if __name__ == "__main__":
    unittest.main()
