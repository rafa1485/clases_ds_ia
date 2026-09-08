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

> **Cómo leer esta consigna:** los recuadros como este (con fondo gris y borde amarillo) son notas aclaratorias. Explican en palabras simples una idea técnica antes de que la necesites usar. No son parte de lo que hay que entregar; están para ayudarte a entender el "por qué" detrás de cada pedido.

## Propósito

Vas a trabajar con un **par de columnas que vos mismo elijas** de la lista de pares preaprobados (sección 3), tomado de la tabla `producto` que armaste en el notebook de la clase 2. Antes de arrancar con el análisis, dejá registrado por escrito en el notebook cuál es el par que elegiste: así queda claro tu compromiso con esa elección desde el principio, y no hay lugar para ir cambiando de par sobre la marcha según te convenga el resultado. La idea es avanzar en dos etapas: primero conocer cada variable por separado (¿qué significa, cómo se distribuye, tiene datos faltantes?) y recién después mirar cómo se relacionan entre sí.

> **Nota:** "explorar" en ciencia de datos significa describir los datos tal como son —sus valores típicos, sus casos raros, sus huecos— antes de sacar conclusiones. Es un paso previo a cualquier modelo o afirmación fuerte, y muchas veces revela problemas (errores de carga, columnas mal definidas, datos faltantes) que conviene detectar temprano.

Un punto central de este trabajo: encontrar que dos variables se mueven juntas (una **asociación** o **correlación**) no significa que una sea la causa de la otra (una **relación causal**). Por ejemplo, que haya más pickups de taxi cuando hace más calor no prueba que el calor "cause" los viajes; puede haber otros factores compartidos (día de la semana, hora pico, eventos). Este trabajo pide que documentes lo que los datos permiten decir, ni más ni menos.

El informe final debe responder tres preguntas:

1. ¿Cómo varía cada columna durante el periodo estudiado?
2. ¿Qué valores faltantes, ceros, extremos o casos potencialmente anómalos aparecen?
3. ¿Qué relación se observa entre las dos columnas y bajo qué límites puede sostenerse?

> El objetivo no es encontrar una correlación alta ni confirmar una historia previa que ya tenías en mente. El objetivo es construir una descripción trazable (es decir, que cualquiera pueda reproducir con tu código), revisar explicaciones alternativas antes de quedarte con la primera que se te ocurra, y comunicar con honestidad qué permiten afirmar los registros y qué no.

## 1. Preparación del trabajo

Antes de tocar las variables que elijas, dejá el notebook base andando de punta a punta:

1. Crear una copia personal de `Taller_Clase_02_Movilidad.ipynb` (no trabajes sobre el original de la clase).
2. Buscá en el notebook la variable `MODO_CLASE` y cambiala a `MODO_CLASE = False`. Pensala como un interruptor: en `True` (como estaba durante la clase) el notebook recorta el análisis a la primera semana de enero (del 1 al 7, hasta el 8 de enero sin incluir). Ojo: no es una muestra aleatoria de filas, sino un recorte determinista de fechas —siempre la misma semana—, pensado para conservar horas consecutivas y que la clase corra más rápido. En `False`, esa misma lógica se aplica sobre el mes completo, que es justo lo que este trabajo necesita. Si te olvidás de cambiarlo, vas a terminar analizando solo esa primera semana y no el mes entero, sin darte cuenta, y todos tus resultados van a estar armados sobre datos incompletos.
3. Ejecutar todas las celdas en orden hasta construir la tabla `producto`. Si salteás celdas o las corrés en otro orden, corrés el riesgo de trabajar con una tabla inconsistente.
4. Confirmar que el periodo sea `[2024-01-01, 2024-02-01)` en la zona `America/New_York`. La notación `[...)` significa que el 1° de enero a las 00:00 está incluido y el 1° de febrero a las 00:00 ya no; es un intervalo "cerrado a la izquierda, abierto a la derecha", muy usado para evitar contar dos veces el instante límite.
5. Agregar al final del notebook una sección titulada `Trabajo práctico: exploración de dos variables`, para que quede claro dónde empieza tu trabajo propio.
6. Antes de ejecutar cualquier análisis, escribí en el notebook cuál es el par de columnas que elegiste (de la lista de la sección 3) y qué vista analítica te corresponde usar (ver sección 2). Puede parecer un trámite, pero cumple una función concreta: si dejás esto anotado *antes* de ver ningún resultado, evitás la tentación —muchas veces inconsciente— de cambiar de par, de vista o de enfoque más adelante solo porque te terminó dando un resultado más prolijo o más interesante. Es la misma lógica que usan los estudios serios: primero se define el plan, después se mira qué pasa, y no al revés.
7. No cambies "por izquierda" (es decir, sin avisar) el periodo de tiempo, las fuentes de datos ni las reglas de calidad que ya vienen definidas en el notebook base: son parte del diseño del trabajo y garantizan que todos estén analizando lo mismo, bajo las mismas condiciones. Si en algún momento necesitás modificar alguno de esos elementos (por ejemplo, porque encontraste un error real), no lo hagas en silencio: agregá una celda de texto explicando qué cambiaste y por qué. Así, cualquiera que lea tu notebook —incluido el docente— puede entender la decisión sin tener que adivinarla.

