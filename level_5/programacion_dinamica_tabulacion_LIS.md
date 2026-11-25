# Programación dinámica: tabulación y Longest Increasing Subsequence (LIS)

Apuntes de la ruta Python de O'Reilly. Basados en los apuntes y los tres ejemplos de la clase compartidos por el estudiante. Las aclaraciones, casos límite y alternativas son ampliaciones de estudio.

## 1. Ideas centrales de la clase

- La tabulación es una técnica de programación dinámica que almacena resultados de subproblemas para evitar cálculos redundantes.
- Una implementación recursiva ingenua puede invocar repetidamente `lis(hi)` para el mismo índice.
- Para aplicar tabulación, debemos resolver los subproblemas en un orden que garantice que sus dependencias ya estén calculadas.
- La solución se construye reutilizando esos resultados.

## 2. El problema LIS

LIS significa *Longest Increasing Subsequence*: subsecuencia estrictamente creciente más larga. Una subsecuencia conserva el orden original, pero sus elementos no necesitan ser consecutivos. No es lo mismo que ordenar la lista ni buscar un segmento contiguo.

```python
A = [3, 10, 2, 1, 20]
```

Una LIS es `[3, 10, 20]`, de longitud 3. Puede haber varias soluciones óptimas para otras entradas. La comparación `<` exige crecimiento estricto: los valores iguales no prolongan la subsecuencia.

## 3. Programación dinámica (DP)

Es una técnica para resolver problemas mediante subproblemas cuyos resultados se almacenan y reutilizan. Dos propiedades relevantes en LIS son los subproblemas superpuestos (se vuelven a necesitar los mismos resultados) y la subestructura óptima (una solución óptima puede construirse a partir de soluciones óptimas de subproblemas).

| Enfoque | Dirección | Implementación habitual | Almacenamiento |
|---|---|---|---|
| Memoización | Top-down | Recursiva | Caché |
| Tabulación | Bottom-up | Iterativa | Tabla |

La memoización calcula resultados cuando se solicitan; la tabulación los calcula siguiendo el orden de dependencias. No toda recursión es programación dinámica ni todo algoritmo iterativo es tabulación.

## 4. Ejemplo 1: recursión ingenua

Código de la clase (formato normalizado):

```python
A = [3, 10, 2, 1, 20]


def lis(hi):
    longest = 1
    for j in range(hi):
        if A[j] < A[hi]:
            longest = max(longest, 1 + lis(j))
    return longest


print(lis(len(A) - 1))  # 3
```

`hi` es un índice, no una longitud. `lis(hi)` calcula la longitud de la mejor subsecuencia que termina exactamente en `A[hi]`.

- `longest = 1`: cualquier elemento por sí solo forma una subsecuencia.
- `range(hi)`: recorre todos los índices anteriores a `hi`, sin incluirlo.
- `A[j] < A[hi]`: comprueba si podemos añadir el elemento actual a una subsecuencia que termina en `j`.
- `1 + lis(j)`: añade un elemento a la longitud de esa subsecuencia.
- `max(...)`: conserva la mejor alternativa encontrada.

El caso base es implícito: para `hi = 0`, el bucle no se ejecuta y devuelve 1.

### Por qué repite trabajo

Para la lista de ejemplo, el árbol de llamadas es:

```text
lis(4)  # 20
├── lis(0)  # 3
├── lis(1)  # 10
│   └── lis(0)  # 3, nuevamente
├── lis(2)  # 2
└── lis(3)  # 1
```

`lis(0)` se calcula dos veces. En una lista estrictamente creciente de 20 elementos, una llamada a `lis(19)` invoca `lis(10)` 256 veces: una por cada subconjunto de los ocho índices intermedios 11 a 18. En otras listas la cantidad depende de los valores. En el peor caso, la recursión tiene tiempo O(2^N) y profundidad O(N).

### Corrección conceptual importante

`lis(len(A) - 1)` solo calcula la mejor subsecuencia que termina en el último elemento. Coincide con la LIS global en el ejemplo, pero no siempre.

