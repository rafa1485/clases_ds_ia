---
title: "Diseño experimental de Machine Learning"
subtitle: "De datos históricos a decisiones confiables"
author: "Curso de Inteligencia Artificial"
course: "Inteligencia Artificial"
week: 5
class: 5
lang: es
---

# Diseño experimental de Machine Learning

## De datos históricos a decisiones confiables

**Semana 5 · Clase 5**

**Recorrido conceptual:** `decisión -> datos -> función aprendida -> evaluación -> acción`.

El valor de una predicción depende del experimento que permite confiar en ella.

---

# Continuidad: de incertidumbre a aprendizaje

Un agente decide con información parcial y costos distintos para cada error.

- La probabilidad representó la creencia sobre un estado oculto.
- El costo esperado conectó esa creencia con una acción.
- En sistemas reales, las probabilidades y reglas se estiman con datos históricos.

**Continuidad:** diseñar el experimento determina si una estimación aprendida puede sostener una decisión fuera de los datos usados para construirla.

---

# Propósito y resultados de aprendizaje

**Propósito:** diseñar una evaluación de Machine Learning alineada con la decisión y libre de información indebida.

Al finalizar podremos:

- distinguir tarea, modelo, regla de decisión y agente;
- definir unidad, población, instante, horizonte, variables y etiqueta;
- elegir particiones coherentes con la forma de uso;
- construir baselines y métricas vinculadas con costos;
- aplicar validación cruzada sin fuga de información;
- reconocer subajuste, sobreajuste y comparaciones injustas;
- documentar un procedimiento reproducible y congelado.

---

# Pregunta de apertura

> Un vehículo debe decidir si ingresa a un tramo. ¿Cómo demostramos que su estimación de bloqueo funcionará con tramos futuros?

- ¿Qué señales existen antes de ingresar?
- ¿Cuándo se confirma el estado real?
- ¿Qué error es más costoso: ingresar con bloqueo o desviarse sin necesidad?
- ¿Qué datos representan el uso real?

**Idea:** el experimento debe reproducir la información y las restricciones disponibles al decidir.

---

# De probabilidades dadas a estimaciones aprendidas

| Probabilidad especificada | Estimación aprendida |
|---|---|
| Se entrega $P(B)$ y $P(A\mid B)$ | Se observan ejemplos históricos $(x_i,y_i)$ |
| La tabla define la relación | Una función $f$ aproxima la relación |
| Bayes actualiza la creencia | $\hat y=f(x)$ estima el objetivo |

**Puente:** los datos reemplazan parámetros dados por estimaciones; el diseño experimental controla si esas estimaciones generalizan.

---

# ¿Qué significa aprender?

Aprender es ajustar, a partir de ejemplos, una función que transforma información disponible en una salida útil:

$$
f:\mathcal{X}\rightarrow\mathcal{Y},\qquad \hat y=f(x).
$$

- $x$: variables observadas antes de decidir.
- $y$: resultado real definido por el problema.
- $\hat y$: estimación producida por la función aprendida.
- El ajuste busca buen desempeño en casos no usados para aprender.

**Resultado:** memorizar ejemplos no equivale a aprender una relación generalizable.

---

# Modelo, regla de decisión y agente

**Flujo:** `señales x -> modelo f -> predicción yhat -> regla y costos -> acción -> entorno`.

| Componente | Responsabilidad |
|---|---|
| Modelo | estima una clase, valor o puntaje |
| Regla de decisión | convierte la salida y los costos en una acción |
| Agente | observa, aplica la regla, actúa y recibe consecuencias |

**Control:** una predicción de bloqueo no ordena desviarse; la acción depende del umbral, los costos y las restricciones operativas.

---

# Anatomía de un ejemplo

Para un tramo observado a las 08:00:

| Elemento | Ejemplo |
|---|---|
| $x$ | lluvia reciente, velocidad aguas arriba, alertas previas, tipo de vía |
| $y$ | `1` si el tramo queda confirmado como bloqueado en 15 min; `0` si queda libre |
| $\hat y$ | puntaje de bloqueo estimado antes de ingresar |

Una fila representa una unidad en un instante. La etiqueta se conoce después; la predicción debe usar únicamente el pasado disponible a las 08:00.

---

# Aprendizaje supervisado

El conjunto de entrenamiento contiene pares $(x_i,y_i)$ con una respuesta conocida.

