# Semana 6 — Práctica: selección de variables con redes neuronales

Resolución de [`Consignas_seleccion_features_practica.pdf`](Consignas_seleccion_features_practica.pdf).

| Archivo | Consigna |
|---|---|
| [`Practica_Seleccion_Features_1_Regresion_Energia.ipynb`](Practica_Seleccion_Features_1_Regresion_Energia.ipynb) | 1 — Regresión temporal del consumo de electrodomésticos (*Appliances Energy Prediction*) |
| [`Practica_Seleccion_Features_2_Clasificacion_Diagnostico.ipynb`](Practica_Seleccion_Features_2_Clasificacion_Diagnostico.ipynb) | 2 — Clasificación de diagnósticos (*Breast Cancer Wisconsin Diagnostic*) |

Los dos notebooks se entregan **ya ejecutados** (con todas las salidas) y se pueden volver a correr de
punta a punta con *Run All*. Descargan los datos con `ucimlrepo`, así que necesitan internet.

## Cómo correrlos

```bash
pip install ucimlrepo scikit-learn pandas matplotlib jupyter
jupyter notebook
```

Tiempos aproximados: consigna 1 ≈ 15 min (entrena ~35 veces el MLP sobre 13.800 filas); consigna 2 ≈ 3 min.

## Resultados

### Consigna 1 — Regresión (misma RNA `(64, 32)`, partición cronológica 70/15/15, semilla 42)

| Variables | n | Val. MAE | Val. R² | Prueba MAE | Prueba RMSE | Prueba R² |
|---|---|---|---|---|---|---|
| Todas | 30 | 60,8 | −0,29 | 171,3 | 226,2 | −5,19 |
| `hour_sin`, `hour_cos`, `lights`, `T2` | 4 | 47,4 | 0,11 | 50,5 | 89,9 | 0,02 |

### Consigna 2 — Clasificación (misma RNA `(32, 16)`, partición estratificada 341/114/114, semilla 42)

| Variables | n | Val. F1 | Val. FN | Prueba accuracy | Prueba F1 | Prueba recall (M) | Prueba FN |
|---|---|---|---|---|---|---|---|
| Todas | 30 | 0,955 | 1 | 0,956 | 0,940 | 0,929 | 3 |
| Selección L1 | 11 | 0,966 | 1 | 0,956 | 0,941 | 0,952 | 2 |

## Cómo se cumple cada actividad

### Consigna 1

| Actividad | Sección del notebook |
|---|---|
| 1. Descargar, ordenar por `date`, describir variables | §2 (tabla de variables + `describe`) |
| 2. Transformar `date` en atributos (no como texto) | §2: `hour_sin`, `hour_cos`, `day_of_week`; `date` se descarta |
| 3. Asociaciones con `Appliances`, redundancias, `rv1`/`rv2` | §4.2 (Spearman, Pearson, información mutua), §4.3 (mapa de correlación y pares redundantes), §4.4 (`rv1` = `rv2`, sin asociación) |
| 4. Al menos dos subconjuntos (correlación, IM, permutación, regularización) | §5–6: cuatro candidatos (Spearman + redundancia, IM + redundancia, Lasso L1, permutación) |
| 5. Misma arquitectura, todas vs. subconjunto | §7: una sola función `crear_rna()` para todos los experimentos |
| 6. Partición temporal, sin usar prueba para seleccionar | §3 (antes de explorar); los rankings solo usan train; la prueba se usa una vez (§10) |
| 7. MAE, RMSE, R²; estabilidad, redundancia y fugas | §7, §8 (bloques temporales y semillas), §9–§11 |

### Consigna 2

| Actividad | Sección del notebook |
|---|---|
| 1. Verificar clases, escalas y correlaciones; excluir identificador | §2 (clases, `ID` excluido, escalas), §4 (correlaciones) |
| 2. Redundancia radio/perímetro/área/textura y sus resúmenes | §4.1 y §4.2 |
| 3. Al menos dos subconjuntos (ANOVA, IM, RFE, L1, permutación) | §5: cuatro candidatos (ANOVA + redundancia, IM + redundancia, L1, RFE) |
| 4. Misma arquitectura y particiones, 30 vs. subconjunto | §6: una sola función `crear_rna()` |
| 5. Partición estratificada; escalado y selección solo con train | §3; `StandardScaler` dentro del `Pipeline`; en la CV la selección se rehace dentro de cada fold (§5.1) |
| 6. Accuracy, precisión, recall, F1, matriz de confusión; foco en malignos no detectados | §6 y §8 (columna FN en todas las tablas + matrices de confusión) |
| 7. Justificar considerando desempeño, estabilidad y cantidad | §5.2 (Jaccard entre folds), §6.1 (semillas), §7 |

### Criterio común

En ambos notebooks solo cambia la lista de columnas: arquitectura, particiones, semilla,
preprocesamiento y métricas son las del código inicial y se definen una única vez.

## Notas

- **Corrección al código inicial (consigna 1):** `ucimlrepo` entrega `date` sin espacio entre fecha y
  hora (`"2016-01-1117:00:00"`) y `pd.to_datetime(df["date"])` falla. Se usa
  `format="%Y-%m-%d%H:%M:%S"`; está comentado en el notebook.
- Se silencian los `ConvergenceWarning` del MLP (el código inicial usa `max_iter` fijo y a veces llega al
  tope); no afectan la comparación.
- Los controles con varias semillas son **adicionales**: la comparación principal usa siempre la semilla 42.
