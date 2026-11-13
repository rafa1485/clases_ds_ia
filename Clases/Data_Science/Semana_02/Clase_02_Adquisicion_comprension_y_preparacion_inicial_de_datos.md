---
title: "Adquisición, comprensión y preparación inicial de datos"
subtitle: "De fuentes heterogéneas a una tabla analítica defendible"
course: "Data Science"
week: 2
class: 2
language: es
---

# Adquisición, comprensión y preparación inicial de datos

## De fuentes heterogéneas a una tabla analítica defendible

**Semana 2 · Clase 2**

---

# Propósito y resultados de aprendizaje

**Propósito:** adquirir, comprender y preparar datos sin separar decisiones técnicas de su significado y uso.

Al finalizar podremos:

- distinguir fuente, archivo, tabla, dataset y producto;
- documentar procedencia, unidad, granularidad y regla de una fila;
- evaluar calidad apta al propósito, faltantes, duplicados, claves y cardinalidad;
- integrar viajes, zonas y clima en una tabla **zona-hora** reproducible;
- explicar qué se pierde al agregar y qué límites conserva el análisis.

Correspondencia: capítulos **2, 3 y 4** del libro.

---

# La preparación comienza con una pregunta

> “Tenemos muchos archivos” no define un problema de datos.

Ejemplo genérico: para describir entregas tardías por sucursal-día debemos precisar:

- producto esperado: tabla, gráfico o decisión;
- unidad final: sucursal-día;
- población, periodo y exclusiones;
- variables necesarias y momento de disponibilidad.

**La pregunta determina qué adquirir y cómo representarlo.**

---

# Fuente, archivo, tabla, dataset y producto

| Concepto | Función | Ejemplo breve |
|---|---|---|
| Fuente | Sistema o institución de origen | portal municipal |
| Archivo | Objeto de intercambio | `enero.parquet` |
| Tabla | Estructura de filas y columnas | viajes |
| Dataset | Colección delimitada y documentada | viajes + diccionario |
| Producto | Evidencia destinada a un uso | perfil zona-hora |

Un archivo puede contener varias tablas; un dataset puede usar varios archivos; el producto es una **transformación**, no otro nombre para la fuente.

---

# Procedencia y linaje

**Diagrama:** `fenómeno → captura → fuente → extracción → transformaciones → producto`.

Por cada fuente registrar:

- responsable, propósito original y mecanismo de generación;
- URL o ubicación, fecha de acceso, versión y licencia;
- filtros, conversiones y uniones realizadas;
- artefacto resultante y responsable de la decisión.

La procedencia responde **de dónde viene**; el linaje permite reconstruir **qué le hicimos**.

---

# Unidad y granularidad

- **Unidad de análisis:** entidad elemental sobre la que se describe o compara.
- **Granularidad:** nivel de detalle temporal, espacial y de entidad.

Ejemplo:

| Representación | Unidad | Granularidad |
|---|---|---|
| ventas | transacción | producto-instante |
| resumen | tienda-día | tienda × día |

Cambiar granularidad cambia preguntas válidas, dependencias y cantidad de filas.

---

# La regla de una fila

Antes de limpiar, completar:

> **Una fila representa ________.**

Ejemplo: “una medición de un sensor en un instante”, no “un sensor”.

Comprobar:

- qué columnas identifican esa unidad;
- si dos filas con la misma clave son repetición, corrección o duplicado;
- si listas, intervalos o medidas repetidas rompen la regla.

Sin esta regla, `drop_duplicates()` puede borrar observaciones legítimas.

---

# Tipos físicos y tipos semánticos

| Valor almacenado | Tipo físico | Tipo semántico correcto |
|---|---|---|
| `00123` | texto | identificador nominal |
| `2024-01-05` | texto | fecha |
| `1, 2, 3` | entero | categoría ordinal |
| `-73.98` | decimal | longitud geográfica |

El tipo físico permite operaciones; el semántico determina cuáles **tienen sentido**.

Promediar códigos postales es computable, pero semánticamente inválido.

---

# Calidad apta al propósito

La calidad no es perfección universal; es suficiencia para un uso declarado.

| Dimensión | Pregunta de control |
|---|---|
| Completitud | ¿faltan campos o unidades necesarias? |
| Validez | ¿cumple dominio, formato y rango? |
| Consistencia | ¿concuerdan campos y fuentes? |
| Unicidad | ¿la clave identifica una fila? |
| Oportunidad | ¿llega antes de usarla? |
| Cobertura | ¿representa población, lugar y periodo? |

**Un dato puede ser correcto y aun así no ser apto.**

---

# Faltantes: ausencia con significado

Un nulo puede significar:

- no medido, no aplicable o desconocido;
- fallo de captura o unión sin correspondencia;
- valor censurado o todavía no disponible.

