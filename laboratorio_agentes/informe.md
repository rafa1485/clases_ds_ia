# Informe: Agentes Reactivos para Refuerzo de Taxis

**Asignatura / Trabajo:** Trabajo Práctico: Agentes reactivos para refuerzo de movilidad  
**Archivos asociados:** [`agentes_movilidad.py`](file:///c:/Users/imano/OneDrive/Escritorio/IA/clases_ds_ia/laboratorio_agentes/agentes_movilidad.py), [`test_agentes_movilidad.py`](file:///c:/Users/imano/OneDrive/Escritorio/IA/clases_ds_ia/laboratorio_agentes/test_agentes_movilidad.py), [`bitacora_agentes.csv`](file:///c:/Users/imano/OneDrive/Escritorio/IA/clases_ds_ia/laboratorio_agentes/bitacora_agentes.csv)

---

## 1. Respuestas a las Preguntas Teóricas y Metodológicas

### 1. ¿En qué situaciones ambos agentes producen la misma acción?
Ambos agentes coinciden en las siguientes condiciones:
1. **Presión baja sostenida (`presion < 0.85`):** Cuando la demanda asignada a la empresa X no satura su capacidad disponible, ambos agentes determinan `NO_REFORZAR`.
2. **Presión alta persistente (`presion >= 0.85` por 2 o más horas consecutivas):** Una vez que la racha de alta presión alcanza `racha_presion_alta >= 2`, tanto el reactivo simple (que evalúa el instante actual) como el basado en modelo (que confirma la persistencia) emiten `RECOMENDAR_REFUERZO`.
3. **Percepciones inválidas o incompletas:** Ante datos faltantes, valores nulos/NaN, tipos de datos erróneos o capacidades no positivas ($\le 0$), ambos agentes detectan la anomalía y devuelven `ABSTENERSE`.

### 2. ¿Cuándo reaccionan de forma diferente?
Reaccionan de forma diferente en la **primera hora en que la presión supera o iguala el umbral (`presion >= 0.85`, con `racha_presion_alta == 1`) tras haber estado baja o al iniciar el monitoreo:**
- **Agente Reactivo Simple:** Al no poseer memoria, reacciona instantáneamente al valor observado en $h$ y emite `RECOMENDAR_REFUERZO`, siendo vulnerable a falsas alarmas provocadas por picos espurios o transitorios de demanda.
- **Agente Basado en Modelo:** Al evaluar su estado interno, identifica que la condición de alta demanda no tiene suficiente persistencia histórica (`racha = 1 < 2`) y decide `NO_REFORZAR`, esperando una segunda observación consecutiva para confirmar la tendencia antes de sugerir una movilización de recursos.

### 3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?
En la formulación canónica de Inteligencia Artificial (Russell & Norvig), un agente está **basado en modelo** si mantiene un **estado interno** que modela aspectos del entorno no observables directamente en la percepción actual.
En este caso, la historia temporal (horas consecutivas con alta presión `racha_presion_alta` y validez acumulada) no está presente en la fotografía instantánea de la hora $h$. El agente actualiza su representación interna del mundo ($s_{t} = f(s_{t-1}, p_t)$) y toma decisiones en función de dicho estado ($a_t = g(s_t)$). No requiere búsqueda prospectiva en árbol ni algoritmos de planificación para ser clasificado como agente basado en modelo.

### 4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?
- **Qué representa:** Representa una proporción sintética y estocástica de viajes capturada por competidores ficticios, calculada mediante una curva didáctica inversamente proporcional a la flota de X ($q_{\text{otras}} \in [0.15, 0.75]$) con perturbación gaussiana ($\varepsilon \sim N(0, 0.05)$).
- **Qué NO permite afirmar:**
  - No refleja la cuota de mercado real de competidores (ej. Uber, Lyft) en la ciudad de Nueva York.
  - No estima la cantidad real de vehículos o capacidad de la competencia.
  - No describe elasticidad económica real ni comportamientos estratégicos de mercado.

### 5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?
Porque violaría el principio de **causalidad temporal** introduciendo **fuga de datos del futuro** (*temporal data leakage*).
Al finalizar la hora $h$, los eventos de la hora $h+1$ aún no han ocurrido. Un agente en producción solo puede basar sus decisiones en información observada hasta $h$. El archivo `resultado_h_mas_1.csv` se reserva exclusivamente para evaluación post-hoc (auditoría o validación del impacto de la recomendación).

---

## 2. Especificación PEAS

| Componente | Descripción Detallada |
|---|---|
| **Performance** (Medida de Rendimiento) | - Coherencia estricta de las recomendaciones con las políticas definidas.<br>- Minimización de falsos positivos ante picos aislados (mediante filtro de persistencia).<br>- Detección robusta de anomalías y abstención segura ante datos inválidos.<br>- Causalidad temporal estricta (cero fuga de información de $h+1$).<br>- Trazabilidad y claridad en la justificación de cada recomendación emitida. |
| **Environment** (Entorno) | - Secuencia temporal horaria de viajes simulados por zona TLC de NYC (ej. Zona 161 Midtown Center).<br>- Flota constante y simplificada de la empresa X.<br>- Demanda sintética de competidores generada con ruido estocástico.<br>- Parcialmente observable (el pasado no viene en la percepción actual), discreto (horas), secuencial y estocástico. |
| **Actuators** (Actuadores) | - Salida estructurada de mensajes informativos: `NO_REFORZAR`, `RECOMENDAR_REFUERZO`, `ABSTENERSE`.<br>- Cadena de texto con el motivo y justificación de la regla/estado aplicado.<br>- Destinatario: Operador humano (no ejecuta movimientos autónomos de flota). |
| **Sensors** (Sensores) | - Lector lógico de registros estructurados horarias (`percepciones.csv` / DataFrame).<br>- Variables percibidas en $h$: `zona_id`, `zona`, `hora`, `taxis_x`, `demanda_total`, `demanda_x`, `capacidad_x`, `presion`. |

---

## 3. Limitaciones Reconocidas

1. **Naturaleza de los datos base (TLC Yellow Taxi):** Los registros originales solo contabilizan viajes efectivamente iniciados y completados; no miden la demanda latente insatisfecha ni a usuarios que desistieron de viajar.
2. **Empresas y competencia sintéticas:** La partición entre la empresa X y competidores es un ejercicio didáctico simulado, no una división real de mercado.
3. **Hipótesis simplificada de participación:** La fórmula inversamente proporcional entre flota propia y participación externa es una hipótesis didáctica no calibrada con modelos econométricos reales.
4. **Capacidad fija por taxi:** Asumir que 1 taxi provee exactamente 1 unidad de capacidad por hora abstrae la duración real de los viajes, distancias de retorno y demoras por congestión.
5. **Geometría y centroides:** La distancia entre centroides de zonas no refleja la red vial, tiempos de viaje dinámicos ni disponibilidad geográfica intra-zona.
6. **Alcance de la acción:** `RECOMENDAR_REFUERZO` es una sugerencia consultiva para supervisión humana; no constituye una orden operativa de reubicación física de vehículos.

---

## 4. Análisis de la Bitácora del Escenario Reproducible

Sobre el escenario generado para la **Zona 161 (Midtown Center)** con 20 taxis al cierre de la **Hora 8** con 3 horas de historia (`h=6, 7, 8`), se obtuvo la siguiente bitácora ([`bitacora_agentes.csv`](file:///c:/Users/imano/OneDrive/Escritorio/IA/clases_ds_ia/laboratorio_agentes/bitacora_agentes.csv)):

| hora | presion | racha_presion_alta | accion_simple | motivo_simple | accion_modelo | motivo_modelo |
|:---:|:---:|:---:|:---|:---|:---|:---|
| **6** | 0.95 | 1 | `RECOMENDAR_REFUERZO` | Presión actual (0.95) >= 0.85. | `NO_REFORZAR` | Presión alta aislada (racha = 1 hora); se requiere persistencia de al menos 2 horas. |
| **7** | 1.75 | 2 | `RECOMENDAR_REFUERZO` | Presión actual (1.75) >= 0.85. | `RECOMENDAR_REFUERZO` | Presión alta persistente (2 horas consecutivas >= 0.85). |
| **8** | 3.25 | 3 | `RECOMENDAR_REFUERZO` | Presión actual (3.25) >= 0.85. | `RECOMENDAR_REFUERZO` | Presión alta persistente (3 horas consecutivas >= 0.85). |

### Conclusiones del Escenario
- En la **hora 6**, se evidencia claramente la diferencia entre agentes: el simple reacciona precipitadamente ante el pico inicial de 0.95, mientras que el basado en modelo aguarda confirmación.
- En las **horas 7 y 8**, la presión se mantiene alta (1.75 y 3.25 respectivamente). Al consolidarse la racha en 2 y 3 horas consecutivas, el agente basado en modelo activa la recomendación de refuerzo con plena justificación basada en su memoria interna.
