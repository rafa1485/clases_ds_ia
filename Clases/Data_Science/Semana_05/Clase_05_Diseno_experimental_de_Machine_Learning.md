---
title: "Diseño experimental de Machine Learning"
subtitle: "Cómo formular, evaluar y comparar modelos de manera confiable"
course: "Data Science"
week: 5
class: 5
language: es
---

# Diseño experimental de Machine Learning

## Cómo formular, evaluar y comparar modelos de manera confiable

**Semana 5 · Clase 5**

**Recorrido conceptual:** `problema → tarea → partición → baseline → evaluación → evidencia`.

*Un resultado es confiable cuando el experimento representa el uso futuro y evita información indebida.*

---

# De la incertidumbre al aprendizaje

En la Semana 4 estudiamos estimaciones, variabilidad y decisiones. Ahora usaremos datos históricos para construir una función que produzca estimaciones en casos nuevos.

| Antes | Ahora |
|---|---|
| Estimar una proporción o una media | Aprender una relación entre variables |
| Cuantificar variabilidad muestral | Medir desempeño fuera del ajuste |
| Comparar acciones y costos | Elegir métricas vinculadas con esos costos |

**Continuidad:** una métrica también es una estimación obtenida sobre una muestra y bajo supuestos determinados.

---

# Propósito y resultados de aprendizaje

**Propósito:** diseñar una evaluación de Machine Learning que produzca evidencia relevante, reproducible y libre de fuga de información.

Al finalizar podremos:

- distinguir paradigma, tarea, modelo, predicción y decisión;
- formular clasificación, regresión, clustering y series temporales;
- elegir particiones coherentes con la población de uso;
- establecer baselines y métricas pertinentes;
- aplicar validación cruzada sin contaminar la evaluación;
- reconocer subajuste, sobreajuste y comparaciones injustas;
- documentar un protocolo experimental reproducible.

---

# Pregunta de apertura

Una organización desea anticipar problemas de calidad del agua para priorizar inspecciones.

- ¿Qué debe predecirse exactamente?
- ¿Qué información estará disponible al predecir?
- ¿Se evaluarán nuevas mediciones, nuevos sitios o meses futuros?
- ¿Qué error tiene mayor costo?
- ¿Cómo sabremos que un modelo mejora la práctica actual?

**Idea:** antes de elegir un algoritmo debemos definir qué evidencia demostraría que su resultado es útil fuera de los datos usados para construirlo.

---

# ¿Qué significa aprender de los datos?

Aprender es ajustar una función a partir de ejemplos:

$$
f:\mathcal X\rightarrow\mathcal Y,\qquad \widehat y=f(x).
$$

- $x$: variables disponibles para un caso.
- $y$: resultado real que se desea estimar.
- $\widehat y$: predicción producida por el modelo.
- El ajuste utiliza casos históricos.
- La evaluación debe usar casos que no participaron del ajuste.

**Resultado:** memorizar el pasado no demuestra que el modelo generalice.

---

# Paradigma, tarea y algoritmo

| Nivel | Pregunta | Ejemplo |
|---|---|---|
| Paradigma | ¿De dónde proviene la señal de aprendizaje? | supervisado o no supervisado |
| Tarea | ¿Qué salida necesitamos? | clase, valor, grupo o pronóstico |
| Algoritmo | ¿Qué procedimiento ajustará la relación? | regresión, árbol o K-means |

Una misma tarea admite varios algoritmos y un algoritmo puede resolver tareas diferentes.

*Elegir “un árbol” no define todavía la población, la etiqueta, la partición ni la métrica.*

---

# Aprendizaje supervisado

El conjunto de entrenamiento contiene pares con respuesta conocida:

$$
\mathcal D=\{(x_1,y_1),\ldots,(x_n,y_n)\}.
$$

- La respuesta $y$ guía el ajuste.
- En **clasificación**, $y$ representa una categoría.
- En **regresión**, $y$ representa una cantidad.
- El desempeño se mide comparando $\widehat y$ con respuestas reservadas.