$$
\{(x_1,y_1),\ldots,(x_n,y_n)\}\ \longrightarrow\ \hat f.
$$

- La etiqueta guía el ajuste de la función.
- La salida se compara con respuestas reales no usadas en el ajuste.
- Ejemplos: bloqueo de un tramo, demanda de agua y tiempo de resolución de un reclamo.

**Idea:** supervisado describe la disponibilidad de etiquetas, no un algoritmo particular.

---

# Clasificación y regresión

| Tarea supervisada | Salida | Ejemplo de transferencia |
|---|---|---|
| Clasificación | categoría o puntaje por categoría | tramo `bloqueado/libre`; reclamo `urgente/no urgente` |
| Regresión | valor numérico | demanda de agua; minutos para resolver un reclamo |

En clasificación, un puntaje puede convertirse en clase mediante un umbral. En regresión, la salida conserva escala y unidad.

**Control:** la forma de $y$ define la tarea; la acción pertenece al sistema de decisión.

---

# Aprendizaje no supervisado

Los datos contienen variables $x_i$, pero no una etiqueta objetivo $y_i$.

- Busca estructura, similitudes o representaciones en los datos.
- El **clustering** agrupa observaciones según un criterio de similitud.
- Ejemplo: agrupar patrones de consumo de agua sin categorías previas.
- Los grupos obtenidos requieren interpretación y validación respecto del propósito.

**Resultado:** descubrir estructura no demuestra por sí mismo capacidad predictiva ni prescribe una acción.

---

# Aprendizaje semisupervisado

Combina pocos ejemplos etiquetados con muchos ejemplos sin etiqueta:

$$
\mathcal{D}_L=\{(x_i,y_i)\},\qquad \mathcal{D}_U=\{x_j\},\qquad |\mathcal{D}_L|\ll|\mathcal{D}_U|.
$$

- Es útil cuando medir señales es barato y confirmar el resultado es costoso.
- En movilidad, abundan trazas de tránsito, pero confirmar cada bloqueo exige verificación.
- La evaluación final necesita etiquetas confiables y una partición representativa.

**Control:** datos sin etiqueta amplían información sobre $x$; no reemplazan una definición precisa de $y$.

---

# Comparación de paradigmas

| Paradigma | Evidencia disponible | Pregunta central |
|---|---|---|
| Supervisado | ejemplos $(x,y)$ | ¿qué salida corresponde a un caso nuevo? |
| No supervisado | ejemplos $x$ | ¿qué estructura aparece en los datos? |
| Semisupervisado | pocos $(x,y)$ y muchos $x$ | ¿cómo aprovechar ambos conjuntos? |
| Refuerzo | interacción, acciones y recompensas | ¿qué acciones acumulan mejores consecuencias? |

**Idea:** el paradigma surge del tipo de retroalimentación disponible y del objetivo de la tarea.

---

# Partir de la decisión

El diseño comienza en el uso, no en el archivo de datos:

1. decisión que debe tomar el sistema;
2. consecuencias de cada error;
3. salida predictiva que informa la decisión;
4. instante exacto en que se requiere esa salida;
5. evidencia disponible en ese instante;
6. evaluación que reproduce esas condiciones.

**Pregunta de control:** ¿qué cambiará operativamente cuando el modelo produzca $\hat y$?

---

# Definición del caso conductor

| Elemento | Definición |
|---|---|
| Decisión | ingresar al tramo o tomar un desvío |
| Salida predictiva | puntaje de bloqueo en los próximos 15 min |
| Regla | desviar si el puntaje supera el umbral operativo |
| Evidencia | señales registradas antes de ingresar |
| Confirmación | reporte verificado del estado del tramo |
| Costo principal | seguridad, demora y consumo del recorrido |

**Criterio de consistencia:** cada ejemplo debe respetar estas definiciones para representar la misma tarea.

---

# Unidad y población

- **Unidad de análisis:** un par `(tramo, instante de decisión)`.
- **Población objetivo:** decisiones de ingreso de la flota en la red y condiciones operativas definidas.
- **Muestra:** unidades históricas observadas y recuperadas por el sistema de datos.

La misma vía en dos instantes produce dos unidades distintas. Dos registros de la misma unidad no son evidencia independiente.

**Control:** evaluar sobre otra población responde otra pregunta, aunque las columnas coincidan.

