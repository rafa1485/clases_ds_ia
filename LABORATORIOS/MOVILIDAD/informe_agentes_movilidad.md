# Trabajo Práctico: Agentes Reactivos para Refuerzo de Taxis

## 1. Objetivo

El objetivo de este trabajo es programar y comparar un agente reactivo simple y un agente reactivo basado en modelo.

Ambos agentes deben recomendar si una empresa ficticia X debería considerar reforzar con más taxis una zona Z durante la hora siguiente (`h+1`).

El trabajo se centra en reglas condición-acción, percepción, estado interno, dependencia de la historia, causalidad temporal y trazabilidad de las decisiones. No busca construir un predictor de demanda ni optimizar una flota real.


## 2. Escenario utilizado

Para las pruebas se utilizó el escenario reproducible indicado en la consigna:

- Zona TLC: `161`
- Zona: `Midtown Center`
- Hora de decisión: `8`
- Taxis de X: `20`
- Horas de historia: `3`
- Semilla: `42`

El entorno genera viajes a partir de datos de Yellow Taxi TLC y realiza una división sintética entre la empresa ficticia X y otras empresas.

La proporción `tasa_otras_simulada` se genera de manera aleatoria, acotada e inversamente proporcional al número de taxis de X. Esta relación es una hipótesis didáctica y no representa el comportamiento real de ninguna empresa.


## 3. Percepción

La entrada de los agentes es el archivo `percepciones.csv`.

Cada fila representa una observación horaria y contiene información como:

- `zona_id`: identificador TLC de la zona.
- `zona`: nombre de la zona.
- `hora`: hora observada.
- `taxis_x`: cantidad de taxis de X.
- `demanda_total`: viajes simulados con pickup en la zona.
- `tasa_otras_simulada`: proporción sintética para otras empresas.
- `viajes_otras`: viajes asignados a otras empresas.
- `demanda_x`: viajes asignados a X.
- `capacidad_x`: capacidad simplificada de la flota de X.
- `viajes_atendibles_x`: viajes que X podría atender con su capacidad.
- `demanda_no_cubierta_x`: diferencia positiva entre demanda y capacidad.
- `presion`: cociente entre `demanda_x` y `capacidad_x`.

Para este trabajo se supone que cada taxi aporta una unidad de capacidad por hora y que la flota se mantiene constante.


## 4. Acciones posibles

Los agentes pueden producir tres acciones:

### `NO_REFORZAR`

La política no encuentra evidencia suficiente para recomendar más taxis.

### `RECOMENDAR_REFUERZO`

Se aconseja que una persona considere reforzar la zona en `h+1`.

### `ABSTENERSE`

La percepción es inválida o no permite aplicar la política con seguridad.

La recomendación no ejecuta ningún traslado ni despacho de taxis. Es un mensaje destinado a una persona responsable de tomar la decisión.


# 5. Agente reactivo simple

El agente reactivo simple utiliza exclusivamente la percepción actual.

Las reglas implementadas son:

| Condición | Acción |
|---|---|
| Faltan datos requeridos, existen valores inválidos o la capacidad es desconocida | `ABSTENERSE` |
| `presion >= 0.85` | `RECOMENDAR_REFUERZO` |
| `presion < 0.85` | `NO_REFORZAR` |

El agente no utiliza observaciones anteriores, estado persistente ni información de la hora siguiente.

Por lo tanto, ante una misma percepción actual debe producir la misma acción.


# 6. Agente reactivo basado en modelo

El segundo agente mantiene un estado interno que resume parte de la historia reciente.

El estado utilizado es:

```python
{
    "percepcion_valida": False,
    "racha_presion_alta": 0,
    "presion_anterior": None,
    "ultima_accion": None,
}
```

La variable principal utilizada para la decisión es `racha_presion_alta`.

La actualización funciona de la siguiente manera:

- Si `presion >= 0.85`, se incrementa la racha.
- Si `presion < 0.85`, la racha se reinicia a cero.
- Si la percepción es inválida, el estado queda en una condición que produce `ABSTENERSE`.

Las reglas de decisión son:

| Estado actualizado | Acción |
|---|---|
| Percepción inválida | `ABSTENERSE` |
| Dos o más horas consecutivas con presión alta | `RECOMENDAR_REFUERZO` |
| Cualquier otro estado válido | `NO_REFORZAR` |

Este agente sigue siendo reactivo porque actualiza un resumen de la historia y aplica reglas sobre el estado actual. No genera sucesores, no busca caminos y no planifica traslados.


# 7. Bitácora y comparación

La función `procesar_secuencia()` ejecuta ambos agentes en orden temporal y genera una bitácora comparativa.

La bitácora contiene como mínimo:

- `hora`
- `presion`
- `racha_presion_alta`
- `accion_simple`
- `motivo_simple`
- `accion_modelo`
- `motivo_modelo`

Para el escenario utilizado se obtuvo:

