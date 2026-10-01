<style>
@page { size: A4; margin: 16mm 16mm 17mm 16mm; }
body { font-family: "DejaVu Sans", sans-serif; color: #17324d; line-height: 1.38; font-size: 10pt; }
h1 { color: #17324d; border-bottom: 4px solid #007f82; padding-bottom: 8px; }
h2 { color: #17324d; border-bottom: 2px solid #e2a33a; padding-bottom: 4px; margin: 20px 0 8px; page-break-after: avoid; }
h3 { color: #007f82; margin: 12px 0 4px; page-break-after: avoid; }
h4 { color: #536471; margin: 9px 0 3px; page-break-after: avoid; }
p { margin: 6px 0; }
ul, ol { margin-top: 4px; margin-bottom: 8px; }
blockquote { border-left: 4px solid #e2a33a; background: #f3f6f8; margin: 10px 0; padding: 8px 12px; page-break-inside: avoid; }
table { border-collapse: collapse; width: 100%; font-size: 8.7pt; }
th { background: #17324d; color: white; }
th, td { border: 1px solid #aab7c1; padding: 6px; vertical-align: top; }
code { color: #007f82; }
strong { color: #17324d; }
</style>

# Guía docente: Introducción a la Ciencia de Datos

**Curso:** Data Science

**Semana y clase:** semana 1, clase 1

**Presentación asociada:** *Introducción a la Ciencia de Datos: de una necesidad a evidencia útil para decidir* (40 diapositivas)

**Fuentes principales:** capítulos 1 y 2 del libro *Ciencia de Datos e Inteligencia Artificial*

### Propósito y forma de uso

Esta guía sincroniza cada marco con qué mostrar, distinguir y comprobar. La clase comienza con una necesidad, la evidencia posible y la decisión que apoyaría, no con software.

El caso transversal es una empresa de **movilidad urbana**. Se conservan unidad **zona-franja**, horizonte de **treinta minutos** y decisión humana de operaciones. Un **modelo** representa o estima; la **evidencia** es un resultado evaluado; la **decisión** selecciona bajo restricciones; la **autoridad humana** aprueba, modifica, rechaza, ejecuta y responde.

### Recorrido de la clase

| Bloque | Diapositivas | Resultado esperado |
|---|---:|---|
| Apertura y concepto | 1-6 | Delimitar Ciencia de Datos y entender los datos como representaciones |
| Proceso y propósitos | 7-14 | Explicar el ciclo, clasificar preguntas y separar descripción, predicción y decisión |
| Formulación | 15-18 | Especificar problema, unidad, población, alcance, corte y horizonte |
| Organización del trabajo | 19-30 | Comparar metodologías, estructuras, fuentes y reproducibilidad |
| Caso aplicado | 31-34 | Formular movilidad, distinguir tareas y detectar fuga temporal |
| Producción y defensa | 35-37 | Elaborar, revisar y defender una ficha del problema |
| Cierre | 38-40 | Recuperar siete ideas, leer la síntesis visual y orientar la continuidad |

> **Tesis de la clase:** un proyecto de datos es un sistema de producción de evidencia para una decisión. Un modelo puede formar parte de ese sistema, pero no reemplaza la formulación, la validación, la responsabilidad ni la autoridad de uso.

## Diapositiva 1. Introducción a la Ciencia de Datos

**Correspondencia con el libro.** Capítulo 1, propósito y §1.1.1; capítulo 2, propósito.

**Propósito.** Instalar la pregunta rectora: datos o modelo no equivalen a saber qué hacer.

**Guion sugerido.** Decir: “Hoy no empezaremos preguntando qué algoritmo usar, sino qué situación modificar, qué observar y quién podría actuar”. La evidencia es un resultado evaluado dentro de límites; el conocimiento agrega interpretación y reglas de uso; la decisión elige una acción; la autoridad reside en personas y organizaciones. Anticipar el caso estable de movilidad.

**Conceptos y términos.** *Necesidad*: situación que se busca comprender o modificar. *Evidencia*: información evaluada dentro de condiciones. *Conocimiento*: patrones interpretados con experiencia y reglas. *Decisión*: selección de una acción. “Útil” exige pertinencia, oportunidad y uso posible.

**Ejemplo de movilidad.** Reducir espera sin más cancelaciones mediante evidencia zona-franja; operaciones decide para los próximos treinta minutos.

**Error frecuente o límite.** Equiparar Ciencia de Datos y aprendizaje automático, o prometer impacto desde un pronóstico.

**Comprobación.** “¿Quién ejecuta legítimamente un traslado?”. El responsable autorizado; dato, predicción y recomendación son insumos.

**Conclusión que debe quedar.** La clase estudiará la cadena completa entre una necesidad y una decisión, no una colección de técnicas aisladas.

**Transición sugerida.** “Para saber qué exigiremos al final, hagamos explícito el propósito de la clase”.

## Diapositiva 2. Propósito de la clase

**Correspondencia con el libro.** Capítulo 1, §§1.1.1, 1.1.4-1.1.6; capítulo 2, objetivos de aprendizaje y §§2.1-2.4.

**Propósito.** Convertir los cinco resultados en una definición de la formulación y la argumentación, no del entrenamiento.

**Guion sugerido.** Leer los resultados como capacidades conectadas: distinguir objetos; separar descripción, predicción y prescripción; fijar unidad, población, alcance y horizonte; organizar el trabajo mediante *workflow*, **Descubrimiento de Conocimiento en Bases de Datos (KDD, por *Knowledge Discovery in Databases*)** y **Proceso Estándar Intersectorial para Minería de Datos (CRISP-DM, por *Cross-Industry Standard Process for Data Mining*)**; aplicar todo a zona-franja. Las siglas se definen aquí por ser su primera aparición.

**Conceptos y términos.** *Workflow*: actividades, entradas, salidas, controles y retornos. KDD incluye minería dentro del descubrimiento; CRISP-DM organiza el proyecto completo. *Procedencia* registra origen y transformaciones; *reproducibilidad* permite reconstruir resultados.

**Ejemplo de movilidad.** Explicar fila zona-franja, población, datos al corte y autoridad sobre traslados.

**Error frecuente o límite.** Memorizar definiciones sin detectar incoherencias ni aplicar conceptos.

**Comprobación.** “¿Por qué el horizonte distingue entrada y fuga?”. Por momento de decisión y disponibilidad.

**Conclusión que debe quedar.** La coherencia entre pregunta, unidad, tiempo, método y decisión es el criterio transversal de la sesión.

**Transición sugerida.** “Probemos ese criterio con una frase deliberadamente amplia: mejorar el servicio”.

## Diapositiva 3. Pregunta de apertura

**Correspondencia con el libro.** Capítulo 2, §§2.1 y 2.1.1; capítulo 1, §1.1.6.

**Propósito.** Separar intención y problema verificable.

**Guion sugerido.** Presentar “mejorar el servicio” sin corregirla. Organizar respuestas según las columnas y conectar sus preguntas: la unidad coincide con la acción, los datos llegan antes y el valor observa consecuencias. Aplicar la prueba contrafactual: si el pronóstico cambiara, ¿cambiaría una acción disponible?

**Conceptos y términos.** *Usuario*: quien emplea el producto, no necesariamente quien resulta afectado. *Acción disponible*: intervención autorizada y factible. *Valor*: mejora bajo costos y riesgos. *Éxito*: condición verificable fijada de antemano.

**Ejemplo de movilidad.** Reducir espera alta sin más cancelaciones; decidir a las 09:00 para 09:00-09:30 sobre zona-franja.

**Composición visual relevante.** Arriba están situación y pregunta; abajo, comprensión y uso en dos columnas. Alternarlas evita relegar la operación.

**Error frecuente o límite.** Dejar que columnas disponibles definan el problema o usar objetivos no observables.

**Comprobación.** Si la distribución no cambia con la salida, no hay decisión asociada; puede quedar valor descriptivo.

**Conclusión que debe quedar.** Antes de abrir datos se necesita una hipótesis explícita sobre usuario, unidad, acción, tiempo y valor.

**Transición sugerida.** “Ahora podemos definir la disciplina por el tipo de trabajo que hace, no por una herramienta”.

## Diapositiva 4. ¿Qué es la Ciencia de Datos?

**Correspondencia con el libro.** Capítulo 1, §1.1.1 y síntesis; capítulo 2, propósito.

**Propósito.** Definir Ciencia de Datos y sus productos legítimos.

**Guion sugerido.** Recorrer tres verbos: obtener exige interpretar representaciones; comunicar hace comprensibles incertidumbre y límites; apoyar preserva la autoridad humana. Programar, graficar o entrenar son actividades, no la disciplina completa. Si la incertidumbre crítica es cobertura u oportunidad, el producto correcto puede ser un inventario o auditoría.

**Conceptos y términos.** *Interdisciplinario* reúne preguntas no sustituibles. *Modelo*: representación o función. *Auditoría*: examen contra criterios. *Estimación*: cuantificación con incertidumbre. *Recomendación*: comparación sin autoridad propia.

**Ejemplo de movilidad.** Un inventario de posicionamiento satelital, una auditoría de latencia o un perfil zona-franja pueden preceder al pronóstico.

**Composición visual relevante.** Leer definición, contraste “no se reduce a/producto apropiado” y alerta final; no hay progresión obligatoria.

**Error frecuente o límite.** Definir la disciplina por Python, volumen o predicción.

**Comprobación.** Pedir un producto no predictivo útil para el caso. Son válidos un diccionario, un análisis de cobertura, una visualización de cuantiles o una prueba de integración.

**Conclusión que debe quedar.** Ciencia de Datos diseña evidencia para una pregunta y uso; el modelo es una pieza posible.

**Transición sugerida.** “Esa evidencia parte de datos; por eso debemos abandonar la idea de que el registro es la realidad misma”.

## Diapositiva 5. Los datos representan, no reproducen

**Correspondencia con el libro.** Capítulo 1, §1.1.1; capítulo 2, introducción de §2.3 y §§2.3.4-2.3.6.

**Propósito.** Mostrar que todo dato es producido por un mecanismo situado y que error, sesgo, cobertura y selección no son detalles posteriores.

**Guion sugerido.** Partir del fenómeno y preguntar si cabe completo en una fila. Sensor, regla y canal determinan registros de hora, ubicación o reclamo. *Error* es discrepancia; *sesgo*, desviación sistemática; *cobertura*, qué puede observarse; *selección*, qué casos entran. No reclamar no demuestra ausencia de demora.

**Conceptos y términos.** El **Sistema de Posicionamiento Global (GPS)** estima posición, velocidad y tiempo; depende de dispositivo, recepción, entorno y latencia. Como ampliación didáctica, no fórmula literal del libro, $x_{obs}=g(z,instrumento,contexto)+\varepsilon$: $z$ es el fenómeno, $g$ el mecanismo o función de observación y $\varepsilon$ el error; no supone que toda pérdida sea ruido recuperable.

**Descripción detallada del diagrama.** El diagrama representa la producción de un registro, no un flujo operativo. La caja azul superior “Fenómeno: demoras en la ciudad” es el referente amplio. La caja verde central “Proceso de observación” codifica transformación y enumera sensor, regla y canal. La caja amarilla inferior “Registro” codifica el dato materializado: hora, GPS o reclamo. Las flechas azules continuas indican dependencia: el fenómeno se observa mediante un proceso y ese proceso produce registros; no significan copia exacta ni causalidad exhaustiva. A la derecha, una caja clara “Queda fuera” enumera contexto, silencios, error y selección. La flecha verde discontinua que sale del proceso hacia esa caja marca pérdidas y exclusiones, no una fase deseable ni retroalimentación temporal. Orden de lectura: fenómeno, proceso, registro y desvío hacia lo que queda fuera; cerrar con las cuatro preguntas mínimas de la columna derecha. Interpretación válida: el significado y los límites del dato dependen de cómo se obtuvo. Inferencia incorrecta: que todo lo omitido pueda medirse o corregirse después, o que un sensor elimine selección. Ejemplo oral: un GPS puede registrar un vehículo detenido, pero no distinguir por sí solo congestión, espera deliberada o pérdida de señal. Pregunta visual: “¿En qué caja se origina que solo ciertos pasajeros reclamen?”. En proceso de observación y selección, no en el fenómeno exclusivamente. Conclusión visual: entre mundo y registro siempre hay una transformación auditable.

**Ejemplo de movilidad.** GPS, reclamos y `hora_real` observan partes distintas, con coberturas y relojes diferentes.

**Error frecuente o límite.** Llamar objetivo al sensor, igualar ausencia y cero, o creer que volumen elimina sesgo.

**Comprobación.** Ante `GPS=(0,0)`, distinguir ubicación, error y ausencia mediante especificación y procedencia.

**Conclusión que debe quedar.** Un dato es una representación parcial producida, con observaciones y ausencias que deben explicarse.

**Transición sugerida.** “Si el registro no es todavía conocimiento, veamos qué trabajo agrega cada transición”.

## Diapositiva 6. De datos a conocimiento

**Correspondencia con el libro.** Capítulo 1, §1.1.1, distinción entre datos, información, conocimiento y decisión; capítulo 2, síntesis.

**Propósito.** Diferenciar niveles epistemológicos y mostrar por qué la trazabilidad debe cubrir interpretaciones, no solo archivos.

**Guion sugerido.** Los datos codifican; la información organiza con unidad, periodo y fuente; el conocimiento interpreta patrones con experiencia y reglas; la decisión delibera y actúa. La evidencia respalda una afirmación evaluada. Cada transición agrega contexto y supuestos: excluir cancelados, interpretar causalmente o deliberar con objetivos incompletos puede sesgarla.

**Conceptos y términos.** *Trazabilidad* reconstruye entradas, transformaciones, interpretaciones y decisiones. *Información* tiene contexto; *conocimiento* no equivale a patrón novedoso; *deliberación* compara consecuencias bajo autoridad.

**Descripción detallada del diagrama.** Cuatro cajas horizontales forman una cadena. La amarilla “Datos” codifica observaciones registradas. Dos cajas verdes, “Información” y “Conocimiento”, representan trabajo de organización e interpretación. La caja dorada “Decisión” destaca intervención humana. Las flechas azules continuas están rotuladas “organizar”, “interpretar” y “deliberar”; los rótulos son operaciones que deben documentarse, no conversiones automáticas. Leer de izquierda a derecha y luego regresar de derecha a izquierda: desde la decisión preguntar qué conocimiento la justifica, qué información lo sostiene y qué datos la originan. La interpretación válida es que cada nivel depende del anterior y agrega contexto. No afirma que toda organización produzca información correcta, que un patrón sea conocimiento verdadero ni que una decisión sea inevitable. Ejemplo oral: eventos GPS se organizan por zona-franja, se interpreta un patrón de demanda, y operaciones considera ese patrón junto con seguridad. Pregunta: “¿Dónde entra el objetivo de no aumentar cancelaciones?”. En conocimiento contextual y deliberación, no en el dato bruto. Conclusión visual: el tránsito es humano, técnico y auditable.

**Ejemplo de movilidad.** GPS es dato; conteos contextualizados, información; patrón interpretado, conocimiento; traslado, decisión.

**Error frecuente o límite.** Presentar una escalera automática o afirmar que “los datos hablan”.

**Comprobación.** “Una tabla de conteos sin definición de zona ni periodo, ¿es ya información utilizable?”. No de forma suficiente: falta contexto para interpretar.

**Conclusión que debe quedar.** La evidencia y el conocimiento se construyen mediante transiciones justificables; la decisión agrega deliberación y autoridad.

**Transición sugerida.** “Ubicaremos ahora esos niveles dentro de la cadena completa que comienza en una necesidad”.

## Diapositiva 7. De la necesidad a la decisión

**Correspondencia con el libro.** Capítulo 2, §2.1.1 y teoría de cambio de §2.1.2; capítulo 1, ciclo general de §1.1.1.

**Propósito.** Establecer correspondencia hacia adelante y hacia atrás entre cada eslabón, y separar evidencia, decisión e impacto.

**Guion sugerido.** Hacia adelante: necesidad, pregunta, datos, análisis, evidencia evaluada, decisión e impacto. Hacia atrás: el impacto define valor; la acción, unidad y oportunidad; la evidencia, evaluación; esta, datos y análisis. La doble lectura evita una salida correcta sin uso.

**Conceptos y términos.** *Correspondencia*: compatibilidad entre eslabones. *Impacto*: consecuencia, no métrica interna. *Teoría de cambio*: conexión argumentada entre salida, interpretación, acción y consecuencia.

**Descripción detallada del diagrama.** Siete nodos horizontales se leen de izquierda a derecha: “Necesidad” y “Impacto” son cajas azul claro que delimitan el dominio; “Pregunta” y “Análisis” son verdes y representan trabajo analítico; “Datos” y “Evidencia” son amarillas y distinguen insumo de resultado validado; “Decisión humana” es dorada y marca autoridad. Seis flechas azules continuas conectan nodos adyacentes. No indican inevitabilidad ni que no haya retornos; solo hacen visible la dependencia principal. Debajo, dos bloques explican lecturas complementarias: hacia adelante, producir evidencia utilizable; hacia atrás, dejar que la decisión determine unidad, oportunidad, evaluación y datos. Orden exacto: nombrar los siete nodos, detenerse entre análisis y evidencia, detenerse entre evidencia y decisión, leer ambos bloques y cerrar con la alerta. Interpretación válida: el modelo, si existe, ocupa parte de “Análisis”. Inferencias incorrectas: que evidencia cause por sí sola impacto, que una decisión humana garantice corrección o que toda necesidad exija modelado. Ejemplo oral: un pronóstico oportuno puede apoyar una reasignación, pero el impacto depende de ejecución y entorno. Pregunta: “¿Qué flecha falla si el resultado llega a las 09:05?”. Evidencia-decisión para el corte de 09:00. Conclusión visual: cada frontera necesita una justificación.

**Ejemplo de movilidad.** Reducir espera; pronosticar zona-franja al corte; evaluar; decidir; observar espera, cancelaciones y cobertura.

**Error frecuente o límite.** Llamar impacto a precisión o atribuir mejora al modelo sin observar acción.

**Comprobación.** Pedir identificar qué eslabón contiene el baseline. Principalmente evaluación de la evidencia, aunque debe definirse desde formulación.

**Conclusión que debe quedar.** Una salida analítica solo adquiere sentido por su correspondencia con una acción y una evaluación reales.

**Transición sugerida.** “La cadena aclara dependencias, pero el trabajo real no avanza una sola vez de izquierda a derecha”.

## Diapositiva 8. El ciclo aprende y vuelve atrás

**Correspondencia con el libro.** Capítulo 1, §1.1.1; capítulo 2, propósito, §§2.2.3-2.2.5 y síntesis.

**Propósito.** Normalizar la iteración como aprendizaje controlado y ubicar autoridad, monitoreo y detención dentro del ciclo.

**Guion sugerido.** Volver no es improvisar: cada retorno registra evidencia. Explorar puede revelar falta de observabilidad; evaluar, no superar el *baseline* o referencia real; usar, cambios en los datos. La autoridad aprueba, ejecuta, revisa y detiene según condiciones previas como cobertura, riesgo o valor.

**Conceptos y términos.** *Iteración*: hipótesis, artefacto, evidencia y decisión. *Monitoreo*: datos, error, uso e impacto. *Detención*: regla para suspender o reformular. *Autoridad efectiva*: tiempo, información y poder.

**Descripción detallada del diagrama.** Cinco cajas forman un anillo. Arriba, “Formular”; a la derecha, “Obtener y representar”; abajo a la derecha, “Analizar y evaluar”; abajo a la izquierda, “Revisar y decidir”; a la izquierda, “Observar impacto”. Las flechas azules continuas recorren el ciclo en sentido horario y regresan desde impacto a formulación. Dos flechas verdes discontinuas acortan el retorno: de análisis a formulación y de revisión a obtención. El trazo discontinuo codifica retroalimentación correctiva, no menor importancia. Leer primero el perímetro completo; después los dos atajos; finalmente la columna de ejemplos y la caja de autoridad. Interpretación válida: hay retornos específicos según el tipo de evidencia. No afirma que todas las etapas deban repetirse siempre ni autoriza cambiar la prueba después de ver resultados. Ejemplo oral: al descubrir que cancelados fueron eliminados, se vuelve a representación; si aun corregido no hay acción útil, se vuelve a formulación. Pregunta: “¿A dónde volvemos si GPS llega tarde?”. A obtención/representación y posiblemente formulación temporal. Conclusión visual: aprender significa revisar decisiones documentadas.

**Ejemplo de movilidad.** Reasignar cambia GPS y demanda futuros; monitoreo separa entorno y política.

**Error frecuente o límite.** Cambiar métricas retrospectivamente o iterar sin retroalimentación semántica.

**Comprobación.** “Si el pronóstico no supera usar la demanda de la franja anterior, ¿qué resultado legítimo tiene la iteración?”. No avanzar, reformular o detener; haber aprendido que la complejidad no aporta bajo ese protocolo.

**Conclusión que debe quedar.** Un ciclo confiable aprende con retornos trazables y permite detenerse.

**Transición sugerida.** “Dentro de este ciclo, el tipo de pregunta determina qué resultado y qué evaluación son pertinentes”.

## Diapositiva 9. Taxonomía de preguntas analíticas

**Correspondencia con el libro.** Capítulo 1, §1.1.1; capítulo 2, §2.1.1.

**Propósito.** Distinguir cinco objetivos que pueden conectarse, pero que no comparten automáticamente evidencia ni criterios de éxito.

**Guion sugerido.** Leer cada fila como pregunta y producto: describir resume; diagnosticar estudia asociaciones, no prueba causas; predecir estima; prescribir compara acciones; monitorear detecta cambios. Pueden conectarse, pero no forman una madurez obligatoria.

**Conceptos y términos.** *Descripción*: observaciones; *diagnóstico*: asociaciones; *predicción*: valor desconocido; *prescripción*: acciones bajo utilidad y restricciones; *monitoreo*: cambio respecto de referencias.

**Lectura detallada de la tabla.** La primera columna nombra objetivo; la segunda, pregunta; la tercera, ejemplo de movilidad. Leer cada fila completa desde describir hasta monitorear; luego la tercera columna verticalmente para mostrar productos distintos. Las filas pueden encadenarse, no equivalen: asociación no garantiza predicción; predicción no contiene costos; monitoreo revisa datos, modelo e impacto. La alerta exige evaluación diferente.

**Ejemplo de movilidad.** Perfiles, lluvia asociada, demanda futura, traslados factibles y monitoreo GPS son objetivos distintos.

**Error frecuente o límite.** Confundir predicción con explicación, diagnóstico con causa o prescripción con ranking.

**Comprobación.** Clasificar cobertura GPS, demanda futura y traslado: monitoreo, predicción y prescripción.

**Conclusión que debe quedar.** El verbo de la pregunta fija qué afirmación puede sostenerse y cómo debe evaluarse.

**Transición sugerida.** “Comencemos por la operación menos exigente en supuestos: resumir lo observado”.

## Diapositiva 10. Describir: resumir lo observado

**Correspondencia con el libro.** Capítulo 1, §§1.1.5 y 1.1.6; capítulo 2, preguntas descriptivas en §2.1.1. Esta diapositiva trata descripción, medias, proporciones y cuantiles, no predicción.

**Propósito.** Enseñar qué resumen responde cada estadístico y qué no puede concluirse de una descripción.

**Guion sugerido.** Una distribución reparte valores y frecuencias. La media resume balance; la proporción, una fracción; los cuantiles, posiciones ordenadas. El **percentil 90 (P90)** deja aproximadamente 90 % de observaciones por debajo o igual y 10 % por encima; muestra una cola que la media puede ocultar. Todo resumen depende de población, periodo, unidad y faltantes.

**Lectura de la fórmula.** En $\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i$, $x_i$ es el valor de la observación $i$, $n$ la cantidad incluida, $\sum$ suma todos los valores, $1/n$ divide por el conteo y $\bar{x}$ es la media muestral. Supone valores comparables y una regla clara de inclusión; no exige normalidad para calcularse, pero puede ser sensible a extremos. En $\widehat p=\frac{1}{n}\sum_{i=1}^{n}\mathbb{1}(y_i=1)$, la función indicadora vale 1 si se cumple la condición y 0 si no; la suma cuenta casos y la división produce proporción. El sombrero indica estimación desde la muestra. Ninguna fórmula prueba causa, representa casos ausentes ni anticipa automáticamente otra franja. Un cuantil $q_{0.90}$, ampliación didáctica, satisface aproximadamente $P(X\le q_{0.90})=0.90$; con muestras y empates existen convenciones de cálculo, por lo que debe documentarse el método.

**Conceptos y términos.** *Distribución*: valores y frecuencias; *media*: promedio aritmético; *proporción*: parte del total; *cuantil*: posición acumulada; *segmento*: subconjunto definido.

**Composición visual relevante.** Las fórmulas ocupan el centro conceptual. Debajo, la caja izquierda enumera productos y la derecha aterriza movilidad; leer fórmula, producto general y aplicación concreta. La alerta final impide el salto de asociación a causa o de pasado a futuro.

**Ejemplo de movilidad.** Para cada zona-franja se informa cantidad de viajes, mediana y P90 de espera, proporción de cancelaciones y cobertura GPS. P90 de 18 minutos significa que aproximadamente 90 % de esperas observadas no superó 18 y 10 % sí; no significa que cada usuario espere 18 ni que el próximo P90 será igual.

**Error frecuente o límite.** Promediar zonas con distinta cantidad de viajes sin explicar ponderación; excluir cancelados porque no tienen `hora_real`; interpretar P90 como “90 % de probabilidad para el próximo caso”.

**Comprobación.** “Dos zonas tienen media de diez minutos, pero P90 de doce y veinticinco. ¿Son equivalentes?”. No: la segunda tiene una cola alta mucho más severa.

**Conclusión que debe quedar.** Describir exige elegir resúmenes que conserven el aspecto relevante de la distribución y declarar su alcance.

**Transición sugerida.** “Resumir observaciones conocidas no responde cuánto valdrá una franja todavía no observada”.

## Diapositiva 11. Predecir: estimar lo no observado

**Correspondencia con el libro.** Capítulo 1, §§1.1.3, 1.1.5 y 1.1.6; capítulo 2, §§2.1.1 y 2.1.5. El foco es predicción y evaluación fuera del ajuste.

**Propósito.** Definir predicción mediante cantidades condicionales y explicar por qué generalización, partición y baseline son parte de la tarea.

**Guion sugerido.** Una predicción estima un futuro, etiqueta no medida o resultado costoso. La **distribución condicional** $P(Y\mid X)$ conserva resultados posibles e incertidumbre; la **esperanza condicional** $\mathbb E[Y\mid X]$ resume su promedio. La barra se lee “dado”, no “causado por”. Evaluar fuera del ajuste exige casos no usados para estimar ni elegir, respetando tiempo, grupos y duplicados.

**Lectura de la fórmula.** En $\widehat P(Y\mid X)$, $Y$ es el resultado desconocido, $X$ el conjunto de entradas disponibles, $P$ una distribución condicional y el sombrero indica que se estima desde datos. Puede devolver probabilidades de demanda baja, media o alta. En $\widehat{\mathbb E}[Y\mid X]$, $\mathbb E$ es una media teórica condicionada y el sombrero vuelve a indicar estimación. Si la pérdida es cuadrática, la esperanza condicional suele ser el objetivo puntual natural, pero eso no la convierte en valor seguro. Las expresiones suponen que $X$ existirá con semántica y oportunidad comparables y que la evaluación representa el uso. No permiten concluir causalidad, baja incertidumbre individual, utilidad operativa ni estabilidad ante cambio de población.

**Conceptos y términos.** *Ajuste*: estimar parámetros; *generalización*: funcionar en casos nuevos; *partición temporal*: reservar periodos posteriores; *baseline*: alternativa pertinente, como último valor o patrón estacional.

**Ejemplo de movilidad.** A las 09:00 se estima demanda de cada zona durante 09:00-09:30 con solicitudes recibidas, disponibilidad de flota, calendario y señales oportunas. El modelo se compara en semanas posteriores con un baseline estacional.

**Error frecuente o límite.** Reportar error de entrenamiento, elegir el candidato usando repetidamente la prueba o mezclar filas dependientes de una misma zona y momento en ambos lados. Un error bajo tampoco demuestra que la acción derivada mejore espera.

**Comprobación.** “¿Por qué no basta ocultar al azar 20 % de filas?”. Porque el uso es futuro y existen dependencias temporales, zonales y duplicados que una división aleatoria puede compartir.

**Conclusión que debe quedar.** Predecir exige entradas disponibles al uso y una evaluación independiente que reproduzca la generalización pretendida.

**Transición sugerida.** “Pongamos lado a lado la pregunta retrospectiva y la prospectiva para no confundir sus productos”.

## Diapositiva 12. Describir no es predecir

**Correspondencia con el libro.** Capítulo 1, §1.1.5; capítulo 2, §2.1.1. Esta lámina contrasta describir frente a predecir.

**Propósito.** Mostrar que una descripción puede inspirar una hipótesis predictiva, pero no garantiza error bajo en casos futuros.

**Guion sugerido.** Contrastar las preguntas inferiores: demoras observadas frente a demanda no observada. Luego comparar productos: media, cuantiles y distribución frente a probabilidad condicional y error futuro. Usar una regularidad histórica para pronosticar agrega un supuesto de estabilidad: es hipótesis, no garantía.

**Conceptos y términos.** *Error futuro*: discrepancia en casos de uso; *estabilidad*: relaciones transferibles; *hipótesis predictiva*: información que anticipa sin afirmar causa.

**Descripción detallada del diagrama.** Dos tarjetas claras grandes se alinean horizontalmente. La izquierda, “Descripción”, contiene “resume casos observados” y símbolos de media, cuantiles y distribución. La derecha, “Predicción”, contiene “estima casos no observados”, probabilidad condicional y error futuro. Una flecha azul de izquierda a derecha está rotulada “hipótesis, no garantía”: indica que patrones descriptivos pueden motivar predicción, no que la descripción se transforme automáticamente ni que la relación sea unidireccional obligatoria. Debajo de cada tarjeta hay una caja amarilla con su pregunta de movilidad. Orden exacto: preguntas inferiores, tarjetas superiores, flecha, bloque de prueba decisiva. Interpretación válida: ambos análisis pueden usar las mismas fuentes, pero cambian población de evaluación y afirmación. No afirma que predecir sea superior, que toda descripción preceda cronológicamente a todo modelo o que una explicación histórica carezca de valor. Ejemplo oral: la zona A tuvo alta demanda los lunes; solo una evaluación en lunes posteriores dirá si el patrón pronostica. Pregunta: “¿Qué elemento visual introduce la necesidad de evaluación futura?”. La tarjeta derecha y su “error futuro”. Conclusión visual: describir caracteriza lo visto; predecir debe responder por lo no visto.

**Ejemplo de movilidad.** Un mapa de P90 de espera del mes pasado identifica concentración observada. Un pronóstico para la próxima franja necesita un corte, entradas oportunas y comparación en fechas no ajustadas.

**Error frecuente o límite.** Presentar una curva histórica bien ajustada como validación prospectiva o afirmar que el grupo con mayor media seguirá siendo el de mayor demanda.

**Comprobación.** Pedir una evidencia adicional para pasar de descripción a predicción. Respuesta: desempeño contra baseline en periodos posteriores, con partición y disponibilidad realistas.

**Conclusión que debe quedar.** Explicar bien el pasado no implica anticipar bien el futuro.

**Transición sugerida.** “Incluso un buen pronóstico deja abierta otra pregunta: qué acción conviene”.

## Diapositiva 13. Predecir no es decidir

**Correspondencia con el libro.** Capítulo 1, §§1.1.2, 1.1.5 y 1.2.4; capítulo 2, §§2.1.1, 2.1.4 y 2.1.5. Esta lámina contrasta predecir frente a decidir.

**Propósito.** Separar estimación, comparación de acciones y autoridad, incorporando incertidumbre, utilidad y factibilidad.

**Guion sugerido.** La predicción presenta demanda e incertidumbre; la política compara costos, restricciones y consecuencias; el responsable aprueba, modifica o rechaza. Una acción factible satisface restricciones duras. La utilidad representa consecuencias valoradas, no una verdad natural. Autoridad efectiva exige tiempo, información y poder para detener.

**Lectura de la fórmula.** En $a^*=\arg\max_{a\in\mathcal A}\mathbb E[U(a,S)\mid X]$, $\mathcal A$ es el conjunto de acciones factibles, $a$ una candidata, $S$ un estado incierto del entorno, $U(a,S)$ la utilidad o valoración de las consecuencias de ejecutar $a$ si ocurre $S$, y $X$ la evidencia disponible. $\mathbb E$ pondera la utilidad sobre estados posibles; $\arg\max$ devuelve la acción que alcanza el mayor valor esperado, no el valor numérico. $a^*$ es una recomendación bajo ese modelo. Supone estados, probabilidades, utilidad y restricciones suficientemente especificados. No demuestra que la utilidad sea justa, que se hayan incluido todas las consecuencias, que la acción sea legal ni que la persona deba obedecer.

**Descripción detallada del diagrama.** Tres cajas horizontales se conectan por flechas azules. La amarilla “Predicción: demanda + incertidumbre” es evidencia cuantitativa. La verde “Comparar acciones: costos, restricciones, consecuencias” representa la política de decisión. La dorada “Responsable: aprueba, modifica o rechaza” marca autoridad. A la derecha, la fórmula formaliza únicamente la comparación, y tres viñetas repiten fronteras: modelo informa, política compara, persona decide. Leer predicción, comparación, fórmula, responsable y alerta inferior. Los colores distinguen dato, proceso y humano; no representan niveles de calidad. Interpretación válida: una predicción puede alimentar varias decisiones según restricciones. No afirma que siempre haya una función de utilidad completa, que la persona sea infalible o que “humano en el circuito” baste sin autoridad. Ejemplo oral: demanda alta en B puede no justificar traslado si deja A bajo cobertura mínima. Pregunta: “¿Dónde se excluye mover un vehículo no disponible?”. En $\mathcal A$ y en la caja de restricciones. Conclusión visual: entre pronóstico y acción hay una política explícita y una autoridad.

**Ejemplo de movilidad.** El sistema estima demanda alta con intervalo amplio. Compara mantener, mover uno o mover dos vehículos. Mover dos viola cobertura mínima; mover uno es reversible. Operaciones incorpora un cierre vial no capturado y rechaza, registrando motivo.

**Error frecuente o límite.** Convertir probabilidad alta en orden, esconder restricciones duras como costos negociables o llamar supervisión a una aprobación rutinaria sin información.

**Comprobación.** “¿Puede rechazarse una predicción muy precisa?”. Sí: puede llegar tarde, no cambiar acciones, implicar riesgo o no superar una alternativa operativa.

**Conclusión que debe quedar.** Una predicción estima; una política compara; una persona u órgano autorizado decide.

**Transición sugerida.** “Sostener estas fronteras requiere perspectivas diferentes coordinadas alrededor de la evidencia”.

## Diapositiva 14. Una disciplina interdisciplinaria

**Correspondencia con el libro.** Capítulo 1, §§1.1.1 y 1.1.4; capítulo 2, §2.2.5.

**Propósito.** Mostrar qué pregunta aporta cada disciplina y por qué ninguna perspectiva aislada garantiza evidencia útil y confiable.

**Guion sugerido.** No presentar áreas como departamentos. Estadística aborda variabilidad e inferencia; matemática, objetivos y restricciones; computación, representación y escala; ingeniería, pruebas y operación; dominio, significado; comunicación, comprensión y uso. Gobernanza y autoridad atraviesan todas. Una persona puede cubrir roles, no omitir preguntas.

**Conceptos y términos.** *Inferencia* relaciona muestra y población. *Observabilidad operativa* revela estado y fallos mediante registros; difiere de observabilidad conceptual. *Plausibilidad* no es prueba. Comunicar incluye incertidumbre y límites.

**Descripción detallada del diagrama.** Un círculo verde central dice “Evidencia útil y confiable”. Seis tarjetas claras lo rodean: estadística arriba a la izquierda, matemática arriba, computación arriba a la derecha, ingeniería abajo a la derecha, dominio abajo y comunicación abajo a la izquierda. Cada tarjeta tiene una flecha azul hacia el centro; la convergencia indica contribución conjunta. No hay flechas entre disciplinas ni una jerarquía. Leer en sentido horario desde estadística y, para cada nodo, formular su pregunta; después señalar el centro y la alerta. La interpretación válida es complementariedad. No afirma que todas las tareas requieran igual dedicación, que el consenso elimine conflicto o que evidencia confiable resulte automáticamente de reunir perfiles. Ejemplo oral: estadística evalúa error, ingeniería asegura llegada antes de las 09:00, dominio valida cancelaciones y comunicación presenta abstención. Pregunta: “¿Qué nodo detectaría que una zona cambió de límites?”. Dominio e ingeniería/computación conjuntamente. Conclusión visual: optimizar una sola contribución puede optimizar la parte equivocada.

**Ejemplo de movilidad.** Operaciones define acciones; ingeniería conserva tiempos de evento y recepción; estadística diseña evaluación; cartografía valida zonas; legal y gobernanza revisan ubicación; comunicación diseña evidencia que pueda cuestionarse.

**Error frecuente o límite.** Consultar dominio solo al final, tratar comunicación como decoración o creer que revisión humana compensa un sistema opaco y tardío.

**Comprobación.** Asignar preguntas: “¿qué significa cancelado?”, dominio; “¿se generaliza el error?”, estadística; “¿llega a tiempo?”, ingeniería; “¿quién autoriza?”, gobernanza operativa.

**Conclusión que debe quedar.** La confiabilidad es una propiedad de coordinación entre preguntas disciplinares y responsabilidades.

**Transición sugerida.** “El primer objeto compartido por esas perspectivas es una formulación que pueda explicarse sin algoritmos”.

## Diapositiva 15. Formular antes de modelar

**Correspondencia con el libro.** Capítulo 2, §2.1.1; capítulo 1, §§1.1.1 y 1.1.6.

**Propósito.** Diferenciar necesidad real, pregunta analítica y tarea computacional, y exigir correspondencia con el uso.

**Guion sugerido.** “Reducir esperas” es necesidad; “¿qué demanda tendrá cada zona-franja?”, pregunta analítica; “agregar o predecir”, tarea computacional. La necesidad también podría exigir descripción o auditoría. Justificar la tarea con “¿sirve para decidir?” y explicar sin algoritmos.

**Conceptos y términos.** *Tarea computacional*: operación formal; *pregunta analítica*: propiedad observable delimitada; *correspondencia hacia atrás*: tarea, datos y unidad responden a la acción.

**Descripción detallada del diagrama.** Tres cajas horizontales: azul “Necesidad real: reducir esperas”, verde “Pregunta analítica: demanda por zona-franja” y amarilla “Tarea computacional: agregar o predecir”. Flechas azules avanzan entre ellas. Desde la tarea sale una flecha verde discontinua hacia abajo y regresa a la necesidad, rotulada “¿sirve para decidir?”. Ese retorno es una prueba de utilidad, no una optimización automática. Orden: necesidad, pregunta, tarea, flecha de retorno y bloque “prueba sin algoritmos”. Interpretación válida: cada traducción restringe el significado y puede revisarse. No afirma que la cadena sea única, que toda pregunta requiera predicción o que una tarea útil garantice impacto. Ejemplo oral: reducir espera podría requerir primero agregar cancelaciones, no entrenar. Pregunta: “¿Qué cambiaría si la acción fuera informar pasajeros y no reasignar flota?”. Cambiarían unidad, horizonte, producto y posiblemente tarea. Conclusión visual: modelar antes de formular congela supuestos no examinados.

**Ejemplo de movilidad.** Necesidad: reducir P90 de espera. Pregunta: demanda por zona durante los siguientes treinta minutos. Tarea: construir zona-franja y pronosticar contra baseline; luego comparar traslados factibles.

**Error frecuente o límite.** Traducir una necesidad directamente a “usar redes neuronales” o elegir como objetivo una columna conveniente que no representa espera.

**Comprobación.** Pedir completar: quién decide, sobre qué unidad, con qué información, para cuándo y con qué propósito. Si falta una respuesta, la formulación sigue incompleta.

**Conclusión que debe quedar.** Una técnica solo es pertinente después de justificar la pregunta y su conexión con una decisión.

**Transición sugerida.** “Hagamos esa formulación compacta para poder revisar sus componentes uno por uno”.

## Diapositiva 16. Especificación compacta del problema

**Correspondencia con el libro.** Capítulo 1, §1.1.1; capítulo 2, §§2.1.1-2.1.4. La notación combina las formulaciones de ambos capítulos y agrega población y objetivo de manera explícita.

**Propósito.** Proporcionar una ficha mínima y cuatro pruebas que revelen formulaciones sin observación, acción o temporalidad.

**Guion sugerido.** Leer la tupla como preguntas. Empezar por objetivo y acción; fijar unidad y población; luego resultado, entradas, horizonte y restricciones. Completar usuario, valor, afectados y responsables. Cuatro pruebas: **observabilidad**, medición defendible; **accionabilidad**, elección real; **disponibilidad temporal**, entrada previa; **contrafactual de uso**, qué acción cambiaría. La última no estima causalidad.

**Lectura de la fórmula.** $\mathcal P=(U,\mathcal R,O,X,Y,A,H,C)$ define un objeto de especificación. $U$ es unidad de análisis; $\mathcal R$, población objetivo; $O$, objetivo; $X$, entradas disponibles; $Y$, resultado de interés; $A$, acciones posibles; $H$, horizonte; $C$, restricciones. Paréntesis y comas agrupan componentes; no indican suma, probabilidad ni orden causal. El caligráfico distingue la especificación del uso informal de $P$ como probabilidad. Supone que los componentes pueden declararse y revisarse, pero no que sean correctos ni completos. No permite concluir factibilidad de datos, generalización o valor sin evidencia.

**Conceptos y términos.** *Observable* admite operacionalización con error; *accionable* aún requiere capacidad y autoridad; *contrafactual* aquí prueba cambio de acción, no estima efecto causal.

**Ejemplo de movilidad.** $U$: zona-franja; $\mathcal R$: zonas operadas en condiciones normales; $O$: reducir espera extrema sin elevar cancelaciones; $X$: información recibida al corte; $Y$: demanda y espera en la franja siguiente; $A$: mantener o proponer traslados; $H$: treinta minutos; $C$: capacidad, distancia, seguridad y cobertura.

**Error frecuente o límite.** Confundir objetivo con métrica, población con archivo, acción con salida del modelo o incluir en $X$ una etiqueta posterior.

**Comprobación.** Cambiar $U$ a viaje y preguntar qué se rompe. La acción sigue siendo zonal, por lo que se necesitaría agregación explícita y revisar población, dependencias, evaluación y producto.

**Conclusión que debe quedar.** Una formulación defendible hace explícitos entidad, población, propósito, información, resultado, acción, tiempo y límites.

**Transición sugerida.** “Tres de esos componentes determinan sobre qué puede hablar legítimamente una fila: unidad, población y alcance”.

## Diapositiva 17. Unidad, población y alcance

**Correspondencia con el libro.** Capítulo 2, §2.1.3; capítulo 1, §§1.1.4 y 1.1.6.

**Propósito.** Diferenciar entidad elemental, conjunto de generalización, muestra observada y fronteras autorizadas de uso.

**Guion sugerido.** La **unidad** define una observación y nivel de acción; la **población objetivo**, dónde generalizar; la **muestra**, qué se observó bajo cobertura y selección; el **alcance**, periodos, lugares, usos y exclusiones. La **granularidad** es detalle temporal, espacial y de entidad: zona-franja difiere de viaje o GPS.

**Conceptos y términos.** *Clave* identifica unidad o relación. *Dependencia*: filas comparten entidad o tiempo. *Generalización* declara dónde, cuándo, bajo qué condiciones y qué no se evaluó.

**Composición visual relevante.** Tres columnas paralelas dan igual peso a unidad, población y alcance. Leerlas de izquierda a derecha y luego la alerta de granularidad. La línea final presenta tres conjuntos no equivalentes: población objetivo, muestra disponible y población futura. El símbolo $\neq$ significa que no deben asumirse idénticos, aunque puedan solaparse.

**Ejemplo de movilidad.** Una fila zona-franja agrega viajes y señales recibidas para una zona durante treinta minutos. La población incluye zonas de operadores participantes en operación ordinaria. La muestra puede sobrerrepresentar centro y excluir eventos sin registro. Emergencias y zonas no operadas quedan fuera hasta nueva evaluación.

**Error frecuente o límite.** Llamar censo de la ciudad a todos los viajes de una plataforma, tratar filas repetidas de una zona como independientes o ampliar uso porque la interfaz permite seleccionar otra ciudad.

**Comprobación.** “Si el sistema se usará en fechas futuras de las mismas zonas, ¿cómo separar?”. Temporalmente. “Si se usará en zonas nuevas?”. Reservando grupos zonales pertinentes, además de considerar tiempo.

**Conclusión que debe quedar.** Población objetivo, muestra y uso futuro son objetos distintos; la unidad debe coincidir con la acción.

**Transición sugerida.** “Además de saber para quién vale una fila, necesitamos reconstruir exactamente qué podía saberse al decidir”.

## Diapositiva 18. Horizonte y disponibilidad: reconstruir el reloj

**Correspondencia con el libro.** Capítulo 2, §§2.1.4 y 2.3.6; capítulo 1, §1.1.6. El contenido es horizonte, corte y disponibilidad temporal.

**Propósito.** Separar histórico, corte de decisión, franja objetivo y observación posterior del resultado.

**Guion sugerido.** **Horizonte** es distancia del corte al objetivo; **corte** $t_0$, el instante que congela información; **disponibilidad**, recepción y procesamiento, no solo ocurrencia. Para decidir 09:00 sobre 09:00-09:30, lo recibido después no es entrada. $Y$ posterior sirve para evaluar.

**Descripción detallada del diagrama.** Una línea horizontal azul con flecha a la derecha representa tiempo. Cuatro marcas ordenadas son “histórico”, “corte $t_0$”, “franja objetivo” y “resultado”. Sobre el tramo previo hay una caja amarilla “Entradas $X$ conocidas antes de $t_0$”. Bajo el corte hay una caja dorada “Decisión en $t_0$”. A la derecha y arriba, una caja azul “Objetivo $Y$ se observa después”. Una flecha azul lleva entradas a decisión. Una flecha verde discontinua parte de $Y$ hacia la zona del corte y dice “prohibido como entrada”; se dibuja como retorno para advertir fuga, no como flujo permitido. Orden exacto: eje y marcas de izquierda a derecha; caja $X$; decisión; caja $Y$; flecha prohibida; regla inferior. Interpretación válida: las características deben reconstruirse según disponibilidad al corte. No afirma que todo evento anterior sea válido, que $Y$ nunca pueda usarse en futuros reentrenamientos o que el horizonte sea el tiempo de cómputo. Ejemplo oral: el GPS de 08:58 recibido 09:04 no estaba disponible a las 09:00. Pregunta: “¿Dónde ubicar una corrección administrativa de las 10:00?”. Después del corte; puede corregir histórico, no la entrada en línea. Conclusión visual: evaluar justamente exige reproducir el reloj de decisión.

**Ejemplo de movilidad.** Histórico hasta 09:00, decisión a las 09:00, objetivo 09:00-09:30 y demanda total conocida después de cerrar la franja. Deben conservarse tiempo de evento, recepción, disponibilidad y decisión.

**Error frecuente o límite.** Filtrar solo por `hora_evento < t_0`, usar una tabla actualizada retrospectivamente o confundir horizonte de treinta minutos con una ventana histórica de treinta minutos.

**Comprobación.** “Evento 08:58, recepción 09:04, decisión 09:00: ¿entrada válida?”. No para esa decisión, aunque ocurriera antes.

**Conclusión que debe quedar.** El reloj relevante es qué información estaba disponible al corte, no qué sabemos al reconstruir meses después.

**Transición sugerida.** “Con problema, población y reloj definidos, podemos organizar el trabajo completo y sus retornos”.

## Diapositiva 19. Workflow de un proyecto de datos

**Correspondencia con el libro.** Capítulo 2, propósito, §§2.1.5 y 2.2.3-2.2.4; capítulo 1, ciclo de §1.1.1.

**Propósito.** Presentar un flujo de seis actividades con baseline y criterios fijados antes de comparar resultados finales.

**Guion sugerido.** El *workflow* explicita: formular decisión y éxito; obtener con inventario y permiso; preparar con procedencia; analizar; evaluar contra baseline, incertidumbre y riesgo; comunicar o integrar con autoridad y monitoreo. Es iterativo. Baseline y protocolo preceden a la prueba final.

**Conceptos y términos.** *Protocolo*: población, partición, métricas y tolerancias. *Artefacto*: objeto verificable. *Integrar* no equivale a automatizar.

**Descripción detallada del diagrama.** Cinco cajas numeradas forman una fila: 1 formular, 2 obtener, 3 preparar, 4 analizar/modelar y 5 evaluar/contrastar. Los colores distinguen decisión, dato y proceso para recordar la naturaleza dominante, no equipos propietarios. Flechas azules conectan la fila. Debajo, una caja dorada más ancha contiene la fase 6, “Comunicar o integrar con autoridad y monitoreo”. Desde evaluación una flecha baja a fase 6; una flecha verde discontinua regresa desde fase 6 a formulación. Orden: recorrer 1 a 5, bajar a 6, seguir el retorno, leer el principio. Interpretación válida: el uso produce evidencia para reformular. No afirma cascada rígida, que evaluación ocurra una sola vez ni que todo producto se despliegue. Ejemplo oral: una auditoría de GPS puede pasar por todas las fases sin modelo. Pregunta: “¿Dónde se fija el baseline?”. En formulación/evaluación planificada, antes de comparación final. Conclusión visual: el flujo conecta aprendizaje técnico y operativo.

**Ejemplo de movilidad.** Ficha zona-franja; inventario de viajes, GPS, clima y zonas; tabla con corte; baseline estacional y candidato; evaluación temporal; tablero asistido con abstención y monitoreo.

**Error frecuente o límite.** Usar la prueba para elegir modelos, considerar “mejor de los probados” equivalente a aceptable o dejar monitoreo para después de publicar.

**Comprobación.** Preguntar qué fase revisa una salida precisa que operaciones no comprende. Comunicación/integración, con posible retorno a formulación y representación.

**Conclusión que debe quedar.** El workflow organiza evidencia y decisiones de avance, no solo procesamiento de datos.

**Transición sugerida.** “Para impedir que avanzar sea automático, cada transición necesita una puerta y un artefacto revisable”.

## Diapositiva 20. Puertas y artefactos: aprender antes de escalar

**Correspondencia con el libro.** Capítulo 2, §§2.2.2-2.2.3 y §2.1.5.

**Propósito.** Convertir fases en decisiones verificables y priorizar la incertidumbre que podría invalidar el proyecto.

**Guion sugerido.** Una **puerta** decide avanzar, modificar, escalar o detener con evidencia mínima. Un **artefacto vivo** es versionado y evoluciona. Un **producto mínimo evaluable** es la menor implementación que prueba el supuesto crítico: si se desconoce GPS, primero perfil de cobertura y latencia. “Mínimo” reduce inversión, no rigor.

**Lectura detallada de la tabla.** La primera columna nombra cuatro transiciones. La segunda responde qué evidencia mínima autoriza cruzarlas. La tercera identifica el artefacto vivo que conserva esa evidencia. Leer por filas: de formular a datos se necesitan unidad, alcance, autoridad y valor, registrados en ficha; de datos a análisis, cobertura, licencia, calidad y tiempo, registrados en inventario y diccionario; de análisis a uso, superar baseline y aceptar riesgos, en registro de experimento; de uso a escala, observar utilidad, carga y fallos, en plan de monitoreo y retirada. Después leer verticalmente la tercera columna para mostrar acumulación documental. Las flechas escritas en la primera columna son transiciones, no garantías de avance.

**Conceptos y términos.** *Aceptación* decide suficiencia; *selección* elige candidato; *retirada* vuelve a una alternativa segura. Un artefacto vivo conserva versión, responsable y motivo.

**Ejemplo de movilidad.** Antes de analizar se exige conocer qué porcentaje de eventos GPS llega antes del corte. Antes de uso se exige mejorar el baseline temporal sin degradar cancelaciones. Antes de escala se observa carga del operador y rechazos.

**Error frecuente o límite.** Convertir puertas en burocracia documental, exigir certeza total o cruzarlas porque “ya se invirtió mucho”. Tampoco se compensan restricciones críticas con una puntuación global.

**Comprobación.** “No sabemos si clima llega antes de las 09:00. ¿Cuál es el producto mínimo evaluable?”. Una medición versionada de latencia y cobertura por periodo, no un modelo con clima.

**Conclusión que debe quedar.** Escalar es una decisión basada en evidencia acumulada; detener también es un resultado legítimo.

**Transición sugerida.** “Dos metodologías conocidas ayudan a nombrar estas actividades; primero veremos la que sitúa minería dentro del descubrimiento”.

## Diapositiva 21. KDD: del dato al conocimiento validado

**Correspondencia con el libro.** Capítulo 2, §2.2.1.

**Propósito.** Explicar KDD como proceso amplio y evitar el salto de salida computacional a conocimiento o regla operativa.

**Guion sugerido.** En KDD, selección justifica fuentes y unidades; preprocesamiento estudia faltantes, errores y duplicados; transformación representa; minería encuentra patrones; interpretación/evaluación comprueba validez y utilidad. Distinguir resultado, patrón, hipótesis, hallazgo validado y regla aprobada: cada salto requiere control.

**Conceptos y términos.** *Minería*: búsqueda de patrones; *hallazgo validado*: resultado que resiste controles; *regla operativa*: uso aprobado. Novedad depende del contexto.

**Descripción detallada del diagrama.** Cinco cajas horizontales: selección amarilla; preprocesamiento y transformación verdes; minería verde; interpretación/evaluación azul. Flechas continuas avanzan entre etapas. Desde la última sale una flecha verde discontinua que baja y regresa a preprocesamiento, rotulada “iterar”. Leer de selección a interpretación, luego seguir el retorno y finalmente las dos cajas inferiores: minería no es KDD completo y deben evitarse saltos entre estados. Los colores distinguen insumo, proceso y juicio evaluativo; no señalan que selección ocurra una sola vez. Interpretación válida: un patrón inesperado puede exigir revisar codificación. No afirma que siempre se vuelva solo a preprocesamiento, que interpretación sea subjetiva sin criterios ni que KDD termine automáticamente en decisión. Ejemplo oral: una regla “alta demanda a las 08:00” puede ser correcta pero no accionable. Pregunta: “¿Dónde se descubre que el patrón proviene de duplicados?”. En interpretación/evaluación y se retorna a preprocesamiento. Conclusión visual: conocimiento requiere validar e interpretar el resultado en contexto.

**Ejemplo de movilidad.** Se seleccionan viajes y franjas; se corrigen duplicados; se agregan eventos a zona-franja; se encuentra un patrón de demanda; se verifica en periodos separados y se consulta a operaciones antes de considerarlo evidencia.

**Error frecuente o límite.** Llamar descubrimiento a cualquier correlación novedosa para el analista o limpiar hasta producir el patrón esperado.

**Comprobación.** “Un cluster está muy separado pero no cambia ninguna acción ni tiene significado de dominio. ¿Es conocimiento operativo?”. No; es un resultado que requiere interpretación y quizá no avance.

**Conclusión que debe quedar.** La minería produce patrones; KDD organiza el trabajo necesario para convertir algunos en conocimiento validado.

**Transición sugerida.** “Antes de comparar con otra metodología, traduzcamos cada caja de KDD a una tarea y un resultado verificable”.

## Diapositiva 22. Etapas de KDD explicadas

**Correspondencia con el libro.** Capítulo 2, §2.2.1.

**Propósito.** Convertir el diagrama de KDD en una secuencia operativa de tareas, controles y productos.

**Guion sugerido.** Recorrer la tabla por filas. Selección delimita fuentes, población, unidad y variables; deja datos relevantes y alcance justificado. Preprocesamiento no significa borrar todo valor extraño: diagnostica faltantes, errores, duplicados, sesgos y consistencia, y documenta decisiones. Transformación construye la representación analítica mediante agregación, codificación, escalado o atributos derivados. Minería aplica métodos y produce patrones o modelos candidatos. Interpretación y evaluación contrasta validez, novedad, utilidad y límites; puede aceptar un hallazgo o exigir volver atrás.

**Lectura detallada de la tabla.** La columna central responde “qué trabajo ocurre”; la derecha exige un producto auditable. Leer primero las cinco tareas y luego verticalmente los cinco resultados. Destacar que “resultado candidato” impide confundir minería con conocimiento. En movilidad: seleccionar viajes, revisar duplicados, agregar a zona-franja, detectar un patrón y validarlo en otro periodo con operaciones.

**Comprobación.** “¿En qué etapa se decide que un cluster estadísticamente separado no tiene significado operativo?”. En interpretación y evaluación; esa conclusión puede provocar una nueva transformación o formulación.

**Conclusión que debe quedar.** Cada etapa de KDD reduce una incertidumbre distinta y deja evidencia para justificar el paso siguiente.

**Transición sugerida.** “KDD enfoca el descubrimiento; CRISP-DM amplía la mirada a la organización completa del proyecto”.

## Diapositiva 23. CRISP-DM: organizar el proyecto completo

**Correspondencia con el libro.** Capítulo 2, §2.2.2.

**Propósito.** Presentar seis fases cíclicas, sus entregables y el sentido amplio de despliegue.

**Guion sugerido.** CRISP-DM comienza con la comprensión del negocio, rotulada “comprensión del problema” en la diapositiva; después comprende datos, prepara, modela, evalúa y despliega. Sus productos incluyen ficha, inventario, tabla versionada, baseline, evaluación técnica-operativa y entrega. Despliegue puede ser informe, tablero, servicio o regla; no implica autonomía. Monitoreo y retirada continúan.

**Conceptos y términos.** *Despliegue*: integración real. Una **Interfaz de Programación de Aplicaciones (API, por *Application Programming Interface*)** expone datos u operaciones mediante una especificación; una respuesta exitosa no garantiza cobertura. *Retirada*: suspensión con alternativa segura.

**Descripción detallada del diagrama.** Seis cajas forman un ciclo aproximadamente hexagonal. Arriba está comprensión del problema; luego, en sentido horario, comprensión de datos, preparación, modelado, evaluación y despliegue/entrega. Flechas azules recorren el ciclo y vuelven de despliegue al problema. Una flecha verde discontinua conecta evaluación con comprensión de datos y hace visible un retorno específico. La columna derecha resume tres ideas y una alerta sobre continuidad operativa. Orden: nombrar las fases en sentido horario, explicar el retorno evaluación-datos, leer que comienza por el problema y terminar en “no termina al publicar”. Interpretación válida: las fases son vocabulario y puntos de control. No afirma que sean departamentos, que se ejecuten una vez ni que CRISP-DM prescriba herramientas concretas. Ejemplo oral: evaluación revela cobertura desigual y obliga a revisar inventario. Pregunta: “¿Puede un informe semanal ser despliegue?”. Sí, si integra evidencia en el proceso de uso. Conclusión visual: el proyecto completo es cíclico y operacional.

**Ejemplo de movilidad.** La primera entrega puede ser un tablero asistido que muestra pronóstico, incertidumbre y procedencia; operaciones decide y registra motivos. Si cambia cobertura, se vuelve a comprensión de datos.

**Error frecuente o límite.** Tratar fases como casillas administrativas o suponer que “negocio” excluye objetivos públicos y sociales.

**Comprobación.** Preguntar dónde se revisa un modelo preciso que no reduce espera bajo simulación. En evaluación respecto del problema, con retorno a comprensión del problema o modelado.

**Conclusión que debe quedar.** CRISP-DM organiza desde propósito hasta uso y mantiene retornos después de la entrega.

**Transición sugerida.** “El ciclo muestra relaciones; ahora explicaremos qué trabajo y qué producto corresponden a cada fase”.

## Diapositiva 24. Etapas de CRISP-DM explicadas

**Correspondencia con el libro.** Capítulo 2, §2.2.2.

**Propósito.** Traducir las seis fases de CRISP-DM a responsabilidades y entregables concretos.

**Guion sugerido.** Comprensión del problema acuerda necesidad, usuarios, acciones, éxito y restricciones; deja una ficha y criterios de aceptación. Comprensión de datos inventaría significado, cobertura, calidad y riesgos; deja diccionario, perfil y límites. Preparación construye datos versionados y reproducibles. Modelado compara baseline y candidatos bajo un protocolo registrado. Evaluación contrasta desempeño técnico, utilidad, equidad y riesgo para continuar, modificar o detener. Despliegue integra el resultado en el uso real con monitoreo, responsables, incidentes y retirada.

**Lectura detallada de la tabla.** Leer cada fase como verbo y luego su evidencia. Subrayar que el entregable no es siempre un modelo: puede ser una decisión de detener, una tabla versionada o un plan de retirada. Los retornos del diagrama significan que un producto insuficiente reabre fases anteriores.

**Comprobación.** “La métrica técnica mejora, pero el tablero llega después de que operaciones decide. ¿Qué fases deben revisarse?”. Evaluación, despliegue y comprensión del problema; la entrega no satisface el horizonte de uso.

**Conclusión que debe quedar.** CRISP-DM coordina propósito, datos, análisis y uso mediante productos revisables, no mediante una secuencia rígida.

**Transición sugerida.** “Para comprender los datos debemos distinguir su forma de almacenamiento de su significado”.

## Diapositiva 25. Estructura de los datos

**Correspondencia con el libro.** Capítulo 2, §§2.3.1-2.3.3.

**Propósito.** Comparar datos estructurados, semiestructurados y no estructurados, y mostrar las decisiones de representación propias de cada forma.

**Guion sugerido.** Estructurados: esquema, filas, columnas y claves. El **Lenguaje de Consulta Estructurada (SQL, por *Structured Query Language*)** consulta y transforma datos relacionales, sin garantizar semántica. Semiestructurados: claves flexibles; la **Notación de Objetos de JavaScript (JSON, por *JavaScript Object Notation*)** representa objetos y arreglos, distinguiendo ausente, nulo y vacío. Texto, audio e imagen carecen de variables tabulares inmediatas, no de estructura interna.

**Conceptos y términos.** *Esquema*: nombres, tipos y restricciones. *Clave primaria*: identidad; *foránea*: relación. *Cardinalidad*: uno a uno, uno a muchos o muchos a muchos. *Representación*: variables derivadas con significado.

**Lectura detallada de la tabla.** La primera columna clasifica el tipo; la segunda describe su organización; la tercera une ejemplo y decisión. Leer cada fila completa. Estructurados: viajes SQL; revisar unidad, tipos y cardinalidad. Semiestructurados: eventos JSON; distinguir ausente, nulo y lista vacía. No estructurados: texto, audio o imagen; construir una representación, por ejemplo tokens, espectrograma o características visuales. Después leer verticalmente la tercera columna para mostrar que todos exigen decisiones, aunque cambie el procedimiento. La tabla clasifica organización, no calidad, procedencia ni mecanismo generador.

**Ejemplo de movilidad.** Tabla SQL de viajes, eventos JSON de telemetría y texto de reclamos pueden contribuir a zona-franja. Expandir una lista de incidentes puede multiplicar filas; agregar texto puede perder matices; ambas transformaciones deben declararse.

**Error frecuente o límite.** Creer que un esquema válido asegura significado, que JSON no necesita especificación o que “no estructurado” significa caótico. Una unión muchos-a-muchos puede inflar conteos sin producir error técnico.

**Comprobación.** “Cada viaje tiene tres etiquetas y se expande a tres filas antes de contar. ¿Qué ocurre?”. Se triplica el conteo salvo que se preserve la unidad mediante otra tabla o agregación.

**Conclusión que debe quedar.** La forma determina controles de representación; el significado exige esquema, diccionario, claves y cardinalidades.

**Transición sugerida.** “Ahora veremos cómo fuentes con unidades distintas se convierten, mediante reglas explícitas, en una tabla zona-franja”.

## Diapositiva 26. De fuentes heterogéneas a una tabla analítica

**Correspondencia con el libro.** Capítulo 2, §2.3.1, especialmente normalización, tablas analíticas y estado al corte; §2.3.8. Esta lámina trata construcción de tabla analítica.

**Propósito.** Explicar cómo agregar, unir, filtrar y cortar fuentes sin cambiar silenciosamente la unidad ni perder procedencia.

**Guion sugerido.** Una **tabla analítica** deriva de fuentes para una pregunta y corte. Una fila es zona durante treinta minutos: viajes se agregan; clima se asigna temporal y espacialmente; zonas aportan geometría versionada. Cada unión declara claves, cardinalidad, cobertura y corte. Cambiar filas puede cambiar población o unidad.

**Conceptos y términos.** *Agregar*: resumir unidades; *unir*: relacionar por claves; *filtrar*: incluir/excluir; *cortar*: reconstruir estado; *linaje*: retroceder hasta fuente y transformación.

**Descripción detallada del diagrama.** A la izquierda hay tres cajas amarillas apiladas: viajes con unidad viaje, clima con estación-hora y zonas con polígono-versión. Las tres flechas azules convergen en una caja verde central “Reglas explícitas: agregar, unir, filtrar, cortar”. Desde ella una flecha llega a una caja azul “Tabla analítica: una fila = zona-franja; claves + procedencia”. La convergencia significa integración controlada, no que se concatenen tablas sin transformación. Orden exacto: leer unidad de cada fuente de arriba abajo; seguir cada flecha hacia reglas; explicar los cuatro verbos; llegar a la unidad final; leer las tres viñetas inferiores. Interpretación válida: una tabla puede reconciliar granularidades con reglas. No afirma que las tres fuentes sean obligatorias, que toda unión tenga una clave simple ni que la tabla resultante sea verdadera por ser rectangular. Ejemplo oral: viajes 08:30-09:00 se cuentan por zona, clima de estación se asigna por proximidad y el polígono vigente determina pertenencia. Pregunta: “¿Dónde se evita que dos versiones de zona dupliquen una franja?”. En regla de vigencia, claves y cardinalidad. Conclusión visual: la unidad final es construida, no heredada automáticamente.

**Ejemplo de movilidad.** Clave analítica `(zona_id, inicio_franja)`. Se conserva versión de polígonos, corte de extracción, conteo antes y después de cada unión y cobertura de fuentes.

**Error frecuente o límite.** Usar límites actuales para historia sin declarar, unir clima solo por hora ignorando zona o aceptar una multiplicación de filas porque la consulta ejecutó.

**Comprobación.** “La unión aumenta de 100 a 140 zonas-franja. ¿Qué se revisa?”. Cardinalidad, duplicados de clave, vigencias y relación muchos-a-muchos antes de interpretar.

**Conclusión que debe quedar.** Construir una tabla analítica es una decisión semántica y temporal documentada.

**Transición sugerida.** “Antes de integrar masivamente, el equipo necesita inventariar qué es y cómo falla cada fuente”.

## Diapositiva 27. Fuentes: inventariar antes de integrar

**Correspondencia con el libro.** Capítulo 2, introducción de §2.3, §§2.3.5-2.3.6 y §2.3.8. Esta lámina es el inventario de fuentes.

**Propósito.** Leer cada fuente por unidad, acceso y riesgo, y presentar el inventario como especificación de integración y gobernanza.

**Guion sugerido.** Inventariar antes de descargar revela fuentes no integrables, autorizadas o tardías. Registrar propietario, propósito, unidad, cobertura, captura, formato, frecuencia, licencia, sensibilidad, calidad y cambios. Gobernanza asigna acceso, uso, retención y responsabilidad. API, archivo y flujo tienen fallos distintos.

**Lectura detallada de la tabla.** Las columnas son fuente, unidad original, acceso y riesgo principal. Leer por filas. Viajes: viaje, base o archivo, cobertura incompleta de operadores. GPS: dispositivo-evento, flujo o API, latencia, deriva y pérdida. Clima: estación-hora, API, desfase horario y distancia espacial. Zonas: polígono-versión, archivo geográfico, límites modificados. Calendario: día, archivo o tabla, definiciones locales. Luego leer verticalmente “unidad original” para mostrar incompatibilidad de granularidades y “riesgo” para asociar un control específico. La tabla no clasifica calidad total ni prioridad; un riesgo principal no excluye otros.

**Conceptos y términos.** *Deriva*: cambio gradual de medición; *cobertura*: operadores, dispositivos, territorio y tiempo; *licencia*: usos permitidos; *sensibilidad*: daño o privacidad potencial.

**Ejemplo de movilidad.** Viajes y zonas son obligatorios para construir unidad; calendario puede ser opcional; clima entra solo si su asignación y latencia cumplen umbral; GPS puede degradarse a indicador de cobertura en vez de característica si llega tarde.

**Error frecuente o límite.** Confundir “descargable” con permitido, una respuesta exitosa mediante el **Protocolo de Transferencia de Hipertexto (HTTP, por *Hypertext Transfer Protocol*)** con una extracción completa o un archivo llamado “final” con una versión inmutable.

**Comprobación.** Antes de unir clima: exigir zona horaria, instante de actualización, estación, regla espacial, cobertura, faltantes, frecuencia y disponibilidad al corte.

**Conclusión que debe quedar.** Un inventario es una decisión argumentada sobre pertinencia, integración, legitimidad y continuidad de cada fuente.

**Transición sugerida.** “Además de acceso y formato, necesitamos saber qué mecanismo produjo los datos y qué recorrido siguieron”.

## Diapositiva 28. Procedencia: ejes distintos, preguntas distintas

**Correspondencia con el libro.** Capítulo 2, introducción de §2.3 y §§2.3.4-2.3.7. La clasificación primario/secundario es una ampliación didáctica.

**Propósito.** Separar mecanismo de generación, propósito de recolección, acceso/gobernanza y linaje.

**Guion sugerido.** **Procedencia** documenta origen, contexto y transformación. El mecanismo es observacional, con confusión posible; experimental, con condiciones asignadas; o simulado, dependiente del simulador. El propósito es primario o secundario; el acceso, abierto, privado o restringido. **Linaje** conecta origen y producto. Son ejes independientes.

**Conceptos y términos.** *Gobernanza*: permisos, usos y responsables. *Linaje*: artefactos y transformaciones. *Secundario* significa otro propósito, no menor calidad. *Observacional* no significa neutral.

**Descripción detallada del diagrama.** Cuatro tarjetas horizontales iguales están apiladas. La primera contiene el eje “Mecanismo de generación” con observacional, experimental y simulado. La segunda, “Propósito de recolección” con primario y secundario. La tercera, “Acceso y gobernanza” con abierto, privado y restringido. La cuarta dibuja el linaje como origen, extracción, transformación y producto unidos por flechas. La igualdad visual muestra ejes independientes; las barras verticales dentro de cada tarjeta separan alternativas de ese eje, no etapas. Leer de arriba abajo y luego construir una combinación cruzada. Interpretación válida: un dato puede ocupar una categoría en cada eje simultáneamente. No afirma que abierto sea experimental, que privado sea confiable, que simulado sea falso ni que el linaje por sí solo otorgue legitimidad. Ejemplo oral: GPS de una plataforma es observacional, secundario para este análisis y privado, con linaje de evento a tabla zona-franja. Pregunta: “¿Qué eje limita inferencia causal?”. Principalmente mecanismo generador; los demás afectan uso y auditoría. Conclusión visual: preguntas distintas requieren metadatos distintos.

**Ejemplo de movilidad.** El pronóstico puede usar viajes observacionales privados recolectados para facturación, clima abierto secundario y escenarios simulados de reasignación. Deben mantenerse distinguibles.

**Error frecuente o límite.** Presentar una simulación como observación, inferir causalidad de asociación o creer que licencia abierta elimina privacidad y sesgo.

**Comprobación.** Clasificar viajes operativos: observacionales, probablemente secundarios respecto del proyecto, privados o restringidos; su linaje debe documentarse.

**Conclusión que debe quedar.** Saber de dónde viene un dato implica describir generación, propósito, gobernanza y transformaciones, no solo citar un archivo.

**Transición sugerida.** “Cuando cantidad, ritmo y diversidad crecen, estas mismas preguntas se organizan mediante seis diagnósticos”.

## Diapositiva 29. Big Data: seis V, seis diagnósticos

**Correspondencia con el libro.** Capítulo 2, §2.3.7; capítulo 1, §1.3.5 como antecedente de cinco V. El capítulo 2 incorpora variabilidad.

**Propósito.** Usar las seis V como dimensiones diagnósticas, no como etiqueta de prestigio ni métrica única.

**Guion sugerido.** **Volumen**: cuánto; **velocidad**: ritmo y latencia; **variedad**: formatos y fuentes; **veracidad**: confiabilidad; **valor**: mejora de decisión; **variabilidad**: cambios de distribución o significado. Asociar medidas concretas; más infraestructura no corrige semántica.

**Conceptos y términos.** Las **seis V de Big Data** diagnostican, no clasifican binariamente. *Latencia* es demora entre relojes; *variabilidad* incluye definición, estacionalidad y deriva.

**Descripción detallada del diagrama.** Un círculo verde central dice “Desafío de datos”. Seis tarjetas lo rodean: volumen arriba izquierda, velocidad arriba, variedad arriba derecha, veracidad abajo derecha, valor abajo y variabilidad abajo izquierda. Cada tarjeta formula una pregunta y envía una flecha azul al centro. La convergencia indica que el desafío combina dimensiones. Orden exacto: volumen, velocidad, variedad, veracidad, valor y variabilidad; para cada una asociar un control; terminar en el centro y la alerta. Aunque valor está abajo, no es menos importante ni el centro geométrico. Interpretación válida: distintas combinaciones requieren soluciones distintas. No afirma que todas deban ser altas, que seis V definan una escala universal ni que distribuir mejore calidad. Ejemplo oral: muchos GPS tardíos tienen volumen y velocidad, pero poco valor al corte. Pregunta: “¿Qué V captura un cambio de límites zonales?”. Variabilidad, con consecuencias también para veracidad. Conclusión visual: Big Data es un conjunto de tensiones técnicas y semánticas orientadas al uso.

**Ejemplo de movilidad.** GPS genera volumen y velocidad; viajes, clima y zonas añaden variedad; pérdidas afectan veracidad; cambios estacionales, variabilidad; valor existe solo si la evidencia llega antes y cambia una acción segura.

**Error frecuente o límite.** Adoptar computación distribuida sin medir memoria o tiempo, o estimar con gran precisión el concepto equivocado.

**Comprobación.** “Un archivo pequeño de cierres críticos puede tener alto valor?”. Sí. “Una zona cuyo significado cambia?”. Variabilidad.

**Conclusión que debe quedar.** Escala se diagnostica por dimensiones medibles; ninguna sustituye validez semántica ni conexión con la decisión.

**Transición sugerida.** “Sea pequeño o grande, un resultado confiable debe poder reconstruirse y auditarse”.

## Diapositiva 30. Herramientas y reproducibilidad

**Correspondencia con el libro.** Capítulo 1, §1.1.4; capítulo 2, §§2.4, 2.4.1-2.4.2 y 2.4.5-2.4.7.

**Propósito.** Relacionar entornos, artefactos y controles en una cadena reproducible, diferenciando reproducibilidad y trazabilidad.

**Guion sugerido.** **Reproducibilidad** reconstruye resultados; **trazabilidad** sigue decisiones y transformaciones. Python, R y SQL son medios. **Jupyter** combina narrativa, código y resultados y debe ejecutarse desde cero. **Quarto** genera documentos reproducibles. Una **semilla** repite secuencias bajo condiciones compatibles, no controla todo no determinismo. Un **checksum** identifica contenido exacto, no significado.

**Conceptos y términos.** *Versión*: estado; *configuración*: parámetros; *prueba*: especificación verificada; *registro*: razón de una decisión, no solo métricas.

**Composición visual relevante.** Tres columnas superiores agrupan entornos, artefactos y controles. Deben leerse horizontalmente como combinación: un entorno ejecuta código y datos bajo configuración; los controles vinculan versiones, checksums, pruebas y semillas. La caja central dibuja fuente identificada, transformación versionada, experimento registrado y resultado reconstruible. Las flechas indican dependencia documental, no que baste con conservar el último artefacto. Las viñetas inferiores corrigen tres reduccionismos: semilla, notebook y preferencia personal.

**Ejemplo de movilidad.** Un gráfico de P90 por zona registra corte, operadores, versión de polígonos, zona horaria, consulta, código, entorno y regla para cancelados. Otra persona puede regenerarlo sin buscar `final_v2.csv`.

**Error frecuente o límite.** “Corre en mi equipo”, guardar solo el modelo, pegar tablas manualmente o creer que checksum prueba calidad. Reproducibilidad tampoco justifica retener datos sensibles indefinidamente.

**Comprobación.** “Tenemos código y semilla, pero la API devuelve datos actuales. ¿Qué falta?”. Instantánea, versión o consulta con corte verificable.

**Conclusión que debe quedar.** Reconstruir evidencia exige identificar datos, código, entorno, configuración, partición, variación y decisiones.

**Transición sugerida.** “Apliquemos ahora toda la formulación a un caso único y coherente de movilidad”.

## Diapositiva 31. Caso movilidad: formulación coherente

**Correspondencia con el libro.** Capítulo 1, §1.1.6; capítulo 2, §§2.1.3-2.1.5 y §2.3.8.

**Propósito.** Consolidar una ficha donde unidad, horizonte, resultado, acciones, restricciones, valor y autoridad sean compatibles.

**Guion sugerido.** Partir de la decisión antes de cada franja y verificar la ficha. Zona-franja coincide con predicción y traslado; población son zonas operadas en condiciones declaradas; horizonte, treinta minutos; resultado, demanda y espera; acciones, mantener o trasladar; valor, espera extrema sin más cancelaciones; autoridad, operaciones.

**Conceptos y términos.** *Restricción dura*: excluye; *blanda*: penaliza. *Autoridad*: aprobar y responder. *Valor*: consecuencia operativa.

**Composición visual relevante.** La caja superior fija la decisión; dos columnas inferiores distribuyen cuatro componentes cada una. Leer en pares: unidad-acciones, población-restricciones, horizonte-valor, resultado-autoridad. La alerta final resume coherencia de granularidad. No leer las columnas como dos fichas independientes.

**Ejemplo de movilidad.** A las 09:00 se estima 09:00-09:30. Se ofrecen mantener o mover un vehículo si distancia y cobertura lo permiten. Operaciones puede rechazar por un cierre no registrado. La acción efectiva y el motivo quedan documentados.

**Error frecuente o límite.** Mezclar zona-franja con resultado por viaje, omitir “mantener” del conjunto de acciones o medir éxito solo por demanda predicha.

**Comprobación.** Pedir encontrar una contradicción si el resultado fuera demora de cada viaje y la acción mover flota entre zonas. Falta regla explícita de agregación y evaluación zonal.

**Conclusión que debe quedar.** La formulación es coherente cuando evidencia, decisión y evaluación comparten unidad, población y reloj.

**Transición sugerida.** “La ficha se convierte ahora en una cadena operativa que preserva la frontera entre recomendación y autoridad”.

## Diapositiva 32. Movilidad: evidencia, recomendación y autoridad

**Correspondencia con el libro.** Capítulo 1, §§1.1.5-1.1.6 y §1.4.4; capítulo 2, §§2.1.2, 2.1.4 y 2.2.5.

**Propósito.** Recorrer el caso desde fuentes hasta acción, incorporando incertidumbre, opciones factibles, abstención y retroalimentación.

**Guion sugerido.** Las fuentes se transforman en zona-franja; la evidencia combina demanda, incertidumbre y evaluación; las opciones incluyen consecuencias y factibilidad; el responsable aprueba, modifica, rechaza o mantiene. La **abstención** es salida explícita ante información o riesgo insuficiente. La acción genera observaciones y puede cambiar datos futuros.

**Conceptos y términos.** *Incertidumbre*: variabilidad o desconocimiento; *abstención*: derivar o mantener alternativa segura; *autoridad humana*: contradecir y detener.

**Descripción detallada del diagrama.** Cinco cajas forman la fila principal: fuentes amarillas; proceso verde de construir zona-franja; evidencia amarilla de demanda esperada e incertidumbre; proceso verde de opciones factibles y consecuencias; responsable dorado. Flechas continuas avanzan. Debajo de opciones hay una caja azul “Acción en la flota o mantener estado”; una flecha desde responsable llega a ella, mostrando que la acción ocurre después de la decisión humana. Una flecha verde discontinua vuelve desde acción a construcción de unidad y se rotula “impacto observado”. Orden: fuentes, construcción, evidencia, opciones, responsable, acción, retorno y alerta de automatización. Interpretación válida: el uso genera nuevos datos y aprendizaje. No afirma que el impacto pueda atribuirse causalmente sin diseño, que toda consecuencia sea observada ni que el responsable deba aceptar. Ejemplo oral: baja cobertura activa abstención y se mantiene regla vigente. Pregunta: “¿Dónde puede detenerse la cadena sin fallo?”. En evidencia u opciones mediante abstención, y en responsable mediante rechazo. Conclusión visual: recomendación y ejecución están separadas por autoridad.

**Ejemplo de movilidad.** El sistema presenta mover uno, mantener y abstenerse, con efecto esperado en P90, cancelaciones y cobertura. Operaciones elige mantener por incidente vial nuevo.

**Error frecuente o límite.** Escribir “el algoritmo reasigna”, ocultar incertidumbre o tratar rechazo humano como etiqueta de error sin investigar contexto.

**Comprobación.** Preguntar qué registrar ante un rechazo: corte, entradas, versión, predicción, incertidumbre, opciones, motivo, decisión, acción efectiva y resultado.

**Conclusión que debe quedar.** El producto es evidencia y opciones; la autoridad decide y el monitoreo aprende de la acción real.

**Transición sugerida.** “Una misma cadena contiene tareas distintas; la tabla siguiente vuelve a separarlas por producto y evaluación”.

## Diapositiva 33. Del caso amplio a tareas concretas

**Correspondencia con el libro.** Capítulo 1, §§1.1.5-1.1.6; capítulo 2, §§2.1.1, 2.1.5 y 2.2.4.

**Propósito.** Traducir un caso amplio en cuatro tareas sobre la misma unidad, cada una con producto y evaluación propios.

**Guion sugerido.** Mantener zona-franja y cambiar el verbo. Describir agrega y controla cobertura; predecir estima y compara con baseline temporal; prescribir evalúa reasignaciones, utilidad y restricciones; monitorear detecta cambios y activa revisión o retirada. Un ranking sin acciones ni consecuencias no prescribe.

**Conceptos y términos.** *Perfil*: resumen; *pronóstico*: resultado futuro; *opción factible*: satisface restricciones; *alerta*: condición, responsable y respuesta; *retirada*: alternativa segura.

**Lectura detallada de la tabla.** La primera columna fija cuatro objetivos; la segunda formula la tarea manteniendo “sobre zona-franja”; la tercera une producto y forma de evaluación. Leer por filas: describir produce perfil; predecir, pronóstico comparado con baseline; prescribir, opciones con utilidad y restricciones; monitorear, alertas y decisiones de revisión. Luego leer verticalmente la segunda columna para comprobar que la unidad no cambia. Las relaciones son encadenables: un perfil puede informar baseline, un pronóstico alimentar opciones y monitoreo revisar todos; no son equivalentes ni una escala de sofisticación. El bloque inferior recuerda que eventos de viaje deben agregarse y no deben presentarse como decisiones individuales.

**Ejemplo de movilidad.** Para 09:00-09:30: el perfil resume semanas previas; el pronóstico estima demanda; la prescripción compara mover uno o mantener; monitoreo comprueba latencia GPS, error, tasa de abstención y P90 observado.

**Error frecuente o límite.** Evaluar prescripción solo por error predictivo, presentar cada viaje como decisión o monitorear únicamente disponibilidad del servicio sin impacto.

**Comprobación.** “Un modelo mejora error, pero las opciones resultantes dejan una zona sin cobertura. ¿Qué tarea falla?”. Prescripción/factibilidad, aunque predicción pudiera mejorar.

**Conclusión que debe quedar.** Compartir unidad y fuentes no elimina las diferencias entre describir, predecir, prescribir y monitorear.

**Transición sugerida.** “Antes de confiar en el pronóstico, auditaremos el fallo que más fácilmente produce resultados extraordinarios e irreales: usar futuro”.

## Diapositiva 34. Fuga temporal: saber hoy lo que mañana ocurrió

**Correspondencia con el libro.** Capítulo 1, §§1.1.3, 1.1.6 y §1.4.5; capítulo 2, §§2.1.3-2.1.5 y tiempos de evento, recepción y decisión en §2.3.6.

**Propósito.** Definir fuga temporal con precisión, reconocer sus mecanismos, explicar por qué vuelve optimista la evaluación y establecer controles de detección y prevención.

**Guion sugerido.** **Fuga de información** ocurre cuando entrenamiento, características, selección o evaluación acceden a información ausente en uso real, o la comparten de modo que la prueba deja de representar casos nuevos. La **fuga temporal** viola el reloj de decisión. Importan ocurrencia, recepción, procesamiento y disponibilidad.

Separar cuatro relojes: **evento**, cuando ocurre; **recepción**, cuando llega; **disponibilidad**, cuando puede consultarse tras procesar; y **decisión**, cuando se congela evidencia. Para cada característica:

$$
t_{disponibilidad}\le t_{decisión}.
$$

La disponibilidad debe ser anterior o igual a decisión; no equivale a `hora_evento`. La igualdad admite el corte si la especificación lo permite. Es necesaria, no suficiente: aún puede haber derivación de etiqueta, uso ilegítimo o contaminación global.

La misma condición puede expresarse como:

$$
X_i\in\mathcal I(t_0),
$$

donde $X_i$ es el vector de la fila, $t_0$ el corte, $\mathcal I(t_0)$ la información disponible y $\in$ pertenencia. Es ampliación didáctica, no fórmula literal del libro. Solo impone disponibilidad, no verdad, legitimidad o causalidad, y exige la versión *point-in-time*.

Explicar cuatro mecanismos. **Fuga de características o etiquetas**: una entrada contiene resultado o derivado posterior. `hora_real`, cancelación final y demanda total 09:00-09:30 se conocen después; sirven para evaluar, no para decidir esa franja. También puede filtrarse un código administrativo de cierre.

**Joins retrospectivos** unen el valor actual o final, no el vigente al corte: polígonos actuales, cancelación final, clima corregido o flota final. La consulta puede ejecutar correctamente y contaminar historia.

**Contaminación entrenamiento-evaluación**: imputación, escalado, vocabulario, variables o hiperparámetros usan todo el dataset; se consulta la prueba o se agregan periodos futuros. El procedimiento aprende de evaluación.

**Dependencias y duplicados** comparten viaje, vehículo o zona-franja entre entrenamiento y prueba. No siempre son fuga temporal estricta, pero contaminan la evaluación; la clave de separación debe representar la generalización.

**Lectura de la fórmula.** Los tiempos usan igual huso y definición; “disponible” exige recepción, validación y publicación. $\le$ se prueba por fila y característica. En $X_i\in\mathcal I(t_0)$, todos los componentes y transformaciones pertenecen al corte: una ventana con 09:01 incumple. Las fórmulas no prueban independencia ni ausencia de fuga entre entidades.

**Descripción detallada del diagrama.** Una línea horizontal azul con flecha hacia la derecha representa el avance del tiempo. Una marca dorada vertical representa el corte de las 09:00. Debajo de esa marca, una caja dorada dice “Decidir 09:00 para 09:00-09:30”; combina tiempo de decisión y horizonte. A la izquierda hay dos cajas amarillas válidas: “GPS recibido hasta 08:55” y “Calendario y flota disponible”. Sus flechas azules convergen en la decisión, indicando que estaban disponibles antes del corte. A la derecha hay dos cajas azules de resultado futuro: “Viajes completados a las 09:20” y “Demanda total de la franja”. Sus flechas verdes discontinuas apuntan hacia la decisión y están rotuladas “fuga”. La dirección hacia atrás no describe un flujo real; visualiza el uso retrospectivo prohibido de conocimiento futuro. Los colores distinguen entradas, decisión humana y resultados posteriores; no significan que todo GPS izquierdo sea correcto ni que todo dato derecho quede prohibido para siempre.

Orden exacto de lectura: 1) fijar la decisión a las 09:00 y el horizonte 09:00-09:30; 2) recorrer el eje de izquierda a derecha; 3) leer GPS recibido hasta 08:55; 4) leer calendario y flota disponible; 5) seguir las flechas válidas hacia la decisión; 6) leer viajes completados y demanda total; 7) seguir las flechas discontinuas en sentido inverso y nombrarlas como fuga; 8) leer el bloque inferior sobre tres relojes; 9) agregar verbalmente disponibilidad como cuarto reloj operacional.

Interpretación válida: reconstruir con la versión recibida y procesada. El diagrama **no afirma** que todo GPS previo sea correcto o suficiente, que calendario y flota sean exactos, que resultados no sirvan para decisiones posteriores ni que 08:55 sea regla universal. Tampoco prueba causalidad, independencia, calidad o ausencia de fuga en transformaciones: solo fija la frontera temporal.

Ejemplo oral obligatorio: “Para decidir a las 09:00 sobre 09:00-09:30, un GPS con evento 08:54 y recepción 08:55 es temporalmente válido, si además fue procesado y estaba disponible. Un GPS con evento 08:58 pero recepción 09:04 es inválido para esa decisión: ocurrió antes, pero el sistema todavía no lo conocía. Puede incorporarse al histórico retrospectivo y a decisiones posteriores, conservando ambos tiempos, pero no debe reescribir lo que el sistema sabía a las 09:00”. Pregunta de comprobación visual: “¿A qué lado se ubica el GPS 08:58 recibido 09:04?”. Por disponibilidad, a la derecha del corte para esa decisión. Conclusión visual: el pasado del fenómeno y el pasado conocido por el sistema no son el mismo conjunto.

**Ejemplo de movilidad.** A las 09:00 se construye una fila por zona para 09:00-09:30. Son candidatas válidas las solicitudes recibidas y validadas, flota publicada y GPS oportunos. `hora_real`, estado de cancelación final y demanda total de la franja son posteriores. Si `hora_real` nula se rellena después con la hora de cierre o la cancelación se actualiza in situ, una consulta actual no reconstruye el estado de las 09:00. Se requieren snapshots o historial de vigencia.

**Por qué produce evaluación optimista.** El futuro reduce incertidumbre: `hora_real`, cancelación y demanda revelan el resultado; duplicados y transformaciones globales reducen novedad. Las métricas superan lo alcanzable, incluso con modelos simples y validación formal sobre datos ya contaminados.

**Diferencia con sobreajuste.** El **sobreajuste** aprende peculiaridades de entrenamiento legítimo; la fuga accede indebidamente al resultado o evaluación. Regularizar puede reducir el primero, no legitima `hora_real`; hasta un modelo lineal explota fuga.

**Detección.** **Auditoría temporal** por campo; **replay** cronológico sin estados finales; **ablation** de variables sospechosas; **partición temporal** con transformaciones ajustadas en entrenamiento; búsqueda de duplicados, entidades compartidas y agregados que cruzan cortes. Investigar rendimiento extraordinario y diferencias entre retrospectiva y modo sombra.

**Prevención.** **Point-in-time joins** por vigencia y disponibilidad; **snapshots** inmutables; timestamps separados de evento, recepción, procesamiento, disponibilidad y decisión; **requisitos de latencia** con tolerancia y degradación; pruebas automatizadas de cortes, ventanas, ajuste en entrenamiento, claves y cardinalidad. Versionar etiquetas y ejecutar replay antes del piloto.

**Error frecuente o límite.** Creer que ordenar por `hora_evento` resuelve todo, que usar datos históricos autoriza conocer su versión final o que una partición temporal elimina fugas creadas antes de dividir. Tampoco toda variable muy predictiva es fuga: se necesita examinar mecanismo y disponibilidad.

**Comprobación.** Plantear cuatro casos: GPS 08:54/recibido 08:55, válido temporalmente; GPS 08:58/recibido 09:04, inválido; demanda total 09:00-09:30, etiqueta posterior; promedio global calculado con semanas futuras, contaminación. Pedir para cada uno reloj violado y control preventivo.

**Conclusión que debe quedar.** La evaluación solo representa producción si cada fila reconstruye lo que el sistema realmente sabía, con versiones, dependencias y transformaciones compatibles con el corte.

**Transición sugerida.** “La actividad reunirá unidad, decisión, fuentes, baseline y este control temporal en una ficha revisable”.

## Diapositiva 35. Actividad guiada: ficha del problema

**Correspondencia con el libro.** Capítulo 1, §1.1.6 y actividad de reflexión; capítulo 2, §§2.1.1-2.1.5, §2.3.8 y actividad integradora. La actividad adapta esos contenidos a movilidad; no reproduce una actividad homónima del libro.

**Propósito.** Producir en equipo una formulación de una página antes de elegir algoritmo y hacer visibles supuestos que otro equipo pueda contrastar.

**Guion sugerido.** Asignar treinta minutos y diez de contraste. Completar: necesidad, usuarios y afectados; zona-franja, población y alcance; decisión, acciones y autoridad; corte y treinta minutos; tres tipos de pregunta; fuentes e integración; baseline, valor y detención; fuga y control.

**Conceptos y términos.** *Afectados* no siempre usan la herramienta. *Exclusión*: uso no evaluado. *Detención*: cobertura, baseline, riesgo o falta de uso. *Entregable*: formulación, no promesa.

**Composición visual relevante.** La lista numerada organiza ocho componentes y la caja inferior fija tiempo. Leer la lista una vez, luego agrupar oralmente en propósito, unidad, reloj, fuentes y evaluación. La numeración ayuda a distribuir trabajo, pero no implica independencia: cambiar horizonte obliga a revisar entradas y etiqueta.

**Ejemplo de movilidad.** Corte 09:00, horizonte 09:00-09:30, unidad zona-franja, baseline demanda de franja equivalente anterior, valor P90 sin elevar cancelaciones, abstención si cobertura o latencia cae bajo umbral acordado.

**Error frecuente o límite.** Comenzar por algoritmo, usar “toda la ciudad” sin cobertura, llamar acción a una probabilidad o escribir “supervisión humana” sin persona y poder concreto.

**Comprobación.** Antes del intercambio, cada equipo responde: “¿Qué cambia en el mundo si la evidencia cambia?”. Si no puede nombrar una acción distinta, debe revisar accionabilidad.

**Conclusión que debe quedar.** La ficha hace examinable la coherencia antes de invertir en integración o modelado.

**Transición sugerida.** “La revisión no premiará complejidad: buscará correspondencia y límites explícitos”.

## Diapositiva 36. Criterios de revisión

**Correspondencia con el libro.** Capítulo 2, método de revisión de §2.1.1, §§2.1.3-2.1.5 y criterios de la actividad [AGUA-01], adaptados a movilidad.

**Propósito.** Proporcionar una lista de control cualitativa para detectar saltos entre unidad, reloj, datos, baseline, valor y autoridad.

**Guion sugerido.** Exigir evidencia para: coherencia zona-franja; población, alcance y horizonte; disponibilidad; tipos de pregunta; procedencia e integración; baseline; valor, riesgos y detención; autoridad efectiva. La devolución contiene fortaleza, supuesto no demostrado y corrección prioritaria, sin cuestionario ni puntaje.

**Conceptos y términos.** *Verificable*: comprobable por otra persona. *Baseline realista*: alternativa disponible. *Riesgo*: fallo, impacto, control y responsable.

**Composición visual relevante.** Ocho viñetas ocupan el cuerpo y una caja inferior define el entregable: ficha más diagrama necesidad-evidencia-decisión-impacto. Leer las viñetas en pares: granularidad y alcance; tiempo y tipo de tarea; procedencia y baseline; riesgo y autoridad. Así se evita una revisión puramente documental.

**Ejemplo de movilidad.** Una ficha puede ser técnicamente clara y aun fallar si mover dos vehículos viola cobertura. La revisión debe marcar esa restricción como no compensable por menor error esperado.

**Error frecuente o límite.** Aceptar una entrada porque “está en la base”, premiar un baseline irrelevante o compensar fuga y falta de autoridad con otros aciertos.

**Comprobación.** Presentar: “90 % de precisión, sin corte ni usuario”. Debe rechazarse como formulación insuficiente; la métrica aislada no resuelve temporalidad ni uso.

**Conclusión que debe quedar.** La calidad de la ficha se juzga por coherencia verificable y capacidad de controlar fallos críticos.

**Transición sugerida.** “La puesta en común comprobará si esas elecciones resisten una explicación breve y preguntas de contraste”.

## Diapositiva 37. Puesta en común

**Correspondencia con el libro.** Capítulo 2, §§2.1.3-2.1.5, §2.2.4 sobre hipótesis y §2.2.5 sobre revisión y responsabilidad.

**Propósito.** Defender las decisiones centrales de la ficha, reconocer el supuesto que puede invalidarla y convertir contraste en evidencia siguiente.

**Guion sugerido.** En un minuto: decisión y autoridad; unidad, corte y horizonte; baseline y valor; supuesto invalidante. Contrastar oportunidad y granularidad, muestra y ausencias, modificación o detención. Traducir “datos insuficientes” a cobertura y “decide una persona” a cargo, información y poder.

**Conceptos y términos.** *Supuesto invalidante*: rompe evidencia-uso. *Incertidumbre*: rango, escenarios o abstención. *Defensa*: límites conocidos y controlados.

**Composición visual relevante.** La lista numerada superior fija cuatro contenidos obligatorios; el bloque inferior abre contraste con tres preguntas. Leer primero el minuto como argumento y luego usar el bloque como prueba. No convertir la puesta en común en una exposición de herramientas.

**Ejemplo de movilidad.** “Decide operaciones; unidad zona-franja; corte 09:00 para treinta minutos; baseline estacional; valor P90 y cancelaciones; si menos de 80 % de GPS llega antes del corte, el sistema se abstiene y vuelve al baseline”. El 80 % es solo ejemplo de ficha, no umbral prescrito por el libro.

**Error frecuente o límite.** Generalizar para parecer ambicioso, ocultar incertidumbre o afirmar que el revisor humano controla sin tiempo ni capacidad de detener.

**Comprobación.** Cerrar cada intervención con “¿qué evidencia mínima buscarían a continuación?”. Debe responderse con perfil, prueba de integración, replay o baseline, no “modelo más complejo”.

**Conclusión que debe quedar.** Una formulación defendible explica decisiones y límites con la misma claridad.

**Transición sugerida.** “Las defensas permiten recuperar siete ideas textuales que organizan toda la clase”.

## Diapositiva 38. Síntesis: siete ideas para conservar

**Correspondencia con el libro.** Capítulo 1, síntesis y §§1.1.1, 1.1.4-1.1.6; capítulo 2, síntesis. La diapositiva contiene exactamente siete ideas textuales.

**Propósito.** Consolidar las siete afirmaciones de la presentación sin sustituirlas por una síntesis diferente.

**Guion sugerido.** Conservar literalmente siete ideas: 1) datos parciales producidos; 2) evidencia, no solo modelos; 3) describir, predecir y decidir difieren; 4) unidad, población, alcance y horizonte preceden al algoritmo; 5) workflow, KDD y CRISP-DM son iterativos y trazables; 6) procedencia y reproducibilidad sostienen afirmaciones; 7) autoridad y responsabilidad son humanas e institucionales. Vincular respectivamente GPS, productos, cuantiles/probabilidad/utilidad, formulación, retornos, linaje y decisión.

