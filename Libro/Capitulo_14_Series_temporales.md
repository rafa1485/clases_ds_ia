# Capítulo 14. Análisis y pronóstico de series temporales

Una serie temporal es una colección de observaciones ordenadas por el instante en que se producen. Esta definición parece sencilla, pero modifica de manera profunda el análisis estadístico: dos observaciones cercanas pueden depender entre sí, la distribución puede cambiar con el calendario y el futuro no está disponible al construir una predicción. Mezclar aleatoriamente los registros, como se haría en muchos problemas supervisados, destruye justamente la estructura que se desea aprender.

El propósito de este capítulo es desarrollar un lenguaje riguroso para describir, modelar y evaluar series. Se distinguirán frecuencia, tendencia, estacionalidad, ciclo, ruido, faltantes y valores atípicos; se estudiarán dependencia, estacionariedad, autocorrelación y transformaciones; se derivará la familia ARIMA; y se establecerá un protocolo de evaluación temporal. Los ejemplos proceden de movilidad, energía, comercio minorista y manufactura. El objetivo no es elegir un algoritmo por prestigio, sino formular un pronóstico reproducible para un horizonte, una información disponible y una decisión concretos.

Sea $y_t$ el valor observado en el instante o intervalo $t$, con $t=1,\ldots,n$. En una serie de conteos, $y_t$ puede ser la cantidad de pickups de taxi en una zona durante una hora; en energía, la demanda eléctrica de un edificio cada quince minutos; en comercio, las unidades vendidas por día. El origen de tiempo, la zona horaria, la frecuencia y la regla de agregación forman parte de la definición de la variable. Sin ellos, la sucesión de números no constituye un objeto analítico bien especificado.

**Convenciones de lectura.** Una letra mayúscula, como $Y_t$, denota una variable aleatoria; la minúscula $y_t$, su realización observada. $\widehat y_{t+h|t}$ es el pronóstico emitido al terminar $t$ para el objetivo $t+h$, y $\mathcal F_t$ representa toda la información legítimamente disponible en ese origen. El rezago $k$ siempre se mide en pasos de la frecuencia declarada: en una serie horaria, $k=24$ equivale a un día solo si la cuadrícula y el tratamiento del horario civil están bien definidos. Los parámetros verdaderos se distinguen de sus estimaciones cuando ello afecta la derivación; en explicaciones operativas se omite el sombrero si no existe ambigüedad.

Pronosticar no equivale a explicar causalmente. Un modelo puede aprovechar que la demanda de energía a las 10:00 se parece a la de las 9:00 sin afirmar que una lectura cause la siguiente. Tampoco equivale a reconstruir datos: la imputación estima un valor no observado dentro de una historia, mientras el pronóstico anticipa un valor todavía no realizado. Ambas tareas pueden compartir métodos, pero poseen conjuntos de información y criterios diferentes.

La secuencia recomendada a lo largo del capítulo es: definir el objeto temporal; auditar su medición; proponer estructura; transformar solo si existe una razón; ajustar candidatos parsimoniosos; simular pronósticos históricos; y conectar error e incertidumbre con una decisión. Saltar directamente al ajuste suele producir una curva numéricamente correcta para una pregunta mal definida. Por eso cada ejemplo explicita unidad, origen y horizonte antes de mencionar el modelo.

## 14.1. Estructura de las series temporales

El primer análisis debe responder qué se observó, cuándo y mediante qué proceso de medición. Una gráfica temporal es indispensable, aunque no suficiente. Conviene acompañarla con perfiles por hora, día de semana o mes; distribuciones condicionadas por calendario; cobertura; y anotaciones de eventos conocidos. La estructura visual sugiere hipótesis, no las demuestra. Una oscilación puede ser estacionalidad real, un cambio del sistema de captura o la combinación de ambas.

### 14.1.1. Índice temporal y frecuencia

El índice temporal ordena las observaciones y define distancias entre ellas. Puede ser regular, cuando $t_{i+1}-t_i=\Delta$ para todo $i$, o irregular, cuando los intervalos varían. ARIMA y muchas herramientas de descomposición presuponen una cuadrícula regular. Por ello, antes de modelar eventos individuales suele agregarse su cantidad o magnitud en intervalos fijos.

La **frecuencia de muestreo** es el ritmo al que se obtienen observaciones: cada minuto, hora, día o semana. La **frecuencia de un patrón** es la cantidad de repeticiones por unidad de tiempo. Su inversa es el periodo. Si un perfil se repite cada 24 observaciones horarias, su periodo es $m=24$ y su frecuencia discreta es $1/24$ ciclos por observación. En una serie horaria también puede existir un periodo semanal $m=168$. Debe evitarse confundir la granularidad del dato con la periodicidad de un fenómeno.

Agregar modifica la pregunta. Si $x_i$ son pickups individuales y $I_t$ es la hora $t$, el conteo horario es

$$
y_t=\sum_i \mathbf{1}(x_i\text{ ocurre en }I_t).
$$

Una suma conserva volúmenes; una media representa nivel medio; un máximo representa carga pico. Ninguna agregación es universal. El intervalo debe ser suficientemente corto para la decisión y suficientemente largo para evitar una serie casi enteramente nula o dominada por ruido de captura.

Una cuadrícula regular exige distinguir un **cero observado** de un **intervalo sin cobertura**. En una tienda abierta y correctamente medida, cero ventas puede ser un valor legítimo. Si el sistema dejó de transmitir, completar con cero inventa una caída. También deben fijarse zona horaria, horario de verano, límites inclusivos de los intervalos y calendario comercial. Dos registros con la misma hora local durante un cambio de horario pueden corresponder a instantes diferentes.

**Fallo frecuente.** Inferir la frecuencia solo porque las marcas de tiempo “parecen horarias”. Deben calcularse diferencias, duplicados y huecos. Si una planta registra solo cuando cambia el sensor, la ausencia de fila no significa valor cero ni frecuencia regular.

### 14.1.2. Tendencia

La tendencia $T_t$ representa una evolución suave del nivel a largo plazo respecto de la escala estudiada. Puede ser creciente, decreciente, aproximadamente lineal, curvada o presentar cambios de pendiente. Una formulación local sencilla es

$$
T_t=\beta_0+\beta_1t,
$$

pero una recta no debe extrapolarse mecánicamente. La expansión de una cadena minorista puede impulsar ventas durante meses y luego saturarse; una mejora de eficiencia puede reducir gradualmente el consumo energético por unidad producida; una obra puede cambiar de forma abrupta los flujos de movilidad.

La tendencia depende de la ventana. Una subida durante dos semanas puede ser parte de un ciclo mensual, mientras que en una ventana de tres años podría resultar irrelevante. Para reconocerla se emplean medias o medianas móviles, suavizado y descomposición. Una media móvil centrada de ancho impar $2k+1$ es

$$
\widetilde T_t=\frac{1}{2k+1}\sum_{j=-k}^{k}y_{t+j}.
$$

Es útil para descripción retrospectiva, pero usa futuro respecto de $t$ y no puede convertirse sin más en una característica predictiva. En operación se utiliza una versión rezagada calculada únicamente con $y_{t-k},\ldots,y_t$.

Tendencia no significa causalidad. Una serie creciente no prueba que el tiempo cause el cambio; el tiempo resume factores omitidos. Tampoco garantiza continuación. Para pronosticar debe preguntarse qué mecanismo podría sostenerla y hasta qué horizonte. Los cambios estructurales, como una nueva tarifa eléctrica o una modificación de turnos de producción, obligan a reestimar el nivel.

**Ejemplo.** Las ventas semanales de una familia de productos aumentan tras ampliar el número de locales. Si se modela el total, aparece tendencia; si se divide por locales activos, puede desaparecer. Ambas series son válidas, pero responden preguntas diferentes: volumen total frente a productividad media.

### 14.1.3. Estacionalidad

La estacionalidad es una variación sistemática asociada a posiciones conocidas de un calendario y repetida con periodo aproximadamente fijo. Ejemplos son las puntas de demanda eléctrica a ciertas horas, la reducción de actividad manufacturera durante fines de semana o el perfil semanal de pickups. Si el periodo es $m$, una representación aditiva escribe $S_{t+m}=S_t$ y suele imponer $\sum_{j=1}^{m}S_j=0$ para identificar el nivel.

Una serie puede tener varias estacionalidades: intradiaria, semanal y anual. Con datos horarios, $m=24$ describe posición horaria y $m=168$ combinación de hora y día. La estacionalidad de calendario no siempre ocupa igual número de observaciones: meses y festividades móviles tienen duración variable. En esos casos son preferibles indicadores de calendario o modelos con múltiples componentes antes que forzar un único periodo.

La amplitud puede ser constante o proporcional al nivel. En el primer caso, una estructura aditiva

$$
y_t=T_t+S_t+R_t
$$

es razonable. Si los picos crecen al crecer el nivel, puede ser más apropiada una estructura multiplicativa

