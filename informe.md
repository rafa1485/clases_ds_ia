# Trabajo práctico: agentes reactivos para refuerzo de taxis

## 1. Objetivo

El objetivo del trabajo fue implementar y comparar dos agentes que recomiendan si una empresa ficticia X debería considerar reforzar con más taxis una zona durante la hora siguiente.

Se implementaron:

- Un agente reactivo simple, que utiliza únicamente la percepción de la hora actual.
- Un agente reactivo basado en modelo, que mantiene un estado interno con la cantidad de horas consecutivas de presión alta.

La recomendación no ejecuta un traslado de taxis. Solamente genera un mensaje para que una persona evalúe la situación.

## 2. Escenario utilizado

Se generó un escenario reproducible con los siguientes parámetros:

- Zona TLC: 161, Midtown Center.
- Hora de decisión: 8.
- Taxis de la empresa X: 20.
- Horas de historia: 3.
- Semilla: 42.

Las percepciones obtenidas fueron:

| Hora | Presión | Racha de presión alta |
|---:|---:|---:|
| 6 | 0.95 | 1 |
| 7 | 1.75 | 2 |
| 8 | 3.25 | 3 |

El umbral utilizado para considerar que existe presión alta fue 0.85.

## 3. Comparación de los agentes

### ¿En qué situaciones ambos agentes producen la misma acción?

Ambos agentes producen `NO_REFORZAR` cuando la presión actual es menor que 0.85 y la percepción es válida.

También producen `RECOMENDAR_REFUERZO` cuando existen al menos dos horas consecutivas con presión igual o superior a 0.85. En ese caso, el agente simple recomienda por la presión actual y el agente basado en modelo recomienda por la persistencia de la presión alta.

Cuando la percepción es inválida o la capacidad es desconocida, ambos producen `ABSTENERSE`.

### ¿Cuándo reaccionan de forma diferente?

Reaccionan de manera diferente durante la primera hora con presión alta.

El agente simple recomienda refuerzo inmediatamente porque solo evalúa si la presión actual supera el umbral. El agente basado en modelo todavía devuelve `NO_REFORZAR`, debido a que necesita observar dos horas consecutivas con presión alta.

En el escenario generado, esto ocurrió en la hora 6:

- Agente simple: `RECOMENDAR_REFUERZO`.
- Agente basado en modelo: `NO_REFORZAR`.

A partir de la hora 7, ambos recomendaron refuerzo.

### ¿Por qué el segundo agente está basado en modelo aunque no planifique?

Está basado en modelo porque mantiene un estado interno que resume información de las percepciones anteriores.

En este trabajo, el estado guarda la racha de horas consecutivas con presión alta, la presión anterior, la validez de la percepción y la última acción. Gracias a esta memoria, dos historias diferentes pueden producir decisiones distintas aunque terminen con la misma percepción actual.

El agente no planifica porque no genera estados futuros, no busca caminos y no decide desde qué zona trasladar taxis.

### ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?

`tasa_otras_simulada` representa la proporción sintética de viajes asignados a otras empresas dentro del entorno del ejercicio.

Este valor fue generado mediante una relación aleatoria y didáctica. No representa una participación real de mercado y no permite afirmar cuántos vehículos tienen otras empresas ni cómo se comportan en la realidad.

### ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?

El archivo `resultado_h_mas_1.csv` contiene información de la hora futura. Si el agente utilizara esos datos para decidir, estaría accediendo a información que todavía no estaría disponible en un caso real.

Esto produciría una fuga temporal de información. Por ese motivo, los agentes solo utilizan `percepciones.csv`, que contiene datos disponibles hasta la hora de decisión.

El resultado de la hora siguiente se reserva exclusivamente para evaluar posteriormente la recomendación.

## 4. Demostración de dependencia histórica

Se probaron dos historias diferentes que terminaban en la misma percepción de presión alta.

En la primera historia, la hora anterior tenía presión baja. En la segunda, la hora anterior también tenía presión alta.

El agente reactivo simple produjo la misma acción en ambos casos porque solamente utiliza la percepción actual.

El agente basado en modelo produjo acciones diferentes:

- Después de una hora baja y una alta: `NO_REFORZAR`.
- Después de dos horas altas consecutivas: `RECOMENDAR_REFUERZO`.

Esto demuestra que la decisión del segundo agente depende de su estado interno y de la historia de percepciones.

## 5. Análisis PEAS

### Performance

- Cumplimiento de las reglas definidas.
- Recomendaciones coherentes con la presión observada.
- Ausencia de fuga de información temporal.
- Abstención frente a datos inválidos o capacidad desconocida.
- Registro de las decisiones y sus motivos en una bitácora.

### Environment

- Secuencia simulada de horas para una zona TLC.
- Datos históricos transformados de viajes Yellow Taxi.
- Empresa ficticia X con una cantidad conocida de taxis.
- Otras empresas representadas de manera sintética.
- Responsable humano que recibe y evalúa la recomendación.

### Actuators

Los actuadores son los mensajes producidos por los agentes:

- `NO_REFORZAR`
- `RECOMENDAR_REFUERZO`
- `ABSTENERSE`

Los agentes no trasladan taxis ni seleccionan una zona de origen.

### Sensors

El sensor es la lectura lógica del archivo `percepciones.csv`.

Este archivo contiene información como la hora, la demanda asignada a X, la capacidad disponible y la presión. No se trata de un sensor físico ni de una fuente conectada en tiempo real.

## 6. Pruebas realizadas

Se implementaron pruebas para comprobar:

- Presión baja.
- Primera hora con presión alta.
- Segunda hora consecutiva con presión alta.
- Percepción inválida.
- Capacidad desconocida.
- Dos historias diferentes con la misma percepción final.
- Ausencia de datos futuros en las funciones de decisión.

Todas las pruebas finalizaron correctamente.

## 7. Limitaciones

- Los datos TLC representan viajes Yellow Taxi realizados y reportados, no la demanda total de movilidad.
- No se incluyen solicitudes de viaje que no fueron atendidas.
- La empresa X y las demás empresas son entidades ficticias.
- La proporción asignada a otras empresas es sintética y no fue estimada con datos reales.
- Se supone que cada taxi aporta una unidad de capacidad por hora.
- La distancia entre centroides no representa una ruta real ni permite conocer su duración.
- No se consideran tránsito, clima, duración de los viajes ni disponibilidad futura.
- `RECOMENDAR_REFUERZO` es una sugerencia para revisión humana, no una orden automática.
- El ejercicio no es un predictor de demanda ni un sistema de optimización de flota.

## 8. Conclusión

El trabajo permitió observar la diferencia entre reaccionar solamente ante la percepción actual y utilizar un estado interno que resume la historia.

El agente simple responde más rápidamente ante una presión alta, mientras que el agente basado en modelo exige que la situación persista durante dos horas consecutivas. Esto evita recomendar un refuerzo basándose únicamente en una observación aislada.

En el escenario analizado, el agente simple recomendó refuerzo desde la hora 6. El agente basado en modelo comenzó a recomendarlo en la hora 7, cuando la racha de presión alta alcanzó dos horas consecutivas.
