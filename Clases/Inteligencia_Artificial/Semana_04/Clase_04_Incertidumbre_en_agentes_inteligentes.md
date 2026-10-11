---
title: "Incertidumbre en agentes inteligentes"
subtitle: "De la observación imperfecta a la acción"
author: "Curso de Inteligencia Artificial"
course: "Inteligencia Artificial"
week: 4
class: 4
lang: es
---

# Incertidumbre en agentes inteligentes

## De la observación imperfecta a la acción

**Semana 4 · Clase 4**

**Recorrido conceptual:** `mundo real → observación → creencia → acción → consecuencia`, con retorno de actualización hacia la creencia.

*El agente no conoce el mundo: lo percibe, forma una creencia, la actualiza y actúa asumiendo consecuencias.*

---

# Punto de partida

En las semanas 1 a 3 construimos agentes que resuelven problemas. La Semana 1 ya reconoció entornos parcialmente observables y estocásticos.

- Semana 1: agentes, entornos y racionalidad (observabilidad parcial, estocasticidad).
- Semana 2: representación de estados, acciones, objetivos y restricciones.
- Semana 3: búsqueda ciega e informada sobre un modelo fijo.

Para ejecutar esa búsqueda, las Semanas 2 y 3 adoptaron una abstracción determinista: el estado siempre era conocido con exactitud y cada acción llevaba a un único resultado posible.

**Continuidad:** ahora levantamos esa abstracción: el agente no observa todo, sus sensores fallan y las acciones pueden tener resultados múltiples.

---

# Propósito y resultados de aprendizaje

**Propósito:** comprender por qué aparece la incertidumbre, cómo se representa y cómo un agente decide sin fingir certeza.

Al finalizar podremos:

- identificar fuentes y tipos de incertidumbre;
- distinguir estado real, percepción y creencia;
- construir una distribución conjunta y marginalizarla;
- actualizar una creencia con el teorema de Bayes;
- comparar acciones mediante costo esperado;
- reconocer cuándo una decisión se vuelve secuencial y qué papel juega una política;
- reconocer cómo se estiman estas probabilidades a partir de datos reales, más allá de una tabla dada.

*La clase es conceptual y numérica; no se implementan todavía algoritmos de aprendizaje por refuerzo.*

---

# Pregunta de apertura

> Si un robot no puede saber con certeza si el camino está libre, ¿cómo decide cruzar?

**Diagrama:** `[Inicio] → [?] → [Meta]` — nuestro caso conductor, desarrollado en detalle más adelante.

- ¿Qué es exactamente lo que no sabe?
- ¿Qué puede observar y qué puede fallar?
- ¿Qué información tenía antes de observar?
- ¿Qué cuesta equivocarse en cada sentido?
- ¿Cómo cambia su decisión al recibir una señal?

*La incertidumbre no es un defecto del agente: es una propiedad de su relación con el entorno.*

---

# ¿Por qué aparece la incertidumbre?

Un agente actúa sobre un mundo que no puede conocer por completo. Entre el mundo y la decisión median percepciones, modelos y evidencia, cada uno con pérdidas.

**Diagrama:** `mundo real → observación → creencia → acción → consecuencia`, con pérdidas por lo no observado, el ruido, lo mal modelado y lo que cambiará.

**Idea:** decidir con certeza es un caso especial; lo habitual es decidir con información parcial.

---

# Fuentes de incertidumbre

| Del lado de la observación | Del lado del mundo y del modelo |
|---|---|
| observabilidad parcial | resultados estocásticos |
| ruido de sensores | estados omitidos |
| información faltante o ambigua | cambio del entorno |
| datos insuficientes o mal cubiertos | |

*Las fuentes se combinan: un sensor ruidoso sobre un mundo cambiante y modelado de forma incompleta.*

---

# Dos tipos fundamentales

| Aleatoria | Epistémica |
|---|---|
| variabilidad que permanece aun conociendo el modelo | falta de conocimiento potencialmente reducible |
| resultado de un dado o de un sensor ruidoso | pocos datos o parámetros imprecisos |
| respuesta: reservas, redundancia, robustez | respuesta: más datos pertinentes, mejores mediciones |

**La frontera depende del modelo: lo que parece aleatorio puede explicarse al añadir variables.**

