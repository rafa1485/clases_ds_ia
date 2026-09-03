import unittest

from agentes_movilidad import (
    decidir_reactivo_simple,
    crear_estado_inicial,
    actualizar_estado,
    decidir_reactivo_modelo,
)


class TestAgenteReactivoSimple(unittest.TestCase):

    def test_presion_baja(self):
        percepcion = {
            "capacidad_x": 20,
            "presion": 0.70
        }

        accion, motivo = decidir_reactivo_simple(percepcion)

        self.assertEqual(accion, "NO_REFORZAR")
        self.assertIn("menor", motivo)

    def test_primera_hora_presion_alta(self):
        percepcion = {
            "capacidad_x": 20,
            "presion": 0.90
        }

        accion, motivo = decidir_reactivo_simple(percepcion)

        self.assertEqual(accion, "RECOMENDAR_REFUERZO")
        self.assertIn("mayor o igual", motivo)

    def test_capacidad_desconocida(self):
        percepcion = {
            "capacidad_x": None,
            "presion": 0.90
        }

        accion, motivo = decidir_reactivo_simple(percepcion)

        self.assertEqual(accion, "ABSTENERSE")
        self.assertIn("desconocida", motivo)


class TestAgenteReactivoModelo(unittest.TestCase):

    def test_primera_hora_presion_alta_no_refuerza(self):
        estado = crear_estado_inicial()

        estado = actualizar_estado(
            estado,
            {"capacidad_x": 20, "presion": 0.90}
        )

        accion, motivo = decidir_reactivo_modelo(estado)

        self.assertEqual(accion, "NO_REFORZAR")
        self.assertEqual(estado["racha_presion_alta"], 1)

    def test_segunda_hora_presion_alta_recomienda(self):
        estado = crear_estado_inicial()

        estado = actualizar_estado(
            estado,
            {"capacidad_x": 20, "presion": 0.90}
        )

        estado = actualizar_estado(
            estado,
            {"capacidad_x": 20, "presion": 1.10}
        )

        accion, motivo = decidir_reactivo_modelo(estado)

        self.assertEqual(accion, "RECOMENDAR_REFUERZO")
        self.assertEqual(estado["racha_presion_alta"], 2)

    def test_presion_baja_reinicia_racha(self):
        estado = crear_estado_inicial()

        estado = actualizar_estado(
            estado,
            {"capacidad_x": 20, "presion": 0.90}
        )

        estado = actualizar_estado(
            estado,
            {"capacidad_x": 20, "presion": 0.60}
        )

        accion, motivo = decidir_reactivo_modelo(estado)

        self.assertEqual(accion, "NO_REFORZAR")
        self.assertEqual(estado["racha_presion_alta"], 0)

    def test_dos_historias_misma_percepcion_actual(self):
        percepcion_actual = {
            "capacidad_x": 20,
            "presion": 0.90
        }

        # Historia A:
        # primero presión baja y luego presión alta.
        estado_a = crear_estado_inicial()

        estado_a = actualizar_estado(
            estado_a,
            {"capacidad_x": 20, "presion": 0.60}
        )

        estado_a = actualizar_estado(
            estado_a,
            percepcion_actual
        )

        accion_a, _ = decidir_reactivo_modelo(estado_a)

        # Historia B:
        # dos horas consecutivas con presión alta.
        estado_b = crear_estado_inicial()

        estado_b = actualizar_estado(
            estado_b,
            {"capacidad_x": 20, "presion": 0.90}
        )

        estado_b = actualizar_estado(
            estado_b,
            percepcion_actual
        )

        accion_b, _ = decidir_reactivo_modelo(estado_b)

        self.assertEqual(accion_a, "NO_REFORZAR")
        self.assertEqual(accion_b, "RECOMENDAR_REFUERZO")


if __name__ == "__main__":
    unittest.main()