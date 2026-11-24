# Concurrencia y paralelismo en Python

## 1. Conceptos fundamentales

-   **Concurrencia:** varias tareas progresan durante un mismo período, aunque no necesariamente se ejecuten simultáneamente.
-   **Paralelismo:** varias tareas se ejecutan simultáneamente, por ejemplo, en distintos núcleos de la CPU.
-   **Hilo (thread):** unidad de ejecución dentro de un proceso. Los hilos de un proceso comparten memoria.
-   **Proceso (process):** instancia de un programa en ejecución, con su propio espacio de memoria.

## 2. CPU-bound vs. I/O-bound

  ------------------------------------------------------------------------------------------------
  Tipo de tarea           Limitación principal         Ejemplos
  ----------------------- ---------------------------- -------------------------------------------
  CPU-bound               Capacidad de procesamiento   Cálculos intensivos

  I/O-bound               Espera de entrada/salida     Peticiones HTTP, archivos, bases de datos
  ------------------------------------------------------------------------------------------------

## 3. GIL (Global Interpreter Lock)

En CPython con el GIL habilitado, solamente un hilo por intérprete puede ejecutar bytecode de Python en un momento dado.

Durante muchas operaciones bloqueantes de I/O, el GIL se libera, permitiendo que otro hilo ejecute código Python mientras el primero espera.

Por eso:

-   En tareas CPU-bound escritas en Python puro, el GIL limita el paralelismo entre hilos.
-   En tareas I/O-bound, los hilos pueden superponer sus tiempos de espera (*overlap*).

**El GIL limita el paralelismo del bytecode, no impide la concurrencia.**

## 4. Herramientas de concurrencia

  ------------------------------------------------------------------------------------------------------
  Herramienta             Característica principal                               Uso habitual
  ----------------------- ------------------------------------------------------ -----------------------
  `asyncio`               Multitarea cooperativa                                 I/O asíncrono

  `threading`             Multitarea apropiativa (*preemptive*)                  I/O bloqueante

  `multiprocessing`       Procesos independientes y paralelismo real             CPU-bound

  `ThreadPoolExecutor`    Administración automática de un conjunto de hilos      I/O bloqueante

  `ProcessPoolExecutor`   Administración automática de un conjunto de procesos   CPU-bound
  ------------------------------------------------------------------------------------------------------

### asyncio

Las tareas cooperan entre sí mediante un event loop. Una corrutina puede ceder el control mediante `await` cuando debe esperar una operación asíncrona. No todo `await` implica necesariamente una suspensión.

### threading

El sistema operativo planifica los hilos. A diferencia de la multitarea cooperativa, un hilo no necesita ceder voluntariamente el control para que el sistema operativo planifique otro. En CPython convencional, también interviene el GIL.

### multiprocessing

Utiliza procesos independientes. Cada proceso tiene su propio espacio de memoria y, en CPython convencional, su propio GIL. Esto permite aprovechar múltiples núcleos para ejecutar código Python en paralelo.

### concurrent.futures.ThreadPoolExecutor

Es una abstracción de alto nivel sobre los hilos. Crea, administra y reutiliza un conjunto de hilos (*thread pool*). No es un modelo de concurrencia distinto de `threading`.

``` python
from concurrent.futures import ThreadPoolExecutor


def square(n):
    return n**2


with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(square, [1, 2, 3, 4, 5, 6]))

print(results)  # [1, 4, 9, 16, 25, 36]
```

El ejemplo ilustra la interfaz, no una mejora de rendimiento para cálculos CPU-bound.

  -------------------------------------------------------------------------------------------------------------------------------
  Método                              Función
  ----------------------------------- -------------------------------------------------------------------------------------------
  `submit()`                          Envía una tarea y devuelve un objeto `Future`.

  `map()`                             Aplica una función a los elementos de iterables y entrega resultados en orden de entrada.

  `Future.result()`                   Obtiene el resultado de una tarea; espera si aún no terminó.

  `shutdown()`                        Finaliza el executor y libera sus recursos.
  -------------------------------------------------------------------------------------------------------------------------------

El context manager (`with`) llama automáticamente a `shutdown(wait=True)` al salir.

## 5. Resumen para recordar

-   Cooperative multitasking → `asyncio`.
-   Preemptive multitasking → `threading`.
-   True parallel execution on multiple CPU cores → `multiprocessing` (en el modelo convencional del curso).
-   Automatically manages a pool of worker threads → `ThreadPoolExecutor`.
-   GIL: **bytecode**, **releases**, **overlap** (respuestas del cuestionario).

## 6. Aclaración sobre versiones modernas de Python

Desde Python 3.13 existen compilaciones opcionales de CPython sin GIL (*free-threaded*), que permiten ejecutar código Python en paralelo mediante hilos. Los conceptos del cuestionario se refieren a CPython con el GIL habilitado.

## Documentación oficial

-   [threading](https://docs.python.org/3/library/threading.html)
-   [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
-   [asyncio](https://docs.python.org/3/library/asyncio.html)
-   [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
-   [Free-threaded Python](https://docs.python.org/3/howto/free-threading-python.html)