La tabla `producto` representa una **zona de origen con al menos un pickup registrado durante una hora local**. Su clave (la combinación de columnas que identifica una fila de forma única) es `pickup_hora` junto con `PULocationID`. Importante: los registros TLC representan viajes en Yellow Taxi que efectivamente se realizaron y se reportaron, y que además pasaron los filtros de calidad. No representan la demanda total de viajes ni las solicitudes que no fueron atendidas (por ejemplo, alguien que pidió un taxi y no consiguió uno no aparece acá).

## 2. Vistas analíticas obligatorias

> **Nota:** una "vista" define cuál es la unidad de análisis, es decir, qué representa cada fila cuando hacés el análisis. No todos los pares de columnas se pueden estudiar directamente sobre las filas de `producto` tal como están; según el par, hay que reagrupar los datos de una manera específica.

Cada par de columnas se entrega junto con la vista que le corresponde:

| Código | Vista | Unidad analítica | Uso |
|---|---|---|---|
| H | Horaria | una hora de enero | pares que incluyen clima o pickups totales |
| ZH | Zona-hora activa | una zona-hora con al menos un pickup | comparación de pickups entre boroughs |
| T | Temporal horaria | una hora ordenada cronológicamente | evolución temporal de una medida |

### Vista H: una fila por hora

Las variables de clima (NOAA) vienen de una sola estación meteorológica y por eso su valor se repite en todas las zonas activas de una misma hora: si a las 14:00 hubo 10 zonas con pickups, las 10 tienen la misma temperatura registrada. Antes de analizar un par que incluya clima, hay que volver a una fila por hora para no contar ese mismo valor climático varias veces. Concretamente:

- sumar `pickups`, porque cada zona sí aporta viajes distintos (esto no se repite, se suma);
- conservar una sola observación de cada variable NOAA (temperatura, humedad, etc.), ya que están repetidas;
- comprobar que cada variable NOAA tenga como máximo un valor distinto por hora entre las zonas (si aparece más de uno, hay un problema que investigar antes de seguir);
- mantener las horas sin clima como faltantes (`NaN`), no convertirlas automáticamente en cero. Un dato faltante y un cero no son lo mismo: cero grados es una medición real, mientras que un faltante es "no sabemos".

La operación esperada sigue esta estructura, que debe completarse y verificarse en el notebook:

```python
por_hora = producto.groupby("pickup_hora", as_index=False).agg(
    pickups=("pickups", "sum"),
    temperatura_c=("temperatura_c", "first"),
    humedad_relativa=("humedad_relativa", "first"),
    viento=("viento", "first"),
    visibilidad=("visibilidad", "first"),
)
```

Notá que `precipitacion_mm` no aparece en esta agregación: como se explica en la sección 3, esa columna queda descartada del trabajo, así que no hace falta arrastrarla en ningún resumen.

Usar `"first"` (quedarse con el primer valor de cada grupo) solo tiene sentido después de comprobar que todos los valores del grupo son iguales entre sí. Si simplemente eliminás filas duplicadas sin verificar esto, no estás demostrando que la simplificación sea correcta.

### Vista ZH: zona-hora activa

El producto del notebook no contiene una grilla completa con todas las combinaciones posibles de zona y hora (por ejemplo, si una zona no tuvo ningún pickup en una hora dada, simplemente no aparece una fila para esa combinación). Por eso, una comparación geográfica entre boroughs debe formularse con cuidado, como:

> Distribución de pickups entre las zona-horas que tuvieron al menos un pickup registrado durante enero de 2024.

Es decir: la ausencia de una fila **no** se puede convertir automáticamente en `pickups = 0`, porque no sabemos si esa combinación tuvo cero pickups o si directamente no está en los datos por otro motivo. Si decidís construir una grilla completa (con todas las combinaciones posibles), vas a tener que justificar qué marco esperabas y documentar esa transformación aparte.