$$
y_t=T_tS_tR_t,
$$

con componentes positivos. Al tomar logaritmos, esta última se vuelve aditiva: $\log y_t=\log T_t+\log S_t+\log R_t$.

Reconocer estacionalidad requiere varias repeticiones. Dos semanas horarias permiten ver indicios semanales, pero ofrecen poca evidencia sobre estabilidad; tres meses no sostienen una estacionalidad anual. Además, una media por hora calculada con todo el conjunto filtraría información futura si se usa como entrada del modelo. Dentro de cada corte de validación debe aprenderse solo con el pasado.

**Fallo frecuente.** Llamar “estacional” a cualquier onda. Si su duración y fecha no son relativamente previsibles, puede tratarse de un ciclo. Una promoción que cambia de semana cada año requiere una variable de promoción conocida, no necesariamente un término estacional fijo.

### 14.1.4. Ciclos

Los ciclos son movimientos de expansión y contracción con duración o amplitud no estrictamente fijas. Se diferencian de la estacionalidad porque no están anclados de manera estable a una posición del calendario. Los ciclos de pedidos industriales, reposición de inventario o actividad económica pueden extenderse durante periodos variables y cambiar de forma.

Una representación conceptual es

$$
y_t=T_t+C_t+S_t+R_t,
$$

donde $C_t$ varía más lentamente que el ruido, pero no satisface necesariamente $C_{t+m}=C_t$. En ventanas cortas, ciclo y tendencia pueden ser inseparables. Lo que parece una tendencia descendente puede ser apenas la fase descendente de un ciclo largo. Por ello, atribuir componentes requiere contexto y longitud suficiente.

El ciclo no debe estimarse escogiendo a posteriori una onda que ajuste bien. Esa práctica produce una explicación visual sin capacidad predictiva. Resultan más defendibles variables vinculadas al mecanismo: cartera de pedidos, inventario, precio o índice de actividad, siempre que su valor futuro sea conocido o pueda pronosticarse honestamente.

**Ejemplo.** Una fábrica recibe lotes grandes cada cuatro a siete semanas según los pedidos. La carga de máquinas exhibe máximos recurrentes, pero no un periodo fijo. Tratarla como estacionalidad mensual genera pronósticos desfasados. Incorporar pedidos confirmados puede explicar el ciclo mejor que imponer $m=30$.

En series breves, conviene describir el movimiento como fluctuación de baja frecuencia y reconocer incertidumbre, en vez de bautizarlo como ciclo económico. La distinción tiene consecuencias: una estacionalidad estable admite un baseline estacional; un ciclo irregular exige información adicional o intervalos más amplios.

### 14.1.5. Ruido

El ruido $R_t$ reúne variación no explicada por los componentes considerados. No es sinónimo de dato inútil. Puede contener fluctuación aleatoria inherente, error de medición, factores omitidos o estructura que el modelo aún no capturó. Solo después del ajuste se evalúa si el residuo se aproxima a una innovación impredecible.

En un modelo elemental,

$$
y_t=\mu+\varepsilon_t,\qquad E(\varepsilon_t)=0,
\quad \operatorname{Var}(\varepsilon_t)=\sigma^2,
$$

y el ruido blanco satisface además $\operatorname{Cov}(\varepsilon_t,\varepsilon_{t-k})=0$ para $k\ne0$. Incorrelación no implica independencia, salvo bajo supuestos adicionales como normalidad conjunta. Un residuo puede tener autocorrelación nula y conservar cambios de varianza o colas pesadas.

La relación señal-ruido depende de la frecuencia. El consumo energético minuto a minuto puede ser muy irregular; al agregar por hora se atenúan fluctuaciones, aunque también se pierden picos operativos. El alisado mejora legibilidad, no crea información. Además, el ruido de conteos suele aumentar con el nivel: una aproximación de Poisson tiene media y varianza iguales, por lo que asumir varianza constante puede ser inadecuado.

No debe “limpiarse” toda desviación. Un pico de ventas durante una campaña es señal para un sistema que deba anticipar campañas, aunque sea ruido para un análisis de demanda ordinaria. La clasificación depende del objetivo y de la información disponible. El procedimiento correcto conserva el dato original, registra cualquier tratamiento y evalúa sensibilidad con y sin él.

### 14.1.6. Valores faltantes y atípicos temporales

Un faltante temporal puede aparecer como celda vacía dentro de una cuadrícula o como intervalo completamente ausente. Primero se determina su causa: falta de actividad, interrupción de captura, cierre planificado o error de integración. El mecanismo afecta el tratamiento. Completar siempre con cero sesga nivel y estacionalidad; interpolar siempre suaviza picos y reduce artificialmente el error.

Las opciones incluyen mantener el faltante y usar métodos compatibles, imputar con último valor, interpolación, mediana estacional o modelo. Toda imputación para pronóstico debe ser **causal**: al instante $t$ no puede consultar $y_{t+1}$. La interpolación bilateral es válida para reconstrucción histórica claramente etiquetada, pero no para simular operación en una validación.

Un atípico temporal es una observación incompatible con su contexto. Puede ser:

- **puntual**, como una lectura extrema aislada;
- **contextual**, normal a mediodía pero anómala de madrugada;
- **colectiva**, una secuencia moderada cuya duración es excepcional;
- **cambio de nivel**, desde el cual la serie adopta otro régimen.

Para detectarlos se comparan residuos robustos, mediana y desviación absoluta mediana, bandas por posición estacional o modelos de intervención. Si $r_t$ es un residuo y $M=\operatorname{mediana}(r_t)$, una puntuación robusta puede ser

$$
z_t^{(r)}=\frac{0.6745(r_t-M)}{\operatorname{mediana}|r_t-M|}.
$$

El umbral identifica candidatos, no errores confirmados. Un pico de pickups tras un evento puede ser real; una caída simultánea en muchas zonas y proveedores puede sugerir cobertura. Sustituir atípicos sin auditoría elimina precisamente los eventos de mayor interés.

**Regla práctica:** conservar una columna de valor original, otra de valor tratado y una bandera con motivo, método y momento de detección. Evaluar el modelo tanto en condiciones ordinarias como ante episodios extremos.

### 14.1.7. Descomposición

Descomponer consiste en representar la serie mediante componentes interpretables. En el esquema aditivo,

$$
y_t=T_t+S_t+R_t,
$$

la magnitud estacional no depende del nivel. En el multiplicativo, $y_t=T_tS_tR_t$, las variaciones son relativas. La elección debe apoyarse en gráficos y estabilidad de varianza, no en una preferencia automática.

La descomposición clásica con periodo $m$ sigue, conceptualmente, estos pasos:

1. estimar tendencia-ciclo mediante una media móvil de longitud relacionada con $m$;
2. quitar tendencia, restando o dividiendo;
3. promediar los valores destendenciados en cada posición estacional;
4. normalizar los índices estacionales;
5. definir el resto como lo no explicado.

Los extremos pierden estimaciones cuando la media es centrada y los atípicos contaminan promedios. Métodos robustos y suavizados locales toleran mejor cambios graduales en tendencia y estacionalidad. Aun así, la descomposición no identifica causas y sus componentes dependen del método, periodo y ventana.

Una descomposición retrospectiva puede usar observaciones a ambos lados de $t$ para explicar el pasado. Un sistema de pronóstico no dispone de ese futuro. Esta diferencia es crucial: las componentes utilizadas como características deben recalcularse causalmente en cada origen de validación. De otro modo, la curva de tendencia cerca del corte transmite el comportamiento posterior.

La utilidad práctica es triple: revelar estructura, construir baselines y diagnosticar residuos. Si el resto conserva picos cada 24 rezagos, la estacionalidad no se eliminó. Si su amplitud aumenta con el nivel, puede faltar una transformación. Una descomposición bonita no prueba que el patrón sea estable fuera de muestra.

### 14.1.8. Ejemplo práctico guiado: descomposición de una serie de demanda

Considérese la demanda eléctrica horaria de una planta durante dieciséis semanas. La unidad es kWh por hora; la planta opera tres turnos de lunes a viernes y uno reducido los fines de semana. El objetivo es anticipar las próximas seis horas para programar cargas flexibles.

**Inspección.** La cuadrícula revela cuatro huecos por mantenimiento del medidor, que se marcan como falta de cobertura y no como consumo cero. La gráfica muestra un nivel lentamente creciente, máximos diurnos y mínimos dominicales. Los perfiles por hora y día sugieren periodos $m_1=24$ y $m_2=168$. Un pico aislado coincide con una prueba documentada de maquinaria y se conserva.

**Hipótesis de estructura.** Como la amplitud diaria crece con el nivel, se compara una descomposición aditiva sobre $y_t$ con otra sobre $\log y_t$. La segunda produce una estacionalidad relativa más estable. Conceptualmente,

$$
\log y_t=L_t+S_{24,t}+S_{168,t}+R_t.
$$