Diagnóstico mínimo: proporción por variable, patrón por grupo y periodo, y relación con el proceso de captura.

No imputar hasta explicar el mecanismo y el costo de equivocarse.

---

# Duplicados: definir antes de eliminar

- **Exacto:** todas las columnas coinciden.
- **De clave:** coincide la clave esperada, difieren atributos.
- **De entidad:** dos registros representan el mismo objeto sin clave común.

Ejemplo: dos lecturas del mismo paciente-hora pueden ser duplicados, reintentos o mediciones válidas.

Decidir con regla documentada: conservar, consolidar, versionar o excluir.

---

# Claves y cardinalidad

- Clave primaria: identifica filas en una tabla.
- Clave foránea: referencia otra tabla.
- Cardinalidad esperada: `one_to_one`, `many_to_one`, `one_to_many` o `many_to_many`.

Ejemplo: muchas ventas pertenecen a una tienda: `ventas → tiendas` es **many-to-one**.

Una unión many-to-many accidental multiplica filas y totales sin lanzar error.

---

# Integración segura

Antes y después de unir:

1. declarar unidad y clave de cada tabla;
2. verificar unicidad del lado que debe ser “uno”;
3. validar cardinalidad en el código;
4. medir coincidencias y no coincidencias;
5. comprobar filas, unidades y totales.

**Toda unión es una hipótesis sobre correspondencia.**

---

# Integración temporal

Tres relojes pueden diferir: tiempo del evento, de registro y de disponibilidad.

Para unir por hora:

- interpretar zona horaria de origen;
- convertir a una zona común;
- definir intervalos, bordes y horario de verano;
- agregar cada fuente a granularidad compatible.

`10:00 UTC` y `10:00 America/New_York` no son el mismo instante.

---

# Integración espacial

Una relación espacial puede usar:

- identificador administrativo estable;
- punto dentro de polígono;
- zona más cercana o intersección.

Registrar sistema de referencia de coordenadas (CRS), versión de límites y casos sin zona.

Los centroides resumen geometría, pero pueden quedar fuera del polígono o distorsionar distancia.

---

# Agregación y pérdida de información

Al pasar de eventos a grupos:

$$n_g=\sum_i \mathbb{1}(G_i=g), \qquad \bar{x}_g=\frac{1}{n_g}\sum_{i:G_i=g}x_i$$

Ganamos comparabilidad y reducimos volumen; perdemos orden intra-grupo, variabilidad individual y posibilidad de reconstruir casos.

Conservar conteo, dispersión, cobertura y regla de agregación junto a la media.

---

# Reproducibilidad desde la adquisición

Una ejecución reconstruible registra:

- URL, fecha de acceso, periodo y parámetros;
- versiones de librerías y formato;
- código ordenado de inicio a fin;
- validaciones y decisiones de exclusión;
- salida con esquema, clave y procedencia.

**Notebook de la clase:** `Taller_Clase_02_Movilidad.ipynb`.

---

# Del concepto al taller

**Pregunta:** ¿cómo varían los viajes Yellow Taxi reportados por zona de origen y hora, y qué asociación descriptiva muestran con el clima?

Flujo: `TLC viajes → zonas + shapefile → zona-hora ← NOAA clima`.

Meta: construir una tabla analítica auditada, no un modelo predictivo.

**Importante:** viajes reportados por TLC ≠ demanda total de movilidad.

---

# Taller 1: fuentes y definición analítica

**Notebook:** `Taller_Clase_02_Movilidad.ipynb`

| Fuente | Archivo / tabla | Unidad original |
|---|---|---|
| NYC TLC | Yellow Taxi enero 2024, Parquet | viaje reportado |
| NYC TLC | `taxi_zone_lookup.csv` | zona-ID |
| NYC TLC | `taxi_zones.zip`, shapefile | polígono-zona |
| NOAA GHCNh | estación USW00094728, PSV | estación-observación |

Producto: una fila = **zona de origen-hora local**; clave `PULocationID, hora`.

---

# Taller 2: construir la URL TLC

```python
def construir_url_tlc(tipo, anio, mes):
    prefijos = {
        "yellow": "yellow_tripdata",
        "green": "green_tripdata",
        "fhv": "fhv_tripdata",
        "fhvhv": "fhvhv_tripdata",
    }
    return ("https://d37ci6vzurychx.cloudfront.net/trip-data/"
            f"{prefijos[tipo]}_{anio}-{mes:02d}.parquet")
```

Parámetros explícitos hacen visible el periodo y evitan editar URL manualmente.

---

# Taller 3: cargar Parquet con proyección

```python
cols = ["tpep_pickup_datetime", "tpep_dropoff_datetime",
        "PULocationID", "DOLocationID", "passenger_count",
        "trip_distance", "fare_amount", "total_amount"]
url = construir_url_tlc("yellow", 2024, 1)
viajes = pd.read_parquet(url, columns=cols)
print(viajes.shape)
```

