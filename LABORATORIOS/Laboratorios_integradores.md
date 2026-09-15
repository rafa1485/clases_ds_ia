# Laboratorios integradores

## Propósito

Los laboratorios integradores conectan los contenidos del libro mediante cuatro cadenas completas de trabajo:

`fuente -> auditoría -> representación -> análisis o modelo -> decisión simulada -> comunicación`

Cada laboratorio reutiliza las evidencias producidas por cuatro actividades EMO. El producto final es grupal, pero cada estudiante debe construir, interpretar y defender una variante individual. La aprobación no depende de alcanzar la mejor métrica; depende de demostrar que la solución es reproducible, metodológicamente correcta y realizable con las variables disponibles.

Las fuentes, campos y límites se definen en el [Apéndice D](Apendice_D_Proyectos_integradores.md). Este documento operacionaliza ese contrato. Ante una diferencia con una explicación genérica de otro capítulo, prevalecen las variables y restricciones del Apéndice D.

## 1. Reglas comunes de ejecución

### 1.1. Congelamiento de datos

Antes de comenzar, el equipo docente debe publicar un manifiesto de la versión utilizada. El manifiesto incluye fuente oficial, fecha de descarga, archivos, periodo, tamaño, suma de comprobación, esquema y particiones comunes.

No se permite reemplazar una fuente por otra versión durante el laboratorio sin generar un nuevo manifiesto. Una actualización puede modificar filas, categorías, distribución y métricas, aunque conserve el nombre del archivo.

### 1.2. Datos originales y productos derivados

Los originales se conservan sin modificaciones. Toda limpieza, agregación o partición produce un artefacto derivado con versión. El equipo debe poder reconstruir cada producto desde las fuentes congeladas.

La estructura mínima contiene:

```text
laboratorio/
  datos_originales/
  datos_procesados/
  src/
  notebooks/
  configuracion/
  resultados/
  modelos/
  documentacion/
```

El repositorio no debe incluir secretos ni copias de datos cuya redistribución no esté autorizada.

### 1.3. Partición antes de ajustar

Toda transformación aprendida se ajusta exclusivamente con entrenamiento. Esto incluye imputación, escalado, vocabulario, TF-IDF, categorías raras, componentes, selección de variables, umbrales y calibración.

La unidad de separación depende del caso:

| Caso | Separación obligatoria |
|---|---|
| Agua | Tiempo; considerar sitio para análisis de dependencia |
| Movilidad | Tiempo; zona según pregunta de generalización |
| Reclamos | Tiempo y grupo de duplicados o plantillas |
| Vegetales | `leaf_id`; prueba oficial reservada |

### 1.4. Baseline y criterio de aceptación

Todo modelo se compara con una regla simple. El baseline debe implementarse con el mismo protocolo y las mismas particiones. Seleccionar el mejor candidato no implica que sea aceptable: también debe superar criterios mínimos de utilidad, estabilidad, costo y riesgo.

### 1.5. Evidencia individual

Cada estudiante entrega un anexo que incluya:

- unidad o subconjunto asignado;
- una decisión metodológica propia;
- reproducción de un resultado común;
- análisis de al menos un error o anomalía;
- una limitación que afecte la decisión;
- respuesta a preguntas de defensa.

### 1.6. Extensiones

Una extensión no reemplaza una capacidad obligatoria. Solo puede incorporarse si se documentan fuente, licencia, variables, integración y nueva limitación. No se penaliza a quien complete correctamente el mínimo sin extensiones.

---

# Laboratorio integrador 1. Calidad del agua y prioridad de revisión

**Etiqueta:** `[LAB · AGUA]`

**EMO integradas:** `AGUA-01`, `AGUA-02`, `AGUA-03` y `AGUA-04`.

## 2.1. Fuente y alcance

Se utiliza **NYC DEP Drinking Water Quality Distribution Monitoring Data**, identificador `bkwf-xfky`:

- metadatos: <https://data.cityofnewyork.us/api/views/bkwf-xfky>;
- API: <https://data.cityofnewyork.us/resource/bkwf-xfky.json>.

Cada fila representa una muestra tomada en un sitio, fecha y hora. El laboratorio construye un indicador didáctico de riesgo de detección de coliformes y una prioridad de revisión o remuestreo.

El laboratorio **no** estudia presión, caudal, consumo ni fugas, porque esas variables no existen en la fuente. Tampoco certifica potabilidad ni recomienda tratamiento.