---

# Objetivo, etiqueta, predicción y acción

| Concepto | Caso conductor |
|---|---|
| Objetivo | anticipar bloqueo antes de ingresar |
| Etiqueta $y$ | estado confirmado dentro del horizonte: $1/0$ |
| Predicción $\hat y$ | puntaje o clase estimada |
| Acción | ingresar, desviar o solicitar verificación |

$$
x\xrightarrow{f}\hat y\xrightarrow{\text{regla + costos}}a.
$$

**Resultado:** evaluar $\hat y$ mide predicción; evaluar consecuencias de $a$ mide el sistema de decisión.

---

# Instante y horizonte

- $t_0$: instante en que el vehículo debe decidir.
- Ventana de observación: datos con marca temporal $t\le t_0$.
- Horizonte $H=15$ min: intervalo en que se define el resultado.
- Etiqueta: bloqueo confirmado en $(t_0,t_0+H]$.

**Línea temporal:** `pasado observable | t0: predicción y acción | horizonte H | confirmación`.

Cambiar $t_0$ o $H$ cambia la tarea, la etiqueta y la utilidad operativa.

---

# Variables disponibles al decidir

| Admitidas en $t_0$ | No admitidas en $t_0$ |
|---|---|
| lluvia acumulada hasta $t_0$ | lluvia registrada después de $t_0$ |
| velocidad aguas arriba hasta $t_0$ | velocidad medida tras ingresar |
| reportes recibidos antes de $t_0$ | confirmación final del bloqueo |
| atributos estables del tramo | duración total del incidente |

**Control:** una columna es válida por su momento real de disponibilidad, no por aparecer en la tabla histórica.

---

# Fuga de información

Existe **fuga** cuando el entrenamiento o la evaluación reciben información que no estaría disponible al producir la predicción real.

- Infla el resultado medido sin mejorar el uso futuro.
- Puede ocurrir en variables, transformaciones o particiones.
- También aparece cuando una misma entidad aporta registros casi idénticos a entrenamiento y evaluación.

**Prueba operativa:** para cada valor usado, registrar quién lo genera, cuándo existe y qué datos intervinieron en su cálculo.

---

# Tres fugas frecuentes

| Tipo | Ejemplo | Control |
|---|---|---|
| Temporal | usar la duración final del bloqueo | cortar variables en $t_0$ |
| Preprocesamiento | normalizar con media de todo el conjunto | ajustar transformación solo con entrenamiento |
| Duplicados o entidad | misma ventana o mismo vehículo en ambos lados | deduplicar y separar por unidad o grupo |

**Resultado:** quitar una columna sospechosa no basta; la frontera experimental debe aislar toda información futura o compartida.

---

# Generalización

Generalizar es mantener desempeño en unidades nuevas de la población objetivo.

$$
R(f)=\mathbb{E}_{(X,Y)\sim P_{\mathrm{uso}}}[L(Y,f(X))].
$$

La evaluación estima ese riesgo con datos no usados para ajustar el procedimiento.

- Muestra representativa del uso esperado.
- Separación compatible con dependencias temporales y de entidad.
- Métrica alineada con el error relevante.

**Idea:** un valor fuera de muestra es evidencia bajo un escenario de uso definido, no una garantía universal.

---

# Entrenamiento, validación y prueba

| Partición | Uso permitido |
|---|---|
| Entrenamiento | ajustar parámetros y transformaciones |
| Validación | elegir variables, configuraciones y umbral con la métrica principal ya definida |
| Prueba | medir una vez el procedimiento congelado |

Consultar repetidamente la prueba la convierte en validación.

**Control:** la prueba se reserva para la medición final; cualquier cambio motivado por ella exige una nueva prueba independiente.

---

# Partición aleatoria y estratificada

- **Aleatoria:** asigna unidades al azar; es apropiada cuando son intercambiables e independientes.
- **Estratificada:** conserva aproximadamente la proporción de clases en cada partición.
- La estratificación estabiliza la medición cuando el bloqueo es poco frecuente.
- Ninguna de las dos resuelve dependencias entre registros de una entidad ni anticipación temporal.

**Control:** primero se define qué observaciones pueden separarse; después se conserva la distribución relevante.

---

# Partición por grupos

Todos los registros de un mismo grupo quedan en una sola partición.