**Conceptos y términos.** Conecta representación, evidencia, pregunta, formulación, metodología, procedencia y autoridad; no agrega vocabulario.

**Composición visual relevante.** La lista numerada es la composición central y debe leerse como siete afirmaciones completas, no como palabras clave. La caja final “Idea de cierre” comprime la secuencia: primero decisión y evidencia necesaria; después datos, métodos y herramientas. No existe un diagrama de cinco cajas en esta diapositiva.

**Ejemplo de movilidad.** Zona-franja y corte se fijan antes del modelo; fuentes conservan procedencia; la evaluación temporal produce evidencia; operaciones decide; monitoreo puede detener.

**Error frecuente o límite.** Alterar la lista para cerrar con herramientas, omitir autoridad o presentar iteración como ausencia de criterios.

**Comprobación.** Asignar una idea a cada grupo y pedir una consecuencia práctica. Para la idea 6: conservar versión de zonas y tiempos de recepción.

**Conclusión que debe quedar.** Primero se diseña la decisión y la evidencia necesaria; después se eligen datos, métodos y herramientas.

**Transición sugerida.** “La última figura reúne esas siete ideas en una sola cadena con controles y retorno”.

## Diapositiva 39. Síntesis visual: la cadena completa

**Correspondencia con el libro.** Capítulo 1, ciclo general y síntesis; capítulo 2, síntesis del ciclo de vida.

