---
title: "Ingeniería de características"
subtitle: "De datos brutos a representaciones útiles"
author: "Curso de Inteligencia Artificial"
course: "Inteligencia Artificial"
week: 6
class: 6
lang: es
---

# Ingeniería de características

## De datos brutos a representaciones útiles

**Semana 6 · Clase 6**

**Recorrido conceptual:** `dato bruto → característica → pipeline → modelo`.

El modelo solo puede aprender diferencias que su representación vuelve visibles.

---

# La representación define qué puede aprenderse

Una **característica** o **atributo** es una magnitud utilizada como entrada de un modelo.

| Dato disponible | Representación posible | Supuesto incorporado |
|---|---|---|
| fecha y hora | hora, día, feriado | existe un patrón de calendario |
| lluvia acumulada | valor, nivel o indicador | importa la magnitud o un umbral |
| ubicación | zona, distancia o conectividad | la cercanía relevante está bien definida |

Una característica útil tiene significado, está disponible al predecir, se calcula igual durante entrenamiento e inferencia y mantiene estabilidad operativa.

---

# Características numéricas

| Operación | Uso | Riesgo |
|---|---|---|
| Estandarizar | comparar escalas | aprender media y dispersión con todos los datos |
| Logaritmo | representar cambios relativos | aplicarlo a ceros o negativos |
| Razón | normalizar por exposición | denominadores pequeños o nulos |
| Recorte | limitar extremos | ocultar eventos reales |

**Ejemplo:** si una zona registra 120 viajes con capacidad 150,

$$
\text{presión}=120/150=0{,}80.
$$

La razón facilita comparar zonas de tamaños distintos, pero necesita una regla para capacidad cero.

---

# Características categóricas

- Una categoría nominal no tiene distancia ni orden intrínsecos.
- Codificar `norte`, `centro`, `sur` como 1, 2, 3 crea una geometría artificial.
- La codificación indicadora crea una columna binaria por nivel.
- Las categorías ordinales admiten orden, pero no necesariamente intervalos iguales.
- Los niveles raros y desconocidos necesitan una política explícita.

---

# Categoría desconocida: ejemplo y cuidados

El modelo se entrenó con `zona ∈ {norte, centro, sur}` y durante el uso aparece `oeste`.

**Tratamiento riesgoso:** un pipeline configurado para sustituir valores no reconocidos por la categoría más frecuente podría codificar `oeste` como `norte`. Esta sustitución evita un error técnico, pero no existe evidencia de que ambas zonas se comporten igual y se oculta una posible diferencia entre entrenamiento y uso.

**Cuidados necesarios:**

- distinguir una categoría nueva de un dato faltante;
- comprobar si se debe a un error de escritura, una fuente nueva o una ampliación de la población;
- representarla como `desconocida` u `otra` mediante un codificador preparado para niveles no vistos;
- registrar su frecuencia y revisar el desempeño del modelo en esos casos;
- actualizar y reevaluar el modelo si la categoría se vuelve habitual.

---

# Tiempo y espacio

Para una posición temporal $t$ dentro de un periodo $P$:

$$
x_{\sin}=\sin(2\pi t/P),\qquad x_{\cos}=\cos(2\pi t/P).
$$

El par conserva que las 23:00 y las 00:00 son horas cercanas. Los rezagos y medias móviles deben usar únicamente valores anteriores al instante de predicción.

En espacio pueden utilizarse distancias, pertenencia a zonas, accesibilidad o conectividad. La distancia geométrica no siempre representa tiempo de viaje ni transferencia del fenómeno.

---

# Interacciones y conocimiento del dominio

Una interacción representa que el efecto de una variable depende de otra:

$$
f(x)=\beta_0+\beta_1x_1+\beta_2x_2+\beta_{12}x_1x_2.
$$

**Ejemplo:** `lluvia × hora pico` puede representar que la lluvia afecta más la circulación cuando la red está congestionada.

- Priorizar combinaciones con una explicación operativa.
- Verificar que existan suficientes observaciones de la combinación.
- Comparar su aporte fuera de muestra.

Con 100 variables existen 4950 interacciones por pares: generar todas aumenta capacidad y riesgo de sobreajuste.

---

# Selección de atributos

Seleccionar atributos conserva un subconjunto de las variables disponibles.

| Familia | Estrategia | Limitación principal |
|---|---|---|
| Filtro | puntuar antes del modelo final | puede ignorar interacciones |
| Envolvente | comparar subconjuntos con el modelo | costo y sobreajuste de la búsqueda |
| Embebida | seleccionar durante el ajuste | depende del modelo y la escala |

