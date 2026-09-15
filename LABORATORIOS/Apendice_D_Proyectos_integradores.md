# Apéndice D. Proyectos integradores y contratos de datos

## D.0. Propósito del apéndice

Este apéndice convierte los cuatro casos transversales del libro en actividades realizables con fuentes concretas. Su función principal es evitar una situación frecuente en cursos de Ciencia de Datos e Inteligencia Artificial: formular una consigna atractiva que el dataset no puede responder.

Cada caso se trata como un **contrato de datos y evaluación**. El contrato establece:

- qué fuente debe utilizarse y cómo fijar su versión;
- qué representa una observación;
- qué variables existen realmente;
- qué variables pueden derivarse sin incorporar información futura;
- qué objetivo es medible;
- qué actividades son obligatorias y cuáles son extensiones;
- qué afirmaciones quedan fuera del alcance;
- qué evidencia demuestra que el laboratorio fue completado.

La regla general es:

> Ninguna actividad obligatoria puede depender de una variable que no esté en la fuente principal o en una fuente auxiliar declarada como obligatoria.

Una variable obtenida de una fuente opcional puede mejorar o ampliar un análisis, pero no puede convertirse en requisito de aprobación. Del mismo modo, una etiqueta construida con información posterior a la decisión no puede utilizarse como entrada predictiva.

## D.0.1. Convenciones de disponibilidad

Las tablas utilizan tres niveles:

| Nivel | Significado |
|---|---|
| **Directa** | La variable está incluida en el dataset y puede leerse sin otra fuente. |
| **Derivada** | Puede calcularse exclusivamente a partir de variables directas, respetando el tiempo de decisión. |
| **Auxiliar** | Requiere una fuente adicional identificada en este apéndice. |

Si una variable no aparece en uno de esos niveles, no debe asumirse disponible.

## D.0.2. Congelamiento de versiones

Las fuentes abiertas cambian. Antes de comenzar una EMO, el equipo docente debe publicar un manifiesto con:

- URL o identificador oficial;
- fecha de descarga;
- archivos utilizados;
- tamaño y suma de comprobación;
- esquema observado;
- periodo incluido;
- reglas de inclusión;
- particiones oficiales o semillas cuando correspondan.

Todos los estudiantes deben trabajar sobre la misma versión mínima. Se permite una versión posterior únicamente como extensión, nunca como sustitución silenciosa.

## D.0.3. Matriz general de viabilidad

| Caso | Fuente principal | Unidad mínima | Objetivo obligatorio realizable |
|---|---|---|---|
| Movilidad | NYC TLC Yellow Taxi | Viaje; luego zona-franja | Demanda, grafo OD, segmentación y pronóstico corto |
| Agua | NYC DEP Distribution Monitoring | Muestra de sitio y fecha | Calidad, detección microbiológica y prioridad de revisión |
| Reclamos | CFPB Consumer Complaint Database | Reclamo con narrativa publicada | Clasificación temática y derivación por confianza |
| Sanidad vegetal | PlantVillage, configuración color | Imagen con `leaf_id` y clase | Clasificación visual en condiciones PlantVillage |


---

## D.1. Movilidad urbana y transporte

### D.1.1. Fuente abierta, versión y archivos obligatorios

La fuente principal es **NYC Taxi and Limousine Commission, Yellow Taxi Trip Records**:

- página oficial: <https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page>;
- diccionario oficial: enlazado como *Yellow Trips Data Dictionary* en la página de TLC;
- formato: Parquet mensual;
- publicación: mensual, con advertencia de posibles cambios de esquema;
- limitación declarada: los registros son aportados por proveedores tecnológicos y TLC no garantiza exactitud o completitud total.

La instantánea disponible en el repositorio contiene:

| Archivo | Filas verificadas | Periodo nominal |
|---|---:|---|
| `DATASETS/yellow_tripdata_2026-02.parquet` | 3.399.866 | febrero de 2026 |
| `DATASETS/yellow_tripdata_2026-03.parquet` | 3.952.451 | marzo de 2026 |
| `DATASETS/yellow_tripdata_2026-04.parquet` | 3.831.240 | abril de 2026 |

Los tres archivos comparten el mismo esquema de veinte columnas. Para mapas y nombres de zonas son obligatorias dos fuentes auxiliares oficiales:

- Taxi Zone Lookup Table: <https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv>;
- Taxi Zone Shapefile: <https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip>.

El lookup aporta `LocationID`, `Borough`, `Zone` y `service_zone`. El shapefile aporta la geometría de las zonas. Las actividades no requieren clima, población ni red vial externa.

### D.1.2. Unidad de análisis y niveles derivados

La unidad original es un **viaje reportado**. La clave no está publicada como identificador único; por tanto, no debe inventarse unicidad a partir de una sola columna. Para controles de duplicación se puede utilizar una clave compuesta aproximada, pero los casos coincidentes deben tratarse como posibles duplicados, no como duplicados confirmados.

Las actividades utilizan tres niveles:

| Nivel | Definición | Actividades |
|---|---|---|
| Viaje | Una fila del Parquet después de validación | Auditoría y derivación de duración |
| Zona-franja | `PULocationID` agregado por intervalo | `MOV-01`, `MOV-03`, `MOV-04` |
| Grafo OD | Nodos de zona y aristas origen-destino observadas | `MOV-02` |

La variable de demanda obligatoria es la **cantidad de pickups válidos por zona y franja**. No representa toda la demanda de transporte de Nueva York: representa viajes de taxi amarillo reportados en la fuente.

### D.1.3. Diccionario de variables directas

