# Programación dinámica: de la recursión ingenua a la tabulación

*Apuntes del salto de O'Reilly a Tabulation / Dynamic Programming (sin consigna de ejercicio), a partir del ejemplo de la Longest Increasing Subsequence (LIS). Revisados y ampliados, con el código probado.*

## El problema: Longest Increasing Subsequence (LIS)

Dada una lista, encontrar la subsecuencia más larga de elementos que aparecen en el mismo orden y van aumentando (no hace falta que sean consecutivos en la lista original).

```python
A = [3, 10, 2, 1, 20]
```

Acá la LIS es `[3, 10, 20]`, de longitud 3. (`[3, 10]` y `[2, 20]` también son crecientes, pero más cortas.)

## 1. La versión recursiva ingenua

```python
def lis(hi):
    longest = 1
    for j in range(hi):
        if A[j] < A[hi]:
            longest = max(longest, 1 + lis(j))
    return longest

print(lis(len(A) - 1))   # 3
```

**Qué calcula `lis(hi)`:** la longitud de la LIS que **termina justo en** `A[hi]`. No es "la LIS de toda la lista hasta `hi`": es, específicamente, la que usa `A[hi]` como último elemento.

**Por qué funciona:** para cada `j` anterior a `hi` con `A[j] < A[hi]`, `A[hi]` podría extender la subsecuencia que termina en `A[j]`. Probamos todas esas opciones y nos quedamos con la mejor (`max`). El caso base es `longest = 1`: cualquier elemento solo ya es una subsecuencia creciente de largo 1.

**El problema (lo que dice tu comentario):** `lis(hi)` vuelve a llamar a `lis(j)` para cada `j < hi` que cumpla la condición, y esos a su vez vuelven a llamar a sus propios `j` anteriores. El mismo subproblema (ej. `lis(2)`) se recalcula una y otra vez desde distintas ramas.

Lo medí ejecutando el código con una lista estrictamente creciente de tamaño 20 (el peor caso, porque ahí *todos* los `A[j] < A[hi]` son verdaderos y se disparan todas las llamadas posibles): **524.288 llamadas** a la función. Con tamaño 10: **512 llamadas**. La relación es `2^(N-1)`, es decir, **crecimiento exponencial**. Para una lista de 20 elementos, sin ningún cálculo complicado involucrado, el recursivo ingenuo hace medio millón de llamadas.

## 2. Qué es la tabulación

Del comentario de tu apunte, con una corrección menor: la tabulación es la técnica de **guardar el resultado de cada subproblema en una tabla** (acá, una lista) para no recalcularlo. Hay dos ingredientes:

1. **Resolver los subproblemas más chicos primero**, en orden, y guardarlos.
2. **Construir cada solución nueva a partir de las ya guardadas**, nunca con una llamada recursiva.