---

# Otras distinciones útiles

| Tipo | Pregunta que responde y ejemplo |
|---|---|
| Observacional | ¿la medición coincide con el estado? el sensor reporta alerta aunque el camino esté libre |
| Estructural | ¿el modelo incluye lo relevante? un robot que ignora que el piso puede estar húmedo |
| Distribucional (cambio de distribución) | ¿el futuro se parece al pasado? condiciones de hoy distintas de las históricas |
| Vaguedad | ¿la categoría tiene límites nítidos? "cerca", "alto", "riesgoso" |

*Ninguna etiqueta es universal: clasificar sirve para elegir la respuesta, no para fijar una división metafísica.*

---

# Problemáticas asociadas (I)

La incertidumbre no resuelta produce errores de razonamiento:

- confundir "no sé" con "no existe": la ausencia de dato no prueba ausencia del fenómeno;
- invertir la condición: $P(\text{alerta}\mid \text{bloqueo}) \neq P(\text{bloqueo}\mid \text{alerta})$;
- ignorar la tasa base: una señal poco común puede seguir indicando un estado poco probable;
- contar dos veces evidencia dependiente: dos sensores con una causa común no aportan información independiente.

*Cada error convierte un número correcto en una conclusión equivocada.*

---

# Problemáticas asociadas (II)

- falsa precisión: asignar un número sin respaldo ni análisis de sensibilidad;
- confundir probabilidad con importancia: un evento raro puede ser gravísimo;
- ocultar incertidumbre del modelo: presentar una creencia como si fuera un hecho;
- actuar fuera de distribución: confiar en datos históricos ante condiciones nuevas;
- explorar sin control: aprender por prueba y error en un entorno donde equivocarse daña.

*El riesgo no está en usar probabilidades, sino en presentarlas como certezas que no son.*

---

# ¿Qué podemos hacer?

| Reducir y representar | Decidir y controlar |
|---|---|
| obtener información pertinente | comparar acciones por costo o utilidad esperada |
| modelar estados posibles y sus probabilidades | hacer análisis de sensibilidad |
| mantener conjuntos de estados consistentes | elegir políticas robustas ante escenarios |

| Actualizar | Limitar el daño |
|---|---|
| incorporar evidencia con Bayes | abstenerse o pedir intervención humana |
| combinar observaciones sin doble conteo | aprender por interacción solo si es seguro |

---

# El flujo completo del agente

**Diagrama:** `mundo real → observación → creencia → acción → consecuencia`, con retorno de actualización hacia la creencia.

- La creencia resume todo lo que el agente sabe del estado.
- La acción se elige comparando consecuencias bajo esa creencia.
- La actualización convierte la observación nueva en creencia nueva.

*Esta cadena organiza todo lo que sigue: representación, actualización y decisión.*

---

# Caso conductor: un robot con sensor

Un robot avanza por un pasillo de tres celdas y debe llegar a la meta. La celda central puede estar libre o bloqueada; el robot no lo sabe.

**Diagrama:** `[Inicio] → [?] → [Meta]`, con la celda central marcada como estado oculto.

- Un sensor informa `alerta` o `sin alerta` sobre la celda central.
- El sensor es imperfecto: a veces se equivoca.
- El robot elige entre cruzar directo o rodear por un camino más largo.

*Este escenario mínimo aísla los conceptos: estado oculto, evidencia ruidosa y decisión bajo costo.*

---

# ¿Qué desconoce el robot?

El robot conoce su posición y su meta, pero ignora el estado real de la celda central.

- **Estado real:** libre o bloqueada, exista o no quien lo observe.
- **Percepción:** la lectura del sensor (`alerta` o `sin alerta`).
- **Creencia:** lo que el robot concluye a partir de sus observaciones previas.

**El estado no cambia por no observarlo; cambia lo que el agente puede afirmar sobre él.**

---

# Estado real vs percepción

La lectura del sensor no es el estado: es una proyección ruidosa.

| Símbolo | Significado |
|---|---|
| $B$ | evento "la celda está bloqueada" |
| $L$ | evento "la celda está libre" |
| $A$ | lectura "el sensor informa alerta" |
| $\neg A$ | lectura "el sensor informa sin alerta" |

