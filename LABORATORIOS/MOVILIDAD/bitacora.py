import pandas as pd
from plantilla_agentes_movilidad import procesar_secuencia

df_percepciones = pd.read_csv("escenario_agente/percepciones.csv")

df_bitacora = procesar_secuencia(df_percepciones)

df_bitacora.to_csv("bitacora_agentes.csv", index=False)
print("¡Bitácora generada con éxito!")