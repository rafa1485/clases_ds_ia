<meta charset="UTF-8">
<style>
@page { size: A4; margin: 14mm 15mm 15mm 15mm; }
body { font-family: "DejaVu Sans", sans-serif; color: #17324d; line-height: 1.3; font-size: 9.5pt; }
h1 { color: #17324d; border-bottom: 4px solid #007f82; padding-bottom: 8px; }
h2 { color: #17324d; border-bottom: 2px solid #e2a33a; padding-bottom: 4px; margin: 15px 0 6px; page-break-after: avoid; }
h3 { color: #007f82; margin: 10px 0 3px; page-break-after: avoid; }
p { margin: 5px 0; }
ul, ol { margin-top: 3px; margin-bottom: 6px; }
blockquote { border-left: 4px solid #e2a33a; background: #f3f6f8; margin: 9px 0; padding: 7px 11px; page-break-inside: avoid; }
table { border-collapse: collapse; width: 100%; font-size: 8.7pt; page-break-inside: avoid; }
th { background: #17324d; color: white; }
th, td { border: 1px solid #aab7c1; padding: 5px; vertical-align: top; }
code { color: #007f82; }
pre { background: #f3f6f8; border: 1px solid #aab7c1; padding: 8px; white-space: pre-wrap; page-break-inside: avoid; }
strong { color: #17324d; }
.formula { text-align: center; font-size: 12pt; background: #f3f6f8; border: 1px solid #aab7c1; padding: 7px; page-break-inside: avoid; }
</style>

# Trabajo práctico: probabilidad y decisiones

**Curso:** Data Science<br>
**Semana y clase:** semana 4, clase 4<br>
**Dataset:** Bank Marketing, archivo `bank.csv`<br>
**Modalidad:** individual
**Duración estimada:** 60 a 90 minutos

## Propósito

En este trabajo vas a estimar la proporción de suscripciones registrada en una campaña bancaria, observar cómo cambia esa estimación entre muestras y usarla en una decisión sencilla.

La pregunta central es:

> **¿Qué proporción de los registros terminó en suscripción y cuánto cambia esa estimación al trabajar con distintas muestras?**

El recorrido será: `datos → proporción observada → variabilidad → decisión`.

## 1. Preparar los datos

El dataset reúne resultados de campañas telefónicas de una institución bancaria portuguesa. La variable `y` indica si el cliente contrató un depósito a plazo y `campaign` informa la cantidad de contactos realizados durante la campaña actual para ese cliente.

1. Ingresá al [enlace directo de descarga](https://archive.ics.uci.edu/static/public/222/bank+marketing.zip).
2. Descargá y extraé los archivos hasta ubicar `bank.csv`.
3. Cargá el archivo con pandas:

```python
import pandas as pd

datos = pd.read_csv("bank.csv", sep=";")
```

4. Confirmá que la tabla tenga **4.521 filas y 17 columnas**.
5. Mostrá las primeras filas y los tipos de datos.

Registrá en una celda de texto:

| Elemento | Definición para este trabajo |
|---|---|
| Unidad de análisis | un registro de cliente dentro de la campaña |
| Población registrada | los registros incluidos en `bank.csv` |
| Evento de interés, S | el registro tiene `y = "yes"` |
| Denominador | registros con un valor válido en `y` |

> `bank.csv` es una muestra aleatoria del 10 % de `bank-full.csv`. En este práctico, la proporción de todo `bank.csv` será la referencia observada para comparar las muestras más pequeñas.

## 2. Revisar y describir

Realizá una revisión inicial:

- informá la cantidad de filas duplicadas;
- contá los valores faltantes por columna.

Después describí las variables `y` y `campaign`.

### Variable `y`

1. Calculá la frecuencia absoluta de `yes` y `no`.
2. Calculá sus porcentajes.
3. Construí un gráfico de barras con título, nombres de ejes y valores visibles.

### Variable `campaign`

1. Informá mínimo, primer cuartil, mediana, tercer cuartil y máximo.
2. Construí un histograma.
3. Escribí una frase sobre la forma de la distribución y sus valores más altos.

## 3. Calcular la proporción observada

Sea **S** el evento “el registro terminó en suscripción”. Calculá:

<p class="formula">P(S) = cantidad de registros con y = "yes" / cantidad de registros válidos</p>

Calculá también la proporción complementaria:

<p class="formula">P(S<sup>c</sup>) = 1 - P(S)</p>

Presentá cada resultado como decimal y porcentaje. Acompañalo con su numerador y denominador, por ejemplo: `521 / 4521 = 0,1152 = 11,52 %`.

Comprobá que ambas proporciones sumen 1.

## 4. Observar la variabilidad entre muestras

Tomá cinco muestras aleatorias de 300 registros, sin reemplazo, usando las semillas `1, 2, 3, 4 y 5`.

Esta instrucción produce una muestra reproducible:

```python
muestra = datos.sample(n=300, replace=False, random_state=semilla)
```

Construí una tabla con este formato:

| Semilla | Suscripciones | Tamaño de muestra | Proporción |
|---:|---:|---:|---:|
| 1 | | 300 | |
| 2 | | 300 | |
| 3 | | 300 | |
| 4 | | 300 | |
| 5 | | 300 | |

Luego respondé:

1. ¿Cuál fue la proporción mínima y cuál fue la máxima?
2. ¿Cuál fue la diferencia entre ambas?
3. ¿Qué muestra quedó más cerca de la proporción observada en todo `bank.csv`?
4. ¿Por qué las cinco estimaciones pueden ser distintas aunque provengan del mismo archivo?

## 5. Tomar una decisión sencilla

Considerá este escenario didáctico para una campaña futura:

- realizar un contacto cuesta **1 unidad**;
- una suscripción genera un beneficio de **12 unidades**;
- la proporción observada en `bank.csv` se usa como referencia inicial.

Antes de realizar el piloto, el **valor esperado neto por contacto** representa la ganancia promedio estimada para cada contacto. El beneficio esperado es `12 × P(S)` y a ese valor se le resta el costo de 1 unidad del contacto:

<p class="formula">valor esperado = 12 × P(S) - 1</p>

1. Calculá el valor esperado neto por contacto y explicá el resultado con una frase.
2. ¿Cuál es el valor esperado neto para una prueba piloto de 100 contactos?
3. Según el resultado calculado, indicá si realizarías la prueba piloto y justificá tu respuesta.

## 6. Cierre

Redactá un cierre breve con tres puntos:

1. la proporción de suscripción observada, con numerador y denominador;
2. la variación encontrada entre las cinco muestras;
3. la decisión propuesta y el supuesto principal que la sostiene.

Las conclusiones deben referirse a los registros analizados y utilizar expresiones como “se observa” o “la muestra indica”.

## Producto esperado

Entregá un notebook ejecutable que incluya:

- identificación del estudiante y fuente de los datos;
- carga y revisión inicial;
- gráfico de barras de `y`;
- resumen e histograma de `campaign`;
- cálculo de la proporción y su complemento;
- tabla de las cinco muestras;
- cálculo del valor esperado;
- cierre en tres puntos.

**Referencia:** Moro, S., Rita, P. y Cortez, P. (2014). *Bank Marketing*. UCI Machine Learning Repository. [https://doi.org/10.24432/C5K306](https://doi.org/10.24432/C5K306). Licencia CC BY 4.0.
