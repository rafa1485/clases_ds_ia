# Capítulo 13. Aprendizaje no supervisado y descubrimiento de estructuras

El aprendizaje no supervisado estudia observaciones para las que no se dispone de una variable objetivo que indique la respuesta correcta. Su propósito no es adivinar etiquetas ocultas, sino construir representaciones, detectar regularidades, resumir heterogeneidad y formular hipótesis que luego deberán contrastarse. Agrupar clientes, documentos o zonas de operación puede ayudar a describir un sistema; no demuestra, por sí solo, que existan clases naturales ni explica por qué se formaron los grupos.

Esta diferencia cambia el criterio de éxito. En una tarea supervisada puede medirse el error frente a respuestas conocidas. En una tarea no supervisada existen muchas particiones matemáticamente válidas y la calidad depende de la representación, la métrica, el algoritmo, los hiperparámetros y el uso previsto. Una solución compacta según una métrica puede ser inestable, trivial o irrelevante para la decisión. Por ello, este capítulo trata el agrupamiento como un proceso de modelado y validación, no como la ejecución aislada de un algoritmo.

Al finalizar el capítulo, se espera que el estudiante pueda:

- formular una pregunta no supervisada con unidad de análisis y propósito explícitos;
- elegir distancias y transformaciones coherentes con variables numéricas, categóricas o mixtas;
- explicar y diagnosticar K-means, agrupamiento jerárquico, DBSCAN y mapas autoorganizados;
- combinar métricas internas, referencias externas, estabilidad y utilidad para seleccionar una solución;
- caracterizar grupos sin convertir resultados algorítmicos en categorías esenciales;
- distinguir una observación atípica, el ruido del algoritmo y un evento que requiere investigación;
- documentar límites de cobertura, sensibilidad y consecuencias de uso.

## 13.1. Distancias, similitudes y representación

Todo método de agrupamiento incorpora una definición de semejanza. A veces aparece de forma explícita como una matriz de distancias; otras queda implícita en una función objetivo. Antes de elegir un algoritmo debe definirse qué significa que dos unidades sean parecidas, qué diferencias importan y cuáles son artefactos de escala o codificación. La distancia es, por tanto, una hipótesis de dominio expresada matemáticamente.

Sea una matriz de datos $X\in\mathbb{R}^{n\times p}$, con $n$ observaciones y $p$ variables. La fila $\mathbf{x}_i$ representa una unidad de análisis. Esta notación sencilla oculta decisiones importantes: una fila podría representar una persona, una compra, una zona o un día; las columnas podrían ser mediciones originales, proporciones, indicadores o resúmenes temporales. Cambiar cualquiera de esas decisiones cambia el problema aun cuando el algoritmo conserve el mismo nombre.

### 13.1.1. Objetivos del aprendizaje no supervisado

Los objetivos más frecuentes pueden organizarse en cuatro familias. La primera es el **descubrimiento de grupos**, que busca particiones con alta semejanza interna y diferencia entre grupos. La segunda es la **representación**, que resume observaciones mediante prototipos, componentes o mapas de menor dimensión. La tercera es la **detección de estructura local**, que identifica vecindades, regiones densas y observaciones aisladas. La cuarta es la **exploración generadora de hipótesis**, donde los patrones sugieren preguntas para estudios posteriores.

Estos objetivos no son equivalentes. Si el propósito es comprimir datos, puede aceptarse una representación que preserve bien el promedio aunque simplifique casos raros. Si el propósito es investigar anomalías, esos mismos casos raros son centrales. Si se pretende asignar recursos, importan además la estabilidad de los segmentos, su tamaño y la posibilidad de describirlos con variables disponibles al momento de decidir.

Una formulación adecuada responde antes del ajuste:

1. ¿Cuál es la unidad de análisis?
2. ¿Qué periodo, población y mecanismo de observación cubren los datos?
3. ¿Qué significa semejanza para el problema?
4. ¿Se requiere una partición exhaustiva o se admite ruido sin asignar?
5. ¿Cómo se utilizará y revisará el resultado?

No disponer de etiquetas no significa carecer de conocimiento. Restricciones físicas, taxonomías parciales, auditorías humanas y variables contextuales pueden validar una solución sin usarse para construirla. Conviene separar variables de **formación**, que determinan los grupos, de variables de **caracterización**, que ayudan a interpretarlos después. Así se evita fabricar una conclusión al introducirla previamente en la representación.

Una precaución conceptual es hablar de *segmentos encontrados bajo una representación y un método*, no de clases verdaderas. Dos algoritmos pueden responder preguntas distintas: K-means busca centroides que reduzcan dispersión cuadrática; DBSCAN busca componentes conectados por densidad. El desacuerdo puede revelar geometrías diferentes en lugar de señalar automáticamente que uno de ellos está equivocado.

### 13.1.2. Distancia euclídea

Para dos vectores numéricos $\mathbf{x},\mathbf{z}\in\mathbb{R}^p$, la distancia euclídea es

$$
d_2(\mathbf{x},\mathbf{z})=
\sqrt{\sum_{j=1}^{p}(x_j-z_j)^2}.
$$

Es la longitud del segmento recto entre ambos puntos. Satisface no negatividad, identidad, simetría y desigualdad triangular, por lo que es una métrica. Elevar las diferencias al cuadrado hace que las discrepancias grandes pesen más. Por ejemplo, entre $A=(2,3)$ y $B=(5,7)$ se obtiene $d_2(A,B)=\sqrt{3^2+4^2}=5$.

La distancia euclídea es coherente cuando las variables son cuantitativas, comparables y las diferencias poseen significado aproximadamente lineal. Está ligada a K-means: el centro que minimiza la suma de distancias euclídeas al cuadrado dentro de un grupo es la media aritmética. También se relaciona con la suposición de grupos aproximadamente esféricos y con varianzas similares cuando se interpreta probabilísticamente.

Sus limitaciones son decisivas. Una variable expresada en miles puede dominar a otra expresada entre cero y uno. Los valores extremos se amplifican por el cuadrado. En muchas dimensiones, las distancias tienden a concentrarse: la diferencia relativa entre vecinos cercanos y lejanos disminuye, y el concepto de vecindad pierde contraste. Variables redundantes cuentan varias veces el mismo fenómeno. Además, la geometría recta no es apropiada para todos los dominios: dos horas cercanas a medianoche parecen lejanas si se codifica la hora como un número lineal.

El diagnóstico debe incluir distribución de distancias, contribución de cada variable y sensibilidad al retirar variables correlacionadas. Si casi todos los pares están a distancias similares, no basta con ejecutar un método; hay que reconsiderar representación, dimensión o métrica. Una transformación no se justifica porque mejore una cifra, sino porque aproxima mejor la noción sustantiva de diferencia.

### 13.1.3. Distancia Manhattan

La distancia Manhattan, $L_1$ o de bloques, suma diferencias absolutas:

$$
d_1(\mathbf{x},\mathbf{z})=
\sum_{j=1}^{p}|x_j-z_j|.
$$

Para los puntos anteriores, $d_1(A,B)=|2-5|+|3-7|=7$. A diferencia de la euclídea, no eleva las discrepancias al cuadrado. Un cambio de cuatro unidades en una variable aporta lo mismo que cuatro cambios de una unidad distribuidos entre variables. Esto puede reducir la influencia relativa de diferencias extremas, aunque no elimina la necesidad de escalar ni convierte el método en inmune a valores atípicos.

La geometría inducida por $L_1$ favorece contornos en forma de rombo y puede ser adecuada cuando los atributos representan cantidades aditivas o cuando la ruta conceptual solo permite cambios por coordenadas. En espacios dispersos, como perfiles con muchas entradas cero, puede conservar contrastes distintos de los de $L_2$. El representante que minimiza desviaciones absolutas en una dimensión es la mediana; esta relación motiva métodos de medoides o variantes basadas en $L_1$, pero no autoriza a reemplazar la distancia de K-means estándar sin cambiar también su actualización y su objetivo.

Un ejemplo simple ilustra el cambio de vecino. Considérese un punto origen $O=(0,0)$ y candidatos $P=(3,0)$ y $Q=(2,2)$. Según Euclídea, $d_2(O,P)=3$ y $d_2(O,Q)=\sqrt{8}\approx2{,}83$, por lo que $Q$ está más cerca. Según Manhattan, $d_1(O,P)=3$ y $d_1(O,Q)=4$, por lo que $P$ está más cerca. Ningún resultado es universalmente correcto: cada uno expresa un costo de desplazamiento distinto.

Conviene comparar matrices de vecinos bajo $L_1$ y $L_2$, observar qué unidades cambian de vecindad y explicar el cambio variable por variable. Si una conclusión desaparece al alternar métricas igualmente defendibles, debe reportarse como sensible y no como estructura robusta.

### 13.1.4. Similitud coseno

La similitud coseno compara orientación y no distancia absoluta:

$$
s_{\cos}(\mathbf{x},\mathbf{z})=
\frac{\mathbf{x}^{\mathsf T}\mathbf{z}}
{\|\mathbf{x}\|_2\|\mathbf{z}\|_2},
$$

si ambos vectores tienen norma no nula. Para datos no negativos toma valores usualmente entre 0 y 1; en general, entre $-1$ y 1. Una distancia derivada frecuente es $d_{\cos}=1-s_{\cos}$, aunque no todas las transformaciones de similitud conservan todas las propiedades métricas.

