# Ejemplos de cómo completar el Contrato del análisis

**Material de apoyo** para el Trabajo práctico: exploración de dos variables (sección 5 de la consigna, "Contrato del análisis").

> **Cómo usar este documento:** acá abajo vas a encontrar tres ejemplos completos de cómo podría quedar la tabla del contrato, cada uno con un par distinto (uno por cada vista: H, ZH y T). La idea **no** es que copies estas respuestas ni que uses estos mismos pares si te tocó otro: la idea es que veas el *nivel de detalle y el tono* que se espera en cada campo, para que sepas qué es "una buena respuesta" cuando completes la tuya. Cambiá lo que corresponda según el par que elegiste y según lo que efectivamente encuentres al ejecutar tu notebook (por ejemplo, los tamaños de muestra son inventados acá a modo de ilustración; los tuyos van a salir de tu propio código).

---

## Ejemplo 1 — Par numérica-numérica con vista H (PC-01: `pickups` y `temperatura_c`)

| Campo | Respuesta de ejemplo |
|---|---|
| Código y par elegido | PC-01 — `pickups` y `temperatura_c` |
| Pregunta exploratoria | ¿Cómo varían los pickups totales por hora junto con la temperatura registrada durante enero de 2024? |
| Significado de la primera columna | `pickups`: cantidad total de recogidas de Yellow Taxi que arrancaron durante esa hora, sumadas entre todas las zonas activas. No es la demanda total de viajes de la ciudad, sino los viajes que efectivamente se realizaron, se reportaron y pasaron los filtros de calidad del notebook. |
| Significado de la segunda columna | `temperatura_c`: temperatura del aire medida por la estación meteorológica NOAA `USW00094728`, en grados Celsius, resumida a un solo valor por hora (promedio de los reportes subhorarios de esa hora). |
| Tipo semántico de cada columna | `pickups` es numérica discreta de conteo (siempre entera y ≥ 0). `temperatura_c` es numérica continua. |
| Unidad analítica y vista | Vista H (horaria): cada fila representa una hora de enero, ya reducida a una sola observación por hora. |
| Periodo y zona horaria | Enero de 2024 completo, intervalo `[2024-01-01, 2024-02-01)`, zona horaria `America/New_York`. |
| Población registrada | Todas las horas de enero de 2024 en las que hubo al menos un pickup válido en alguna zona (porque `producto` solo contiene zonas con actividad); las horas sin ningún pickup registrado no forman parte de esta tabla y no deben confundirse con "cero pickups". |
| Denominador o tamaño válido | Sobre 744 horas posibles en enero, se usan las que tienen temperatura no faltante (por ejemplo: N = 738 horas válidas, 6 horas con clima faltante se excluyen de los estadísticos que lo requieran). *(Este número hay que sacarlo del propio notebook, acá es solo un ejemplo.)* |
| Afirmaciones que los datos no permiten | No se puede afirmar que la temperatura "cause" cambios en los pickups (correlación no implica causalidad). Tampoco se puede estimar la demanda total de transporte de la ciudad: solo se observan los viajes de Yellow Taxi efectivamente registrados. |

---

## Ejemplo 2 — Par categórica-numérica con vista ZH (GT-01: `pickup_borough` y `pickups`)

| Campo | Respuesta de ejemplo |
|---|---|
| Código y par elegido | GT-01 — `pickup_borough` y `pickups` |
| Pregunta exploratoria | ¿Cómo se distribuyen los pickups de enero de 2024 entre los distintos boroughs, considerando solo las zona-horas que tuvieron al menos un pickup? |
| Significado de la primera columna | `pickup_borough`: el borough (Manhattan, Brooklyn, Queens, Bronx, Staten Island o EWR) al que pertenece la zona de origen de los pickups de esa fila. |
| Significado de la segunda columna | `pickups`: cantidad de recogidas registradas en esa zona-hora puntual. |
| Tipo semántico de cada columna | `pickup_borough` es categórica nominal (no tiene un orden natural). `pickups` es numérica discreta de conteo. |
| Unidad analítica y vista | Vista ZH (zona-hora activa): cada fila es una combinación de zona y hora que tuvo al menos un pickup registrado. |
| Periodo y zona horaria | Enero de 2024 completo, zona horaria `America/New_York`. |
| Población registrada | Todas las zona-horas activas de enero de 2024 (es decir, con al menos un pickup); no incluye combinaciones de zona y hora sin actividad, porque esas simplemente no aparecen como fila. |
| Denominador o tamaño válido | Total de zona-horas activas en el producto (por ejemplo, N = 41.200 filas), y además el tamaño de cada grupo por separado (cuántas zona-horas activas tiene cada borough), porque eso afecta cómo se interpretan las comparaciones. *(Números de ejemplo; los reales salen del notebook.)* |
| Afirmaciones que los datos no permiten | No se puede decir que un borough "tiene más demanda de taxis" en términos absolutos: solo se sabe que tiene más pickups entre las zona-horas activas. Como no existe una grilla completa de zonas y horas, un borough con más zonas geográficas puede tener más zona-horas activas por ese motivo estructural, y no necesariamente porque haya más actividad por zona. |

