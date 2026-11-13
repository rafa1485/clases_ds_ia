---
title: "Probabilidad, incertidumbre y decisiones"
subtitle: "De una muestra observada a una acción defendible"
course: "Data Science"
week: 4
class: 4
language: es
---

# Probabilidad, incertidumbre y decisiones

## De una muestra observada a una acción defendible

**Semana 4 · Clase 4**

**Recorrido conceptual:** `muestra → estimación → incertidumbre → decisión`.

*La muestra aporta evidencia parcial; la estimación resume lo observado; la incertidumbre reconoce lo que puede variar; la decisión incorpora consecuencias.*

---

# De los hallazgos a las decisiones

En la Semana 3 aprendimos a describir distribuciones y asociaciones. Ahora preguntaremos cuánto podemos generalizar y cómo actuar cuando el resultado todavía es incierto.

| Etapa | Pregunta | Producto |
|---|---|---|
| Explorar | ¿Qué patrón aparece? | hallazgo descriptivo |
| Estimar | ¿Qué cantidad desconocida aproximamos? | estimación |
| Cuantificar | ¿Cuánto podría cambiar? | medida de incertidumbre |
| Decidir | ¿Qué acción conviene? | regla explícita |

*Las etapas se conectan, pero no son equivalentes: observar un patrón no determina automáticamente una acción.*

---

# Propósito y resultados de aprendizaje

**Propósito:** comprender cómo la probabilidad representa incertidumbre y cómo una decisión agrega objetivos, costos y restricciones a la evidencia disponible.

Al finalizar podremos:

- definir población, muestra, parámetro y estimación;
- calcular probabilidades marginales, conjuntas y condicionales;
- interpretar independencia y actualización bayesiana;
- reconocer variabilidad muestral y evaluar estabilidad;
- distinguir descripción, predicción y prescripción;
- comparar acciones mediante consecuencias esperadas.

*La clase desarrolla razonamiento conceptual y ejemplos numéricos breves; no entrena todavía un modelo predictivo.*

---

# Continuidad de las semanas 1 a 4

| Semana | Pregunta central | Producto |
|---|---|---|
| 1. Formulación | ¿Qué necesidad y decisión importan? | problema analítico |
| 2. Preparación | ¿Qué representa cada fila? | tabla defendible |
| 3. Exploración | ¿Qué patrones aparecen? | hallazgos limitados |
| 4. Incertidumbre | ¿Qué puede variar y cómo decidimos? | regla de decisión |

**Diagrama:** `problema → datos → hallazgo → estimación → decisión`, con retornos hacia etapas anteriores.

*Los retornos indican que una estimación inestable puede exigir más datos y que una decisión inviable puede obligar a reformular la pregunta.*

---

# Pregunta de apertura: ¿qué tan probable es?

Una organización dispone de muestras históricas de calidad del agua y solo puede revisar algunos sitios. Desea priorizar aquellos con mayor posibilidad de detectar coliformes.

Antes de responder necesita precisar:

- qué evento contará como detección;
- qué población y periodo desea representar;
- qué evidencia estaba disponible antes de decidir;
- qué costo tiene revisar y qué costo tiene omitir;
- cuántas revisiones puede realizar.

---

# Describir no es predecir

| Afirmación | Tipo | Alcance temporal |
|---|---|---|
| “El 3 % de las muestras registradas tuvo detección” | descriptiva | datos observados |
| “Una nueva muestra tiene 3 % de probabilidad de detección” | predictiva | caso no observado |
| “Conviene revisar este sitio” | prescriptiva | acción y consecuencias |

La primera frase resume un archivo; la segunda generaliza bajo supuestos; la tercera agrega una comparación entre acciones.

*El cambio de verbo revela un cambio de pregunta: frecuencia observada, incertidumbre futura y elección no son sinónimos.*

---

# Población, muestra y unidad de análisis

- **Población objetivo:** conjunto sobre el cual interesa afirmar o decidir.
- **Muestra:** subconjunto efectivamente observado mediante un mecanismo de selección.
- **Unidad de análisis:** objeto representado por cada observación utilizada.
- **Población registrada:** eventos capturados por el sistema durante el alcance declarado.

