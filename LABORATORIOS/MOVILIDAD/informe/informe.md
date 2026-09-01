# Informe del Agente de Movilidad

## Respuestas al Cuestionario

**1. ¿En qué situaciones ambos agentes producen la misma acción?**
Ambos agentes producen la misma acción cuando los datos de percepción son inválidos o nulos (ambos deciden `ABSTENERSE`), cuando la presión de la demanda es baja (ambos deciden `NO_REFORZAR`) y cuando la presión de la demanda ha sido alta de forma sostenida por dos o más horas consecutivas (ambos deciden `RECOMENDAR_REFUERZO`).

**2. ¿Cuándo reaccionan de forma diferente?**
Reaccionan de forma distinta en la **primera hora** en la que se registra una presión alta. El agente reactivo simple evalúa únicamente el estado presente y lanza la alerta de `RECOMENDAR_REFUERZO` inmediatamente. Por otro lado, el agente basado en modelo verifica su estado interno (su historia) y nota que la racha apenas es de 1, por lo que decide `NO_REFORZAR` a la espera de que la tendencia se confirme en la hora siguiente.

**3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?**
El agente está basado en modelo porque mantiene un **estado interno** que le permite recordar aspectos relevantes de su historia (la variable `racha_presion_alta`). A pesar de no generar simulaciones hacia el futuro, buscar caminos, ni planificar estrategias (como haría un agente basado en objetivos o utilidades), utiliza este "modelo interno" de cómo ha ido evolucionando la presión para tomar decisiones condicionadas a la historia, superando la limitación del agente simple que es "ciego" al pasado.

**4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?**
Representa de forma puramente matemática y aleatoria la proporción de viajes que, en el escenario del simulador, han sido tomados por otras empresas competidoras, siendo inversamente proporcional al número de taxis de la empresa X. **No permite afirmar** que este sea el comportamiento real del mercado. Es una relación sintética creada con fines didácticos, ya que los datos de la TLC utilizados solo indican viajes reportados, no quién los operó ni la demanda que no fue atendida.

**5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?**
Porque violaría el principio de causalidad temporal (fuga temporal). Un agente solo puede percibir su estado actual (`h`) o pasado, pero no puede conocer de antemano lo que sucederá en el futuro (`h+1`) para tomar su decisión en el presente. El archivo `resultado_h_mas_1.csv` está destinado únicamente para evaluar el rendimiento de la decisión del agente a posteriori, no como entrada para el proceso de decisión.

---

## Análisis PEAS

A continuación se detalla el entorno de tareas del agente bajo el marco PEAS (Performance, Environment, Actuators, Sensors):

* **Performance (Medida de Rendimiento):** Recomendaciones lógicas y coherentes según las reglas de negocio establecidas para el umbral de presión, total ausencia de fuga temporal (no consultar el futuro), abstención garantizada ante datos corruptos o inválidos, y alta trazabilidad en la justificación de las decisiones (el motivo que devuelve la función).
* **Environment (Entorno):** Una secuencia temporal simulada (zona-hora), construida a partir de una demanda transformada proveniente de los datos históricos de TLC, en la cual operan flotas de taxis ficticias (empresa X y competidores sintéticos). El entorno no ejecuta acciones, sino que provee una recomendación para un responsable humano.
* **Actuators (Actuadores):** Un canal de comunicación por el cual el agente emite los mensajes: `NO_REFORZAR`, `RECOMENDAR_REFUERZO` y `ABSTENERSE`. 
* **Sensors (Sensores):** Lectura lógica y estructurada del archivo de datos `percepciones.csv` (ingresado al agente como un diccionario). No es un sensor conectado en tiempo real a la ciudad.

---

## Limitaciones Reconocidas

Al analizar el modelo actual, es imperativo reconocer las siguientes limitaciones:
1. **La naturaleza de los datos:** Los registros de "pickups" de TLC reflejan exclusivamente viajes realizados y reportados por Yellow Taxi, lo cual **no** equivale a la demanda total real ni cuenta las solicitudes que no pudieron ser atendidas.
2. **Entidades Ficticias:** Tanto la empresa "X" como la competencia y la relación matemática que dicta que la participación externa disminuye cuantos más taxis tiene X, son supuestos netamente didácticos que carecen de respaldo en los datos de la TLC.
3. **Métrica de Capacidad:** Asumir que "un taxi equivale a una unidad de capacidad por hora" es una simplificación extrema que ignora duraciones de viaje.
4. **Geometría:** La distancia utilizada entre los centroides de las zonas no es una distancia vial y es igual a cero para viajes internos, por lo que no puede usarse para estimar disponibilidad.
5. **Alcance de la Decisión:** El actuador es estrictamente informativo. Cuando se emite `RECOMENDAR_REFUERZO`, es una mera sugerencia dirigida a un humano; el sistema no ejecuta, ordena ni despliega traslados de vehículos en la realidad.