**Ejemplo:** variables fisicoquímicas y antecedentes permiten estimar si una futura medición excederá un límite.

---

# Aprendizaje no supervisado y semisupervisado

**No supervisado:** trabaja con entradas $x$ sin una respuesta objetivo conocida.

- Busca estructura, similitudes o representaciones.
- El clustering agrupa sitios con perfiles semejantes.
- Los grupos requieren interpretación y validación.

**Semisupervisado:** combina pocos casos etiquetados con muchos casos sin etiqueta.

- Puede ser útil cuando medir es barato y confirmar el resultado es costoso.
- La evaluación final sigue necesitando etiquetas confiables.

---

# Cuatro tareas de análisis

| Tarea | Salida | Pregunta de evaluación |
|---|---|---|
| Clasificación | categoría o probabilidad | ¿detecta correctamente las clases? |
| Regresión | valor numérico | ¿cuánto se aleja del valor real? |
| Clustering | grupo o pertenencia | ¿los grupos son estables e interpretables? |
| Serie temporal | valor futuro | ¿supera un pronóstico ingenuo respetando el tiempo? |

**Control:** la codificación numérica de una categoría no la convierte en regresión.

---

# Un dominio, cuatro formulaciones

Con datos de calidad del agua podemos formular problemas distintos:

| Necesidad | Tarea | Objetivo |
|---|---|---|
| Activar una inspección | clasificación | excede/no excede un límite |
| Estimar concentración | regresión | concentración en mg/L |
| Comparar perfiles de sitios | clustering | agrupación por similitud |
| Anticipar el próximo mes | serie temporal | concentración futura |

Cada formulación cambia la unidad, la salida, la partición y el criterio de evaluación.

---

# Definición del problema predictivo

Antes de modelar debemos establecer:

1. decisión o uso de la predicción;
2. unidad de análisis;
3. población objetivo;
4. instante en que se predice;
5. horizonte del resultado;
6. variables disponibles;
7. objetivo y fuente de confirmación;
8. criterio de evaluación.

**Pregunta de control:** ¿qué cambiará operativamente cuando el modelo produzca una predicción?

---

# Unidad, población y muestra

- **Unidad:** entidad sobre la que se produce una predicción; por ejemplo, `(sitio, fecha)`.
- **Población objetivo:** conjunto de unidades donde se pretende utilizar el modelo.
- **Muestra histórica:** unidades observadas disponibles para ajustar y evaluar.

La misma estación en dos fechas produce dos filas, pero esas filas pueden estar relacionadas.

**Consecuencia:** el número de filas no siempre coincide con el número de unidades independientes.

---

# Instante y horizonte

- $t_0$: instante en que debe emitirse la predicción.
- Ventana de observación: información disponible hasta $t_0$.
- Horizonte $H$: periodo futuro donde se define el resultado.
- Confirmación: momento en que la etiqueta puede conocerse.

**Línea temporal:** `pasado observable | t0: predicción | horizonte H | resultado confirmado`.

Cambiar $t_0$ o $H$ cambia el problema, aunque las columnas tengan los mismos nombres.

---

# Generalización

Generalizar es mantener un desempeño útil en casos nuevos de la población objetivo.

$$
R(f)=\mathbb E_{(X,Y)\sim P_{\mathrm{uso}}}[L(Y,f(X))].
$$

La evaluación aproxima ese error esperado con datos no utilizados para ajustar el procedimiento.

- Casos representativos del uso esperado.
- Separación compatible con tiempo y entidades.
- Métrica alineada con el error relevante.

**Alcance:** el resultado vale para el escenario evaluado, no para cualquier población futura.

---

# Entrenamiento, validación y prueba

| Partición | Uso permitido |
|---|---|
| Entrenamiento | ajustar parámetros y transformaciones |
| Validación | elegir variables, configuración y umbral |
| Prueba | medir una vez el procedimiento congelado |

