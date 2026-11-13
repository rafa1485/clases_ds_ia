---
title: "Exploración, diagnóstico y visualización de datos"
subtitle: "De una tabla analítica a hallazgos defendibles"
course: "Data Science"
week: 3
class: 3
language: es
---

# Exploración, diagnóstico y visualización de datos

## De una tabla analítica a hallazgos defendibles

**Semana 3 · Clase 3**

**Diagrama conceptual:** `tabla analítica → vistas y resúmenes → controles → hallazgo defendible`.

Diagnóstico significa aquí indagación descriptiva: no identificación causal.

---

# Propósito y resultados

**Propósito:** explorar una tabla analítica mediante preguntas coordinadas sobre representación, distribución, relación y cobertura.

Al finalizar podremos:

- delimitar población, unidad, estimando y denominador;
- describir posición, dispersión, forma y extremos;
- elegir gráficos según la comparación requerida;
- estudiar asociaciones y estratos sin convertirlos en causas;
- redactar hallazgos trazables, limitados y comprobables.

Esta clase es teórica y conceptual: no incluye programación ni resultados empíricos.

---

# Continuidad semanas 1-3

| Semana | Pregunta central | Producto |
|---|---|---|
| 1. Formulación | ¿Qué necesidad, población y decisión importan? | problema analítico |
| 2. Preparación | ¿Qué representa cada fila y cómo se construyó? | tabla analítica defendible |
| 3. Exploración | ¿Cómo se distribuyen y relacionan los registros? | hallazgos limitados |

**Diagrama:** `formulación → adquisición y preparación → exploración → hallazgo`, con retornos desde exploración hacia preparación y formulación.

Explorar también audita las decisiones previas; no autoriza redefinirlas hasta obtener un patrón atractivo.

---

# Alcance del cronograma

| Bloque conceptual | Diapositivas |
|---|---:|
| Definición y fundamentos | 1-10 |
| Descripción univariada | 11-19 |
| Codificación visual | 20-25 |
| Relaciones | 26-34 |
| Tiempo, espacio y multivariado | 35-37 |
| Hallazgos y cierre | 38-40 |

Hoy no cubriremos pruebas confirmatorias, identificación causal, predicción ni despliegue.

La práctica se realizará después en un notebook que **todavía no forma parte de esta entrega**.

---

# Pregunta de apertura

> Tenemos una tabla zona-hora con pickups reportados, atributos de zona y clima de una estación: ¿qué miraríamos primero y qué podríamos afirmar?

| Dimensión | Pregunta inicial |
|---|---|
| Representación | ¿Qué significa una fila y qué quedó fuera? |
| Distribución | ¿Qué valores, frecuencias, ceros y faltantes existen? |
| Relación | ¿Qué variables varían juntas y bajo qué estratos? |
| Límite | ¿A qué población y periodo alcanza la evidencia? |

Los pickups TLC son viajes realizados y reportados, **no demanda total**. NOAA aporta contexto de una estación, **no clima zonal**.

---

# Qué es y qué no es EDA

El **análisis exploratorio de datos (EDA)** es una indagación disciplinada que combina revisión semántica, controles de calidad, resúmenes y visualizaciones complementarias.

| EDA sí | EDA no |
|---|---|
| examina distribuciones y cobertura | repara automáticamente los datos |
| contrasta representaciones | confirma historias descubiertas al mirar |
| localiza casos que requieren explicación | sustituye inferencia o diseño causal |
| genera hipótesis y controles | garantiza representatividad |

**Diagnóstico exploratorio no es causal:** produce comprensión provisional, no veredictos.

---

# Ciclo exploratorio

**Diagrama circular:**

`preguntar → revisar unidad y cobertura → visualizar → resumir → contrastar por estratos → registrar`

Retornos explícitos conectan visualización con calidad e interpretación con pregunta.

En el centro del ciclo se mantiene una **bitácora** de filtros, transformaciones, descartes, límites y explicaciones alternativas.

Iterar no significa buscar indefinidamente: cada cambio debe responder a evidencia y quedar trazado.

---

# Población, muestra y población registrada

| Concepto | Delimitación |
|---|---|
| Población objetivo | unidades sustantivas sobre las que interesa afirmar |
| Muestra observada | subconjunto obtenido mediante un mecanismo de selección |
| Población registrada | eventos materializados por el sistema dentro del alcance declarado |

