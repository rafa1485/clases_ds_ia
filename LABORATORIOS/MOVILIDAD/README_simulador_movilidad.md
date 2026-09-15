# Simulador de movilidad

El archivo [`simulador_movilidad.py`](simulador_movilidad.py) simula los
viajes de Yellow Taxi que comienzan durante una hora determinada de un lunes.
El modelo utiliza como referencia los viajes históricos publicados por la
Taxi and Limousine Commission (TLC) de Nueva York.

## Alcance

Cada ejecución produce una realización aleatoria de los viajes de una hora.
Para cada viaje se simulan:

- el minuto de inicio;
- la zona TLC de *pickup*;
- la zona TLC de *dropoff*;
- la distancia recta entre los centros de ambas zonas.

Los registros de TLC corresponden a viajes realizados y reportados. Por lo
tanto, la simulación no representa solicitudes no atendidas, otros medios de
transporte ni la demanda total de movilidad.

## Modelo de simulación

Para el año, mes y hora seleccionados, el simulador realiza los siguientes
pasos:

1. Conserva solamente los viajes iniciados un lunes durante la hora indicada.
2. Descarta los viajes cuyas zonas de origen o destino no tengan geometría.
3. Calcula la demanda histórica promedio dividiendo la cantidad de viajes
   válidos por la cantidad total de lunes calendario del mes. En este cálculo
   también se consideran los lunes sin viajes registrados.
4. Sortea la cantidad de viajes mediante una distribución de Poisson:

   ```text
   N ~ Poisson(demanda histórica promedio)
   ```

5. Sortea cada par *pickup-dropoff* según su frecuencia conjunta entre los
   viajes históricos filtrados.
6. Sortea el minuto de inicio con una distribución uniforme discreta entre 0
   y 59.
7. Calcula la distancia de Haversine entre los centroides de las zonas.

Los centroides se calculan proyectando primero las geometrías a `EPSG:2263` y
convirtiendo posteriormente sus coordenadas a `EPSG:4326`.

## Dependencias

Desde la raíz del repositorio, instalar las dependencias con:

```bash
python -m pip install -r requirements.txt
```

Las dependencias principales del simulador son:

- `numpy`;
- `pandas`;
- `pyarrow`;
- `geopandas`.

La ejecución requiere conexión a Internet cuando se utilizan las fuentes TLC
predeterminadas.

## Entrada por línea de comandos

El único parámetro obligatorio es `--hora`:

```bash
python MATERIAL_CURSOS/LABORATORIOS/MOVILIDAD/simulador_movilidad.py \
  --hora 8
```

### Parámetros

| Parámetro | Tipo | Valor predeterminado | Descripción |
|---|---:|---:|---|
| `--hora` | entero | Sin valor | Hora que se simulará, entre 0 y 23. |
| `--anio` | entero | `2024` | Año de los datos históricos. |
| `--mes` | entero | `1` | Mes de los datos históricos, entre 1 y 12. |
| `--datos` | texto | URL de TLC | Ruta local o URL del archivo parquet de viajes. |
| `--semilla` | entero | Aleatoria | Semilla para obtener resultados reproducibles. |
| `--salida` | ruta | Sin valor | Archivo CSV donde se guardará la tabla completa. |

El parquet indicado mediante `--datos` debe contener estas columnas:

- `tpep_pickup_datetime`;
- `PULocationID`;
- `DOLocationID`.

Si no se especifica `--datos`, se utiliza automáticamente el parquet mensual
de Yellow Taxi correspondiente a `--anio` y `--mes`.

## Ejemplos

### Simulación básica

Simular los viajes de los lunes entre las 08:00 y las 08:59:

```bash
python MATERIAL_CURSOS/LABORATORIOS/MOVILIDAD/simulador_movilidad.py \
  --hora 8
```

Sin `--salida`, el programa muestra la demanda promedio, la cantidad de viajes
simulados y las primeras diez filas.

### Simulación reproducible y exportación

```bash
python MATERIAL_CURSOS/LABORATORIOS/MOVILIDAD/simulador_movilidad.py \
  --hora 8 \
  --semilla 42 \
  --salida MATERIAL_CURSOS/LABORATORIOS/MOVILIDAD/viajes_lunes_08.csv
```

El mismo conjunto de datos, hora y semilla produce el mismo resultado.

### Uso de un parquet local