**Diagrama:** `población objetivo ⊃ población accesible ⊃ muestra observada`.

*Los bloques representan inclusiones conceptuales: cada reducción puede excluir unidades y modificar qué generalizaciones son razonables.*

En el caso del agua, una fila representa una muestra tomada en un sitio, fecha y hora; no representa automáticamente a todos los hogares ni a toda el agua distribuida.

---

# Parámetro, estadístico y estimación

Un **parámetro** es una cantidad fija pero generalmente desconocida de la población, como una proporción de detección $p$. Un **estadístico** es una función de los datos, como la proporción muestral:

$$
\widehat p=\frac{x}{n}
$$

donde $x$ es el número de detecciones válidas y $n$ el número de muestras válidas.

| Objeto | Se refiere a | Estado |
|---|---|---|
| $p$ | población definida | desconocido |
| $\widehat p$ | muestra observada | calculable |

*Usamos el estadístico como estimación del parámetro; la igualdad entre ambos no está garantizada.*

---

# ¿Por qué cambia una estimación?

Si repitiéramos el proceso de muestreo, las unidades seleccionadas y los resultados podrían ser diferentes. Por eso $\widehat p$ o $\bar x$ varían entre muestras aun cuando la población permanezca estable.

**Diagrama:** `misma población → muestra A / muestra B / muestra C → estimaciones distintas`.

*Las ramas representan repeticiones hipotéticas del mismo diseño. La dispersión entre resultados expresa variabilidad muestral, no un error de programación.*

Cuanto menor sea la muestra o más raro sea el evento, más visibles pueden ser esas diferencias relativas.

---

# Sesgo y variabilidad: dos problemas distintos

| Propiedad | Pregunta | Ejemplo |
|---|---|---|
| Sesgo | ¿el procedimiento apunta sistemáticamente fuera del objetivo? | solo se visitan sitios accesibles |
| Variabilidad | ¿cuánto cambia el resultado entre muestras? | pocos resultados por sitio |

**Diagrama de blancos:** agrupación compacta desplazada = baja variabilidad y alto sesgo; agrupación dispersa centrada = bajo sesgo y alta variabilidad.

*La posición media representa sesgo; la separación entre puntos representa variabilidad. Son dimensiones diferentes y requieren soluciones diferentes.*

**Advertencia crítica:** una muestra enorme puede producir una cifra muy estable y, al mismo tiempo, estar sistemáticamente sesgada.

---

# Cobertura, selección y representatividad

La cobertura indica qué parte de la población pudo entrar en el registro. La selección describe cómo unas unidades terminaron observadas y otras no.

| Mecanismo | Posible efecto |
|---|---|
| horarios operativos limitados | ciertas franjas quedan subrepresentadas |
| remuestreo tras una detección | los eventos positivos reciben más observaciones |
| sitios con acceso más sencillo | cambia la composición espacial |
| valores inválidos excluidos | quedan menos casos válidos y la proporción puede cambiar |

Excluir un registro no solo reduce el denominador. Si los resultados inválidos se concentran en ciertos sitios, periodos o condiciones, la proporción calculada también puede quedar sesgada.

*La representatividad depende del mecanismo que produjo los datos, no únicamente del número de filas.*

---

# Tipos de muestreo

| Diseño | Regla básica ampliada |
|---|---|
| Aleatorio simple | construir un marco completo y sortear $n$ unidades; cada conjunto posible de tamaño $n$ debe tener la misma probabilidad de selección |
| Estratificado | dividir la población en grupos exhaustivos y mutuamente excluyentes; sortear unidades dentro de cada grupo y combinar los resultados respetando sus pesos |

En ambos diseños la selección se realiza al azar y parte de un marco definido. La diferencia es que el aleatorio simple realiza un único sorteo sobre toda la población, mientras que el estratificado realiza sorteos separados para asegurar representación de cada grupo.

*El diseño no consiste en tomar filas al azar de una tabla ya disponible: define las probabilidades de inclusión y las ponderaciones necesarias para representar la población.*

---

# Muestreo aleatorio simple

En un muestreo aleatorio simple de tamaño $n$, cada conjunto posible de $n$ unidades tiene la misma probabilidad de ser elegido.

Proceso conceptual:

