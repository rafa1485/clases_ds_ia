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

**Control:** una categoría nueva puede indicar cambio de población; reemplazarla silenciosamente por la más frecuente oculta ese cambio.

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
