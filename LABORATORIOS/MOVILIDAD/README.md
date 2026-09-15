# TP: Agentes reactivos para refuerzo de taxis

Trabajo práctico de IA clásica: implementación y comparación de un agente reactivo simple y un agente reactivo basado en modelo que recomiendan si conviene reforzar la flota de taxis de una empresa ficticia "X" en una zona, para la hora siguiente. Enunciado completo en [`consigna_agentes_movilidad.md`](consigna_agentes_movilidad.md).

## Mapa de archivos

| Archivo | Qué es |
|---|---|
| `consigna_agentes_movilidad.md` / `.pdf` | Enunciado original del TP. |
| `plantilla_agentes_movilidad.py` | Plantilla original provista por la cátedra. |
| **`agentes_movilidad.py`** | **Entrega 1.** Agentes implementados: `decidir_reactivo_simple`, `crear_estado_inicial` / `actualizar_estado` / `decidir_reactivo_modelo`, y `procesar_secuencia`. |
| **`test_agentes_movilidad.py`** | **Entrega 2.** Suite de tests (8 casos de prueba cubriendo todos los requisitos de la consigna). |
| `simulador_movilidad.py` | Simulador de viajes de taxi (provisto por la cátedra con ajuste de compatibilidad para Windows). |
| `simulador_entorno_agente.py` | Transforma los viajes simulados en percepciones horarias para los agentes. |
| `escenario_agente/percepciones.csv` | Escenario reproducible generado (zona 161, hora 8, 20 taxis de X, semilla 42). |
| `escenario_agente/resultado_h_mas_1.csv` | Resultado de la hora `h+1` (reservado para evaluación posterior, no usado para decidir). |
| `generar_bitacora.py` | Script que ejecuta `procesar_secuencia` sobre las percepciones para generar la bitácora. |
| **`bitacora_agentes.csv`** | **Entrega 3.** Comparación de ambos agentes hora por hora sobre el escenario. |
| **`informe.md`** | **Entrega 4.** Respuestas conceptuales, tabla PEAS y limitaciones del enfoque. |
| `CONSIGNAS_DE_REVISION.md` | Checklist de revisión y validación contra la rúbrica. |
| `requirements.txt` | Dependencias de Python necesarias. |
| `dataset_movilidad.py`, `DataSet_Movilidad.ipynb` / `.pdf`, `README_simulador_movilidad.md` | Material complementario sobre el dataset TLC y el simulador. |

## Cómo correr todo

Desde esta carpeta (`LABORATORIOS/MOVILIDAD/`):

```bash
# Instalar dependencias
python -m pip install -r requirements.txt

# Correr los tests obligatorios
python -m pytest test_agentes_movilidad.py -v

# Regenerar el escenario reproducible (descarga datos de TLC y el shapefile de zonas)
python simulador_entorno_agente.py --zona 161 --hora 8 --taxis-x 20 \
  --horas-historia 3 --semilla 42 --salida-dir escenario_agente

# Regenerar la bitácora a partir del escenario
python generar_bitacora.py
```

Con la semilla fija (`42`) y los mismos parámetros, el escenario generado es siempre idéntico, garantizando reproducibilidad.