**Propósito.** Integrar formulación, procedencia, representación, evaluación, autoridad, impacto y aprendizaje en una lectura visual única.

**Guion sugerido.** Recorrer necesidad/alcance, formulación, fuentes/procedencia, representación, evidencia y decisión; bajar a impacto/monitoreo/aprendizaje y volver. Las tarjetas controlan pregunta/valor, calidad/licencia y baseline/riesgos. Cada flecha documenta una decisión; cada retorno, su evidencia.

**Conceptos y términos.** *Cadena* no implica rigidez; *impacto* incluye consecuencias no buscadas; *aprendizaje* modifica con justificación; *decisión autorizada* implica responsabilidad.

**Descripción detallada del diagrama.** Seis cajas horizontales forman la trayectoria principal. La primera azul dice “Necesidad y alcance”. La segunda verde contiene “Unidad, población, horizonte”. La tercera amarilla, “Fuentes y procedencia”. La cuarta verde, “Representación analítica”. La quinta amarilla, “Evidencia evaluada”. La sexta dorada, “Decisión autorizada”. Cinco flechas azules conectan la secuencia. Debajo de la representación hay una caja azul ancha “Impacto · monitoreo · aprendizaje”. Una flecha baja desde decisión y entra por la derecha; una flecha verde discontinua sale por la izquierda y regresa a necesidad. Tres tarjetas claras se sitúan debajo de necesidad, fuentes y evidencia: “Pregunta y valor”, “Calidad y licencia” y “Baseline y riesgos”. Funcionan como controles asociados, no como etapas posteriores.