## 2.2. Variables disponibles

| Variable | Función en el laboratorio |
|---|---|
| `sample_number` | Clave de muestra y control de duplicados. |
| `sample_date` | Orden temporal, particiones, mes y estación. |
| `sample_time` | Hora; requiere armonización de formatos. |
| `sample_site` | Identificador del sitio; permite historial y comparación. |
| `sample_class` | Describe cumplimiento, operación o remuestreo. No se usa como predictor sin reconstruir su temporalidad. |
| `residual_free_chlorine_mg_l` | Evidencia química, originalmente texto. |
| `turbidity_ntu` | Evidencia física, originalmente texto. |
| `fluoride_mg_l` | Medición disponible en un subconjunto; no se exige imputación. |
| `coliform_quanti_tray_mpn_100ml` | Base para el evento `coliforme_detectado`. |
| `e_coli_quanti_tray_mpn_100ml` | Variable descriptiva; no objetivo obligatorio por extrema rareza. |

### 2.2.1. Derivados permitidos

- `fecha_hora`, luego de validar fecha y hora;
- año, mes, estación y franja;
- `coliforme_detectado`, diferenciando `<1` de resultados detectables;
- estado de censura inferior, observado o superior;
- cloro y turbidez numéricos con código original conservado;
- historial del sitio calculado únicamente con muestras anteriores;
- días desde la muestra anterior;
- tasa histórica de detección estimada en entrenamiento.

### 2.2.2. Variables y usos prohibidos

- no convertir `<1` en una medición exacta sin indicador de censura;
- no interpretar `-9` o `-9.99` como valores físicos antes de consultar el diccionario;
- no usar el resultado de coliformes como entrada para predecirse a sí mismo;
- no tratar una muestra de remuestreo como si fuera independiente del evento inicial;
- no construir una etiqueta general de “agua potable”;
- no incorporar presión, caudal o ubicación geográfica supuesta desde el código del sitio.

## 2.3. Objetivo y decisión simulada

### 2.3.1. Evento

El evento obligatorio es `coliforme_detectado`: resultado microbiológico válido que no está por debajo del límite indicado por `<1`. Los códigos inválidos o faltantes no se etiquetan como negativos.

### 2.3.2. Decisión

La decisión simulada es seleccionar muestras o sitios-periodo para revisión técnica o remuestreo bajo una capacidad $k$. No representa un protocolo regulatorio real.

Se admiten dos formulaciones, elegidas por el equipo docente:

1. **Triage retrospectivo:** ocultar el resultado de coliformes y utilizar cloro, turbidez y contexto de la misma muestra como evidencias preliminares. Debe declararse el supuesto didáctico de que esas evidencias estarían disponibles primero.
2. **Prioridad prospectiva:** utilizar exclusivamente historial anterior del sitio, estación y tiempo desde última muestra para priorizar la siguiente observación.

La cohorte completa debe utilizar la misma formulación para comparar resultados.

### 2.3.3. Baseline

El baseline es la tasa histórica de detección en entrenamiento. Puede ser global o por sitio cuando exista soporte mínimo. Los sitios nuevos utilizan la tasa global, no una estimación basada en prueba.

## 2.4. Secuencia de actividades

### Fase A. Formulación, `AGUA-01`

El equipo define usuario, unidad, horizonte, capacidad, evento, costo de revisión y costo de omisión. Debe explicar qué información se considera disponible al decidir.

**Entrega:** ficha de decisión y diagrama `muestra -> evidencia -> riesgo -> revisar/no revisar`.

**Control de viabilidad:** todas las entradas aparecen en la tabla de variables o son derivados autorizados.

### Fase B. Auditoría y limpieza, `AGUA-02`

Tareas obligatorias:

1. validar esquema y unicidad de `sample_number`;
2. perfilar faltantes por variable, periodo y `sample_class`;
3. armonizar `sample_time` y construir fecha-hora;
4. separar valor microbiológico y estado de censura;
5. detectar códigos negativos y conservar su forma original;
6. convertir cloro y turbidez con trazabilidad;
7. comparar filas antes y después;
8. producir una tabla de cuarentena para casos no interpretables.

**Entrega:** dataset procesado, diccionario, tabla de reglas y reporte de calidad.

**Control:** una detección rara nunca se elimina automáticamente como atípico.

### Fase C. Exploración, `AGUA-03`