| Variable | Tipo observado | Significado y uso permitido |
|---|---|---|
| `VendorID` | Entero | Proveedor que envió el registro. Útil para perfil de cobertura; no representa conductor. |
| `tpep_pickup_datetime` | Fecha-hora | Inicio reportado. Base para fecha, hora, día y orden temporal. |
| `tpep_dropoff_datetime` | Fecha-hora | Fin reportado. Permite derivar duración, siempre posterior al inicio. |
| `passenger_count` | Entero con faltantes posibles | Conteo reportado por el conductor/proveedor. No usar como medida exacta de ocupación sin auditoría. |
| `trip_distance` | Real | Distancia reportada por taxímetro, en millas según diccionario TLC. |
| `RatecodeID` | Entero categórico | Código de tarifa final. Puede reflejar información conocida al final del viaje. |
| `store_and_fwd_flag` | Texto categórico | Indica almacenamiento previo al envío por falta de conexión. Útil para calidad de captura. |
| `PULocationID` | Entero | Zona TLC de ascenso. Variable espacial principal para demanda. |
| `DOLocationID` | Entero | Zona TLC de descenso. Permite construir pares OD. |
| `payment_type` | Entero categórico | Forma de pago al finalizar. No debe usarse para pronosticar demanda antes del viaje. |
| `fare_amount` | Real | Tarifa calculada por taxímetro antes de extras. |
| `extra` | Real | Extras y recargos agregados. |
| `mta_tax` | Real | Impuesto MTA cuando corresponde. |
| `tip_amount` | Real | Propina registrada; para efectivo suele no reflejar la propina real. |
| `tolls_amount` | Real | Peajes cobrados. |
| `improvement_surcharge` | Real | Recargo de mejora. |
| `total_amount` | Real | Total cobrado, sin interpretar automáticamente como suma perfecta antes de validar reglas. |
| `congestion_surcharge` | Real | Recargo de congestión. |
| `Airport_fee` | Real | Tarifa de aeropuerto cuando corresponde. |
| `cbd_congestion_fee` | Real | Cargo de congestión CBD incorporado en datos desde 2025. |

#### Variables derivadas permitidas

| Variable derivada | Fórmula o regla | Restricción |
|---|---|---|
| `duracion_min` | diferencia entre drop-off y pickup | Debe ser positiva y plausible. |
| `fecha_pickup` | fecha del pickup | Usar calendario local documentado. |
| `hora`, `dia_semana`, `mes` | componentes del pickup | Disponibles antes o al inicio del viaje. |
| `franja_horaria` | intervalos fijos, por ejemplo una hora | Los mismos cortes para todos los meses. |
| `demanda_zona_franja` | conteo de pickups válidos | Informar cobertura y filtros. |
| `viajes_od` | conteo por `PULocationID`, `DOLocationID` | Excluir o documentar zonas desconocidas. |
| `tiempo_od_mediano` | mediana de duración por par OD | Solo para aristas con muestra mínima. |
| `distancia_od_mediana` | mediana de distancia por par OD | No equivale a distancia vial exacta. |
| `velocidad_mph` | distancia dividida por duración | Solo después de validar ambas variables. |
| `borough`, `zone` | unión con lookup | Fuente auxiliar obligatoria. |
| `geometria_zona` | unión con shapefile | Para mapas; validar sistema de referencia. |

Los cargos, tipo de pago y hora de descenso no son entradas válidas para pronosticar pickups futuros. Pueden utilizarse en análisis retrospectivos de viaje, siempre que la pregunta lo permita.

#### Reglas mínimas de calidad

Antes de cualquier EMO se aplican, al menos, estas reglas:

1. pickup dentro del periodo declarado;
2. drop-off posterior al pickup;
3. duración positiva y sometida a un límite plausible documentado;
4. distancia no negativa y revisada frente a duración;
5. `PULocationID` y `DOLocationID` existentes en el lookup o marcados como desconocidos;
6. conteo de filas y faltantes por archivo y proveedor;
7. control de claves compuestas repetidas sin eliminación automática;
8. misma zona horaria y mismos cortes para todos los meses.

No se recomienda eliminar viajes usando un único umbral global sin analizar aeropuerto, tarifas especiales y trayectos largos. Toda exclusión debe acompañarse de conteo y sensibilidad.

### D.1.4. Actividades `MOV-01` a `MOV-04`

#### `MOV-01`: diagnóstico geotemporal

**Pregunta realizable:** ¿cómo se distribuyen los pickups de taxi amarillo por zona TLC, día y franja durante la instantánea?

**Variables requeridas:** `tpep_pickup_datetime`, `PULocationID`, lookup y geometría.

**Producto mínimo:**

- tabla zona-franja con conteos;
- mapa de demanda con zonas sin datos visibles;
- serie o mapa de calor temporal;
- dos patrones y una anomalía con evidencia;
- advertencia de que la fuente no representa toda la movilidad.

**No exigir:** población residente, clima o estimación de demanda no observada.

#### `MOV-02`: grafo de movilidad observado

**Pregunta realizable:** ¿qué caminos entre zonas pueden construirse sobre la red dirigida de conexiones OD observadas y cómo cambia la búsqueda según el costo?

**Variables requeridas:** `PULocationID`, `DOLocationID`, pickup, drop-off y `trip_distance`.

**Construcción:** cada zona es un nodo; existe arista dirigida $i\rightarrow j$ cuando hay una cantidad mínima de viajes válidos. El costo puede ser duración mediana, distancia mediana o su combinación. La cantidad mínima evita aristas sostenidas por un único viaje.

**Comparación obligatoria:** costo uniforme y A* sobre el mismo par origen-destino. Una heurística admisible puede usar distancia entre centroides de zonas si se dispone de geometría y el costo es distancia. Si el costo es tiempo, una distancia dividida por una velocidad máxima documentada puede actuar como cota inferior.

**Límite:** el resultado es una ruta en una **red de zonas conectadas por viajes observados**. No es una ruta vial calle por calle ni una recomendación de conducción. Para eso sería obligatoria una red vial externa, que no forma parte del caso mínimo.

#### `MOV-03`: segmentación de zonas