Orden exacto de lectura: 1) cadena superior de izquierda a derecha; 2) detenerse entre fuentes y representación para recordar construcción de tabla; 3) detenerse entre representación y evidencia para recordar evaluación; 4) detenerse antes de decisión para recordar autoridad; 5) bajar a impacto; 6) seguir el retorno a necesidad; 7) leer las tres tarjetas de izquierda a derecha; 8) cerrar con la alerta. La codificación de colores recupera tipos usados en toda la presentación: azul para necesidad/decisión del dominio, verde para procesos, amarillo para datos/evidencia, dorado para humano y verde discontinuo para retroalimentación.

Interpretación válida: evidencia depende de formulación, procedencia, representación y evaluación; decidir exige monitorear consecuencias. No afirma necesidad de modelo, causalidad, observación total, retorno sin costo, legitimidad por licencia, baseline exhaustivo ni humano infalible. Ejemplo oral: cambiar límites afecta fuentes, tabla, evidencia y alcance; el linaje indica qué regenerar. Pregunta: si una acción no modifica espera con pronóstico preciso, volver a necesidad y teoría de cambio. Conclusión visual: cadena y retornos son reconstruibles.

**Ejemplo de movilidad.** Necesidad de reducir P90; zona-franja y treinta minutos; viajes/GPS/clima/zonas con procedencia; tabla al corte; pronóstico contra baseline; decisión de operaciones; monitoreo de espera, cancelación, cobertura, abstención y rechazos.

