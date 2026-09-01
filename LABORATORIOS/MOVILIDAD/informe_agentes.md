# Informe: Agentes Reactivos para Refuerzo de Taxis

**Integrantes:** Justin Garcia – Harryson Ladines

---

## 1. Cuestionario de Evaluación

**1. ¿En qué situaciones ambos agentes producen la misma acción?**
Ambos agentes coinciden en su respuesta en tres escenarios principales:
*   **Presión baja sostenida:** Cuando la métrica presión es inferior a 0.85, ambos responden `NO_REFORZAR`.
*   **Presión alta continuada ($\ge 2$ horas):** Cuando la presión supera o iguala 0.85 durante dos o más horas consecutivas, tanto el agente simple como el basado en modelo emiten la señal `RECOMENDAR_REFUERZO`.
*   **Datos inválidos o faltantes:** Si la percepción carece de información requerida o presenta formatos erróneos, ambos agentes se abstienen de decidir emitiendo `ABSTENERSE`.

**2. ¿Cuándo reaccionan de forma diferente?**
Reaccionan de manera distinta en el primer pico de presión alta (cuando un periodo de demanda alta ocurre tras un periodo normal):
*   El **agente reactivo simple** evalúa únicamente la hora presente y recomienda el refuerzo inmediatamente (`RECOMENDAR_REFUERZO`).
*   El **agente basado en modelo** consulta su estado interno (`racha_presion_alta = 1`) y responde `NO_REFORZAR`, exigiendo una persistencia de al menos dos horas consecutivas para confirmar la tendencia antes de emitir la recomendación.

**3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?**
Se clasifica como un agente basado en modelo porque mantiene un estado interno persistente que evoluciona con el tiempo. El estado actualiza variables como la racha acumulada y la última acción realizada para reflejar aspectos del entorno que no son visibles únicamente en la observación puntual de la hora actual. No requiere un algoritmo de búsqueda o planificación en un árbol de estados futuros para considerarse basado en modelo; basta con que su regla de decisión dependa de una representación acumulada de la historia del entorno.

**4. ¿Qué representa tasa_otras_simulada y qué no permite afirmar?**
`tasa_otras_simulada` representa la proporción estimada de la demanda total de la zona que está siendo atendida por empresas competidoras (otras plataformas o taxis independientes) durante esa hora.

No permite afirmar:
*   La causa real o comercial de esa preferencia (precios, calidad de servicio o disponibilidad de la competencia).
*   El comportamiento ni las decisiones individuales de los usuarios.
*   La demanda futura en las horas posteriores.

**5. ¿Por qué resultado_h_mas_1.csv no puede formar parte de la percepción?**
El archivo `resultado_h_mas_1.csv` contiene la simulación del estado del sistema en la hora subsiguiente ($h+1$). Incluirlo dentro del flujo de percepciones del agente constituiría un fuga de información del futuro (*data leakage*). Un agente que tome decisiones en tiempo real únicamente puede acceder a las observaciones acumuladas hasta la hora actual ($h$); el uso de información futura invalida la evaluación y la simulación realista del entorno de decisión.


## 2. Definición del Entorno de Tareas (PEAS)

*   **Performance (Rendimiento):** Maximizar la tasa de cobertura de la demanda en la zona asignada, emitir recomendaciones de refuerzo oportunas evitando falsas alarmas, mantener la trazabilidad en la bitácora y abstenerse de operar cuando la información recibida sea incompleta o errónea.
*   **Environment (Entorno):** Entorno simulado determinista y parcialmente observable basado en datos históricos de viajes TLC. Comprende la demanda sintética dividida entre la empresa X y competidores, la disponibilidad de flota en la zona y la presencia de un operador humano que toma la decisión final.
*   **Actuators (Actuadores):** Emisión de señales y recomendaciones de acción enviadas al sistema: `RECOMENDAR_REFUERZO`, `NO_REFORZAR` o `ABSTENERSE`.
*   **Sensors (Sensores):** Lectura e interpretación del archivo de percepciones (`percepciones.csv`), del cual se extraen métricas como la demanda, capacidad y el cálculo de la variable `presion`.

## 3. Limitaciones del Modelo

*   **Parcialmente observable y reactivo:** Los agentes solo reaccionan a las métricas del archivo de percepciones hasta la hora actual. No incorporan predicciones ni modelos de series temporales para anticipar fluctuaciones futuras de la demanda.
*   **Dependencia de umbrales rígidos:** La regla de decisión utiliza un umbral fijo ($presion \ge 0.85$). Esto no considera factores contextuales externos como condiciones climáticas, eventos masivos o días festivos que puedan alterar temporalmente el comportamiento de la demanda.
*   **Ausencia de planificación geográfica o logística:** El agente recomienda cuándo enviar refuerzos, pero no evalúa de qué zonas vecinas extraer los taxis ni el impacto del tráfico en el tiempo de desplazamiento de las unidades.
*   **Acoplamiento al historial reciente:** El agente basado en modelo depende únicamente de la racha de horas consecutivas (`racha_presion_alta`). Una interrupción momentánea de una sola hora por debajo del umbral reinicia el contador a cero, perdiendo el contexto acumulado de alta demanda previa.