### Vista T: serie temporal

Acá la columna `pickup_hora` se usa como eje ordenado en el tiempo, no como un número cualquiera. No corresponde convertir el timestamp a un número (como los segundos desde una fecha de referencia) y calcular una correlación convencional con él: eso no tiene una interpretación clara. En cambio, hay que estudiar el orden temporal, los ciclos (por ejemplo, patrones que se repiten cada 24 horas o cada semana), los huecos, los cambios de nivel y el efecto del calendario (días de semana vs. fines de semana, feriados, etc.).

## 3. Pares preaprobados

Elegí libremente uno de los siguientes pares de columnas preaprobados: la selección queda en tus manos, no te lo asigna el docente. Un mismo par puede ser elegido por más de un estudiante, así que no hay problema si coincide con el de un compañero. Eso sí: una vez que decidas cuál vas a trabajar, registralo por escrito en el notebook (punto 6 de la sección 1, y contrato del análisis en la sección 5) antes de empezar a explorar los datos, y sostené esa elección durante todo el trabajo.

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
| GT-02 | `pickup_hora` | `temperatura_c` | T |
| GT-03 | `pickup_hora` | `humedad_relativa` | T |
| GT-04 | `pickup_hora` | `viento` | T |
| GT-05 | `pickup_hora` | `visibilidad` | T |

### Precipitación: columna descartada

`precipitacion_mm` **no** forma parte de ningún par preaprobado y no debe usarse en ningún análisis de este trabajo. No es una restricción temporal a la espera de una futura auditoría: la columna queda directamente descartada. El motivo puntual está detallado en la sección 4, junto con el resto de los usos que no deben hacerse.

## 4. Pares que no deben utilizarse

La siguiente tabla lista combinaciones que **no** tienen sentido analizar de la forma habitual, junto con el motivo. Vale la pena leerla entera, porque entender por qué algo está mal ayuda a no repetir el error en otros contextos:

| Par o uso | Motivo |
|---|---|
| `pickup_hora` con `hora` | son claves temporales redundantes (dicen básicamente lo mismo); además, `hora` también refleja si la unión (`merge`) con otra tabla salió bien o mal |
| `PULocationID` con una numérica mediante correlación | `PULocationID` es un identificador (como un número de DNI de la zona), no una magnitud; calcular una correlación con un ID no tiene interpretación |
| `PULocationID` con `pickup_zone` o `pickup_borough` | es una relación de catálogo (el ID simplemente nombra a la zona), no una asociación que se pueda "descubrir" en los datos |
| `pickup_zone` con `pickup_borough` | es una relación jerárquica casi determinista: cada zona pertenece a un solo borough por definición, no es algo que los datos "revelen" |
| clima con zona o borough sobre `producto` | como vimos en la vista H, el dato de NOAA no varía espacialmente dentro de una hora; el mismo valor horario está repetido en todas las zonas, así que "cruzarlo" con la zona no aporta información nueva |
| dos variables NOAA directamente sobre `producto` | produce **pseudorreplicación** por zona activa: como el mismo valor climático se repite en varias filas (una por cada zona activa esa hora), parecería que tenés muchas más observaciones independientes de las que realmente tenés |
| `observaciones` como intensidad climática | esa columna cuenta cuántos reportes de NOAA hubo, no representa una magnitud meteorológica (como milímetros de lluvia o grados de temperatura) |
| `precipitacion_mm` con cualquier otra columna | el notebook base arma esta columna sumando los reportes subhorarios de GHCNh para obtener el total de cada hora, pero nunca audita si esos reportes cubren periodos que se superponen entre sí ni revisa sus banderas de calidad; el propio notebook deja esto anotado como un límite sin resolver, así que el total horario de lluvia no está validado y puede estar duplicando milímetros |

<div class="page-break"></div>

## 5. Contrato del análisis

> **Nota:** completar esta tabla antes de calcular nada te obliga a definir con precisión qué vas a medir, sobre qué población y con qué alcance. Es una forma de comprometerte con un plan antes de ver los resultados, para no terminar "acomodando" el análisis a lo que más te convenga después.

Antes de calcular estadísticas, completar:

| Campo | Respuesta del estudiante |
|---|---|
| Código y par elegido | |
| Pregunta exploratoria | |
| Significado de la primera columna | |
| Significado de la segunda columna | |
| Tipo semántico de cada columna | |
| Unidad analítica y vista | |
| Periodo y zona horaria | |
| Población registrada | |
| Denominador o tamaño válido | |
| Afirmaciones que los datos no permiten | |