El componente $L_t$ aumenta tras incorporar una nueva línea; $S_{24,t}$ separa turnos; $S_{168,t}$ recoge el fin de semana. El resto muestra variación mayor durante cambios de turno, señal de que la varianza condicional aún no es uniforme.

**Qué podría predecirse.** El calendario de turnos y los perfiles diarios son parcialmente repetibles; el nuevo nivel puede extrapolarse con cautela durante seis horas. La prueba excepcional de maquinaria no es predecible sin agenda. Los huecos no deben enseñar falsas caídas. Si los turnos futuros son conocidos, constituyen una variable exógena legítima.

**Contraste.** Un baseline estacional $\widehat y_{t+h|t}=y_{t+h-168}$ ofrece una referencia fuerte. Si el modelo complejo no lo supera en varios orígenes, la descomposición no justifica mayor complejidad.

**Preguntas de diagnóstico:** ¿cambia la conclusión al excluir la semana de incorporación de la línea?, ¿el residuo mantiene autocorrelación?, ¿los intervalos cubren las horas de cambio de turno?, ¿una decisión a seis horas necesita modelar también el máximo, además del promedio?

## 14.2. Dependencia temporal y estacionariedad

La estructura temporal permite que el pasado informe sobre el futuro, pero invalida la suposición de observaciones intercambiables. Esta sección formaliza la dependencia y las condiciones bajo las cuales puede aprenderse una relación relativamente estable. Estacionarizar no es un ritual: es una estrategia para que los patrones estimados en el pasado sean transferibles al horizonte de interés.

### 14.2.1. Dependencia serial

Existe dependencia serial cuando la distribución de $Y_t$ condicionada por valores pasados difiere de su distribución marginal. En términos simples, conocer $Y_{t-1},Y_{t-2},\ldots$ cambia lo que se espera de $Y_t$. Una forma lineal se expresa mediante covarianza; dependencias no lineales pueden existir aun con covarianza cero.

La dependencia puede originarse en inercia física, hábitos, inventarios, calendario o agregación. La temperatura de un edificio cambia gradualmente; las ventas de hoy afectan el inventario de mañana; la movilidad a las 9:00 se parece a la de otras mañanas. También puede ser espuria: dos observaciones comparten una tendencia y parecen correlacionadas sin interacción dinámica.

La esperanza condicional de un proceso de primer orden puede escribirse

$$
E(Y_t\mid Y_{t-1},Y_{t-2},\ldots)=g(Y_{t-1}).
$$

Si, dado $Y_{t-1}$, el pasado más remoto no añade información, el proceso cumple una propiedad de Markov de orden uno. ARIMA no exige interpretar esa propiedad como causalidad; modela regularidades predictivas lineales.

La dirección temporal importa. Una correlación entre ventas y publicidad no indica si la publicidad anticipa ventas o fue decidida tras observarlas. Para usar una variable en $t+h$, debe conocerse en el origen $t$. La dependencia útil se define respecto del conjunto de información $\mathcal F_t$, no solo respecto de columnas disponibles retrospectivamente.

### 14.2.2. Estacionariedad

Un proceso es **estrictamente estacionario** si la distribución conjunta de $(Y_{t_1},\ldots,Y_{t_k})$ es igual a la de $(Y_{t_1+h},\ldots,Y_{t_k+h})$ para todo conjunto de tiempos y desplazamiento $h$. Es una condición fuerte. En práctica se usa estacionariedad débil o de segundo orden:

$$
E(Y_t)=\mu,\qquad \operatorname{Var}(Y_t)=\sigma^2,
\qquad \operatorname{Cov}(Y_t,Y_{t-k})=\gamma_k,
$$

donde media y varianza no dependen de $t$ y la covarianza depende solo del rezago $k$.

Una serie con tendencia determinista no es estacionaria en media. Un paseo aleatorio

$$
Y_t=Y_{t-1}+\varepsilon_t
$$

tampoco lo es: aunque los incrementos tengan media cero, $\operatorname{Var}(Y_t)=t\sigma_\varepsilon^2$ crece. Ambos casos pueden parecer ascendentes, pero requieren tratamientos distintos.

Las pruebas de raíz unitaria ayudan, pero tienen potencia limitada, dependen de términos deterministas y no sustituyen gráficos ni contexto. Una prueba puede no rechazar raíz unitaria en una serie corta; otra puede rechazarla debido a un cambio estructural. La pregunta operativa es si las relaciones usadas por el modelo permanecen suficientemente estables durante entrenamiento y uso.

La estacionalidad tampoco equivale a no estacionariedad irresoluble. Puede modelarse explícitamente o eliminarse mediante diferencias estacionales. En una serie con cambios de régimen, transformar no basta: conviene acortar ventana, añadir intervenciones o revisar el proceso generador.

### 14.2.3. Autocorrelación

La autocovarianza de rezago $k$ es

$$
\gamma_k=\operatorname{Cov}(Y_t,Y_{t-k}),
$$

y la autocorrelación es $\rho_k=\gamma_k/\gamma_0$. Para una muestra de media $\bar y$ se estima, según una convención habitual,

$$
\widehat\rho_k=
\frac{\sum_{t=k+1}^{n}(y_t-\bar y)(y_{t-k}-\bar y)}
{\sum_{t=1}^{n}(y_t-\bar y)^2}.
$$

La función de autocorrelación (ACF) representa $\widehat\rho_k$ para distintos rezagos. Un máximo en $k=24$ en datos horarios sugiere repetición diaria; máximos en múltiplos de 168 sugieren patrón semanal. Una caída muy lenta desde valores próximos a uno puede indicar tendencia o raíz unitaria, no necesariamente memoria de muchos órdenes.

Las bandas aproximadas $\pm1.96/\sqrt n$ sirven como referencia bajo ruido blanco, pero no son pruebas independientes: se observan muchos rezagos y los estimadores están relacionados. Buscar un único punto que cruce la banda favorece falsos hallazgos.

Antes de interpretar la ACF deben tratarse tendencia y estacionalidad. Una serie minorista creciente mostrará correlaciones altas aun si las desviaciones alrededor de la tendencia son independientes. También importa la longitud: estimaciones a rezagos grandes utilizan menos pares y son inestables.

La ACF es descriptiva, no causal. Puede guiar órdenes y diagnosticar residuos, pero la elección final se valida fuera de muestra. Para residuos, autocorrelaciones importantes indican que queda información lineal aprovechable.

### 14.2.4. Autocorrelación parcial

La autocorrelación parcial de orden $k$ mide la asociación lineal entre $Y_t$ y $Y_{t-k}$ después de controlar los rezagos intermedios $Y_{t-1},\ldots,Y_{t-k+1}$. Puede definirse como el coeficiente $\phi_{kk}$ de $Y_{t-k}$ en la regresión

$$
Y_t=c+\phi_{k1}Y_{t-1}+\cdots+\phi_{kk}Y_{t-k}+u_t.
$$

La función PACF grafica esos coeficientes. En un proceso AR($p$) ideal, la PACF se corta tras $p$, mientras la ACF decae. En un MA($q$), la ACF se corta tras $q$ y la PACF decae. “Corte” significa que los valores poblacionales posteriores son cero; en muestras finitas nunca se observa una frontera perfecta.

La PACF distingue correlación directa de asociación transmitida. Si $Y_t$ depende de $Y_{t-1}$ y este de $Y_{t-2}$, la ACF en rezago 2 puede ser alta aunque $Y_{t-2}$ no aporte efecto lineal adicional. La PACF intenta retirar ese camino intermedio.

No debe seleccionarse un orden contando barras significativas de manera automática. Diferenciación excesiva, atípicos, mezcla de estacionalidades y muestras pequeñas distorsionan ambos gráficos. Se combinan conocimiento del periodo, ACF/PACF, criterios de información, parsimonia, diagnóstico residual y validación temporal.

### 14.2.5. Transformaciones de varianza

Muchos modelos lineales presuponen innovaciones de varianza aproximadamente constante. En demanda y conteos, la dispersión suele crecer con el nivel. Una transformación monótona puede estabilizarla, hacer aditivos efectos multiplicativos y reducir la influencia de extremos.

Para valores positivos, la transformación de Box-Cox es

$$
g_\lambda(y)=
\begin{cases}
(y^\lambda-1)/\lambda, & \lambda\ne0,\\
\log y, & \lambda=0.
\end{cases}
$$

$\lambda=1$ se aproxima a la escala original, $\lambda=1/2$ a raíz cuadrada y $\lambda=0$ a logaritmo. La raíz es frecuente en conteos; el logaritmo interpreta diferencias como cambios relativos. Si existen ceros, $\log y$ no está definido. Sumar una constante altera especialmente valores pequeños y debe justificarse. Transformaciones que admiten cero y negativos pueden ser alternativas, pero sus parámetros se aprenden solo con entrenamiento.

Pronosticar en escala transformada y aplicar la inversa no produce necesariamente la media en escala original. Por desigualdad de Jensen,

