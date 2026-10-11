<style>
@page { size: A4; margin: 16mm 16mm 17mm 16mm; }
body { font-family: "DejaVu Sans", sans-serif; color: #17324d; line-height: 1.38; font-size: 10pt; }
h1 { color: #17324d; border-bottom: 4px solid #007f82; padding-bottom: 8px; }
h2 { color: #17324d; border-bottom: 2px solid #e2a33a; padding-bottom: 4px; margin: 20px 0 8px; page-break-after: avoid; }
h3 { color: #007f82; margin: 12px 0 4px; page-break-after: avoid; }
h4 { color: #536471; margin: 9px 0 3px; page-break-after: avoid; }
p { margin: 6px 0; }
ul, ol { margin-top: 4px; margin-bottom: 8px; }
blockquote { border-left: 4px solid #e2a33a; background: #f3f6f8; margin: 10px 0; padding: 8px 12px; page-break-inside: avoid; }
table { border-collapse: collapse; width: 100%; font-size: 8.7pt; }
th { background: #17324d; color: white; }
th, td { border: 1px solid #aab7c1; padding: 6px; vertical-align: top; }
code { color: #007f82; }
strong { color: #17324d; }
</style>

# Guía docente: Adquisición, comprensión y preparación inicial de datos

**Curso:** Data Science

**Semana y clase:** semana 2, clase 2

**Presentación asociada:** *Adquisición, comprensión y preparación inicial de datos: de fuentes heterogéneas a una tabla analítica defendible* (38 diapositivas)

**Notebook asociado:** `Taller_Clase_02_Movilidad.ipynb`

**Fuentes principales:** capítulos 2, 3 y 4 del libro *Ciencia de Datos e Inteligencia Artificial*

### Propósito y forma de uso

Esta guía sincroniza la exposición conceptual con un taller de datos públicos sobre viajes de NYC TLC Yellow Taxi, zonas de taxi y clima NOAA. La meta no es obtener una cifra predeterminada, sino construir y auditar una tabla cuya fila representa una **zona de origen-hora local**. Los conteos, porcentajes, asociaciones y gráficos dependen de la disponibilidad de las fuentes, de `MODO_CLASE` y de los filtros ejecutados; por ello se comprueba la lógica y no se anticipan resultados numéricos.

La sesión debe conservar una distinción central: los registros son **viajes reportados**, no demanda total de movilidad. La tabla analítica permite descripción y asociación exploratoria; no identifica causalidad ni representa por sí sola toda la ciudad, todos los servicios o todo el clima urbano.

### Recorrido por bloques

| Bloque | Diapositivas | Resultado esperado |
|---|---:|---|
| Bloque conceptual | 1-17 | Delimitar producto, procedencia, unidad, calidad, integración, agregación y reproducibilidad |
| Transición | 18 | Convertir los conceptos en pregunta, flujo y límites del caso |
| Taller guiado | 19-35 | Adquirir, inspeccionar, auditar, integrar, agregar, visualizar y guardar el producto |
| Producto | 36 | Presentar evidencias y artefactos verificables |
| Límites | 37 | Formular únicamente afirmaciones compatibles con cobertura y diseño |
| Cierre | 38 | Recuperar el proceso completo y enlazar con exploración estadística |

> **Tesis de la clase:** preparar datos no es aplicar una secuencia automática de limpieza. Es justificar qué representa cada fila, de dónde proviene, qué reglas soporta, qué se pierde al transformar y para qué afirmaciones sigue siendo apta.

### Agenda temporal sugerida: 150 minutos

| Tiempo | Actividad | Diapositivas |
|---:|---|---:|
| 0-8 min | Apertura, propósito y pregunta rectora | 1-3 |
| 8-30 min | Objetos de datos, procedencia, unidad y regla de una fila | 4-7 |
| 30-52 min | Tipos, calidad, faltantes, duplicados y claves | 8-12 |
| 52-68 min | Integración temporal/espacial, agregación y reproducibilidad | 13-17 |
| 68-73 min | Transición y definición del taller | 18-19 |
| 73-81 min | Pausa breve | -- |
| 81-111 min | Adquisición, inspección, auditoría y zonas | 20-27 |
| 111-132 min | Zona-hora, clima e integración | 28-31 |
| 132-143 min | Visualizaciones, asociación y guardado | 32-35 |
| 143-150 min | Producto, límites y cierre | 36-38 |

Los tiempos son orientativos. Si las descargas se retrasan, priorizar los controles de unidad, calidad, cardinalidad y cobertura; la extensión espacial puede demostrarse sin esperar su renderizado.

### Preparación previa del docente

1. Confirmar internet estable y acceso desde el entorno de clase a las cuatro URL definidas en `URL_VIAJES`, `URL_ZONAS`, `URL_GEOMETRIAS` y `URL_CLIMA`.
2. Verificar dependencias base: `pandas`, `numpy`, `matplotlib`, `pyarrow` e IPython. Para la extensión opcional, verificar `geopandas`, `folium` y `requests`.
3. Abrir una copia de trabajo del notebook y mantener `MODO_CLASE = True`; esta opción procesa la primera semana consecutiva y reduce tiempo sin convertirla en muestra aleatoria.
4. Ejecutar el notebook de inicio a fin antes de la sesión, incluidas las comprobaciones y, si el entorno lo permite, la extensión espacial. Revisar mensajes de error, cambios de esquema y nombres de columnas NOAA.
5. Comprobar que el entorno permite leer Parquet remoto con filtros mediante `pyarrow` y que las fechas quedan con zona `America/New_York` después de la conversión.
6. No guardar datasets descargados en el repositorio. Si se necesita conservar el producto para evaluación, usar almacenamiento temporal del entorno, una carpeta externa o la descarga local del artefacto generado.

### Plan B offline, sin añadir datasets al repositorio

Antes de clase, ejecutar el notebook conectado y conservar **fuera del repositorio** una copia temporal de los recursos requeridos, por ejemplo en el almacenamiento local privado del docente, una unidad institucional o el directorio temporal del entorno. Registrar junto a esa copia URL, fecha de acceso y nombre original. En clase, si falla internet, sustituir únicamente las cuatro variables URL por rutas locales externas y mantener intactas las celdas de validación, filtrado, unión y análisis. Para Parquet se conserva `columns` y, si el motor local admite el filtro, `filters`; CSV/PSV se leen desde la ruta externa; el ZIP espacial se pasa a `geopandas` desde esa ubicación.

Si no existe una copia externa autorizada, usar la ejecución previa ya visible para discutir esquema, auditorías y gráficos, y realizar en vivo ejercicios de lectura de código y predicción de invariantes. No fabricar cifras, no presentar capturas como una nueva fuente y no incorporar datos ni salidas al control de versiones. Explicar que este plan preserva la enseñanza del flujo, pero no demuestra reproducibilidad de red en ese momento; registrar la incidencia y repetir la ejecución conectada después.

### Evaluación del producto

| Criterio | Evidencia observable | Peso sugerido |
|---|---|---:|
| Definición y procedencia | Cuatro fuentes, periodo, unidad, clave, zona horaria y propósito declarados | 20 % |
| Calidad y decisiones | Faltantes, duplicados o aproximación de clave, reglas de validez, exclusiones y sensibilidad justificadas | 20 % |
| Integración verificable | Unicidad del lado “uno”, `validate`, conservación de filas y cobertura de zonas/clima | 20 % |
| Producto reproducible | Notebook ejecutable, tabla zona-hora con clave única, orden, metadatos y procedencia | 20 % |
| Comunicación responsable | Perfil, mapa o extensión espacial, gráficos clima-viajes, hallazgos con evidencia y al menos tres límites | 20 % |

Una falla crítica de cardinalidad no resuelta, una unidad ambigua o una afirmación causal invalida la defensa aunque los gráficos se rendericen. No calificar por obtener conteos idénticos entre fechas de ejecución; calificar reglas, trazabilidad e interpretación.

### Pautas para los ejercicios del notebook

**Pregunta breve sobre ventana consecutiva.** Una semana consecutiva conserva orden, ciclos diarios, horas contiguas y denominador temporal. Una muestra aleatoria puede fragmentar horas y alterar conteos; la ventana tampoco garantiza representar el mes completo.

**Ejercicio 1, sensibilidad de distancia.** Construir una máscara independiente, sin modificar `viajes_validos`: `fuera_con_umbral_50 = (~calidad["trip_distance"].between(0, 50)).sum()`. Comparar conceptualmente con `ok_distancia` y explicar que el cambio mide sensibilidad a una decisión de dominio; el total debe leerse de la ejecución.

**Ejercicio 2, cobertura temporal.** Crear `horas_esperadas = pd.date_range(inicio_local, fin_local, freq="h", inclusive="left")` y obtener `horas_sin_clima = horas_esperadas.difference(clima_horario["hora"])`. Interpretar los huecos reales sin presuponer cuántos existen; verificar también que ambas series sean conscientes de zona horaria.

**Ejercicio 3, interpretar sin exagerar.** Aceptar observaciones que nombren variable, dirección o franja, ventana analizada y evidencia gráfica. Exigir una explicación alternativa como hora del día, día de semana, aeropuerto, feriado, oferta o selección. Rechazar lenguaje causal y generalizaciones desde `MODO_CLASE=True` al mes completo.

## Diapositiva 1. Adquisición, comprensión y preparación inicial de datos

**Correspondencia con el libro.** Capítulos 2, ciclo y fuentes; 3, preparación e integración; 4, exploración y visualización.

**Propósito.** Presentar la preparación como construcción de una tabla analítica defendible, no como limpieza mecánica.

**Guion sugerido.** Abrir con: “Hoy partiremos de fuentes heterogéneas y terminaremos en una fila cuyo significado, clave y límites podemos explicar”. Anticipar viajes, zonas y clima.

**Conceptos y términos.** *Adquisición*: obtención documentada; *comprensión*: interpretación de estructura y significado; *preparación*: transformaciones justificadas; *defendible*: reconstruible y limitada a afirmaciones permitidas.

**Ejemplo o acción en notebook.** Mostrar el título, la pregunta guía y la ficha de fuentes, sin ejecutar todavía.

**Error frecuente o límite.** Prometer “datos limpios” como ausencia universal de errores o confundir tabla preparada con verdad completa.

**Comprobación.** Preguntar cuál será la unidad final. Respuesta esperada: zona de origen-hora local.

**Conclusión que debe quedar.** La calidad del producto depende de decisiones semánticas y técnicas trazables.

**Transición sugerida.** “Convirtamos esa meta general en resultados que podamos comprobar al final”.

## Diapositiva 2. Propósito y resultados de aprendizaje

**Correspondencia con el libro.** Capítulo 2, §§2.2-2.4; capítulo 3, §§3.1-3.3; capítulo 4, exploración descriptiva.

**Propósito.** Fijar la definición del aprendizaje de la sesión.

**Guion sugerido.** Recorrer los cinco resultados en orden: distinguir objetos, documentar representación, evaluar calidad, integrar a zona-hora y declarar pérdida y límites. Subrayar que cada resultado tendrá evidencia en el notebook.

**Conceptos y términos.** *Procedencia*, *granularidad*, *regla de una fila*, *cardinalidad*, *reproducibilidad* y *tabla analítica*.

**Ejemplo o acción en notebook.** Vincular los objetivos del notebook con los resultados; aclarar que “pickups” es el conteo de viajes reportados con origen registrado.

**Error frecuente o límite.** Reducir el objetivo a descargar archivos o producir gráficos.

**Comprobación.** Pedir dos controles indispensables al integrar. Respuestas válidas: cardinalidad y cobertura, además de filas, claves o totales pertinentes.

**Conclusión que debe quedar.** El producto deberá ser interpretable, verificable y reproducible.

**Transición sugerida.** “Para decidir qué datos sirven, primero hace falta una pregunta suficientemente precisa”.

## Diapositiva 3. La preparación comienza con una pregunta

**Correspondencia con el libro.** Capítulo 2, formulación del problema, comprensión del negocio y de los datos.

**Propósito.** Mostrar que pregunta y producto determinan adquisición y representación.

**Guion sugerido.** Usar el ejemplo sucursal-día: precisar producto, unidad, población, periodo, exclusiones y disponibilidad. Contrastar “tenemos archivos” con una necesidad analítica delimitada.

**Conceptos y términos.** *Producto esperado*, *población*, *periodo*, *exclusión*, *momento de disponibilidad*.

**Ejemplo o acción en notebook.** Leer la pregunta guía y pedir que identifiquen producto, periodo y unidad antes de ejecutar. La unidad final se completa con la definición de la diapositiva 19.

**Error frecuente o límite.** Elegir columnas disponibles y después inventar una pregunta que las justifique.

**Comprobación.** “¿Cambiaría la adquisición si el producto fuera viaje individual en vez de zona-hora?”. Sí: cambiarían unidad, clave, integración y afirmaciones.

**Conclusión que debe quedar.** La pregunta restringe qué adquirir, conservar, transformar y comunicar.

**Transición sugerida.** “Antes de descargar, distingamos los objetos que solemos llamar indistintamente datos”.

## Diapositiva 4. Fuente, archivo, tabla, dataset y producto

**Correspondencia con el libro.** Capítulo 2, §2.3 sobre fuentes, tipos y arquitectura; §2.4 sobre artefactos reproducibles.

**Propósito.** Evitar que origen, contenedor, estructura, colección y resultado se usen como sinónimos.

**Guion sugerido.** Leer cada fila de la tabla y encadenar un ejemplo: portal TLC, Parquet mensual, tabla de viajes, conjunto documentado y perfil zona-hora. El producto siempre implica transformación y propósito.

**Conceptos y términos.** *Fuente*: sistema de origen; *archivo*: objeto intercambiable; *tabla*: filas y columnas; *dataset*: colección delimitada y documentada; *producto*: evidencia preparada para uso.

**Descripción visual relevante.** La tabla tiene tres columnas: concepto, función y ejemplo. Leer horizontalmente cada fila y después verticalmente la primera columna; no interpretar los cinco objetos como etapas obligatorias ni relación uno a uno.

**Ejemplo o acción en notebook.** Identificar TLC y NOAA como fuentes, Parquet/CSV/ZIP/PSV como archivos, DataFrames como tablas y `zona_hora_clima` como producto analítico intermedio/final.

**Error frecuente o límite.** Llamar “fuente” a una copia descargada o “dataset” a cualquier DataFrame sin alcance ni documentación.

**Comprobación.** Preguntar si un ZIP espacial es ya la tabla zona-hora. No: es un archivo con recursos geométricos.

**Conclusión que debe quedar.** Saber qué objeto se nombra aclara procedencia y responsabilidad.

**Transición sugerida.** “Ahora reconstruyamos el camino desde el fenómeno hasta el producto”.

## Diapositiva 5. Procedencia y linaje

**Correspondencia con el libro.** Capítulo 2, adquisición, procedencia, documentación y reproducibilidad.

**Propósito.** Diferenciar origen documentado y cadena de transformaciones.

**Guion sugerido.** Recorrer fenómeno, captura, fuente, extracción, transformaciones y producto. Para cada fuente registrar responsable, propósito original, URL, acceso, versión, licencia, filtros y uniones.

**Conceptos y términos.** *Procedencia*: de dónde viene; *linaje*: qué transformaciones y decisiones condujeron al artefacto.

**Descripción visual relevante.** El diagrama es una cadena lineal `fenómeno → captura → fuente → extracción → transformaciones → producto`. Las flechas significan dependencia trazable, no copia exacta ni garantía de calidad; leer también hacia atrás desde el producto para preguntar qué debe reconstruirse.

**Ejemplo o acción en notebook.** Revisar “Ficha de fuentes” y las constantes `URL_*`; pedir anotar fecha de acceso y `MODO_CLASE` en la entrega.

**Error frecuente o límite.** Registrar solo la URL final o suponer que una licencia corrige problemas de cobertura y significado.

**Comprobación.** “¿Dónde queda documentado que solo se leyó la primera semana?”. En parámetros/filtros y metadatos de ejecución, no en el nombre del archivo original.

**Conclusión que debe quedar.** Procedencia y linaje permiten explicar y regenerar el producto.

**Transición sugerida.** “Para reconstruir una tabla también debemos saber qué representa cada observación”.

## Diapositiva 6. Unidad y granularidad

**Correspondencia con el libro.** Capítulo 2, unidad y alcance; capítulo 3, estructura tabular y transformación.

**Propósito.** Separar entidad elemental y nivel de detalle.

**Guion sugerido.** Contrastar transacción producto-instante con resumen tienda-día. Explicar que cambiar granularidad modifica preguntas, dependencias y número de filas.

**Conceptos y términos.** *Unidad de análisis*: entidad elemental descrita; *granularidad*: detalle temporal, espacial y de entidad.

**Ejemplo o acción en notebook.** Señalar el cambio de viaje en `viajes_originales` a zona-hora en `pickups_zona_hora`.

**Error frecuente o límite.** Decir que una tabla es “por zona” omitiendo hora, o comparar medias sin reconocer unidades distintas.

**Comprobación.** Pedir la unidad antes y después de `groupby`: viaje reportado y zona de pickup-hora local.

**Conclusión que debe quedar.** Toda transformación debe declarar si conserva o cambia la unidad.

**Transición sugerida.** “Hagamos esa declaración operativa con una frase que pueda comprobarse”.

## Diapositiva 7. La regla de una fila

**Correspondencia con el libro.** Capítulo 3, §3.1 sobre estructura, claves, perfiles y diccionarios.

**Propósito.** Establecer una frase verificable antes de limpiar o deduplicar.

**Guion sugerido.** Completar “una fila representa...”, identificar columnas candidatas a clave y discutir si coincidencias significan repetición, corrección o evento válido.

**Conceptos y términos.** *Regla de una fila*, *clave candidata*, *medida repetida*, *duplicado legítimo o problemático*.

**Ejemplo o acción en notebook.** Para `viajes_originales`, una fila es un viaje Yellow Taxi reportado sin identificador oficial expuesto; para `pickups_zona_hora`, una fila es una combinación única `pickup_hora, PULocationID`.

**Error frecuente o límite.** Ejecutar `drop_duplicates()` sin definir unidad; la aproximación de columnas de viaje puede colisionar con eventos distintos.

**Comprobación.** Verificar el `assert` de no duplicidad en `pickups_zona_hora` y pedir que expliquen qué garantiza y qué no.

**Conclusión que debe quedar.** La regla de una fila precede a claves, duplicados y agregaciones.

**Transición sugerida.** “Con la unidad clara, distingamos cómo está almacenado un valor de lo que significa”.

## Diapositiva 8. Tipos físicos y tipos semánticos

**Correspondencia con el libro.** Capítulo 2, tipos de datos; capítulo 3, comprensión, diccionario y conversiones.

**Propósito.** Evitar operaciones computables pero conceptualmente inválidas.

**Guion sugerido.** Leer los cuatro ejemplos de la tabla. Señalar que formato físico habilita operaciones, mientras significado determina si son válidas.

**Conceptos y términos.** *Tipo físico*, *tipo semántico*, *identificador nominal*, *categoría ordinal*, *fecha*, *coordenada*.

**Ejemplo o acción en notebook.** Inspeccionar `dtypes`; tratar `PULocationID` como identificador aunque sea numérico y `tpep_pickup_datetime` como tiempo local ingenuo hasta localizarlo.

**Error frecuente o límite.** Promediar IDs de zona o asumir que toda columna numérica es una medida continua.

**Comprobación.** “¿Qué significa la media de `PULocationID`?”. Ninguna cantidad geográfica interpretable.

**Conclusión que debe quedar.** El diccionario semántico gobierna transformaciones válidas.

**Transición sugerida.** “Tipos correctos no bastan: la calidad siempre debe juzgarse contra un propósito”.

## Diapositiva 9. Calidad apta al propósito

**Correspondencia con el libro.** Capítulo 3, §3.1 sobre evaluación y perfiles de calidad.

**Propósito.** Definir calidad como suficiencia para un uso declarado.

**Guion sugerido.** Recorrer completitud, validez, consistencia, unicidad, oportunidad y cobertura. Dar un contraejemplo: un valor correcto que llega después de decidir no es apto.

**Conceptos y términos.** Las seis dimensiones de la tabla y *apto al propósito*.

**Descripción visual relevante.** La tabla empareja cada dimensión con una pregunta de control. Leer cada par como prueba distinta; ninguna fila resume por sí sola “calidad total” y las dimensiones pueden entrar en tensión.

**Ejemplo o acción en notebook.** Relacionar `faltantes`, columnas `ok_*`, unicidad de claves y `auditoria_union` con dimensiones distintas.

**Error frecuente o límite.** Convertir dimensiones en una puntuación única que oculte una falla crítica.

**Comprobación.** Pedir qué dimensión evalúa una zona válida ausente del lookup: cobertura/consistencia de integración, no solo completitud de la tabla original.

**Conclusión que debe quedar.** Cada control necesita una pregunta de uso y una consecuencia.

**Transición sugerida.** “Comencemos por una señal visible cuya causa no puede inferirse solo desde la celda: el faltante”.

## Diapositiva 10. Faltantes: ausencia con significado

**Correspondencia con el libro.** Capítulo 3, limpieza y tratamiento de valores ausentes; capítulo 4, omisión de datos.

**Propósito.** Interpretar nulos según mecanismo y costo antes de imputar o excluir.

**Guion sugerido.** Distinguir no medido, no aplicable, desconocido, fallo de captura, no correspondencia, censura y demora. Pedir proporciones por variable, grupo y periodo.

**Conceptos y términos.** *Mecanismo de ausencia*, *imputación*, *no aplicable*, *fallo de unión*.

**Ejemplo o acción en notebook.** Mostrar `faltantes`; explicar por qué `passenger_count` ausente se conserva y solo valores presentes fuera del intervalo se marcan problemáticos.

**Error frecuente o límite.** Rellenar nulos con cero o media sin distinguir ausencia, o eliminar toda fila con algún nulo.

**Comprobación.** “¿Un `passenger_count` nulo invalida automáticamente el viaje?”. No bajo la regla explícita del taller.

**Conclusión que debe quedar.** Un nulo es evidencia sobre captura o integración, no una instrucción automática.

**Transición sugerida.** “La misma precaución se aplica a filas aparentemente repetidas”.

## Diapositiva 11. Duplicados: definir antes de eliminar

**Correspondencia con el libro.** Capítulo 3, limpieza, duplicados, claves y consistencia.

**Propósito.** Distinguir coincidencia exacta, de clave y de entidad.

**Guion sugerido.** Usar el ejemplo paciente-hora para mostrar que dos filas pueden ser reintentos, correcciones o mediciones válidas. Exigir regla documentada: conservar, consolidar, versionar o excluir.

**Conceptos y términos.** *Duplicado exacto*, *de clave*, *de entidad*, *resolución de entidades*.

**Ejemplo o acción en notebook.** Discutir la clave operativa propuesta en la presentación; el notebook evita borrar silenciosamente y mantiene rechazados separados.

**Error frecuente o límite.** Tratar una combinación operativa como identificador oficial de viaje.

**Comprobación.** Pedir una razón válida para conservar dos filas con tiempos iguales: pueden ser viajes distintos que coinciden en variables observadas.

**Conclusión que debe quedar.** El significado de repetición depende de unidad, clave y proceso generador.

**Transición sugerida.** “Para controlar repeticiones e integración necesitamos declarar claves y relaciones”.

## Diapositiva 12. Claves y cardinalidad

**Correspondencia con el libro.** Capítulo 3, estructura tabular e integración de tablas.

**Propósito.** Prevenir multiplicaciones silenciosas en uniones.

**Guion sugerido.** Definir clave primaria y foránea; recorrer `one_to_one`, `many_to_one`, `one_to_many` y `many_to_many`. Ejemplificar muchas ventas hacia una tienda.

**Conceptos y términos.** *Clave primaria*, *clave foránea*, *cardinalidad esperada*, *multiplicación de filas*.

**Ejemplo o acción en notebook.** `LocationID` debe ser único; muchos viajes referencian una zona. Mostrar `validate="many_to_one"` en ambas uniones del catálogo.

**Error frecuente o límite.** Confiar en que `merge` avisará por sí solo una relación many-to-many accidental.

**Comprobación.** Preguntar qué falla si `LocationID` aparece dos veces: deja de ser lado “uno” y puede duplicar viajes.

**Conclusión que debe quedar.** La cardinalidad es una hipótesis comprobable, no un detalle sintáctico.

**Transición sugerida.** “Convirtamos esa hipótesis en un protocolo antes y después de cada unión”.

## Diapositiva 13. Integración segura

**Correspondencia con el libro.** Capítulo 3, §3.3 sobre integración y ejemplo guiado.

**Propósito.** Establecer cinco controles mínimos para unir tablas.

**Guion sugerido.** Declarar unidad/clave, comprobar unicidad, validar cardinalidad, medir coincidencias y revisar filas/unidades/totales. Repetir que toda unión afirma correspondencia.

**Conceptos y términos.** *Cobertura de unión*, *lado uno*, *coincidencia*, *invariante*.

**Ejemplo o acción en notebook.** Señalar `validate`, el `assert len(viajes_zonas) == len(viajes_validos)` y los conteos sin nombre de pickup/dropoff.

**Error frecuente o límite.** Considerar exitosa una unión solo porque no lanzó excepción; conservar filas no garantiza atributos completos.

**Comprobación.** Pedir dos preguntas posteriores: ¿cambió el número de viajes?, ¿cuántos quedaron sin zona?

**Conclusión que debe quedar.** Una unión se acepta por invariantes y cobertura, no por ejecución técnica.

**Transición sugerida.** “Cuando la clave incluye tiempo, primero hay que reconciliar relojes”.

## Diapositiva 14. Integración temporal

**Correspondencia con el libro.** Capítulos 2 y 3, disponibilidad temporal, transformación e integración.

**Propósito.** Separar tiempo de evento, registro y disponibilidad, y alinear zonas horarias e intervalos.

**Guion sugerido.** Explicar que `10:00 UTC` y `10:00 America/New_York` no son el mismo instante. Definir origen, conversión común, bordes, horario de verano y agregación compatible.

**Conceptos y términos.** *UTC*, *hora local*, *timestamp ingenuo/con zona*, *intervalo semiabierto*, *horario de verano*.

**Ejemplo o acción en notebook.** TLC se localiza en `America/New_York`; NOAA se interpreta con `utc=True` y luego usa `tz_convert`. Enero no contiene transición, pero la regla queda explícita.

**Error frecuente o límite.** Usar `tz_localize` para un instante ya UTC o quitar zona horaria para hacer coincidir etiquetas.

**Comprobación.** Preguntar por qué NOAA usa conversión y TLC localización: una serie representa instantes UTC; la otra, etiquetas locales ingenuas.

**Conclusión que debe quedar.** Integrar por hora exige igualdad de instantes y definición de bordes, no parecido textual.

**Transición sugerida.** “La correspondencia espacial también requiere una regla y metadatos”.

## Diapositiva 15. Integración espacial

**Correspondencia con el libro.** Capítulo 3, integración; capítulo 4, visualización espacial y sus límites.

**Propósito.** Distinguir unión por identificador y relaciones geométricas.

**Guion sugerido.** Enumerar ID administrativo, punto en polígono, zona cercana e intersección. Registrar CRS, versión de límites y casos sin zona; advertir sobre centroides.

**Conceptos y términos.** *Sistema de referencia de coordenadas (CRS)*, *polígono*, *centroide*, *intersección espacial*.

**Ejemplo o acción en notebook.** El taller une viajes por `LocationID`; la extensión lee polígonos y convierte a EPSG:4326 para el mapa Folium.

**Error frecuente o límite.** Reemplazar cobertura por distancia a centroides o calcular centroides en coordenadas geográficas como medida precisa.

**Comprobación.** “¿El centroide usado para centrar el mapa redefine la zona?”. No; solo ayuda a la vista y genera una advertencia geométrica posible.

**Conclusión que debe quedar.** Una relación espacial debe declarar geometría, CRS, versión y casos no asignados.

**Transición sugerida.** “Después de alinear espacio y tiempo, agregaremos y haremos explícita la pérdida”.

## Diapositiva 16. Agregación y pérdida de información

**Correspondencia con el libro.** Capítulo 3, agregación y transformación; capítulo 4, resúmenes descriptivos.

**Propósito.** Explicar ganancias y pérdidas al pasar de eventos a grupos.

**Guion sugerido.** Leer conteo y media por grupo. Ganamos comparabilidad y volumen manejable; perdemos orden intra-grupo, variabilidad individual y reconstrucción de casos. Conservar conteos, dispersión, cobertura y regla.

**Conceptos y términos.** *Grupo*, *conteo*, *media*, *dispersión*, *pérdida irreversible*.

**Lectura de fórmulas.** En $n_g=\sum_i \mathbb{1}(G_i=g)$, la indicadora cuenta observaciones del grupo $g$. En $\bar{x}_g=\frac{1}{n_g}\sum_{i:G_i=g}x_i$, se promedian valores incluidos. Ambas expresiones dependen de reglas de inclusión y no recuperan eventos descartados ni prueban representatividad.

**Ejemplo o acción en notebook.** `groupby(...).size()` crea `pickups`; NOAA resume medias y suma precipitación con `min_count=1`, conservando `observaciones`.

**Error frecuente o límite.** Promediar precipitación cuando el significado requiere acumulación o convertir una hora enteramente ausente en cero.

**Comprobación.** Pedir qué ya no contiene `pickups_zona_hora`: importes, destinos y secuencia de viajes individuales.

**Conclusión que debe quedar.** Agregar es una decisión semántica con pérdidas documentables.

**Transición sugerida.** “Para defender esas decisiones, la adquisición y cada transformación deben poder repetirse”.

## Diapositiva 17. Reproducibilidad desde la adquisición

**Correspondencia con el libro.** Capítulo 2, §2.4 sobre reproducibilidad, organización y versionado; capítulo 3, controles documentados.

**Propósito.** Fijar los elementos que permiten reconstruir una ejecución.

**Guion sugerido.** Enumerar URL, acceso, periodo, parámetros, versiones, orden, validaciones, exclusiones, esquema, clave y procedencia. Presentar el notebook como registro ejecutable, no como garantía automática.

**Conceptos y términos.** *Reproducibilidad*, *parámetro*, *versión*, *artefacto*, *ejecución de inicio a fin*.

**Ejemplo o acción en notebook.** Mostrar `MODO_CLASE`, fechas, `ZONA_HORARIA`, funciones y aserciones. Pedir registrar fecha y entorno junto al producto.

**Error frecuente o límite.** Entregar un notebook con celdas fuera de orden o resultados sin código que los genere.

**Comprobación.** Reiniciar kernel y ejecutar todo; cada variable debe originarse antes de usarse y cada aserción debe pasar.

**Conclusión que debe quedar.** La reproducibilidad comienza al adquirir, no al guardar el gráfico final.

**Transición sugerida.** “Apliquemos ahora estas reglas a una pregunta concreta de movilidad y clima”.

## Diapositiva 18. Del concepto al taller

**Correspondencia con el libro.** Capítulos 2-4: formulación, preparación/integración y exploración descriptiva.

**Propósito.** Conectar el marco conceptual con la pregunta, las fuentes y la meta práctica.

**Guion sugerido.** Leer la pregunta exacta y el flujo TLC-zonas-zona-hora-clima. Aclarar que se construirá una tabla auditada, no un modelo predictivo, y que viajes reportados no equivalen a demanda.

**Conceptos y términos.** *Tabla analítica auditada*, *asociación descriptiva*, *viajes reportados*, *demanda no observada*.

**Descripción visual relevante.** El flujo `TLC viajes → zonas + shapefile → zona-hora ← NOAA clima` converge en zona-hora. La flecha desde NOAA indica enriquecimiento temporal; `zonas + shapefile` reúne atributos y geometría, no afirma que todo viaje tenga correspondencia ni que una estación represente cada zona.

**Ejemplo o acción en notebook.** Mostrar la pregunta guía y anticipar `zona_hora_clima`; pedir una hipótesis descriptiva sin cifras ni causalidad.

**Error frecuente o límite.** Convertir “asociación con clima” en “efecto del clima” o usar pickups como solicitudes totales.

**Comprobación.** “¿Entrenaremos un predictor?”. No; construiremos evidencia descriptiva y una tabla reproducible.

**Conclusión que debe quedar.** El taller prueba preparación e integración bajo límites explícitos.

**Transición sugerida.** “Definamos formalmente fuentes, unidades originales y especificación del producto”.

## Diapositiva 19. Taller 1: fuentes y definición analítica

**Correspondencia con el libro.** Capítulo 2, inventario de fuentes; capítulo 3, unidad, clave e integración.

**Propósito.** Declarar cuatro fuentes, unidades originales y producto antes de cargar.

**Guion sugerido.** Leer TLC viajes, lookup, shapefile y NOAA. Fijar una fila igual a zona de origen-hora local y clave `PULocationID, hora`.

**Conceptos y términos.** *Definición analítica*, *unidad original*, *clave compuesta*, *estación-observación*.

**Descripción visual relevante.** La tabla organiza fuente, archivo/tabla y unidad original; leer por filas y luego contrastar todas con la unidad final inferior. El cambio de unidad ocurre por transformación, no porque los archivos ya compartan granularidad.

**Ejemplo o acción en notebook.** Revisar “Ficha de fuentes” y completar metadatos. En el código, `pickup_hora` corresponde a `hora` y `pickups_zona_hora` materializa la especificación.

**Error frecuente o límite.** Confundir zona-ID del lookup con una observación de viaje o clima horario con clima zonal.

**Comprobación.** Pedir la cardinalidad esperada de viajes a zona: many-to-one.

**Conclusión que debe quedar.** Las fuentes heterogéneas solo se integran después de declarar unidades y clave final.

**Transición sugerida.** “Hagamos visible el periodo construyendo la URL en lugar de editar texto manualmente”.

## Diapositiva 20. Taller 2: construir la URL TLC

**Correspondencia con el libro.** Capítulo 2, adquisición parametrizada y reproducibilidad.

**Propósito.** Hacer explícitos tipo de servicio, año y mes.

**Guion sugerido.** Recorrer el diccionario de prefijos y el formato `anio-mes`. Explicar que parametrizar reduce errores manuales y registra intención.

**Conceptos y términos.** *Parámetro*, *plantilla de URL*, *validación de entrada*.

**Ejemplo o acción en notebook.** Ejecutar `construir_url_tlc("yellow", 2024, 1)`; destacar que el notebook además valida tipo, rango de año, rango de mes y excluye booleanos.

**Error frecuente o límite.** Aceptar cualquier texto como tipo o asumir que una URL bien formada garantiza disponibilidad y esquema.

**Comprobación.** Probar conceptualmente un mes fuera de rango: debe producir `ValueError`, no una URL silenciosa.

**Conclusión que debe quedar.** Parámetros validados hacen auditable qué recurso se solicitó.

**Transición sugerida.** “Con la dirección construida, leeremos solo periodo y columnas necesarios”.

## Diapositiva 21. Taller 3: cargar Parquet con proyección

**Correspondencia con el libro.** Capítulo 2, archivos, eficiencia y adquisición; capítulo 3, esquema.

**Propósito.** Cargar columnas y ventana explícitas sin leer indiscriminadamente.

**Guion sugerido.** Explicar proyección de columnas y filtro temporal. Parquet conserva tipos y `pyarrow` puede reducir lectura; la fuente sigue siendo secundaria y operativa.

**Conceptos y términos.** *Parquet*, *proyección*, *predicate pushdown/filtro de lectura*, *fuente secundaria*.

**Ejemplo o acción en notebook.** Ejecutar `COLUMNAS_VIAJES`, `filtros` y `pd.read_parquet`; observar el total real sin memorizarlo. `MODO_CLASE=True` fija una semana consecutiva.

**Error frecuente o límite.** Llamar muestra aleatoria a la primera semana o inferir representatividad mensual por menor volumen.

**Comprobación.** Resolver la pregunta breve: una ventana contigua conserva ciclos y denominador temporal, pero no garantiza representar el mes.

**Conclusión que debe quedar.** La adquisición eficiente debe preservar significado de selección y periodo.

**Transición sugerida.** “Antes de imponer reglas, inspeccionemos qué llegó realmente”.

## Diapositiva 22. Taller 4: inspeccionar antes de transformar

**Correspondencia con el libro.** Capítulo 3, perfilado, estructura y diccionario; capítulo 4, exploración inicial.

**Propósito.** Generar hipótesis sobre esquema, tipos, rangos y faltantes.

**Guion sugerido.** Revisar forma, primeras filas, `info`, tipos y tabla de faltantes. Preguntar qué representa una fila y qué columnas son IDs, tiempos o medidas.

**Conceptos y términos.** *Perfilado*, *esquema*, *rango observado*, *hipótesis de calidad*.

**Ejemplo o acción en notebook.** Ejecutar la sección 3; sustituye `describe(include="all")` de la lámina por un perfil explícito de tipos y ausencias adecuado al taller.

**Error frecuente o límite.** Convertir valores o eliminar filas durante la misma inspección y perder el estado original.

**Comprobación.** Pedir una hipótesis y su control: por ejemplo, duración no positiva se prueba calculando diferencia temporal.

**Conclusión que debe quedar.** Inspección propone preguntas; reglas booleanas las vuelven auditables.

**Transición sugerida.** “Materialicemos ahora esos controles sin borrar información”.

## Diapositiva 23. Taller 5: controles de calidad básicos

**Correspondencia con el libro.** Capítulo 3, perfiles, faltantes, duplicados y validez.

**Propósito.** Convertir dimensiones de calidad en métricas y señales verificables.

**Guion sugerido.** Presentar nulos, aproximación de duplicados y duración. Aclarar que la combinación de clave no es ID oficial y que los resultados dependen de datos/filtros.

**Conceptos y términos.** *Control de calidad (QC)*, *máscara booleana*, *clave operativa*, *duración no positiva*.

**Ejemplo o acción en notebook.** El notebook amplía la lámina: calcula `duracion_min`, crea columnas `ok_*` y una `auditoria` con cumplen/incumplen.

**Error frecuente o límite.** Interpretar `duplicados_clave` como número cierto de viajes repetidos o sumar incumplimientos como si fueran filas distintas.

**Comprobación.** Verificar que cada regla pueda señalarse por separado y que una fila puede incumplir más de una.

**Conclusión que debe quedar.** Un control útil hace visible su definición y no exagera lo que detecta.

**Transición sugerida.** “Pasemos de diagnosticar a decidir qué registros cumplen el criterio operativo”.

## Diapositiva 24. Taller 6: validez y filtros explícitos

**Correspondencia con el libro.** Capítulo 3, limpieza, rangos, consistencia y documentación de exclusiones.

**Propósito.** Aplicar reglas explícitas conservando rechazados y sensibilidad.

**Guion sugerido.** Explicar cada máscara y sus umbrales como criterios analíticos. Separar válidos y rechazados; no borrar en sitio. Reportar exclusiones por regla desde la ejecución.

**Conceptos y términos.** *Validez*, *plausibilidad*, *umbral*, *sensibilidad*, *exclusión documentada*.

**Ejemplo o acción en notebook.** Ejecutar `registro_valido`, `viajes_rechazados` y `viajes_validos`. Resolver Ejercicio 1 con una máscara de 50 millas sin modificar el producto.

**Error frecuente o límite.** Llamar falso a todo valor extremo o escoger umbrales después de mirar el resultado deseado.

**Comprobación.** Confirmar que `viajes_rechazados` conserva filas y columnas `ok_*`; comparar definiciones, no anticipar totales.

**Conclusión que debe quedar.** Filtrar requiere regla, justificación, conteo y conservación de evidencia excluida.

**Transición sugerida.** “La pertenencia de los IDs al catálogo se comprobará mediante una unión validada”.

## Diapositiva 25. Taller 7: zonas y unión many-to-one

**Correspondencia con el libro.** Capítulo 3, claves, cardinalidad e integración.

**Propósito.** Enriquecer pickup y dropoff sin multiplicar viajes.

**Guion sugerido.** Comprobar unicidad del catálogo, renombrar por rol y unir dos veces con `many_to_one`. Explicar por qué pickup y dropoff no son intercambiables.

**Conceptos y términos.** *Tabla de referencia*, *rol de clave*, *many-to-one*, *enriquecimiento*.

**Ejemplo o acción en notebook.** Ejecutar `zonas_pickup`, `zonas_dropoff` y `viajes_zonas`; revisar el `assert` de longitud.

**Error frecuente o límite.** Unir dos veces sin renombrar y confundir columnas, o no verificar unicidad antes de `merge`.

**Comprobación.** Si la longitud cambia, detener la clase y diagnosticar cardinalidad; no continuar hacia gráficos.

**Conclusión que debe quedar.** La misma dimensión puede cumplir roles distintos y cada unión necesita una especificación.

**Transición sugerida.** “Conservar filas no implica que todas hayan encontrado nombre de zona; midamos cobertura”.

## Diapositiva 26. Taller 8: cobertura y pérdidas de la unión

**Correspondencia con el libro.** Capítulo 3, auditoría de integración y faltantes derivados.

**Propósito.** Separar conservación de filas y cobertura semántica.

**Guion sugerido.** Una unión izquierda conserva viajes, pero puede dejar atributos nulos. Medir coincidencias/no coincidencias y revisar IDs sin zona.

**Conceptos y términos.** *Left join*, *left-only*, *cobertura semántica*, *multiplicación*.

**Ejemplo o acción en notebook.** El notebook mide `sin_nombre_pickup` y `sin_nombre_dropoff`; el `assert` controla filas. Explicar que podría usarse `indicator=True` para la auditoría mostrada en la lámina.

**Error frecuente o límite.** Concluir cobertura completa solo porque el número de filas no cambió.

**Comprobación.** Pedir interpretar por separado longitud estable y nombres ausentes; responden a riesgos distintos.

**Conclusión que debe quedar.** La auditoría de unión requiere cardinalidad y cobertura.

**Transición sugerida.** “El catálogo aporta nombres; para representar límites necesitamos geometría”.

## Diapositiva 27. Taller 9: shapefile y geometría

**Correspondencia con el libro.** Capítulo 3, integración espacial; capítulo 4, mapas.

**Propósito.** Incorporar polígonos de zonas como extensión espacial separada del lookup.

**Guion sugerido.** Distinguir nombres y geometría; convertir `LocationID`, fijar CRS y comprobar unicidad. La geometría no debe sustituirse por centroides para cobertura.

**Conceptos y términos.** *Shapefile*, *ZIP*, *GeoDataFrame*, *EPSG:4326*, *mapa coroplético*.

**Ejemplo o acción en notebook.** Ejecutar la extensión opcional si están `geopandas`, `folium` y `requests`; el ZIP vive en `TemporaryDirectory` y no se añade al repo.

**Error frecuente o límite.** Hacer obligatoria la extensión cuando faltan dependencias o interpretar el centro visual como ubicación exacta de actividad.

**Comprobación.** Verificar mensaje explícito si faltan dependencias y, si se ejecuta, unicidad implícita mediante `validate="one_to_one"` al unir conteos.

**Conclusión que debe quedar.** Geometría y atributos cumplen funciones complementarias y tienen metadatos propios.

**Transición sugerida.** “Volvamos al eje central: cambiar la unidad desde viaje a zona-hora”.

## Diapositiva 28. Taller 10: construir zona-hora

**Correspondencia con el libro.** Capítulo 3, transformación y agregación; capítulo 4, series y resúmenes.

**Propósito.** Localizar tiempo, redondear por hora y agregar pickups con clave única.

**Guion sugerido.** Mostrar localización TLC, `floor("h")` y agrupación. Explicar que una fila nueva resume muchos viajes y elimina detalle individual.

**Conceptos y términos.** *Localización temporal*, *hora local*, *floor*, *groupby*, *clave compuesta*.

**Ejemplo o acción en notebook.** Ejecutar `pickup_hora` y `pickups_zona_hora`; el notebook conserva borough y nombre además de ID, y comprueba duplicados de `pickup_hora, PULocationID`.

**Error frecuente o límite.** Sumar una tabla que ya está agregada como si cada fila siguiera siendo viaje, o localizar dos veces una serie.

**Comprobación.** La aserción de clave debe pasar; pedir explicar por qué `pickups` es conteo de reportes, no demanda.

**Conclusión que debe quedar.** La tabla zona-hora tiene nueva unidad, clave y alcance.

**Transición sugerida.** “Para enriquecer cada hora, primero interpretaremos correctamente el reloj NOAA”.

## Diapositiva 29. Taller 11: NOAA e interpretación UTC

**Correspondencia con el libro.** Capítulos 2 y 3, adquisición, tipos temporales e integración.

**Propósito.** Cargar clima y convertir instantes UTC a hora local.

**Guion sugerido.** Leer el PSV, verificar estación, parsear `DATE` con `utc=True` y convertir a Nueva York. Repetir que convertir un instante no es cambiar una etiqueta.

**Conceptos y términos.** *PSV*, *estación meteorológica*, *UTC*, *tz_convert*.

**Ejemplo o acción en notebook.** Ejecutar `urlopen`, `clima_bruto`, `fecha_utc` y `fecha_ny`; observar errores de conversión como faltantes mediante `errors="coerce"`.

**Error frecuente o límite.** Tratar `DATE` como hora local o asumir que una estación representa espacialmente todas las zonas.

**Comprobación.** Revisar que `fecha_utc` y `fecha_ny` expresan los mismos instantes con zonas distintas.

**Conclusión que debe quedar.** La semántica temporal debe resolverse antes de agrupar y unir.

**Transición sugerida.** “Resumamos las observaciones subhorarias con reglas específicas por variable”.

## Diapositiva 30. Taller 12: clima horario de enero

**Correspondencia con el libro.** Capítulo 3, tipos, faltantes y agregación; capítulo 4, resúmenes temporales.

**Propósito.** Filtrar la ventana local y producir una fila meteorológica por hora.

**Guion sugerido.** Convertir variables a numéricas, agrupar por hora, usar medias donde corresponde y suma para precipitación con `min_count=1`; conservar número de observaciones.

**Conceptos y términos.** *Observación subhoraria*, *agregación variable-específica*, *cobertura temporal*, *intervalo semiabierto*.

**Ejemplo o acción en notebook.** Ejecutar `clima_horario` y resolver Ejercicio 2 comparando `horas_esperadas` con horas observadas.

**Error frecuente o límite.** Convertir ausencia total de precipitación en cero o suponer frecuencia constante sin consultar documentación NOAA.

**Comprobación.** Verificar unicidad de `hora` y leer los huecos que realmente arroje la ejecución, sin anticiparlos.

**Conclusión que debe quedar.** El resumen horario debe conservar regla y cobertura, no solo medias.

**Transición sugerida.** “Con ambos lados a la misma granularidad temporal, validemos su integración”.

## Diapositiva 31. Taller 13: unir zona-hora con clima

**Correspondencia con el libro.** Capítulo 3, integración, cardinalidad y cobertura.

**Propósito.** Enriquecer muchas zonas-hora con como máximo una observación climática por hora.

**Guion sugerido.** Comprobar unicidad climática, unir a izquierda con `many_to_one`, conservar filas y medir `_merge`/faltantes. Explicitar el supuesto espacial de una estación.

**Conceptos y términos.** *Many-to-one temporal*, *indicador de unión*, *representatividad espacial*.

**Ejemplo o acción en notebook.** Ejecutar `zona_hora_clima` y `auditoria_union`; el notebook elimina `_merge` solo después de mostrar la auditoría.

**Error frecuente o límite.** Correlacionar directamente la tabla sin recordar que el clima se repite por zona o imputar huecos sin justificarlos.

**Comprobación.** Confirmar longitud izquierda estable y revisar categorías reales de la auditoría.

**Conclusión que debe quedar.** La unión es técnicamente many-to-one y conceptualmente depende de un supuesto espacial fuerte.

**Transición sugerida.** “Leamos ahora el patrón temporal como descripción de reportes”.

## Diapositiva 32. Taller 14: perfil horario de viajes reportados

**Correspondencia con el libro.** Capítulo 4, series, perfiles y visualización descriptiva.

**Propósito.** Describir variación temporal sin convertirla en demanda o pronóstico.

**Guion sugerido.** Leer ejes, unidad, ventana y filtros antes del patrón. Comparar serie por hora y mapa de calor día-hora disponibles en el notebook.

**Conceptos y términos.** *Perfil horario*, *serie temporal*, *ciclo diario*, *mapa de calor*.

**Ejemplo o acción en notebook.** Ejecutar `viajes_por_hora` y `patron`; describir picos y valles solo según lo visible en la ejecución.

**Descripción visual relevante.** La línea ordena conteos por hora local; el mapa de calor organiza días en filas y horas en columnas, con color como cantidad. Ninguno muestra solicitudes no atendidas ni controla por oferta.

**Error frecuente o límite.** Generalizar una semana a todo enero o atribuir un pico a una causa no observada.

**Comprobación.** Pedir una frase completa: variable, unidad, periodo y carácter descriptivo.

**Conclusión que debe quedar.** El perfil caracteriza viajes Yellow Taxi reportados dentro de la ventana filtrada.

**Transición sugerida.** “La dimensión temporal puede complementarse con la distribución espacial”.

## Diapositiva 33. Taller 15: mapa por zona

**Correspondencia con el libro.** Capítulo 4, visualización espacial; capítulo 3, integración geométrica.

**Propósito.** Comparar conteos por zona conservando cautelas de cobertura y escala.

**Guion sugerido.** Agregar por `PULocationID`, unir one-to-one con polígonos y representar ausencias. Explicar que conteos mezclan tamaño, actividad, cobertura y registro.

**Conceptos y términos.** *Coropleta*, *conteo zonal*, *geometría sin dato*, *comparabilidad espacial*.

**Ejemplo o acción en notebook.** Usar barras `top_zonas` como vista base y Folium como extensión opcional. Leer valores reales del entorno, no una lista fija de zonas.

**Descripción visual relevante.** En barras, longitud representa pickups y solo aparece el subconjunto superior; en el mapa, color rellena polígonos según conteo y no densidad. Áreas grandes captan más atención visual sin implicar más viajes por superficie.

**Error frecuente o límite.** Interpretar color como preferencia individual o comparar conteos brutos como tasas.

**Comprobación.** Preguntar qué denominador faltaría para una tasa: población, superficie, oferta u otro, según la pregunta; ninguno se incorpora automáticamente.

**Conclusión que debe quedar.** Un mapa de conteos localiza registros, no explica por sí solo su distribución.

**Transición sugerida.** “Finalmente, exploremos clima y pickups sin saltar de asociación a causalidad”.

## Diapositiva 34. Taller 16: clima y asociación descriptiva

**Correspondencia con el libro.** Capítulo 4, dispersión, correlación, exploración y comunicación de límites.

**Propósito.** Explorar asociación horaria evitando repetición del clima por zona y lenguaje causal.

**Guion sugerido.** Volver primero a una fila por hora, sumar pickups y tomar una sola observación climática. Leer dispersión y correlación como asociación lineal condicionada por selección y calendario.

**Conceptos y términos.** *Diagrama de dispersión*, *correlación*, *factor de confusión*, *unidad horaria*.

**Ejemplo o acción en notebook.** Ejecutar `comparacion_horaria`, los dos gráficos y la matriz de correlación; resolver Ejercicio 3 con dos observaciones y una explicación alternativa.

**Descripción visual relevante.** Cada punto representa una hora, no una zona ni un viaje. Los paneles comparan pickups con temperatura y precipitación; cercanía o pendiente aparente no identifica mecanismo causal.

**Error frecuente o límite.** Calcular correlación sobre clima replicado por zona o afirmar “la lluvia provoca” a partir de puntos observacionales.

**Comprobación.** Exigir mencionar al menos un confusor: hora, día, aeropuerto, feriado, oferta, eventos o selección.

**Conclusión que debe quedar.** Correlación resume asociación en la ventana; no demuestra causalidad ni transportabilidad.

**Transición sugerida.** “Guardemos el producto junto con la información necesaria para reconstruirlo”.

## Diapositiva 35. Taller 17: guardar un producto reproducible

**Correspondencia con el libro.** Capítulo 2, organización, metadatos y versionado; capítulo 3, producto preparado.

**Propósito.** Materializar tabla ordenada, clave única y metadatos mínimos.

**Guion sugerido.** Ordenar por hora e ID, comprobar clave, exportar Parquet y registrar unidad, zona horaria y fuentes. Adjuntar controles, exclusiones, versiones y fecha.

**Conceptos y términos.** *Artefacto reproducible*, *metadatos*, *esquema*, *clave única*, *fecha de ejecución*.

**Ejemplo o acción en notebook.** Adaptar la lámina a nombres reales: ordenar `zona_hora_clima` por `pickup_hora, PULocationID`, comprobar no duplicidad y exportar al directorio temporal. Verificar que el nombre indique `primera_semana_enero_2024` con `MODO_CLASE=True` o `enero_2024` en modo completo.

**Error frecuente o límite.** Escribir el dataset generado dentro del repositorio, omitir el modo de ejecución o guardar una tabla con resultados de celdas fuera de orden.

**Comprobación.** Recargar el Parquet desde su ubicación externa y comprobar esquema, clave y rango temporal contra los parámetros, sin exigir un conteo fijo.

**Conclusión que debe quedar.** Un archivo solo es producto reproducible si viaja con especificación, controles y procedencia.

**Transición sugerida.** “Reunamos ahora los artefactos que demostrarán el aprendizaje”.

## Diapositiva 36. Producto y evidencia de aprendizaje

**Correspondencia con el libro.** Capítulo 2, productos y reproducibilidad; capítulo 3, auditoría; capítulo 4, evidencia visual.

**Propósito.** Definir un entregable verificable y defendible.

**Guion sugerido.** Recorrer inventario, regla de fila, diccionario, controles, tabla, visualizaciones, cinco hallazgos y tres límites. Aplicar la rúbrica de esta guía y exigir ejecución ordenada.

**Conceptos y términos.** *Entregable*, *evidencia de aprendizaje*, *diccionario semántico*, *hallazgo con evidencia*.

**Ejemplo o acción en notebook.** Entregar el notebook ejecutado de inicio a fin y el Parquet fuera del repo o como descarga separada. Los hallazgos deben citar tabla/gráfico y ventana real.

**Descripción visual relevante.** La composición es una lista de seis evidencias complementarias; no es una secuencia ni permite sustituir auditoría por gráficos. La tabla y el notebook sostienen los hallazgos, mientras los límites acotan su lectura.

**Error frecuente o límite.** Entregar capturas sin código, cinco opiniones sin evidencia o un mapa como sustituto de controles de cardinalidad.

**Comprobación.** Seleccionar una fila del producto y reconstruir fuentes, filtros, uniones y agregación que la originaron.

**Conclusión que debe quedar.** El aprendizaje se demuestra mediante trazabilidad, controles e interpretación, no por una cifra particular.

**Transición sugerida.** “Antes de cerrar, fijemos qué afirmaciones permite y cuáles prohíbe este diseño”.

## Diapositiva 37. Límites y afirmaciones permitidas

**Correspondencia con el libro.** Capítulo 2, alcance y riesgo; capítulo 3, cobertura; capítulo 4, interpretación descriptiva.

**Propósito.** Restringir conclusiones a población, periodo, fuentes y diseño observacional.

**Guion sugerido.** Afirmar únicamente descripción de viajes reportados y asociaciones en la cobertura analizada. Negar demanda total, generalización universal, causalidad, clima zonal idéntico y exactitud individual garantizada.

**Conceptos y términos.** *Alcance*, *cobertura*, *validez descriptiva*, *causalidad*, *representatividad*.

**Ejemplo o acción en notebook.** Revisar “Conclusiones y límites”; añadir explícitamente el alcance de `MODO_CLASE` usado y cualquier hueco observado de NOAA o zona.

**Error frecuente o límite.** Redactar el límite como fórmula vacía después de una conclusión exagerada, o usar “podría causar” para insinuar causalidad no identificada.

**Comprobación.** Reformular “la lluvia reduce/aumenta la demanda” como “en las horas observadas, pickups reportados y precipitación muestran la asociación visible, confundida por...”. La dirección se completa solo desde el resultado real.

**Conclusión que debe quedar.** Los límites forman parte de la evidencia y determinan el lenguaje permitido.

**Transición sugerida.** “Cerremos reconstruyendo las seis decisiones que convierten datos disponibles en evidencia defendible”.

## Diapositiva 38. Cierre: de datos disponibles a evidencia defendible

**Correspondencia con el libro.** Síntesis de capítulos 2, 3 y 4.

**Propósito.** Consolidar formulación, representación, calidad, integración, agregación y reproducibilidad.

**Guion sugerido.** Recuperar las seis ideas en el orden de la lámina: propósito/producto; fuente/unidad/fila; tipos/faltantes/duplicados; claves/cardinalidad/cobertura; tiempo/espacio/agregación; pérdidas/límites/cadena reproducible. Conectar cada una con un objeto del notebook.

**Conceptos y términos.** No introducir vocabulario nuevo; integrar definición, procedencia, calidad apta, cardinalidad, granularidad y límites.

**Ejemplo o acción en notebook.** Cerrar con la pregunta final: qué dato permitiría distinguir mejor demanda, oferta y viajes realizados. Aceptar propuestas justificadas por unidad, disponibilidad y procedencia.

**Descripción visual relevante.** La lista numerada es una secuencia de controles acumulativos, no una receta rígida. La línea final enlaza capítulos 2-4 y anticipa exploración estadística sin ampliar lo que representan los datos.

**Error frecuente o límite.** Terminar mostrando solo gráficos o presentar preparación como fase acabada que ya no requiere revisión.

**Comprobación.** Pedir a cada estudiante una decisión del flujo, su comprobación y el límite que permanece.

**Conclusión que debe quedar.** La evidencia defendible conserva significado, controles, pérdidas, procedencia y alcance desde la adquisición hasta el producto.

**Transición sugerida.** “La próxima etapa profundizará la exploración estadística sin exceder la representación construida hoy”.

### Referencias

- `../../../Libro/Capitulo_02_Ciclo_de_vida_de_un_proyecto_de_datos.md`
- `../../../Libro/Capitulo_03_Preparacion_calidad_y_transformacion_de_datos.md`
- `../../../Libro/Capitulo_04_Estadistica_descriptiva_exploracion_y_visualizacion.md`
- `Clase_02_Adquisicion_comprension_y_preparacion_inicial_de_datos.md`
- `Taller_Clase_02_Movilidad.ipynb`
