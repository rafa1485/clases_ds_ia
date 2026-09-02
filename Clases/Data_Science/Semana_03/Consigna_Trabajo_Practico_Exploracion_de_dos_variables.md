<style>
@page { size: A4; margin: 16mm 16mm 17mm 16mm; }
body { font-family: "DejaVu Sans", sans-serif; color: #17324d; line-height: 1.36; font-size: 10pt; }
h1 { color: #17324d; border-bottom: 4px solid #007f82; padding-bottom: 8px; }
h2 { color: #17324d; border-bottom: 2px solid #e2a33a; padding-bottom: 4px; margin: 20px 0 8px; page-break-after: avoid; }
h3 { color: #007f82; margin: 13px 0 4px; page-break-after: avoid; }
p { margin: 6px 0; }
ul, ol { margin-top: 4px; margin-bottom: 8px; }
blockquote { border-left: 4px solid #e2a33a; background: #f3f6f8; margin: 10px 0; padding: 8px 12px; page-break-inside: avoid; }
table { border-collapse: collapse; width: 100%; font-size: 8.6pt; page-break-inside: avoid; }
th { background: #17324d; color: white; }
th, td { border: 1px solid #aab7c1; padding: 6px; vertical-align: top; }
code { color: #007f82; }
pre { background: #f3f6f8; border: 1px solid #aab7c1; padding: 8px; white-space: pre-wrap; page-break-inside: avoid; }
strong { color: #17324d; }
.formula { text-align: center; font-size: 12pt; background: #f3f6f8; border: 1px solid #aab7c1; padding: 7px; page-break-inside: avoid; }
.page-break { page-break-before: always; }
</style>

# Trabajo práctico: exploración de dos variables

**Curso:** Data Science  
**Semana y clase:** semana 3, clase 3  
**Notebook base:** `Taller_Clase_02_Movilidad.ipynb`  
**Periodo principal:** enero de 2024 completo  
**Modalidad:** individual

## Propósito

Cada estudiante trabajará con un **par de columnas preaprobado** de la tabla preparada en el notebook de la clase 2. Primero deberá comprender y explorar cada variable por separado. Después evaluará la forma en que ambas variables se relacionan, sin convertir una asociación descriptiva en una explicación causal.

El trabajo debe responder tres preguntas:

1. ¿Cómo varía cada columna durante el periodo estudiado?
2. ¿Qué valores faltantes, ceros, extremos o casos potencialmente anómalos aparecen?
3. ¿Qué relación se observa entre las dos columnas y bajo qué límites puede sostenerse?

> El objetivo no es encontrar una correlación alta ni confirmar una historia previa. El objetivo es construir una descripción trazable, revisar explicaciones alternativas y comunicar qué permiten afirmar los registros.

## 1. Preparación del trabajo

1. Crear una copia personal de `Taller_Clase_02_Movilidad.ipynb`.
2. Cambiar la configuración a `MODO_CLASE = False` para procesar enero completo.
3. Ejecutar todas las celdas en orden hasta construir la tabla `producto`.
4. Confirmar que el periodo sea `[2024-01-01, 2024-02-01)` en la zona `America/New_York`.
5. Agregar al final del notebook una sección titulada `Trabajo práctico: exploración de dos variables`.
6. Registrar el par asignado y la vista analítica obligatoria antes de observar los resultados.
7. No modificar silenciosamente el periodo, las fuentes ni las reglas de calidad del notebook base.

La tabla `producto` representa una **zona de origen con al menos un pickup registrado durante una hora local**. Su clave es `pickup_hora` junto con `PULocationID`. Los registros TLC representan viajes Yellow Taxi realizados y reportados que superaron los filtros; no representan demanda total ni solicitudes no atendidas.

## 2. Vistas analíticas obligatorias

No todos los pares pueden estudiarse directamente sobre las filas de `producto`. Cada par se entrega junto con una vista que fija la unidad del análisis.

| Código | Vista | Unidad analítica | Uso |
|---|---|---|---|
| H | Horaria | una hora de enero | pares que incluyen clima o pickups totales |
| ZH | Zona-hora activa | una zona-hora con al menos un pickup | comparación de pickups entre boroughs |
| T | Temporal horaria | una hora ordenada cronológicamente | evolución temporal de una medida |

### Vista H: una fila por hora

Las variables NOAA corresponden a una sola estación y se repiten en todas las zonas activas de una hora. Antes de analizar un par con clima se debe volver a una fila por hora:

- sumar `pickups`, porque cada zona aporta viajes distintos;
- conservar una sola observación de cada variable NOAA;
- comprobar que una variable NOAA tenga como máximo un valor distinto por hora entre las zonas;
- mantener las horas sin clima como faltantes, no convertirlas automáticamente en cero.

La operación esperada sigue esta estructura, que debe completarse y verificarse en el notebook:

```python
por_hora = producto.groupby("pickup_hora", as_index=False).agg(
    pickups=("pickups", "sum"),
    temperatura_c=("temperatura_c", "first"),
    humedad_relativa=("humedad_relativa", "first"),
    viento=("viento", "first"),
    precipitacion_mm=("precipitacion_mm", "first"),
    visibilidad=("visibilidad", "first"),
)
```

Usar `first` solo después de comprobar la consistencia horaria. Eliminar filas duplicadas sin explicar su origen no constituye esa comprobación.

### Vista ZH: zona-hora activa

El producto del notebook no contiene una grilla completa de todas las zonas y horas. Por ello, una comparación geográfica deberá formularse así:

> Distribución de pickups entre las zona-horas que tuvieron al menos un pickup registrado durante enero de 2024.

La ausencia de una fila no puede convertirse automáticamente en `pickups = 0`. Si se decide construir una grilla completa, deberá justificarse el marco esperado y documentarse por separado esa transformación.

### Vista T: serie temporal

La columna `pickup_hora` se utiliza como eje ordenado. No corresponde convertir el timestamp a un número y calcular una correlación convencional. Deben estudiarse orden, ciclos, huecos, cambios y calendario.

## 3. Pares preaprobados

El docente asignará uno de los siguientes pares. Un mismo par puede ser trabajado por más de un estudiante.

### Pickups y clima

| Código | Columna 1 | Columna 2 | Vista |
|---|---|---|---|
| PC-01 | `pickups` | `temperatura_c` | H |
| PC-02 | `pickups` | `humedad_relativa` | H |
| PC-03 | `pickups` | `viento` | H |
| PC-04 | `pickups` | `visibilidad` | H |

### Relaciones meteorológicas

| Código | Columna 1 | Columna 2 | Vista |
|---|---|---|---|
| CM-01 | `temperatura_c` | `humedad_relativa` | H |
| CM-02 | `temperatura_c` | `viento` | H |
| CM-03 | `temperatura_c` | `visibilidad` | H |
| CM-04 | `viento` | `visibilidad` | H |

### Geografía y tiempo

| Código | Columna 1 | Columna 2 | Vista |
|---|---|---|---|
| GT-01 | `pickup_borough` | `pickups` | ZH |
| GT-02 | `pickup_hora` | `pickups` | T, con pickups totales por hora |
| GT-03 | `pickup_hora` | `temperatura_c` | T |
| GT-04 | `pickup_hora` | `humedad_relativa` | T |
| GT-05 | `pickup_hora` | `viento` | T |
| GT-06 | `pickup_hora` | `visibilidad` | T |

### Pares condicionales con precipitación

`precipitacion_mm` no se asignará como par preaprobado mientras no se auditen la duración, procedencia, frecuencia y banderas de calidad de los reportes GHCNh. Sumar observaciones subhorarias puede duplicar acumulaciones si representan periodos superpuestos.

Solo después de documentar que la agregación produce una cantidad horaria defendible podrán habilitarse pares de precipitación con `pickups`, humedad, viento, visibilidad o `pickup_hora`. Si esa auditoría no puede completarse, la columna se conserva como dato pendiente de interpretación y no se utiliza para estudiar relaciones.

## 4. Pares que no deben utilizarse

| Par o uso | Motivo |
|---|---|
| `pickup_hora` con `hora` | son claves temporales redundantes; `hora` también refleja el éxito de la unión |
| `PULocationID` con una numérica mediante correlación | el identificador es nominal, no una magnitud |
| `PULocationID` con `pickup_zone` o `pickup_borough` | relación de catálogo, no asociación empírica |
| `pickup_zone` con `pickup_borough` | relación jerárquica casi determinista |
| clima con zona o borough sobre `producto` | NOAA no varía espacialmente; el valor horario está replicado |
| dos variables NOAA directamente sobre `producto` | produce pseudorreplicación por zona activa |
| `observaciones` como intensidad climática | cuenta reportes NOAA, no magnitud meteorológica |

<div class="page-break"></div>

## 5. Contrato del análisis

Antes de calcular estadísticas, completar:

| Campo | Respuesta del estudiante |
|---|---|
| Código y par asignado | |
| Pregunta exploratoria | |
| Significado de la primera columna | |
| Significado de la segunda columna | |
| Tipo semántico de cada columna | |
| Unidad analítica y vista | |
| Periodo y zona horaria | |
| Población registrada | |
| Denominador o tamaño válido | |
| Afirmaciones que los datos no permiten | |

La pregunta debe nombrar las variables y el alcance. Por ejemplo, no preguntar “¿cómo afecta el clima a la demanda?”, porque TLC no mide demanda total y el diseño no identifica efectos causales.

## 6. Exploración individual de cada columna

Realizar primero el EDA de la columna 1 y luego repetirlo para la columna 2. No comenzar por el coeficiente de correlación.

### 6.1. Comprensión y cobertura

Para cada columna:

1. Explicar qué representa y en qué unidad está expresada.
2. Mostrar su tipo de dato físico y su tipo semántico.
3. Informar filas totales, valores válidos y faltantes.
4. Contar valores únicos cuando corresponda.
5. Distinguir cero, faltante y ausencia de fila.
6. Revisar valores mínimos y máximos contra el dominio de la variable.
7. Declarar si la variable fue agregada y mediante qué operación.

### 6.2. Distribución

Para una variable numérica, incluir cuando sean interpretables:

- mínimo y máximo;
- media y mediana;
- cuartiles e IQR;
- desviación estándar;
- proporción de ceros;
- histograma con resolución justificada;
- caja o violín como vista complementaria.

Para una variable categórica, incluir:

- frecuencia absoluta y relativa;
- faltantes y categorías poco frecuentes;
- tamaño de cada grupo;
- barras ordenadas o una tabla legible.

Para una variable temporal, incluir:

- cobertura desde la primera hasta la última hora;
- horas esperadas y observadas;
- huecos;
- evolución y ciclos por hora del día o día de semana.

Cada gráfico debe incluir título, ejes, unidad, periodo y una frase que explique qué comparación facilita.

## 7. Casos potencialmente anómalos

Una regla estadística genera candidatos para revisión, no errores confirmados. Para una variable numérica puede utilizarse la regla de Tukey:

<p class="formula">[Q<sub>1</sub> - 1.5 IQR, Q<sub>3</sub> + 1.5 IQR]</p>

El estudiante deberá:

1. declarar la regla utilizada;
2. contar los casos señalados;
3. mostrar una tabla con valor, fecha, hora y contexto disponible;
4. comprobar si el valor viola el dominio o solo es extremo;
5. proponer explicaciones alternativas;
6. conservarlo, excluirlo o corregirlo únicamente con justificación trazable;
7. comparar al menos un resumen con y sin esos casos.

Para precipitación, un cero válido no es un faltante. Para pickups, una hora o zona extrema puede reflejar aeropuerto, evento, calendario, oferta, error de agregación u otra condición no observada.

## 8. Relación entre las columnas

### 8.1. Dos variables numéricas

1. Construir un diagrama de dispersión.
2. Examinar dirección, forma, curvatura, grupos, sobreposición y puntos influyentes.
3. Calcular Pearson solo si interesa la relación lineal.
4. Calcular Spearman si interesa una relación monotónica o la forma y los extremos desaconsejan limitarse a Pearson.
5. Comparar los resultados con y sin los casos señalados, sin eliminar observaciones automáticamente.

### 8.2. Una variable categórica y una numérica

1. Informar tamaño y cobertura de cada grupo.
2. Comparar mediana, IQR y, cuando corresponda, media y desviación.
3. Utilizar cajas, violines o puntos con una escala común.
4. Evitar interpretar una diferencia descriptiva como efecto del grupo.

### 8.3. Una variable temporal y una numérica

1. Ordenar cronológicamente.
2. Representar la serie sin unir artificialmente huecos.
3. Examinar ciclos por hora del día y día de semana.
4. Señalar cambios, extremos y periodos sin cobertura.
5. No correlacionar directamente el timestamp con la medida.

### 8.4. Dependencia y explicaciones alternativas

Las horas consecutivas no son observaciones independientes. En la vista ZH, una misma zona aporta mediciones repetidas y todas las zonas activas de una hora comparten condiciones temporales. El número de zona-horas no debe interpretarse como cantidad de réplicas independientes. Las relaciones pueden estar asociadas con hora pico, día de semana, feriados, aeropuertos, eventos, disponibilidad de taxis, cobertura de datos o tendencias compartidas.

Si el par incluye NOAA, recordar que todas las variables proceden de una estación. Reducir a una fila por hora corrige la repetición artificial entre zonas, pero no elimina dependencia temporal ni convierte la estación en clima zonal.

## 9. Análisis de sensibilidad

Repetir una decisión del análisis bajo una alternativa razonable. Elegir al menos una:

- comparar media y mediana;
- comparar Pearson y Spearman;
- variar justificadamente el ancho de los intervalos del histograma;
- comparar resultados con y sin casos extremos identificados;
- estratificar por hora del día o día de semana;
- cambiar una agregación y explicar cómo cambia el estimando.

La alternativa debe definirse antes de conocer cuál produce el resultado más llamativo.

## 10. Hallazgos finales

Redactar como mínimo:

1. un hallazgo sobre la primera variable;
2. un hallazgo sobre la segunda variable;
3. un hallazgo sobre su relación.

Cada hallazgo debe contener:

- contrato: población, unidad y periodo;
- observación respaldada por una tabla o figura;
- cobertura, faltantes y denominador;
- interpretación proporcional a la evidencia;
- explicación alternativa;
- límite;
- siguiente comprobación posible.

Usar expresiones como “se observa”, “se relaciona” o “se asocia”. No utilizar “produce”, “provoca”, “explica” o “causa” sin un diseño adicional que lo permita.

## 11. Producto esperado

Entregar una copia ejecutable del notebook con:

- identificación del estudiante y del par asignado;
- ejecución reproducible para enero completo;
- contrato del análisis;
- construcción y validación de la vista requerida;
- dos análisis univariados;
- tabla de casos potencialmente anómalos;
- análisis bivariado;
- al menos tres visualizaciones interpretadas;
- análisis de sensibilidad;
- tres hallazgos finales;
- límites y próximos pasos.

No se evalúa la obtención de un resultado predeterminado. Dos análisis pueden llegar a conclusiones diferentes si documentan correctamente su unidad, transformaciones, evidencia y alcance.

<div class="page-break"></div>

# Actividad EXTRA: estabilidad de la relación durante seis meses

**Carácter:** opcional  
**Periodo ampliado:** enero a junio de 2024  
**Fin exclusivo:** `2024-07-01`

## 12. Objetivo de la actividad extra

Ampliar el análisis a seis meses de TLC y evaluar si las distribuciones, los casos anómalos y la relación identificada en enero se mantienen al incorporar nuevos periodos.

No se busca obtener una correlación mayor ni confirmar causalidad. Se estudiará la **estabilidad temporal** del hallazgo bajo las mismas definiciones y reglas.

## 13. Procesamiento mensual y concatenación

Procesar los archivos Yellow Taxi de enero, febrero, marzo, abril, mayo y junio de 2024.

No cargar simultáneamente los seis archivos crudos. Para cada mes:

1. construir la URL mediante `construir_url_tlc("yellow", 2024, mes)`;
2. leer únicamente las columnas requeridas por el flujo de calidad;
3. filtrar por límites mensuales conscientes de `America/New_York`;
4. aplicar las mismas reglas de validez;
5. registrar filas leídas dentro de la ventana, válidas y rechazadas;
6. enriquecer zonas con una única copia identificada del catálogo;
7. agregar a zona-hora;
8. añadir `mes_fuente`, `url_fuente` y fecha de acceso;
9. conservar el producto mensual y liberar la tabla cruda.

Después, concatenar verticalmente los productos mensuales:

```python
producto_seis_meses = pd.concat(
    productos_mensuales,
    ignore_index=True,
)
```

`concat` apila periodos con el mismo esquema. No es una unión por claves como `merge`. No debe usarse `drop_duplicates()` para resolver diferencias de esquema o periodos superpuestos.

## 14. Manifiesto y controles

Construir un manifiesto con una fila por mes:

| Campo | Descripción |
|---|---|
| `mes_fuente` | mes procesado |
| `url_fuente` | archivo TLC utilizado |
| `filas_leidas_ventana` | registros devueltos por la lectura temporal, antes de aplicar calidad |
| `filas_validas` | registros que superaron las reglas |
| `filas_rechazadas` | registros excluidos |
| `filas_fuera_periodo` | registros que no pertenecen al intervalo mensual después de verificarlo |
| `filas_zona_hora` | filas del producto agregado |
| `fecha_minima` | primer pickup válido |
| `fecha_maxima` | último pickup válido |
| `fecha_acceso` | momento en que se obtuvo la fuente |

`filas_leidas_ventana` no es necesariamente la cantidad física total del archivo mensual: es la cantidad obtenida después de aplicar el filtro de lectura y antes de las reglas de calidad. Esta definición debe utilizarse igual en los seis meses.

Registrar también, para TLC, NOAA y el catálogo de zonas, URL, fecha de acceso, nombre del recurso y un hash si el archivo fue descargado. El catálogo debe cargarse una vez y reutilizarse en los seis procesos. Repetir una URL no demuestra por sí solo que el contenido remoto sea idéntico entre ejecuciones.

Comprobar mediante código que:

- estén presentes exactamente los seis meses;
- no se repita una URL;
- todas las tablas mensuales tengan las mismas columnas y tipos compatibles;
- cada timestamp pertenezca al mes declarado;
- la clave zona-hora sea única dentro de cada producto mensual;
- no existan superposiciones temporales entre meses;
- las filas combinadas coincidan con la suma de las filas mensuales.

### Cambio al horario de verano

El periodo incluye el inicio del horario de verano de Nueva York, el 10 de marzo de 2024. La grilla esperada debe generarse con límites conscientes de zona horaria y `pd.date_range(..., freq="h", inclusive="left")`; no debe suponerse que todos los días tienen 24 horas. Marzo contiene 743 horas locales y el intervalo enero-junio contiene 4367, pero estos valores deben derivarse del calendario en el código, no escribirse como una constante de control.

Los timestamps TLC son horas locales sin zona. Si aparece una hora local inexistente durante el salto de marzo, no debe desplazarse ni eliminarse silenciosamente: debe marcarse, conservarse en la auditoría y tratarse mediante una regla explícita. NOAA parte de UTC y debe convertirse después a `America/New_York`, lo que representa correctamente el salto temporal.

## 15. Extensión del clima

Si el par incluye una variable meteorológica:

1. usar la fuente NOAA de 2024 ya definida en el notebook;
2. ampliar la ventana local hasta `2024-07-01`, con fin excluido;
3. resumir a una fila meteorológica por hora;
4. revisar cobertura y faltantes para cada mes;
5. unir el clima con la tabla zona-hora después de concatenar los productos TLC;
6. volver a una fila por hora antes del análisis clima-clima o pickups-clima.

Si el par no incluye clima, no es necesario procesar NOAA para esta actividad extra.

## 16. Repetición y comparación del EDA

Repetir sobre enero-junio:

1. exploración univariada de ambas columnas;
2. revisión de faltantes, ceros y cobertura;
3. identificación de casos potencialmente anómalos con reglas declaradas;
4. análisis de la relación con la misma vista y método principal;
5. análisis de sensibilidad.

Usar enero como periodo inicial y febrero-junio como periodo de contraste no solapado. Presentar además enero-junio como resumen global descriptivo. No utilizar la comparación “enero frente a enero-junio” como evidencia de estabilidad, porque ambos conjuntos comparten las observaciones de enero.

Para estudiar recurrencia de anomalías, utilizar como análisis principal los límites definidos en enero y aplicarlos sin recalibrar a febrero-junio. Como sensibilidad puede calcularse una regla separada dentro de cada mes, aclarando que identifica extremos locales y responde una pregunta diferente.

Comparar enero, febrero-junio y el resumen global:

| Dimensión | Pregunta |
|---|---|
| Distribución | ¿cambian centro, dispersión, forma o colas? |
| Cobertura | ¿aparecen diferencias mensuales de faltantes o tamaño? |
| Anomalías | ¿son recurrentes o específicas de un mes? |
| Relación o estructura temporal | ¿mantiene dirección, forma, magnitud, ciclos o cambios de nivel? |
| Estratos | ¿el resultado global coincide con los resultados mensuales? |
| Sensibilidad | ¿la conclusión depende de un mes particular? |

## 17. Visualizaciones de la actividad extra

Incluir como mínimo:

- una visualización que compare la distribución por mes;
- una visualización de la relación diferenciada por mes;
- una tabla mensual de cobertura, tamaño y resumen de la relación o estructura temporal.

Según el tipo de par:

- numérica-numérica: dispersión global y facetas mensuales con escalas comunes;
- categórica-numérica: distribuciones por grupo y mes;
- temporal-numérica: serie completa y perfiles por mes, día u hora.

## 18. Relación global y relaciones mensuales

Para pares numérica-numérica o categórica-numérica, comparar explícitamente:

<p class="formula">relación global de seis meses &nbsp; frente a &nbsp; relaciones dentro de cada mes</p>

Una asociación global puede estar dominada por estacionalidad, tamaños mensuales diferentes o mezcla de periodos. Si el patrón global cambia o se invierte dentro de los meses, discutir confusión temporal o una posible manifestación del efecto de Simpson.

Para los pares `GT-02` a `GT-06`, no calcular una correlación contra el timestamp ni exigir una lectura de Simpson. Comparar perfiles horarios, ciclos semanales, cambios de nivel, huecos y anomalías entre meses con la misma agregación y escala.

No elegir ni excluir meses después de observar cuál respalda mejor la conclusión original.

## 19. Preguntas finales de la actividad extra

1. ¿El patrón observado en enero se mantiene en el periodo no solapado febrero-junio?
2. ¿La dirección y forma de la relación son estables?
3. ¿Qué meses presentan diferencias importantes?
4. ¿Los casos anómalos son recurrentes o específicos?
5. ¿Algún mes domina el resultado combinado?
6. ¿La conclusión original debe mantenerse, limitarse o reformularse?
7. ¿Qué explicaciones alternativas siguen siendo compatibles con los datos?

<div class="page-break"></div>

## 20. Producto de la actividad extra

Agregar al notebook una sección identificada como `Actividad EXTRA` con:

- manifiesto de las seis fuentes TLC;
- identificación de versiones o huellas de las fuentes auxiliares;
- auditoría mensual;
- construcción reproducible de `producto_seis_meses`;
- extensión de NOAA si corresponde;
- comparación de distribuciones;
- revisión de anomalías por mes;
- contraste enero frente a febrero-junio y resumen global enero-junio;
- análisis global y mensual de la relación o estructura temporal;
- al menos dos visualizaciones adicionales;
- conclusión sobre estabilidad temporal;
- límites y siguiente comprobación.

Los datos de seis meses siguen representando viajes Yellow Taxi realizados y reportados. Más filas no eliminan sesgos de cobertura, dependencia temporal, pseudorreplicación ni explicaciones alternativas.