Relevancia no equivale a causalidad. Dos variables correlacionadas pueden sustituirse y cambiar de posición entre muestras.

**Regla:** cualquier selección basada en datos se ajusta dentro de cada fold.

---

# Métodos de filtro

Los filtros puntúan atributos sin entrenar repetidamente el modelo final.

| Criterio | Qué busca | Ejemplo |
|---|---|---|
| Varianza | columnas constantes o casi constantes | retirar un sensor que siempre informa `1` |
| Asociación | correlación lineal, relación monótona o asociación categórica con $y$ | ordenar velocidad según su asociación con bloqueo |
| Información mutua | dependencia lineal o no lineal con $y$ | detectar señal aportada por lluvia |

**Ejemplo ilustrativo:** información mutua con bloqueo: `velocidad = 0,31`, `lluvia = 0,18`, `hora = 0,05`, `identificador = 0,01`. Un selector `top-2` conservaría velocidad y lluvia.

**Cuidados:** el número de atributos se valida; un filtro univariado puede perder interacciones y todo filtro que usa $y$ se ajusta dentro de cada fold.

---

# Métodos envolventes

Evalúan subconjuntos entrenando el modelo que finalmente se utilizará.

| Método | Procedimiento |
|---|---|
| Selección hacia adelante | comienza sin atributos y agrega el que más mejora validación |
| Eliminación hacia atrás | comienza con todos y retira el menos útil |
| RFE | ajusta, ordena, elimina los menos importantes y repite |

**Ejemplo:** con selección hacia adelante, `velocidad` obtiene $F_1=0,71$; al agregar `lluvia`, $F_1=0,78$; agregar `hora` mantiene $F_1=0,78$. Si la regla exige una mejora mínima de 0,01, se conservan dos atributos.

**Cuidados:** son costosos, no garantizan el mejor subconjunto y pueden sobreajustar la validación después de probar muchas alternativas. La búsqueda se realiza en el ciclo interno de validación.

---

# Métodos embebidos

La selección ocurre durante el ajuste del modelo.

| Método | Mecanismo | Ejemplo de selección |
|---|---|---|
| Lasso o L1 | produce algunos coeficientes exactamente iguales a cero | descarta entradas con coeficiente cero |
| Elastic Net | combina L1 y L2 | estabiliza grupos correlacionados |
| Árbol | utiliza atributos para construir divisiones | conserva variables presentes en ramas válidas |

**Ejemplo ilustrativo:** después de estandarizar, una regresión logística con L1 produce `velocidad = -1,20`, `lluvia = 0,70`, `hora = 0` e `identificador = 0`. Bajo la regla definida, conserva velocidad y lluvia.

**Cuidados:** la penalización y la escala se ajustan dentro de cada fold. Variables correlacionadas pueden sustituirse de forma inestable y un cero no demuestra irrelevancia causal.

---

# Reducción dimensional y PCA

La selección conserva columnas originales; la reducción construye nuevas coordenadas $Z=g(X)$ con $q<p$.

En PCA, los componentes son direcciones ortogonales ordenadas por varianza. Si los autovalores son $(4{,}2;2{,}1;0{,}7)$:

$$
\mathrm{PVE}_1=4{,}2/7=60\%,\qquad
\mathrm{PVE}_{1:2}=6{,}3/7=90\%.
$$

Conservar 90 % de la varianza no garantiza conservar 90 % de la capacidad predictiva. Una señal rara puede encontrarse en una dirección de baja varianza.

---

# El pipeline completo es la unidad evaluada

**Flujo:** `datos → imputación → codificación → escala → selección o PCA → modelo`.

En cada partición:

1. ajustar transformaciones únicamente con entrenamiento;
2. aplicar esos parámetros a validación;
3. ajustar el modelo con la representación transformada;
4. medir sobre los casos reservados.

En inferencia se reutilizan medias, categorías, columnas seleccionadas y componentes aprendidos; no se vuelven a ajustar.

---

# Caso integrado: anticipar un bloqueo

Un vehículo debe estimar, antes de ingresar, si un tramo quedará bloqueado en los próximos 15 minutos.

| Datos brutos | Características candidatas | Control necesario |
|---|---|---|
| fecha y hora | seno/coseno de hora; día hábil | calendario disponible |
| lluvia reciente | acumulado causal; indicador intenso | corte en el instante de decisión |
| velocidades previas | media y tendencia anteriores | excluir mediciones futuras |
| tramo y red | tipo de vía; centralidad; desvío | política para tramos nuevos |

**Actividad:** proponer una interacción útil, una variable que causaría fuga y una prueba para detectar una diferencia entre entrenamiento e inferencia.