Dos vectores proporcionales tienen coseno uno. Así, perfiles $A=(2,4,2)$ y $B=(20,40,20)$ poseen la misma composición relativa aunque magnitudes muy diferentes. Esto resulta útil al comparar distribuciones horarias, frecuencias de términos o preferencias relativas. Pero sería inadecuado si el volumen total fuera sustantivo: dos zonas con el mismo patrón horario y cien veces distinta cantidad de observaciones no deberían tratarse necesariamente como equivalentes.

La decisión puede resolverse separando **forma** y **nivel**. Las proporciones normalizadas describen la forma del perfil, mientras una variable adicional transformada, como el logaritmo del volumen, conserva información de magnitud. Su peso debe declararse. Centrar variables cambia radicalmente el significado del coseno, porque pasa de comparar direcciones desde el origen a comparar direcciones respecto de otro punto. La correlación de Pearson se relaciona con el coseno de vectores centrados, pero no es idéntica al coseno de los datos originales.

Los vectores nulos requieren una regla explícita: no tienen dirección y su coseno no está definido. Tampoco debe interpretarse un coseno alto como cercanía causal o equivalencia general. Solo indica orientación semejante en las variables incluidas. El diagnóstico mínimo compara similitud, normas y volumen; de ese modo se detectan pares que parecen idénticos por composición pero difieren operacionalmente en escala.

### 13.1.5. Escalas y ponderación de variables

Supóngase que una variable varía entre 0 y 10 000 y otra entre 0 y 1. Sin transformación, la primera dominará casi cualquier distancia euclídea o Manhattan. Estandarizar por media y desviación típica produce

$$
z_{ij}=\frac{x_{ij}-\bar{x}_j}{s_j}.
$$

Esta operación asigna a cada variable varianza unitaria, pero no es neutral: afirma que una desviación típica representa una diferencia comparable en todas las dimensiones. Si una variable tiene una distribución muy asimétrica o valores extremos, la media y la desviación pueden ser poco representativas. Una alternativa robusta usa mediana y rango intercuartílico:

$$
r_{ij}=\frac{x_{ij}-\operatorname{mediana}(X_j)}
{Q_{0.75}(X_j)-Q_{0.25}(X_j)}.
$$

El escalado mínimo-máximo sitúa valores observados en un intervalo, por lo común $[0,1]$, pero es sensible a extremos y a nuevos valores fuera del rango de ajuste. Las transformaciones logarítmicas pueden comprimir colas derechas para cantidades no negativas. Las proporciones necesitan tratamiento cuidadoso: sus componentes suman uno y no constituyen dimensiones independientes. Incluir cuatro proporciones horarias y además su suma agrega redundancia perfecta.

La distancia ponderada explicita prioridades:

$$
d_w(\mathbf{x},\mathbf{z})=
\sqrt{\sum_{j=1}^{p}w_j(x_j-z_j)^2},
\qquad w_j\geq0.
$$

Los pesos no deben elegirse solo para obtener grupos visualmente atractivos. Pueden derivarse de confiabilidad, relevancia operativa o equilibrio entre bloques. Por ejemplo, si se incluyen doce proporciones temporales y dos variables de diversidad, el bloque temporal puede dominar por cantidad de columnas aunque cada una esté estandarizada. Asignar peso total comparable a cada bloque evita que la dimensionalidad sustituya al juicio sustantivo.

Todo transformador debe ajustarse con el conjunto que corresponde al análisis y conservarse para nuevas observaciones. En estudios de estabilidad temporal, usar información futura para escalar el pasado introduce una dependencia innecesaria. Se recomienda documentar parámetros, inspeccionar distribuciones antes y después, y repetir el análisis con transformaciones plausibles. Una segmentación que cambia completamente ante pequeñas modificaciones de escalado carece de solidez para usos persistentes.

### 13.1.6. Datos mixtos

Muchos problemas combinan variables numéricas, binarias, nominales, ordinales y posiblemente fechas. Convertir categorías nominales a enteros crea distancias ficticias: codificar rojo, verde y azul como 1, 2 y 3 implica un orden y hace que rojo-azul sea el doble de distante que rojo-verde. La codificación one-hot evita ese orden, pero puede sobrerrepresentar variables con muchas categorías y modifica la geometría.

La distancia de Gower ofrece una estrategia para datos mixtos. Para dos observaciones $i$ y $l$, calcula una disimilitud parcial $\delta_{ilj}$ por variable y las combina:

$$
d_G(i,l)=
\frac{\sum_{j=1}^{p}w_{ilj}\delta_{ilj}}
{\sum_{j=1}^{p}w_{ilj}}.
$$

Para una variable numérica, $\delta_{ilj}=|x_{ij}-x_{lj}|/R_j$, donde $R_j$ es un rango documentado. Para una nominal, vale cero si coincide y uno si difiere. Para una ordinal, se transforman categorías a rangos normalizados respetando el orden. El peso $w_{ilj}$ puede ser cero si falta uno de los valores, lo que permite comparar con la información disponible; sin embargo, dos distancias calculadas con conjuntos de variables distintos no poseen necesariamente la misma confiabilidad.

Las variables binarias merecen distinguir presencia y ausencia. En una binaria simétrica, coincidencias en cero y en uno cuentan por igual. En una asimétrica, como presencia de una característica rara, dos ausencias conjuntas aportan poca evidencia de semejanza; índices como Jaccard ignoran esa coincidencia. La elección debe responder al significado, no al tipo de almacenamiento.

Una matriz de Gower puede alimentar métodos que aceptan disimilitudes, como clustering jerárquico o k-medoids. K-means no es directamente apropiado porque requiere medias en un espacio euclídeo. Para categorías puras existen métodos basados en modas, y para datos mixtos hay extensiones, pero sus objetivos deben explicarse.

Los faltantes no son una categoría por defecto. “Desconocido” puede describir el proceso de captura y formar un grupo artificial. Antes de agrupar se evalúan patrón de ausencia, comparabilidad y calidad. Un buen diagnóstico informa cuántas variables contribuyeron a cada distancia y prueba si los grupos separan principalmente niveles de faltantes.

### 13.1.7. Ejemplo práctico guiado: comparación de similitudes entre observaciones

Considérense cuatro establecimientos descritos por visitas semanales, duración mediana de la visita en minutos y proporción de visitas de fin de semana:

| Unidad | Visitas | Duración | Proporción fin de semana |
|---|---:|---:|---:|
| A | 100 | 20 | 0,20 |
| B | 120 | 22 | 0,70 |
| C | 300 | 21 | 0,22 |
| D | 105 | 45 | 0,19 |

Sin escalar, la diferencia de visitas domina la distancia euclídea. Para A, B parece cercano por volumen y C lejano, aunque A y C se parecen en duración y composición semanal. Tras estandarizar, las tres dimensiones tienen influencia comparable: la gran proporción de fin de semana aleja a B y la duración aleja a D. No se ha “corregido” una respuesta: se ha cambiado la definición de semejanza.

El análisis guiado sigue estos pasos:

1. **Definir el propósito.** Si interesa capacidad total, el volumen no debe desaparecer. Si interesa únicamente la forma de uso, puede normalizarse o analizarse por separado.
2. **Auditar variables.** Visitas es una cuenta con posible asimetría; duración puede contener extremos; la proporción está acotada.
3. **Comparar representaciones.** Se contrastan datos originales, estandarización y transformación logarítmica de visitas seguida de escalado robusto.
4. **Comparar métricas.** Para cada alternativa se ordenan los vecinos de A con Euclídea y Manhattan.
5. **Explicar cambios.** Se descompone la distancia en aportes por variable, no solo se presenta el vecino final.

Supóngase que, después de una transformación defendible, A tiene como vecino a C bajo ambas métricas, mientras B y D intercambian posiciones. La coincidencia A-C es evidencia local de robustez; el orden B-D es sensible. Con solo cuatro unidades no corresponde declarar segmentos estables. El ejemplo sirve para mostrar que el preprocesamiento forma parte del modelo.

Un informe breve incluiría una tabla de vecinos bajo cada escenario, histogramas de variables, matriz de distancias y una conclusión condicional: “A y C son similares respecto de composición y duración; no son equivalentes en volumen”. También registraría qué ocurriría si la proporción de fin de semana tuviera error de medición. Este análisis de sensibilidad es más informativo que escoger automáticamente la alternativa con separación visual mayor.

## 13.2. Agrupamiento particional y jerárquico

Los métodos particionales asignan observaciones a un número de grupos definido o seleccionado mediante un criterio. Los jerárquicos construyen relaciones anidadas y permiten examinar soluciones a distintas escalas. Ambos dependen de la representación y ninguno garantiza recuperar una taxonomía verdadera. La elección se fundamenta en la geometría buscada, el tamaño de los datos, la necesidad de prototipos y la estabilidad.

### 13.2.1. Algoritmo K-means

K-means divide $n$ observaciones numéricas en $K$ grupos $C_1,\ldots,C_K$ minimizando la suma de cuadrados dentro de grupos:

$$
J=\sum_{k=1}^{K}\sum_{\mathbf{x}_i\in C_k}
\|\mathbf{x}_i-\boldsymbol{\mu}_k\|_2^2,
\qquad
\boldsymbol{\mu}_k=\frac{1}{|C_k|}
\sum_{\mathbf{x}_i\in C_k}\mathbf{x}_i.
$$

El algoritmo alterna dos operaciones. Con centroides fijos, asigna cada observación al centro más cercano. Con asignaciones fijas, reemplaza cada centro por la media de su grupo. Cada operación no aumenta $J$, de modo que el procedimiento converge en un número finito de asignaciones, aunque puede hacerlo a un mínimo local.

**Pseudocódigo conceptual de K-means**