**Pregunta realizable:** ¿qué zonas muestran perfiles semejantes de pickups dentro del periodo?

**Variables derivadas mínimas por zona:**

- pickups medios por hora;
- proporción en mañana, tarde, noche y madrugada;
- proporción de fin de semana;
- variabilidad entre días;
- cantidad de destinos distintos o entropía OD;
- duración o distancia mediana de viajes originados.

**Producto mínimo:** comparación de dos estrategias de agrupamiento, escalado dentro del pipeline, elección justificada de hiperparámetros, estabilidad y ficha de cada segmento.

**Límite:** los grupos son perfiles algorítmicos de viajes de taxi amarillo, no categorías socioeconómicas de barrios.

#### `MOV-04`: pronóstico de demanda

**Pregunta realizable:** ¿cuántos pickups se observarán en la siguiente hora o día para una zona o segmento?

**Variables requeridas:** pickup y zona. Se construye una serie regular con ceros explícitos cuando existe cobertura y no hubo viajes; los periodos de datos faltantes no deben rellenarse como demanda cero.

**Horizonte obligatorio:** corto, compatible con tres meses de datos: una hora, varias horas o un día. No debe exigirse estacionalidad anual.

**Modelos mínimos:** baseline de último valor o estacional; ARIMA/SARIMA u otra alternativa; validación walk-forward; métricas por horizonte.

**Límite:** el pronóstico describe pickups reportados. La caída de registros puede ser demanda, cobertura o cambio del servicio.

### D.1.5. Guía del laboratorio de movilidad

**Decisión común:** proponer una regla de posicionamiento o priorización de zonas para el siguiente horizonte, utilizando exclusivamente evidencia del dataset.

**Cadena mínima:**

1. construir tabla zona-franja (`MOV-01`);
2. construir grafo OD y evaluar un trayecto (`MOV-02`);
3. segmentar zonas con perfiles comparables (`MOV-03`);
4. pronosticar pickups para una zona o segmento (`MOV-04`);
5. recomendar dónde priorizar capacidad, declarando que no se observa oferta disponible ni demanda insatisfecha.

**Regla realizable de ejemplo:** priorizar zonas con pronóstico por encima de su baseline, ponderado por conectividad del grafo. Esta es una regla didáctica de prioridad, no una optimización completa de flota porque el dataset no contiene ubicación y disponibilidad de vehículos libres.

**Criterio de cumplimiento:** todos los componentes usan la misma definición de zona, franja, filtros y periodo. La recomendación puede reconstruirse desde los productos de las cuatro EMO.

#### Extensiones opcionales

- clima por estación y hora;
- calendario de eventos;
- población o empleo para tasas contextuales;
- red vial OpenStreetMap para rutas calle por calle;
- datos de otros modos u operadores;
- más meses para estacionalidad anual.

Ninguna extensión forma parte del mínimo obligatorio hasta que el equipo docente distribuya la fuente, licencia, diccionario y regla de integración.

---

## D.2. Calidad y gestión del agua

### D.2.1. Fuente abierta y versión

La fuente principal es **NYC Department of Environmental Protection, Drinking Water Quality Distribution Monitoring Data**:

- identificador NYC Open Data: `bkwf-xfky`;
- metadatos: <https://data.cityofnewyork.us/api/views/bkwf-xfky>;
- API de datos: <https://data.cityofnewyork.us/resource/bkwf-xfky.json>;
- actualización declarada: mensual;
- procedencia: oficial, NYC DEP;
- volumen verificado en metadatos al preparar este apéndice: 170.113 muestras, desde 2015 hasta 2026;
- documentación auxiliar: diccionario y catálogo de sitios adjuntos en la ficha oficial.

El dataset resume cloro residual libre, turbidez, fluoruro, coliformes y *E. coli* en sitios de la red de distribución. **No contiene presión, caudal, consumo, fugas, coordenadas directas ni reclamos.** Las actividades obligatorias se reformulan en términos de calidad y prioridad de revisión o remuestreo.

### D.2.2. Unidad de análisis y contexto operativo

Cada fila representa una **muestra tomada en un sitio, fecha y hora**, con un identificador `Sample Number`. El objetivo didáctico es evaluar condiciones registradas y priorizar revisión de muestras o sitios. No se pretende certificar potabilidad completa ni sustituir protocolos regulatorios.

La clase de muestra distingue `Compliance`, `Operational` y variantes de remuestreo. Como un remuestreo puede ocurrir después de un hallazgo, `sample_class` puede contener información sobre el proceso posterior. Debe utilizarse para describir el muestreo y analizar sesgo, no como entrada para predecir retrospectivamente la detección inicial sin reconstruir la secuencia.

### D.2.3. Diccionario de variables directas

| Variable API | Tipo publicado | Uso y observaciones |
|---|---|---|
| `sample_number` | Número | Identificador de muestra; debe tratarse como clave, no magnitud. |
| `sample_date` | Fecha | Día de toma. Permite orden, mes, estación y corte temporal. |
| `sample_time` | Texto | Hora de toma; presenta formatos heterogéneos y valores textuales como `NULL`. |
| `sample_site` | Texto | Código de sitio. No es coordenada ni barrio por sí mismo. |
| `sample_class` | Texto | Tipo de muestra: cumplimiento, operacional o remuestreo. |
| `residual_free_chlorine_mg_l` | Texto | Cloro residual libre en mg/L; requiere conversión y tratamiento de códigos especiales. |
| `turbidity_ntu` | Texto | Turbidez en NTU; requiere conversión numérica y validación. |
| `fluoride_mg_l` | Texto | Fluoruro en mg/L; gran cantidad de ausencias porque no se registra en toda muestra. |
| `coliform_quanti_tray_mpn_100ml` | Texto | Coliformes MPN/100 mL; contiene `<1`, valores numéricos y `>200.5`. Es dato censurado. |
| `e_coli_quanti_tray_mpn_100ml` | Texto | *E. coli* MPN/100 mL; casi todos los registros son `<1`, con muy pocos positivos. |