Esto es la contraparte de la *memoización* (memoization): ambas evitan recálculos, pero la memoización sigue siendo recursiva y agrega una caché por arriba (ej. con [`functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache)); la tabulación directamente reemplaza la recursión por un bucle que avanza "de abajo hacia arriba" (*bottom-up*).

## 3. La versión tabulada

```python
def lis_tabulation(A):
    N = len(A)
    LIS = [1] * N          # LIS[i] = longitud de la LIS que termina en A[i]
    for i in range(N):             # subproblemas de menor a mayor índice
        for j in range(i):         # todos los subproblemas ya resueltos antes que i
            if A[j] < A[i] and LIS[j] + 1 > LIS[i]:
                LIS[i] = LIS[j] + 1
    return max(LIS)

print(lis_tabulation(A))   # 3
```

Lo corrí: da `3`, igual que la versión recursiva. La corrección de tu comentario (*"problemas"*, no *"problemas"* con la "a" de más) no afecta la lógica, es solo una errata de tipeo (`problemas` → estaba bien escrito "problemas", el error tipográfico real está en el comentario `# Solve problemas smallest...`, sobra la "as": sería "Solve problems").

**La diferencia clave con la versión recursiva:**

| | Recursiva | Tabulada |
|---|---|---|
| Orden de cálculo | Empieza por el final (`hi` más alto) y baja | Empieza por el principio (`i = 0`) y sube |
| Qué guarda | Nada; recalcula | `LIS[i]` para cada `i`, una sola vez |
| Costo | `O(2^N)` en el peor caso | `O(N²)`: dos bucles anidados de tamaño `N` |

`LIS[i] + 1 > LIS[i]` en el `if`: la condición compara el candidato nuevo (`LIS[j] + 1`, es decir "extiendo la subsecuencia que termina en `j`") contra el mejor valor que `LIS[i]` ya tiene guardado. Si el candidato es mejor, se actualiza. Es exactamente el mismo `max` de la versión recursiva, pero hecho con una comparación sobre valores ya calculados en vez de con una llamada nueva.

Al final, `max(LIS)` recorre la tabla y se queda con la mayor longitud encontrada, sin importar en qué índice haya terminado.

## 4. Reconstruir la secuencia, no solo su longitud

El primer `lis_tabulation` devuelve `3`, pero no dice **cuál** es la subsecuencia. Tu segundo ejemplo (`lis_tabulation_two`) agrega eso con un arreglo auxiliar:

```python
def lis_tabulation_two(A):
    N = len(A)
    LIS = [1] * N
    prev = [-1] * N         # prev[i] = índice del elemento anterior en la LIS que termina en A[i]
    for i in range(N):
        for j in range(i):
            if A[j] < A[i] and LIS[j] + 1 > LIS[i]:
                LIS[i] = LIS[j] + 1
                prev[i] = j   # me acuerdo de quién fue el anterior

    i = LIS.index(max(LIS))   # arranco desde el índice con la LIS más larga
    result = []
    while i != -1:
        result.append(A[i])
        i = prev[i]            # voy retrocediendo por los "anteriores"
    return list(reversed(result))
```

Lo corrí: con `A = [3, 10, 2, 1, 20]` devuelve `[3, 10, 20]`.

**La idea de `prev`:** cada vez que mejoro `LIS[i]` porque encontré un `j` que la extiende, anoto `prev[i] = j`. Al final, `LIS.index(max(LIS))` encuentra el índice donde termina la subsecuencia más larga (si hay empate, [`list.index`](https://docs.python.org/3/library/stdtypes.html#list.index) devuelve el primero), y el `while` camina hacia atrás por esos "anteriores" hasta llegar a un `-1` (que marca "no tengo anterior, soy el inicio de la subsecuencia"). Como se arma de atrás para adelante, hay que invertir la lista al final con [`reversed()`](https://docs.python.org/3/library/functions.html#reversed).

**Por qué `prev[i] = -1` como valor inicial:** `-1` nunca puede ser un índice válido de la lista, así que sirve como centinela para "este elemento no tiene predecesor en su LIS" sin confundirse con un índice real. Es el mismo truco que usar `None`, pero permite usar `prev[i]` directamente como índice en el `while` sin chequear primero.

## 5. ¿Por qué aparece justo acá, después de recursión?

El salto tiene sentido si se mira como una progresión:

1. **Recursión ingenua:** expresa el problema de forma natural ("la respuesta depende de respuestas más chicas"), pero recalcula subproblemas superpuestos → exponencial.
2. **Memoización:** la misma recursión, pero con una caché que evita recalcular (ej. un diccionario o `@lru_cache`) → el mismo orden "de arriba hacia abajo", con el costo de la versión tabulada.
3. **Tabulación:** se da vuelta el orden: se resuelve explícitamente de los subproblemas más chicos a los más grandes, en un bucle, sin pila de recursión → mismo resultado, sin riesgo de `RecursionError` en listas grandes, y generalmente más eficiente en memoria porque no acumula *frames* de llamada.

La condición para que la tabulación funcione (como dice tu apunte, y es correcto) es que el problema se pueda ordenar de manera que, al llegar a resolver el subproblema `i`, **todos los subproblemas de los que depende ya estén resueltos**. Acá se cumple porque `LIS[i]` solo depende de `LIS[j]` con `j < i`, y el bucle externo va de menor a mayor.

## Para practicar tranquilo

- Probar `lis_tabulation_two` con una lista que tenga dos subsecuencias crecientes de la misma longitud máxima (ej. `[1, 2, 3, 0, 5, 6]`) y ver cuál devuelve `LIS.index(max(LIS))` cuando hay empate.
- Adaptar el patrón (tabla + `prev`) a otro problema clásico de DP, como la subsecuencia común más larga (*Longest Common Subsequence*) entre dos listas, para confirmar que el mismo esquema ("tabla ordenada + reconstrucción con `prev`") se repite.
- Medir con `timeit` cuánto tarda la versión recursiva contra la tabulada para listas crecientes de tamaño 15, 20 y 25, y confirmar a ojo el crecimiento `O(2^N)` contra `O(N²)`.

## Referencias

- [`functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache) — memoización lista para usar sobre una función recursiva.
- [`sys.setrecursionlimit`](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit) — por qué la recursión ingenua puede romper con listas grandes.
- [`list.index`](https://docs.python.org/3/library/stdtypes.html#list.index) y [`reversed()`](https://docs.python.org/3/library/functions.html#reversed) — usadas en la reconstrucción de la secuencia.