Parquet conserva tipos y permite leer solo columnas necesarias. La fuente es pública y secundaria, generada con propósito operativo/administrativo.

---

# Taller 4: inspeccionar antes de transformar

```python
viajes.info()
display(viajes.head(3))
display(viajes.describe(include="all").T)
print(viajes.dtypes)
```

Preguntas: ¿qué representa una fila?, ¿qué rango temporal aparece?, ¿IDs son medidas o categorías?, ¿hay importes o duraciones imposibles?

La inspección produce hipótesis; los controles las vuelven verificables.

---

# Taller 5: controles de calidad básicos

```python
clave = ["tpep_pickup_datetime", "tpep_dropoff_datetime",
         "PULocationID", "DOLocationID", "total_amount"]
qc = {
    "nulos_pct": viajes.isna().mean().mul(100),
    "duplicados_clave": viajes.duplicated(clave).sum(),
    "duracion_no_positiva": (viajes.tpep_dropoff_datetime <=
                              viajes.tpep_pickup_datetime).sum(),
}
```

La clave es una aproximación operativa, no un identificador oficial de viaje.

---

# Taller 6: validez y filtros explícitos

```python
validos = (
    viajes["PULocationID"].notna()
    & (viajes["trip_distance"] >= 0)
    & (viajes["total_amount"] >= 0)
    & (viajes["tpep_dropoff_datetime"] >
       viajes["tpep_pickup_datetime"])
)
viajes_limpios = viajes.loc[validos].copy()
```

Reportar cuántas filas excluye cada regla. La pertenencia al catálogo TLC se comprobará al unir; rango plausible no equivale a verdad.

---

# Taller 7: zonas y unión many-to-one

```python
zones_url = ("https://d37ci6vzurychx.cloudfront.net/"
             "misc/taxi_zone_lookup.csv")
zonas = pd.read_csv(zones_url)
assert zonas["LocationID"].is_unique
viajes_z = viajes_limpios.merge(
    zonas, left_on="PULocationID", right_on="LocationID",
    how="left", validate="many_to_one", indicator=True)
```

Auditar `_merge`: cada viaje debe encontrar como máximo una zona de origen.

---

# Taller 8: cobertura y pérdidas de la unión

```python
cobertura = viajes_z["_merge"].value_counts(dropna=False)
sin_zona = viajes_z.loc[
    viajes_z["_merge"] == "left_only", "PULocationID"
].value_counts()
assert len(viajes_z) == len(viajes_limpios)
print(cobertura, sin_zona.head())
```

Una unión izquierda conserva viajes, pero deja atributos nulos. El control de filas detecta multiplicación, no garantiza cobertura semántica.

---

# Taller 9: shapefile y geometría

```python
geo_url = ("https://d37ci6vzurychx.cloudfront.net/"
           "misc/taxi_zones.zip")
zonas_geo = gpd.read_file(f"zip://{geo_url}")
zonas_geo["LocationID"] = zonas_geo["LocationID"].astype(int)
zonas_geo = zonas_geo.to_crs(4326)
assert zonas_geo["LocationID"].is_unique
```

El lookup aporta nombres; el shapefile aporta polígonos. No reemplazar geometría por centroides para análisis de cobertura.

---

# Taller 10: construir zona-hora

```python
viajes_z["hora"] = (
    viajes_z["tpep_pickup_datetime"]
    .dt.tz_localize("America/New_York", ambiguous="NaT",
                    nonexistent="shift_forward")
    .dt.floor("h")
)
zona_hora = (viajes_z.groupby(["PULocationID", "hora"])
             .agg(viajes_reportados=("PULocationID", "size"),
                  distancia_media=("trip_distance", "mean"))
             .reset_index())
```

La agregación cambia la unidad de viaje a zona-hora y elimina detalle individual.

---

# Taller 11: NOAA e interpretación UTC

```python
meteo_url = ("https://www.ncei.noaa.gov/oa/global-historical-"
             "climatology-network/hourly/access/by-year/2024/psv/"
             "GHCNh_USW00094728_2024.psv")
clima = pd.read_csv(meteo_url, sep="|", low_memory=False)
clima["DATE_UTC"] = pd.to_datetime(clima["DATE"], utc=True)
clima["DATE_NY"] = clima["DATE_UTC"].dt.tz_convert(
    "America/New_York")
```

Convertimos un instante UTC; no “cambiamos la etiqueta” de una hora ingenua.

---

# Taller 12: clima horario de enero