**Diagrama conceptual:** la población registrada se superpone solo parcialmente con la población objetivo y la muestra observada queda dentro de la población registrada. “Archivo completo” no equivale a “población completa”.

Todos los pickups TLC reportados de un periodo pueden constituir la población registrada del estudio, pero excluyen solicitudes no atendidas, otros operadores y viajes no reportados.

Más filas no corrigen una frontera de cobertura.

---

# Unidad, estimando, ponderación y denominador

El **estimando** es la cantidad precisa que se desea describir. Cambia si cada zona, cada zona-hora o cada viaje reportado recibe el mismo peso.

Para una proporción:

$$
\widehat{p} = \frac{n_A}{n_{\mathrm{válido}}}
$$

Debemos poder completar:

> Este estadístico describe ___ para ___ durante ___, dando a cada ___ un peso de ___ y usando como denominador ___.

Una tasa de pickups por hora observada describe registros y exposición temporal; no estima por sí sola demanda total.

---

# Tipos semánticos y preguntas válidas

| Tipo | Operaciones conceptualmente válidas | Ejemplo del caso |
|---|---|---|
| Nominal | igualdad, conteo, agrupación | ID de zona |
| Ordinal | igualdad y orden | categoría ordenada |
| Intervalo | diferencias | temperatura Celsius |
| Razón | diferencias y razones | conteo de pickups |
| Temporal | orden, intervalo, ciclo | hora local |
| Espacial | ubicación, vecindad, área | zona de origen |

Que un ID sea numérico no vuelve significativa su media. Que la hora esté codificada como entero no elimina su dependencia cíclica.

La semántica, no el tipo físico, gobierna el resumen y el gráfico.

---

# Distribuciones de frecuencia

Para una categoría o intervalo $j$:

$$
f_j = \sum_{i=1}^{n}\mathbb{1}(x_i\in j),
\qquad
h_j = \frac{f_j}{n_{\mathrm{válido}}},
\qquad
H_j = \sum_{k\leq j}h_k
$$

| Medida | Lectura |
|---|---|
| $f_j$ | frecuencia absoluta |
| $h_j$ | frecuencia relativa |
| $100h_j$ | porcentaje |
| $H_j$ | frecuencia acumulada, solo si existe orden |

La distribución debe informar valores válidos, faltantes, exclusiones y denominador.

---

# Cero, faltante y ausencia de fila

| Situación | Representación | Pregunta de control |
|---|---|---|
| Cero | existe fila y valor $0$ | ¿se observó realmente ausencia del evento? |
| Faltante | existe fila, falta el valor | ¿falló medición, unión o disponibilidad? |
| Ausencia de fila | no existe la unidad esperada | ¿el marco debía contenerla? |

**Diagrama:** un marco completo zona-hora apunta a tres tarjetas: `fila con 0`, `fila con celda vacía`, `combinación inexistente`.

Sin un marco esperado no puede distinguirse “cero pickups reportados” de “zona-hora no materializada”. Un valor NOAA faltante no equivale a precipitación cero.

---

# Media, mediana y moda

La media aritmética de valores válidos es:

$$
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
$$

| Centro | Interpretación | Sensibilidad |
|---|---|---|
| Media | punto de balance de magnitudes | alta ante extremos |
| Mediana | posición que divide datos ordenados | menor ante extremos |
| Moda | valor o categoría más frecuente | depende de resolución |

Para pickups por zona-hora, cada centro responde una pregunta diferente dentro de los viajes realizados/reportados. Ninguno describe por sí solo colas o cobertura.

---

# Cuantiles y percentiles

El cuantil conceptual de orden $p$ puede expresarse como:

$$
Q(p)=\inf\{x:F(x)\geq p\}, \qquad 0<p<1
$$

$Q_1=Q(0.25)$, la mediana es $Q(0.50)$ y $Q_3=Q(0.75)$. Los percentiles expresan el orden en cien partes.

**Diagrama conceptual:** una secuencia ordenada marca $Q_1$, mediana, $Q_3$ y un percentil alto; las áreas representan proporciones observadas aproximadas.

Un P90 describe una posición en la población y periodo declarados; no es la probabilidad del próximo caso. Las convenciones muestrales pueden interpolar de modo distinto.

---

# Rango, varianza y desviación estándar

$$
R=x_{\max}-x_{\min}
$$