```text
Entrada: observaciones X, número de grupos K, criterio de parada
Inicializar K centroides
Repetir:
    asignar cada observación al centroide más cercano
    recalcular cada centroide como media de sus observaciones
    tratar cualquier grupo vacío con una regla documentada
Hasta que no cambien las asignaciones o la mejora sea menor que la tolerancia
Salida: asignaciones, centroides e inercia
```

K-means produce una partición exhaustiva: incluso una observación muy alejada queda asignada. Sus fronteras son regiones de Voronoi y, por ello, los grupos resultantes son convexos en el espacio transformado. Funciona mejor con grupos compactos, aproximadamente esféricos, de dispersión y tamaño no demasiado diferentes. Puede dividir un grupo alargado o fusionar grupos de densidades distintas.

Los centroides no siempre corresponden a observaciones reales. Son perfiles promedio y pueden ser imposibles si se aplican a variables binarias o categorías. El método requiere datos numéricos y distancia euclídea al cuadrado coherente con la media; cambiar arbitrariamente la métrica rompe la correspondencia entre asignación, actualización y objetivo.

El costo por iteración es aproximadamente $O(nKp)$, lo que lo hace escalable. Esa eficiencia no compensa una geometría inadecuada. Los diagnósticos incluyen tamaño por grupo, distancias al centro, contribución por variable, observaciones fronterizas y comparación entre reinicios.

### 13.2.2. Inicialización y convergencia

La función de K-means no es convexa conjuntamente en asignaciones y centroides. Dos inicializaciones pueden conducir a soluciones diferentes. Elegir al azar $K$ observaciones como centros es sencillo, pero puede ubicar varios centros en una región densa y dejar otras mal representadas. El método K-means++ selecciona el primer centro al azar y favorece luego puntos con gran distancia cuadrática al centro más cercano ya elegido. Esto tiende a dispersar los centros iniciales y suele mejorar velocidad y calidad, sin garantizar el óptimo global.

Una práctica esencial es ejecutar múltiples reinicios y conservar la solución con menor inercia. Sin embargo, si varias soluciones poseen inercias casi iguales y asignaciones muy distintas, elegir solo la menor oculta ambigüedad estructural. Deben compararse las particiones, por ejemplo mediante índice de Rand ajustado entre corridas, y contar cuántas veces aparece cada solución.

La convergencia puede definirse por ausencia de cambios, desplazamiento de centroides menor que una tolerancia, reducción mínima del objetivo o máximo de iteraciones. Alcanzar el criterio solo significa que el algoritmo dejó de mejorar localmente; no demuestra validez de los grupos. Una tolerancia excesiva puede detenerlo antes de tiempo y una muy estricta puede añadir costo sin cambio relevante.

Los grupos vacíos aparecen cuando ningún punto queda asociado a un centro. Posibles reglas son reinicializar ese centro en una observación distante o dividir el grupo con mayor dispersión. La regla afecta el resultado y debe registrarse. Duplicados numerosos también pueden producir menos de $K$ puntos distintos efectivos.

El diagnóstico de convergencia reporta, como mínimo, número de reinicios, estrategia inicial, distribución de inercias finales, iteraciones y acuerdo entre particiones. Para evaluar estabilidad no basta cambiar la semilla sobre los mismos datos: también se remuestrean observaciones, se perturban mediciones dentro de su incertidumbre o se repite por periodos. La semilla mide variabilidad algorítmica; el remuestreo aproxima sensibilidad a la muestra.

### 13.2.3. Selección del número de grupos

K-means exige $K$, pero los datos rara vez contienen un valor inequívoco. La inercia disminuye siempre al aumentar $K$ y llega a cero si cada observación distinta constituye su propio grupo. El método del codo busca un punto a partir del cual añadir grupos produce mejoras marginales menores. Es una heurística visual y puede no mostrar un codo claro.

Silhouette, Davies-Bouldin y otras métricas internas comparan compactación y separación, pero favorecen determinadas geometrías. El máximo de silhouette no debe adoptarse mecánicamente. Una solución con dos grupos puede separar volumen alto y bajo de manera estable, mientras una de cuatro revela patrones temporales útiles aunque tenga una cifra algo menor. La decisión depende del propósito y del costo de mantener segmentos.

Un protocolo razonable es:

1. definir un rango de $K$ compatible con el tamaño muestral y el uso;
2. ejecutar múltiples inicializaciones para cada $K$;
3. comparar inercia, silhouette, Davies-Bouldin y tamaños;
4. medir estabilidad ante semillas, remuestreo, periodos y transformaciones plausibles;
5. caracterizar las soluciones candidatas sin usar nombres valorativos;
6. elegir la solución más simple que aporte distinciones estables y accionables.

Los grupos diminutos requieren investigación. Pueden representar un patrón legítimo, errores, extremos o la fragmentación forzada por $K$. Un grupo con una observación hace indefinidas algunas medidas y no es automáticamente una anomalía válida. Del mismo modo, exigir tamaños iguales puede ocultar una estructura real, pero aceptar cualquier desequilibrio puede producir segmentos inoperantes.

La estabilidad de $K$ puede estudiarse observando si grupos de una solución se subdividen de manera coherente al aumentar $K$. Un diagrama de flujo entre particiones muestra continuidad o reorganización completa. Si pasar de tres a cuatro grupos cambia casi todas las asignaciones, la jerarquía conceptual es débil. La selección final debe presentar alternativas descartadas y explicar el compromiso, no solo anunciar un entero.

### 13.2.4. Clustering jerárquico

El agrupamiento jerárquico representa relaciones anidadas entre observaciones. En el enfoque aglomerativo, cada observación comienza como un grupo y se fusionan repetidamente los dos grupos más próximos. En el divisivo, todas comienzan juntas y el conjunto se divide. El resultado se visualiza mediante un dendrograma.

El método aglomerativo requiere una disimilitud entre observaciones y una regla de enlace para convertir distancias entre puntos en distancias entre grupos. Su pseudocódigo conceptual es:

```text
Entrada: matriz de disimilitudes y regla de enlace
Crear un grupo por observación
Mientras exista más de un grupo:
    identificar el par de grupos con menor disimilitud de enlace
    fusionar ese par
    actualizar las disimilitudes entre el nuevo grupo y los restantes
    registrar la altura de fusión
Salida: secuencia de fusiones y dendrograma
```

Una vez realizada una fusión aglomerativa no se deshace. Una decisión local temprana puede propagarse por toda la jerarquía. No existe una función objetivo única compartida por todos los enlaces. Por ello debe examinarse la coherencia entre métrica y enlace.

La jerarquía es útil cuando interesa explorar distintos niveles de granularidad, cuando no se desea fijar $K$ inicialmente o cuando una matriz de distancias permite datos mixtos. Su costo de memoria suele ser $O(n^2)$ por la matriz de pares, lo que limita muestras grandes. Para datos masivos puede aplicarse a prototipos o a una muestra, aclarando que la jerarquía resultante corresponde a esa aproximación.

El dendrograma no prueba que el mundo sea jerárquico. Siempre puede construirse uno, incluso con ruido sin grupos. La validación evalúa alturas, estabilidad de ramas y asociación con perfiles interpretables. El orden horizontal de hojas puede cambiar sin alterar la jerarquía; no debe interpretarse como una escala adicional.

### 13.2.5. Métodos aglomerativos y divisivos

Los métodos **aglomerativos** siguen una estrategia ascendente. Empiezan con $n$ grupos y realizan $n-1$ fusiones. Son los más difundidos por su formulación sencilla y disponibilidad de enlaces. Resultan apropiados para reconocer pequeñas unidades muy similares que luego forman conjuntos mayores. Su debilidad es la irreversibilidad: una fusión errónea al inicio permanece.

Los métodos **divisivos** siguen una estrategia descendente. Comienzan con un único conjunto y seleccionan un grupo para dividirlo, a menudo buscando la división que más reduce heterogeneidad. Pueden concentrar esfuerzo en separaciones globales importantes, pero explorar todas las divisiones posibles es combinatoriamente costoso. En la práctica se utilizan heurísticas, por ejemplo una partición binaria repetida.

Ambas estrategias pueden generar árboles diferentes porque optimizan decisiones locales opuestas. Considérese un conjunto con dos nubes grandes unidas por pocos puntos intermedios. Un método aglomerativo con enlace simple puede encadenarlas temprano a través del puente. Uno divisivo podría reconocer primero la separación global si su criterio penaliza el corte de regiones densas.

La elección debe atender a la pregunta. Si interesan microgrupos de alta similitud que se integran progresivamente, la perspectiva ascendente es natural. Si existe una división global justificable y luego se desean subtipos, la descendente puede comunicar mejor el análisis. En ambos casos se deben revisar ramas pequeñas, sensibilidad a observaciones extremas y estabilidad por remuestreo.

Para comparar árboles completos pueden usarse correlaciones cofenéticas, que contrastan distancias originales con alturas de fusión, o medidas de similitud entre dendrogramas. Una correlación alta indica que el árbol conserva razonablemente disimilitudes pares; no certifica utilidad ni una cantidad de grupos. La comparación más directa para una decisión concreta consiste en cortar ambos árboles a granularidades candidatas y evaluar asignaciones, perfiles y estabilidad.

### 13.2.6. Tipos de enlace

La regla de enlace define distancia entre grupos $A$ y $B$.

**Enlace simple:**

$$
D_{\text{simple}}(A,B)=\min_{i\in A,\,l\in B}d(i,l).
$$

Une grupos si al menos un par está cerca. Puede descubrir formas alargadas, pero sufre el efecto de encadenamiento: una sucesión de puntos puente conecta regiones distintas.

**Enlace completo:**

$$
D_{\text{completo}}(A,B)=\max_{i\in A,\,l\in B}d(i,l).
$$

