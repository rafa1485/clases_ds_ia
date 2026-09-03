import pandas as pd
from clases_ds_ia.LABORATORIOS.MOVILIDAD.agentes_movilidad import procesar_secuencia

percepciones = pd.read_csv(
    "clases_ds_ia/escenario_agente/percepciones.csv"
)

bitacora = procesar_secuencia(percepciones)

bitacora.to_csv(
    "clases_ds_ia/bitacora_agentes.csv",
    index=False
)

print(bitacora.to_string(index=False))
print("\nBitácora guardada en:")
print("clases_ds_ia/bitacora_agentes.csv")