*La dirección de la condición cambia la pregunta: $P(A\mid B)$ y $P(A\mid L)$ parten del estado real y describen qué lectura produce el sensor; $P(B\mid A)$ parte de una alerta observada y expresa cuánta probabilidad merece el bloqueo. En $P(A\mid L)$, $A$ sigue significando "el sensor emite una alerta": como el estado real es libre, esa alerta es un falso positivo.*

---

# El sensor y la previa

Para cuantificar el caso necesitamos dos ingredientes: cómo se comporta el sensor y qué tan probable era el bloqueo antes de mirar. "Alerta" es la salida del sensor, no el estado.

| El sensor (dado el estado) | La previa (antes de mirar) |
|---|---|
| $P(A\mid B)=0{,}90$, $P(A\mid L)=0{,}10$ | $P(B)=0{,}20$, $P(L)=0{,}80$ |
| sensibilidad: si está bloqueada, el sensor alerta en 90 de cada 100 casos | antes de observar, 20 de cada 100 celdas están bloqueadas |
| falsos positivos: si está libre, alerta igual en 10 de cada 100; son alertas falsas | esta frecuencia previa condiciona cuánto cambia la creencia |

**Valores ilustrativos:** $P(B)=0{,}20$, $P(A\mid B)=0{,}90$ y $P(A\mid L)=0{,}10$ se eligen para el ejercicio; en un caso real se estiman con datos o especificaciones del sensor.

---

# Cómo se construye la tabla

Cada celda de la tabla combina la previa con el comportamiento del sensor:

$$
P(\text{estado},\text{lectura})=P(\text{estado})\,P(\text{lectura}\mid \text{estado})
$$

Primero, los complementos del sensor:

$$
P(\neg A\mid B)=1-0{,}90=0{,}10, \qquad P(\neg A\mid L)=1-0{,}10=0{,}90
$$

$$
P(B,A)=P(B)\,P(A\mid B)=0{,}20(0{,}90)=0{,}18
$$

$$
P(B,\neg A)=P(B)\,P(\neg A\mid B)=0{,}20(0{,}10)=0{,}02
$$

$$
P(L,A)=P(L)\,P(A\mid L)=0{,}80(0{,}10)=0{,}08
$$

$$
P(L,\neg A)=P(L)\,P(\neg A\mid L)=0{,}80(0{,}90)=0{,}72
$$

*Cada expresión es una celda de la tabla siguiente: $P(B,A)$ bloqueada con alerta (verdadero positivo), $P(B,\neg A)$ bloqueada sin alerta (falso negativo), $P(L,A)$ libre con alerta (falso positivo) y $P(L,\neg A)$ libre sin alerta (verdadero negativo).*

---

# Cómo se interpreta la tabla

| | $A$ (alerta) | $\neg A$ (sin alerta) | Marginal |
|---|---:|---:|---:|
| $B$ (bloqueada) | 0,18 | 0,02 | 0,20 |
| $L$ (libre) | 0,08 | 0,72 | 0,80 |
| Marginal | 0,26 | 0,74 | 1,00 |

- **Filas:** estado real ($B$ bloqueada, $L$ libre).
- **Columnas interiores:** lectura del sensor ($A$ alerta, $\neg A$ sin alerta).
- **Celda interior:** probabilidad conjunta $P(\text{estado},\text{lectura})$.
- **Margen de fila:** previas $P(B)$ y $P(L)$.
- **Margen de columna:** $P(A)$ y $P(\neg A)$, la probabilidad de cada lectura.
- **Esquina:** suma total $1$, comprobación de normalización.

*$P(B,A)=0{,}18$: probabilidad de que la celda esté bloqueada y el sensor informe alerta. Que exista una alerta no demuestra bloqueo: la celda $P(L,A)=0{,}08$ muestra que el sensor también alerta cuando la celda está libre.*

---

# Marginalizar: probabilidad de una lectura

La probabilidad de una lectura se obtiene marginalizando el estado:

$$
P(A)=P(A\mid B)P(B)+P(A\mid L)P(L)
$$

Con los números del ejemplo:

$$
P(A)=0{,}90(0{,}20)+0{,}10(0{,}80)=0{,}18+0{,}08=0{,}26
$$