**Diagrama:** `vehículos A,B,C -> entrenamiento | D -> validación | E -> prueba`.

- Grupo posible: vehículo, corredor, sensor, cliente o evento.
- Evalúa transferencia hacia grupos no observados durante el ajuste.
- Evita que patrones propios de una entidad aparezcan a ambos lados.

**Pregunta:** ¿el uso real predice nuevos instantes de entidades conocidas o entidades completamente nuevas?

---

# Partición temporal

El pasado entrena y el futuro evalúa:

`enero-marzo: entrenamiento -> abril: validación -> mayo: prueba`.

- Respeta causalidad y simula despliegue prospectivo.
- Conserva juntas las ventanas de un mismo incidente cuando corresponde.
- Puede revelar cambios de estación, sensores, rutas o comportamiento.

**Control:** toda variable y transformación de cada corte se calcula únicamente con información anterior al período evaluado.

---

# Baseline: el mínimo que debe superarse

Un baseline es una referencia simple, reproducible y disponible con la misma información.

- Clasificación: clase mayoritaria o regla operativa vigente.
- Regresión: media o mediana del entrenamiento.
- Series temporales: último valor observado o patrón estacional simple.

**Resultado:** un modelo complejo aporta valor solo si mejora una referencia pertinente en la métrica y el escenario elegidos.

---

# Baseline de clasificación: accuracy engañosa

En 100 registros hay 20 bloqueos y 80 tramos libres. El baseline siempre predice `libre`.

| | Real bloqueado | Real libre |
|---|---:|---:|
| Predice bloqueado | VP = 0 | FP = 0 |
| Predice libre | FN = 20 | VN = 80 |

$$
\mathrm{accuracy}=\frac{0+80}{100}=80\%,\qquad \mathrm{recall}=\frac{0}{0+20}=0\%.
$$

**Lectura:** acierta la clase frecuente, pero no detecta ningún bloqueo; por eso accuracy sola no representa el objetivo.

---

# Baselines de regresión y temporales

| Problema | Baseline | Qué controla |
|---|---|---|
| demanda diaria de agua | mediana del entrenamiento | error frente a un nivel constante robusto |
| tiempo de resolución | media del entrenamiento | mejora sobre el promedio histórico |
| velocidad del tramo | último valor observado | persistencia temporal |
| demanda semanal | valor del mismo día previo | estacionalidad simple |

Los baselines fijos se estiman con entrenamiento. Un baseline temporal actualiza su estado en cada origen usando solo información disponible hasta ese instante.

---

# Métrica y costo

La métrica resume errores predictivos; el costo expresa sus consecuencias.

| Error | Consecuencia posible |
|---|---|
| FN: predecir libre cuando está bloqueado | ingreso inseguro, detención y demora alta |
| FP: predecir bloqueado cuando está libre | desvío innecesario |

- Un umbral cambia el equilibrio entre FP y FN.
- La métrica elegida debe visibilizar el error costoso.
- La decisión final puede minimizar costo esperado sujeto a restricciones de seguridad.

**Idea:** ninguna métrica reemplaza la declaración explícita de costos y límites operativos.

---

# Matriz de confusión

| | Real positivo: bloqueado | Real negativo: libre |
|---|---:|---:|
| Predicción positiva: bloqueado | VP | FP |
| Predicción negativa: libre | FN | VN |

- VP y VN son aciertos respecto de la clase definida como positiva.
- FP es una falsa alarma; FN es un bloqueo omitido.
- Total $N=VP+VN+FP+FN$.
- Positivos reales $P=VP+FN$; positivos predichos $\hat P=VP+FP$.

**Control:** definir la clase positiva antes de interpretar cualquier métrica.

---

# Accuracy, precisión, recall y F1

$$
\mathrm{accuracy}=\frac{VP+VN}{VP+VN+FP+FN},\qquad
\mathrm{precisión}=\frac{VP}{VP+FP},
$$

$$
\mathrm{recall}=\frac{VP}{VP+FN},\qquad
F_1=2\frac{\mathrm{precisión}\,\mathrm{recall}}{\mathrm{precisión}+\mathrm{recall}}=\frac{2VP}{2VP+FP+FN}.
$$

- Precisión: de las alertas emitidas, qué fracción era bloqueo.
- Recall: de los bloqueos reales, qué fracción fue detectada.
- $F_1$: media armónica de precisión y recall; no incorpora VN.