Exige que los puntos más alejados sean relativamente próximos y favorece grupos compactos. Es sensible a extremos, pues un solo punto distante controla el enlace.

**Enlace promedio:**

$$
D_{\text{promedio}}(A,B)=
\frac{1}{|A||B|}\sum_{i\in A}\sum_{l\in B}d(i,l).
$$

Equilibra los criterios anteriores y usa toda la información entre pares. Puede ser más estable, aunque el costo y la interpretación dependen de la disimilitud.

**Enlace de Ward:** fusiona los grupos que producen el menor incremento en suma de cuadrados dentro de grupos:

$$
\Delta(A,B)=\frac{|A||B|}{|A|+|B|}
\|\boldsymbol{\mu}_A-\boldsymbol{\mu}_B\|_2^2.
$$

Favorece grupos compactos y de tamaño parecido. Su interpretación clásica corresponde a datos numéricos con geometría euclídea; combinar Ward con una disimilitud arbitraria de datos mixtos carece de la misma justificación.

No hay un enlace universalmente superior. Debe evaluarse con datos simulados de geometría conocida o análisis de sensibilidad. Si simple produce una cadena gigante, se inspeccionan puentes. Si completo aísla extremos, se auditan esas observaciones. Si Ward divide principalmente por volumen, se reconsideran escalas. El acuerdo de un núcleo de observaciones entre enlaces fortalece la evidencia; las unidades que cambian se etiquetan como fronterizas en vez de forzarlas a una narrativa inequívoca.

### 13.2.7. Dendrogramas

Un dendrograma muestra hojas, fusiones y alturas. Cada hoja representa una observación o grupo inicial. La altura vertical de una unión indica la disimilitud de enlace a la que se fusionaron sus ramas. Trazar un corte horizontal induce una partición: el número de ramas interceptadas es el número de grupos.

Las alturas deben leerse según el enlace. En Ward representan incrementos de heterogeneidad, no necesariamente distancias directas entre puntos. Grandes saltos verticales sugieren cortes posibles, pero no constituyen una prueba. Con datos continuos sin separación clara también habrá un salto máximo. Además, la apariencia depende de escala, transformaciones y cantidad de observaciones.

Tres errores son frecuentes. Primero, interpretar proximidad horizontal entre hojas como distancia: las ramas pueden rotarse sin cambiar el árbol. Segundo, escoger un corte solo porque produce un número deseado. Tercero, describir cada rama como categoría real sin examinar perfiles. Un dendrograma con cientos de hojas necesita recursos complementarios, como colores de corte, mapa de calor de variables ordenadas y resúmenes por rama.

La estabilidad puede visualizarse con soporte de ramas obtenido por remuestreo. Si una rama aparece en una proporción alta de muestras, su composición es relativamente estable. Aun así, el soporte depende del esquema de remuestreo y de cómo se emparejan grupos. También puede calcularse una matriz de coasignación $P_{il}$: proporción de ejecuciones en que $i$ y $l$ quedan juntos. Bloques nítidos indican núcleos estables; bandas difusas revelan fronteras.

Antes de aceptar un corte se revisan tamaños, alturas vecinas, silhouette por observación, variables que distinguen ramas y sensibilidad a enlaces. El dendrograma es una herramienta de exploración multiescala, no una máquina automática para contar grupos.

### 13.2.8. Ejemplo práctico guiado: segmentación de patrones de consumo

Una organización desea resumir patrones de compras mensuales de productos de oficina para planificar inventario. La unidad es una cuenta activa y el periodo comprende doce meses completos. Las variables de formación son proporciones de gasto en cuatro familias, frecuencia mensual, variabilidad entre meses y valor mediano por compra. No se incluyen nombres de empresa ni resultados comerciales; esas variables, si fueran pertinentes y legítimas, se reservarían para caracterización.

Primero se audita cobertura. Cuentas con un solo mes observado no son comparables con cuentas de doce meses y se tratan por separado. El gasto total tiene cola derecha, por lo que se transforma logarítmicamente. Las proporciones describen composición y la frecuencia describe intensidad; se ponderan ambos bloques para evitar que las cuatro proporciones dominen por número de columnas.

Se comparan K-means y clustering aglomerativo de Ward, ambos sobre la misma representación euclídea estandarizada. Para K-means se exploran $K=2,\ldots,8$, con múltiples inicializaciones. Para Ward se examina el dendrograma y se cortan las mismas granularidades. Una tabla de diagnóstico podría ser:

| Solución | Silhouette | Grupo mínimo | Estabilidad por remuestreo | Observación |
|---|---:|---:|---:|---|
| K-means, $K=3$ | 0,48 | 18 % | 0,86 | perfiles amplios y estables |
| K-means, $K=4$ | 0,45 | 7 % | 0,72 | separa compras esporádicas |
| Ward, 3 grupos | 0,46 | 16 % | 0,83 | concordancia alta con K-means |
| Ward, 4 grupos | 0,39 | 4 % | 0,58 | rama pequeña sensible |

Los valores son didácticos, no umbrales universales. La solución de tres grupos se prefiere por parsimonia, estabilidad y acuerdo entre métodos. Se caracterizan con medianas e intervalos: “frecuencia alta y composición diversificada”, “frecuencia baja y compras concentradas” y “frecuencia intermedia con mayor variabilidad”. Estos nombres describen las variables observadas, no calidad, rentabilidad ni identidad esencial.

El diagnóstico individual detecta cuentas con silhouette negativa y revisa si son errores, transiciones o fronteras legítimas. Después se repite el ajuste retirando una variable por vez y sobre dos subperiodos. Si el primer grupo persiste pero el tercero cambia mucho, se reportan distintos niveles de confianza.

La conclusión no es “existen tres tipos de clientes”, sino: “bajo esta ventana, representación y métrica, una partición de tres perfiles resume de manera estable los patrones observados y resulta suficiente para comparar escenarios de inventario”. Nuevos periodos requieren reasignación con el transformador conservado y vigilancia de deriva.

## 13.3. Métodos basados en densidad y representaciones neuronales

Los grupos no siempre son compactos ni esféricos. Los métodos de densidad describen regiones con muchas observaciones separadas por regiones escasas y pueden dejar puntos sin asignar. Los mapas autoorganizados, en cambio, aprenden prototipos ordenados sobre una rejilla y facilitan explorar relaciones no lineales. Ambas familias amplían la mirada, pero introducen hiperparámetros y diagnósticos propios.

### 13.3.1. Concepto de densidad

Intuitivamente, una región es densa cuando contiene muchas observaciones en poco volumen. En una esfera de radio $\varepsilon$ alrededor de $\mathbf{x}$,

$$
N_{\varepsilon}(\mathbf{x})=
\{\mathbf{z}:d(\mathbf{x},\mathbf{z})\leq\varepsilon\},
$$

el conteo $|N_{\varepsilon}(\mathbf{x})|$ actúa como estimación local simple. “Muchas” y “poco” dependen de $\varepsilon$, dimensión, escala y métrica. Por eso la densidad no es una propiedad absoluta del registro.

Los métodos basados en densidad separan regiones densas conectadas por zonas de baja densidad. Pueden encontrar anillos, bandas y otras formas no convexas que K-means dividiría. También reconocen ruido. Sin embargo, presentan dificultades cuando los grupos tienen densidades muy distintas: un único radio puede fusionar una región densa o fragmentar otra dispersa.

En alta dimensión, el volumen de una esfera y la concentración de distancias complican la estimación local. Variables irrelevantes diluyen vecindades. Reducir dimensión puede ayudar, pero agrupar únicamente una proyección bidimensional puede fabricar proximidades que no existían en el espacio original. Si se usa una reducción, deben declararse su objetivo, parámetros y pérdida de información.

El concepto de densidad está ligado al mecanismo de muestreo. Una zona con pocos registros puede ser realmente poco activa o estar subobservada. Una región con alta frecuencia puede reflejar duplicación. Antes de interpretar densidad se revisan cobertura y proceso de captura. Los diagnósticos incluyen distribución de distancias al vecino $k$, número de vecinos por punto y estabilidad al variar radio y muestra.

### 13.3.2. DBSCAN

DBSCAN (*Density-Based Spatial Clustering of Applications with Noise*) utiliza dos parámetros: radio $\varepsilon$ y número mínimo de observaciones `minPts`. Un punto es **núcleo** si su vecindad de radio $\varepsilon$ contiene al menos `minPts` observaciones, contando según la convención adoptada. Un punto es **frontera** si no es núcleo pero cae en la vecindad de uno. Un punto es **ruido** si no satisface ninguna condición anterior.

Un punto $q$ es directamente alcanzable por densidad desde un núcleo $p$ si $q\in N_\varepsilon(p)$. La alcanzabilidad por densidad extiende esa relación mediante una cadena de núcleos. Dos puntos pertenecen al mismo grupo si están conectados por densidad. Esta construcción permite seguir formas arbitrarias.

**Pseudocódigo conceptual de DBSCAN**

```text
Entrada: observaciones X, distancia, radio epsilon y minPts
Marcar todas las observaciones como no visitadas
Para cada observación no visitada:
    obtener su vecindad de radio epsilon
    si no alcanza minPts, marcar provisionalmente como ruido
    si es núcleo, iniciar un grupo y expandirlo:
        incorporar vecinos alcanzables
        si un vecino también es núcleo, incorporar su vecindad
Salida: grupos, puntos frontera y puntos etiquetados como ruido
```

La etiqueta de ruido puede cambiar durante la expansión si el punto resulta frontera de un núcleo posterior. En casos donde un punto frontera toca dos grupos, la asignación puede depender del orden de visita, aunque los núcleos conectados sean estables. Conviene distinguir núcleos de fronteras en los resultados.