$$
P(\neg A)=0{,}10(0{,}20)+0{,}90(0{,}80)=0{,}02+0{,}72=0{,}74
$$

*Para saber cuán probable es una alerta se suman todos los casos en que el sensor alerta: bloqueada con alerta más libre con alerta, $P(A)=P(B,A)+P(L,A)=0{,}18+0{,}08=0{,}26$.*

---

# Independencia de observaciones

Dos observaciones son independientes (dado el estado) cuando cada una aporta información nueva:

$$
P(A_1,A_2\mid B)=P(A_1\mid B)\,P(A_2\mid B)
$$

- Si dos sensores comparten una causa común o miden el mismo fallo, multiplicarlos cuenta dos veces la evidencia.
- Asumir independencia cuando no existe produce confianza excesiva.

**En nuestro caso:** si el robot incorporara un segundo sensor, esta sería la condición para combinar ambas lecturas sin sobreestimar la evidencia.

*La independencia es un supuesto que debe justificarse, no una propiedad automática de tener dos mediciones.*

---

# Actualizar creencias: teorema de Bayes

La creencia sobre el estado, tras observar la lectura, se actualiza:

$$
P(B\mid A)=\frac{P(A\mid B)\,P(B)}{P(A)}
$$

- $P(B)$ (previa): ¿qué probabilidad tenía el bloqueo antes de observar?
- $P(A\mid B)$ (verosimilitud): si había bloqueo, ¿qué probabilidad tenía el sensor de alertar?
- $P(A)$ (evidencia): ¿qué probabilidad había de observar una alerta, cualquiera fuera el estado?
- $P(B\mid A)$ (posterior): después de observar la alerta, ¿qué probabilidad tiene el bloqueo?

*Bayes no decide por nosotros: convierte la observación en una creencia coherente con el modelo.*

---

# Efecto de la tasa base

Con una previa $P(B)=0{,}20$:

$$
P(B\mid A)=\frac{0{,}90(0{,}20)}{0{,}26}\approx0{,}6923
$$

Aunque la sensibilidad es alta, la posterior no es $0{,}90$: una alerta puede venir de una celda bloqueada o de una libre, y la frecuencia previa de cada estado decide cuántas alertas corresponden a bloqueos reales.

Si la celda bloqueada fuera rarísima, por ejemplo $P(B)=0{,}01$, una alerta apenas elevaría la creencia:

$$
P(B\mid A)=\frac{0{,}90(0{,}01)}{0{,}90(0{,}01)+0{,}10(0{,}99)}\approx0{,}083
$$

*La misma señal no significa lo mismo en poblaciones con prevalencias distintas.*

---

# Números del ejemplo

| Lectura | Posterior $P(B\mid \cdot)$ | Lectura de la creencia |
|---|---:|---|
| $\neg A$ (sin alerta) | $\frac{0{,}10(0{,}20)}{0{,}74}\approx0{,}027$ | creencia baja en bloqueo |
| $A$ (alerta) | $\frac{0{,}90(0{,}20)}{0{,}26}\approx0{,}692$ | creencia alta en bloqueo |

- Sin alerta, el bloqueo pasa de $0{,}20$ a $0{,}027$.
- Con alerta, el bloqueo pasa de $0{,}20$ a $0{,}692$.

*La misma previa produce posteriores opuestas según la observación; ahora falta convertir creencia en acción.*

---

# De la creencia a la acción: matriz de costos

La creencia por sí sola no dice qué hacer; hace falta valorar las consecuencias.

| Acción | Bloqueada | Libre |
|---|---:|---:|
| Cruzar | 30 | 0 |
| Rodear | 8 | 8 |

- Cruzar es gratis si la celda está libre, pero cuesta 30 si choca.
- Rodear siempre cuesta 8: es el desvío seguro.

*Valores hipotéticos del ejercicio; en un caso real se fijan según daño, tiempo y recursos. Un falso negativo (cruzar con bloqueo) puede costar más que un falso positivo (rodear sin bloqueo); cada error se valora por separado.*

---

# Valor esperado de una acción

Usamos $EC$ por *Expected Cost* (**costo esperado**). Para una acción $a$, evidencia $E$ y posibles estados $s$:

$$
EC(a\mid E)=\sum_s P(s\mid E)\,C(a,s)
$$

