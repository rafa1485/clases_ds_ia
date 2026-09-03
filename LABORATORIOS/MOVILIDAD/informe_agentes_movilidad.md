# Informe breve — Agentes de Movilidad

## 1. Descripción

Se implementaron dos agentes reactivos para decidir si una compañía ficticia X debería considerar un refuerzo de cobertura en una zona:

- **Agente reactivo simple:** decide usando únicamente la percepción actual.
- **Agente reactivo basado en modelo:** mantiene un estado interno con información de horas anteriores.

La variable principal es la **presión**, calculada como:

```text
presion = demanda_x / capacidad_x
```

El umbral utilizado es `0.85`.

---

## 2. Respuestas

### 1. ¿Cuándo ambos agentes producen la misma acción?

Ambos producen `NO_REFORZAR` cuando la presión actual es menor a `0.85`.

También producen `RECOMENDAR_REFUERZO` cuando el agente basado en modelo ya acumula al menos **dos horas consecutivas con presión alta**.

Ante una percepción inválida, ambos deben producir `ABSTENERSE`.

### 2. ¿Cuándo difieren?

Difieren principalmente en la **primera hora con presión alta**.

Por ejemplo, si `presion = 0.90`:

- El agente simple recomienda refuerzo inmediatamente.
- El agente basado en modelo todavía tiene una racha de presión alta igual a `1`, por lo que no recomienda.

Así, el agente simple reacciona al estado actual, mientras que el basado en modelo considera también el historial.

### 3. ¿Por qué el segundo agente es basado en modelo si no planifica?

Porque mantiene un **estado interno** que resume información de percepciones anteriores.

No necesita realizar búsqueda, planificación ni predicción para ser basado en modelo. Su decisión depende de una representación interna del historial reciente.

### 4. ¿Qué representa `tasa_otras_simulada` y qué no puede afirmar?

`tasa_otras_simulada` representa una **participación estimada y simulada de otras compañías** dentro del escenario generado.

No demuestra la participación real del mercado ni permite afirmar cómo se comportan realmente otras empresas. Es una variable construida para el experimento.

### 5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?

Porque contiene información de la **hora futura `h+1`**.

Utilizarla para decidir en `h` produciría **fuga de información temporal (`data leakage`)** y haría que el agente utilizara información que todavía no estaría disponible en una situación real.

---

## 3. PEAS

| Componente | Descripción |
|---|---|
| **Performance** | Decisiones coherentes con las reglas, manejo de datos inválidos, trazabilidad y ausencia de información futura. |
| **Environment** | Zona y horas simuladas, demanda derivada de datos históricos de TLC, flota ficticia de X y participación simulada de otras compañías. |
| **Actuators** | `NO_REFORZAR`, `RECOMENDAR_REFUERZO`, `ABSTENERSE`. |
| **Sensors** | Percepciones de `percepciones.csv`, principalmente presión, demanda, capacidad y hora. |

---

## 4. Limitaciones

- Los datos de TLC corresponden a viajes de **Yellow Taxi reportados** y no representan la demanda total ni todas las solicitudes de transporte.
- La compañía X y las demás compañías son ficticias.
- La relación entre la cantidad de taxis de X y la participación de otras compañías es una **suposición de simulación**, no una estimación real.
- La capacidad utilizada por taxi-hora es una simplificación.
- La distancia entre centroides de zonas no determina por sí sola la duración del viaje ni la disponibilidad de los taxis.
- El agente no predice la demanda ni planifica rutas.
- `RECOMENDAR_REFUERZO` es una recomendación para revisión humana, no una acción ejecutada automáticamente.

---

## 5. Conclusión

El agente reactivo simple utiliza únicamente la percepción actual, mientras que el agente basado en modelo incorpora memoria mediante un estado interno. La comparación permite demostrar que el historial puede modificar la decisión ante una misma percepción actual. Además, mantener `h+1` fuera de la percepción garantiza la causalidad temporal del experimento.