$$
\sigma^2=\frac{1}{N}\sum_{i=1}^{N}(x_i-\mu)^2,
\qquad
s^2=\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2,
\qquad
s=\sqrt{s^2}
$$

El rango usa solo extremos; la varianza queda en unidades al cuadrado; la desviación estándar recupera la unidad original.

$N$ describe la varianza de una población finita; bajo supuestos de muestreo, $n-1$ corrige el sesgo de la varianza muestral como estimador de una varianza poblacional. La regla 68-95 requiere una forma aproximadamente normal y no es universal.

---

# IQR, MAD y robustez

$$
IQR=Q_3-Q_1,
\qquad
MAD=\operatorname{mediana}_i\left|x_i-\operatorname{mediana}(x)\right|
$$

| Medida robusta | Qué resume |
|---|---|
| IQR | extensión del 50 % central |
| MAD | distancia absoluta típica respecto de la mediana |

Son menos sensibles a valores extremos que rango, varianza y desviación estándar.

**Robustez no es representatividad:** mediana e IQR no recuperan viajes no registrados ni corrigen faltantes sistemáticos.

---

# Asimetría, colas y multimodalidad

**Diagrama conceptual:** cuatro curvas sin datos representan simetría, cola derecha, cola izquierda y dos modos.

| Rasgo | Pregunta que abre |
|---|---|
| Asimetría | ¿qué lado concentra la cola? |
| Cola | ¿hay extremos, censura o mezcla? |
| Multimodalidad | ¿coexisten grupos, ciclos o resoluciones? |
| Acumulación | ¿existen redondeo, umbral o saturación? |

Una segunda moda en pickups zona-hora puede sugerir franjas, zonas o reglas mezcladas. Es una hipótesis para revisar, no evidencia de una causa.

---

# Atípico no equivale a error

La regla de Tukey marca valores fuera de:

$$
[Q_1-1.5\,IQR,\;Q_3+1.5\,IQR]
$$

| Caso señalado | Acción responsable |
|---|---|
| plausible y relevante | conservar y contextualizar |
| compatible pero influyente | evaluar sensibilidad |
| incompatible con unidad o dominio | revisar captura y transformación |
| significado desconocido | investigar antes de decidir |

Una zona-hora extrema puede corresponder a aeropuerto, evento, error de agregación u otra explicación. La distancia estadística no justifica eliminarla.

---

# Perfil estadístico coherente

| Componente | Control mínimo |
|---|---|
| Definición | población, unidad, periodo, estimando |
| Cobertura | válidos, faltantes, ceros, filas ausentes |
| Distribución | frecuencias y forma |
| Posición | centro y cuantiles |
| Dispersión | clásica y robusta |
| Extremos | plausibilidad e influencia |
| Sensibilidad | filtros, resolución y denominador |
| Conclusión | afirmación permitida y límite |

Todas las piezas deben compartir reglas de inclusión o declarar sus diferencias. Un perfil no es una colección de cifras desconectadas.

---

# Visualización como codificación

**Diagrama bidireccional:**

`datos definidos ↔ transformación ↔ marcas y canales ↔ comparación ↔ interpretación`

- **Marcas:** puntos, líneas y áreas.
- **Canales:** posición, longitud, color, forma y tamaño.
- **Decisiones:** escala, agregación, orden, denominador y exclusiones.

Un gráfico no es una ventana neutral: decide qué comparación será fácil y qué información quedará menos visible.

---

# Posición, longitud, área y color

| Canal | Precisión comparativa | Uso apropiado |
|---|---|---|
| Posición común | alta | diferencias y orden |
| Longitud | alta a media | magnitudes desde una base |
| Área | media a baja | tamaño aproximado |
| Color | media a baja | patrón, categoría o intensidad |

Paleta secuencial: magnitud. Paleta divergente: distancia respecto de un centro significativo. Paleta cualitativa: categorías.

El faltante necesita una apariencia propia. El área debe ser proporcional al dato, no su radio, y el color no debe exagerar diferencias.

---

# Matriz de selección de gráficos

| Objetivo | Vistas posibles | Control principal |
|---|---|---|
| Comparar magnitudes | puntos, barras | base y orden |
| Mostrar distribución | histograma, caja, violín | resolución y tamaño |
| Relacionar variables | dispersión, tabla | unidad conjunta |
| Mostrar tiempo | línea, mapa día-hora | orden, huecos y frecuencia |
| Mostrar composición | barras apiladas | denominador y volumen |
| Mostrar espacio | mapa | medida, cobertura y proyección |

