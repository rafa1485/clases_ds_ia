## Responder brevemente:

1. ¿En qué situaciones ambos agentes producen la misma acción?
2. ¿Cuándo reaccionan de forma diferente?
3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?
4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?
5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?

## Respuestas 
1. Ambos agentes producen la misma acción cuando:
  - La percepción es inválida: ambos devuelven ABSTENERSE.
  - La presión es baja (presion < 0.85): ambos devuelven NO_REFORZAR.
  - Existen dos o más horas consecutivas con presión alta: ambos devuelven RECOMENDAR_REFUERZO.

2. Reaccionan de forma diferente durante la primera hora con presión alta (presion >= 0.85). El   agente reactivo simple recomienda refuerzo inmediatamente, mientras que el agente basado en modelo  devuelve NO_REFORZAR porque todavía no se alcanzaron dos horas consecutivas de presión alta.

3. El segundo agente está basado en modelo porque mantiene un estado interno que resume la historia observada. En este caso, recuerda la racha de horas consecutivas con presión alta, la presión anterior y la última acción. No necesita planificar: utiliza su memoria para representar una parte del estado del entorno y aplicar reglas sobre ella.

4. tasa_otras_simulada representa la proporción sintética de viajes asignados a otras empresas. Se genera mediante una fórmula y un componente aleatorio para el ejercicio. No permite afirmar cuál es la participación real de mercado de otras empresas, cuántos vehículos poseen ni cómo se comportan realmente, porque esa información no proviene de datos observados.

5. resultado_h_mas_1.csv contiene información correspondiente a la hora futura h+1. Al tomar una decisión al finalizar la hora h, esa información todavía no debería estar disponible. Utilizarla produciría una fuga temporal: el agente decidiría con conocimiento del futuro. Por eso solamente puede usarse después, para evaluar la recomendación realizada.

## PEAS de los agentes de movilidad

### Performance

El desempeño se evalúa verificando que las recomendaciones sean coherentes con
las reglas establecidas. El agente debe abstenerse ante datos inválidos,
evitar el uso de información futura y registrar el motivo de cada decisión
para garantizar su trazabilidad.

En el agente basado en modelo también se verifica que la racha de presión alta
se actualice correctamente.

### Environment

El entorno es una secuencia simulada de observaciones por zona y hora. Incluye
la demanda obtenida a partir de datos TLC transformados, la flota sintética de
la empresa X y una participación simulada de otras empresas.

También forma parte del entorno el responsable humano que recibe la
recomendación y decide si corresponde realizar un refuerzo. El agente no
traslada taxis automáticamente.

### Actuators

Los actuadores son los mensajes que los agentes pueden generar:

- `NO_REFORZAR`: no se encontró evidencia suficiente para recomendar más taxis.
- `RECOMENDAR_REFUERZO`: se aconseja que una persona considere reforzar la zona.
- `ABSTENERSE`: los datos no permiten tomar una decisión segura.

Estos actuadores producen recomendaciones, no acciones físicas sobre la flota.

### Sensors

El sensor es la lectura lógica del archivo `percepciones.csv`. Cada fila
representa la información disponible para una zona durante una hora.

No se trata de un sensor físico ni de una conexión en tiempo real. Los agentes
tampoco utilizan `resultado_h_mas_1.csv`, porque contiene información futura
reservada para evaluar posteriormente las decisiones.

## Limitaciones

- Los datos de TLC representan viajes Yellow Taxi realizados y reportados. No
  representan toda la demanda de movilidad ni solicitudes que no fueron
  atendidas.

- La empresa X y las otras empresas son entidades ficticias creadas para el
  ejercicio.

- `tasa_otras_simulada` es un valor sintético. No representa una participación
  real de mercado.

- La relación inversa entre la cantidad de taxis de X y la participación de
  otras empresas no fue estimada a partir de datos reales.

- Se supone que cada taxi aporta una unidad de capacidad por hora, lo cual
  simplifica el funcionamiento real de una flota.

- La distancia entre los centroides de las zonas no representa necesariamente
  la distancia vial, la duración del viaje ni la disponibilidad de los taxis.

- `RECOMENDAR_REFUERZO` es únicamente una recomendación para una persona. El
  agente no selecciona taxis, no decide desde qué zona trasladarlos y no
  ejecuta ningún movimiento.