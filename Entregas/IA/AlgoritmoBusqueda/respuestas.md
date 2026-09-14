# Respuestas de análisis — TP Búsqueda Voraz y A*

## 1. ¿Por qué Voraz y A* coinciden en este grafo particular?

Voraz y A* encontraron el mismo camino porque, en este grafo, la heurística ayudó a elegir correctamente los nodos. Desde A, Voraz eligió C porque tenía el menor valor de `h` (`h(C)=3`). A* también eligió C porque al combinar el costo recorrido con la heurística obtuvo un valor favorable: `f(C)=g(C)+h(C)=4+3=7`. Como C realmente conducía al camino más barato, ambos algoritmos terminaron encontrando `S → A → C → G`, con costo 7.

Esto ocurre en este grafo particular y no significa que Voraz y A* siempre encuentren el mismo camino.

## 2. ¿Voraz garantiza la solución óptima en general?

No. Voraz solamente tiene en cuenta la heurística `h(n)`, es decir, qué tan cerca parece estar un nodo del objetivo. No tiene en cuenta cuánto costó llegar hasta ese nodo.

Por ejemplo, podría elegir un nodo que parece muy cercano al objetivo, pero al que se llegó mediante un camino muy costoso. Por eso Voraz puede encontrar una solución rápidamente, pero no garantiza que sea la solución más barata.

En este ejercicio encontró el camino óptimo de costo 7, pero esto no está garantizado en general.

## 3. ¿Qué pasa con A* si h(n) = 0 para todos los nodos?

A* utiliza la función:

`f(n) = g(n) + h(n)`

Si `h(n)=0` para todos los nodos, entonces:

`f(n) = g(n)`

Por lo tanto, A* pasa a utilizar solamente el costo acumulado desde el inicio, exactamente igual que UCS. Por eso se dice que UCS es un caso particular de A* cuando la heurística es cero.

## 4. ¿Hubo reaperturas? ¿Por qué?

Sí. En UCS hubo una reapertura del nodo D.

Primero se encontró D mediante `S → A → D`, con un costo de 7. Después se encontró otra forma de llegar a D mediante `S → B → D`, con un costo de 4.

Como 4 es menor que 7, se actualizó el costo de D y se volvió a considerar ese nodo. Por eso se registró una reapertura.

En Voraz y A* no hubo reaperturas en esta ejecución.

## 5. ¿"Expandir menos nodos" es lo mismo que "encontrar la solución más barata"?

No. Son dos conceptos diferentes.

Expandir menos nodos significa que el algoritmo realizó menos trabajo durante la búsqueda. Encontrar la solución más barata significa que encontró el camino de menor costo.

En este ejercicio, UCS expandió 6 nodos, mientras que Voraz y A* expandieron 4. Sin embargo, los tres encontraron el mismo camino `S → A → C → G`, con costo 7.

Por lo tanto, en este caso Voraz y A* fueron más eficientes que UCS, pero esto no significa que expandir menos nodos garantice encontrar una solución más barata. Voraz, por ejemplo, puede expandir pocos nodos y aun así encontrar una solución que no sea óptima.