El análisis mínimo incluye:

- distribución de cloro y turbidez;
- cobertura de fluoruro sin imputación obligatoria;
- detecciones de coliformes por periodo, sitio o clase con denominador;
- serie temporal de cantidad de muestras y detecciones;
- comparación entre muestras iniciales y remuestreos;
- tres hallazgos y tres explicaciones alternativas.

**Entrega:** notebook o informe con medidas robustas, al menos tres visualizaciones y limitaciones.

**Control:** no confundir asociación de turbidez con causa de detección.

### Fase D. Actualización de riesgo, `AGUA-04`

El conjunto se divide temporalmente. La previa y las verosimilitudes se estiman con entrenamiento. El mínimo incluye:

1. previa global o por sitio con soporte;
2. una evidencia discretizada, por ejemplo turbidez alta;
3. una segunda evidencia opcional o una tabla conjunta con soporte suficiente;
4. cálculo de posterior;
5. matriz de costos;
6. regla de selección de hasta $k$ casos;
7. sensibilidad a previa, verosimilitud y costos.

Si cloro y turbidez se tratan como condicionalmente independientes, el supuesto debe justificarse y compararse con una alternativa conjunta. Multiplicar evidencias correlacionadas sin revisión no cumple la actividad.

## 2.5. Integración y producto final

El equipo genera una tabla con:

| Campo | Descripción |
|---|---|
| Identificador | muestra o sitio-periodo |
| Fecha de decisión | instante del escenario |
| Evidencias | valores o categorías permitidas |
| Previa | riesgo antes de evidencias |
| Posterior | riesgo actualizado |
| Costo esperado | revisar frente a no revisar |
| Prioridad | posición dentro de capacidad $k$ |
| Acción | revisar, remuestrear o no priorizar |
| Advertencia | censura, cobertura o dato faltante relevante |

El reporte final explica qué se sabe, qué se supone y qué no puede concluirse. Debe incluir un análisis de sensibilidad donde al menos una prioridad cambie o se demuestre que permanece estable.

## 2.6. Criterios de aprobación

- la formulación utiliza variables realmente disponibles;
- la limpieza preserva censura y códigos originales;
- la exploración informa denominadores y cobertura;
- la actualización diferencia previa, verosimilitud y posterior;
- la decisión deriva de probabilidades y costos;
- el producto no afirma fugas, potabilidad ni causalidad;
- la cadena completa se reconstruye desde el manifiesto.

## 2.7. Extensiones opcionales

Catálogo oficial de sitios, clima, modelos jerárquicos o tratamiento formal de censura. Una extensión no permite presentar la actividad como evaluación regulatoria.

---

# Laboratorio integrador 2. Movilidad geotemporal y prioridad de zonas

**Etiqueta:** `[LAB · MOVILIDAD]`

**EMO integradas:** `MOV-01`, `MOV-02`, `MOV-03` y `MOV-04`.

## 3.1. Fuente y alcance

Se utilizan los Yellow Taxi Trip Records de NYC TLC disponibles en el repositorio:

- `yellow_tripdata_2026-02.parquet`;
- `yellow_tripdata_2026-03.parquet`;
- `yellow_tripdata_2026-04.parquet`.

La fuente auxiliar obligatoria es el Taxi Zone Lookup; para mapas se utiliza el Taxi Zone Shapefile oficial. Las fuentes están enlazadas en el Apéndice D.

El laboratorio analiza pickups reportados de taxi amarillo. No observa viajes de todos los modos, demanda insatisfecha, vehículos libres ni ubicación de conductores.

## 3.2. Variables disponibles

### 3.2.1. Variables obligatorias

| Variable | Uso |
|---|---|
| `tpep_pickup_datetime` | Tiempo de demanda y orden temporal. |
| `tpep_dropoff_datetime` | Duración retrospectiva y costo de aristas. |
| `PULocationID` | Zona de origen y unidad espacial de demanda. |
| `DOLocationID` | Zona de destino y grafo OD. |
| `trip_distance` | Distancia reportada y costo alternativo. |
| `passenger_count` | Auditoría y descripción; presenta faltantes. |
| `VendorID` | Control de cobertura por proveedor. |
| `store_and_fwd_flag` | Calidad de transmisión. |

Las variables monetarias pueden auditarse, pero no son necesarias para completar el laboratorio. `payment_type`, cargos y `total_amount` se conocen al finalizar y no se usan para pronosticar pickups.