donde $C(a,s)$ es el costo de ejecutar la acción $a$ cuando ocurre el estado $s$.

En criollo: para cada estado posible $s$ multiplicamos qué tan probable creemos que es ($P(s\mid E)$) por lo que costaría actuar si ese estado fuera el real ($C(a,s)$), y sumamos. El resultado es un promedio de costos ponderado por la creencia: no predice qué va a pasar, mide qué tan cara es la acción **en promedio**.

*La evidencia $E$ puede ser una lectura del sensor, pero también puede no haber evidencia todavía. La fórmula es siempre la misma; lo que cambia de un caso a otro es qué creencia $P(s\mid E)$ usamos.*

---

# Decidir sin haber observado nada

Antes de leer el sensor no hay evidencia: $E=\varnothing$. En ese caso $P(s\mid E)$ es simplemente la previa $P(s)$, porque todavía no condicionamos en ningún dato.

Con previa $P(B)=0{,}20$ (y $P(L)=0{,}80$), reemplazando en la fórmula:

$$
EC(\text{cruzar})=P(B)(30)+P(L)(0)=0{,}20(30)+0{,}80(0)=6
$$

$$
EC(\text{rodear})=P(B)(8)+P(L)(8)=8
$$

Con la previa, **cruzar** tiene menor costo esperado ($6<8$).

*Es el mismo $EC(a\mid E)$ de la diapositiva anterior, solo que con $E=\varnothing$: por eso "sin observar" no usa otra fórmula, usa la misma con la creencia inicial.*

---

# Decidir después de observar

Con alerta, la creencia sube a $P(B\mid A)=0{,}692$:

$$
EC(\text{cruzar}\mid A)=0{,}692(30)+0{,}308(0)\approx20{,}8
$$

$$
EC(\text{rodear}\mid A)=8
$$

Con sin alerta, la creencia baja a $P(B\mid \neg A)=0{,}027$:

$$
EC(\text{cruzar}\mid \neg A)=0{,}027(30)+0{,}973(0)\approx0{,}8
$$

**Regla resultante:** rodear ante alerta; cruzar ante sin alerta.

*La observación cambió la acción: ahora la decisión es una función de la evidencia, no una elección fija.*

---

# Umbral y sensibilidad

Llamemos $p=P(B\mid E)$ a la creencia de bloqueo, con o sin evidencia. Cruzar conviene cuando su costo esperado es menor que rodear:

$$
p(30)+(1-p)(0)<8 \quad\Longrightarrow\quad p<\frac{8}{30}\approx0{,}267
$$

- Previa $p=0{,}20<0{,}267$: conviene cruzar sin observar.
- Alerta $p=0{,}692>0{,}267$: conviene rodear.
- Sin alerta $p=0{,}027<0{,}267$: conviene cruzar.

**Análisis de sensibilidad:** si los costos cambian (choque más grave, desvío más barato), el umbral se desplaza y la decisión puede invertirse.

---

# Errores frecuentes al decidir

- invertir el condicional: tratar $P(A\mid B)$ como si fuera $P(B\mid A)$;
- ignorar la previa: usar solo la sensibilidad del sensor;
- confundir creencia con certeza: "el sensor dijo alerta" no es "está bloqueada";
- valorar mal los errores: tratar falso positivo y falso negativo como equivalentes;
- omitir el costo de actuar: decidir sin sumar el precio de la propia decisión.

*La fórmula es corta; construir bien sus componentes es el trabajo real.*

---

# De una decisión a una secuencia

Hasta aquí decidimos una sola vez. En un problema real, cada acción cambia el estado y condiciona las decisiones siguientes.

- Cruzar coloca al robot en otra celda; rodear consume batería.
- La posición, la batería y el riesgo acumulado forman el estado.
- Ya no basta "la mejor acción ahora": importa la mejor regla para cada situación futura.

**Nuevo objeto:** una política indica qué acción tomar en cada estado, anticipando consecuencias futuras.

*La decisión única es el caso especial en que el futuro no depende de la acción presente.*

---

# Política: qué hacer en cada situación

Con observabilidad parcial, el agente no conoce el estado oculto: decide sobre su creencia acerca de él, junto con lo que sí conoce (posición, batería).