#### Particularidades de calidad que deben convertirse en actividad

Este dataset fue elegido porque los problemas de calidad son reales y documentables:

- las mediciones químicas y microbiológicas están almacenadas como texto;
- `<1` representa valor por debajo del límite, no cero exacto;
- `>200.5` representa censura superior, no 200.5 exacto;
- valores negativos como `-9` o `-9.99` deben contrastarse con el diccionario como posibles códigos de ausencia;
- fluoruro es medido solo en un subconjunto, por lo que sus faltantes no deben imputarse automáticamente;
- `sample_time` presenta formatos diferentes;
- sitios y clases cambian en frecuencia a lo largo del tiempo;
- las detecciones microbiológicas son raras y producen fuerte desbalance.

El tratamiento mínimo conserva tres columnas para resultados censurados: valor original, estado (`inferior`, `observado`, `superior`, `faltante/código`) y valor numérico utilizado en un análisis específico. Sustituir `<1` por cero puede ser razonable para una visualización didáctica si se declara, pero no debe presentarse como medición exacta.

#### Variables derivadas permitidas

| Variable | Derivación | Uso permitido |
|---|---|---|
| `fecha_hora` | combinación validada de fecha y hora | Orden temporal y análisis por franja. |
| `anio`, `mes`, `estacion` | desde fecha | Comparación temporal. |
| `coliforme_detectado` | resultado distinto de `<1`, excluyendo códigos inválidos | Evento binario didáctico principal. |
| `ecoli_detectado` | resultado válido distinto de `<1` | Solo descriptivo o extensión por extrema rareza. |
| `cloro_numerico` | conversión con códigos separados | Evidencia química. |
| `turbidez_numerica` | conversión con códigos separados | Evidencia física. |
| `historial_sitio` | medidas anteriores al instante de interés | Priorización sin fuga temporal. |
| `dias_desde_ultima_muestra` | diferencia respecto de muestra anterior del sitio | Cobertura y prioridad. |
| `es_remuestreo` | categoría de `sample_class` | Descripción del proceso; uso predictivo restringido. |

No debe construirse una etiqueta de “agua potable” a partir de este dataset aislado. Tampoco debe usarse el resultado microbiológico de la misma muestra como entrada para predecirse a sí mismo.

### D.2.4. Actividades `AGUA-01` a `AGUA-04`

#### `AGUA-01`: formular problema y decisión

**Decisión realizable:** priorizar sitios o muestras para revisión técnica o muestreo de seguimiento dentro de una capacidad limitada.

**Objetivo medible:** detectar o estimar riesgo de `coliforme_detectado`, sin afirmar diagnóstico sanitario completo.

**Ficha mínima:** unidad muestra o sitio-periodo, usuario hipotético, horizonte, capacidad, evento, baseline y costo de omitir/revisar.

**Baseline sugerido:** frecuencia histórica del sitio calculada solo con observaciones anteriores; si el sitio no tiene historia suficiente, frecuencia global de entrenamiento.

#### `AGUA-02`: auditar y limpiar

**Variables obligatorias:** fecha, hora, sitio, clase, cloro, turbidez, coliformes y *E. coli*. Fluoruro puede describirse sin imputación obligatoria.

**Tareas mínimas:**

- validar unicidad de `sample_number`;
- unificar fecha-hora;
- separar censura de microbiología;
- identificar códigos negativos;
- convertir cloro y turbidez con trazabilidad;
- comparar faltantes por clase y periodo;
- conservar datos originales y tabla de reglas.

**No exigir:** imputación de fluoruro ni eliminación automática de detecciones raras.

#### `AGUA-03`: explorar patrones y anomalías

**Preguntas realizables:** ¿cómo varían cloro y turbidez por sitio, mes y clase?, ¿dónde aparecen detecciones de coliformes?, ¿qué cambios pueden ser de medición o cobertura?

**Producto mínimo:** distribuciones robustas, serie temporal, comparación por sitio o clase y tres hallazgos. Toda tasa microbiológica informa denominador y distingue muestras iniciales de remuestreos.

**Límite:** una asociación entre turbidez y detección no demuestra mecanismo causal ni incumplimiento normativo.

#### `AGUA-04`: actualizar riesgo y priorizar

**Evento recomendado:** `coliforme_detectado`. *E. coli* no es objetivo obligatorio porque los positivos publicados son demasiado escasos para una actividad estable.

**Previa:** tasa histórica en entrenamiento, global o jerárquica por sitio/clase.

**Evidencias posibles:** turbidez en intervalos, cloro en intervalos, estación, historial previo del sitio y tiempo desde última muestra. Cada verosimilitud se estima en datos de entrenamiento.

**Dependencia:** cloro y turbidez pueden depender de sitio y proceso; no multiplicar verosimilitudes como independientes sin analizarlo. Para el mínimo se puede usar una sola evidencia o una tabla conjunta discretizada con soporte suficiente.

**Decisión:** priorizar revisión/remuestreo cuando la pérdida esperada de omitir supera el costo de revisar, o seleccionar las primeras $k$ muestras bajo capacidad.

### D.2.5. Guía del laboratorio de agua

**Propósito ajustado al dataset:** construir una cadena reproducible que transforme mediciones publicadas en un indicador didáctico de riesgo de detección de coliformes y una prioridad de revisión.

**Cadena mínima:**

1. formular evento, usuario y capacidad (`AGUA-01`);
2. limpiar texto, censura y códigos (`AGUA-02`);
3. describir cobertura, variables y detecciones (`AGUA-03`);
4. estimar previa, actualizar con evidencia y aplicar costos (`AGUA-04`);
5. comunicar ranking, sensibilidad y límites.

