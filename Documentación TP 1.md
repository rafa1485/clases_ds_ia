# Informe: Agentes Reactivos para Refuerzo de Taxis

## 1. Definición del marco PEAS

| Elemento | Descripción |
| :--- | :--- |
| **Performance (Rendimiento)** | Coherencia con las reglas condición-acción, ausencia de fuga temporal (sin acceso a $h+1$), abstención ante datos inválidos y trazabilidad de los motivos de decisión. |
| **Environment (Entorno)** | Secuencia temporal de pares zona-hora, demanda sintética basada en registros Yellow Taxi de NYC, flota fija de la empresa X, empresas competidoras simuladas y operador humano. |
| **Actuators (Actuadores)** | Emisión de mensajes de decisión: `NO_REFORZAR`, `RECOMENDAR_REFUERZO` y `ABSTENERSE`. |
| **Sensors (Sensores)** | Lectura lógica estructurada del archivo `percepciones.csv` (no corresponde a un sensor telemático en tiempo real). |

---

## 2. Respuestas a las Preguntas Conceptuales

**1. ¿En qué situaciones ambos agentes producen la misma acción?**
* Emiten `NO_REFORZAR` cuando la presión observada es baja ($< 0.85$).
* Emiten `RECOMENDAR_REFUERZO` a partir de la segunda hora consecutiva con presión alta ($\ge 0.85$).
* Emiten `ABSTENERSE` ante entradas incompletas, datos nulos o valores de capacidad inválidos ($<= 0$).

**2. ¿Cuándo reaccionan de forma diferente?**
* Durante la primera hora aislada en la que la presión supera o iguala el umbral de $0.85$. El agente reactivo simple recomienda refuerzo de inmediato, mientras que el agente basado en modelo emite `NO_REFORZAR` para evitar falsos positivos ante picos no sostenidos (racha = 1).

**3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?**
* Porque mantiene y actualiza un estado interno persistente (`racha_presion_alta`, `presion_anterior`) que modela aspectos del entorno no visibles en la percepción actual. Su decisión combina la percepción instantánea con la historia previa, a pesar de seguir una política reactiva basada en reglas y no generar árboles de búsqueda ni planificación.

**4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?**
* Representa una proporción estocástica y acotada de viajes captados por otras empresas, modelada sintéticamente de forma inversamente proporcional a la flota de X.
* No permite afirmar la cuota real de mercado de ninguna empresa existente ni describir dinámicas competitivas verídicas, tratándose de una hipótesis didáctica.

**5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?**
* Porque contiene las observaciones del paso temporal posterior ($h+1$), las cuales no han ocurrido al momento de tomar la decisión al cierre de la hora $h$. Utilizarlo implicaría una fuga temporal (*data leakage*) y rompería la causalidad física del agente.

---

## 3. Limitaciones e Hipótesis Didácticas

* **Métrica de viajes:** Los datos de origen TLC reflejan únicamente servicios completados de Yellow Taxi, no representan la demanda total no atendida ni cancelaciones.
* **Entidades sintéticas:** La empresa X y sus competidoras son abstracciones creadas con fines educativos.
* **Simplificación de capacidad:** Asumir una unidad fija de capacidad por taxi-hora ignora variables operativas como el congestionamiento, traslados en vacío y tiempos de descanso.
* **Naturaleza de la acción:** La salida `RECOMENDAR_REFUERZO` es una notificación de asistencia para un operador humano, no una orden de despacho ni un traslado vehicular ejecutado.
