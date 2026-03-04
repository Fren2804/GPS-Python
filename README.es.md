# 🔍 Comparación de Algoritmos de Búsqueda de Caminos en Python

> 🇪🇸 Español | [🇬🇧 English Version](README.md)

## 📌 Descripción

Este proyecto implementa y compara dos algoritmos clásicos de búsqueda de caminos: Dijkstra y A*.

El objetivo es entender su implementación y analizar su comportamiento, eficiencia y resultados al encontrar el camino más corto entre dos nodos dentro de un grafo o mapa.

## 🧪 Introducción

Este proyecto utiliza la librería **pygame** para gestionar el entorno gráfico y la visualización.

Se genera un mapa de **ROWS x COLS**, donde cada celda tiene un tamaño definido por **CELL**.  
Después se seleccionan aleatoriamente las posiciones **start** y **goal**.

A continuación, se generan paredes (`walls`) de forma aleatoria con una probabilidad del **30%**. Luego, mediante la función `has_path`, se comprueba que existe al menos un camino válido entre **start** y **goal**.

Y, finalmente, se incluyen funciones como `set_speed_9` y `set_speed_99`, que asignan de forma aleatoria la velocidad o coste de cada casilla.

```
1 Rápido - 2 - 3 - 4 - 5 - ... - 99 Lento
```

## 🔦 Dijkstra

Este algoritmo analiza cada casilla teniendo en cuenta el coste o velocidad asociada a ella, explorando siempre el camino con el menor coste acumulado hasta ese momento.

A diferencia de otros algoritmos de búsqueda, **Dijkstra no utiliza ningún tipo de heurística** para aproximarse al objetivo. En su lugar, explora el mapa expandiendo gradualmente los nodos con menor coste total desde la posición inicial.

Gracias a este enfoque, el algoritmo garantiza encontrar **el camino más corto posible** entre `start` y `goal`. Sin embargo, al no tener información sobre la dirección del objetivo, puede llegar a explorar una gran cantidad de nodos antes de encontrar la solución.

### Ejemplo

```
 S(0)  A(1)  B(6)
 C(2)  D(4)  E(1)
 F(1)  H(8)  G(2)
```

#### Paso 1

Comienza en S con coste acumulado 0. S(0)

```
[S(0)]  A(1)  B(6)
 C(2)   D(4)  E(1)
 F(1)   H(8)  G(2)
```

#### Paso 2

Analiza el nodo `S` con coste acumulado **W(S) = 0**.

Calcula el coste de sus vecinos:

- W(S -> A) = S(0) + coste(A) -> 0 + 1 = **1**
- W(S -> C) = S(0) + coste(C) -> 0 + 2 = **2**

Elige **W(S -> A) -> W(SA) = 1**

```
 S(0)  [A(1)]  B(6)
[C(2)]  D(4)   E(1)
 F(1)   H(8)   G(2)
```

#### Paso 3

Nodos anteriores:

- W(S -> C) -> W(SC) = **2**

Analiza el nodo `A` con coste acumulado **W(SA) = 1**.

Calcula el coste de sus vecinos:

- W(SA -> B) = W(SA) + coste(B) -> 1 + 6 = **7**
- W(SA -> D) = W(SA) + coste(D) -> 1 + 4 = **5**

Elige **W(S -> C) -> W(SC) = 2**

Siempre elige el nodo con menor coste, siempre que el **nodo no haya sido visitado**

```
 S(0)  A(1)  [B(6)]
 C(2) [D(4)]  E(1)
 F(1)  H(8)   G(2)
```

#### Paso 4

Nodos anteriores, orden ascendente:

- W(SA -> D) -> W(AD) = **5**
- W(SA -> B) -> W(AB) = **7**

Analiza el nodo `C` con coste acumulado **W(SC) = 2**.

Calcula el coste de sus vecinos:

- W(SC -> D) = W(SC) + coste(D) = 2 + 4 = **6**
- W(SC -> F) = W(SF) + coste(F) = 2 + 1 = **3**

Elige **W(SC -> F) -> W(CF) = 3**

```
 S(0)   A(1)  B(6)
 C(2)  [D(4)] E(1)
[F(1)]  H(8)  G(2)
```

#### Paso 5

Nodos anteriores, orden ascendente:

- W(SA -> D) -> W(AD) = **5**
- W(SC -> F) -> W(CF) = **6**
- W(SA -> B) -> W(AB) = **7**

Analiza el nodo `F` con coste acumulado **W(CF) = 3**.

Calcula el coste de sus vecinos:

- W(CF -> H) = W(CF) + coste(H) = 3 + 8 = **11**

Elige **W(SA -> D) -> W(AD) = 5**

```
 S(0)  A(1)  B(6)
 C(2)  D(4)  E(1)
 F(1) [H(8)] G(2)
```

#### Paso 6

Nodos anteriores, orden ascendente:

- W(SC -> F) -> W(CF) = **6**
- W(SA -> B) -> W(AB) = **7**
- W(CF -> H) -> W(FH) = **11**

Analiza el nodo `D` con coste acumulado W(AD) = **5**

Calcula el coste de sus vecinos:

- W(AD -> E) = W(AD) + coste(E) = 5 + 1 = **6**
- W(AD -> H) = W(AD) + coste(H) = 5 + 8 = **13**

Elige **W(AD -> E) -> W(DE) = 6**

```
 S(0)  A(1)  B(6)
 C(2)  D(4) [E(1)]
 F(1) [H(8)] G(2)
```

#### Paso 7

Está en el nodo `E` donde ya llega al nodo final `G`. Tiene un coste de:

- W(DE -> G) = W(DE) + coste(G) = 6 + 2 = **8**.

```
 S(0)  A(1)  B(6)
 C(2)  D(4)  E(1)
 F(1)  H(8) [G(2)]
```

El camino ha sido **W(EG) -> W(DE) -> W(AD) -> W(SA)**

### Mapa calor Dijkstra

![Mapa calor Dijkstra](Dijkstra.png)

## ⭐ A* (A-star)

El algoritmo **A\*** es una mejora del algoritmo de Dijkstra que utiliza una **heurística** para estimar la distancia restante hasta el objetivo.

En cada paso, el algoritmo evalúa las casillas teniendo en cuenta dos factores:  
- el **coste acumulado** desde `start` hasta la posición actual  
- una **estimación de la distancia** desde esa posición hasta `goal`

La suma de ambos valores permite priorizar las casillas que parecen acercarse más rápidamente al objetivo. Gracias a esta estrategia, **A\*** suele explorar muchos menos nodos que Dijkstra.

Si la heurística utilizada es **admisible** (es decir, no sobreestima la distancia real al objetivo), el algoritmo garantiza encontrar **el camino óptimo** entre `start` y `goal`.

### Mapa calor A*

Es simbólico, ya que según la heurística elegida pueden variar los mapas de calor.

![Mapa calor A-star](A-star.png)

## ⚖️ Comparación

| Algoritmo | Heurística | Nodos explorados | Garantiza camino óptimo |
|-----------|-----------|-----------------|------------------------|
| Dijkstra  | ❌ No     | Alto            | ✅ Sí                  |
| A*        | ✅ Sí     | Bajo            | ✅ Sí (heurística admisible) |