DBSCAN no exige $K$ y puede dejar observaciones sin grupo. Esto es ventajoso si la noción de ruido tiene sentido. No obstante, imponer que cierto porcentaje sea ruido para obtener una narrativa deseada es una selección circular. La complejidad puede acercarse a $O(n\log n)$ con índices espaciales eficaces en dimensiones moderadas; en alta dimensión o con métricas complejas puede aproximarse a $O(n^2)$.

### 13.3.3. Ruido y formas arbitrarias

El término **ruido** en DBSCAN es una etiqueta geométrica: indica que el punto no está conectado a una región suficientemente densa con los parámetros elegidos. No equivale a error, fraude, evento relevante ni observación prescindible. Un registro correcto de un patrón raro puede ser ruido; un error repetido muchas veces puede formar un grupo denso.

Esta distinción obliga a una investigación posterior. Para cada punto aislado se comprueba integridad, cobertura, unidades, periodo y variables que explican su distancia. Luego se consulta evidencia contextual independiente. Las acciones automáticas basadas solo en la etiqueta deben evitarse, especialmente si afectan a personas o servicios.

La ventaja geométrica puede ilustrarse con dos semicírculos entrelazados. K-means traza fronteras lineales entre centroides y corta ambos arcos. DBSCAN puede recorrer cada arco mediante vecindades locales y recuperar dos componentes. Sin embargo, si puntos espurios forman un puente con separaciones menores que $\varepsilon$, el algoritmo unirá los arcos. Si $\varepsilon$ es demasiado pequeño, fragmentará cada uno.

El porcentaje de ruido es un diagnóstico, no una métrica a maximizar o minimizar. Cero ruido puede indicar un radio tan grande que todo se fusionó. Mucho ruido puede indicar radio pequeño, `minPts` alto, escala deficiente o ausencia real de regiones densas. También se revisan tamaños de grupos y proporción de núcleos frente a fronteras. Un grupo compuesto casi enteramente por fronteras suele ser frágil.

Las observaciones de ruido pueden analizarse colectivamente, pero reagruparlas repetidamente hasta asignarlas a algo contradice el propósito de permitir no asignación. Es preferible mantener una categoría operacional de “sin perfil denso bajo esta configuración” y revisarla con el tiempo.

### 13.3.4. Sensibilidad a parámetros

`minPts` establece la evidencia mínima local. Como regla exploratoria suele relacionarse con la dimensión, pero no existe una fórmula universal. Un valor pequeño acepta cadenas frágiles y grupos diminutos; uno grande exige regiones más pobladas y puede convertir patrones válidos en ruido. El tamaño muestral y la presencia de duplicados influyen en su significado.

Para un `minPts` dado, el gráfico de distancia al vecino $k$ ordena para cada punto la distancia a su vecino correspondiente. Un cambio de pendiente puede sugerir $\varepsilon$. El codo rara vez es inequívoco y no sustituye el conocimiento de escala. Seleccionar visualmente el radio y luego reportar la misma curva como confirmación sobrestima la evidencia.

Se recomienda construir un mapa de sensibilidad sobre una rejilla de valores plausibles. Para cada par $(\varepsilon,\text{minPts})$ se registra número de grupos, proporción de ruido, tamaños, núcleos y similitud con soluciones vecinas. Las **mesetas** donde la estructura cambia poco son más confiables que un punto aislado con una métrica óptima.

El escalado es parte de los parámetros efectivos: multiplicar una variable por diez cambia las vecindades aunque $\varepsilon$ conserve su valor numérico. Por ello, el radio debe expresarse respecto de una representación documentada. También debe repetirse el análisis por submuestras o periodos. Una estructura estable solo ante parámetros, pero no ante nuevas observaciones, sigue siendo débil.

Cuando existen densidades muy variables, puede considerarse una extensión de densidad jerárquica, pero no debe ocultarse que responde a otro algoritmo. Para DBSCAN estándar, la limitación se informa. La respuesta profesional ante la ausencia de un rango estable puede ser concluir que el método no identifica una segmentación defendible, en lugar de forzar parámetros.

### 13.3.5. Mapas autoorganizados

Un mapa autoorganizado o SOM (*Self-Organizing Map*) es una red de prototipos dispuestos normalmente en una rejilla bidimensional. Cada nodo $m$ posee un vector de pesos $\mathbf{w}_m\in\mathbb{R}^p$. Para una observación $\mathbf{x}$ se identifica la unidad de mejor coincidencia, BMU:

$$
c=\arg\min_m\|\mathbf{x}-\mathbf{w}_m\|_2.
$$

Durante el entrenamiento se actualizan la BMU y sus vecinas en la rejilla:

$$
\mathbf{w}_m(t+1)=\mathbf{w}_m(t)+
\alpha(t)h_{cm}(t)[\mathbf{x}(t)-\mathbf{w}_m(t)],
$$

donde $\alpha(t)$ es la tasa de aprendizaje y $h_{cm}(t)$ disminuye con la distancia topológica entre nodos y con el tiempo. Al principio, un vecindario amplio organiza globalmente el mapa; luego uno más estrecho refina prototipos locales.

**Pseudocódigo conceptual de SOM**

```text
Entrada: datos escalados, dimensiones de rejilla y calendario de aprendizaje
Inicializar los vectores prototipo
Para cada época:
    presentar observaciones en orden aleatorio
    localizar la unidad de mejor coincidencia de cada observación
    acercar a la observación la BMU y sus vecinas de rejilla
    reducir tasa de aprendizaje y radio según el calendario
Salida: prototipos, asignaciones a BMU y relaciones de vecindad
```

El SOM realiza cuantización vectorial y busca preservar vecindades aproximadas, no todas las distancias. La rejilla es discreta y puede distorsionar la topología. Su entrenamiento depende de inicialización, tamaño y forma del mapa, tasa, radio y número de épocas. No produce automáticamente grupos: segmentar los prototipos es una etapa adicional que debe validarse.

Es útil para explorar muchas variables mediante componentes sobre una superficie común. No obstante, una visualización atractiva no garantiza fidelidad. Deben reportarse error de cuantización, error topográfico y estabilidad entre entrenamientos.

### 13.3.6. Proyección y visualización de prototipos

Cada nodo del SOM resume las observaciones asignadas y ocupa una posición fija en la rejilla. Un **mapa de componentes** colorea cada nodo según una variable de su prototipo. Comparar mapas permite detectar asociaciones: zonas altas coincidentes en dos componentes sugieren relación en los prototipos, no causalidad.

La **matriz U** representa distancias entre prototipos vecinos. Regiones claras u oscuras, según la convención, pueden señalar fronteras; áreas homogéneas sugieren continuidad. Un mapa de conteos muestra cuántas observaciones caen en cada nodo y revela nodos vacíos o sobrecargados. Las etiquetas externas pueden superponerse solo para validación, dejando claro que no entrenaron el mapa.

Dos medidas básicas son:

$$
E_Q=\frac{1}{n}\sum_{i=1}^{n}
\|\mathbf{x}_i-\mathbf{w}_{c(i)}\|_2,
$$

el error de cuantización, y

$$
E_T=\frac{1}{n}\sum_{i=1}^{n}u_i,
$$

donde $u_i=1$ si la primera y segunda BMU no son vecinas en la rejilla. Un error de cuantización bajo puede obtenerse con muchos nodos y sobreajuste; el error topográfico evalúa otro aspecto. Ambos deben analizarse junto con ocupación y estabilidad.

El tamaño de rejilla controla resolución. Una rejilla pequeña mezcla patrones; una muy grande contiene numerosos nodos vacíos y presenta detalle aparente. Para comparar configuraciones se conservan el preprocesamiento y el protocolo de reinicios. También se alinean mapas, porque rotaciones o reflexiones pueden representar la misma organización.

Si después se agrupan prototipos, las métricas deben ponderar por cantidad de observaciones representadas para que un nodo vacío o poco ocupado no tenga el mismo peso que uno denso. La caracterización final vuelve a las observaciones originales: el prototipo es un resumen, no una unidad real.

### 13.3.7. Ejemplo práctico guiado: detección de zonas de movilidad atípicas

Se analizan zonas de ascenso mediante perfiles de conteos observados por franja, proporción de fin de semana, variabilidad diaria y diversidad de destinos. La unidad es la zona durante un periodo fijo. Antes del análisis se exige cobertura mínima y se separan volumen y composición temporal. No se incorporan atributos demográficos ni se interpretan los resultados como rasgos de quienes habitan una zona.

Los perfiles se escalan de forma robusta y se aplica DBSCAN. El gráfico de vecino $k$ sugiere un intervalo de radios, no un único valor. En una rejilla de sensibilidad aparece una meseta con tres grupos y entre 6 % y 10 % de ruido. Dos grupos permanecen casi intactos; el tercero se fragmenta al reducir el radio. La conclusión debe conservar esa diferencia de confianza.

Las zonas etiquetadas como ruido se auditan una por una:

- cobertura por día y archivo;
- correspondencia válida con el catálogo de zonas;
- volumen total y efecto de la transformación;
- componente de distancia que causa aislamiento;
- persistencia del patrón por mes.

Una zona puede aislarse por una concentración nocturna persistente; otra, por datos presentes solo en parte del periodo. La primera es un perfil operativo infrecuente. La segunda es un problema de comparabilidad y debería excluirse o marcarse, no presentarse como anomalía de movilidad. Una tercera puede dejar de ser ruido con un cambio mínimo de $\varepsilon$ y debe clasificarse como fronteriza.