$$
g^{-1}\{E[g(Y)]\}\ne E(Y).
$$

Con logaritmos y error normal de varianza $\sigma_h^2$, la media aproximada es $\exp(\widehat z_{t+h}+\sigma_h^2/2)$, mientras $\exp(\widehat z)$ se relaciona con la mediana. La corrección debe reflejar el objetivo.

Una transformación no corrige dependencia ni cambios estructurales. Debe verificarse si mejora estabilidad, residuos, calibración e interpretación. En conteos bajos, un modelo probabilístico discreto puede resultar más natural que forzar normalidad.

### 14.2.6. Diferenciación regular y estacional

El operador de rezago $B$ se define por $BY_t=Y_{t-1}$. La diferencia regular es

$$
\nabla Y_t=(1-B)Y_t=Y_t-Y_{t-1}.
$$

Si $Y_t=Y_{t-1}+\varepsilon_t$, entonces $\nabla Y_t=\varepsilon_t$: la diferencia elimina la raíz unitaria. Una segunda diferencia es $(1-B)^2Y_t=Y_t-2Y_{t-1}+Y_{t-2}$ y puede retirar una tendencia estocástica de orden mayor, aunque rara vez debe aplicarse sin evidencia.

La diferencia estacional de periodo $m$ es

$$
\nabla_mY_t=(1-B^m)Y_t=Y_t-Y_{t-m}.
$$

En datos horarios, $m=24$ compara con la misma hora del día anterior; $m=168$, con la misma hora de la semana anterior. Las diferencias pueden combinarse: $(1-B)(1-B^m)Y_t$.

Diferenciar reduce longitud, modifica interpretación y aumenta incertidumbre al reintegrar. La **sobrediferenciación** introduce dependencia artificial, eleva varianza y puede producir una ACF muy negativa en rezago uno. Si una tendencia determinista puede representarse explícitamente, no siempre hace falta diferenciarla. Si hay cambio de nivel, una diferencia genera un pulso, pero no garantiza estabilidad del régimen.

Para recuperar niveles, los pronósticos de diferencias se acumulan. Si $w_t=Y_t-Y_{t-1}$,

$$
\widehat Y_{t+h|t}=Y_t+\sum_{j=1}^{h}\widehat w_{t+j|t}.
$$

Los errores también se acumulan; por eso los intervalos suelen ensancharse con $h$. Toda decisión sobre $d$ y $D$ debe tomarse dentro de cada ventana de entrenamiento, no mirando la serie futura completa.

### 14.2.7. Ejemplo práctico guiado: transformación de una serie no estacionaria

Supóngase una serie diaria de unidades vendidas por una cadena durante dos años. El nivel crece, la variabilidad aumenta y existe un patrón semanal. El objetivo es pronosticar siete días.

1. La gráfica original muestra picos cada sábado y dispersión proporcional al nivel. La ACF decae lentamente y tiene máximos en múltiplos de siete.
2. Se aplica $z_t=\log(y_t+1)$ porque hay algunos ceros legítimos. La constante y su impacto se documentan. La amplitud semanal queda más uniforme.
3. Se calcula $w_t=(1-B^7)z_t=z_t-z_{t-7}$. Esto elimina gran parte del perfil semanal, pero persiste una evolución lenta.
4. Se compara añadir diferencia regular, $v_t=(1-B)w_t$, frente a modelar una deriva. La doble transformación deja una autocorrelación negativa fuerte en rezago uno y peor validación: indicio de sobrediferenciación. Se conserva solo $D=1$.

La secuencia conceptual es:

```text
para cada origen temporal de evaluación:
    estimar parámetros de transformación con el pasado disponible
    transformar el pasado
    decidir diferencias regulares y estacionales sin consultar el futuro
    ajustar el modelo en la serie resultante
    pronosticar y reintegrar hasta la escala original
    guardar errores por horizonte
comparar estabilidad, residuos y desempeño fuera de muestra
```

La transformación seleccionada no se acepta porque la gráfica “parezca estacionaria”. Se exige que la media y varianza locales sean más estables, que ACF/PACF sean interpretables, que los residuos mejoren y que MAE o una métrica escalada no empeoren. La inversión del logaritmo debe distinguir mediana y media. Una campaña futura no conocida seguirá siendo impredecible: transformar no reemplaza información.

## 14.3. Modelos ARIMA

ARIMA reúne modelos lineales parsimoniosos para la dinámica de una serie. Su fortaleza reside en representar dependencia y diferenciación con pocos parámetros, producir pronósticos probabilísticos bajo supuestos y ofrecer diagnósticos claros. No es una única receta ni garantiza superioridad frente a un baseline. La notación se entiende mejor usando innovaciones $\varepsilon_t$, errores nuevos que no eran previsibles con $\mathcal F_{t-1}$.

### 14.3.1. Modelos autorregresivos

Un modelo AR($p$) expresa el valor actual como combinación lineal de sus $p$ rezagos:

$$
Y_t=c+\phi_1Y_{t-1}+\cdots+\phi_pY_{t-p}+\varepsilon_t,
\qquad \varepsilon_t\sim WN(0,\sigma^2).
$$

Para AR(1), $Y_t=c+\phi Y_{t-1}+\varepsilon_t$. Si $|\phi|<1$, su media estacionaria se obtiene tomando esperanzas:

$$
\mu=c+\phi\mu \quad\Rightarrow\quad \mu=\frac{c}{1-\phi}.
$$

Al centrar $X_t=Y_t-\mu$, $X_t=\phi X_{t-1}+\varepsilon_t$. Sustituciones sucesivas producen $X_t=\sum_{j=0}^{\infty}\phi^j\varepsilon_{t-j}$, y por tanto

$$
\operatorname{Var}(Y_t)=\frac{\sigma^2}{1-\phi^2},
\qquad \rho_k=\phi^k.
$$

Si $\phi$ está cerca de uno, los choques persisten; si es negativo, aparecen alternancias. Con $\phi=1$ se obtiene un paseo aleatorio, no un AR estacionario.

El pronóstico AR(1) a un paso es $\widehat Y_{t+1|t}=c+\phi Y_t$. A $h$ pasos,

$$
\widehat Y_{t+h|t}=\mu+\phi^h(Y_t-\mu),
$$

que converge a la media. Para AR($p$), la estacionariedad requiere que las raíces del polinomio $1-\phi_1z-\cdots-\phi_pz^p$ estén fuera del círculo unitario.

Un orden alto puede memorizar ruido y generar coeficientes inestables por colinealidad entre rezagos. La interpretación es predictiva: $\phi_i$ es un efecto parcial lineal condicionado por otros rezagos, no un mecanismo causal.

### 14.3.2. Modelos de medias móviles

Un modelo MA($q$) representa el valor mediante innovaciones actuales y pasadas:

$$
Y_t=\mu+\varepsilon_t+\theta_1\varepsilon_{t-1}+\cdots+\theta_q\varepsilon_{t-q}.
$$

El nombre “medias móviles” puede inducir a error: no es la media móvil usada para suavizar observaciones, sino una combinación de errores no observados. Durante el ajuste, las innovaciones se infieren de manera recursiva.

Para MA(1), $Y_t=\mu+\varepsilon_t+\theta\varepsilon_{t-1}$. Su varianza es $\sigma^2(1+\theta^2)$ y

$$
\rho_1=\frac{\theta}{1+\theta^2},\qquad \rho_k=0\quad(k>1).
$$

Esta ACF truncada motiva su identificación. Un choque afecta $Y_t$ y hasta $q$ valores posteriores; luego desaparece explícitamente del modelo.

La condición de **invertibilidad** permite expresar innovaciones como función convergente de observaciones y escoger una representación única. Para MA(1) exige, con esta convención de signos, $|\theta|<1$. Distintas convenciones escriben signos opuestos; deben comprobarse al interpretar software.

El pronóstico MA(1) a un paso usa el residuo estimado: $\widehat Y_{t+1|t}=\mu+\theta\widehat\varepsilon_t$. Para $h>1$ vuelve a $\mu$, porque las innovaciones futuras tienen esperanza cero. En series donde los choques se disipan rápidamente, esta memoria finita es útil.

### 14.3.3. Modelos ARMA

ARMA($p,q$) combina persistencia autorregresiva y choques de media móvil:

$$
Y_t=c+\sum_{i=1}^{p}\phi_iY_{t-i}
+\varepsilon_t+\sum_{j=1}^{q}\theta_j\varepsilon_{t-j}.
$$

Con operadores,

$$
\phi(B)Y_t=c+\theta(B)\varepsilon_t,
$$

donde $\phi(B)=1-\phi_1B-\cdots-\phi_pB^p$ y $\theta(B)=1+\theta_1B+\cdots+\theta_qB^q$. El componente AR ofrece memoria potencialmente infinita con decaimiento; MA modela el efecto corto de innovaciones.