1. definir un marco con las unidades elegibles;
2. asignar una selección aleatoria reproducible;
3. observar las unidades seleccionadas;
4. registrar no respuesta o imposibilidad de medición.

*El marco es anterior al sorteo: si una unidad no figura en él, no puede ser seleccionada y la aleatoriedad no corrige esa ausencia.*

Es un diseño transparente, pero puede producir pocos casos de grupos pequeños que sean importantes para la decisión.

---

# Muestreo estratificado

La población se divide en estratos mutuamente excluyentes, como sitio, estación o tipo de muestra, y se seleccionan unidades dentro de cada uno.

**Diagrama:** `población → estratos A, B y C → muestra de cada estrato → combinación ponderada`.

*La separación garantiza presencia de grupos; la combinación final debe recuperar sus pesos poblacionales si las fracciones de muestreo fueron distintas.*

Puede mejorar precisión cuando los estratos son internamente homogéneos y permite comparar grupos relevantes con tamaños suficientes.

---

# La muestra como proceso de medición

Una fila observada es el resultado de varias etapas:

`unidad elegible → selección → acceso → medición → registro → validación → análisis`

*Cada bloque puede excluir unidades o alterar valores. Las flechas describen un proceso de producción de evidencia, no una simple lectura neutral de la realidad.*

| Etapa | Pregunta concreta |
|---|---|
| Selección | ¿por qué se observó esta unidad? |
| Medición | ¿qué instrumento y límite se usaron? |
| Registro | ¿cómo se codificaron censura y faltantes? |
| Validación | ¿qué reglas determinaron un resultado válido? |

---

# Evento, resultado y espacio muestral

Un **experimento aleatorio** produce uno de varios resultados posibles. El **espacio muestral** $\Omega$ reúne esos resultados y un **evento** es un subconjunto de ellos.

Para una muestra microbiológica simplificada:

$$
\Omega=\{\text{no detectado},\text{detectado},\text{resultado inválido}\}
$$

El evento $D$ puede definirse como “resultado microbiológico válido con detección”.

*El rectángulo $\Omega$ contiene todos los resultados previstos; la región $D$ agrupa solo aquellos que cumplen la definición del evento.*

Definir el evento antes de contar evita modificarlo para acomodar los datos obtenidos.

---

# Probabilidad como proporción de largo plazo

Si un procedimiento se repitiera en condiciones comparables, la frecuencia relativa de un evento puede aproximarse a una probabilidad:

$$
P(D)\approx\frac{\text{detecciones válidas}}{\text{muestras válidas}}
$$

Una probabilidad también puede expresar incertidumbre sobre un caso particular, siempre que se especifique la información disponible.

| Valor | Lectura |
|---:|---|
| 0 | evento imposible bajo el modelo |
| entre 0 y 1 | distintos grados de posibilidad |
| 1 | evento seguro bajo el modelo |

*La probabilidad se interpreta dentro de un modelo y una población definidos; no es una propiedad aislada de una etiqueta.*

---

# Probabilidad marginal y complemento

La probabilidad **marginal** considera un evento sin fijar otra condición. El complemento reúne todos los resultados en los que el evento no ocurre:

$$
P(D^c)=1-P(D)
$$

Si $P(D)=0{,}04$, entonces $P(D^c)=0{,}96$.

**Diagrama:** el espacio completo se divide en dos regiones sin superposición: $D$ y $D^c$.

*Ambas regiones cubren todos los resultados posibles; aumentar una reduce necesariamente la otra.*

La categoría “inválido” debe resolverse en la definición del universo antes de tratar “no detectado” como complemento de “detectado”.

---

# Probabilidad conjunta

La intersección $A\cap B$ contiene los resultados donde ocurren ambos eventos. Su probabilidad es conjunta:

$$
P(A\cap B)
$$

Ejemplo: $A=$ “muestra tomada en verano” y $B=$ “detección”. La intersección cuenta detecciones ocurridas en verano.

| Cantidad | Pregunta |
|---|---|
| $P(A)$ | ¿qué proporción pertenece al verano? |
| $P(B)$ | ¿qué proporción presenta detección? |
| $P(A\cap B)$ | ¿qué proporción cumple ambas condiciones? |