La pregunta exploratoria debe nombrar las variables concretas y su alcance. Por ejemplo, evitá preguntar "¿cómo afecta el clima a la demanda?": TLC no mide la demanda total (solo los viajes que efectivamente se hicieron) y el diseño del estudio no permite identificar efectos causales. Una pregunta mejor sería, por ejemplo, "¿cómo varían los pickups por hora junto con la temperatura registrada durante enero de 2024?".

## 6. Exploración individual de cada columna

> **Nota:** a este proceso de mirar los datos con atención antes de modelarlos se lo llama EDA, por sus siglas en inglés (*Exploratory Data Analysis*, análisis exploratorio de datos).

Realizar primero el EDA completo de la columna 1 y luego repetirlo para la columna 2. No arranques por el coeficiente de correlación: primero hay que entender cada variable por separado.

### 6.1. Comprensión y cobertura

Para cada columna:

1. Explicar qué representa y en qué unidad está expresada (por ejemplo, "temperatura en grados Celsius").
2. Mostrar su tipo de dato físico (cómo está guardada: entero, decimal, texto, fecha) y su tipo semántico (qué significa en realidad: por ejemplo, un código de zona puede estar guardado como número pero funcionar como categoría).
3. Informar filas totales, valores válidos y faltantes.
4. Contar valores únicos cuando corresponda (útil sobre todo para columnas categóricas).
5. Distinguir entre cero, faltante y ausencia de fila: son tres cosas distintas y confundirlas lleva a conclusiones erróneas.
6. Revisar valores mínimos y máximos contra el dominio esperado de la variable (por ejemplo, una humedad relativa no debería superar el 100%).
7. Declarar si la variable fue agregada (resumida a partir de otras filas) y mediante qué operación (suma, promedio, "first", etc.).

### 6.2. Distribución

Para una variable **numérica**, incluir cuando sean interpretables:

- mínimo y máximo;
- media (el promedio) y mediana (el valor central, que deja la mitad de los datos por debajo y la mitad por arriba; es más resistente a valores extremos que la media);
- cuartiles e IQR (los cuartiles dividen los datos ordenados en cuatro partes iguales; el IQR o rango intercuartílico es la distancia entre el primer cuartil Q1 y el tercero Q3, y mide qué tan dispersa está la parte "central" de los datos);
- desviación estándar (otra medida de dispersión, más sensible a valores extremos que el IQR);
- proporción de ceros;
- histograma con resolución justificada (explicá por qué elegiste ese ancho de barra y no otro);
- caja (boxplot) o violín como vista complementaria.

Para una variable **categórica**, incluir:

- frecuencia absoluta y relativa (cuántas veces aparece cada categoría, en cantidad y en porcentaje);
- faltantes y categorías poco frecuentes;
- tamaño de cada grupo;
- barras ordenadas (por frecuencia, por ejemplo) o una tabla legible.

Para una variable **temporal**, incluir:

- cobertura desde la primera hasta la última hora;
- horas esperadas versus horas observadas (¿faltan horas en el medio?);
- huecos (periodos sin datos);
- evolución y ciclos por hora del día o día de semana.

Cada gráfico debe incluir título, ejes con su unidad, el periodo que representa y una frase que explique qué comparación facilita ese gráfico en particular. No alcanza con "mostrar el gráfico"; hay que decir qué se puede leer en él.

## 7. Casos potencialmente anómalos

> **Nota:** un valor "anómalo" (outlier) no es automáticamente un error. Puede ser un dato real pero inusual (por ejemplo, una hora con muchísimos pickups por un evento especial). Por eso hablamos de "casos potencialmente anómalos": son candidatos a revisar, no errores confirmados de antemano.

Una regla estadística genera candidatos para revisión, no errores confirmados. Para una variable numérica se puede utilizar la regla de Tukey, que marca como candidato a todo valor fuera de este rango:

<p class="formula">[Q<sub>1</sub> - 1.5 IQR, Q<sub>3</sub> + 1.5 IQR]</p>

Es decir: se toma el primer cuartil (Q1) menos 1.5 veces el IQR como límite inferior, y el tercer cuartil (Q3) más 1.5 veces el IQR como límite superior. Todo lo que caiga fuera de ese rango queda señalado para revisar.

El estudiante deberá:

1. declarar la regla utilizada;
2. contar los casos señalados;
3. mostrar una tabla con valor, fecha, hora y contexto disponible para cada caso señalado;
4. comprobar si el valor viola el dominio de la variable (por ejemplo, una humedad negativa, que sería imposible) o si simplemente es un valor extremo pero válido;
5. proponer explicaciones alternativas para cada caso llamativo;
6. conservarlo, excluirlo o corregirlo, pero siempre con una justificación trazable (que quede documentada en el notebook, no solo en tu cabeza);
7. comparar al menos un resumen estadístico con y sin esos casos, para ver cuánto cambia el resultado.

Para una variable como la humedad relativa, un cero sería un valor sospechoso (rara vez el aire está completamente seco), mientras que para otras magnitudes un cero es perfectamente válido y no un dato faltante: conviene pensarlo caso por caso, según el dominio de cada variable. Para pickups, una hora o zona con un valor extremo puede reflejar un aeropuerto, un evento puntual, un efecto de calendario, cambios en la oferta de taxis, un error de agregación, u otra condición que no está directamente en los datos. Explorar estas posibilidades antes de descartar el dato es parte del ejercicio.

## 8. Relación entre las columnas

### 8.1. Dos variables numéricas

1. Construir un diagrama de dispersión (scatter plot).
2. Examinar dirección (¿sube o baja una cuando sube la otra?), forma, curvatura, posibles grupos o agrupamientos, puntos que se superponen y puntos influyentes (los que, si se sacaran, cambiarían mucho el resultado).
3. Calcular el coeficiente de correlación de **Pearson** solo si te interesa específicamente la relación **lineal** entre las variables.
4. Calcular el coeficiente de **Spearman** si te interesa una relación **monotónica** (que crece o decrece de forma consistente, aunque no en línea recta) o si la forma de los datos y la presencia de valores extremos desaconsejan quedarte solo con Pearson. A diferencia de Pearson, Spearman trabaja con el orden (ranking) de los valores, lo que lo hace menos sensible a valores extremos.
5. Comparar los resultados con y sin los casos señalados en la sección 7, sin eliminar observaciones de forma automática ni sin justificar.

### 8.2. Una variable categórica y una numérica

1. Informar tamaño y cobertura de cada grupo (categoría).
2. Comparar mediana, IQR y, cuando corresponda, media y desviación estándar entre grupos.
3. Utilizar cajas (boxplots), violines o gráficos de puntos, todos con una escala común para poder comparar entre grupos.
4. Evitar interpretar una diferencia descriptiva entre grupos como si fuera un efecto causal del grupo sobre la variable numérica.

### 8.3. Una variable temporal y una numérica

1. Ordenar cronológicamente.
2. Representar la serie temporal sin "rellenar" artificialmente los huecos (si falta un dato, que se vea el hueco, no una línea que lo disimule).
3. Examinar ciclos por hora del día y por día de la semana.
4. Señalar cambios de nivel, valores extremos y periodos sin cobertura.
5. No correlacionar directamente el timestamp (convertido a número) con la medida; en su lugar, describí el comportamiento a lo largo del tiempo.

### 8.4. Dependencia y explicaciones alternativas

> **Nota:** muchos métodos estadísticos asumen que las observaciones son independientes entre sí. Acá eso no se cumple del todo, y es importante que lo tengas presente al interpretar tus resultados.

Las horas consecutivas no son observaciones independientes entre sí (lo que pasa a las 14:00 está relacionado con lo que pasa a las 15:00). En la vista ZH, una misma zona aporta mediciones repetidas a lo largo del mes, y todas las zonas activas en una misma hora comparten las mismas condiciones temporales (por ejemplo, todas están en hora pico o no). Por eso, el número de zona-horas **no** debe interpretarse como si fuera la cantidad de réplicas independientes que tenés. Las relaciones que observes pueden estar asociadas con la hora pico, el día de la semana, feriados, aeropuertos, eventos puntuales, la disponibilidad de taxis, la cobertura de los datos, o tendencias compartidas que no estás midiendo directamente.

Si tu par incluye una variable NOAA, recordá que todas esas variables vienen de una sola estación meteorológica. Reducir los datos a una fila por hora (como se explicó en la vista H) corrige la repetición artificial entre zonas, pero no elimina la dependencia temporal (una hora se parece a la siguiente) ni convierte ese dato puntual de la estación en un clima que varía por zona.

## 9. Análisis de sensibilidad

> **Nota:** un análisis de sensibilidad sirve para chequear si tu conclusión depende de una decisión metodológica particular (por ejemplo, usar la media en vez de la mediana) o si se mantiene aunque cambies esa decisión por una alternativa razonable. Si el resultado cambia mucho, es una señal de que hay que ser más cauteloso al comunicarlo.

