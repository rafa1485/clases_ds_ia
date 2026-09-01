# Consignas de revisión — TP Agentes de Movilidad

Esta guía es para que el equipo revise el 100% de la
entrega del TP `consigna_agentes_movilidad.pdf` antes de entregarlo. Seguir
los pasos en orden; cada uno indica qué mirar, cómo verificarlo y contra qué
parte exacta de la consigna se contrasta.

## 0. Preparación

- [ ] Estar parado en `LABORATORIOS/MOVILIDAD/` (o ajustar rutas).
- [ ] Tener Python 3 instalado y correr, desde la raíz del repo:
  ```bash
  python -m pip install -r requirements.txt
  ```
- [ ] Confirmar que existen los 4 archivos que pide la sección **"Entrega"**
      de la consigna, más los auxiliares de reproducibilidad:
  - [ ] `agentes_movilidad.py`
  - [ ] `test_agentes_movilidad.py`
  - [ ] `bitacora_agentes.csv`
  - [ ] `informe.md`
  - [ ] (auxiliares) `escenario_agente/percepciones.csv`,
        `escenario_agente/resultado_h_mas_1.csv`, `generar_bitacora.py`

## 1. Revisar el agente reactivo simple (`decidir_reactivo_simple`)

Abrir `agentes_movilidad.py` y contrastar contra la tabla de la sección
**"Parte 1"** de la consigna:

| Condición esperada | Cómo verificarla en el código |
|---|---|
| Faltan datos, hay valores inválidos o la capacidad es desconocida → `ABSTENERSE` | Revisar `_percepcion_valida`: ¿chequea que existan `presion` y `capacidad_x`? ¿rechaza `NaN`/infinito? ¿rechaza `capacidad_x <= 0`? |
| `presion >= 0.85` → `RECOMENDAR_REFUERZO` | Confirmar que la comparación es `>=` (no `>`) contra `UMBRAL_PRESION = 0.85`. |
| `presion < 0.85` → `NO_REFORZAR` | Confirmar el `else`. |
| No usa variables globales mutables ni observaciones anteriores | Confirmar que la función **no** lee ni modifica nada fuera de su parámetro `percepcion` (no hay `global`, no hay listas/diccionarios definidos fuera de la función que se modifiquen). |
| No usa el archivo de evaluación futura | Confirmar que la función no importa ni abre `resultado_h_mas_1.csv` en ningún lado. |

- [ ] Las 5 filas de la tabla verificadas.

## 2. Revisar el agente basado en modelo (`actualizar_estado` + `decidir_reactivo_modelo`)

Contrastar contra la sección **"Parte 2"**:

- [ ] El estado inicial (`crear_estado_inicial`) tiene exactamente las 4
      claves que pide la consigna: `percepcion_valida`, `racha_presion_alta`,
      `presion_anterior`, `ultima_accion`.
- [ ] `actualizar_estado`: con percepción inválida, ¿deja el estado en una
      condición que fuerza `ABSTENERSE` (es decir, `percepcion_valida=False`)?
- [ ] `actualizar_estado`: con `presion >= 0.85`, ¿incrementa
      `racha_presion_alta` en 1 respecto al estado anterior?
- [ ] `actualizar_estado`: con `presion < 0.85`, ¿reinicia la racha a 0?
- [ ] `decidir_reactivo_modelo`: percepción inválida → `ABSTENERSE`.
- [ ] `decidir_reactivo_modelo`: racha ≥ 2 → `RECOMENDAR_REFUERZO`.
- [ ] `decidir_reactivo_modelo`: cualquier otro estado válido → `NO_REFORZAR`.
- [ ] Ninguna de las dos funciones recibe como parámetro nada que permita
      leer datos de `h+1` (mirar la firma: `actualizar_estado(estado_anterior,
      percepcion)`, `decidir_reactivo_modelo(estado_actual)`).

## 3. Correr los tests obligatorios

```bash
python -m pytest test_agentes_movilidad.py -v
```

- [ ] Los 8 tests pasan (`8 passed`).
- [ ] Verificar que estén los casos que pide literalmente la sección
      **"Pruebas obligatorias"**:
  - [ ] Presión baja → ambos `NO_REFORZAR`.
  - [ ] Primera hora con presión alta → simple recomienda, modelo no.
  - [ ] Segunda hora consecutiva con presión alta → ambos recomiendan.
  - [ ] Prueba decisiva: dos historias distintas que terminan en la misma
        percepción; el simple da la misma acción en las dos, el de modelo
        puede diferir.
  - [ ] Alguna prueba que compruebe que ninguna función de decisión usa
        datos de `h+1` (en este TP: `test_funciones_de_decision_no_reciben_datos_futuros`
        y `test_procesar_secuencia_ignora_cambios_futuros`).