**Error frecuente o límite.** Leer la figura como pipeline automático, omitir controles inferiores o atribuir el impacto al modelo sin observar acción y contexto.

**Comprobación.** Pedir recorrer hacia atrás desde una cancelación observada: acción efectiva, decisión y evidencia, versión analítica, fuentes y formulación. Si se rompe una flecha, falta trazabilidad.

**Conclusión que debe quedar.** Cada flecha es una decisión documentable y cada retorno una oportunidad controlada de aprender.

**Transición sugerida.** “Las lecturas permiten profundizar los eslabones; la última lámina indica qué revisar y qué producto continuar”.

## Diapositiva 40. Lecturas y recursos

**Correspondencia con el libro.** Capítulo 1, §§1.1.1, 1.1.4-1.1.6; capítulo 2, §§2.1-2.4, con el énfasis textual indicado en la diapositiva.

**Propósito.** Orientar lecturas y continuidad sin afirmar enlaces o elementos visuales que no aparecen en la lámina.

**Guion sugerido.** Leer las referencias visibles: capítulo 1, §§1.1.1, 1.1.4-1.1.6; capítulo 2, §§2.1-2.4 con énfasis en 2.1.3, 2.2.1, 2.2.2, 2.3 y 2.4. Continuar con glosarios, ficha y linaje hasta zona-franja. Son referencias textuales; no afirmar hipervínculos visibles.