ARMA presupone una serie estacionaria. Aplicarlo directamente a un nivel con raíz unitaria produce relaciones espurias y pronósticos mal calibrados. Sus parámetros suelen estimarse conjuntamente por máxima verosimilitud, no mediante regresión ordinaria, porque los errores pasados son latentes y dependen de parámetros.

La parsimonia importa. Un ARMA pequeño puede aproximar la dinámica que requeriría muchos términos AR. No obstante, combinaciones AR y MA pueden casi cancelarse, dificultando identificación. Se revisan convergencia, raíces, incertidumbre de coeficientes y sensibilidad a inicialización.

**Fallo frecuente.** Elegir $p$ y $q$ para maximizar ajuste dentro de muestra. Añadir parámetros reduce residuos de entrenamiento, pero puede deteriorar pronóstico. Los criterios de información penalizan complejidad y la validación temporal comprueba transferencia.

### 14.3.4. Modelos ARIMA

ARIMA($p,d,q$) aplica un ARMA a una serie diferenciada $d$ veces:

$$
\phi(B)(1-B)^dY_t=c+\theta(B)\varepsilon_t.
$$

$p$ es el orden autorregresivo, $d$ el número de diferencias regulares y $q$ el orden de medias móviles. ARIMA(0,1,0) es el paseo aleatorio:

$$
(1-B)Y_t=\varepsilon_t,
\quad\text{de donde}\quad
\widehat Y_{t+h|t}=Y_t.
$$

Por ello, el baseline de último valor no es ingenuo en sentido despectivo: corresponde a un modelo probabilístico coherente. Si se añade deriva $c$ a las diferencias, $Y_t=Y_{t-1}+c+\varepsilon_t$ y $\widehat Y_{t+h|t}=Y_t+hc$.

Para ARIMA(1,1,0), $\Delta Y_t=\phi\Delta Y_{t-1}+\varepsilon_t$. Primero se pronostican cambios y luego se acumulan. La incertidumbre crece porque cada nivel futuro incorpora innovaciones. Bajo paseo aleatorio,

$$
\operatorname{Var}(Y_{t+h}-\widehat Y_{t+h|t})=h\sigma^2.
$$

El intercepto cambia de significado según $d$. En un modelo sin diferencias se relaciona con nivel medio; con una diferencia puede implicar deriva. Esta distinción evita interpretar una constante como media universal.

ARIMA modela relaciones lineales en la escala elegida. Puede funcionar muy bien con series cortas y patrones estables, pero no impone no negatividad y puede pronosticar conteos negativos. Transformación, modelos de conteo o truncamiento cuidadosamente evaluado son alternativas; recortar a cero cambia sesgo e intervalos y no debe ocultarse.

### 14.3.5. Componentes estacionales

SARIMA extiende ARIMA mediante operadores estacionales. Se denota

$$
\operatorname{ARIMA}(p,d,q)(P,D,Q)_m
$$

y satisface

$$
\Phi(B^m)\phi(B)(1-B)^d(1-B^m)^DY_t
=\Theta(B^m)\theta(B)\varepsilon_t.
$$

$P,D,Q$ son órdenes AR, de diferenciación y MA estacionales; $m$ es el periodo. Un término AR estacional de orden uno relaciona $Y_t$ con $Y_{t-m}$; un MA estacional relaciona innovaciones separadas por $m$.

Por ejemplo, SARIMA$(0,0,0)(0,1,0)_{168}$ implica $Y_t-Y_{t-168}=\varepsilon_t$ y su pronóstico es el último valor de la misma hora semanal. Es el baseline estacional expresado como modelo. Un modelo con factores regulares y estacionales genera también términos cruzados. Si

$$
(1-\phi B)(1-\Phi B^m)Y_t=\varepsilon_t,
$$

al expandir aparece $Y_t-\phi Y_{t-1}-\Phi Y_{t-m}+\phi\Phi Y_{t-m-1}$.

Elegir $m$ exige dominio y evidencia. En series horarias con patrones diario y semanal, un SARIMA estándar representa cómodamente un periodo principal; forzar órdenes enormes para ambos puede ser costoso. Variables de calendario, términos armónicos o métodos de estacionalidad múltiple constituyen alternativas.

No se estima estacionalidad anual con tres meses de observaciones. Tampoco debe confundirse una festividad única con componente estacional. Los componentes estacionales consumen datos: una diferencia semanal pierde 168 observaciones iniciales y requiere suficientes repeticiones para estimación estable.

### 14.3.6. Selección de órdenes

La selección de $(p,d,q)(P,D,Q)_m$ combina razonamiento y comparación. Un flujo defendible es:

1. fijar frecuencia y periodos plausibles con conocimiento del proceso;
2. estabilizar varianza si es necesario;
3. elegir $d$ y $D$ mínimos mediante gráficos, pruebas y señales de sobrediferenciación;
4. proponer órdenes pequeños con ACF/PACF de la serie estacionarizada;
5. estimar modelos candidatos y comprobar raíces, convergencia y residuos;
6. comparar criterios de información y, sobre todo, validación temporal.

El AIC se define como

$$
\operatorname{AIC}=-2\log L+2k,
$$

donde $L$ es la verosimilitud maximizada y $k$ el número de parámetros. BIC penaliza más con $\operatorname{BIC}=-2\log L+k\log n$. AICc corrige AIC para muestras pequeñas. Solo son comparables entre modelos ajustados a la misma respuesta, periodo y observaciones; cambiar transformación o pérdida rompe una comparación directa ingenua.

La búsqueda exhaustiva puede seleccionar accidentalmente peculiaridades del conjunto. Debe limitarse a una región parsimoniosa, registrar candidatos fallidos y reservar evaluación fuera de muestra. Si dos modelos tienen rendimiento semejante, se prefiere el más simple, estable y rápido de actualizar.

**Señales de alarma:** coeficientes enormes con errores estándar grandes, raíces casi canceladas, órdenes cercanos a la longitud estacional, no convergencia y resultados muy sensibles a pocas observaciones. Automatizar órdenes no elimina la responsabilidad de diagnosticar.

### 14.3.7. Variables exógenas

Una regresión dinámica o ARIMAX combina predictores $x_t$ con errores ARIMA:

$$
Y_t=\beta_0+\boldsymbol\beta^\top\mathbf x_t+n_t,
\qquad \phi(B)(1-B)^dn_t=\theta(B)\varepsilon_t.
$$

Los coeficientes explican asociación en la escala y condicionamiento especificados; no se vuelven causales por incluir dinámica. Pueden incorporarse turnos programados, festivos, precios anunciados o promociones aprobadas. Para pronosticar $Y_{t+h}$ se necesitan $x_{t+h}$ o escenarios de ellos.

La disponibilidad es más restrictiva que la existencia retrospectiva. El total cobrado al terminar un viaje no puede predecir pickups antes de que ocurran. Una temperatura futura observada en el dataset histórico tampoco estaba disponible; debe usarse el pronóstico meteorológico que habría existido en cada origen, o declararse un escenario.

Los indicadores de calendario son conocidos de antemano, pero su efecto puede cambiar. Las variables altamente correlacionadas generan coeficientes inestables. Rezagos exógenos deben respetar causalidad: $x_{t-1}$ puede ser válido, mientras $x_{t+1}$ es fuga salvo que sea una programación conocida.

Hay dos incertidumbres: la del modelo de respuesta y la de los predictores futuros. Condicionar intervalos a un único escenario exógeno suele subestimar incertidumbre. Es preferible presentar escenarios o propagar distribuciones cuando los predictores también se pronostican.

### 14.3.8. Diagnóstico de residuos

El residuo de un paso es $e_t=y_t-\widehat y_{t|t-1}$. Un modelo adecuado deja residuos de media cercana a cero, sin autocorrelación aprovechable, varianza razonablemente estable y distribución compatible con el procedimiento de intervalos. Ajuste visual de la serie no basta.

Se examinan:

- residuos en el tiempo, para nivel, régimen, varianza y extremos;
- histograma y cuantiles, para asimetría y colas;
- ACF residual, para dependencia remanente;
- residuos frente a ajustados y calendario;
- errores por horizonte y subgrupo operativo.

La prueba de Ljung-Box contrasta conjuntamente autocorrelaciones hasta $h$:

$$
Q=n(n+2)\sum_{k=1}^{h}\frac{\widehat\rho_k^2}{n-k}.
$$

Los grados de libertad deben considerar parámetros estimados. No rechazar no demuestra independencia; con pocas observaciones hay baja potencia. Rechazar con una muestra enorme puede señalar desviaciones pequeñas sin impacto operativo. El gráfico y la validación complementan la prueba.

Normalidad no es necesaria para que el pronóstico puntual sea útil, pero afecta intervalos gaussianos. Heterocedasticidad y extremos producen cobertura insuficiente. Se pueden transformar datos, usar intervalos empíricos, bootstrap compatible con dependencia o modelos de varianza.

