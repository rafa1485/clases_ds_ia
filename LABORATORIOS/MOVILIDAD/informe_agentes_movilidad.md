# Informe: Agentes reactivos para refuerzo de taxis

## Bitácora del escenario reproducible

Escenario generado con: zona `161` (Midtown Center), hora de decisión `h=8`,
`20` taxis de X, 3 horas de historia, semilla `42`.

| hora | presion | racha_presion_alta | accion_simple       | motivo_simple                           | accion_modelo       | motivo_modelo                                                              |
|------|---------|--------------------|---------------------|-----------------------------------------|---------------------|----------------------------------------------------------------------------|
| 6    | 1.15    | 1                  | RECOMENDAR_REFUERZO | Presion alta observada (1.15 >= 0.85)  | NO_REFORZAR         | Presión alta durante 1 hora(s); se requieren al menos 2 horas consecutivas |
| 7    | 1.95    | 2                  | RECOMENDAR_REFUERZO | Presion alta observada (1.95 >= 0.85)  | RECOMENDAR_REFUERZO | Presión alta persistente durante 2 horas consecutivas                      |
| 8    | 3.10    | 3                  | RECOMENDAR_REFUERZO | Presion alta observada (3.10 >= 0.85)  | RECOMENDAR_REFUERZO | Presión alta persistente durante 3 horas consecutivas                      |

---

## Respuestas a las preguntas

### 1. ¿En qué situaciones ambos agentes producen la misma acción?

Ambos agentes coinciden en dos casos:

- **Presión baja** (`presion < 0.85`): ambos devuelven `NO_REFORZAR`, ya que ninguna regla activa se dispara.
- **Dos o más horas consecutivas con presión alta**: una vez que el estado interno del agente basado en modelo acumula `racha_presion_alta >= 2`, su acción se alinea con la del agente simple, que siempre recomienda refuerzo ante presión alta.

En el escenario ejecutado, ambos coinciden en las horas 7 y 8 (ambos `RECOMENDAR_REFUERZO`) y coincidirían en presión baja si esta se presentara.

### 2. ¿Cuándo reaccionan de forma diferente?

El único caso de divergencia observable es **la primera hora en que se registra presión alta**. En ese momento:

- El agente **simple** ya recomienda refuerzo (solo evalúa la percepción actual).
- El agente **basado en modelo** todavía devuelve `NO_REFORZAR` porque `racha_presion_alta = 1`, que no alcanza el umbral de 2 horas consecutivas.

En el escenario, esto ocurre en la hora 6: el agente simple recomendó refuerzo mientras el agente modelo esperó hasta tener confirmación histórica en la hora 7.

### 3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?

El agente basado en modelo **mantiene un estado interno** (`racha_presion_alta`, `presion_anterior`, `ultima_accion`) que representa un resumen de la historia del entorno que ya no puede percibir directamente. Esto es exactamente la definición de "basado en modelo" según Russell & Norvig: el agente construye un modelo del mundo para compensar la parcialidad de su percepción actual.

No es un planificador porque no genera ni evalúa secuencias de acciones futuras; simplemente aplica reglas condición-acción sobre ese estado persistente. La diferencia con un agente puramente reactivo es que su decisión depende de observaciones anteriores, no únicamente de la percepción del instante actual.

### 4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?

`tasa_otras_simulada` es una **proporción sintética** generada aleatoriamente por el simulador para distribuir los viajes TLC entre la empresa X y otras empresas ficticias. Su valor se sortea usando una relación inversa al número de taxis de X más ruido gaussiano.

**Lo que no permite afirmar:**

- No representa la participación de mercado real de ninguna empresa.
- No proviene de datos observados sobre otras empresas; los datos TLC originales solo registran viajes Yellow Taxi realizados.
- No puede usarse para inferir cuántos vehículos tienen las otras empresas ni su estrategia operativa.
- La relación inversa entre flota de X y `tasa_otras_simulada` es una hipótesis didáctica no calibrada con datos reales.

### 5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?

Porque contiene información sobre la hora `h+1`, es decir, el **futuro respecto al momento de decisión**. El agente debe decidir al finalizar la hora `h` si recomienda refuerzo para `h+1`. Utilizar `resultado_h_mas_1.csv` constituiría una **fuga temporal** (*data leakage*): el agente estaría tomando una decisión con información que todavía no existe en el momento real de la acción, haciendo que la evaluación sea inválida y el sistema no deployable en producción.

---

## PEAS mínimo

| Elemento    | Contenido                                                                                                                                                                     |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Performance**  | Recomendaciones coherentes con las reglas condición-acción; ausencia de fuga temporal (nunca se consulta `h+1`); abstención ante datos inválidos o faltantes; trazabilidad mediante el campo `motivo` en cada decisión. |
| **Environment**  | Secuencia simulada zona-hora basada en datos Yellow Taxi TLC 2024; demanda transformada sintéticamente para dividir entre empresa X (flota constante) y otras empresas ficticias; responsable humano que recibe la recomendación y decide el traslado. |
| **Actuators**    | Tres mensajes simbólicos: `NO_REFORZAR` (no hay evidencia suficiente), `RECOMENDAR_REFUERZO` (se aconseja revisión humana para reforzar) y `ABSTENERSE` (percepción inválida o insuficiente para aplicar la política con seguridad). |
| **Sensors**      | Lectura lógica de `percepciones.csv`, que contiene una fila por hora observada con campos derivados (presión, demanda, capacidad, etc.); no es un sensor conectado en tiempo real sino un archivo de entrada estático. |

---

## Limitaciones reconocidas

- Los pickups TLC representan actividad Yellow Taxi **realizada y reportada**, no demanda total del mercado ni solicitudes no atendidas.
- La empresa X y las "otras empresas" son **entidades ficticias** creadas exclusivamente para el ejercicio; no corresponden a ninguna empresa real.
- La relación inversa entre la flota de X y `tasa_otras_simulada` es una **hipótesis didáctica** no estimada con datos reales.
- La simplificación de **una unidad de capacidad por taxi-hora** no refleja la disponibilidad real (desplazamientos, tiempos muertos, zonas de origen).
- La distancia entre centroides de zonas no determina la duración ni la disponibilidad real de los vehículos.
- `RECOMENDAR_REFUERZO` es un **mensaje para revisión humana**, no una orden ejecutada automáticamente ni un traslado completado.
- La política del agente simple puede generar falsos positivos ante presiones altas transitorias; la del agente modelo puede generar falsos negativos en el primer ciclo de presión alta.
