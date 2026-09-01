# Informe: agentes reactivos para refuerzo de taxis

## Escenario reproducible utilizado

Se usó exactamente el escenario de ejemplo de `consigna_agentes_movilidad.md`:

```bash
python simulador_entorno_agente.py \
  --zona 161 \
  --hora 8 \
  --taxis-x 20 \
  --horas-historia 3 \
  --semilla 42 \
  --salida-dir escenario_agente
```

Zona `161` (Midtown Center), decisión al cierre de la hora 8, 20 taxis de X,
3 horas de historial visible, semilla `42`. El comando generó
`escenario_agente/percepciones.csv` (entrada permitida) y
`escenario_agente/resultado_h_mas_1.csv` (reservado, no usado para decidir).

`generar_bitacora.py` leyó únicamente `percepciones.csv` y corrió
`procesar_secuencia` para producir `bitacora_agentes.csv`:

| hora | presión | racha_presion_alta | acción simple | acción modelo |
|---:|---:|---:|---|---|
| 6 | 1.15 | 1 | `RECOMENDAR_REFUERZO` | `NO_REFORZAR` |
| 7 | 1.95 | 2 | `RECOMENDAR_REFUERZO` | `RECOMENDAR_REFUERZO` |
| 8 | 3.10 | 3 | `RECOMENDAR_REFUERZO` | `RECOMENDAR_REFUERZO` |

En este escenario la presión ya está por encima del umbral (0.85) desde la
primera hora observable, así que sirve para mostrar exactamente el efecto que
pide comprobar la consigna: la hora 6 es la primera con presión alta dentro
de la ventana visible, y ahí los dos agentes difieren.

## Respuestas

### 1. ¿En qué situaciones ambos agentes producen la misma acción?

Coinciden en dos casos: (a) cuando la presión está por debajo del umbral,
porque ninguno de los dos encuentra evidencia para recomendar refuerzo; y
(b) cuando la presión alta ya lleva **dos o más horas consecutivas**, porque
ahí la condición del agente simple (presión actual alta) y la del agente con
memoria (racha ≥ 2) se cumplen al mismo tiempo. En la bitácora esto se ve en
las horas 7 y 8: ambos devuelven `RECOMENDAR_REFUERZO`. También coinciden
cuando la percepción es inválida: los dos abstienen.

### 2. ¿Cuándo reaccionan de forma diferente?

Difieren en la transición: la primera hora en que la presión cruza el
umbral después de un período bajo (o después del arranque del historial).
El agente simple no tiene memoria, así que reacciona de inmediato con esa
única observación. El agente con memoria exige confirmar el patrón durante
una segunda hora antes de recomendar, para no reaccionar a un pico aislado
que podría ser ruido. La hora 6 de la bitácora es exactamente ese caso:
presión 1.15 (≥0.85), racha recién en 1, simple recomienda y el basado en
modelo todavía no.

### 3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?

"Basado en modelo" no significa que planifique ni busque una secuencia de
acciones hacia un objetivo (eso sería un agente planificador o basado en
objetivos/utilidad). Significa que mantiene un **modelo interno del mundo**
—en este caso, un resumen de un aspecto no observable directamente en la
percepción actual: cuántas horas consecutivas lleva la presión alta— y usa
ese modelo para interpretar la percepción presente. Sigue siendo una regla
condición-acción (reactivo), pero la condición se evalúa sobre el estado
actualizado, no solo sobre el dato crudo de esta hora. Es la definición
clásica de "agente reactivo basado en modelo": reactivo en la decisión,
pero con memoria de la historia relevante.

### 4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?

Representa una proporción de viajes que el entorno le asigna de forma
sintética a "otras empresas", calculada con una fórmula didáctica (una curva
que decrece cuando crece `taxis_x`, más ruido aleatorio) — no es un dato
observado ni estimado con información real de mercado. Por lo tanto no
permite afirmar cuál es la participación real de otras empresas de taxis,
ni que exista una relación causal real entre el tamaño de la flota de X y el
comportamiento de sus competidores: es una hipótesis inventada para poder
generar el ejercicio, según aclara explícitamente la consigna.

### 5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?

Porque contiene información de la hora `h+1`, es decir, posterior al
instante en el que el agente debe decidir. Un agente que decide en tiempo
real nunca podría observar el resultado de una hora que todavía no ocurrió;
usarlo sería una fuga de información desde el futuro (violación de
causalidad temporal) y invalidaría la comparación, porque el agente ya no
estaría "prediciendo" sino copiando la respuesta.

## PEAS

| Elemento | Contenido en este trabajo |
|---|---|
| **Performance** | Recomendaciones coherentes con las reglas de presión y racha, cero uso de datos de `h+1`, abstención ante percepciones inválidas o con capacidad desconocida, y motivo trazable en cada decisión (`motivo_simple` / `motivo_modelo`). |
| **Environment** | Secuencia zona-hora simulada (zona 161, horas 6 a 8 de un lunes), demanda TLC real transformada por el simulador, flota sintética de 20 taxis de X constante, participación sintética de "otras empresas", y una persona humana que recibe la recomendación y decide si actuar. |
| **Actuators** | Los tres mensajes de salida: `NO_REFORZAR`, `RECOMENDAR_REFUERZO`, `ABSTENERSE`. Ninguno ejecuta un traslado real. |
| **Sensors** | Lectura de `percepciones.csv`, fila por fila, en orden temporal; no es un sensor en tiempo real ni conectado a un sistema en producción. |

## Limitaciones

- Los pickups de TLC son viajes de Yellow Taxi realizados y reportados, no
  demanda total de movilidad ni solicitudes que quedaron sin atender.
- La empresa X y las "otras empresas" son entidades ficticias creadas para
  este ejercicio; no representan compañías reales.
- La relación inversa entre el tamaño de la flota de X y la participación de
  otras empresas (`tasa_otras_simulada`) es una hipótesis didáctica, no una
  relación estimada con datos reales.
- Se supone que cada taxi aporta exactamente una unidad de capacidad por
  hora; es una simplificación que ignora tiempos de viaje, reposicionamiento
  y disponibilidad real.
- La distancia entre centroides de zona (usada en otras partes del
  simulador) no determina duración ni disponibilidad real de un taxi.
- `RECOMENDAR_REFUERZO` es un mensaje para que una persona lo evalúe; no es
  una orden automática ni ejecuta un traslado de vehículos.
- **Efecto de borde del historial exportado:** el estado del agente con
  memoria se reinicia vacío al principio de la ventana visible
  (`crear_estado_inicial`). Esto significa que si la presión ya venía alta
  *antes* de la primera hora exportada (hora 6 en este escenario), el agente
  con memoria no puede saberlo y trata esa primera hora como si fuera la
  primera vez que ocurre. Con `--horas-historia` más grande este efecto se
  reduce, pero nunca desaparece del todo: siempre hay un instante inicial en
  el que la racha arranca en cero por definición, no porque se haya
  verificado que la presión estaba baja antes.