Repetir una decisión del análisis bajo una alternativa razonable. Elegí al menos una de estas opciones:

- comparar media y mediana;
- comparar Pearson y Spearman;
- variar de forma justificada el ancho de los intervalos del histograma;
- comparar resultados con y sin los casos extremos identificados;
- estratificar (separar) por hora del día o día de la semana;
- cambiar una agregación y explicar cómo cambia lo que estás estimando.

Importante: la alternativa debe definirse **antes** de conocer cuál de las dos opciones produce el resultado más llamativo. Si elegís la alternativa después de ver cuál te "conviene" más, el análisis de sensibilidad pierde su sentido.

## 10. Hallazgos finales

Redactar como mínimo:

1. un hallazgo sobre la primera variable;
2. un hallazgo sobre la segunda variable;
3. un hallazgo sobre su relación.

Cada hallazgo debe contener:

- **contrato:** población, unidad y periodo a los que se refiere;
- **observación:** respaldada por una tabla o figura concreta, no solo una afirmación suelta;
- **cobertura:** faltantes y denominador (sobre cuántos casos válidos se basa la observación);
- **interpretación:** proporcional a la evidencia (no exageres lo que el dato realmente muestra);
- **explicación alternativa:** al menos una causa posible distinta a la que estás proponiendo;
- **límite:** qué cosas este análisis no permite afirmar;
- **siguiente comprobación posible:** qué harías después para reforzar o refutar el hallazgo.

Para redactar, usá expresiones como "se observa", "se relaciona" o "se asocia". Evitá "produce", "provoca", "explica" o "causa", salvo que tengas un diseño experimental adicional que realmente permita hablar de causalidad (que no es el caso en este trabajo).

## 11. Producto esperado

Entregar una copia ejecutable del notebook con:

- identificación del estudiante y del par elegido;
- ejecución reproducible para enero completo (que corra de punta a punta sin errores);
- contrato del análisis (sección 5);
- construcción y validación de la vista requerida (sección 2);
- dos análisis univariados (uno por columna, sección 6);
- tabla de casos potencialmente anómalos (sección 7);
- análisis bivariado (sección 8);
- al menos tres visualizaciones interpretadas (con su frase explicativa, no solo el gráfico);
- análisis de sensibilidad (sección 9);
- tres hallazgos finales (sección 10);
- límites y próximos pasos.

No se evalúa si llegaste a un resultado predeterminado. Dos análisis distintos pueden llegar a conclusiones diferentes y ambos estar bien, siempre que documenten correctamente su unidad de análisis, sus transformaciones, la evidencia que los respalda y el alcance de lo que afirman.

<div class="page-break"></div>

# Actividad EXTRA: estabilidad de la relación durante seis meses

**Carácter:** opcional
**Periodo ampliado:** enero a junio de 2024
**Fin exclusivo:** `2024-07-01`

> Esta actividad es opcional y pensada para quienes quieran ir un paso más allá. Si te interesa entender mejor si tus hallazgos de enero "se sostienen" con más datos, seguí leyendo; si no, con el trabajo principal ya cumplís con la consigna.

## 12. Objetivo de la actividad extra

Ampliar el análisis a seis meses de datos TLC y evaluar si las distribuciones, los casos anómalos y la relación identificada en enero se mantienen al incorporar nuevos periodos.

No se busca obtener una correlación mayor ni confirmar la causalidad. Se va a estudiar la **estabilidad temporal** del hallazgo: ¿lo que viste en enero sigue siendo cierto cuando mirás más meses, con las mismas definiciones y reglas?

## 13. Procesamiento mensual y concatenación

Procesar los archivos Yellow Taxi de enero, febrero, marzo, abril, mayo y junio de 2024.

> **Nota:** no cargues los seis archivos crudos al mismo tiempo en memoria; son pesados y podés quedarte sin memoria RAM. La estrategia correcta es procesar mes a mes y quedarte solo con el resultado ya resumido de cada uno.

Para cada mes:

1. construir la URL mediante `construir_url_tlc("yellow", 2024, mes)`;
2. leer únicamente las columnas requeridas por el flujo de calidad (no todas las columnas del archivo original);
3. filtrar por los límites de ese mes, siendo consciente de la zona horaria `America/New_York`;
4. aplicar las mismas reglas de validez que usaste en enero;
5. registrar cuántas filas se leyeron dentro de la ventana temporal, cuántas fueron válidas y cuántas fueron rechazadas;
6. enriquecer las zonas usando una única copia identificada del catálogo de zonas (no cargues el catálogo de nuevo en cada mes);
7. agregar los datos a nivel zona-hora;
8. añadir columnas `mes_fuente`, `url_fuente` y la fecha de acceso;
9. conservar el producto ya resumido de ese mes y liberar la tabla cruda de la memoria antes de pasar al siguiente mes.