| Situación (posición, batería, creencia) | Acción de la política |
|---|---|
| creencia de bloqueo por debajo del umbral ($<0{,}267$) | cruzar |
| creencia por encima del umbral, batería suficiente | rodear |
| creencia alta, batería insuficiente para rodear | detenerse / pedir asistencia |

- La política condensa la decisión en una regla por situación.
- Puede ser determinista (siempre la misma acción) o estocástica (con probabilidades).

*Una política no es indecisión ni una lista de ocurrencias: es una regla sistemática y auditable.*

---

# Recompensa y exploración

Si el agente debe aprender a actuar por interacción, aparece el aprendizaje por refuerzo (RL).

- **Recompensa:** expresa el objetivo, pero puede estar mal diseñada y premiar atajos.
- **Explorar vs explotar:** probar acciones da información y también costo o riesgo.
- Explorar una celda desconocida puede revelar un obstáculo o provocar un choque.
- Explotar siempre lo conocido consolida una creencia quizá equivocada.

---

# ¿Cuándo corresponde RL?

RL no es la respuesta a toda incertidumbre. Es apropiado cuando:

- hay decisiones secuenciales significativas;
- la acción presente modifica estados y opciones futuras;
- existe retroalimentación repetida y un objetivo medible;
- se puede explorar con seguridad o en simulación.

**No usar RL cuando:** una regla simple ya resuelve el problema; la interacción es escasa, costosa o no ética; equivocarse durante el entrenamiento es inaceptable.

---

# Transferencia: el caso de una app de rutas

Una app de rutas debe elegir entre un camino largo, siempre disponible, y un camino corto cuyo estado no puede confirmar con certeza: se nutre de las trazas GPS de los celulares que lo cruzan, y por allí pasa tan poca gente que la señal es débil.

**Diagrama:** `[Origen] → [Destino]` por dos caminos: uno corto (¿transitable u obstruido?) y uno largo (siempre disponible).

- **Estado real** ↔ el paso corto es transitable en auto (aunque sea lento) u obstruido para autos.
- **Lectura** ↔ trazas GPS de otros vehículos en ese tramo, en los últimos minutos.
- **Previa** ↔ tasa histórica de obstrucción del paso, para esa franja horaria.
- **Matriz de costos** ↔ tiempo de viaje esperado, en minutos.

*El mismo esquema del robot —estado, lectura, previa, sensor y costo— se aplica; lo que cambia es el dominio.*

---

# El sensor y la previa en el cruce

Igual que con el robot, hacen falta dos ingredientes: cómo se comporta la evidencia y qué tan probable era la obstrucción antes de mirar.

| La evidencia GPS (dado el estado) | La previa (antes de mirar) |
|---|---|
| $P(D\mid O)=0{,}95$, $P(D\mid T)=0{,}30$ | $P(O)=0{,}30$, $P(T)=0{,}70$ |
| $D$: la señal es débil (pocas o ninguna traza vehicular reciente) | tasa histórica de obstrucción en esa franja horaria |
| $P(D\mid T)=0{,}30$: si el camino está transitable, en 3 de cada 10 ventanas la señal es igualmente débil por el bajo tránsito; es una falsa señal de obstrucción | $O$: obstruido para autos. $T$: transitable, aunque sea lento |

**Diferencia con el robot:** acá la evidencia es menos discriminante ($P(D\mid T)=0{,}30$ no es chico), porque el bajo tránsito propio de la calle también genera poca señal. Valores ilustrativos; en un caso real se estiman con datos históricos del propio sistema.

---

# Tabla conjunta y posterior

Con el mismo procedimiento de las diapositivas 17 a 21 ($P(\text{estado},\text{lectura})=P(\text{estado})\,P(\text{lectura}\mid\text{estado})$, y Bayes para actualizar la probabilidad de obstrucción):

| | $D$ (señal débil) | $\neg D$ (señal normal) | Marginal |
|---|---:|---:|---:|
| $O$ (obstruido) | 0,285 | 0,015 | 0,30 |
| $T$ (transitable) | 0,21 | 0,49 | 0,70 |
| Marginal | 0,495 | 0,505 | 1,00 |

$$
P(O\mid D)=\frac{0{,}285}{0{,}495}\approx0{,}576 \qquad P(O\mid \neg D)=\frac{0{,}015}{0{,}505}\approx0{,}030
$$