| Hora | Presión | Racha | Agente simple | Agente basado en modelo |
|---:|---:|---:|---|---|
| 6 | 1.15 | 1 | `RECOMENDAR_REFUERZO` | `NO_REFORZAR` |
| 7 | 1.95 | 2 | `RECOMENDAR_REFUERZO` | `RECOMENDAR_REFUERZO` |
| 8 | 3.10 | 3 | `RECOMENDAR_REFUERZO` | `RECOMENDAR_REFUERZO` |

La diferencia principal aparece en la hora 6.

El agente simple recomienda inmediatamente porque la presión `1.15` supera el umbral de `0.85`.

El agente basado en modelo todavía no recomienda porque solamente tiene una hora consecutiva de presión alta.

En la hora 7 la racha alcanza dos horas consecutivas y el agente basado en modelo también recomienda refuerzo.


# 8. Respuestas a las preguntas

## 8.1. ¿En qué situaciones ambos agentes producen la misma acción?

Ambos agentes producen la misma acción cuando las reglas de ambos llevan al mismo resultado.

En el escenario utilizado:

- En la hora 7, ambos recomiendan refuerzo.
- En la hora 8, ambos recomiendan refuerzo.

También pueden coincidir en `NO_REFORZAR` cuando la presión es baja y en `ABSTENERSE` cuando la percepción es inválida.


## 8.2. ¿Cuándo reaccionan de forma diferente?

Reaccionan de forma diferente cuando la presión actual es alta pero todavía no existe una racha de dos horas consecutivas.

En ese caso:

- El agente simple reacciona inmediatamente a la presión actual y recomienda refuerzo.
- El agente basado en modelo espera a que la presión alta persista durante al menos dos horas consecutivas.

Un ejemplo del escenario es:

```text
Hora: 6
Presión: 1.15
Racha: 1

Agente simple: RECOMENDAR_REFUERZO
Agente basado en modelo: NO_REFORZAR
```


## 8.3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?

El segundo agente está basado en modelo porque mantiene un estado interno que representa un resumen de la historia observada.

En este caso, el estado incluye la cantidad de horas consecutivas con presión alta.

No realiza planificación, búsqueda de caminos ni generación de sucesores. Su comportamiento sigue siendo reactivo: recibe una percepción, actualiza su estado y aplica una regla para obtener una acción.

La diferencia respecto del agente simple es que el agente basado en modelo puede utilizar información resumida de observaciones anteriores.


## 8.4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?

`tasa_otras_simulada` representa una proporción sintética generada por el entorno para repartir los viajes entre la empresa ficticia X y otras empresas.

No representa una medición real de la participación de mercado de otras empresas.

Tampoco permite afirmar que:

- una empresa real tenga determinada participación;
- los usuarios hayan elegido una empresa específica;
- exista una relación causal real entre la cantidad de taxis de X y la participación de otras empresas.

La relación inversa entre la flota de X y la participación externa es una hipótesis didáctica utilizada por el simulador.


## 8.5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?

`resultado_h_mas_1.csv` contiene información correspondiente a la hora siguiente a la decisión.

Por lo tanto, esa información todavía no está disponible cuando el agente debe tomar su decisión.

Utilizarla como percepción produciría una fuga de información temporal o `data leakage`.

En este trabajo:

```text
Percepciones hasta h
        ↓
     Agente
        ↓
    Decisión
        ↓
Información de h+1
        ↓
Evaluación posterior
```

Por este motivo, `resultado_h_mas_1.csv` solamente se utiliza para evaluar posteriormente la decisión y nunca para generarla.


# 9. Pruebas realizadas

Se implementaron pruebas automatizadas utilizando `unittest`.

Se verificaron los siguientes casos:

### Presión baja

Con presión menor a `0.85`, el agente simple devuelve:

```text
NO_REFORZAR
```

y el agente basado en modelo también devuelve:

```text
NO_REFORZAR
```

### Primera hora con presión alta

Con una primera observación de presión alta:

```text
Agente simple → RECOMENDAR_REFUERZO
Agente basado en modelo → NO_REFORZAR
```

Esto demuestra la diferencia entre reaccionar solamente a la percepción actual y considerar la persistencia de la presión.

### Segunda hora consecutiva con presión alta

Después de dos observaciones consecutivas con presión alta:

```text
Agente simple → RECOMENDAR_REFUERZO
Agente basado en modelo → RECOMENDAR_REFUERZO
```

### Reinicio de la racha

Cuando después de una presión alta aparece una presión menor a `0.85`, la racha vuelve a cero.

### Datos inválidos

Cuando la capacidad es desconocida o la percepción es inválida, el agente basado en modelo queda en un estado que produce:

```text
ABSTENERSE
```

### Prueba decisiva de dependencia histórica

Se probaron dos historias diferentes que terminan en la misma percepción actual.

Historia A:

```text
Presión baja → Presión alta
```

Historia B:

```text
Presión alta → Presión alta
```

En ambos casos la percepción actual es:

```text
capacidad_x = 20
presion = 0.90
```

El agente basado en modelo produce:

```text
Historia A → NO_REFORZAR
Historia B → RECOMENDAR_REFUERZO
```

Esto demuestra que el agente basado en modelo puede producir acciones diferentes ante la misma percepción actual debido a su estado interno.

El agente reactivo simple, en cambio, produciría la misma acción en ambos casos porque solamente utiliza la percepción actual.

En total se implementaron y ejecutaron 7 pruebas automatizadas, todas con resultado satisfactorio.


# 10. Evaluación con `h+1`

La información de `resultado_h_mas_1.csv` fue utilizada solamente después de tomar las decisiones.

Para la hora 9 se obtuvo:

- Demanda total: `125`
- Demanda de X: `69`
- Capacidad de X: `20`
- Demanda no cubierta: `49`
- Presión: `3.45`
- Necesita refuerzo: `True`
- Taxis adicionales sugeridos: `49`

En la hora 8 ambos agentes habían recomendado:

```text
RECOMENDAR_REFUERZO
```

Por lo tanto, en este escenario particular, ambas recomendaciones resultaron coherentes con el resultado observado posteriormente en la hora 9.

Esto no significa que los agentes hayan predicho el futuro. El resultado de la hora 9 solamente fue utilizado para realizar una evaluación retrospectiva.


# 11. PEAS

## Performance

El desempeño esperado del agente consiste en:

- Producir recomendaciones coherentes con las reglas definidas.
- Abstenerse ante percepciones inválidas.
- Evitar cualquier fuga de información temporal.
- Mantener trazabilidad mediante el motivo asociado a cada decisión.
- Permitir comparar el comportamiento del agente simple con el agente basado en modelo.

## Environment

El entorno está formado por:

- Una secuencia simulada de observaciones zona-hora.
- Demanda TLC transformada para el ejercicio.
- Una flota sintética de la empresa X.
- Otras empresas sintéticas.
- Un responsable humano que recibe la recomendación.

## Actuators

Los actuadores son los mensajes de decisión:

```text
NO_REFORZAR
RECOMENDAR_REFUERZO
ABSTENERSE
```

El agente no realiza físicamente el traslado ni el despacho de taxis.

## Sensors

El sensor lógico del agente es la lectura de:

```text
percepciones.csv
```

No se trata de un sensor conectado en tiempo real, sino de información suministrada por el escenario simulado.


# 12. Causalidad temporal

La causalidad temporal es una característica importante del trabajo.

Las decisiones se toman utilizando solamente la información disponible hasta la hora actual.

Por ejemplo:

```text
Hora 6 → percepción de hora 6 → decisión
Hora 7 → percepción de hora 7 → decisión
Hora 8 → percepción de hora 8 → decisión
```

La información de la hora 9 solamente se conoce posteriormente y se encuentra en `resultado_h_mas_1.csv`.

Por lo tanto, ninguna función de decisión utiliza información de `h+1`.

Esto evita la fuga temporal y permite evaluar correctamente el comportamiento del agente.


# 13. Limitaciones

El modelo utilizado presenta varias limitaciones:

1. Los pickups TLC son actividad de Yellow Taxi realizada y reportada, no demanda total ni solicitudes no atendidas.

2. X y las otras empresas son entidades ficticias creadas para el ejercicio.

3. La relación inversa entre la flota de X y la participación externa no ha sido estimada con datos reales.

4. Una unidad de capacidad por taxi-hora es una simplificación.

5. La distancia entre centroides no determina por sí sola la duración ni la disponibilidad real de los taxis.

6. `RECOMENDAR_REFUERZO` es un mensaje para revisión humana, no una orden ni un traslado ejecutado.

7. El escenario y la división entre X y otras empresas son simulados, por lo que los resultados no deben interpretarse como predicciones del comportamiento real del transporte.


# 14. Conclusión

En este trabajo se implementaron dos agentes reactivos con diferentes niveles de memoria.

El agente reactivo simple utiliza únicamente la percepción actual y recomienda refuerzo cuando la presión alcanza o supera `0.85`.

El agente reactivo basado en modelo mantiene un estado interno mediante una racha de presión alta y recomienda refuerzo solamente cuando existen dos o más horas consecutivas con presión alta.

Las pruebas realizadas demostraron que ambos agentes pueden producir la misma acción, pero también que pueden reaccionar de manera diferente ante una misma percepción actual cuando la historia previa es distinta.

La prueba decisiva permitió demostrar la dependencia histórica del agente basado en modelo.

Finalmente, se mantuvo la separación temporal entre la información disponible para decidir y la información utilizada posteriormente para evaluar. `resultado_h_mas_1.csv` no forma parte de la percepción y no es consultado por las funciones de decisión.

El resultado es un sistema reactivo simple y basado en modelo que cumple con las reglas planteadas para el escenario simulado y permite observar claramente la diferencia entre reaccionar únicamente al presente y mantener un resumen de la historia reciente.