Después, concatenar verticalmente (apilar, una tabla debajo de la otra) los productos mensuales:

```python
producto_seis_meses = pd.concat(
    productos_mensuales,
    ignore_index=True,
)
```

`concat` apila periodos que comparten el mismo esquema de columnas, uno debajo del otro. No es lo mismo que un `merge`, que combina tablas por una clave en común. Tampoco debe usarse `drop_duplicates()` como forma de "resolver" diferencias de esquema o periodos que se superponen: si eso pasa, hay que entender la causa, no ocultarla borrando filas.

## 14. Manifiesto y controles

> **Nota:** un "manifiesto" es simplemente una tabla de control que documenta, mes por mes, de dónde vinieron los datos y cuántas filas pasaron por cada etapa del procesamiento. Sirve para auditar tu propio trabajo y para que cualquier otra persona pueda verificarlo.

Construir un manifiesto con una fila por mes:

| Campo | Descripción |
|---|---|
| `mes_fuente` | mes procesado |
| `url_fuente` | archivo TLC utilizado |
| `filas_leidas_ventana` | registros devueltos por la lectura temporal, antes de aplicar las reglas de calidad |
| `filas_validas` | registros que superaron las reglas de calidad |
| `filas_rechazadas` | registros excluidos |
| `filas_fuera_periodo` | registros que no pertenecen al intervalo mensual, después de verificarlo |
| `filas_zona_hora` | filas del producto ya agregado |
| `fecha_minima` | primer pickup válido |
| `fecha_maxima` | último pickup válido |
| `fecha_acceso` | momento en que se obtuvo la fuente |

`filas_leidas_ventana` no es necesariamente la cantidad física total de filas del archivo mensual: es la cantidad que queda después de aplicar el filtro de lectura temporal y antes de aplicar las reglas de calidad. Usá esta misma definición de manera consistente en los seis meses.

Registrá también, para TLC, NOAA y el catálogo de zonas: la URL, la fecha de acceso, el nombre del recurso y, si el archivo fue descargado, un hash (una huella digital del archivo que permite verificar que no cambió). El catálogo de zonas debe cargarse una sola vez y reutilizarse en los seis procesos mensuales. Tené en cuenta que repetir la misma URL no demuestra por sí solo que el contenido remoto sea idéntico entre una ejecución y otra (los archivos publicados a veces se actualizan).

Comprobar mediante código (no "a ojo") que:

- estén presentes exactamente los seis meses;
- no se repita ninguna URL;
- todas las tablas mensuales tengan las mismas columnas y tipos de datos compatibles entre sí;
- cada timestamp pertenezca al mes que dice pertenecer;
- la clave zona-hora sea única dentro de cada producto mensual;
- no existan superposiciones temporales entre meses;
- las filas combinadas coincidan con la suma de las filas de cada mes por separado.

### Cambio al horario de verano

El periodo elegido incluye el inicio del horario de verano de Nueva York, el 10 de marzo de 2024. Ese día, por el cambio de horario, una hora "desaparece" del calendario local. La grilla esperada de horas debe generarse con límites conscientes de la zona horaria y usando `pd.date_range(..., freq="h", inclusive="left")`; no asumas que todos los días tienen 24 horas, porque ese día en particular no las tiene. Como referencia: marzo de 2024 contiene 743 horas locales (no 744) y todo el intervalo enero-junio contiene 4367 horas, pero estos valores tienen que salir del cálculo hecho en tu código a partir del calendario, no escribirse como un número fijo.

Los timestamps de TLC están en hora local, sin indicar la zona horaria. Si aparece una hora local que no existió por el salto de marzo (por ejemplo, algo cercano a las 2:00 AM de ese día), no la desplaces ni la elimines en silencio: marcala, conservala en tu auditoría, y tratala con una regla explícita que documentes. Los datos de NOAA, en cambio, parten de UTC y hay que convertirlos después a `America/New_York`, lo cual sí representa correctamente el salto de horario.

## 15. Extensión del clima

Si tu par incluye una variable meteorológica:

1. usar la misma fuente NOAA de 2024 que ya está definida en el notebook;
2. ampliar la ventana temporal local hasta `2024-07-01`, con ese límite excluido;
3. resumir los datos a una fila meteorológica por hora (igual que en la vista H);
4. revisar la cobertura y los faltantes para cada mes;
5. unir el clima con la tabla zona-hora recién después de concatenar los productos mensuales de TLC;
6. volver a una fila por hora antes de hacer el análisis clima-clima o pickups-clima.