*Con señal débil, la creencia de obstrucción sube de $0{,}30$ a $0{,}576$; con señal normal, baja a $0{,}030$.*

---

# Costos y decisión: ¿corto o largo?

| Ruta | Transitable | Obstruido |
|---|---:|---:|
| Corto | 5 | 20 |
| Largo | 12 | 12 |

*minutos de viaje; si el corto resulta obstruido, hay que retroceder y tomar igual el largo.*

$$
EC(\text{corto}\mid D)=5(0{,}424)+20(0{,}576)\approx13{,}6 \qquad EC(\text{largo}\mid D)=12
$$

$$
EC(\text{corto}\mid \neg D)=5(0{,}970)+20(0{,}030)\approx5{,}4 \qquad EC(\text{largo}\mid \neg D)=12
$$

**Regla resultante:** largo ante señal débil ($13{,}6>12$); corto ante señal normal ($5{,}4<12$) — la misma estructura que "rodear ante alerta, cruzar ante sin alerta".

*El umbral de indiferencia es $p^{*}=7/15\approx0{,}467$: exactamente donde cae la frontera entre ambas reglas.*

---

# De la tabla a un sistema real

En el robot, la tabla venía dada. En un sistema real hay que construirla:

- **Previa:** se estima con el historial del propio sistema, condicionada a franja horaria y día — agregarla sin condicionar repite el error de ignorar la tasa base.
- **Evidencia dado el estado:** se estima contando frecuencias sobre pares (señal observada, estado confirmado después), no se define a mano.
- **Pocos datos, sensor débil:** en un tramo de bajo tránsito hay pocas observaciones para calibrar; esa es incertidumbre epistémica sobre el propio modelo, no solo sobre el estado.
- **En producción:** no se arma una tabla de dos estados; se entrena un clasificador que combina varias señales y devuelve $P(\text{obstruido}\mid\text{features})$ directamente — el mismo cálculo, aprendido de datos en vez de definido a mano.
- **Combinar evidencia y actualizar:** sumar fuentes exige justificar independencia (diapositiva 20); si el patrón de uso cambia, el modelo queda desactualizado (actuar fuera de distribución, diapositiva 10).

*La mecánica de Bayes no cambia; lo que cambia es de dónde provienen los parámetros probabilísticos que utiliza.*

---

# También aplica: el caso del agua

El mismo patrón —estado real, lectura, previa, evidencia y matriz de costos— se aplica a la vigilancia de calidad del agua: el estado es la condición real del agua, la lectura es el resultado del análisis o del sensor, y la decisión es revisar o no revisar.

---

# Síntesis conceptual

**Diagrama:** `mundo real → observación → creencia → acción → consecuencia`, con retorno de actualización.

- La incertidumbre se origina en observación, mundo y modelo.
- Se representa con distribuciones conjuntas y creencias.
- Se actualiza con Bayes ante nueva evidencia.
- Se decide comparando costo esperado de las acciones.
- Se secuencializa cuando las acciones cambian el futuro.

---

# Errores que deben evitarse (repaso)

**Repaso:** esta lista integra los errores de razonamiento (diapositivas 9–10) y de decisión (diapositiva 28) ya estudiados.

- confundir estado real, percepción y creencia;
- invertir condicionales o ignorar la tasa base;
- contar dos veces evidencia dependiente;
- presentar una creencia como certeza;
- valorar los errores de decisión como equivalentes;
- decidir sin análisis de sensibilidad sobre costos y probabilidades;
- aplicar RL a un problema que no es secuencial o donde explorar daña.

**Una respuesta correcta pertenece a un modelo y un objetivo declarados; la responsabilidad es examinar ambos.**

---

# Cierre y próxima clase

Hoy construimos el puente entre el agente que percibe y el agente que decide.

- La incertidumbre es parte del problema, no un ruido a ignorar.
- La probabilidad representa creencias; la decisión agrega consecuencias.
- La secuencialidad prepara el terreno para el aprendizaje por refuerzo.

**Próxima clase:** actividad práctica integradora (robot y vehículo autónomo) y diseño experimental de aprendizaje automático: supervisado, no supervisado y evaluación fuera de muestra.