**Producto:** notebook reproducible, diccionario de transformaciones, tabla de prioridad por muestra o sitio-periodo, análisis de sensibilidad y reporte de riesgo.

**Prueba de viabilidad:** todos los componentes pueden construirse con las diez variables publicadas. El catálogo auxiliar de sitios puede enriquecer contexto, pero una ubicación geográfica no es obligatoria.

**Afirmaciones prohibidas:** “detectar fugas”, “predecir presión”, “certificar potabilidad”, “identificar causa de contaminación” o “recomendar tratamiento” con este dataset aislado.

#### Extensiones opcionales

- catálogo oficial de sitios para contexto administrativo;
- clima y precipitaciones por fecha;
- reglas regulatorias documentadas por especialistas;
- modelo de censura en lugar de sustitución simple;
- estructura jerárquica por sitio;
- evaluación prospectiva con meses posteriores.

Estas extensiones requieren documentación y no pueden transformar el laboratorio básico en una evaluación regulatoria real.

---

## D.3. Reclamos financieros y procesamiento de texto

### D.3.1. Fuente abierta, versión y acceso

La fuente principal es **Consumer Financial Protection Bureau, Consumer Complaint Database**:

- descripción oficial: <https://cfpb.github.io/api/ccdb/index.html>;
- referencia de campos: <https://cfpb.github.io/api/ccdb/fields.html>;
- documentación de API: <https://cfpb.github.io/api/ccdb/api.html>;
- descarga masiva oficial habitualmente publicada como `complaints.csv.zip` en `files.consumerfinance.gov/ccdb/`;
- actualización: generalmente diaria según la documentación oficial.

La base contiene reclamos enviados a empresas para respuesta. Se publican después de la respuesta de la empresa o después de quince días, según la explicación del CFPB. No incluye todos los reclamos del sistema financiero: algunos casos se remiten a otros reguladores y las narrativas solo se publican cuando el consumidor consiente y después de medidas de supresión de información personal.

Debido a la actualización diaria, el equipo docente debe congelar una versión. El manifiesto debe incluir fecha máxima de recepción y cantidad de filas totales, filas con narrativa y distribución de productos. Una actividad no debe mezclar descargas realizadas en días diferentes.

### D.3.2. Unidad de análisis, etiquetas y anonimización

La unidad es un **reclamo publicado**, identificado por `Complaint ID`. Para las actividades de NLP se conserva únicamente el subconjunto con `Consumer complaint narrative` no vacía.

El objetivo obligatorio recomendado es **clasificar `Product` a partir de la narrativa inicial**. Es una etiqueta disponible, comprensible y con suficientes observaciones. Como alternativa docente, puede clasificarse `Issue` dentro de un único producto; no se recomienda una clasificación global de `Issue` sin considerar que sus valores dependen de `Product`.

La narrativa fue sometida por CFPB a medidas de supresión de información personal, pero sigue siendo texto aportado por personas. Las entregas no deben reproducir relatos completos. Los ejemplos de error deben limitarse a fragmentos necesarios, volver a revisarse y evitar nombres, direcciones, identificadores o combinaciones que faciliten reidentificación.

La ausencia de narrativa no es aleatoria: depende del consentimiento y del proceso de publicación. El modelo aprendido sobre narrativas consentidas no representa automáticamente todos los reclamos.

### D.3.3. Diccionario de campos y criterios de exclusión

| Campo publicado | Momento aproximado | Uso en el laboratorio |
|---|---|---|
| `Date received` | Ingreso | Corte temporal y variables de calendario. |
| `Product` | Ingreso/registro | Etiqueta obligatoria recomendada. No usar como entrada. |
| `Sub-product` | Ingreso/registro | Etiqueta opcional o análisis jerárquico; presenta faltantes. |
| `Issue` | Ingreso/registro | Etiqueta alternativa dentro de producto. No usar como entrada al predecirse. |
| `Sub-issue` | Ingreso/registro | Etiqueta opcional; depende de producto e issue y puede faltar. |
| `Consumer complaint narrative` | Ingreso, publicada con consentimiento | Texto principal para TF-IDF y clasificación. |
| `Company public response` | Posterior a envío | Excluir: contiene información posterior y respuesta empresarial. |
| `Company` | Conocida en el reclamo | Excluir del baseline obligatorio para evitar atajos por cartera de productos; usar solo en análisis de sesgo opcional. |
| `State` | Ingreso | Contexto opcional; puede faltar y no debe dominar la clasificación temática. |
| `ZIP code` | Ingreso | Excluir del modelo obligatorio por privacidad, granularidad irregular y riesgo de proxy. |
| `Tags` | Ingreso o enriquecimiento | Excluir del modelo obligatorio; pueden reflejar grupos sensibles como personas mayores o militares. |
| `Submitted via` | Ingreso | Contexto opcional disponible al recibir. |
| `Date sent to company` | Posterior al ingreso | Excluir de entradas; se produce durante el flujo. |
| `Company response to consumer` | Posterior | Excluir: resultado posterior. |
| `Timely response?` | Posterior | Excluir: solo existe después de la respuesta. No es etiqueta de urgencia inicial. |
| `Complaint ID` | Identificador | Clave y trazabilidad; nunca atributo predictivo. |

#### Variables derivadas permitidas

| Variable | Derivación | Restricción |
|---|---|---|
| `anio`, `mes`, `dia_semana` | desde `Date received` | Solo si la partición temporal evita futuro. |
| `longitud_texto` | cantidad de caracteres o tokens | Puede utilizarse como diagnóstico o atributo documentado. |
| `tiene_narrativa` | presencia de texto | Para estudiar selección; el corpus obligatorio ya condiciona en verdadero. |
| `tokens`, `ngramas`, `tfidf` | ajustados sobre narrativa | Vocabulario y pesos solo con entrenamiento. |
| `grupo_duplicado` | similitud exacta o casi duplicada | Se utiliza para mantener duplicados en una partición. |
| `confianza_modelo` | probabilidad o margen | Base para derivación a revisión, después de calibración. |