### 3.2.2. Variables auxiliares

El lookup aporta `LocationID`, `Borough`, `Zone` y `service_zone`. El shapefile aporta geometría. No se requiere clima, población, eventos ni red vial.

### 3.2.3. Derivados permitidos

- duración en minutos;
- fecha, hora, día de semana y franja fija;
- conteo de pickups por zona-franja;
- conteo por par OD;
- tiempo y distancia medianos por arista;
- perfiles horarios por zona;
- entropía o diversidad de destinos;
- serie regular de pickups;
- centroides de zona para heurística, si se usa geometría.

## 3.3. Objetivo y decisión simulada

La decisión es priorizar zonas para posicionamiento o atención durante el siguiente horizonte. Es una **prioridad didáctica**, no un despacho óptimo de flota, porque no se dispone de oferta ni ubicación de vehículos libres.

Una regla mínima combina:

- pronóstico de pickups por zona;
- diferencia respecto del baseline;
- perfil del segmento;
- conectividad del grafo OD.

No debe afirmarse que la zona con más pickups tiene mayor necesidad social ni mayor demanda total de movilidad.

## 3.4. Preparación común

Antes de las EMO:

1. leer solo columnas necesarias para controlar memoria;
2. validar mes del pickup;
3. exigir drop-off posterior para variables de duración;
4. revisar distancia y duración conjuntamente;
5. unir zonas mediante `LocationID`;
6. marcar zonas desconocidas;
7. fijar una frecuencia común, por ejemplo una hora;
8. registrar conteos por archivo, proveedor y mes.

Los tres Parquet suman más de once millones de filas. No es obligatorio cargar todas las columnas ni todo el dataset simultáneamente. Se permite procesamiento por archivo o lotes, siempre que las agregaciones sean equivalentes.

## 3.5. Secuencia de actividades

### Fase A. Diagnóstico geotemporal, `MOV-01`

Construir una tabla zona-franja y producir:

- mapa de pickups;
- serie temporal o mapa de calor día-hora;
- distribución entre zonas;
- zonas sin correspondencia visibles;
- dos patrones y una anomalía investigada.

**Control:** el mapa usa los mismos cortes entre periodos y distingue conteo de cualquier tasa opcional.

### Fase B. Grafo OD, `MOV-02`

Construir un grafo dirigido:

- nodos: zonas TLC;
- aristas: pares OD con soporte mínimo;
- pesos: tiempo mediano, distancia mediana o una función declarada;
- frecuencia: cantidad de viajes por arista.

Comparar costo uniforme y A* para el mismo origen-destino. Si el peso es distancia, la distancia entre centroides puede ser heurística. Si es tiempo, debe dividirse por una velocidad máxima documentada para obtener una cota inferior plausible.

**Control:** el camino resultante recorre zonas conectadas por viajes observados. No es una ruta calle por calle.

### Fase C. Segmentación, `MOV-03`

Construir perfiles por zona usando al menos:

- distribución horaria de pickups;
- proporción de fin de semana;
- variabilidad diaria;
- diversidad de destinos;
- duración o distancia mediana.

Comparar dos estrategias de clustering y evaluar escalado, estabilidad, métricas e interpretación. Las zonas con cobertura insuficiente se excluyen o marcan antes de agrupar.

**Control:** el nombre de un segmento describe su perfil, no una categoría social inferida.

### Fase D. Pronóstico, `MOV-04`

Seleccionar una zona o segmento y construir una serie regular. Comparar:

- baseline de último valor o media estacional;
- un modelo ARIMA/SARIMA u otra alternativa;
- validación walk-forward;
- MAE o RMSE por horizonte;
- intervalos y errores temporales.

El horizonte debe ser corto: siguiente hora, varias horas o siguiente día. Tres meses no permiten exigir estacionalidad anual.

**Control:** ninguna transformación usa observaciones posteriores al instante pronosticado.

## 3.6. Integración y producto final

El equipo construye una tabla de prioridad para el próximo horizonte:

| Campo | Descripción |
|---|---|
| Zona | `LocationID` y nombre |
| Segmento | perfil de `MOV-03` |
| Demanda reciente | pickups observados hasta el corte |
| Baseline | demanda esperada por regla simple |
| Pronóstico | pickups e intervalo |
| Exceso esperado | pronóstico menos baseline |
| Conectividad | grado, frecuencia o centralidad documentada |
| Prioridad | regla combinada y reproducible |
| Limitación | cobertura, error o zona desconocida |

