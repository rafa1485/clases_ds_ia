import inspect
import unittest

from plantilla_agentes_movilidad import (
    actualizar_estado,
    crear_estado_inicial,
    decidir_reactivo_modelo,
    decidir_reactivo_simple,
)


def crear_percepcion(presion: float) -> dict:
    """Crea una percepción válida para las pruebas."""
    return {
        "hora": 8,
        "capacidad_x": 20,
        "presion": presion,
    }


class TestAgentesMovilidad(unittest.TestCase):

    def test_presion_baja(self):
        """Ambos agentes deben devolver NO_REFORZAR."""
        percepcion = crear_percepcion(0.50)

        accion_simple, _ = decidir_reactivo_simple(percepcion)

        estado = crear_estado_inicial()
        estado = actualizar_estado(estado, percepcion)
        accion_modelo, _ = decidir_reactivo_modelo(estado)

        self.assertEqual(accion_simple, "NO_REFORZAR")
        self.assertEqual(accion_modelo, "NO_REFORZAR")
        self.assertEqual(estado["racha_presion_alta"], 0)

    def test_primera_hora_con_presion_alta(self):
        """El simple recomienda, pero el modelo todavía no."""
        percepcion = crear_percepcion(0.90)

        accion_simple, _ = decidir_reactivo_simple(percepcion)

        estado = crear_estado_inicial()
        estado = actualizar_estado(estado, percepcion)
        accion_modelo, _ = decidir_reactivo_modelo(estado)

        self.assertEqual(
            accion_simple,
            "RECOMENDAR_REFUERZO",
        )
        self.assertEqual(
            accion_modelo,
            "NO_REFORZAR",
        )
        self.assertEqual(estado["racha_presion_alta"], 1)

    def test_segunda_hora_consecutiva_alta(self):
        """Después de dos horas altas, ambos recomiendan."""
        primera = crear_percepcion(0.90)
        segunda = crear_percepcion(0.95)

        estado = crear_estado_inicial()
        estado = actualizar_estado(estado, primera)
        estado = actualizar_estado(estado, segunda)

        accion_simple, _ = decidir_reactivo_simple(segunda)
        accion_modelo, _ = decidir_reactivo_modelo(estado)

        self.assertEqual(
            accion_simple,
            "RECOMENDAR_REFUERZO",
        )
        self.assertEqual(
            accion_modelo,
            "RECOMENDAR_REFUERZO",
        )
        self.assertEqual(estado["racha_presion_alta"], 2)

    def test_misma_percepcion_con_historias_distintas(self):
        """El modelo puede decidir diferente según su historia."""
        percepcion_final = crear_percepcion(0.90)

        # Historia A: presión baja seguida de presión alta.
        estado_a = crear_estado_inicial()
        estado_a = actualizar_estado(
            estado_a,
            crear_percepcion(0.50),
        )
        estado_a = actualizar_estado(
            estado_a,
            percepcion_final,
        )

        # Historia B: dos presiones altas consecutivas.
        estado_b = crear_estado_inicial()
        estado_b = actualizar_estado(
            estado_b,
            crear_percepcion(0.95),
        )
        estado_b = actualizar_estado(
            estado_b,
            percepcion_final,
        )

        accion_simple_a, _ = decidir_reactivo_simple(
            percepcion_final
        )
        accion_simple_b, _ = decidir_reactivo_simple(
            percepcion_final
        )

        accion_modelo_a, _ = decidir_reactivo_modelo(estado_a)
        accion_modelo_b, _ = decidir_reactivo_modelo(estado_b)

        # El simple ve la misma percepción y decide lo mismo.
        self.assertEqual(accion_simple_a, accion_simple_b)
        self.assertEqual(
            accion_simple_a,
            "RECOMENDAR_REFUERZO",
        )

        # El modelo decide según la historia.
        self.assertEqual(estado_a["racha_presion_alta"], 1)
        self.assertEqual(estado_b["racha_presion_alta"], 2)
        self.assertEqual(accion_modelo_a, "NO_REFORZAR")
        self.assertEqual(
            accion_modelo_b,
            "RECOMENDAR_REFUERZO",
        )

    def test_no_se_utilizan_datos_de_h_mas_1(self):
        """Agregar información futura no debe cambiar la decisión."""
        percepcion_normal = crear_percepcion(0.90)

        percepcion_con_futuro = {
            **percepcion_normal,
            "resultado_h_mas_1": {
                "presion": 0.10,
                "necesita_refuerzo": False,
            },
        }

        resultado_normal = decidir_reactivo_simple(
            percepcion_normal
        )
        resultado_con_futuro = decidir_reactivo_simple(
            percepcion_con_futuro
        )

        self.assertEqual(
            resultado_normal,
            resultado_con_futuro,
        )

        parametros_simple = list(
            inspect.signature(
                decidir_reactivo_simple
            ).parameters
        )
        parametros_modelo = list(
            inspect.signature(
                decidir_reactivo_modelo
            ).parameters
        )

        self.assertEqual(parametros_simple, ["percepcion"])
        self.assertEqual(parametros_modelo, ["estado_actual"])


if __name__ == "__main__":
    unittest.main()