Consultar repetidamente la prueba y modificar el procedimiento convierte la prueba en validación.

*Los porcentajes 60/20/20 u 80/10/10 son opciones, no reglas universales.*

---

# Partición aleatoria y estratificada

- **Aleatoria:** asigna unidades al azar.
- **Estratificada:** conserva aproximadamente la proporción de clases.
- Son adecuadas cuando las unidades pueden tratarse como intercambiables e independientes.
- La estratificación estabiliza la medición de clases poco frecuentes.

**Limitación:** ninguna evita que mediciones del mismo sitio o del mismo episodio aparezcan a ambos lados.

---

# Partición por grupos

Todos los registros de un grupo permanecen en una sola partición.

**Ejemplo:** `sitios A–F → entrenamiento | G–H → validación | I–J → prueba`.

- Grupo posible: sitio, sensor, paciente, cliente, vehículo o evento.
- Evita compartir patrones propios de una entidad.
- Evalúa transferencia hacia grupos no observados.

**Pregunta:** ¿el uso real predice nuevas fechas de sitios conocidos o sitios completamente nuevos?

---

# Partición temporal

El pasado entrena y el futuro evalúa:

`enero–junio: entrenamiento → julio–agosto: validación → septiembre: prueba`.

- Respeta el orden causal.
- Simula un despliegue prospectivo.
- Revela cambios de estación, sensores o procesos.
- Cada transformación se ajusta solo con datos anteriores al periodo evaluado.

Barajar observaciones temporales puede permitir que el futuro ayude a predecir el pasado.

---

# ¿Qué partición representa el uso?

| Uso futuro | Partición principal |
|---|---|
| nuevas filas independientes | aleatoria o estratificada |
| nuevas observaciones de grupos conocidos | temporal dentro de cada grupo |
| grupos nunca observados | por grupos |
| meses futuros | temporal |
| nuevos grupos en periodos futuros | combinación de grupos y tiempo |

**Criterio:** primero se define qué significa “caso nuevo”; después se elige la partición.

---

# Fuga de información

Existe **fuga** cuando el ajuste o la evaluación utilizan información que no estaría disponible al producir una predicción real.

- Produce resultados demasiado optimistas.
- Puede aparecer en variables, particiones o transformaciones.
- También ocurre cuando unidades relacionadas cruzan la frontera experimental.

**Prueba operativa:** para cada variable registrar quién la genera, cuándo existe y qué datos intervinieron en su cálculo.

---

# Tres fugas frecuentes

| Tipo | Ejemplo | Control |
|---|---|---|
| Temporal | usar la medición que confirma el evento | cortar variables en $t_0$ |
| Entidad | mismo sitio en entrenamiento y prueba | separar por grupo |
| Preprocesamiento | imputar con la media de todos los datos | ajustar solo con entrenamiento |

Eliminar una columna sospechosa no basta: toda la frontera experimental debe preservar la separación.

---

# Ejemplo numérico: imputación contaminada

Valores de entrenamiento: $[8,10,12]$. Valor faltante en entrenamiento: `NA`. Valor de prueba: $30$.

- Media correcta, calculada solo con entrenamiento:
  $$\bar x_{train}=(8+10+12)/3=10.$$
- Media contaminada, calculada incluyendo prueba:
  $$\bar x_{todo}=(8+10+12+30)/4=15.$$

Imputar con 15 permite que el valor reservado de prueba modifique los datos de entrenamiento.

---

# Duplicados y selección de atributos

**Duplicados o casos relacionados:** copias, ventanas solapadas o mediciones del mismo episodio pueden inflar la muestra y aparecer en particiones distintas.

**Selección de atributos:** elegir variables mediante correlaciones, rankings o desempeño también aprende de los datos.

- Los duplicados relacionados deben permanecer juntos.
- La selección basada en datos debe realizarse dentro de entrenamiento o de cada fold.
- La prueba no interviene en ninguna selección.

---

# Baseline: referencia mínima