La recomendación puede seleccionar las primeras $k$ zonas para atención. Debe mostrar cómo cambia si varía el horizonte o el peso de conectividad.

## 3.7. Criterios de aprobación

- unidad zona-franja consistente en toda la cadena;
- mapa, grafo, segmentación y pronóstico usan el mismo lookup;
- aristas poseen soporte mínimo y costos interpretables;
- clustering se valida más allá de una métrica única;
- pronóstico respeta orden temporal y baseline;
- la prioridad no se presenta como despacho óptimo;
- se reconoce que TLC no representa toda la movilidad.

## 3.8. Extensiones opcionales

Clima, eventos, población, más meses, otros operadores o red vial OpenStreetMap. Para rutas calle por calle, la red vial deja de ser opcional y debe incorporarse como fuente formal.

---

# Laboratorio integrador 4. Clasificación temática de reclamos y revisión humana

**Etiqueta:** `[LAB · RECLAMOS]`

**EMO integradas:** `REC-01`, `REC-02`, `REC-03` y `REC-04`.

## 4.1. Fuente y alcance

Se utiliza **CFPB Consumer Complaint Database**. La referencia de campos y los enlaces oficiales se encuentran en el Apéndice D.

La unidad es un reclamo publicado con narrativa consentida. El objetivo obligatorio es clasificar `Product` a partir de `Consumer complaint narrative` y decidir si la sugerencia puede utilizarse para enrutamiento o debe revisarse manualmente.

El laboratorio no estima daño, urgencia, fraude ni mérito legal. Tampoco genera asesoramiento financiero o una respuesta automática al consumidor.

## 4.2. Variables disponibles

### 4.2.1. Variables utilizadas

| Campo | Uso |
|---|---|
| `Complaint ID` | Clave y trazabilidad; nunca predictor. |
| `Date received` | Corte temporal y análisis de deriva. |
| `Product` | Etiqueta obligatoria. |
| `Consumer complaint narrative` | Texto de entrada. |
| `Submitted via` | Contexto opcional disponible al ingreso. |
| `State` | Contexto opcional para análisis, con cautela. |

`Sub-product`, `Issue` y `Sub-issue` pueden utilizarse como objetivos alternativos solo si el equipo docente fija una tarea común. No se incorporan como entrada al predecir `Product` porque contienen información temática directa.

### 4.2.2. Campos excluidos del modelo obligatorio

| Campo | Motivo |
|---|---|
| `Company public response` | Respuesta posterior. |
| `Date sent to company` | Evento posterior al ingreso. |
| `Company response to consumer` | Resultado posterior. |
| `Timely response?` | Resultado posterior; no mide urgencia inicial. |
| `Company` | Puede actuar como atajo fuerte hacia el producto. |
| `ZIP code` | Privacidad, granularidad irregular y posible proxy. |
| `Tags` | Puede representar grupos sensibles. |

El equipo puede estudiar estos campos para detectar sesgo o fuga, pero no utilizarlos como atributos en el pipeline obligatorio.

### 4.2.3. Derivados permitidos

- tokens y n-gramas de la narrativa;
- TF-IDF ajustado solo con entrenamiento;
- longitud del texto;
- año, mes o día desde `Date received`;
- grupo de duplicado exacto o aproximado;
- probabilidad, margen o confianza del modelo;
- indicador de revisión derivado de umbral validado.

## 4.3. Selección del corpus

El equipo docente congela una fecha y define clases. Para asegurar viabilidad se recomienda una de estas opciones:

1. productos con soporte mínimo común, agrupando los restantes en `Other` mediante una regla fijada en entrenamiento;
2. un conjunto explícito de productos distribuido a toda la cohorte;
3. clasificación de `Issue` dentro de un producto con soporte suficiente.

Los estudiantes no deben elegir clases después de observar la prueba. La cantidad de narrativas excluidas por falta de consentimiento o texto debe informarse.

Los fragmentos presentados en informes deben revisarse y minimizarse. Aunque CFPB aplica medidas de supresión de información personal, la entrega no debe reproducir narrativas completas.

## 4.4. Objetivo y decisión simulada

### 4.4.1. Objetivo

Estimar la categoría temática `Product` de una narrativa publicada. La salida es una probabilidad o puntaje por clase.