Se compara luego con K-means. Si K-means asigna todos los casos raros al grupo más cercano, se examinan sus distancias al centro. El desacuerdo ilustra los objetivos: K-means ofrece una partición total; DBSCAN permite expresar que algunas zonas no pertenecen a una región densa. Ninguna etiqueta demuestra un evento ni una causa.

El producto final es una tabla con identificación de zona, etiqueta, condición núcleo/frontera/ruido, variables responsables, estabilidad paramétrica y estado de revisión. Los mapas muestran perfiles de pickups reportados, no intensidad general de movilidad. Toda explicación causal requiere fuentes y diseño adicionales.

### Actividad EMO [MOV-03]: segmentar zonas por patrón de movilidad

**Capacidad mínima:** construir y validar segmentos útiles a partir de variables geotemporales.

**Pregunta realizable.** ¿Qué zonas TLC muestran perfiles semejantes de pickups de taxi amarillo reportados durante febrero, marzo y abril de 2026?

**Fuente y alcance.** Se utilizan los archivos `yellow_tripdata_2026-02.parquet`, `yellow_tripdata_2026-03.parquet` y `yellow_tripdata_2026-04.parquet` de NYC Taxi and Limousine Commission indicados en el Apéndice D, junto con Taxi Zone Lookup y, si se elaboran mapas, Taxi Zone Shapefile. La fila original es un viaje reportado; la unidad de esta actividad es la zona de ascenso `PULocationID`, derivada de agregaciones zona-franja con cortes temporales comunes. La fuente no representa toda la movilidad, demanda insatisfecha, vehículos libres ni actividad total de cada zona.

**Preparación común.** Antes de formar perfiles se aplican las reglas del Apéndice D: pickup dentro del periodo declarado; drop-off posterior cuando se usa duración; distancia no negativa revisada junto con duración; zonas presentes en el lookup o marcadas como desconocidas; control de filas, faltantes, proveedor y mes; revisión de coincidencias en claves compuestas sin eliminación automática; zona horaria y franjas idénticas. Las zonas con cobertura insuficiente se excluyen con una regla previa o se mantienen marcadas fuera del ajuste. Toda exclusión informa cantidad y sensibilidad.

**Variables derivadas mínimas por zona:**

- pickups medios por hora;
- proporción de pickups en mañana, tarde, noche y madrugada, con cortes documentados;
- proporción de fin de semana;
- variabilidad entre días;
- cantidad de destinos distintos o entropía OD;
- duración o distancia mediana de viajes originados, tras controles de validez.

Las cuatro proporciones de franja son composicionales y suman uno; el equipo debe reconocer su redundancia y justificar cómo las representa. Volumen y forma temporal se analizan por separado o se ponderan explícitamente. `Borough`, `Zone` y `service_zone` sirven para identificación y caracterización, no deben dominar la formación de grupos por codificación arbitraria.

**Consigna.** Definir características comparables por zona, aplicar al menos dos estrategias de agrupamiento y caracterizar los segmentos según demanda observada, temporalidad, diversidad de destinos u otra dimensión operativa permitida. Una comparación válida podría enfrentar K-means con jerárquico sobre una representación euclídea común, o K-means con DBSCAN explicando que el segundo admite ruido. No es suficiente ejecutar dos algoritmos con sus valores predeterminados.

**Protocolo mínimo:**

1. construir una tabla reproducible de una fila por zona y mostrar cobertura;
2. auditar distribuciones, faltantes, extremos, correlaciones y bloques de variables;
3. ajustar escalado dentro del pipeline y justificar métrica y ponderación;
4. explorar hiperparámetros en rangos razonables, sin usar una sola métrica como respuesta;
5. comparar inercia cuando corresponda, silhouette, Davies-Bouldin, tamaños y casos fronterizos;
6. medir variabilidad por inicialización y estabilidad por remuestreo o por mes;
7. caracterizar cada segmento con estadísticas robustas y perfiles horarios;
8. revisar zonas inestables, sin correspondencia y etiquetadas como ruido;
9. documentar elección, alternativas descartadas y límites.

**Estabilidad temporal.** Una opción es ajustar la definición y el transformador en febrero-marzo, asignar o reevaluar abril y comparar perfiles. Otra es repetir todo el procedimiento por mes y emparejar grupos según centroides o coasignación. La etiqueta numérica no tiene identidad: el “grupo 1” de dos ejecuciones no se compara por número, sino por composición o prototipo. Debe distinguirse estabilidad de centroides, de miembros y de caracterización.

**Ficha interpretativa obligatoria por segmento:**

| Campo | Contenido esperado |
|---|---|
| Nombre descriptivo | Patrón observable, por ejemplo “volumen alto con concentración diurna” |
| Tamaño | Número y proporción de zonas |
| Perfil central | Medianas, intervalos y perfil temporal |
| Diferencias | Variables que lo separan, con magnitud |
| Variabilidad interna | Dispersión y observaciones fronterizas |
| Estabilidad | Inicialización, remuestreo y meses |
| Cobertura | Registros y periodos representados |
| Uso posible | Insumo descriptivo para pronóstico o prioridad didáctica |
| Límite | Qué no puede inferirse de ese segmento |

**Modalidad de trabajo:** definición común de variables; ajuste, validación e interpretación individuales.

**Evidencia individual:** notebook con preprocesamiento, selección razonada de hiperparámetros, visualización de grupos, análisis de estabilidad y ficha interpretativa de cada segmento. El capítulo desarrolla teoría y pseudocódigo; la implementación reproducible corresponde a la actividad.

**Criterios de aprobación:**

- las escalas y métricas son coherentes con las variables;
- la selección de grupos combina métricas, estabilidad y utilidad;
- las dos estrategias se comparan bajo un protocolo defendible;
- zonas con cobertura insuficiente y ruido reciben tratamiento explícito;
- la interpretación no confunde separación algorítmica con categorías reales;
- nombres, mapas y conclusiones describen exclusivamente perfiles operativos de pickups reportados.

**Restricción interpretativa.** Los grupos son perfiles algorítmicos de viajes de taxi amarillo observados, no categorías socioeconómicas de barrios, residentes, pasajeros o conductores. No se permiten inferencias sobre ingreso, vulnerabilidad, necesidad social, seguridad, calidad urbana ni composición demográfica. `Borough` y `Zone` localizan y describen cobertura; no explican causalmente los grupos. Cualquier extensión contextual requiere una fuente, una especificación y una pregunta nuevas.

**Aporte al laboratorio:** define perfiles de zonas que podrán utilizarse como insumo en el pronóstico y en una regla didáctica de prioridad. No constituye una optimización de flota porque los datos no observan oferta disponible ni ubicación de vehículos libres.

## 13.4. Evaluación, interpretación y anomalías

Evaluar clustering requiere triangular evidencia. Las métricas internas usan la misma geometría que generó los grupos y pueden premiar sus supuestos. La evaluación externa compara con información independiente, pero una referencia puede ser incompleta o responder a otra pregunta. La estabilidad estudia cuánto cambia el resultado. La caracterización y la utilidad determinan si las diferencias pueden explicarse y usarse responsablemente.

### 13.4.1. Inercia

La inercia de K-means es su función objetivo:

$$
W_K=\sum_{k=1}^{K}\sum_{i\in C_k}
\|\mathbf{x}_i-\boldsymbol{\mu}_k\|_2^2.
$$

Mide dispersión cuadrática dentro de grupos en el espacio transformado. Un valor menor indica que los centroides resumen mejor las observaciones bajo esa geometría. No posee escala universal: cambia con unidades, cantidad de observaciones, dimensión y varianza. Solo es comparable entre soluciones sobre exactamente los mismos datos y preprocesamiento.

$W_K$ nunca aumenta al incrementar $K$. El cociente o reducción $W_{K-1}-W_K$ puede mostrar rendimientos decrecientes. En el gráfico del codo se busca una transición entre mejora sustancial y refinamiento pequeño. Si la curva es suave, no debe inventarse un quiebre. Métodos geométricos para detectar el codo formalizan una heurística, no convierten la curva en verdad.

La inercia favorece grupos compactos y penaliza fuertemente extremos. Puede preferir subdividir una nube grande antes que representar un grupo pequeño separado. Tampoco evalúa separación directamente: dos centroides cercanos podrían producir baja dispersión si los grupos son muy compactos. Una inercia baja con un grupo de una observación no implica una segmentación útil.

Se recomienda reportar la distribución de inercia entre reinicios, no solo el mínimo. Una dispersión amplia revela sensibilidad de optimización. También puede normalizarse descriptivamente por inercia total respecto de la media global:

$$
R^2_K=1-\frac{W_K}{T},\qquad
T=\sum_i\|\mathbf{x}_i-\bar{\mathbf{x}}\|^2,
$$

interpretándola como proporción de dispersión representada, no como desempeño predictivo. Su aumento monotónico mantiene el problema de selección.

### 13.4.2. Coeficiente Silhouette

Para una observación $i$, sea $a(i)$ la distancia media a las demás observaciones de su grupo. Sea $b(i)$ la menor distancia media desde $i$ a cualquier otro grupo. El coeficiente silhouette es

$$
s(i)=\frac{b(i)-a(i)}{\max\{a(i),b(i)\}}.
$$

Toma valores entre $-1$ y 1. Valores cercanos a 1 sugieren buena cohesión y separación; alrededor de cero indican frontera; negativos señalan que, en promedio, la observación está más cerca de otro grupo. Para un grupo unitario suele definirse $s(i)=0$ por convención.