Un baseline es una referencia simple, reproducible y disponible con la misma información que el modelo.

- Determina qué mejora debe justificar la complejidad.
- Detecta errores del pipeline y métricas mal interpretadas.
- Puede ser una regla operativa existente, no solo una constante.
- Debe evaluarse en exactamente los mismos casos.

**Resultado:** superar un baseline débil no demuestra utilidad; la referencia debe ser pertinente.

---

# Baselines por tipo de tarea

| Tarea | Baseline posible |
|---|---|
| Clasificación | clase mayoritaria o frecuencia histórica |
| Regresión | media o mediana del entrenamiento |
| Serie temporal | último valor o mismo periodo anterior |
| Clustering | una partición trivial y estabilidad frente a remuestreo |

En calidad del agua también puede compararse contra la regla de inspección vigente.

---

# Ejemplo: accuracy engañosa

En 100 mediciones hay 20 excedencias y 80 casos normales. El baseline siempre predice “normal”.

| | Excedencia real | Normal real |
|---|---:|---:|
| Predice excedencia | VP = 0 | FP = 0 |
| Predice normal | FN = 20 | VN = 80 |

$$
\mathrm{accuracy}=80/100=80\%,\qquad \mathrm{recall}=0/20=0\%.
$$

Tiene accuracy alta, pero no detecta ninguna excedencia.

---

# Matriz de confusión

| | Real positiva | Real negativa |
|---|---:|---:|
| Predicción positiva | verdadero positivo (VP) | falso positivo (FP) |
| Predicción negativa | falso negativo (FN) | verdadero negativo (VN) |

- VP y VN son aciertos respecto de la clase definida como positiva.
- FP es una falsa alarma.
- FN es un positivo omitido.
- La clase positiva debe declararse antes de interpretar las métricas.

---

# Métricas de clasificación

Supongamos $VP=16$, $FP=8$, $FN=4$ y $VN=72$:

$$
\mathrm{accuracy}=\frac{16+72}{100}=0{,}88,
$$

$$
\operatorname{Prec}=\frac{16}{16+8}=0{,}67,\qquad
\mathrm{recall}=\frac{16}{16+4}=0{,}80,
$$

$$
F_1=\frac{2VP}{2VP+FP+FN}=\frac{32}{44}=0{,}73.
$$

Cada métrica responde una pregunta diferente.

---

# Métrica, prevalencia y costo

- **Accuracy:** fracción total de aciertos; puede ocultar una clase rara.
- **Precisión:** de las alertas emitidas, cuántas eran correctas.
- **Recall:** de los eventos reales, cuántos se detectaron.
- **F1:** equilibra precisión y recall, pero no incorpora verdaderos negativos.

Si omitir una excedencia es más costoso que realizar una inspección innecesaria, recall merece especial atención.

**Control:** ninguna métrica sustituye la declaración de costos y capacidad operativa.

---

# Métricas de regresión

Para errores $e_i=y_i-\widehat y_i$:

$$
\mathrm{MAE}=\frac{1}{n}\sum_{i=1}^n|e_i|,
\qquad
\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum_{i=1}^n e_i^2}.
$$

- Ambas conservan la unidad de $y$.
- MAE pondera linealmente la magnitud del error.
- RMSE penaliza más los errores grandes.
- La elección depende de las consecuencias de los errores extremos.

---

# Ejemplo numérico: MAE y RMSE

Valores reales: $[10,12,18,20]$. Predicciones: $[11,10,17,26]$.

Errores absolutos: $[1,2,1,6]$.

$$
\mathrm{MAE}=\frac{1+2+1+6}{4}=2{,}5.
$$

$$
\mathrm{RMSE}=\sqrt{\frac{1^2+2^2+1^2+6^2}{4}}
=\sqrt{10{,}5}\approx3{,}24.
$$

RMSE aumenta más por el error de 6 unidades.

---

# $R^2$ y sus límites

$$
R^2=1-\frac{\sum_i(y_i-\widehat y_i)^2}{\sum_i(y_i-\bar y)^2}.
$$