*En un diagrama de conjuntos, la zona superpuesta representa casos compartidos; no expresa todavía una probabilidad condicionada.*

---

# Probabilidad condicional

La probabilidad condicional restringe el universo a los casos donde ocurrió $B$:

$$
P(A\mid B)=\frac{P(A\cap B)}{P(B)},\qquad P(B)>0
$$

Para $P(D\mid V)$, primero conservamos las muestras de verano $V$ y luego calculamos qué proporción tuvo detección $D$.

**Diagrama:** `todas las muestras → filtrar B → medir la fracción A dentro de B`.

*La barra vertical se lee “dado que”: modifica el denominador y, por tanto, la pregunta respondida.*

---

# Independencia y asociación

Dos eventos son independientes cuando conocer uno no cambia la probabilidad del otro:

$$
P(A\mid B)=P(A)
$$

Equivalentemente, si las probabilidades son positivas:

$$
P(A\cap B)=P(A)P(B)
$$

Para estudiar si la detección $D$ se relaciona con el verano $V$, primero calculamos la proporción de detecciones entre todas las muestras, $P(D)$. Luego calculamos la proporción únicamente entre las muestras de verano, $P(D\mid V)$.

Si ambas probabilidades son iguales, saber que una muestra pertenece al verano no modifica la probabilidad de detección y los eventos son independientes. En datos muestrales esperamos valores aproximados, por lo que una diferencia pequeña puede deberse a variabilidad del muestreo.

Si $P(D\mid V)$ se aparta claramente de $P(D)$, la detección cambia al restringirnos al verano. Esto indica asociación entre ambos eventos dentro de la población y el periodo definidos.

*La independencia es una propiedad de la distribución conjunta definida; no significa que las variables carezcan de toda relación física o causal.*

---

# Un error frecuente: invertir la condición

Estas cantidades responden preguntas distintas:

$$
P(\text{alerta}\mid\text{detección})
\neq
P(\text{detección}\mid\text{alerta})
$$

| Expresión | Pregunta |
|---|---|
| $P(A\mid D)$ | entre las detecciones, ¿cuántas generan alerta? |
| $P(D\mid A)$ | entre las alertas, ¿cuántas son detecciones? |

**Advertencia crítica:** una alerta sensible puede aparecer en casi todas las detecciones y aun así producir muchas falsas alarmas si la detección es rara.

*Cambiar el orden cambia el grupo usado como denominador; por eso las dos probabilidades no son intercambiables.*

---

# Estimaciones y tamaño de muestra

Una estimación basada en pocos casos suele cambiar más entre muestras que otra basada en muchos casos comparables.

| Sitio | Detecciones | Muestras | Proporción observada |
|---|---:|---:|---:|
| A | 1 | 2 | 50 % |
| B | 40 | 100 | 40 % |

La proporción de A es mayor, pero está sostenida por solo dos observaciones. Una observación adicional podría modificarla drásticamente.

**Diagrama:** barras de igual escala acompañadas por denominadores muy diferentes.

*La altura comunica la estimación puntual; el denominador comunica cuánta evidencia la sostiene. Ambas piezas deben leerse juntas.*

---

# Ejemplo numérico: el denominador importa

Dos sitios parten de proporciones observadas similares, pero con tamaños muy distintos:

| Sitio | Situación inicial | Nueva muestra | Proporción resultante |
|---|---:|---|---:|
| A | $1/2=50\%$ | sin detección | $1/3=33{,}3\%$ |
| B | $40/100=40\%$ | sin detección | $40/101=39{,}6\%$ |

- En A, una observación cambia la estimación en $16{,}7$ puntos porcentuales.
- En B, la misma clase de observación la cambia en apenas $0{,}4$ puntos.

**Resultado:** informar numerador y denominador permite distinguir una proporción inestable de otra sostenida por más evidencia.

---

# Variabilidad muestral de una proporción

Bajo ensayos aproximadamente independientes con probabilidad constante, el error estándar estimado de una proporción es:

$$
SE(\widehat p)\approx\sqrt{\frac{\widehat p(1-\widehat p)}{n}}
$$

El error estándar disminuye cuando aumenta $n$, pero lo hace con la raíz cuadrada: cuadruplicar la muestra reduce aproximadamente a la mitad esta variabilidad.

