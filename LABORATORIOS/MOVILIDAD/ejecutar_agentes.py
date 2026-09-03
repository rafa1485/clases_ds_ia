import pandas as pd

from agentes_movilidad import procesar_secuencia


RUTA_PERCEPCIONES = "../../escenario_agente/percepciones.csv"
RUTA_BITACORA = "bitacora_agentes.csv"


def main():
    percepciones = pd.read_csv(RUTA_PERCEPCIONES)

    bitacora = procesar_secuencia(percepciones)

    bitacora.to_csv(RUTA_BITACORA, index=False)

    print("Bitácora generada correctamente.")
    print()
    print(bitacora.to_string(index=False))
    print()
    print(f"Archivo guardado en: {RUTA_BITACORA}")


if __name__ == "__main__":
    main()