Los cocientes requieren denominador mayor que cero; si no hay positivos reales o predichos, debe reportarse esa condición.

---

# MAE y RMSE

Para errores $e_i=y_i-\hat y_i$ en $n$ observaciones:

$$
\mathrm{MAE}=\frac{1}{n}\sum_{i=1}^{n}|e_i|,
\qquad
\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum_{i=1}^{n}e_i^2}.
$$

- Ambos se expresan en la unidad de $y$.
- MAE pondera linealmente cada magnitud de error.
- RMSE penaliza con mayor fuerza los errores grandes.

**Control:** comparar ambas métricas sobre exactamente las mismas observaciones y declarar si los errores extremos tienen un costo especial.

---

# Validación cruzada K-fold

Para unidades intercambiables, se divide el conjunto de desarrollo en $K$ folds. Cada fold actúa una vez como validación y los $K-1$ restantes como entrenamiento.

$$
\bar m=\frac{1}{K}\sum_{k=1}^{K}m_k.
$$

- Con grupos, cada entidad completa se asigna a un fold.
- Con tiempo, se usan ventanas expansivas o deslizantes: solo el pasado entrena y el futuro valida.
- La prueba permanece fuera del ciclo completo.

**Resultado:** la estrategia de remuestreo debe reproducir las dependencias y el orden del uso real.

---

# Transformaciones dentro de cada fold

En cada iteración:

1. ajustar imputación, escalado y codificación con los folds de entrenamiento;
2. transformar entrenamiento y validación con esos valores ajustados;
3. ajustar el modelo en entrenamiento transformado;
4. medir en validación transformada.

**Diagrama:** `folds de entrenamiento -> ajustar transformación -> ajustar modelo -> aplicar a fold de validación`.

**Control:** ajustar el preprocesamiento una sola vez con todos los datos filtra información entre folds.

---

# Selección de características

Elegir variables también aprende de los datos y forma parte del procedimiento.

- Disponibilidad: cada variable debe existir en $t_0$.
- Pertinencia: debe representar una señal compatible con el objetivo.
- Estabilidad: su significado y medición deben sostenerse en uso.
- Selección: cualquier ranking o descarte basado en datos se ajusta dentro de cada fold.

**Resultado:** una lista fijada por disponibilidad o conocimiento del dominio puede preespecificarse; usar información de validación o prueba para elegir variables produce optimismo.

---

# Subajuste y sobreajuste

**Diagrama conceptual:** al aumentar la complejidad, el error de entrenamiento desciende; el error de validación primero desciende y luego aumenta.

- **Subajuste:** errores altos en entrenamiento y validación; mejorar representación o capacidad.
- **Equilibrio:** validación mínima y brecha controlada; conservar el procedimiento.
- **Sobreajuste:** error de entrenamiento bajo y validación peor; reducir búsqueda, regularizar o reunir datos relevantes.

**Idea:** se elige por desempeño de validación, no por el mejor ajuste al entrenamiento.

---

# Comparación justa y protocolo congelado

Dos alternativas se comparan con las mismas:

- unidades, folds y período de prueba;
- variables disponibles y tratamiento de faltantes;
- métrica, definición de clase positiva y regla de agregación;
- presupuesto de búsqueda y semillas registradas.

**Protocolo congelado:** código, datos identificados por versión, particiones, transformaciones, variables, configuración, umbral y métricas quedan fijados antes de abrir la prueba.

**Resultado:** reproducibilidad significa reconstruir el procedimiento y obtener resultados compatibles bajo las mismas condiciones.

---

# Síntesis

**Flujo:** `decisión -> definición del problema -> partición -> baseline -> procedimiento -> validación -> prueba final -> acción`.

- Aprender estima una función $\hat y=f(x)$; decidir convierte esa salida en acción.
- Unidad, población, instante y horizonte definen qué significa un ejemplo.
- La fuga invalida la evidencia de generalización.
- La partición debe representar dependencias y uso futuro.
- Baselines y métricas adquieren sentido al conectarse con costos.
- Preprocesamiento y selección se ajustan dentro de cada fold.
- La prueba mide una vez un protocolo reproducible y congelado.

**Resultado:** un buen experimento hace creíble la conexión entre datos históricos y decisiones futuras.