**Diagrama:** distribuciones de $\widehat p$ para tamaños pequeño, medio y grande, centradas en el mismo valor y progresivamente más estrechas.

*El ancho representa cuánto cambiaría la estimación entre repeticiones comparables; no representa variabilidad entre individuos.*

---

# Ejemplo numérico: precisión y decisión

En un sitio se observa $\widehat p=0{,}20$. Si la proporción se mantiene al ampliar la muestra:

| $n$ | Error estándar | Rango aproximado $\widehat p\pm2SE$ |
|---:|---:|---:|
| 100 | $\sqrt{0{,}20(0{,}80)/100}=0{,}04$ | $[0{,}12;\,0{,}28]$ |
| 400 | $\sqrt{0{,}20(0{,}80)/400}=0{,}02$ | $[0{,}16;\,0{,}24]$ |

**Ejemplo con una regla supuesta: priorizar el sitio si la proporción supera el 15 %:**

- Con $n=100$, el rango va del 12 % al 28 %: otra muestra comparable podría ubicar la estimación por debajo o por encima del umbral y cambiar la decisión.
- Con $n=400$, todo el rango supera el 15 %, por lo que la decisión de priorizar es más estable.

**Resultado:** reducir el error estándar a la mitad produce una estimación más precisa y una decisión más estable frente a fluctuaciones entre muestras comparables.

---

# Variabilidad muestral de una media

Para observaciones independientes con dispersión finita, el error estándar estimado de la media es:

$$
SE(\bar x)\approx\frac{s}{\sqrt n}
$$

- $s$ resume cuánto difieren las observaciones entre sí;
- $n$ indica cuántas observaciones independientes sostienen la media;
- $SE(\bar x)$ resume cuánto variaría la media entre muestras.

*La desviación estándar describe datos individuales; el error estándar describe la estabilidad del estimador. Responden preguntas distintas.*

Si varias mediciones provienen del mismo sitio o episodio, el número de filas puede exagerar la información independiente disponible.

---

# Ejemplo numérico: estabilidad de una media

La concentración media observada es $18$ mg/L y la desviación estándar es $s=5$ mg/L.

| $n$ | Cálculo | Error estándar |
|---:|---:|---:|
| 25 | $5/\sqrt{25}$ | $1$ mg/L |
| 100 | $5/\sqrt{100}$ | $0{,}5$ mg/L |

- Las mediciones individuales conservan una dispersión de $5$ mg/L.
- La media calculada con $100$ observaciones presenta la mitad del error estándar que la media calculada con $25$.

**Uso práctico:** una media más estable permite comparar periodos o sitios con menor sensibilidad a qué observaciones integraron la muestra.

---

# Bootstrap: evaluar estabilidad

El bootstrap aproxima la variabilidad de un estadístico mediante remuestreo con reemplazo:

1. tomar una muestra bootstrap del mismo tamaño;
2. calcular el estadístico de interés;
3. repetir muchas veces;
4. estudiar la distribución de resultados.

**Diagrama:** `muestra original → muchas remuestras → muchos estadísticos → distribución bootstrap`.

*Cada remuestra reutiliza filas y puede omitir otras. La colección de estadísticas aproxima cómo cambiaría el resultado bajo el esquema de remuestreo elegido.*

Puede aplicarse a medianas o diferencias, pero debe respetar grupos, tiempo o dependencia cuando la estructura lo requiera.

---

# Ejemplo numérico: bootstrap de una mediana

Para la muestra original $[8,10,12,14]$, la mediana es $11$.

| Remuestra con reemplazo | Mediana |
|---|---:|
| $[8,8,12,14]$ | $10$ |
| $[10,10,12,14]$ | $11$ |
| $[8,12,14,14]$ | $13$ |
| $[8,10,10,12]$ | $10$ |

**Lectura:** las medianas cambian entre $10$ y $13$. Al repetir el remuestreo muchas veces, su distribución muestra cuán estable es la mediana observada.

**Aplicación:** el mismo procedimiento permite evaluar estadísticas cuya variabilidad es difícil de resumir con una fórmula simple.

---

# Precisión no es ausencia de sesgo

Un intervalo estrecho expresa poca variabilidad bajo un procedimiento; no demuestra que el procedimiento esté centrado en la cantidad correcta.