Una tabla es preferible cuando se necesitan valores exactos. La pregunta y la tarea perceptiva determinan la vista, no el nombre de la variable.

---

# Histogramas, intervalos y densidad

Un histograma agrupa observaciones numéricas en intervalos. Su apariencia depende de anchura, origen y límites de los bins.

**Diagrama conceptual:** tres histogramas del mismo conjunto usan intervalos anchos, intermedios y estrechos; una curva separada representa una densidad suavizada.

- probar resoluciones ayuda a distinguir estructura estable de artefactos;
- con intervalos desiguales, el **área** debe representar proporción;
- una densidad es una estimación y depende del ancho de banda;
- comparar grupos exige límites y escalas comunes.

No se debe escoger la resolución que produzca la historia más llamativa.

---

# Caja y violín

| Vista | Aporta | Depende de |
|---|---|---|
| Caja | mediana, cuartiles, IQR, bigotes y puntos externos | convención de bigotes |
| Violín | forma y modos aproximados | suavizado y ancho de banda |

**Diagrama conceptual:** caja y violín describen una misma distribución; una segunda pareja muestra que cajas parecidas pueden ocultar formas diferentes.

Al comparar franjas de pickups reportados deben conservarse periodo, unidad, reglas y escala; también debe mostrarse cuántas zona-horas aporta cada grupo.

Estas vistas describen diferencias: no las prueban ni convierten puntos externos en errores.

---

# Barras, conteos, proporciones y tasas

$$
\text{proporción}=\frac{\text{casos de interés}}{\text{total definido}},
\qquad
\text{tasa}=\frac{\text{eventos}}{\text{exposición}}
$$

| Cantidad | Pregunta |
|---|---|
| Conteo | ¿cuántos eventos registrados? |
| Proporción | ¿qué parte del total declarado? |
| Tasa | ¿cuántos por unidad de exposición? |

Las barras de magnitud suelen comenzar en cero. Pickups por zona son conteos; pickups por hora observada son una tasa descriptiva. Ninguna cantidad equivale a demanda total sin otro mecanismo y denominador.

---

# Secuencia para estudiar relaciones

**Ruta conceptual con retornos:**

`comprender variables → revisar faltantes → confirmar unidad conjunta → visualizar → comparar estratos → cuantificar → revisar influencia → registrar alternativas`

Dos candados preceden a la interpretación:

1. forma, escala y pares válidos antes del coeficiente;
2. estratos, dependencia y explicaciones alternativas antes del hallazgo.

Para relacionar NOAA con pickups, una vista horaria evita tratar la misma observación de estación repetida entre zonas como muchas observaciones climáticas independientes.

---

# Tablas de contingencia

Una tabla de contingencia cruza dos variables categóricas:

|  | Categoría B1 | Categoría B2 | Total de fila |
|---|---:|---:|---:|
| Categoría A1 | $n_{11}$ | $n_{12}$ | $n_{1\cdot}$ |
| Categoría A2 | $n_{21}$ | $n_{22}$ | $n_{2\cdot}$ |
| Total de columna | $n_{\cdot1}$ | $n_{\cdot2}$ | $n$ |

Cada celda contiene un conteo conjunto; los márgenes describen volumen. Bajo independencia, el conteo esperado conceptual es $e_{ij}=n_{i\cdot}n_{\cdot j}/n$.

Los conteos todavía no establecen comparabilidad: primero debe elegirse el condicionamiento.

---

# Proporciones condicionadas

$$
P(B_j\mid A_i)\approx\frac{n_{ij}}{n_{i\cdot}},
\qquad
P(A_i\mid B_j)\approx\frac{n_{ij}}{n_{\cdot j}}
$$

| Normalización | Suma 100 % dentro de | Pregunta |
|---|---|---|
| Por fila | cada fila | ¿cómo se distribuye B entre unidades A? |
| Por columna | cada columna | ¿cómo se distribuye A entre unidades B? |

“Proporción de zona-horas de volumen alto dentro de cada franja” no equivale a su frase inversa.

Toda proporción condicionada debe nombrar **dentro de qué** se calcula y mostrar el tamaño del grupo.

---

