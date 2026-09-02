# Informe Agentes reactivos para refuerzo de taxis

## 1. ¿En qué situaciones ambos agentes producen la misma acción?

Ambos agentes producen la misma acción cuando la percepción y el estado interno llevan a la misma conclusión.

Con presión menor a 0.85, ambos agentes producen `NO_REFORZAR`.

Cuando existen dos o más horas consecutivas con presión igual o superior a 0.85, ambos producen `RECOMENDAR_REFUERZO`.

Si la percepción es inválida, el agente basado en modelo produce `ABSTENERSE`, y el agente simple también debe abstenerse cuando faltan datos requeridos, existen valores inválidos o la capacidad es desconocida.

## 2. ¿Cuándo reaccionan de forma diferente?

Reaccionan de forma diferente principalmente durante la primera hora en la que aparece una presión alta.

El agente reactivo simple utiliza solamente la percepción actual. Por lo tanto, si `presion >= 0.85`, recomienda refuerzo inmediatamente.

El agente basado en modelo tiene en cuenta la historia resumida en su estado interno. Durante la primera hora de presión alta, la racha es 1 y todavía no recomienda refuerzo. Recién recomienda cuando existen dos o más horas consecutivas con presión alta.

## 3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?

El segundo agente es basado en modelo porque mantiene un estado interno que representa un resumen de la historia observada. En particular, mantiene la variable `racha_presion_alta`, que registra cuántas horas consecutivas se ha observado una presión igual o superior a 0.85.

No necesita planificar, buscar caminos ni generar sucesores. Simplemente actualiza su estado interno con cada nueva percepción y aplica reglas sobre ese estado. Por eso sigue siendo un agente reactivo basado en modelo.

## 4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?

`tasa_otras_simulada` representa una proporción sintética de viajes que el escenario asigna a otras empresas distintas de X. Es un valor generado artificialmente por el entorno para dividir los viajes simulados entre X y otras empresas.

No permite afirmar cuál es la participación real de otras empresas, ni permite conocer cuántos taxis tienen esas empresas. Tampoco representa una estimación real del comportamiento del mercado, ya que la relación utilizada para generar esta proporción es un ejemplo ficticio utilizado para el ejercicio.

## 5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?

`resultado_h_mas_1.csv` contiene información correspondiente a la evaluación posterior de la hora siguiente.

Si el agente utilizara ese archivo para tomar la decisión, estaría utilizando información del futuro que no estaba disponible al momento de decidir. Esto produciría una fuga temporal y haría que la comparación entre los agentes no representara una decisión válida.

Por este motivo, la percepción de los agentes debe utilizar únicamente la información disponible hasta la hora observada.

---

# PEAS

## Performance

El desempeño del agente se evalúa mediante:

* Recomendaciones coherentes con las reglas establecidas.
* Ausencia de fuga temporal.
* Abstención ante datos inválidos.
* Trazabilidad de las decisiones mediante los motivos registrados en la bitácora.

## Environment

El entorno está formado por:

* Una secuencia simulada de zona y hora.
* Datos de viajes TLC transformados para el ejercicio.
* Una flota ficticia de taxis de la empresa X.
* Otras empresas ficticias.
* Un responsable humano que recibe la recomendación y puede considerar el refuerzo.

## Actuators

Los actuadores son los mensajes de decisión:

* `NO_REFORZAR`
* `RECOMENDAR_REFUERZO`
* `ABSTENERSE`

El agente no ejecuta directamente el traslado de taxis.

## Sensors

El sensor consiste en la lectura lógica de las percepciones contenidas en `percepciones.csv`.

No se trata de un sensor físico ni de una conexión en tiempo real.

---

# Limitaciones

El ejercicio presenta varias limitaciones que deben tenerse en cuenta:

* Los pickups TLC son actividad Yellow Taxi realizada y reportada, no demanda total ni solicitudes no atendidas.
* X y las otras empresas son entidades ficticias creadas para el ejercicio.
* La relación inversa entre flota de X y participación externa no ha sido estimada con datos reales.
* Una unidad de capacidad por taxi-hora es una simplificación.
* La distancia entre centroides no determina duración ni disponibilidad.
* RECOMENDAR_REFUERZO es un mensaje para revisión humana, no una orden ni un traslado ejecutado.

## Conclusión

El agente reactivo simple toma decisiones únicamente a partir de la percepción actual, mientras que el agente reactivo basado en modelo incorpora un resumen de la historia mediante su estado interno.

La comparación muestra que la memoria permite distinguir situaciones que presentan la misma percepción actual pero tienen historias diferentes. Esto permite demostrar la dependencia histórica del agente basado en modelo sin convertirlo en un agente planificador.