La media $\bar{s}$ resume una solución, pero oculta heterogeneidad. Un gráfico por grupo ordena silhouettes individuales y muestra grupos compactos, solapados o pequeños. Deben reportarse media, mediana, proporción negativa y distribución por grupo. Una media alta impulsada por un grupo grande no compensa necesariamente otro incoherente.

Silhouette depende de la métrica y tiende a favorecer grupos convexos y bien separados. Puede penalizar estructuras de densidad no convexas que son válidas para DBSCAN. Para soluciones con ruido hay varias convenciones: excluir el ruido, tratarlo como grupo o asignar cero. Cada una responde algo distinto y debe declararse; excluir muchos puntos puede inflar artificialmente la cifra.

La métrica puede orientar el diagnóstico. Observaciones con $s(i)<0$ se revisan como fronterizas, errores potenciales o transiciones. Comparar silhouette bajo la métrica de formación y una métrica alternativa defendible informa sensibilidad. No es correcto elegir representación y $K$ explorando muchas opciones y presentar el máximo como si proviniera de una prueba independiente.

### 13.4.3. Índice Davies-Bouldin

El índice Davies-Bouldin compara dispersión de grupos con separación entre representantes. Sea

$$
S_k=\frac{1}{|C_k|}\sum_{i\in C_k}
\|\mathbf{x}_i-\boldsymbol{\mu}_k\|_2
$$

la dispersión del grupo $k$, y $M_{kl}=\|\boldsymbol{\mu}_k-\boldsymbol{\mu}_l\|_2$ la distancia entre centroides. Entonces

$$
DB=\frac{1}{K}\sum_{k=1}^{K}
\max_{l\neq k}\frac{S_k+S_l}{M_{kl}}.
$$

Valores menores son preferibles: indican dispersiones pequeñas respecto de la separación. El máximo selecciona para cada grupo su rival más problemático. Examinar esos pares aporta más información que la media final: revela qué segmentos se confunden.

El índice no tiene un umbral universal y solo compara soluciones sobre la misma representación. Favorece grupos aproximadamente esféricos descritos por centroides. Puede valorar mal formas arbitrarias y es sensible a extremos. Si dos centroides coinciden, el denominador plantea un caso degenerado que señala una partición problemática.

Davies-Bouldin y silhouette no son pruebas independientes de la representación: ambos reutilizan distancias. Pueden discrepar porque resumen cohesión y separación de modo distinto. Frente a una discrepancia se inspeccionan tamaños, pares rivales y observaciones fronterizas; no se promedian métricas sin fundamento. Una tabla multicriterio conserva direcciones: inercia y Davies-Bouldin se minimizan; silhouette se maximiza.

La selección responsable no consiste en buscar la fila que gana todas las columnas. Puede no existir. Se identifican soluciones dominadas, se conserva un conjunto de candidatas y se decide según estabilidad, interpretabilidad y uso. Las diferencias pequeñas entre valores no deberían presentarse como decisivas sin cuantificar variabilidad por remuestreo.

### 13.4.4. Evaluación externa

La evaluación externa compara la partición con etiquetas o relaciones que no determinaron el ajuste. No supone que las etiquetas sean la verdad del clustering: pueden representar otra taxonomía. Su valor radica en responder si la estructura recupera una referencia relevante.

Una tabla de contingencia $n_{kr}$ cruza grupo $k$ y clase externa $r$. La **pureza** asigna a cada grupo su clase mayoritaria:

$$
\operatorname{pureza}=\frac{1}{n}\sum_k\max_r n_{kr}.
$$

Es fácil de interpretar, pero aumenta al crear más grupos y alcanza uno con grupos unitarios. No corrige coincidencia aleatoria.

El índice de Rand considera pares juntos o separados en ambas particiones. Su versión ajustada, ARI, corrige el acuerdo esperado por azar y suele tomar valor 0 bajo acuerdo aleatorio, 1 en coincidencia perfecta y a veces valores negativos. La información mutua normalizada compara dependencia entre etiquetas con normalizaciones que deben especificarse. Estas medidas son invariantes a permutar nombres de grupos, propiedad indispensable porque las etiquetas numéricas son arbitrarias.

También puede existir evaluación externa sin clases. Expertos pueden juzgar pares “deberían estar juntos” o “deberían estar separados”; eventos posteriores pueden evaluar si los segmentos anticipan comportamientos sin haberlos usado para formarlos. Se debe evitar fuga: si la variable externa entró en la distancia, ya no valida externamente.

Una referencia imperfecta exige análisis de desacuerdos. Un ARI moderado puede indicar que el algoritmo encontró subestructura útil o que la representación ignoró una distinción importante. La matriz de contingencia y ejemplos concretos aclaran cuál. Si se prueban numerosas referencias y solo se reporta la más favorable, se incurre en selección oportunista.

La validez externa no autoriza causalidad. Que un grupo coincida con una categoría administrativa solo demuestra asociación bajo la muestra. Además, cualquier uso sensible requiere examinar impacto, representatividad y legitimidad de las variables, no solo acuerdo numérico.

### 13.4.5. Caracterización de clusters

Caracterizar significa describir qué distingue a cada grupo y cuánta heterogeneidad contiene. El perfil incluye tamaño, medidas centrales, dispersión, distribuciones y observaciones representativas. Para variables asimétricas se prefieren mediana y cuantiles; para proporciones se informa su estructura conjunta; para categorías, frecuencias con denominadores.

Conviene separar tres conjuntos de variables:

- **formación**, utilizadas por el algoritmo;
- **caracterización**, reservadas para comprender los grupos;
- **resultado**, observadas después y usadas para evaluación prospectiva cuando sea legítimo.

Las diferencias en variables de formación son esperables y no constituyen descubrimiento independiente. Una variable de caracterización puede aportar contexto, pero si se examinan cientos aparecerán asociaciones por azar. Deben informarse magnitudes y, cuando corresponda, incertidumbre y corrección por multiplicidad, no solo significación.

Los centroides son útiles, pero el promedio puede no representar a nadie. Se pueden presentar medoides, observaciones reales con menor distancia media a su grupo, junto con casos fronterizos. Un nombre como “grupo 2” es neutral pero poco informativo; uno como “frecuencia alta y variabilidad baja” es descriptivo. Etiquetas como “buenos”, “problemáticos” o “vulnerables” añaden juicios no contenidos en los datos.

Una ficha de segmento debería responder: qué observaciones contiene, qué variables lo distinguen, cuánto se solapa, qué tan estable es, qué casos no representa y para qué decisión podría servir. Visualizaciones recomendables son perfiles normalizados con intervalos, distribuciones completas y mapas solo cuando la dimensión espacial tenga sentido. Los ejes deben conservar unidades interpretables además de valores estandarizados.

La caracterización debe repetirse en submuestras o periodos. Un grupo cuya descripción cambia aunque sus etiquetas parezcan estables puede haber sufrido deriva interna. Por el contrario, centroides similares con miembros intercambiables pueden seguir siendo útiles para una política agregada. Estabilidad de miembros y estabilidad de perfil son propiedades distintas.

### 13.4.6. Detección no supervisada de anomalías

Una anomalía es una observación incompatible con un patrón de referencia bajo una representación, escala y contexto. Puede ser **global**, alejada del conjunto; **contextual**, extraña dadas condiciones como hora o estación; o **colectiva**, normal individualmente pero inusual como secuencia o grupo. La definición debe preceder al método.

Una puntuación simple basada en centro es

$$
A_i=\|\mathbf{x}_i-\boldsymbol{\mu}_{c_i}\|,
$$

pero solo detecta desviaciones respecto de grupos compactos. La distancia robusta de Mahalanobis incorpora covarianza:

$$
D_M(\mathbf{x})=
\sqrt{(\mathbf{x}-\boldsymbol{\mu})^{\mathsf T}
\Sigma^{-1}(\mathbf{x}-\boldsymbol{\mu})},
$$

aunque requiere estimación estable y es sensible si media y covarianza no son robustas. DBSCAN etiqueta puntos fuera de regiones densas, y otros métodos usan densidad local, aislamiento o error de reconstrucción. Sus puntuaciones no son intercambiables.

Elegir un umbral define la carga de revisión y el balance entre omisiones y falsas alarmas. Sin etiquetas, puede usarse una cuota operativa o cuantiles, pero esto garantiza una cantidad, no una tasa de error. Si existe una muestra auditada, precisión entre los primeros casos, cobertura y tiempo de detección son más relevantes.

El flujo recomendado separa **detección** de **decisión**. Primero se genera una puntuación; luego se verifica calidad, se busca contexto, se registra una resolución humana y se retroalimenta el sistema. Nunca se borran observaciones automáticamente porque sean raras. Los errores repetidos pueden ser densos y pasar inadvertidos, mientras casos válidos poco frecuentes pueden aparecer arriba.

La estabilidad de ranking se evalúa ante transformaciones, ventanas y remuestreo. Una anomalía persistente con explicación consistente merece mayor prioridad que un caso que oscila cerca del umbral. También debe vigilarse deriva: si el patrón normal cambia, un umbral histórico pierde significado.

### 13.4.7. Riesgos de sobreinterpretación

El primer riesgo es la **reificación**: tratar grupos calculados como entidades naturales. Los límites pueden ser continuos y depender de $K$. El segundo es la **causalidad espuria**: una separación describe asociación, no su mecanismo. El tercero es la **falacia ecológica**: atribuir a individuos propiedades observadas en unidades agregadas. El cuarto es convertir falta de cobertura en comportamiento.

Otros riesgos incluyen:

- escoger retrospectivamente la representación que confirma una expectativa;
- asignar nombres valorativos o estigmatizantes;
- ocultar observaciones fronterizas detrás de una etiqueta única;
- confundir alta estabilidad con relevancia: una división trivial por volumen puede ser estable;
- confundir baja estabilidad con inutilidad: una frontera continua puede requerir puntuaciones en vez de grupos;
- aplicar segmentos fuera del periodo o población de ajuste sin evaluar deriva;
- usar pertenencia grupal como sustituto de variables que no fueron observadas.

Las visualizaciones también engañan. Una proyección en dos dimensiones puede separar puntos que estaban cercanos o superponer los lejanos. Colores categóricos acentúan fronteras aunque las transiciones sean graduales. Deben acompañarse con métricas en el espacio de modelado y advertencias de proyección.

En aplicaciones con consecuencias, la agrupación puede crear bucles: una decisión basada en un segmento cambia la observación futura y parece confirmar el segmento. Se requiere registro de intervenciones y reevaluación. También se examina si variables proxy producen impactos desiguales, incluso cuando no se incluyeron atributos sensibles.

Una redacción prudente usa expresiones condicionales: “en los datos observados”, “bajo esta representación” y “el perfil se caracteriza por”. Declara incertidumbre, cobertura y alternativas. El objetivo no es debilitar el resultado, sino hacer explícito exactamente qué evidencia aporta.

### 13.4.8. Ejemplo práctico guiado: validación de una segmentación

Retomemos una segmentación de perfiles operativos con cuatro soluciones candidatas: K-means con tres o cuatro grupos y jerárquico con tres o cuatro. La validación se realiza sin seleccionar primero la opción visualmente más atractiva.

**Paso 1: integridad y representación.** Se verifica unidad de análisis, periodo, faltantes, transformaciones y contribución de bloques. Se repite con escalado estándar y robusto. Si una variable domina más de la mitad de la distancia en la mayoría de pares, se revisa su peso.

**Paso 2: evaluación interna.** Se calculan inercia para K-means, silhouette y Davies-Bouldin para las cuatro alternativas. Se observan distribuciones por grupo y pares rivales. Las diferencias pequeñas se consideran empates prácticos hasta estudiar variabilidad.

**Paso 3: estabilidad algorítmica.** Cada K-means se reinicia muchas veces. Se comparan inercias y ARI entre corridas después de alinear particiones implícitamente mediante una medida invariante. Una solución cuya mejor corrida es excepcional pero rara no se considera robusta.

**Paso 4: estabilidad muestral y temporal.** Se remuestrean observaciones, se reajusta todo el pipeline y se calcula una matriz de coasignación. Luego se repite por periodos. Se examinan estabilidad de miembros, centroides y fichas, no solo un promedio.

**Paso 5: caracterización ciega a nombres.** Se elaboran perfiles con medianas, cuantiles y tamaños antes de asignar etiquetas narrativas. Expertos del proceso valoran si las diferencias son comprensibles y relevantes, sin conocer qué algoritmo produjo cada opción.

**Paso 6: casos problemáticos.** Se revisan silhouettes negativas, grupos diminutos y observaciones que cambian frecuentemente. Estas unidades pueden recibir una puntuación de pertenencia o marca fronteriza en vez de una asignación tajante.

Supóngase que cuatro grupos mejora levemente silhouette, pero uno contiene 3 % de observaciones, cambia mucho por periodo y no posee descripción estable. La solución de tres grupos presenta métricas apenas inferiores, coasignación más nítida y perfiles reproducibles. Se elige tres por parsimonia y estabilidad, dejando constancia de que la cuarta división es una hipótesis exploratoria.

El informe final contiene una tabla de evidencia, fichas, análisis de sensibilidad, lista de casos no representados y condiciones de actualización. La conclusión evita decir que las métricas “demuestran” tres grupos: sostiene que, entre las alternativas evaluadas, tres ofrece el compromiso más defendible para el uso declarado.

## Síntesis

El aprendizaje no supervisado no elimina la necesidad de formular una pregunta; la hace más visible. La unidad de análisis, las variables, el escalado y la métrica definen qué significa semejanza. K-means resume grupos compactos mediante centroides y exige atender a inicialización, mínimos locales y elección de $K$. El clustering jerárquico muestra estructuras anidadas cuya forma depende del enlace. DBSCAN busca conectividad por densidad, admite ruido y requiere estudiar sensibilidad a $\varepsilon$ y `minPts`. Los SOM organizan prototipos en una rejilla y necesitan diagnósticos de cuantización, topología y estabilidad.

Ninguna métrica basta por sí sola. Inercia disminuye al aumentar grupos; silhouette y Davies-Bouldin incorporan supuestos geométricos; una referencia externa puede responder a otra taxonomía. La validación combina evidencia interna, estabilidad algorítmica, remuestreo, repetición temporal, caracterización y utilidad. Una anomalía es relativa al contexto y activa investigación, no una eliminación automática.

La principal competencia es sostener una conclusión proporcional a la evidencia: describir patrones sin esencializarlos, reconocer casos fronterizos y declarar dónde deja de ser válida la solución.

## Glosario

**Agrupamiento o clustering:** proceso de organizar observaciones según una noción explícita o implícita de semejanza.

**Anomalía contextual:** observación inusual dadas ciertas condiciones, aunque pueda ser normal en otro contexto.

**BMU:** unidad del mapa autoorganizado cuyo prototipo está más cerca de una observación.

**Centroide:** media vectorial de las observaciones de un grupo; no tiene que ser una observación real.

**Coasignación:** frecuencia con que dos observaciones aparecen en el mismo grupo a través de ejecuciones.

**Conectividad por densidad:** relación que une puntos mediante cadenas de vecindades densas.

**Dendrograma:** árbol que representa fusiones o divisiones y sus alturas de disimilitud.

**Distancia:** función que cuantifica diferencia; su elección expresa una hipótesis sobre semejanza.

**Enlace:** regla para calcular disimilitud entre grupos en clustering jerárquico.

**Estabilidad:** grado de conservación de una solución ante semillas, muestras, periodos o decisiones plausibles de modelado.

**Grupo frontera:** expresión descriptiva para observaciones con pertenencia inestable o cercanía comparable a varios grupos.

**Inercia:** suma de distancias euclídeas al cuadrado entre observaciones y centroides en K-means.

**Medoide:** observación real que representa un grupo por su posición central según una disimilitud.

**Métrica interna:** criterio calculado con datos y partición, sin referencia externa.

**Prototipo:** vector que resume una región del espacio, como un centroide o nodo de SOM.

**Ruido en DBSCAN:** punto no conectado a una región densa bajo parámetros dados; no equivale necesariamente a error.

**Silhouette:** medida individual de cohesión respecto del grupo propio y separación respecto del grupo alternativo más próximo.

## Preguntas de revisión

1. ¿Por qué la selección de variables y el escalado forman parte del modelo no supervisado?
2. ¿En qué situación Manhattan y Euclídea pueden producir vecinos diferentes? Construya un ejemplo.
3. ¿Qué información ignora la similitud coseno y cuándo podría ser importante conservarla?
4. ¿Por qué codificar una categoría nominal mediante enteros puede fabricar distancias?
5. ¿Qué significa asignar pesos iguales a variables estandarizadas? ¿Es siempre deseable?
6. Explique por qué K-means converge sin garantizar el óptimo global.
7. ¿Qué diferencia existe entre variabilidad por semilla y estabilidad por remuestreo?
8. ¿Por qué la inercia no selecciona por sí sola el número de grupos?
9. Compare el efecto de enlace simple, completo, promedio y Ward ante un punto extremo.
10. ¿Qué información del dendrograma cambia al rotar una rama y cuál permanece?
11. Distinga punto núcleo, frontera y ruido en DBSCAN.
12. ¿Por qué un único $\varepsilon$ puede fallar cuando las densidades son muy distintas?
13. ¿Qué representan el error de cuantización y el error topográfico de un SOM?
14. ¿Cómo puede una proyección bidimensional inducir una interpretación errónea de separación?
15. ¿Por qué silhouette y Davies-Bouldin no son evidencia independiente de la representación?
16. ¿En qué se diferencian pureza y Rand ajustado frente al aumento del número de grupos?
17. Proponga una ficha de segmento que exprese incertidumbre y casos fronterizos.
18. ¿Por qué una etiqueta de ruido no autoriza a eliminar una observación?
19. Distinga estabilidad de miembros, estabilidad de centroides y estabilidad de caracterización.
20. ¿Qué afirmaciones están prohibidas al interpretar los segmentos de `MOV-03` y por qué?

## Actividad integradora del capítulo

Diseñe, sin implementar, un protocolo de segmentación para un conjunto de unidades descritas por dos variables numéricas, una ordinal, una nominal y una proporción temporal. El documento debe contener:

1. pregunta, unidad de análisis, cobertura y uso previsto;
2. tratamiento de faltantes y codificación de cada tipo de variable;
3. dos representaciones alternativas y la hipótesis de semejanza de cada una;
4. selección justificada de dos algoritmos entre K-means, jerárquico, DBSCAN y SOM;
5. pseudocódigo del flujo completo, desde auditoría hasta caracterización;
6. plan de selección de hiperparámetros sin depender de una única métrica;
7. evaluación de estabilidad ante semillas, remuestreo y un cambio plausible de escala;
8. estrategia para observaciones fronterizas y anomalías;
9. ficha de segmentos con nombres puramente descriptivos;
10. tres límites interpretativos y una condición que obligaría a reajustar el modelo.

La evaluación prioriza coherencia entre pregunta, representación y algoritmo; calidad de diagnósticos; capacidad para distinguir estructura de artefactos; y prudencia de las conclusiones. Una respuesta excelente puede concluir que ninguna partición es suficientemente estable si sustenta esa decisión con evidencia.
