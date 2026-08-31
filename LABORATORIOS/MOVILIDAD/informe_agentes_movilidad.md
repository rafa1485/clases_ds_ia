# Informe: agentes reactivos para refuerzo de taxis

## Escenario reproducible

La bitacora entregada se genero para la zona TLC 161 (`Midtown Center`), con
hora de decision 8, 20 taxis de X, tres horas de historia y semilla 42. Solo se
procesaron las percepciones visibles de las horas 6, 7 y 8. El archivo con el
resultado de la hora 9 no se paso a los agentes.

## Comparacion de los agentes

1. **¿En que situaciones ambos agentes producen la misma accion?** Ambos
   devuelven `ABSTENERSE` ante una percepcion invalida y `NO_REFORZAR` cuando
   la presion actual es baja. Tambien recomiendan refuerzo cuando la presion
   lleva al menos dos horas consecutivas por encima del umbral.

2. **¿Cuando reaccionan de forma diferente?** En la primera hora de presion
   alta. El agente simple recomienda refuerzo inmediatamente, mientras que el
   agente basado en modelo espera una segunda observacion alta consecutiva.

3. **¿Por que el segundo agente esta basado en modelo aunque no planifique?**
   Porque mantiene un estado interno —la racha de presion alta— que resume
   observaciones anteriores. Decide sobre ese estado actualizado. No necesita
   generar estados futuros, buscar caminos ni elegir traslados para estar
   basado en modelo.

4. **¿Que representa `tasa_otras_simulada` y que no permite afirmar?** Es una
   proporcion sintetica y aleatoria de viajes asignados a otras empresas. Esta
   acotada y su valor base disminuye al aumentar los taxis de X. No representa
   una participacion observada del mercado ni permite inferir la cantidad real
   de vehiculos, la demanda real o el comportamiento causal de otras empresas.

5. **¿Por que `resultado_h_mas_1.csv` no puede formar parte de la percepcion?**
   Porque contiene informacion que solo se conoceria despues de decidir. Usarla
   produciria fuga temporal: la politica pareceria funcionar viendo el futuro,
   pero no podria operar de esa forma en el momento real de la decision.

## PEAS

| Elemento | Identificacion en el trabajo |
|---|---|
| Performance | Recomendaciones coherentes con las reglas, abstencion ante entradas invalidas, ausencia de fuga temporal y motivos trazables. |
| Environment | Secuencia simulada zona-hora, actividad TLC transformada, flota sintetica de X, participacion sintetica de otras empresas y una persona responsable de revisar la recomendacion. |
| Actuators | Los mensajes `NO_REFORZAR`, `RECOMENDAR_REFUERZO` y `ABSTENERSE`. |
| Sensors | Lectura logica de `percepciones.csv`, no un sensor fisico ni una conexion en tiempo real. |

## Trazabilidad y causalidad temporal

La bitacora registra la percepcion de cada hora, la racha actualizada y el
motivo de ambas acciones. Las filas se procesan en orden temporal. Las
funciones de decision reciben solo la percepcion actual o el estado construido
con percepciones presentes y pasadas; el resultado de `h+1` se reserva para una
evaluacion posterior.

La prueba de las dos historias muestra la diferencia esencial. Ante una misma
percepcion final de presion alta, el agente simple siempre toma la misma
accion. El agente basado en modelo recomienda refuerzo si la hora anterior
tambien tuvo presion alta, pero no lo hace si la observacion anterior fue baja.

## Limitaciones

- Los pickups TLC son viajes Yellow Taxi realizados y reportados; no son la
  demanda total ni incluyen solicitudes no atendidas.
- X y las otras empresas son entidades ficticias del ejercicio.
- La relacion inversa entre flota de X y participacion externa es una hipotesis
  didactica que no fue estimada con datos reales.
- Una unidad de capacidad por taxi-hora simplifica productividad, ocupacion y
  duracion de los viajes.
- La distancia entre centroides no determina la duracion del viaje ni la
  disponibilidad futura de un taxi.
- `RECOMENDAR_REFUERZO` solicita revision humana: no identifica el origen de
  los taxis, no ordena un traslado y no modifica la flota.