### 4.4.2. Decisión

La decisión tiene dos niveles:

- **enrutar:** sugerir una cola temática cuando la confianza supera el umbral;
- **revisar:** derivar a una persona cuando la confianza es baja, hay empate entre clases o la clase tiene alto costo de error.

“Priorizar” significa priorizar revisión del sistema, no afirmar que el reclamo es más urgente o grave.

### 4.4.3. Baselines

- clase mayoritaria;
- clasificador simple con unigramas y configuración fija;
- opcionalmente, regla de palabras clave definida antes de prueba.

## 4.5. Secuencia de actividades

### Fase A. Corpus, `REC-01`

Tareas:

1. congelar fecha y versión;
2. seleccionar narrativas no vacías y etiqueta válida;
3. conservar `Complaint ID` y fecha;
4. armonizar categorías mediante un mapa común;
5. detectar duplicados exactos y plantillas;
6. asignar grupo de partición;
7. producir diccionario y reporte de exclusiones.

**Entrega:** corpus analítico y diagrama de procedencia.

**Control:** la tabla contiene texto inicial y etiqueta, no respuestas posteriores.

### Fase B. Protocolo, `REC-02`

La división es temporal. El periodo más reciente se reserva como prueba. Duplicados y plantillas permanecen en un solo conjunto.

El protocolo define:

- baseline;
- macro-F1 como métrica principal sugerida;
- accuracy y F1 por clase como auxiliares;
- matriz de confusión;
- costo de enrutamiento incorrecto;
- regla de selección de modelos;
- conjunto de prueba usado una única vez.

**Entrega:** ficha experimental anterior al entrenamiento.

### Fase C. Representación, `REC-03`

Construir TF-IDF dentro de un pipeline. Comparar al menos:

- unigramas;
- unigramas y bigramas, o dos decisiones de normalización.

Para cada variante informar vocabulario, dimensionalidad, términos de alto peso y rendimiento de validación con el mismo clasificador.

**Control:** no ajustar vocabulario, frecuencia ni selección con validación o prueba.

### Fase D. Clasificación y errores, `REC-04`

Comparar baseline con al menos un modelo lineal apropiado para texto. Analizar:

- matriz de confusión;
- productos con mayor error;
- efecto de longitud y canal;
- cambio temporal de vocabulario;
- falsos enrutamientos de alto costo;
- casos de baja confianza.

Definir el umbral de revisión en validación. Si las probabilidades no están calibradas, utilizar margen o calibrar sin tocar prueba.

## 4.6. Integración y producto final

El prototipo recibe una narrativa y produce:

| Campo | Descripción |
|---|---|
| Producto sugerido | Clase con mayor puntaje |
| Confianza | Probabilidad calibrada o margen documentado |
| Segunda opción | Clase alternativa útil para revisión |
| Acción | `enrutar` o `revisar` |
| Explicación limitada | Términos o evidencia del modelo, sin afirmar causalidad |
| Advertencia | Cobertura, lenguaje o clase fuera de alcance |

El producto final incluye informe de desempeño, análisis cualitativo de errores y ficha de uso. Debe existir una salida `fuera de alcance` o revisión cuando el texto no corresponde a las clases conocidas.

## 4.7. Criterios de aprobación

- corpus trazable y limitado a narrativas consentidas;
- campos posteriores excluidos;
- partición temporal y duplicados controlados;
- TF-IDF ajustado solo con entrenamiento;
- baseline y macro-F1 informados;
- errores analizados por clase y periodo;
- umbral de revisión definido con validación;
- no se atribuye urgencia, daño ni decisión financiera.

## 4.8. Extensiones opcionales

Clasificación jerárquica, embeddings, recuperación de casos similares o análisis de deriva. La generación automática de respuestas queda fuera del mínimo y requeriría controles adicionales de fuentes y supervisión.

---

# Laboratorio integrador 3. Clasificación visual en PlantVillage

**Etiqueta:** `[LAB · SANIDAD VEGETAL]`

**EMO integradas:** `VEG-01`, `VEG-02`, `VEG-03` y `VEG-04`.

## 5.1. Fuente y alcance

Se utiliza **PlantVillage**, configuración `color`, disponible en Hugging Face y documentada en el Apéndice D.

La unidad es una imagen asociada con una hoja física mediante `leaf_id`. El laboratorio clasifica combinaciones cultivo-condición dentro de imágenes semejantes a PlantVillage.