#### Fugas y atajos que deben probarse

1. incluir `Product`, `Issue` o derivados de la etiqueta en el texto analítico;
2. incorporar respuesta de empresa o campos posteriores;
3. ajustar vocabulario con todo el corpus;
4. repartir textos duplicados o plantillas entre entrenamiento y prueba;
5. utilizar `Company` como sustituto casi directo del producto;
6. seleccionar umbral consultando repetidamente el conjunto de prueba.

### D.3.4. Actividades `REC-01` a `REC-04`

#### `REC-01`: construir el corpus

**Unidad:** reclamo con narrativa publicada y etiqueta `Product` válida.

**Tareas mínimas:** congelar fecha, seleccionar campos, eliminar filas sin narrativa para el corpus, normalizar etiquetas sin modificar el texto original, identificar duplicados exactos, producir tabla con `Complaint ID`, narrativa, producto, fecha y grupo de partición.

**Producto:** corpus versionado, diccionario, reporte de faltantes y diagrama de procedencia. Debe registrarse cuántos reclamos quedaron fuera por ausencia de narrativa.

#### `REC-02`: diseñar evaluación

**Partición recomendada:** temporal. Entrenar con reclamos anteriores, validar con periodo posterior y reservar el periodo más reciente para prueba. Los duplicados o plantillas detectados deben permanecer en un único conjunto.

**Baseline:** clase mayoritaria y, preferentemente, un baseline de palabras simples ajustado solo con entrenamiento.

**Métrica principal:** macro-F1 para dar visibilidad a productos menos frecuentes. Informar también accuracy, matriz de confusión, soporte por clase y, si se usan probabilidades, calibración.

**Criterio de factibilidad:** si algunas clases tienen soporte insuficiente, el equipo docente puede agrupar productos antes de distribuir la consigna. La agrupación debe ser fija y común; no debe decidirla cada estudiante mirando la prueba.

#### `REC-03`: representar con TF-IDF

**Entrada:** solo narrativa de entrenamiento.

**Comparación mínima:** unigramas frente a una variante con bigramas o decisiones de normalización. Deben compararse dimensionalidad, cobertura de vocabulario y términos relevantes.

**Regla:** el vocabulario, frecuencias documentales y cualquier selección de términos se ajustan dentro de entrenamiento o de cada fold. No se requiere stemming o lematización si no mejora una hipótesis lingüística clara.

#### `REC-04`: clasificar y analizar errores

**Tarea:** comparar baseline con al menos un clasificador lineal apropiado para TF-IDF. Examinar errores por producto, longitud, canal y periodo.

**Priorización realizable:** priorizar **revisión humana o enrutamiento**, no urgencia sustantiva. Un ejemplo de regla es:

- alta confianza: proponer ruta temática;
- baja confianza o margen pequeño entre clases: enviar a revisión;
- clases con alto costo de enrutamiento erróneo: exigir umbral mayor.

`Timely response?` no puede utilizarse para definir prioridad al ingreso porque se observa después. El dataset tampoco contiene una etiqueta validada de daño, vulnerabilidad o urgencia del caso.

### D.3.5. Guía del laboratorio de reclamos

**Propósito ajustado:** construir un sistema reproducible de clasificación temática de narrativas y una política de derivación según confianza.

**Cadena mínima:**

1. corpus con procedencia y consentimiento (`REC-01`);
2. protocolo temporal, baseline y métricas (`REC-02`);
3. TF-IDF sin fuga (`REC-03`);
4. clasificador, calibración o margen, errores y abstención (`REC-04`);
5. reporte de limitaciones de cobertura.

**Producto grupal:** notebook o prototipo que recibe narrativa y devuelve producto sugerido, confianza y decisión `enrutar/revisar`. No debe generar una respuesta financiera ni asesorar al consumidor.

**Evidencia individual:** análisis de un producto, reproducción de una comparación y defensa de umbral de revisión.

**Prueba de viabilidad:** narrativa y `Product` están directamente disponibles en el subconjunto consentido; el resto de la cadena utiliza variables derivadas del texto. La priorización se define sobre confianza del sistema y no exige una etiqueta inexistente.

#### Extensiones opcionales

- clasificación jerárquica `Product -> Issue`;
- comparación con embeddings contextuales;
- monitoreo de deriva temporal de vocabulario;
- análisis de desempeño por `Submitted via` o estado con cautela;
- recuperación de reclamos similares para asistencia humana.

No son extensiones válidas inferir atributos personales, producir decisiones crediticias ni reutilizar narrativas fuera del propósito educativo declarado.

---

## D.4. Diagnóstico visual de enfermedades vegetales

### D.4.1. Fuente abierta, licencia y versión

La fuente es **PlantVillage**, distribución mantenida por el repositorio original y disponible en Hugging Face:

- dataset: <https://huggingface.co/datasets/mohanty/PlantVillage>;
- repositorio: <https://github.com/spMohanty/PlantVillage-Dataset>;
- artículo de referencia: Mohanty, Hughes y Salathé (2016), *Using Deep Learning for Image-Based Plant Disease Detection*;
- licencia indicada en Hugging Face: `CC BY-SA 3.0`;
- configuración obligatoria: `color`;
- tamaño publicado: 54.306 imágenes originales, 14 cultivos, 26 enfermedades y 38 combinaciones cultivo-condición;
- partición publicada para color: aproximadamente 43.596 imágenes de entrenamiento y 10.709 de prueba, respetando agrupación por hoja según la tarjeta del dataset.

La versión debe congelarse mediante identificador de revisión o fecha de descarga. No deben mezclarse configuraciones `color`, `grayscale` y `segmented` como si fueran observaciones independientes: son representaciones derivadas de las mismas hojas.

