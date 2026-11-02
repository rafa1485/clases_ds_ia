# Informe: agentes reactivos para refuerzo de taxis

**Estudiante:** Ezequiel Zunino
**Curso:** Inteligencia Artificial
**Modalidad:** individual

## Entrega

| Archivo | Contenido |
|---|---|
| `agentes_movilidad.py` | Agente reactivo simple, agente basado en modelo y bitácora. |
| `test_agentes_movilidad.py` | Pruebas obligatorias y comprobaciones adicionales. |
| `bitacora_agentes.csv` | Comparación de ambos agentes sobre el escenario reproducible. |
| `escenario_agente/` | Percepciones y resultado futuro generados por el simulador del curso. |

## Escenario y reproducción

Se usó el escenario de la consigna: zona TLC 161 (Midtown Center), decisión al finalizar la hora 8, 20 taxis de X, 3 horas de historia y semilla 42. Los datos son los viajes Yellow Taxi de enero de 2024.

```bash
python simulador_entorno_agente.py --zona 161 --hora 8 --taxis-x 20 \
  --horas-historia 3 --semilla 42 --salida-dir escenario_agente
python agentes_movilidad.py escenario_agente/percepciones.csv bitacora_agentes.csv
python -m pytest test_agentes_movilidad.py
```

El simulador no forma parte de la entrega: es `simulador_entorno_agente.py`, del material del curso. Las 34 pruebas pasan.

## Bitácora

| Hora | Presión | Racha | Agente simple | Agente basado en modelo |
|---:|---:|---:|---|---|
| 6 | 1,15 | 1 | `RECOMENDAR_REFUERZO` | `NO_REFORZAR` |
| 7 | 1,95 | 2 | `RECOMENDAR_REFUERZO` | `RECOMENDAR_REFUERZO` |
| 8 | 3,10 | 3 | `RECOMENDAR_REFUERZO` | `RECOMENDAR_REFUERZO` |

Los agentes difieren solo en la hora 6. Este escenario tiene presión alta en las tres horas, por lo que no muestra presión baja ni datos inválidos. Esos casos están cubiertos por las pruebas.

### Dependencia de la historia

La prueba decisiva usa dos historias que terminan en la misma percepción, con presión 1,20:

| Historia de presiones | Racha final | Agente simple | Agente basado en modelo |
|---|---:|---|---|
| 0,50 → 1,20 | 1 | `RECOMENDAR_REFUERZO` | `NO_REFORZAR` |
| 1,20 → 1,20 | 2 | `RECOMENDAR_REFUERZO` | `RECOMENDAR_REFUERZO` |

El agente simple no puede distinguir estas historias porque solo ve la última percepción. El agente basado en modelo sí, porque su estado anterior es distinto.

### Evaluación posterior

`resultado_h_mas_1.csv` se leyó recién después de cerrar la bitácora, y ninguna decisión lo usa. En la hora 9, `demanda_x` fue 69 con capacidad 20, y `necesita_refuerzo` es verdadero. Las dos recomendaciones de la hora 8 son coherentes con ese resultado, pero un solo caso no sirve para evaluar el desempeño de los agentes.

## Respuestas

**1. ¿En qué situaciones ambos agentes producen la misma acción?**

En tres situaciones:

- Con presión menor a 0,85, los dos devuelven `NO_REFORZAR`, porque la racha vuelve a cero.
- Con presión alta desde la segunda hora consecutiva, los dos devuelven `RECOMENDAR_REFUERZO`.
- Con una percepción inválida, los dos devuelven `ABSTENERSE`.

**2. ¿Cuándo reaccionan de forma diferente?**

Solo en la primera hora con presión alta. Eso ocurre al comienzo de la secuencia, después de una hora con presión baja o después de un dato inválido. El simple recomienda refuerzo y el basado en modelo espera a confirmar la persistencia. El primero responde antes y puede reaccionar a un pico aislado. El segundo filtra esos picos a cambio de recomendar una hora más tarde.

**3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?**

Porque mantiene un estado interno que resume una parte del entorno que la percepción actual no muestra: cuántas horas seguidas lleva la presión alta. Ese estado se actualiza con cada percepción y la decisión se toma sobre él. Planificar sería otra cosa: generar sucesores, simular secuencias de acciones y comparar sus consecuencias. Este agente no hace nada de eso. Solo aplica reglas condición-acción al estado actual, y por eso sigue siendo reactivo.

