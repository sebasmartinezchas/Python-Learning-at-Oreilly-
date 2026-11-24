"""
* Understanding Python's Global Interpreter Lock (GIL)
* Imaginemos una cabina de peaje, incluso si aparecen 1000 coches, solo puede pasar uno a la vez.
* El GIL es un mecanismo que evita que múltiples hilos de ejecución accedan a la misma región de memoria
* de manera concurrente, garantizando así la seguridad de la ejecución.
* El GIL es un mecanismo que evita que múltiples hilos de ejecución accedan a la misma región de memoria
* Solo presente en CPython, la implementación de Python por defecto.
* CPU bound task (e.g,number crunching,image processing,etc.
   - Threads compete for the GIL => limited performance gain.
* IO bound task (e.g,network access,file I/O,etc.
   - Threads release the GIL => concurrent execution possible
   - Threads spend time waiting (releasing the GIL) => threading can work well

 GIL is a trade-off between concurrency and performance.

 * Phyton provides two main Apis for threading:
   - threading for lower-level, manual thread management
   - concurrent.futures.ThreadPoolExecutor for higher-level abstraction for running functions in parallel
   thread.

   Why concurrent.futures is preferred?
    - Easier syntax, more readable code
    - Automatically worker threads management
    - Integrates cleanly with submit(),map(),as_completed(),etc.

* Tips:
Utilice subprocesos si esta realizando solicitudes de red paralelas o si necesita realizar operaciones de E/S.

Evite los subprocesos si necesita realizar operaciones de CPU intensivas, utilice multiples procesos o extensiones de C.

"""
