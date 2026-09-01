# Informe: agentes reactivos para refuerzo de taxis

## Escenario utilizado

- Zona TLC: 161 (Midtown Center)
- Hora de decisión: 8 (usando historia de las horas 6, 7 y 8)
- Taxis de X: 20
- Semilla: 42
- Resultado: ver [`bitacora_agentes.csv`](bitacora_agentes.csv)

## Respuestas

### 1. ¿En qué situaciones ambos agentes producen la misma acción?

Coinciden en dos casos. Primero, cuando la presión es baja (`presion < 0.85`): el agente simple da `NO_REFORZAR` porque la percepción actual no supera el umbral, y el agente basado en modelo también da `NO_REFORZAR` porque `racha_presion_alta` queda en 0. Segundo, cuando ya hay dos o más horas consecutivas de presión alta (por ejemplo horas 7 y 8 de la zona 161, con racha 2 y 3): ahí el simple recomienda porque la presión actual ya supera 0.85, y el modelo también recomienda porque `racha_presion_alta >= 2`. En ambos casos coinciden porque, una vez que la racha "se estabiliza" (siempre baja o ya sostenida por dos horas), el resumen de historia del agente con modelo deja de aportar información distinta a la que ya da la percepción instantánea.

### 2. ¿Cuándo reaccionan de forma diferente?

Divergen en la **primera** hora de presión alta después de una racha baja (por ejemplo la hora 6 de la zona 161, con `presion=1.15` y `racha_presion_alta=1`): el agente simple recomienda refuerzo de inmediato porque solo mira la percepción actual, mientras que el agente basado en modelo todavía da `NO_REFORZAR` porque su racha acumulada (1) no llega al umbral de persistencia (2). También pueden divergir en sentido contrario si el estado interno quedó "contaminado" por una racha previa alta y la percepción actual es inválida o de transición, aunque en este TP ese caso se resuelve reseteando la racha ante datos inválidos.

### 3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?

Porque mantiene un estado interno (`racha_presion_alta`, `presion_anterior`, `percepcion_valida`, `ultima_accion`) que resume lo que pasó en percepciones anteriores y lo usa para decidir junto con la percepción actual — es decir, su decisión depende de la **historia**, no solo del instante presente. Eso es justamente lo que define a un agente "basado en modelo": tiene un modelo interno (aunque sea mínimo, un contador de racha) del mundo que actualiza en cada paso. Sigue siendo reactivo porque aplica reglas condición-acción directas sobre ese estado (no genera sucesores, no explora alternativas ni busca un camino óptimo), así que no llega a ser un agente planificador ni basado en objetivos/utilidad.

### 4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?

Representa la proporción de viajes de la zona que el entorno le asignó sintéticamente a "otras empresas" en esa hora, sorteada con la fórmula `qotras = clip(qmin + (qmax - qmin)/(1 + nX/nref) + ε, qmin, qmax)`. No permite afirmar que exista una relación real e inversa entre la flota de X y la participación de otras empresas, porque esa relación es una hipótesis didáctica del enunciado, no algo estimado con datos reales de mercado. Tampoco permite inferir el número real de vehículos de otras empresas, ni su comportamiento real: es un valor aleatorio y acotado, no una medición.

### 5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?

Porque contiene información posterior a la hora en la que se toma la decisión (la evaluación de lo que efectivamente pasó en `h+1`), y usarla violaría la causalidad temporal del problema: el agente tiene que decidir con lo que sabe hasta `h`, no con el resultado que se quiere predecir o evaluar. Si `decidir_reactivo_simple`, `actualizar_estado` o `decidir_reactivo_modelo` consultaran ese archivo, habría fuga de información del futuro hacia la decisión (data leakage), y la recomendación dejaría de ser una decisión reactiva basada en percepción para convertirse en una trampa que "adivina" el resultado que se supone debe recomendar sin conocer.

## PEAS mínimo

| Elemento    | Contenido                                                                                                                                                                                                                                                                                       |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Performance | Recomendaciones coherentes con las reglas de la consigna (umbral de presión y racha), ausencia de fuga temporal (no se usa `resultado_h_mas_1.csv`), abstención ante percepciones inválidas o con capacidad desconocida, y trazabilidad de cada decisión mediante el `motivo` devuelto.         |
| Environment | Secuencia simulada zona-hora (zona 161, horas 6-8 en este escenario), demanda TLC transformada en `percepciones.csv`, flota sintética y constante de X (20 taxis), participación aleatoria de otras empresas sintéticas, y un responsable humano que recibe la recomendación y decide si actúa. |
| Actuators   | Los tres mensajes de salida: `NO_REFORZAR`, `RECOMENDAR_REFUERZO` y `ABSTENERSE`. No hay ningún actuador que mueva taxis: la "acción" del agente es solo un mensaje para revisión humana.                                                                                                       |
| Sensors     | Lectura lógica de las columnas de `percepciones.csv` (`presion`, `capacidad_x`, etc.) hasta la hora `h`. No es un sensor conectado en tiempo real: es una lectura de un archivo generado previamente por el simulador.                                                                          |

## Limitaciones reconocidas

- Los pickups TLC son actividad Yellow Taxi realizada y reportada, no demanda total ni solicitudes no atendidas.
- X y las otras empresas son entidades ficticias creadas para el ejercicio.
- La relación inversa entre flota de X y participación externa no ha sido estimada con datos reales.
- Una unidad de capacidad por taxi-hora es una simplificación.
- La distancia entre centroides no determina duración ni disponibilidad.
- `RECOMENDAR_REFUERZO` es un mensaje para revisión humana, no una orden ni un traslado ejecutado.
