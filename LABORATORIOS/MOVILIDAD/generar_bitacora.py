import pandas as pd
from plantilla_agentes_movilidad import procesar_secuencia

print("Leyendo percepciones...")
datos = pd.read_csv("escenario_agente/percepciones.csv")
print("Procesando agentes...")
bitacora_final = procesar_secuencia(datos)
print("Guardando bitacora_agentes.csv...")
bitacora_final.to_csv("bitacora_agentes.csv", index=False)
print("¡Completado!")