### D.4.2. Clases, procedencia y condiciones de captura

Las etiquetas combinan cultivo y condición, por ejemplo `Apple___Black_rot` o `Potato___healthy`. El objetivo mínimo es clasificar esa combinación dentro del subconjunto elegido.

Las imágenes PlantVillage fueron capturadas en condiciones relativamente controladas, con hojas destacadas del fondo. El dataset no aporta variables de lote, región, clima, manejo, severidad ni confirmación clínica en campo para cada imagen. Por ello:

- el modelo aprende a reconocer clases de PlantVillage;
- no puede afirmarse validación en campo;
- no puede estimar severidad de la enfermedad;
- no puede recomendar tratamiento;
- una probabilidad alta no reemplaza diagnóstico agronómico.

Para mantener el costo computacional razonable, el laboratorio obligatorio puede trabajar con **un cultivo que posea al menos tres clases**. Opciones adecuadas incluyen papa, manzana, maíz, uva o tomate. La elección se fija para toda la cohorte o se distribuye por equipos. La clasificación completa de 38 clases es una extensión.

### D.4.3. Variables, particiones y transformaciones permitidas

La distribución de Hugging Face publica las siguientes variables:

| Variable | Tipo | Uso |
|---|---|---|
| `image` | Imagen | Entrada visual. |
| `image_path` | Texto | Trazabilidad; no usar como atributo predictivo porque contiene nombres de carpetas/clases. |
| `label` | Clase | Objetivo cultivo-condición. |
| `crop` | Texto | Selección de subconjunto o tarea jerárquica. |
| `disease` | Texto | Análisis de clases; no entrada cuando forma parte de la etiqueta. |
| `leaf_id` | Texto | Identificador de hoja física para prevenir fuga. |

#### Partición obligatoria

1. conservar la prueba oficial sin usar durante selección;
2. crear entrenamiento y validación desde la partición oficial de entrenamiento;
3. agrupar por `leaf_id`, de modo que una hoja no aparezca en más de un conjunto;
4. estratificar por etiqueta en la medida compatible con el agrupamiento;
5. registrar lista de `leaf_id` por partición.

Si se usa una versión sin `leaf_id`, debe reconstruirse desde el archivo oficial `leaf_grouping/leaf-map.json`. No se acepta partición aleatoria por imagen ignorando la hoja.

#### Auditoría mínima

- dimensiones, canales y formatos;
- distribución por `label`, `crop` y `disease`;
- imágenes corruptas;
- hashes exactos y perceptuales para duplicados;
- cantidad de imágenes por `leaf_id`;
- galería por clase;
- comparación visual de entrenamiento y prueba.

#### Transformaciones permitidas

Redimensionar, normalizar y aplicar aumento solo a entrenamiento. Rotaciones, reflejos, recortes y cambios de color deben conservar la señal de enfermedad; una transformación que elimina lesiones no es válida. Validación y prueba reciben únicamente transformaciones deterministas necesarias para el modelo.

La configuración `segmented` puede utilizarse en una comparación opcional para estudiar efecto del fondo, manteniendo exactamente los mismos `leaf_id`. No constituye un conjunto independiente.

### D.4.4. Actividades `VEG-01` a `VEG-04`

#### `VEG-01`: preparar el dataset

**Tareas:** seleccionar cultivo, auditar clases, revisar imágenes, detectar duplicados, verificar `leaf_id` y crear entrenamiento/validación sin modificar prueba.

**Producto:** manifiesto de particiones, distribución, galería y reglas de inclusión. Debe probarse que la intersección de `leaf_id` entre conjuntos es vacía.

#### `VEG-02`: baseline y diagnóstico

**Baselines mínimos:** clase mayoritaria y una red pequeña o representación sencilla. La mayoría establece dificultad mínima; la red permite analizar curvas.

**Comparación:** al menos dos configuraciones de tasa de aprendizaje, regularización o early stopping, manteniendo constantes los demás factores. Informar macro-F1 y métricas por clase además de accuracy.

**Producto:** historial, curvas, configuración y diagnóstico de sobreajuste, subajuste o inestabilidad.

#### `VEG-03`: CNN y errores por clase

**Tarea:** entrenar una CNN sobre las particiones congeladas y compararla con el baseline.

**Evidencia:** arquitectura, parámetros, matriz de confusión, precisión/recall/F1 por clase y galería comentada de aciertos y errores. La galería debe usar imágenes de validación durante desarrollo y prueba solo al final.

**Análisis requerido:** distinguir errores entre enfermedades del mismo cultivo y verificar si fondo, orientación o calidad visual explican patrones.

#### `VEG-04`: transferencia y condiciones de uso

**Tarea:** comparar extracción de características con ajuste fino de una arquitectura preentrenada. El aumento se aplica solo en entrenamiento.

**Confianza:** evaluar calibración o, como mínimo, relación entre confianza y error. Definir una regla de abstención basada en validación, por ejemplo derivar casos con probabilidad máxima menor que un umbral.

**Condición de uso obligatoria:** “clasificación de imágenes semejantes a PlantVillage”. No se permite escribir “diagnóstico en campo” sin un conjunto externo de campo.

### D.4.5. Guía del laboratorio de sanidad vegetal

**Propósito ajustado:** construir y documentar un clasificador para un cultivo y sus clases PlantVillage, comparando baseline, CNN y transferencia, con abstención y análisis de errores.

**Cadena mínima:**

1. particiones por hoja y auditoría (`VEG-01`);
2. baseline y diagnóstico de entrenamiento (`VEG-02`);
3. CNN y evaluación por clase (`VEG-03`);
4. transferencia, confianza y abstención (`VEG-04`);
5. ficha del modelo con usos permitidos y prohibidos.

**Producto grupal:** prototipo que recibe una imagen y devuelve clase PlantVillage sugerida, confianza y decisión `clasificar/revisar`. Debe mostrar una advertencia explícita sobre condiciones controladas.