Para hacer viable el entrenamiento, el mínimo trabaja con un cultivo que tenga al menos tres clases, fijado por el equipo docente. Papa, manzana, maíz, uva o tomate son opciones. La tarea de 38 clases es una extensión.

El producto no es un diagnóstico agronómico de campo, no estima severidad y no recomienda tratamiento.

## 5.2. Variables disponibles

| Variable | Uso |
|---|---|
| `image` | Entrada visual. |
| `image_path` | Trazabilidad; se excluye como predictor porque puede contener la clase. |
| `label` | Objetivo cultivo-condición. |
| `crop` | Selección del subconjunto. |
| `disease` | Interpretación de la etiqueta. |
| `leaf_id` | Agrupación obligatoria de particiones. |

No existen variables de región, lote, clima, variedad, severidad, tratamiento ni condiciones de campo.

### 5.2.1. Configuraciones derivadas

`grayscale` y `segmented` son representaciones de las mismas hojas. No deben combinarse con `color` como observaciones independientes. Una comparación opcional debe alinear por `leaf_id` y mantener las mismas particiones.

### 5.2.2. Transformaciones permitidas

- redimensionamiento;
- conversión a tensor y normalización;
- rotaciones moderadas, reflejos y recortes justificados;
- variaciones de color que no destruyan la señal;
- aumento únicamente durante entrenamiento.

Validación y prueba reciben transformaciones deterministas. No se permite elegir transformaciones mirando errores de prueba.

## 5.3. Particiones

1. conservar la prueba oficial intacta;
2. seleccionar el cultivo dentro de cada split;
3. dividir el entrenamiento oficial en entrenamiento y validación por `leaf_id`;
4. verificar intersecciones vacías de `leaf_id`;
5. registrar cantidad de imágenes y hojas por clase;
6. usar prueba una vez después de fijar modelo y umbral.

Si la distribución disponible no expone `leaf_id`, debe recuperarse desde el mapa oficial. Una partición aleatoria por imagen no es aceptable.

## 5.4. Objetivo y decisión simulada

### 5.4.1. Objetivo

Estimar la clase PlantVillage de una imagen dentro del cultivo seleccionado.

### 5.4.2. Decisión

- **clasificar:** mostrar clase sugerida cuando la confianza validada es suficiente;
- **revisar:** abstenerse cuando la confianza es baja o la imagen no se asemeja a las condiciones del dataset.

La revisión debe recomendar consulta experta, no una acción fitosanitaria específica.

### 5.4.3. Baselines

- clase mayoritaria;
- modelo visual pequeño o red superficial;
- CNN específica como modelo intermedio;
- transferencia como candidato final.

## 5.5. Secuencia de actividades

### Fase A. Auditoría y partición, `VEG-01`

Tareas:

1. seleccionar cultivo y clases;
2. verificar canales, dimensiones y archivos corruptos;
3. calcular distribución por imagen y `leaf_id`;
4. detectar hashes duplicados o casi duplicados;
5. crear validación agrupada;
6. producir galería de control;
7. guardar manifiesto de particiones.

**Control:** ninguna hoja física aparece en dos conjuntos.

### Fase B. Baseline y entrenamiento, `VEG-02`

Implementar clase mayoritaria y una red pequeña. Registrar por época:

- pérdida de entrenamiento y validación;
- accuracy y macro-F1;
- tasa de aprendizaje;
- tiempo y mejor época.

Comparar dos configuraciones de regularización, tasa o early stopping, manteniendo constantes los demás factores.

**Control:** el diagnóstico se basa en curvas, no solo en la mejor métrica.

### Fase C. CNN y errores, `VEG-03`

Entrenar una CNN sencilla sobre las mismas particiones. Comparar con baseline y analizar:

- matriz de confusión;
- precisión, recall y F1 por clase;
- clases visualmente próximas;
- imágenes mal encuadradas o de baja calidad;
- galería de aciertos y errores de validación.

La prueba oficial no se utiliza para modificar la arquitectura.

### Fase D. Transferencia y abstención, `VEG-04`

Comparar:

1. extracción de características con base congelada;
2. ajuste fino parcial o completo con tasa reducida.

El aumento se aplica solo en entrenamiento. La selección considera desempeño, estabilidad, tiempo y tamaño.