Un residuo grande no debe borrarse para “aprobar” el diagnóstico. Se investiga si representa error, evento o cambio de régimen; luego se evalúa una intervención y se informa sensibilidad. El diagnóstico busca descubrir límites, no certificar perfección.

### 14.3.9. Ejemplo práctico guiado: pronóstico de consumo de agua

Una planta de alimentos necesita anticipar su consumo agregado diario de agua de proceso durante los próximos cinco días para coordinar producción, almacenamiento y compras de insumos. Hay dieciocho meses de datos, un patrón de cinco días laborables, cierres programados y una ampliación de capacidad a mitad del periodo. Se define $y_t$ como el volumen total utilizado en limpieza, cocción y enfriamiento durante el día $t$. El ejercicio estudia planificación de recursos dentro de la planta; no intenta localizar pérdidas ni representar una red de distribución.

**Preparación.** Se construye un calendario diario regular. Un día de cierre programado puede tener un consumo basal pequeño y legítimo; una interrupción del medidor queda faltante y no debe convertirse en cero. La varianza aumenta con el nivel de producción, por lo que se considera una transformación de raíz cuadrada. La ampliación se representa mediante un indicador de intervención y se discute si su efecto seguirá activo durante el horizonte.

**Identificación.** Tras una diferencia estacional $m=7$, la ACF conserva señal en rezago uno y la PACF decae. Se comparan un baseline del mismo día de la semana, modelos SARIMA de órdenes pequeños y una regresión dinámica con calendario de producción y cierres programados. No se elige por ajuste total: se ejecutan orígenes semanales sobre los últimos cuatro meses.

**Estimación y pronóstico conceptual:**

```text
definir origen, horizonte de cinco días y datos disponibles
para cada origen:
    ajustar transformación, intervención y modelo solo con fechas anteriores
    proporcionar calendario de producción conocido para los cinco días
    generar pronóstico puntual e intervalos
    invertir transformación con corrección coherente con media o mediana
    comparar cada paso con baseline estacional
agrupar métricas, cobertura y residuos por horizonte y tipo de día
```

**Resultados interpretables.** El SARIMA reduce MAE en días 1 y 2, pero no en día 5. Los intervalos al 90 % cubren solo el 78 % de las observaciones durante semanas de producción extraordinaria: están subcalibrados. Los residuos no muestran señal semanal fuerte, aunque sí asimetría positiva. La conclusión no es que el modelo haya “resuelto” el consumo, sino que mejora decisiones muy cortas y exige una reserva adicional cuando el programa incluye lotes atípicos.

**Fallas que deben discutirse:** utilizar el volumen producido definitivo cuando solo se conoce al cerrar el día; rellenar una interrupción de medición con cero; estimar el efecto de la ampliación usando toda la serie; confundir consumo observado con necesidad inevitable; y elegir el mejor orden tras mirar repetidamente el bloque final.

## 14.4. Evaluación de pronósticos

Evaluar pronósticos es reproducir cómo se habrían emitido en el pasado. Deben fijarse origen, horizonte, frecuencia, información disponible, regla de actualización, baseline, métrica y unidad de decisión antes de observar resultados. Una cifra agregada sin esa definición puede ocultar fuga, degradación con horizonte o fallas en periodos críticos.

### 14.4.1. Horizonte de predicción

En el origen $t$, el pronóstico a horizonte $h$ es $\widehat y_{t+h|t}$, construido con $\mathcal F_t$. El horizonte puede expresarse en pasos o tiempo civil: seis pasos horarios, siete días o cuatro semanas. Debe coincidir con la anticipación necesaria para actuar.

Hay estrategias de múltiples pasos. La **recursiva** ajusta un modelo de un paso y alimenta sus propios pronósticos; acumula error. La **directa** ajusta un modelo para cada $h$; evita recursión, pero usa menos pares efectivos y puede generar trayectorias incoherentes. La estrategia múltiple predice todo el vector y modela dependencias entre horizontes.

El error se define por origen y horizonte:

$$
e_{t,h}=y_{t+h}-\widehat y_{t+h|t}.
$$

Promediar todos los $h$ puede esconder que un método es excelente a una hora y deficiente a un día. Se informan métricas por horizonte y, si se resume, pesos ligados a la decisión.

Horizonte y frecuencia interactúan. Pronosticar 24 pasos horarios no equivale necesariamente a pronosticar el total diario: la suma de pronósticos horarios tiene una distribución conjunta y errores correlacionados. También deben declararse vacíos entre entrenamiento y prueba cuando los datos llegan con retraso.

### 14.4.2. Pronósticos puntuales e intervalos

Un pronóstico puntual resume una distribución predictiva. La media minimiza pérdida cuadrática esperada; la mediana minimiza pérdida absoluta; un cuantil $\tau$ minimiza pérdida de pinball. Por tanto, “el mejor valor” depende del costo de sobrestimar y subestimar.

Un intervalo predictivo $(L_{t,h},U_{t,h})$ de nivel nominal $1-\alpha$ busca

$$
P(L_{t,h}\le Y_{t+h}\le U_{t,h}\mid\mathcal F_t)=1-\alpha.
$$

No afirma que un parámetro fijo tenga esa probabilidad ni que cada intervalo individual contenga el futuro. Bajo errores gaussianos, puede aproximarse por

$$
\widehat y_{t+h|t}\pm z_{1-\alpha/2}\widehat\sigma_h.
$$

$\widehat\sigma_h$ debe incluir propagación temporal y, cuando corresponda, incertidumbre paramétrica y exógena. Los intervalos suelen ampliarse con el horizonte, aunque estacionalidad y restricciones pueden producir patrones no monótonos.

Se evalúan **cobertura** y **anchura**. Un intervalo infinito cubre todo y no sirve; uno estrecho que cubre poco transmite falsa precisión. La puntuación de intervalo penaliza ambas propiedades. La cobertura debe revisarse por horizonte, nivel de demanda y régimen, no solo globalmente.

Para conteos, límites negativos carecen de interpretación. Truncarlos después del cálculo cambia cobertura. Son preferibles distribuciones o transformaciones compatibles, o una calibración empírica declarada.

### 14.4.3. MAE, RMSE, MAPE y métricas escaladas

Para $N$ errores, el error absoluto medio es

$$
\operatorname{MAE}=\frac1N\sum_{i=1}^{N}|y_i-\widehat y_i|.
$$

Mantiene la unidad original y corresponde a pérdida absoluta. La raíz del error cuadrático medio,

$$
\operatorname{RMSE}=\sqrt{\frac1N\sum_{i=1}^{N}(y_i-\widehat y_i)^2},
$$

penaliza más los errores grandes. No es “mejor” por ser más sofisticada; es adecuada cuando grandes desviaciones son desproporcionadamente costosas.

El MAPE,

$$
\operatorname{MAPE}=\frac{100}{N}\sum_i\left|\frac{y_i-\widehat y_i}{y_i}\right|,
$$

no está definido con $y_i=0$, explota cerca de cero y penaliza asimétricamente. El sMAPE reduce algunos problemas, pero conserva ambigüedades y no debe presentarse como solución universal.

MASE escala el MAE por el error de un baseline ingenuo en entrenamiento. Para estacionalidad $m$,

$$
\operatorname{MASE}=
\frac{N^{-1}\sum|e_i|}
{(n-m)^{-1}\sum_{t=m+1}^{n}|y_t-y_{t-m}|}.
$$

Valores menores que uno superan, en promedio, la escala del baseline usado. RMSSE aplica cuadrados y raíz. Las métricas escaladas permiten comparar series de niveles distintos, pero el denominador debe calcularse sin prueba y puede ser cero en series constantes.

También se informa sesgo medio $N^{-1}\sum e_i$: un MAE bajo puede coexistir con subpronóstico sistemático. Para intervalos se añaden cobertura, anchura y puntuaciones propias. Seleccionar una métrica después de ver qué método gana es una forma de sesgo analítico.

### 14.4.4. Validación walk-forward

La validación *walk-forward* crea múltiples simulaciones de pronóstico. En cada origen se ajusta con pasado y se evalúa el bloque futuro inmediato. La ventana puede ser **expansiva**, que conserva toda la historia, o **deslizante**, que mantiene longitud fija para adaptarse a cambios de régimen.

Sean $t_1<\cdots<t_K$ los orígenes y $H$ el horizonte. El conjunto de errores es $e_{t_k,h}$ para $k=1,\ldots,K$ y $h=1,\ldots,H$. Un pseudocódigo seguro es:

```text
fijar primer origen, último origen, horizonte y regla de ventana
para cada origen t:
    entrenamiento = observaciones disponibles hasta t
    ajustar en entrenamiento imputación, escalado, transformación y modelo
    construir predictores futuros disponibles en t
    emitir pronósticos para h = 1,...,H
    guardar pronóstico, intervalo, observado, origen y horizonte
    avanzar el origen según la cadencia operativa
resumir errores por horizonte, fecha, régimen y serie
comparar todos los métodos en exactamente los mismos pares origen-objetivo
```