# Comparación numérica entre grupos

Antes de comparar, exigir:

| Control común | Pregunta |
|---|---|
| Unidad | ¿cada observación representa lo mismo? |
| Periodo y marco | ¿los grupos tuvieron oportunidades comparables? |
| Inclusión | ¿ceros y faltantes siguen la misma regla? |
| Cobertura y tamaño | ¿cuántas unidades válidas aporta cada grupo? |
| Distribución | ¿cómo cambian centro, dispersión, forma y colas? |

**Diagrama:** paneles por grupo con escala común, cobertura y $n$, sin valores ni diferencias inventadas.

Segmentar aquí significa comparar estratos definidos y reproducibles, **no clustering formal**.

---

# Diagrama de dispersión

Cada punto debe tener una unidad explícita. Antes de ajustar o resumir, observar:

- rango y dirección;
- curvatura y límites;
- grupos y heterogeneidad;
- sobreposición y densidad;
- puntos potencialmente influyentes.

**Diagrama conceptual:** cuatro nubes sin coeficientes representan relación lineal, relación curva, grupos y un caso influyente.

En el caso transversal, cada punto podría ser una hora con pickups reportados agregados y una observación NOAA; no una zona-hora con clima artificialmente replicado.

---

# Covarianza y correlación

$$
s_{xy}=\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y}),
\qquad
r=\frac{s_{xy}}{s_xs_y},\quad -1\leq r\leq 1
$$

| Medida | Resume | Escala |
|---|---|---|
| Covarianza | variación lineal conjunta | producto de unidades |
| Pearson | asociación lineal estandarizada | sin unidades |
| Spearman / Kendall | asociación de orden monotónica | rangos u orden |

Correlación cero no implica independencia. Ningún coeficiente demuestra causalidad ni reemplaza la nube, la unidad y los estratos.

---

# Trampas de correlación

| Trampa | Qué puede ocultar |
|---|---|
| No linealidad | dependencia fuerte con $r$ cercano a cero |
| Punto influyente | coeficiente dominado por un caso |
| Rango restringido | relación atenuada por selección |
| Mezcla de grupos | patrón global distinto de patrones internos |
| Pseudorreplicación | tamaño aparente mayor que la información independiente |
| Multiplicidad | asociaciones casuales entre muchas búsquedas |

Replicar NOAA en todas las zonas no crea nuevas observaciones meteorológicas. Elegir el coeficiente que mejor respalda una historia es una decisión exploratoria sesgada.

---

# Asociación, causalidad, confusión y Simpson

| Concepto | Afirmación permitida |
|---|---|
| Asociación | la distribución conjunta no se explica como producto de las marginales |
| Causalidad | una intervención cambiaría un resultado bajo un diseño y supuestos |
| Confusión | una causa común previa puede distorsionar la asociación entre exposición y resultado |
| Simpson | el patrón agregado cambia o se invierte dentro de estratos |

**Diagrama conceptual:** $Z$ apunta a $X$ y $Y$ como hipótesis de causa común; tendencias internas por estrato pueden diferir de la tendencia agregada. Que una variable se asocie con ambas no basta para clasificarla como confusor.

“La lluvia causa más demanda” no está autorizada. Puede estudiarse si precipitación de la estación y pickups reportados coinciden, considerando hora, día, oferta, cobertura y otras alternativas.

---

# Segmentación y estratificación

- **Segmentar:** describir subconjuntos sustantivos.
- **Estratificar:** comparar una distribución o relación dentro de niveles de una tercera variable.

| Estrato útil | Riesgo a controlar |
|---|---|
| relevante para el dominio | partición oportunista |
| definido de forma reproducible | regla modificada después de mirar |
| con tamaño y cobertura visibles | celdas escasas |
| comparado en escalas comunes | exageración visual |

Aquí segmentación significa comparar estratos como franja, borough o tipo de zona; **no significa clustering formal**. Estratificar revela heterogeneidad, pero no identifica causas.

---

# Exploración temporal

El tiempo incorpora orden, dependencia, calendario y frecuencia. Una vista temporal debe declarar:

- evento temporal y zona horaria;
- intervalo y regularidad;
- huecos y cobertura;
- ciclos y calendario;
- cambios de definición o captura.

**Diagrama conceptual:** una serie con puntos regulares, un hueco visible y una anotación de cambio de definición, sin unir artificialmente observaciones ausentes.