Para `[3, 10, 20, 1]`, devuelve 1, aunque la LIS global tiene longitud 3. Para obtener la longitud global con esta implementación (y con `A` global definida), podríamos usar `max((lis(i) for i in range(len(A))), default=0)`. Esto no elimina el trabajo redundante. El uso de `A` global también es una dependencia implícita del ejemplo.

## 5. Ejemplo 2: tabulación

```python
def lis_tabulation(A):
    N = len(A)
    LIS = [1] * N  # Length of LIS ending at A[i]
    for i in range(N):
        for j in range(i):
            if A[j] < A[i] and LIS[j] + 1 > LIS[i]:
                LIS[i] = LIS[j] + 1
    return max(LIS)


print(lis_tabulation(A))  # 3
```

### La definición del estado

`LIS[i]` es la longitud de la mejor subsecuencia creciente que termina en `A[i]`. Esta definición es fundamental. La tabla no almacena los elementos de las subsecuencias, sino sus longitudes.

`[1] * N` crea una lista de N unos. Cada elemento es inicialmente una subsecuencia de longitud 1. Como los enteros son inmutables, esta multiplicación no presenta el problema de referencias compartidas que sí puede aparecer con listas anidadas mutables.

### Los dos bucles

El bucle exterior selecciona el elemento final `i`. El interior examina todos los posibles predecesores `j < i`. Cuando se llega a `i`, todos los valores `LIS[j]` anteriores ya están calculados.

La condición tiene dos partes:

1. `A[j] < A[i]`: la extensión es válida.
2. `LIS[j] + 1 > LIS[i]`: la extensión mejora la mejor longitud conocida para `i`.

Si ambas se cumplen, guardamos la nueva longitud. `and` evalúa de izquierda a derecha y no evalúa la segunda condición si la primera es falsa.

### Seguimiento manual

| i | A[i] | Predecesores válidos | LIS después del paso |
|---|---|---|---|
| 0 | 3 | Ninguno | [1, 1, 1, 1, 1] |
| 1 | 10 | 3 | [1, 2, 1, 1, 1] |
| 2 | 2 | Ninguno | [1, 2, 1, 1, 1] |
| 3 | 1 | Ninguno | [1, 2, 1, 1, 1] |
| 4 | 20 | 3, 10, 2, 1 | [1, 2, 1, 1, 3] |

En el último paso, el candidato que termina en 10 ofrece longitud `LIS[1] + 1 = 3`. Los otros candidatos ofrecen 2 y no mejoran ese resultado.

`max(LIS)` devuelve la mejor longitud global, no necesariamente la última posición.

### La recurrencia

En términos matemáticos, para cada i:

`LIS[i] = 1 + max(LIS[j] para j < i y A[j] < A[i])`

Si no existe un predecesor válido, el resultado es 1 (el máximo del conjunto vacío se toma como 0 para esta fórmula). La recursión y la tabulación expresan la misma relación; cambia cómo se calculan y almacenan los resultados.

## 6. Ejemplo 3: reconstrucción de la subsecuencia

```python
def lis_tabulation_two(A):
    N = len(A)
    LIS = [1] * N
    prev = [-1] * N
    for i in range(N):
        for j in range(i):
            if A[j] < A[i] and LIS[j] + 1 > LIS[i]:
                LIS[i] = LIS[j] + 1
                prev[i] = j

    i = LIS.index(max(LIS))
    result = []
    while i != -1:
        result.append(A[i])
        i = prev[i]
    return list(reversed(result))


print(lis_tabulation_two(A))  # [3, 10, 20]
```

La diferencia es que ahora queremos recuperar los elementos, no solo la longitud. Para eso agregamos una segunda tabla: `prev`.

`prev[i]` guarda el índice del elemento inmediatamente anterior en la mejor subsecuencia encontrada que termina en `i`. `-1` indica que no hay predecesor; aquí es un valor centinela, no un índice que queramos consultar.

| Índice | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| A | 3 | 10 | 2 | 1 | 20 |
| LIS | 1 | 2 | 1 | 1 | 3 |
| prev | -1 | 0 | -1 | -1 | 1 |