**4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?**

Es la proporción de viajes asignada a las otras empresas en esa hora. Se sortea con una fórmula supuesta, inversa a la flota de X, más ruido normal. No se estimó con datos reales. No permite afirmar cuál es la participación de mercado de ninguna empresa, cuántos vehículos tienen las otras, ni que aumentar la flota de X reduzca la participación de los demás. Además, `demanda_x` depende de esta tasa, así que `presion` también es en parte sintética.

**5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?**

Porque contiene información de `h+1`, que todavía no existe cuando el agente decide al cerrar la hora `h`. Usarla sería una fuga temporal: la evaluación daría mejor de lo que el agente podría lograr en un uso real, y su función de decisión dependería de datos que nunca tendría disponibles. Ese archivo solo sirve para comparar después de haber decidido.

## PEAS

| Elemento | Contenido |
|---|---|
| Performance | Recomendaciones coherentes con las reglas, ausencia de fuga temporal, abstención ante datos inválidos y trazabilidad de cada decisión mediante su motivo. |
| Environment | Secuencia simulada zona-hora de un lunes, demanda TLC transformada, flota sintética de X, otras empresas sintéticas y un responsable humano que decide. |
| Actuators | Mensajes `NO_REFORZAR`, `RECOMENDAR_REFUERZO` y `ABSTENERSE`. No ejecutan traslados. |
| Sensors | Lectura lógica de `percepciones.csv`. No es un sensor conectado en tiempo real. |

## Decisiones de implementación

La consigna deja abiertos estos puntos:

- **Campos requeridos:** son `presion` y `capacidad_x`, los que usan las reglas. Los demás campos numéricos se validan si están presentes.
- **Flota cero:** la consigna pide abstenerse cuando la capacidad es desconocida, y una capacidad 0 es un dato conocido. El material de la semana 1 hace la misma distinción: la abstención corresponde a la capacidad desconocida, no a la agotada. El simulador informa presión infinita cuando hay demanda y capacidad 0, así que ese caso se tomó como válido: cumple `presion >= 0.85` y recomienda refuerzo. Una presión infinita con capacidad positiva se considera inválida y produce `ABSTENERSE`.
- **Dato inválido:** reinicia la racha a cero, porque no se puede afirmar que las horas alrededor del dato sean consecutivas con presión alta.
- **`presion_anterior`:** guarda la última presión válida, que será la anterior en la siguiente actualización.
- **`ultima_accion`:** la registra `procesar_secuencia`, para que `decidir_reactivo_modelo` no modifique el estado.
- **Validación:** el mismo control se usa en los dos agentes, así que ante un mismo dato inválido nunca se contradicen.

## Causalidad temporal

- Las funciones de decisión solo reciben la percepción actual o el estado. Una prueba comprueba sus parámetros.
- Agregar campos futuros a una percepción no cambia la decisión.
- El código no menciona el archivo de evaluación.
- Agregar o cambiar filas futuras no altera las decisiones ya tomadas sobre filas anteriores.

## Limitaciones

- Los pickups TLC son actividad Yellow Taxi realizada y reportada, no demanda total ni solicitudes no atendidas.
- X y las otras empresas son entidades ficticias creadas para el ejercicio.
- La relación inversa entre la flota de X y la participación externa no fue estimada con datos reales.
- Una unidad de capacidad por taxi-hora es una simplificación.
- La distancia entre centroides no determina duración ni disponibilidad.
- `RECOMENDAR_REFUERZO` es un mensaje para revisión humana, no una orden ni un traslado ejecutado.
- El umbral 0,85 recomienda refuerzo antes de que haya demanda sin cubrir, que aparece con presión mayor a 1. Por eso una recomendación no equivale a `necesita_refuerzo`.
- La racha arranca en cero al comienzo de la secuencia. En la hora 6 el agente basado en modelo no sabe si la hora 5 tuvo presión alta, y su `NO_REFORZAR` se debe en parte al inicio de la ventana.
- `procesar_secuencia` ordena por hora, pero supone que las horas son contiguas, como las que produce el simulador. Si faltara una hora, la racha contaría como seguidas dos horas que no lo son.
- Un único escenario con una semilla no alcanza para comparar el desempeño de los agentes. Esta bitácora muestra cómo deciden, no cuál es mejor.