**Prueba de viabilidad:** las variables `image`, `label`, `crop`, `disease` y `leaf_id` permiten completar toda la cadena. No se necesita información agronómica externa para la clasificación mínima.

**Criterio de aprobación:** comparación con baseline, prueba reservada, métricas por clase, ausencia de fuga por hoja, análisis visual y regla de abstención derivada de validación.

#### Extensiones opcionales

- clasificación de 38 clases;
- tarea jerárquica cultivo y enfermedad;
- comparación color/grayscale/segmented por la misma hoja;
- explicaciones visuales;
- validación externa con imágenes de campo documentadas;
- detección o segmentación con otro dataset que incluya cajas o máscaras.

PlantVillage no incluye cajas de detección ni máscaras de lesiones como objetivo. La existencia de imágenes segmentadas de fondo no las convierte en máscaras supervisadas de enfermedad.

---

## D.5. Rúbrica común de evaluación

La rúbrica evalúa una cadena metodológica, no una competencia por la mejor métrica. Cada dimensión se califica como insuficiente, básico, competente o destacado. El nivel competente representa aprobación.

### D.5.1. Reproducibilidad y trazabilidad

**Competente:** identifica fuente, versión y licencia o términos; conserva originales; registra particiones y semillas; reconstruye el producto desde el manifiesto; vincula resultados con entradas.

**Insuficiente:** utiliza una descarga sin fecha, modifica originales, comparte solo el notebook ejecutado o no puede reconstruir las particiones.

### D.5.2. Corrección metodológica

**Competente:** define unidad y objetivo; evita fuga; ajusta transformaciones con entrenamiento; compara con baseline; utiliza métricas coherentes; respeta tiempo, grupos y dependencias.

**Insuficiente:** usa variables posteriores, consulta prueba durante selección, mezcla unidades o atribuye al modelo información contenida en la etiqueta.

### D.5.3. Interpretación y relación con la decisión

**Competente:** conecta evidencia con una decisión realizable, explicita costos y distingue asociación, predicción y causalidad. La recomendación usa variables realmente disponibles.

**Insuficiente:** propone una acción que requiere variables inexistentes o convierte una clasificación en una decisión sin regla operativa.

### D.5.4. Incertidumbre, sesgos y limitaciones

**Competente:** analiza cobertura, faltantes, desbalance, selección y cambio temporal; presenta sensibilidad; declara poblaciones no representadas y condiciones de abstención.

**Insuficiente:** presenta métricas globales como certeza, oculta clases o zonas sin datos, o generaliza a campo/población fuera del dataset.

### D.5.5. Comunicación y defensa individual

**Competente:** documenta definiciones, gráficos y métricas; diferencia aporte individual; reproduce una comparación; responde qué información cambiaría su decisión.

**Insuficiente:** no puede explicar procedencia, umbral, error relevante o límite de uso.

### D.5.6. Tabla de verificación por laboratorio

| Verificación | Agua | Movilidad | Reclamos | Vegetales |
|---|---:|---:|---:|---:|
| Fuente y versión congeladas | Sí | Sí | Sí | Sí |
| Unidad consistente | Muestra/sitio-periodo | Viaje/zona-franja | Reclamo | Imagen/hoja |
| Grupo o tiempo respetado | Sitio y fecha | Zona y fecha | Fecha/duplicado | `leaf_id` |
| Baseline obligatorio | Frecuencia histórica | Estacional/último valor | Mayoritaria/TF-IDF simple | Mayoritaria/red pequeña |
| Prueba reservada | Periodo posterior | Periodo posterior | Periodo posterior | Split oficial |
| Decisión realizable | Revisar/remuestrear | Priorizar zona | Enrutar/revisar | Clasificar/revisar |
| Límite principal | No potabilidad/fugas | No demanda total/red vial | No urgencia | No campo/severidad |

Un laboratorio no se aprueba si incumple una condición estructural, aunque obtenga una métrica alta.

---

## D.6. Ejemplo práctico guiado: defensa integral de un proyecto

La defensa debe recorrer la cadena completa en diez minutos y responder preguntas sobre decisiones, no recitar el notebook.

### D.6.1. Estructura sugerida

1. **Problema y decisión:** qué usuario decide y qué acción es posible.
2. **Fuente y unidad:** de dónde provienen los datos y qué representa una fila.
3. **Variables:** cuáles son directas, derivadas, auxiliares y excluidas.
4. **Calidad:** qué problema podía cambiar la conclusión.
5. **Partición:** cómo se evitó compartir futuro, entidad o duplicado.
6. **Baseline:** qué regla simple debía superarse.
7. **Modelo o algoritmo:** qué aporta y bajo qué supuestos.
8. **Errores:** qué casos fallan y a quién afectan.
9. **Decisión:** cómo probabilidades o métricas producen una acción.
10. **Límite:** qué afirmación no puede realizarse con ese dataset.

### D.6.2. Preguntas de defensa por caso

**Movilidad:** ¿por qué el grafo OD no es una red vial?, ¿qué significa un cero en una serie?, ¿qué población no observa TLC?

**Agua:** ¿cómo trató `<1`?, ¿por qué `sample_class` puede filtrar el proceso?, ¿por qué no afirma potabilidad?

**Reclamos:** ¿por qué el corpus está seleccionado por consentimiento?, ¿qué campos posteriores excluyó?, ¿qué significa “priorizar” sin urgencia etiquetada?

**Vegetales:** ¿cómo demostró separación por `leaf_id`?, ¿qué diferencia hay entre imagen PlantVillage y campo?, ¿cómo eligió abstención?

### D.6.3. Criterio final

Una defensa satisfactoria muestra que el estudiante sabe qué información tiene y qué información no tiene. La capacidad central no es ejecutar más técnicas, sino construir una conclusión cuyo alcance coincida con la evidencia disponible.