- Compara el error del modelo con predecir la media.
- Puede ser negativo fuera de muestra.
- No conserva la unidad del objetivo.
- Un valor alto no garantiza errores operativamente pequeños.
- En series con tendencia puede resultar engañoso.

**Recomendación:** informar $R^2$ junto con MAE o RMSE y un baseline pertinente.

---

# Evaluar clustering

Sin etiquetas objetivo no existe una accuracy predictiva convencional.

- **Cohesión:** observaciones próximas dentro de cada grupo.
- **Separación:** grupos alejados entre sí.
- **Silhouette:** combina cohesión y separación en una escala aproximada de $-1$ a $1$.
- **Estabilidad:** grupos similares ante remuestreo o cambios razonables.
- **Utilidad:** perfiles interpretables que apoyan una decisión.

Un valor interno alto no demuestra que los grupos sean relevantes para el dominio.

---

# Evaluar series temporales

- Entrenar con pasado y validar sobre periodos posteriores.
- Comparar contra persistencia y estacionalidad simple.
- Medir varios orígenes y horizontes, no un único corte conveniente.
- Ajustar transformaciones nuevamente en cada ventana.

**Ventana expansiva:**

`enero–marzo → abril | enero–abril → mayo | enero–mayo → junio`.

El promedio resume desempeño; la variación entre periodos revela estabilidad temporal.

---

# Validación cruzada

En K-fold, el conjunto de desarrollo se divide en $K$ bloques. Cada bloque actúa una vez como validación:

$$
\bar m=\frac{1}{K}\sum_{k=1}^{K}m_k.
$$

- Estratificada para conservar clases.
- Por grupos para mantener entidades juntas.
- Temporal con ventanas ordenadas.
- La prueba final permanece fuera del ciclo.

Reportar promedio y dispersión entre folds evita depender de una única partición favorable.

---

# El pipeline se ajusta dentro de cada fold

En cada iteración:

1. ajustar imputación, escalado y codificación con los folds de entrenamiento;
2. seleccionar atributos usando solo esos folds;
3. transformar entrenamiento y validación;
4. ajustar el modelo;
5. medir sobre el fold reservado.

**Flujo:** `training del fold → transformaciones → selección → modelo → validación del fold`.

El objeto evaluado es el procedimiento completo, no solo el algoritmo final.

---

# Subajuste y sobreajuste

| Situación | Entrenamiento | Validación | Lectura |
|---|---|---|---|
| Subajuste | error alto | error alto | capacidad o representación insuficiente |
| Equilibrio | error bajo | error bajo y estable | generalización plausible |
| Sobreajuste | error muy bajo | error mayor | adaptación excesiva al entrenamiento |

Se elige por desempeño de validación, estabilidad y simplicidad, no por el mejor ajuste al entrenamiento.

---

# Actividad: protocolo experimental

Cada equipo definirá, antes de entrenar:

| Sección | Evidencia mínima |
|---|---|
| Problema | unidad, población, $t_0$, horizonte, $x$ e $y$ |
| Partición | entrenamiento, validación y prueba justificadas |
| Controles | riesgos de fuga y cómo se comprobarán |
| Referencia | baseline reproducible |
| Evaluación | métrica principal, auxiliares y costo relevante |
| Reproducción | versión de datos, semilla y reglas congeladas |

**Hito:** otro equipo debe poder reconstruir y auditar la evaluación propuesta.

---

# Síntesis y próximo paso

**Flujo:** `definición → tarea → partición → baseline → pipeline → validación → prueba`.

- La tarea determina la salida, no el algoritmo.
- La partición debe representar qué significa un caso nuevo.
- La fuga invalida la evidencia de generalización.
- Cada tarea necesita baselines y métricas pertinentes.
- La validación evalúa todo el procedimiento.
- La prueba mide una vez una configuración congelada.

**Próximo paso:** implementar transformaciones y atributos ajustados únicamente con entrenamiento.