**Conceptos y términos.** *Continuidad*: corregir formulación; *glosario*: estabilizar términos; *linaje*: origen, extracción, transformación, claves, corte y producto.

**Composición visual relevante.** Dos bloques apilados organizan el cierre. El primero contiene dos viñetas, una por capítulo. El segundo contiene tres acciones. Leer de arriba abajo: profundización conceptual y metodológica, luego continuidad práctica. No hay fórmula, diagrama, tabla ni enlaces visibles que deban interpretarse.

**Ejemplo de movilidad.** Elegir GPS y dibujar evento con tiempo de emisión y recepción, extracción, validación, ventana, agregación por zona-franja y característica disponible al corte.

**Error frecuente o límite.** Inventar enlaces, subsecciones o recursos no visibles; convertir la continuidad en un cuestionario o saltar directamente a un algoritmo.

**Comprobación.** Pedir que cada equipo asocie una corrección con lectura: población y alcance, §2.1.3; inventario, §2.3 y su caso de movilidad; reproducibilidad, §2.4.

**Conclusión que debe quedar.** La continuidad consiste en profundizar conceptos y mejorar una ficha y un linaje verificables.

**Transición sugerida.** “Cerramos con la tesis inicial: primero decisión y evidencia; después datos, métodos y herramientas”.

### Referencias

- `../../../Libro/Capitulo_01_Ciencia_de_Datos_e_IA.md`
- `../../../Libro/Capitulo_02_Ciclo_de_vida_de_un_proyecto_de_datos.md`
- `Clase_01_Introduccion_a_la_Ciencia_de_Datos.md`
- `Clase_01_Introduccion_a_la_Ciencia_de_Datos.pdf`