```bash
python MATERIAL_CURSOS/LABORATORIOS/MOVILIDAD/simulador_movilidad.py \
  --hora 18 \
  --anio 2024 \
  --mes 1 \
  --datos /ruta/al/archivo/yellow_tripdata_2024-01.parquet \
  --salida viajes_lunes_18.csv
```

El año y el mes deben coincidir con el período que se desea extraer del
parquet.

## Salida

La salida es una tabla en la que cada fila representa un viaje simulado.

| Columna | Descripción |
|---|---|
| `viaje_id` | Identificador consecutivo dentro de la simulación. |
| `dia_semana` | Día simulado; siempre contiene `lunes`. |
| `hora` | Hora seleccionada. |
| `minuto` | Minuto de inicio sorteado, entre 0 y 59. |
| `PULocationID` | Identificador TLC de la zona de *pickup*. |
| `zona_pickup` | Nombre de la zona de *pickup*. |
| `latitud_pickup` | Latitud del centro de la zona de *pickup*. |
| `longitud_pickup` | Longitud del centro de la zona de *pickup*. |
| `DOLocationID` | Identificador TLC de la zona de *dropoff*. |
| `zona_dropoff` | Nombre de la zona de *dropoff*. |
| `latitud_dropoff` | Latitud del centro de la zona de *dropoff*. |
| `longitud_dropoff` | Longitud del centro de la zona de *dropoff*. |
| `distancia_centros_km` | Distancia de Haversine entre centroides, en kilómetros. |

La tabla se ordena por minuto. Si el sorteo de Poisson produce cero viajes, se
devuelve una tabla vacía que conserva estas columnas.

## Uso desde Python

La lógica también puede utilizarse sin la interfaz de línea de comandos:

```python
import pandas as pd

from MATERIAL_CURSOS.LABORATORIOS.MOVILIDAD.simulador_movilidad import (
    cargar_centros_zonas,
    construir_url_tlc,
    estimar_modelo_demanda,
    simular_viajes,
)

anio = 2024
mes = 1
hora = 8

viajes = pd.read_parquet(
    construir_url_tlc(anio, mes),
    columns=["tpep_pickup_datetime", "PULocationID", "DOLocationID"],
)
centros = cargar_centros_zonas()
tasa, distribucion_od = estimar_modelo_demanda(
    viajes,
    centros,
    hora,
    anio,
    mes,
)
resultado = simular_viajes(
    tasa,
    distribucion_od,
    centros,
    hora,
    semilla=42,
)

print(resultado.head())
```

`simular_viajes` devuelve un `pandas.DataFrame` y no escribe archivos por sí
misma.

## Entorno para agentes

El módulo
[`simulador_entorno_agente.py`](simulador_entorno_agente.py) transforma los
viajes en una secuencia de percepciones para una empresa ficticia X. El entorno
simula una participación aleatoria de otras empresas y separa la información
visible hasta `h` del resultado futuro usado para evaluar la recomendación.

```bash
python MATERIAL_CURSOS/LABORATORIOS/MOVILIDAD/simulador_entorno_agente.py \
  --zona 161 \
  --hora 8 \
  --taxis-x 20 \
  --horas-historia 3 \
  --semilla 42 \
  --salida-dir escenario_agente
```

El comando genera:

- `percepciones.csv`, que puede ser leído por el agente;
- `resultado_h_mas_1.csv`, reservado para evaluación posterior.

La actividad asociada está definida en
[`consigna_agentes_movilidad.md`](consigna_agentes_movilidad.md) y cuenta con
la plantilla inicial
[`plantilla_agentes_movilidad.py`](plantilla_agentes_movilidad.py).

## Interpretación y limitaciones

- La tasa Poisson supone que el promedio histórico es representativo de la
  demanda de viajes reportados para la hora seleccionada.
- La distribución de destinos mantiene las frecuencias históricas conjuntas
  de los pares *pickup-dropoff*.
- El minuto uniforme supone intensidad constante dentro de la hora.
- La distancia entre centroides no es una distancia vial ni reproduce la ruta
  seguida por un taxi.
- Los viajes dentro de una misma zona tienen distancia entre centroides igual
  a cero.
- El modelo no incorpora tránsito, clima, duración, disponibilidad de taxis ni
  cambios estacionales fuera del mes seleccionado.
- La división entre una empresa X y otras empresas en el entorno para agentes
  es sintética y no describe participaciones reales de mercado.
