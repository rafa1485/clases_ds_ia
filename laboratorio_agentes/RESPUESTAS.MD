## 1. Respuestas al Cuestionario

**1. ¿En qué situaciones ambos agentes producen la misma acción?**
Ambos agentes producen la misma acción en tres escenarios precisos:
* Cuando la percepción contiene datos inválidos o faltantes (ambos devuelven `**ABSTENERSE**`).
* Cuando la presión es inferior a 0.85 (ambos devuelven `NO_REFORZAR`).
* A partir de la segunda hora consecutiva con presión alta (>= 0.85), donde ambos devuelven `RECOMENDAR_REFUERZO`.

**2. ¿Cuándo reaccionan de forma diferente?**
Reaccionan diferente durante la primera hora en la que se registra un pico de presión (presión >= 0.85 tras una hora de presión controlada). El agente
reactivo simple recomienda refuerzo inmediatamente como acto reflejo, mientras que el agente basado en modelo indica `NO_REFORZAR`, ya que la regla exige
que la condición de presión alta se sostenga durante al menos dos horas consecutivas para considerarla una tendencia.

**3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?**
Se considera basado en modelo porque mantiene un estado interno que funciona como memoria de eventos pasados (la racha temporal de presión alta),
construyendo una representación del entorno que persiste más allá de la percepción instantánea actual. No se considera que planifique porque no proyecta
múltiples estados futuros, no genera árboles de búsqueda de sucesores ni evalúa las consecuencias a largo plazo de sus acciones para optimizar una función
de utilidad.

**4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?**
Representa una proporción de mercado asignada a otras empresas generada mediante una función sintética y aleatoria, con fines estrictamente didácticos. No
permite afirmar el comportamiento comercial real ni la cuota de mercado verídica de ninguna empresa competidora, ya que es una construcción matemática que
no se correlaciona con la dinámica real del transporte en la ciudad.

**5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?**
Porque representa información del futuro relativo a la toma de decisión del agente. Incluir este archivo en la percepción del agente en el momento
temporal `h` violaría la causalidad estricta (fuga temporal o *data leakage*), asumiendo erróneamente que el agente es capaz de observar y reaccionar a
eventos que aún no han ocurrido en su entorno simulado.

---

## 2. Definición del Entorno (PEAS)

* **Performance (Medida de Rendimiento):** Recomendaciones coherentes con las reglas preestablecidas, estricta ausencia de fuga temporal, abstención
segura ante datos inválidos y trazabilidad de las decisiones históricas.
* **Environment (Entorno):** Secuencia temporal simulada de zona-hora, demanda original **TLC** transformada, flota sintética de la empresa X, comportamiento
sintético de otras empresas y la presencia de un responsable humano.
* **Actuators (Actuadores):** Generación de mensajes y alertas del sistema: `NO_REFORZAR`, `RECOMENDAR_REFUERZO` y `**ABSTENERSE**`.
* **Sensors (Sensores):** Lectura lógica estructurada proveniente del archivo `percepciones.csv` (no constituye un sensor físico de hardware conectado en
tiempo real).

---

## 3. Limitaciones Estructurales a Reconocer

De acuerdo con las premisas del diseño, se asumen las siguientes limitaciones:
* Los viajes (pickups) del dataset **TLC** representan únicamente actividad de *Yellow Taxi* realizada y reportada; no miden la demanda total real ni las
solicitudes no atendidas.
* Asignar que una unidad de capacidad equivale exactamente a un taxi por hora constituye una simplificación del rendimiento logístico real.
* La distancia física entre los centroides de las zonas no es determinante para el cálculo de la duración de los viajes ni para predecir la disponibilidad.
* La acción `RECOMENDAR_REFUERZO` emite únicamente un mensaje en bitácora para ser evaluado por un operador humano; no emite una orden ejecutiva ni
realiza un traslado físico automatizado de la flota.