Definir umbral de abstención en validación. Evaluar cobertura frente a error: al aumentar el umbral se clasifican menos imágenes, pero debería mejorar el desempeño de las aceptadas.

## 5.6. Integración y producto final

El prototipo devuelve:

| Campo | Descripción |
|---|---|
| Cultivo configurado | Alcance del modelo |
| Clase sugerida | Etiqueta PlantVillage |
| Confianza | Probabilidad o puntaje calibrado/documentado |
| Acción | `clasificar` o `revisar` |
| Evidencia visual | Imagen y, opcionalmente, explicación visual |
| Advertencia | “Válido solo para imágenes semejantes a PlantVillage” |

El informe compara clase mayoritaria, red pequeña, CNN y transferencia. La prueba oficial se evalúa una vez y se acompaña con métricas por clase y galería final.

## 5.7. Criterios de aprobación

- configuración y versión registradas;
- particiones sin intersección de `leaf_id`;
- baseline implementado;
- curvas y diagnóstico reproducibles;
- CNN comparada con el baseline;
- transferencia evaluada con el mismo protocolo;
- métricas por clase y análisis visual;
- abstención derivada de validación;
- límites de campo y severidad explícitos.

## 5.8. Extensiones opcionales

Clasificación de 38 clases, tarea jerárquica, comparación entre configuraciones, explicaciones visuales o validación externa de campo. Una validación externa necesita fuente, licencia, etiquetas y protocolo propios.

---

# 6. Entregables comunes

Cada laboratorio entrega:

1. manifiesto de datos y entorno;
2. diccionario de variables directas y derivadas;
3. pipeline reproducible;
4. notebook o informe de auditoría;
5. baseline;
6. experimentos y registro de selección;
7. modelo o algoritmo final;
8. análisis de errores y sensibilidad;
9. producto de decisión o prototipo;
10. ficha de límites y defensa individual.

Los artefactos grandes se almacenan fuera de Git cuando corresponde, pero el repositorio debe contener instrucciones y verificaciones para obtenerlos.

# 7. Rúbrica común

## 7.1. Reproducibilidad y trazabilidad

Se aprueba cuando la fuente, versión, particiones, transformaciones y resultados pueden reconstruirse. Modificar datos originales o depender de pasos manuales no documentados es insuficiente.

## 7.2. Corrección metodológica

Se aprueba cuando unidad, objetivo, partición, baseline, métricas y pipeline son coherentes. La fuga de información, la mezcla de grupos o el uso reiterado de prueba impiden aprobar aunque la métrica sea alta.

## 7.3. Uso de variables disponibles

Se aprueba cuando toda entrada aparece en el contrato del laboratorio o se deriva mediante una regla reproducible. Una variable externa no distribuida no puede ser necesaria para la solución.

## 7.4. Interpretación y decisión

Se aprueba cuando el resultado se convierte en una acción simulada explícita y proporcional a la evidencia. No se aceptan conclusiones causales o diagnósticas que el dataset no permite.

## 7.5. Incertidumbre, sesgos y límites

Se aprueba cuando se analizan cobertura, faltantes, desbalance, selección, cambio temporal y condiciones fuera de alcance. Debe existir abstención o revisión cuando corresponda.

## 7.6. Comunicación y defensa

Se aprueba cuando el producto diferencia dato, inferencia y recomendación; utiliza gráficos y métricas trazables; y cada estudiante explica una decisión, un error y un límite.

# 8. Controles finales de viabilidad

| Laboratorio | Entrada directa | Derivados suficientes | Decisión mínima | Afirmación fuera de alcance |
|---|---|---|---|---|
| Agua | Muestras químicas y microbiológicas | Evento, historia y riesgo | Revisar/remuestrear | Potabilidad, fugas o tratamiento |
| Movilidad | Viajes, tiempos y zonas | Demanda, OD, perfiles y serie | Priorizar zonas | Demanda total o despacho óptimo |
| Reclamos | Narrativa, producto y fecha | TF-IDF, confianza y revisión | Enrutar/revisar | Urgencia, daño o asesoramiento |
| Vegetales | Imagen, clase y `leaf_id` | Tensores, confianza y abstención | Clasificar/revisar | Diagnóstico de campo o severidad |

Si un equipo descubre que su objetivo requiere una variable fuera de esta tabla, debe reformular el objetivo o formalizar la fuente como extensión. No se permite simular una variable inexistente y presentarla como evidencia observada.