- [ ] Abrir cada test y confirmar que el nombre/aserción realmente prueba lo
      que dice probar (no alcanza con que "pase"; tiene que estar probando
      la condición correcta).

## 4. Verificar la reproducibilidad del escenario

```bash
python simulador_entorno_agente.py --zona 161 --hora 8 --taxis-x 20 \
  --horas-historia 3 --semilla 42 --salida-dir escenario_agente_verificacion
```

- [ ] Comparar `escenario_agente_verificacion/percepciones.csv` contra
      `escenario_agente/percepciones.csv` ya entregado: deben ser
      **idénticos** (misma semilla, mismos datos TLC congelados).
- [ ] Confirmar que `percepciones.csv` solo contiene horas hasta la `h`
      indicada (8), y que `resultado_h_mas_1.csv` contiene solo la hora 9.
- [ ] Borrar la carpeta de verificación una vez comparada, para no dejar
      basura en el repo.

> Nota sobre Windows: el script `simulador_movilidad.py`
> utiliza `tempfile.TemporaryDirectory` en la función
> `cargar_centros_zonas` para asegurar compatibilidad en Windows sin
> bloqueos de archivos en la descarga y lectura del shapefile.

## 5. Verificar la bitácora contra las reglas, a mano

Abrir `bitacora_agentes.csv` (o correr `python generar_bitacora.py` de
nuevo, debe dar el mismo resultado) y, para cada fila:

- [ ] `accion_simple` coincide con la regla de umbral 0.85 aplicada a la
      columna `presion` de esa misma fila (sin mirar otras filas).
- [ ] `racha_presion_alta` es coherente con la fila anterior: si `presion`
      de esta fila es `>= 0.85`, la racha debe ser `racha_anterior + 1`; si
      no, debe ser `0`.
- [ ] `accion_modelo` es `RECOMENDAR_REFUERZO` si y solo si
      `racha_presion_alta >= 2`.
- [ ] Las columnas `motivo_simple` y `motivo_modelo` explican la decisión
      (no están vacías ni son genéricas).

## 6. Revisar el informe (`informe.md`)

- [ ] Están respondidas las 5 preguntas de la consigna, y cada respuesta
      usa evidencia concreta de la bitácora generada (no solo teoría
      genérica).
- [ ] La tabla PEAS tiene los 4 elementos (`Performance`, `Environment`,
      `Actuators`, `Sensors`) y describe el escenario **real** usado (zona,
      cantidad de taxis, horas), no una descripción abstracta.
- [ ] Están las 6 limitaciones que la consigna exige reconocer
      textualmente (sección **"Limitaciones que deben reconocerse"**), sin
      reformularlas de forma que pierdan el sentido original.
- [ ] Ninguna afirmación del informe dice que el sistema predice demanda
      real, optimiza una flota real, o que `RECOMENDAR_REFUERZO` ejecuta
      una acción — repasar el **"Propósito"** de la consigna, que
      explícitamente excluye esto.

## 7. Chequeo cruzado contra la rúbrica de evaluación

Para cada criterio de la tabla **"Evaluación"** de la consigna, marcar dónde
está la evidencia:

| Criterio (2 puntos c/u) | Evidencia a mostrar |
|---|---|
| Agente reactivo simple y validación de entradas | `decidir_reactivo_simple` + tests de percepción inválida/capacidad desconocida |
| Actualización correcta del estado interno | `actualizar_estado` + test de racha (paso 2 y 3) |
| Política del agente basado en modelo | `decidir_reactivo_modelo` + test de 2 horas consecutivas |
| Pruebas, bitácora y demostración de dependencia histórica | `test_agentes_movilidad.py` completo + `bitacora_agentes.csv` + test de historias distintas |
| PEAS, causalidad temporal y discusión de limitaciones | `informe.md` completo + tests de no uso de `h+1` |

- [ ] Los 5 criterios tienen evidencia identificable y verificable.

## 8. Defensa individual

Cada integrante del grupo debería poder, sin mirar el código:

- [ ] Explicar con sus palabras la diferencia entre el agente simple y el
      basado en modelo, con un ejemplo propio (no el de la bitácora).
- [ ] Señalar en qué parte del código se garantiza que no hay fuga de datos
      de `h+1`.
- [ ] Explicar por qué `tasa_otras_simulada` es una hipótesis didáctica y no
      un dato real.
- [ ] Justificar la elección del umbral de racha (2 horas) y qué pasaría si
      se cambiara a 1 o a 3.
