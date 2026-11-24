# Módulo 5 — GIL y Threading en Python

```
Understanding Python's Global Interpreter Lock (GIL)

Imaginemos una cabina de peaje: incluso si aparecen 1000 coches, solo puede pasar uno a la vez.

El GIL es un mecanismo que protege el estado interno del intérprete CPython (principalmente
el reference counting) para que múltiples hilos no lo corrompan ejecutándose simultáneamente.

Solo presente en CPython, la implementación de Python por defecto.

CPU bound task (e.g., number crunching, image processing, etc.)
  - Threads compete for the GIL => limited performance gain.

IO bound task (e.g., network access, file I/O, etc.)
  - Threads release the GIL => concurrent execution possible.
  - Threads spend time waiting (releasing the GIL) => threading can work well.

GIL is a trade-off between concurrency and performance.

Python provides two main APIs for threading:
  - threading: lower-level, manual thread management.
  - concurrent.futures.ThreadPoolExecutor: higher-level abstraction for running functions in parallel.

Why concurrent.futures is preferred?
  - Easier syntax, more readable code.
  - Automatic worker thread management.
  - Integrates cleanly with submit(), map(), as_completed(), etc.

Tips:
- Usá threads si estás haciendo solicitudes de red paralelas o necesitás operaciones de I/O.
- Evitá threads para operaciones CPU-intensivas; usá múltiples procesos o extensiones de C.


Explicación de Claude

CPython gestiona la memoria con reference counting: cada objeto tiene un contador que indica cuántas variables apuntan a él. Cuando el contador llega a cero, el objeto se libera. Si dos hilos modifican ese contador al mismo tiempo, puede corromperse y Python liberar memoria que todavía se usa, o no liberar memoria que ya no se usa. El GIL es un lock global que garantiza que solo un hilo ejecuta bytecode de Python en un momento dado, eliminando ese problema.

La consecuencia práctica

En tareas CPU-bound (procesar números, comprimir imágenes) dos hilos no corren en paralelo real aunque tengas 8 cores: uno espera mientras el otro tiene el GIL. No ganás nada con threads; necesitás multiprocessing que lanza procesos separados, cada uno con su propio intérprete y su propio GIL.

En tareas IO-bound (llamadas de red, leer archivos, consultas a base de datos) el hilo libera el GIL mientras espera la respuesta. En ese tiempo otro hilo puede correr. Ahí sí tiene sentido usar threads o ThreadPoolExecutor, que es exactamente lo que usaste en el scanner del ejercicio anterior.

Por qué existe todavía

Quitarlo sin romper el ecosistema es extremadamente difícil: hay miles de extensiones en C que asumen que el GIL existe. Python 3.13 introdujo una build experimental sin GIL (PEP 703), pero no es el default todavía.
```
