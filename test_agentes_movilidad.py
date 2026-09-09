
import inspect
import unittest

from agentes_movilidad import (
    actualizar_estado,
    crear_estado_inicial,
    decidir_reactivo_modelo,
    decidir_reactivo_simple,
)


def crear_percepcion(presion, hora=8, capacidad_x=20):
    """Crea una percepción mínima válida para las pruebas."""
    return {
        "hora": hora,
        "presion": presion,
        "capacidad_x": capacidad_x,
    }


class TestAgentesMovilidad(unittest.TestCase):

    def test_presion_baja(self):
        """Con presión baja, ambos agentes deben decir NO_REFORZAR."""

        percepcion = crear_percepcion(0.50)
        estado = actualizar_estado(crear_estado_inicial(), percepcion)

        accion_simple, _ = decidir_reactivo_simple(percepcion)
        accion_modelo, _ = decidir_reactivo_modelo(estado)

        self.assertEqual(accion_simple, "NO_REFORZAR")
        self.assertEqual(accion_modelo, "NO_REFORZAR")


    def test_primera_hora_presion_alta(self):
        """En la primera hora alta solo recomienda el agente simple."""

        percepcion = crear_percepcion(0.90)
        estado = actualizar_estado(crear_estado_inicial(), percepcion)

        accion_simple, _ = decidir_reactivo_simple(percepcion)
        accion_modelo, _ = decidir_reactivo_modelo(estado)

        self.assertEqual(accion_simple, "RECOMENDAR_REFUERZO")
        self.assertEqual(accion_modelo, "NO_REFORZAR")
        self.assertEqual(estado["racha_presion_alta"], 1)


    def test_segunda_hora_consecutiva_alta(self):
        """Después de dos horas altas, ambos recomiendan refuerzo."""

        estado = crear_estado_inicial()

        estado = actualizar_estado(
            estado,
            crear_percepcion(0.90, hora=7),
        )

        estado = actualizar_estado(
            estado,
            crear_percepcion(1.10, hora=8),
        )

        accion_simple, _ = decidir_reactivo_simple(
            crear_percepcion(1.10, hora=8)
        )
        accion_modelo, _ = decidir_reactivo_modelo(estado)

        self.assertEqual(accion_simple, "RECOMENDAR_REFUERZO")
        self.assertEqual(accion_modelo, "RECOMENDAR_REFUERZO")
        self.assertEqual(estado["racha_presion_alta"], 2)


    def test_dos_historias_misma_percepcion_final(self):
        """
        La percepción final es idéntica, pero la historia anterior cambia
        la decisión del agente basado en modelo.
        """

        percepcion_final = crear_percepcion(0.90, hora=8)

        # Historia A: presión baja y luego presión alta.
        estado_a = crear_estado_inicial()
        estado_a = actualizar_estado(
            estado_a,
            crear_percepcion(0.40, hora=7),
        )
        estado_a = actualizar_estado(estado_a, percepcion_final)

        # Historia B: presión alta y luego presión alta.
        estado_b = crear_estado_inicial()
        estado_b = actualizar_estado(
            estado_b,
            crear_percepcion(0.95, hora=7),
        )
        estado_b = actualizar_estado(estado_b, percepcion_final)

        accion_simple_a, _ = decidir_reactivo_simple(percepcion_final)
        accion_simple_b, _ = decidir_reactivo_simple(percepcion_final)

        accion_modelo_a, _ = decidir_reactivo_modelo(estado_a)
        accion_modelo_b, _ = decidir_reactivo_modelo(estado_b)

        # El agente simple da la misma respuesta.
        self.assertEqual(accion_simple_a, accion_simple_b)
        self.assertEqual(accion_simple_a, "RECOMENDAR_REFUERZO")

        # El agente basado en modelo responde distinto por su memoria.
        self.assertEqual(accion_modelo_a, "NO_REFORZAR")
        self.assertEqual(accion_modelo_b, "RECOMENDAR_REFUERZO")


    def test_percepcion_invalida(self):
        """Los datos inválidos deben producir ABSTENERSE."""

        percepcion = {
            "hora": 8,
            "presion": None,
            "capacidad_x": 20,
        }

        estado = actualizar_estado(crear_estado_inicial(), percepcion)

        accion_simple, _ = decidir_reactivo_simple(percepcion)
        accion_modelo, _ = decidir_reactivo_modelo(estado)

        self.assertEqual(accion_simple, "ABSTENERSE")
        self.assertEqual(accion_modelo, "ABSTENERSE")


    def test_capacidad_desconocida(self):
        """Si no está la capacidad, el agente debe abstenerse."""

        percepcion = {
            "hora": 8,
            "presion": 0.90,
        }

        estado = actualizar_estado(crear_estado_inicial(), percepcion)

        accion_simple, _ = decidir_reactivo_simple(percepcion)
        accion_modelo, _ = decidir_reactivo_modelo(estado)

        self.assertEqual(accion_simple, "ABSTENERSE")
        self.assertEqual(accion_modelo, "ABSTENERSE")


    def test_funciones_no_reciben_datos_futuros(self):
        """Comprueba que las decisiones no reciben información de h+1."""

        parametros_simple = list(
            inspect.signature(decidir_reactivo_simple).parameters
        )

        parametros_modelo = list(
            inspect.signature(decidir_reactivo_modelo).parameters
        )

        self.assertEqual(parametros_simple, ["percepcion"])
        self.assertEqual(parametros_modelo, ["estado_actual"])


if __name__ == "__main__":
    unittest.main()