Cuando mejora una longitud, `prev[i] = j` registra qué decisión permitió esa mejora.

### Reconstrucción paso a paso

`LIS.index(max(LIS))` obtiene el índice de la primera aparición de la longitud máxima. En este ejemplo es 4. Si hay empate, elige la primera; no enumera todas las LIS.

| i | A[i] | result después de append | Siguiente i |
|---|---|---|---|
| 4 | 20 | [20] | 1 |
| 1 | 10 | [20, 10] | 0 |
| 0 | 3 | [20, 10, 3] | -1 |

El recorrido sigue los índices `4 -> 1 -> 0 -> -1`. Como comienza en el último elemento de la subsecuencia, recupera los valores al revés. `reversed(result)` devuelve un iterador inverso; `list(...)` lo materializa como lista. No modifica `result`.

Resultado: `[3, 10, 20]`.

Importante: en Python `A[-1]` sería un acceso válido al último elemento. La condición `while i != -1` evita tratar el centinela como un índice real.

## 7. Complejidad temporal y espacial

Los bucles de tabulación realizan exactamente `0 + 1 + ... + (N-1) = N*(N-1)/2` iteraciones interiores. Esto da tiempo Θ(N²), suponiendo comparaciones y operaciones de coste constante. `max`, `index` y la reconstrucción añaden como máximo trabajo lineal, por lo que no cambian el orden cuadrático.

| Implementación | Tiempo (peor caso) | Espacio auxiliar |
|---|---|---|
| Recursiva ingenua | O(2^N) | O(N), pila de llamadas |
| Tabulación, longitud | Θ(N²) | O(N) |
| Tabulación, reconstrucción | Θ(N²) | O(N) |

La tercera implementación usa dos tablas y una lista de resultado, todas de tamaño a lo sumo N. Existe un algoritmo LIS de O(N log N), pero no forma parte de los ejemplos de esta clase.

### Preguntas del quiz

Para crecimiento cuadrático, al multiplicar N por k, el tiempo dominante cambia aproximadamente por k²:

| Cambio de N | Tiempo esperado |
|---|---|
| Mitad | 1/4 |
| Doble | 4 veces |
| Triple | 9 veces |

Son aproximaciones asintóticas, no garantías de tiempos reales exactos. La otra pregunta identifica correctamente tabulación como *dynamic programming*, de orden *bottom-up*, frente a la recursión ingenua de coste *exponential*.

## 8. Casos límite y pruebas

Las implementaciones de tabulación del profesor fallan con una lista vacía porque `max([])` lanza `ValueError`. Una mejora sería devolver 0 al inicio de la función de longitud y `[]` al inicio de la función de reconstrucción cuando `not A`. Se mantienen arriba los ejemplos originales para distinguirlos de estas mejoras.

| Entrada | Longitud esperada | Una subsecuencia válida |
|---|---|---|
| [3, 10, 2, 1, 20] | 3 | [3, 10, 20] |
| [3, 10, 20, 1] | 3 | [3, 10, 20] |
| [5, 4, 3] | 1 | [5] |
| [2, 2, 2] | 1 | [2] |
| [7] | 1 | [7] |
| [] | 0 | [] (requiere mejora) |

## 9. Qué recordar

- Definir primero qué representa cada estado de la tabla.
- Identificar cómo se relaciona un estado con los anteriores.
- Inicializar los casos base.
- Resolver en orden de dependencias y reutilizar resultados.
- Si necesitamos reconstruir una solución, almacenar también las decisiones que llevaron a ella.

La programación dinámica no consiste simplemente en usar una lista o dos bucles. Lo fundamental es la reutilización de soluciones de subproblemas.

## 10. Referencias para consultar

Documentación oficial de Python (enlaces de referencia, no consultados en línea durante esta revisión):

- [Funciones incorporadas: max, range, reversed](https://docs.python.org/3/library/functions.html)
- [Tipos de secuencia y métodos de listas](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range)
- [functools.cache: herramienta para memoización](https://docs.python.org/3/library/functools.html#functools.cache)