Una línea temporal de pickups describe viajes reportados. Una coincidencia con NOAA describe una estación. **Temporal no significa pronóstico** y precedencia no demuestra causa.

---

# Exploración espacial

| Vista espacial | Uso | Control |
|---|---|---|
| Coropleta | tasa o proporción por área | denominador y cortes |
| Símbolos o puntos | localización y magnitud | sobreposición y privacidad |
| Mapa de cobertura | presencia, ausencia y calidad | cero distinto de sin dato |

**Diagrama conceptual:** tres mapas de la misma geometría distinguen conteo, tasa y cobertura; la tabla exige separar cero de faltante en toda implementación posterior.

Un mapa TLC localiza pickups realizados/reportados, no demanda total. Asociar NOAA por hora no convierte una estación en clima de cada zona. El mapa describe dónde aparece una medida; no explica por qué.

---

# Exploración multivariada y riesgo exploratorio

Matrices de pares, mapas de calor y facetas pueden revelar redundancia, grupos y casos extraños en combinación.

| Decisión | Control necesario |
|---|---|
| Elegir variables | justificación sustantiva |
| Estandarizar | recordar que escala común no implica igual importancia |
| Filtrar y facetar | registrar universo de decisiones |
| Seleccionar patrón | conservar resultados discordantes y alternativas |

**Diagrama:** una frontera separa `hipótesis generada` de `evaluación futura`.

Cuantas más variables, filtros y cortes se prueben, mayor es la posibilidad de hallar casualidades y mayor debe ser la transparencia.

---

# Anatomía de un hallazgo defendible

| Campo | Contenido |
|---|---|
| Definición | pregunta, población, unidad y periodo |
| Observación | patrón y magnitud obtenidos de evidencia |
| Soporte | tabla o figura trazable |
| Cobertura | válidos, faltantes, exclusiones y denominador |
| Interpretación | lenguaje proporcional al diseño |
| Defensa | alternativa, sensibilidad, límite y siguiente control |

Plantilla sin resultado: “En [periodo y unidades], los pickups TLC realizados/reportados muestran [patrón por completar], bajo [cobertura]. Coincide con [variable], pero puede reflejar [alternativas]. NOAA representa una estación, no clima zonal”.

Usar “se observa” o “se asocia”, no “produce” o “causa”.

---

# Definición de cinco hallazgos y continuidad

El **futuro notebook**, aún no creado y **no incluido en esta entrega**, deberá materializar una estructura reproducible para cinco hallazgos complementarios:

| Hallazgo requerido | Pregunta que deberá resolver |
|---|---|
| 1. Distribución univariada | ¿cómo se distribuye una variable bajo cobertura declarada? |
| 2. Comparación de grupos | ¿qué cambia entre estratos comparables? |
| 3. Relación entre variables | ¿qué forma de asociación aparece y qué alternativas existen? |
| 4. Patrón temporal | ¿qué orden, ciclos, huecos o cambios se observan, sin pronosticar? |
| 5. Patrón espacial o multivariado | ¿qué heterogeneidad aparece bajo medida y denominador explícitos? |

Cada hallazgo incluirá definición, evidencia, cobertura, ceros/faltantes, extremos, sensibilidad, límite y próximo paso. No hay resultados predeterminados que deban encontrarse.

---

# Síntesis y lecturas

1. Población no es archivo; estimando, peso y denominador fijan la pregunta.
2. Cero, faltante y ausencia de fila son estados diferentes.
3. Distribución, forma y cobertura preceden a cualquier resumen.
4. Robustez no corrige sesgo; atípico no equivale a error.
5. Un gráfico es una codificación y un coeficiente no reemplaza la forma.
6. Asociación no implica causalidad; diagnóstico exploratorio genera hipótesis.
7. Segmentación compara estratos, temporal no significa pronóstico y un mapa no explica.
8. Todo hallazgo necesita alcance, alternativas, sensibilidad y siguiente comprobación.

**Lectura principal:** capítulo 4, *Estadística descriptiva, exploración y visualización*, del libro *Ciencia de Datos e Inteligencia Artificial*. Como continuidad, revisar los capítulos 2 y 3 sobre formulación, cobertura y preparación.

> Explorar responsablemente es describir con precisión, comparar con honestidad y mantener visibles los límites de los registros TLC y del contexto NOAA.