Si tu par no incluye clima, no hace falta procesar NOAA para esta actividad extra.

## 16. Repetición y comparación del EDA

Repetir sobre el periodo enero-junio:

1. exploración univariada de ambas columnas;
2. revisión de faltantes, ceros y cobertura;
3. identificación de casos potencialmente anómalos con reglas declaradas;
4. análisis de la relación con la misma vista y método principal que usaste en enero;
5. análisis de sensibilidad.

Usá enero como periodo inicial y febrero-junio como periodo de contraste que no se superpone con enero. Presentá además enero-junio como un resumen global descriptivo. Importante: no uses la comparación "enero contra enero-junio" como evidencia de estabilidad, porque ambos conjuntos comparten las observaciones de enero (no son independientes entre sí).

Para estudiar si las anomalías se repiten, usá como análisis principal los límites que definiste en enero, y aplicalos sin recalibrar a los meses de febrero a junio. Como análisis de sensibilidad, podés calcular una regla separada dentro de cada mes, aclarando que eso identifica extremos locales de ese mes y responde una pregunta distinta.

Comparar enero, febrero-junio y el resumen global respondiendo:

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

- numérica-numérica: dispersión global y gráficos separados (facetas) por mes, con escalas comunes para poder comparar;
- categórica-numérica: distribuciones por grupo y por mes;
- temporal-numérica: serie completa y perfiles por mes, día u hora.

## 18. Relación global y relaciones mensuales

Para pares numérica-numérica o categórica-numérica, comparar explícitamente:

<p class="formula">relación global de seis meses &nbsp; frente a &nbsp; relaciones dentro de cada mes</p>

> **Nota:** el **efecto o paradoja de Simpson** ocurre cuando una relación que se observa en los datos combinados desaparece, se debilita o incluso se invierte al mirar los subgrupos (en este caso, los meses) por separado. Suele pasar cuando hay una variable oculta (como la estación del año) que afecta tanto a los grupos como a la relación que estás midiendo.

Una asociación global puede estar dominada por estacionalidad, por tamaños de muestra distintos entre meses, o por la mezcla de periodos con comportamientos distintos. Si el patrón global cambia de dirección o se invierte al mirar los meses por separado, discutí si hay una posible confusión temporal o una manifestación del efecto Simpson.

Para los pares `GT-02` a `GT-05` (los que involucran `pickup_hora`), no calcules una correlación contra el timestamp ni fuerces una lectura en clave de efecto Simpson: en su lugar, comparé perfiles horarios, ciclos semanales, cambios de nivel, huecos y anomalías entre los distintos meses, usando siempre la misma agregación y escala.

Un punto importante de honestidad metodológica: no elijas ni excluyas meses después de haber visto cuál de ellos respalda mejor tu conclusión original.

## 19. Preguntas finales de la actividad extra

1. ¿El patrón observado en enero se mantiene en el periodo no solapado febrero-junio?
2. ¿La dirección y la forma de la relación son estables?
3. ¿Qué meses presentan diferencias importantes?
4. ¿Los casos anómalos son recurrentes o específicos de algún mes?
5. ¿Algún mes domina el resultado combinado?
6. ¿La conclusión original debe mantenerse, limitarse o reformularse?
7. ¿Qué explicaciones alternativas siguen siendo compatibles con los datos?

<div class="page-break"></div>

## 20. Producto de la actividad extra

Agregar al notebook una sección identificada como `Actividad EXTRA` con:

- manifiesto de las seis fuentes TLC;
- identificación de versiones o huellas (hashes) de las fuentes auxiliares;
- auditoría mensual;
- construcción reproducible de `producto_seis_meses`;
- extensión de NOAA si corresponde a tu par;
- comparación de distribuciones;
- revisión de anomalías por mes;
- contraste enero frente a febrero-junio, y resumen global enero-junio;
- análisis global y mensual de la relación o estructura temporal;
- al menos dos visualizaciones adicionales;
- conclusión sobre la estabilidad temporal del hallazgo;
- límites y siguiente comprobación posible.

Los datos de seis meses siguen representando viajes en Yellow Taxi realizados y reportados, no la demanda total. Tener más filas no elimina por sí solo los sesgos de cobertura, la dependencia temporal, la pseudorreplicación ni la existencia de explicaciones alternativas: esas limitaciones siguen valiendo, aunque el conjunto de datos sea más grande.