```python
inicio = pd.Timestamp("2024-01-01", tz="America/New_York")
fin = pd.Timestamp("2024-02-01", tz="America/New_York")
clima_mes = clima[clima["DATE_NY"].between(
    inicio, fin, inclusive="left")].copy()
clima_mes["hora"] = clima_mes["DATE_NY"].dt.floor("h")
vars_num = ["temperature", "relative_humidity",
            "wind_speed", "precipitation"]
clima_h = clima_mes.groupby("hora")[vars_num].mean().reset_index()
```

Promediar mediciones subhorarias pierde extremos y secuencia; conservar conteos por hora.

---

# Taller 13: unir zona-hora con clima

```python
assert clima_h["hora"].is_unique
analitica = zona_hora.merge(
    clima_h, on="hora", how="left",
    validate="many_to_one", indicator="union_clima")
print(analitica["union_clima"].value_counts())
print(analitica.isna().mean().sort_values(ascending=False).head())
```

Una hora meteorológica se replica para muchas zonas: supuesto fuerte de representatividad espacial de una estación.

---

# Taller 14: perfil horario de viajes reportados

```python
perfil_hora = (analitica.assign(
    hora_dia=analitica["hora"].dt.hour)
    .groupby("hora_dia", as_index=False)
    ["viajes_reportados"].sum())
plt.plot(perfil_hora["hora_dia"],
         perfil_hora["viajes_reportados"], marker="o")
plt.ylabel("Viajes Yellow Taxi reportados")
plt.xlabel("Hora local")
```

El patrón describe registros TLC de enero de 2024, no demanda total ni viajes no atendidos.

---

# Taller 15: mapa por zona

```python
por_zona = (analitica.groupby("PULocationID", as_index=False)
            ["viajes_reportados"].sum())
mapa = zonas_geo.merge(
    por_zona, left_on="LocationID", right_on="PULocationID",
    how="left", validate="one_to_one")
mapa.plot(column="viajes_reportados", cmap="YlGnBu",
          legend=True, missing_kwds={"color": "lightgrey"})
```

Comparar conteos refleja tamaño, actividad, cobertura y proceso de registro; no solo preferencia de usuarios.

---

# Taller 16: clima y asociación descriptiva

```python
por_hora = (analitica.groupby("hora", as_index=False)
            .agg(viajes_reportados=("viajes_reportados", "sum"),
                 temperatura=("temperature", "first"),
                 precipitacion=("precipitation", "first")))
plt.scatter(por_hora["temperatura"], por_hora["viajes_reportados"],
            c=por_hora["precipitacion"], cmap="Blues")
r = por_hora[["temperatura", "viajes_reportados"]].corr().iloc[0, 1]
```

Una correlación resume asociación lineal; hora, calendario y selección pueden confundirla. **Correlación no implica causalidad.**

---

# Taller 17: guardar un producto reproducible

```python
analitica = analitica.sort_values(["hora", "PULocationID"])
assert not analitica.duplicated(["PULocationID", "hora"]).any()
alcance = "semana_1_enero_2024" if MODO_CLASE else "enero_2024"
ruta = Path(tempfile.gettempdir()) / f"zona_hora_{alcance}.parquet"
analitica.to_parquet(ruta, index=False)
metadatos = {
    "unidad": "zona de origen-hora local",
    "zona_horaria": "America/New_York",
    "fuentes": [url, zones_url, geo_url, meteo_url],
}
```

Entregar también controles, exclusiones, versiones y fecha de ejecución.

---

# Producto y evidencia de aprendizaje

**Entregable:** `Taller_Clase_02_Movilidad.ipynb` ejecutado de inicio a fin.

Debe incluir:

- inventario de cuatro fuentes y procedencia;
- regla de una fila y diccionario semántico mínimo;
- reporte de faltantes, duplicados, validez, cobertura y cardinalidad;
- tabla zona-hora temporal con alcance explícito y clave única;
- perfil horario, mapa y gráfico clima-viajes;
- cinco hallazgos con evidencia y tres límites.

---

# Límites y afirmaciones permitidas

Podemos describir **viajes Yellow Taxi reportados** y asociaciones dentro del periodo y cobertura analizados.

No podemos afirmar directamente:

- demanda total de movilidad o solicitudes no atendidas;
- comportamiento de todas las plataformas, personas o meses;
- causalidad del clima sobre los viajes;
- clima idéntico en toda zona por usar una estación;
- exactitud de cada registro por superar controles de plausibilidad.

---

# Cierre: de datos disponibles a evidencia defendible

1. Formular propósito y producto antes de descargar.
2. Declarar fuente, procedencia, unidad y regla de una fila.
3. Tratar tipos, faltantes y duplicados según significado.
4. Validar claves, cardinalidad y cobertura al integrar.
5. Alinear tiempo y espacio antes de agregar.
6. Documentar pérdidas, límites y cadena reproducible.

**Lectura:** capítulos 2, 3 y 4. Próximo paso: exploración estadística sin exceder lo que los datos representan.