---

## Ejemplo 3 — Par temporal-numérica con vista T (GT-02: `pickup_hora` y `temperatura_c`)

| Campo | Respuesta de ejemplo |
|---|---|
| Código y par elegido | GT-02 — `pickup_hora` y `temperatura_c` |
| Pregunta exploratoria | ¿Cómo evoluciona la temperatura registrada, hora a hora, a lo largo de enero de 2024, y qué ciclos diarios se observan? |
| Significado de la primera columna | `pickup_hora`: marca temporal que identifica el inicio de cada hora local analizada. Acá no se usa como una variable numérica cualquiera, sino como el eje ordenado en el tiempo. |
| Significado de la segunda columna | `temperatura_c`: temperatura horaria resumida a partir de los reportes de la estación NOAA, en grados Celsius. |
| Tipo semántico de cada columna | `pickup_hora` es temporal (fecha y hora). `temperatura_c` es numérica continua. |
| Unidad analítica y vista | Vista T (temporal horaria): una fila por hora, ordenadas cronológicamente, sin agrupar por zona. |
| Periodo y zona horaria | Enero de 2024 completo, zona horaria `America/New_York`. |
| Población registrada | Todas las horas de enero de 2024 para las que existe un dato climático (puede haber huecos si la estación NOAA no reportó en alguna hora puntual). |
| Denominador o tamaño válido | Horas con temperatura no faltante sobre el total de horas del mes (por ejemplo, N = 738 de 744 horas posibles). *(Ejemplo ilustrativo; el número real depende de tu ejecución.)* |
| Afirmaciones que los datos no permiten | No corresponde calcular una correlación entre el timestamp convertido a número y la temperatura: esa cifra no tendría una interpretación clara. Tampoco se puede generalizar el patrón observado en enero a otros meses del año sin analizar datos adicionales de esos meses. |

---

## Puntos en común que valen para cualquier par

Más allá del ejemplo puntual, hay algunas cosas que se repiten en los tres casos y que conviene tener presentes al completar tu propio contrato:

- La **pregunta exploratoria** siempre nombra las dos columnas concretas y el periodo, y evita palabras que sugieran causalidad ("afecta", "explica", "provoca").
- El **significado de cada columna** se explica en términos que cualquier compañero entendería, sin asumir que ya sabe de qué se trata el dataset.
- El **tipo semántico** distingue claramente entre numérica (discreta o continua), categórica (nominal u ordinal) y temporal — no alcanza con decir "es un número" o "es texto".
- La **unidad analítica y vista** siempre se nombra explícitamente (H, ZH o T) y se explica en una frase qué representa cada fila.
- El **periodo y la zona horaria** se repiten siempre igual (enero de 2024, `America/New_York`), salvo que estés haciendo la actividad extra de seis meses.
- La **población registrada** aclara qué “universo” de datos estás mirando y qué queda afuera (por ejemplo, horas sin pickups, o zona-horas inactivas).
- El **denominador o tamaño válido** siempre es un número concreto que sale de tu propio notebook, nunca una estimación a ojo.
- Las **afirmaciones que los datos no permiten** son específicas del par: no es un párrafo genérico sobre "correlación no es causalidad" copiado y pegado, sino una explicación de qué conclusión puntual sería un error para *ese* par de columnas.