Reajustar en cada origen imita actualización completa; mantener parámetros y actualizar estado imita otro sistema. La validación debe copiar la política prevista. Orígenes solapados generan errores dependientes, de modo que la incertidumbre de diferencias entre modelos no debe calcularse como si fueran observaciones independientes.

Un único corte final es mejor que mezcla aleatoria, pero puede depender de una semana atípica. Múltiples orígenes revelan variación. Aun así, debe conservarse si es posible un periodo final para confirmación, evitando usarlo repetidamente en selección.

### 14.4.5. Prevención de fuga temporal

Hay fuga temporal cuando el proceso de entrenamiento utiliza información que no habría estado disponible al emitir el pronóstico. Puede ser directa, como incluir $y_{t+1}$, o sutil, como normalizar con media de toda la serie.

Fuentes comunes son:

- imputación o suavizado centrado que consulta valores posteriores;
- selección de variables y órdenes usando el bloque final;
- medias estacionales calculadas con todo el periodo;
- variables publicadas con retraso tratadas como contemporáneas;
- resultados del evento, como monto final o hora de cierre;
- agregaciones cuya ventana aún no terminó en el origen;
- mezcla aleatoria de filas temporalmente cercanas;
- ajuste de transformación, escalador o descomposición antes de dividir.

La prevención parte de una **tabla de disponibilidad**: para cada variable se registra instante del evento, instante de publicación y revisiones. El conjunto $\mathcal F_t$ contiene solo lo disponible en producción. Los pipelines completos se ajustan dentro de cada ventana.

La fuga también cruza entidades. Si se pronostican zonas y se usa el total de ciudad de la misma hora, ese total aún no se conoce. Una característica agregada debe rezagarse o construirse con un pronóstico. Duplicados de un mismo evento en entrenamiento y prueba constituyen otra contaminación.

Una puntuación extraordinariamente alta merece auditoría antes que celebración. Comparar con un baseline, desplazar deliberadamente variables y ejecutar una prueba de disponibilidad ayuda a detectar relaciones imposibles.

### 14.4.6. Comparación con modelos de machine learning

Un modelo de aprendizaje automático convierte la serie en tabla supervisada. Para cada instante puede usar rezagos $y_{t-1},y_{t-24},y_{t-168}$, estadísticas móviles causales y calendario. Árboles, *boosting* o redes aprenden relaciones no lineales e interacciones, pero no conocen el tiempo si no se lo representa.

La comparación justa exige misma variable objetivo, orígenes, horizontes, información y métrica. ARIMA integra dependencia y distribución mediante una estructura parsimoniosa; ML suele requerir más datos, diseño de características e intervalos adicionales. Ninguna familia domina siempre.

Ventajas potenciales de ML son no linealidad, muchas covariables y aprendizaje global entre numerosas series. Riesgos son sobreajuste, discontinuidades, dificultad de extrapolar tendencia y fuga en características. Un bosque no extrapola naturalmente fuera del rango observado; un modelo lineal con deriva sí puede hacerlo, aunque quizá de manera errónea.

La media móvil causal de ancho $w$ para predecir $t$ debe ser

$$
\overline y_{t-1}^{(w)}=\frac1w\sum_{j=1}^{w}y_{t-j},
$$

no una ventana que incluya $y_t$. Para múltiples pasos, debe decidirse si los rezagos futuros se reemplazan recursivamente, se entrenan modelos directos o se emite el vector completo.

Se incluyen baselines de último valor, estacional y media estacional. Si ML gana solo marginalmente y exige gran mantenimiento, el método simple puede ser preferible. La decisión incorpora latencia, explicabilidad, calibración, costo de actualización y robustez, no solo RMSE.

### 14.4.7. Incertidumbre y actualización del modelo

La incertidumbre procede de innovaciones, parámetros estimados, predictores futuros, elección de modelo y cambios del proceso. Los intervalos ARIMA estándar suelen representar bien la primera y parcialmente la segunda bajo supuestos; no cubren automáticamente una pandemia, una nueva política comercial o un sensor reemplazado.

Actualizar puede significar incorporar la observación al estado con parámetros fijos, reestimar parámetros, reentrenar características o volver a seleccionar modelo. La cadencia debe corresponder a la velocidad de cambio y al costo. Reentrenar cada hora puede ser innecesario; no reentrenar durante meses puede ignorar deriva.

Se monitorizan error, sesgo, cobertura, anchura, distribución de entradas, faltantes y desempeño frente al baseline. Un esquema de control compara métricas en ventana reciente con límites definidos en validación. La alarma inicia revisión; no ordena automáticamente un cambio.

Ante deriva se puede acortar ventana, ponderar observaciones recientes, añadir una intervención o cambiar especificación. Cada respuesta tiene riesgo: una ventana corta adapta rápido pero aumenta varianza; una larga estabiliza pero tarda. Se conserva una versión anterior y se evalúa el candidato en paralelo.

Los intervalos deben recalibrarse. Si un intervalo nominal del 90 % cubre 70 % en las últimas semanas, la incertidumbre comunicada es insuficiente aun si MAE no cambió. Para decisiones asimétricas se publican cuantiles: inventario puede basarse en un cuantil alto, mientras planificación central usa media.

### 14.4.8. Ejemplo práctico guiado: comparación de métodos de pronóstico

Una cadena minorista pronostica ventas diarias de una categoría a siete días. Se comparan: último valor, valor de hace siete días, media por día de semana, SARIMA y *gradient boosting* con rezagos y calendario. El periodo de entrenamiento inicial es un año; luego se ejecutan 20 orígenes semanales con ventana expansiva.

Todos los métodos reciben las mismas observaciones. La media estacional, escalado, transformación y características se recalculan por origen. Las promociones solo se incluyen si estaban aprobadas en la fecha de emisión. Se guardan $e_{t,h}$, intervalos o cuantiles y tiempo de ajuste.

Una tabla hipotética resume:

| Método | MAE | RMSE | MASE | Cobertura 90 % | Observación |
|---|---:|---:|---:|---:|---|
| Último valor | 18,4 | 26,7 | 1,21 | No aplica | Ignora semana |
| Estacional 7 días | 15,2 | 22,9 | 1,00 | No aplica | Baseline fuerte |
| Media estacional | 14,8 | 22,1 | 0,97 | No aplica | Suaviza extremos |
| SARIMA | 13,9 | 20,8 | 0,91 | 0,87 | Mejor en $h\le3$ |
| *Boosting* | 13,6 | 21,5 | 0,89 | 0,80 | Falla en promociones raras |

La menor MAE global de *boosting* no resuelve la elección. SARIMA tiene menor RMSE, mejor cobertura y costo inferior; *boosting* mejora días ordinarios pero subestima picos. A $h=7$, ambos empatan al baseline. Si la decisión penaliza faltantes de inventario, se comparan cuantiles y no solo medias.

**Conclusión defendible.** Se adopta SARIMA para tres días y baseline estacional para días 4 a 7, o se mantiene un único modelo si la simplicidad operativa pesa más. Se revisa cobertura mensualmente. No se afirma superioridad universal: el resultado corresponde a esa categoría, ventana y protocolo.

### Actividad EMO [MOV-04]: pronosticar demanda por zona y franja horaria

**Alineación obligatoria con el Apéndice D.** La fuente es NYC TLC Yellow Taxi Trip Records y la instantánea común contiene `yellow_tripdata_2026-02.parquet`, `yellow_tripdata_2026-03.parquet` y `yellow_tripdata_2026-04.parquet`. La unidad original es un viaje reportado; la unidad derivada es zona TLC-franja. La variable objetivo es la cantidad de pickups válidos por `PULocationID` e intervalo. Representa pickups de taxi amarillo reportados, no toda la movilidad, vehículos disponibles ni demanda insatisfecha.

**Pregunta realizable.** ¿Cuántos pickups se observarán en la siguiente hora, en las próximas horas o en el día siguiente para una zona o segmento? Con solo febrero-abril de 2026, el horizonte debe ser corto y no se puede exigir estacionalidad anual.

**Consigna.** Seleccionar una zona TLC o un segmento definido de manera reproducible. Construir una serie regular, fijar un horizonte operativo y comparar como mínimo un baseline de último valor o estacional con ARIMA, SARIMA u otra alternativa pertinente mediante validación *walk-forward*.

**Construcción de la serie.** Usar `tpep_pickup_datetime`, `PULocationID` y el Taxi Zone Lookup. Aplicar los mismos filtros, zona horaria y cortes en los tres meses. Los intervalos con cobertura confirmada y ningún viaje reciben cero explícito; los periodos sin cobertura quedan faltantes y se tratan sin usar futuro. Las zonas desconocidas se documentan. Variables conocidas al finalizar el viaje, como tipo de pago, cargos, propina u hora de descenso, no son predictores válidos de pickups futuros.