**Diagrama:** una distribución de estimaciones estrecha aparece desplazada respecto del parámetro verdadero.

*El ancho representa precisión y el desplazamiento representa sesgo. Más repeticiones del mismo mecanismo reducen el ancho, pero no corrigen el desplazamiento.*

**Advertencia crítica:** aumentar el tamaño de una muestra mal seleccionada puede aumentar la confianza aparente en una respuesta equivocada.

---

# Del análisis descriptivo al predictivo

| Dimensión | Descriptivo | Predictivo |
|---|---|---|
| Objetivo | resumir casos observados | estimar casos no observados |
| Referencia | archivo y periodo analizados | población y horizonte futuros |
| Validación | coherencia y cobertura | desempeño fuera del ajuste |
| Salida | tabla, gráfico o estadístico | valor, clase o probabilidad |

**Diagrama:** `datos históricos → patrón aprendido → caso nuevo → predicción`.

*El patrón se construye con el pasado y se aplica a una unidad no usada para producir esa predicción; la evaluación debe imitar ese uso.*

Una frecuencia histórica puede ser un baseline predictivo, pero no garantiza estabilidad ante cambios temporales o de selección.

---

# Del análisis predictivo al prescriptivo

Una predicción estima qué podría ocurrir. Una prescripción compara qué conviene hacer frente a esa incertidumbre.

**Diagrama:** `evidencia → probabilidad → acciones + consecuencias + restricciones → decisión`.

*La probabilidad resume creencias sobre estados; el bloque de decisión agrega valores y límites operativos para elegir una acción.*

Dos organizaciones pueden usar la misma probabilidad y elegir acciones distintas si enfrentan costos, capacidades o responsabilidades diferentes.

---

# Estados inciertos y acciones posibles

Una decisión se puede representar mediante:

- **estados:** condiciones que no conocemos al decidir;
- **acciones:** alternativas bajo control del decisor;
- **consecuencias:** resultados de combinar una acción con un estado;
- **información:** evidencia disponible antes de elegir.

|  | Detección | No detección |
|---|---|---|
| Revisar | detección atendida | revisión innecesaria |
| No revisar | omisión | recurso conservado |

*Las filas son acciones controlables y las columnas estados inciertos. Cada celda describe una consecuencia, no solo una etiqueta estadística.*

---

# Costos de aciertos y errores

Cuando decidimos revisar o no un sitio, el resultado puede ser acertado o equivocado. Revisar una muestra que efectivamente presenta detección es un acierto, pero revisar una muestra sin detección consume un recurso que pudo destinarse a otro caso. No revisar una muestra sin detección es otro acierto, mientras que no revisar una detección real implica una demora o una omisión con consecuencias posibles.

Los costos de estos resultados no son todos iguales. Pueden representar dinero, tiempo, riesgo, equidad y capacidad perdida para atender otros casos.

*Un falso positivo y un falso negativo pueden ocurrir con la misma frecuencia y aun así tener importancias muy distintas. Por eso conviene valorar cada error por separado y no tratarlos como equivalentes.*

---

# Matriz de decisión

Supongamos estos costos didácticos:

| Acción | Detección | No detección |
|---|---:|---:|
| Revisar | 2 | 2 |
| No revisar | 20 | 0 |

Revisar cuesta 2 unidades cualquiera sea el estado. No revisar cuesta 20 si existía una detección y 0 en caso contrario.

**Diagrama:** `probabilidad del estado × costo de cada celda → costo esperado por acción`.

*La multiplicación pondera cada consecuencia por cuán probable se considera; la suma permite comparar acciones en una unidad común.*

---

# Valor esperado de una acción

Para una acción $a$ y estados $s$:

$$
EC(a)=\sum_s P(s\mid E)C(a,s)
$$

Si $P(D\mid E)=0{,}15$:

$$
EC(\text{revisar})=2
$$

$$
EC(\text{no revisar})=0{,}15(20)+0{,}85(0)=3
$$

Con estos supuestos, revisar tiene menor costo esperado.

*El cálculo no predice qué ocurrirá en un caso concreto; compara consecuencias promedio bajo probabilidades y costos explícitos.*
