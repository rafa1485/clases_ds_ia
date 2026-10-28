# TP2: Búsqueda voraz y A* sobre un grafo dirigido

**Materia:** Inteligencia Artificial  
**Alumno:** Lucas Manuel

## Análisis de resultados

### 1. ¿Por qué la búsqueda voraz y A* encuentran el mismo camino?

En este grafo, ambos algoritmos encuentran el camino `S → A → C → G`, con un costo total de 7. La búsqueda voraz prioriza los estados con menor valor heurístico `h(n)`, mientras que A* considera tanto el costo acumulado como la estimación del costo restante mediante `f(n) = g(n) + h(n)`.

En este caso, ambas estrategias priorizan la ruta que llega a `G` con costo 7 antes de explorar las alternativas. Esto ocurre por la estructura particular del grafo y los valores de la heurística; no significa que ambos algoritmos siempre encuentren el mismo camino.

### 2. ¿La búsqueda voraz garantiza encontrar el camino de menor costo?

No. La búsqueda voraz prioriza el valor heurístico `h(n)` y no tiene en cuenta el costo acumulado `g(n)` al ordenar la frontera. Por eso, puede elegir un camino que parezca acercarse rápidamente a la meta, pero que termine teniendo un costo total mayor que otra alternativa.

### 3. ¿Qué ocurre si la heurística de A* vale cero para todos los estados?

Si `h(n) = 0` para todos los estados, entonces `f(n) = g(n) + h(n) = g(n)`. En consecuencia, A* prioriza únicamente el costo acumulado y se comporta como la búsqueda de costo uniforme (UCS), suponiendo el mismo criterio de desempate y el mismo manejo de entradas obsoletas.

### 4. ¿Hubo reaperturas o mejoras de costo en los algoritmos? ¿Por qué?

Con la definición de la consigna —contar las veces que mejora `mejor_g` para un estado que ya era conocido—, UCS registra una mejora: el costo conocido de `D` pasa de 7 a 4 cuando se encuentra un camino mejor a través de `B`.

La búsqueda voraz y A* no registran mejoras de costo para estados ya conocidos en esta ejecución. Técnicamente, la mejora de `D` en UCS sucede antes de expandir su entrada antigua; por eso, es más preciso describirla como una mejora de `mejor_g` que como una reapertura de un estado que ya había sido expandido.

### 5. ¿Expandir menos estados significa encontrar un camino más barato?

No necesariamente. En este ejemplo, los tres algoritmos encuentran un camino de costo 7, pero la búsqueda voraz y A* expanden 3 estados antes de extraer la meta, mientras que UCS expande 5.

Expandir menos estados no garantiza un camino más barato. La búsqueda voraz puede encontrar una ruta más costosa porque ignora el costo acumulado al establecer prioridades. UCS garantiza encontrar un camino de costo mínimo si los costos de las aristas son no negativos. A* también puede garantizar optimalidad cuando se cumplen las condiciones apropiadas para la heurística y la implementación; en este ejercicio, la heurística es consistente.

## Resumen de resultados

| Métrica | UCS | Búsqueda voraz | A* |
|---|---:|---:|---:|
| Camino encontrado | `S → A → C → G` | `S → A → C → G` | `S → A → C → G` |
| Costo total | 7 | 7 | 7 |
| Estados expandidos antes de extraer `G` | 5 | 3 | 3 |
| Nodos generados | 7 | 6 | 6 |
| Frontera máxima | 3 | 3 | 3 |
| Mejoras de `mejor_g` para estados conocidos | 1 | 0 | 0 |

## Conclusión

En este grafo, los tres algoritmos encuentran una solución de costo 7. UCS explora más estados porque ordena la frontera según el costo acumulado. La búsqueda voraz explora menos estados en este ejemplo, pero no garantiza optimalidad en general. A* combina el costo acumulado y la heurística, y con una heurística adecuada puede encontrar una solución óptima mientras reduce la exploración respecto de UCS.