**Protocolo mínimo:**

```text
elegir zona, frecuencia y horizonte corto antes de evaluar
reservar una historia inicial suficiente para al menos varios ciclos semanales
definir múltiples orígenes entre febrero y abril de 2026
para cada origen:
    usar exclusivamente registros publicados y agregados hasta ese instante
    ajustar tratamientos y modelos dentro de la ventana
    emitir baseline y modelo alternativo para idénticos horizontes
    guardar punto, intervalo, observado y banderas de cobertura
calcular MAE o RMSE y una métrica escalada por horizonte
auditar sesgo, cobertura de intervalos y residuos o errores temporales
traducir el resultado a una regla prudente de prioridad de zona
```

**Baseline.** Para serie horaria, comparar al menos con la misma hora del día anterior o de la semana anterior, según evidencia; también puede incluirse último valor. Si se modela demanda diaria, usar día anterior o mismo día de semana. El baseline debe calcularse con pasado y permanecer idéntico entre candidatos.

**Validación temporal.** La ventana expansiva aprovecha los tres meses; una deslizante puede adaptarse a cambios entre meses. Justificar el primer origen, número de repeticiones, cadencia de emisión y si los horizontes se solapan. Ningún escalado, imputación, perfil horario, selección de orden o entrenamiento puede consultar fechas posteriores al origen.

**Producto individual.** Entregar notebook reproducible con especificación de datos, controles de cobertura, particiones temporales, pronósticos e intervalos, métricas por horizonte, análisis de residuos o errores y comparación con baseline. Incluir una tabla con origen, objetivo, horizonte, observado y predicciones para permitir auditoría.

**Interpretación operativa.** Una regla didáctica puede priorizar una zona si su pronóstico supera el baseline, ponderando conectividad definida en el laboratorio. No debe presentarse como despacho óptimo: TLC no informa la ubicación de vehículos libres ni toda la demanda de transporte. Una caída puede reflejar demanda, cobertura o cambio del servicio.

**Criterios de aprobación:**

- serie zona-franja regular con ceros y faltantes correctamente diferenciados;
- horizonte corto compatible con febrero-abril de 2026;
- baseline adecuado y evaluación sobre los mismos orígenes;
- ausencia demostrable de fuga temporal;
- MAE o RMSE por horizonte, más sesgo o métrica escalada;
- intervalos interpretados mediante cobertura y anchura;
- limitaciones de representatividad y decisión explícitas.

**Fallos que invalidan la evidencia.** Mezclar filas aleatoriamente; usar abril para aprender transformaciones evaluadas en febrero o marzo; rellenar toda ausencia con cero; utilizar atributos de fin de viaje; comparar modelos en cortes diferentes; informar solo ajuste dentro de muestra; afirmar estacionalidad anual; o confundir pickups reportados con demanda total.

## Glosario

**ACF:** función de autocorrelación; asociación lineal de una serie con sus rezagos.

**AR:** modelo autorregresivo que combina valores pasados de la respuesta.

**ARIMA:** modelo ARMA aplicado tras diferenciación regular.

**Baseline:** regla simple y reproducible que fija el nivel mínimo de comparación.

**Ciclo:** fluctuación de duración no estrictamente fija y no anclada al calendario.

**Cobertura:** proporción de valores futuros contenidos en sus intervalos predictivos.

**Diferenciación:** operación que resta observaciones separadas por uno o varios rezagos.

**Estacionariedad débil:** constancia de media y varianza, con covarianza dependiente solo del rezago.

**Estacionalidad:** patrón recurrente asociado a una posición conocida del calendario.

**Frecuencia:** ritmo de observación; en patrones, cantidad de ciclos por unidad temporal.

**Horizonte:** distancia entre el origen del pronóstico y el instante objetivo.

**Innovación:** componente nuevo no predecible con la información pasada del modelo.

**MA:** modelo que combina innovaciones actuales y pasadas.

**MAE:** promedio de errores absolutos, en la unidad de la variable.

**MASE:** error absoluto escalado por el desempeño ingenuo de entrenamiento.

**PACF:** autocorrelación parcial después de controlar rezagos intermedios.

**Periodo:** número de observaciones requerido para completar una repetición.

**Residuo:** diferencia entre valor observado y ajustado o pronosticado.

**RMSE:** raíz del promedio de errores cuadrados, sensible a errores grandes.

**SARIMA:** ARIMA con operadores autorregresivos, de diferencia y de media móvil estacionales.

**Serie regular:** serie cuyos intervalos consecutivos siguen una cuadrícula fija.

**Tendencia:** cambio suave del nivel a largo plazo respecto de la ventana analizada.

**Walk-forward:** evaluación que avanza orígenes y entrena siempre con el pasado disponible.

## Preguntas de revisión y discusión

1. ¿Por qué un cero observado y un intervalo sin cobertura producen consecuencias distintas al modelar demanda?
2. Distinga frecuencia de muestreo, frecuencia de un patrón y periodo con una serie horaria.
3. ¿Qué evidencia separaría estacionalidad semanal de un ciclo irregular de pedidos?
4. ¿Por qué una media móvil centrada puede describir el pasado, pero causar fuga al predecir?
5. Explique la diferencia entre estacionariedad estricta y débil.
6. ¿Cómo puede una tendencia crear autocorrelación alta sin dinámica de corto plazo?
7. ¿Qué patrones ideales muestran ACF y PACF en AR($p$) y MA($q$), y por qué no deben aplicarse mecánicamente?
8. Derive la media y la varianza de un AR(1) estacionario.
9. ¿Qué significa que un MA sea invertible?
10. Compare diferencia regular y estacional. ¿Qué síntomas produce sobrediferenciar?
11. ¿Por qué invertir un pronóstico logarítmico puede estimar una mediana y no una media?
12. Interprete cada orden de SARIMA$(p,d,q)(P,D,Q)_m$.
13. ¿Cuándo una variable exógena histórica no es válida para pronosticar?
14. ¿Qué demuestra y qué no demuestra una prueba de Ljung-Box no significativa?
15. Compare estrategias recursiva y directa para varios pasos.
16. ¿Por qué MAPE es problemático en series de conteos con ceros?
17. Diseñe una validación *walk-forward* para pronósticos horarios a seis pasos.
18. Enumere cuatro fugas temporales que pueden ocurrir antes de ajustar el modelo.
19. ¿En qué condiciones un método de ML puede superar a ARIMA y qué costo adicional introduce?
20. En MOV-04, ¿por qué tres meses no permiten exigir estacionalidad anual y qué baselines sí son defendibles?

## Actividad integradora de razonamiento

Un centro de distribución observa despachos horarios durante doce semanas y debe dimensionar personal para las próximas ocho horas. Hay turnos conocidos, faltantes por una interrupción de captura, ceros durante cierres y dos picos por campañas. Sin implementar código, redacte un protocolo técnico que incluya:

1. definición de unidad, frecuencia, origen y horizonte;
2. auditoría que distinga ceros, faltantes y atípicos reales;
3. hipótesis de tendencia, estacionalidad diaria/semanal y ciclos;
4. transformación y diferenciación candidatas con riesgos;
5. dos modelos ARIMA/SARIMA parsimoniosos y un baseline;
6. variables exógenas disponibles en cada origen;
7. diseño *walk-forward* con ventana y cadencia justificadas;
8. MAE, RMSE, MASE, sesgo y evaluación de intervalos por horizonte;
9. controles concretos contra fuga;
10. regla de actualización y condición para retirar el modelo.

La entrega debe incluir un diagrama temporal, las fórmulas de los candidatos, pseudocódigo del protocolo y una discusión de al menos tres modos de falla. Se evaluará la coherencia entre decisión, información y validación, no la complejidad del método.

## Síntesis

Una serie temporal está definida tanto por sus valores como por frecuencia, calendario, cobertura y disponibilidad. Tendencia, estacionalidad, ciclos y ruido son hipótesis útiles, pero dependen de escala y método. Faltantes y atípicos exigen investigar el proceso de observación antes de transformar datos.

La dependencia serial hace posible pronosticar y obliga a respetar orden. Estacionariedad, ACF, PACF, transformaciones y diferencias permiten formular dinámicas relativamente estables. AR, MA, ARMA, ARIMA y SARIMA ofrecen una familia coherente cuya complejidad debe ser parsimoniosa, cuyos predictores futuros deben estar disponibles y cuyos residuos necesitan diagnóstico.

Un pronóstico solo es defendible para un horizonte y una decisión definidos. Puntos sin intervalos ocultan incertidumbre; métricas sin baseline ocultan dificultad; particiones aleatorias ocultan fuga. La validación *walk-forward*, las métricas por horizonte y el seguimiento de cobertura acercan la evaluación al uso real. En MOV-04, esta disciplina se concreta al pronosticar pickups reportados de NYC TLC entre febrero y abril de 2026 mediante horizonte corto, baseline explícito y validación temporal reproducible.
