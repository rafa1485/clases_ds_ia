# Informe: agentes reactivos para refuerzo de taxis

**Autoras:** Silvero – Caviglione
**Zona:** 161 (Midtown Center) · **Decisión al cerrar la hora:** 8 · **Taxis de X:** 20
**Escenario reproducible:** semilla 42, 3 horas de historia

```bash
python simulador_entorno_agente.py --zona 161 --hora 8 --taxis-x 20 \
  --horas-historia 3 --semilla 42 --salida-dir escenario_agente
python plantilla_agentes_movilidad.py  # genera bitacora_agentes.csv
python -m pytest test_agentes_movilidad.py -q
```

## Bitácora sobre el escenario

| hora | presion | racha_presion_alta | accion_simple | accion_modelo |
|---|---|---|---|---|
| 6 | 0.95 | 1 | `RECOMENDAR_REFUERZO` | `NO_REFORZAR` |
| 7 | 1.75 | 2 | `RECOMENDAR_REFUERZO` | `RECOMENDAR_REFUERZO` |
| 8 | 3.25 | 3 | `RECOMENDAR_REFUERZO` | `RECOMENDAR_REFUERZO` |

La hora 6 es exactamente el punto donde los dos agentes se separan: el simple
dispara con el primer valor por encima del umbral, el basado en modelo espera a
que la presión persista. El archivo completo, con los motivos textuales de cada
regla, está en [`bitacora_agentes.csv`](bitacora_agentes.csv).

## Respuestas

**1. ¿En qué situaciones ambos agentes producen la misma acción?**
Cuando la percepción es inválida (ambos `ABSTENERSE`), cuando la presión está
por debajo de 0.85 (ambos `NO_REFORZAR`) y cuando la presión alta ya lleva dos
o más horas consecutivas (ambos `RECOMENDAR_REFUERZO`). En el escenario, las
horas 7 y 8.

**2. ¿Cuándo reaccionan de forma diferente?**
En la primera hora de un episodio de presión alta: el simple recomienda
refuerzo de inmediato (`presion >= 0.85`) y el basado en modelo todavía
responde `NO_REFORZAR` porque su racha vale 1. También difieren cuando una
percepción inválida corta la secuencia: el modelo reinicia la racha, de modo
que la siguiente hora alta vuelve a contar como primera. El simple es más
sensible (reacciona antes, con más falsos positivos ante picos aislados); el
basado en modelo es más específico (filtra el ruido de una hora, a costa de
llegar una hora tarde).

**3. ¿Por qué el segundo agente está basado en modelo aunque no planifique?**
Porque no decide solo con la percepción actual: mantiene un estado interno
(`racha_presion_alta`, `presion_anterior`, `percepcion_valida`) que resume la
historia observada, y ese resumen es lo que le permite distinguir situaciones
que en el instante presente son indistinguibles. Eso es un modelo del mundo,
no una planificación: sigue siendo reactivo porque aplica reglas
condición-acción sobre el estado actualizado. No genera sucesores, no explora
un espacio de estados, no busca caminos ni evalúa consecuencias futuras de sus
propias acciones.

**4. ¿Qué representa `tasa_otras_simulada` y qué no permite afirmar?**
Es la proporción **sintética** de viajes de la zona que el simulador asigna a
otras empresas, sorteada como
`clip(q_min + (q_max−q_min)/(1 + n_X/n_ref) + ε, q_min, q_max)` con
`ε ~ N(0, σ)`: acotada, aleatoria e inversamente proporcional a la flota de X.
Es una hipótesis didáctica para repartir la demanda. **No** permite afirmar
nada sobre la competencia real: no es una cuota de mercado observada, no
proviene de los datos TLC (que solo contienen viajes Yellow Taxi realizados y
reportados, sin identificar empresas), no informa cuántos vehículos tienen
otras compañías, y no sostiene ninguna conclusión de negocio sobre
competidores reales.

**5. ¿Por qué `resultado_h_mas_1.csv` no puede formar parte de la percepción?**
Porque contiene el resultado de la hora `h+1`, es decir, precisamente lo que la
decisión intenta anticipar. Usarlo sería fuga temporal: el agente estaría
mirando el futuro que todavía no ocurrió en el momento de decidir, y su
desempeño aparente no diría nada sobre su utilidad. Rompe la causalidad del
problema (al cerrar la hora 8 esa información no existe) e invalida la
evaluación, ya que ese archivo es justamente el criterio con el que se juzgan
las recomendaciones. Por eso se lo mantiene como conjunto de evaluación
posterior: `cargar_percepciones()` rechaza el archivo de entrada si trae alguna de esas
columnas, y dos pruebas comprueban que inyectar `necesita_refuerzo` o
`taxis_adicionales_sugeridos` en la percepción no altera ninguna decisión.

## PEAS

| Elemento | Contenido |
|---|---|
| **Performance** | Recomendaciones consistentes con las reglas condición-acción (umbral 0.85; racha ≥ 2 para el basado en modelo), ausencia de fuga temporal (ninguna decisión consulta `h+1`), abstención explícita ante datos faltantes, no numéricos, negativos o capacidad ≤ 0, y trazabilidad: cada acción viaja con un motivo textual que cita el valor que la disparó. |
| **Environment** | Secuencia simulada zona-hora (zona TLC 161, horas 6–8 de un lunes), demanda TLC transformada, flota sintética de X (20 taxis, constante), otras empresas representadas por una tasa sintética, y una persona responsable que recibe la recomendación y decide. Entorno parcialmente observable (no se ve la flota ajena), estocástico, secuencial, dinámico y discreto por horas. |
| **Actuators** | Los mensajes `NO_REFORZAR`, `RECOMENDAR_REFUERZO` y `ABSTENERSE`, cada uno acompañado de su motivo. El agente **no** ejecuta traslados ni elige zona de origen: solo emite una recomendación. |
| **Sensors** | Lectura lógica de `percepciones.csv` (un registro por hora cerrada, hasta `h`). No es un sensor conectado en tiempo real ni un GPS de flota: es una lectura de archivo sobre datos simulados. |

## Limitaciones

- **Los datos son sintéticos.** La partición entre X y otras empresas, y por lo
  tanto `demanda_x` y `presion`, dependen de una fórmula inventada con fines
  didácticos. Ninguna conclusión aplica a una operación real.
- **La capacidad es una simplificación grosera:** un taxi = una unidad de
  capacidad por hora, flota constante, sin tiempos de viaje, sin traslados
  entre zonas, sin turnos ni disponibilidad parcial.
- **El umbral 0.85 y la racha ≥ 2 son parámetros fijados por consigna**, no
  calibrados contra ningún costo real de sub- o sobre-refuerzo.
- **No es un predictor.** Ninguno de los dos agentes estima la demanda de
  `h+1`; extrapolan una regla desde lo ya observado.
- **Escenario corto.** La historia disponible son 3 horas, todas con presión
  alta, así que la bitácora real no ejercita el camino `NO_REFORZAR` por
  presión baja ni la abstención; esos casos se cubren en
  `test_agentes_movilidad.py`.
- **La abstención es conservadora:** un dato inválido reinicia la racha, de
  modo que una interrupción en la serie hace que el basado en modelo vuelva a
  necesitar dos horas altas consecutivas.
- **Sin evaluación de aciertos.** El informe no compara las recomendaciones
  contra `resultado_h_mas_1.csv`; ese archivo se reserva como evaluación
  posterior y deliberadamente no se toca desde el código de decisión.


