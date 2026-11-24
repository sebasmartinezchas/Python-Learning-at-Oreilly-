# Módulo 5 — Asyncio y concurrencia en Python

## ¿Qué es asyncio?

Asyncio es una librería de Python para escribir código concurrente usando coroutines, event loops y tasks.

A diferencia de `threading` (que usa múltiples hilos del sistema operativo), asyncio corre todo en un
único hilo con un **event loop** que orquesta las tareas.

**En asyncio, una *task* es una coroutine envuelta por el event loop para ejecutarse concurrentemente
con otras. Los threads y procesos son conceptos de otras APIs (`threading`, `multiprocessing`), no de asyncio.**

---

## Conceptos clave

| Concepto | Descripción |
|---|---|
| `async def` | Define una coroutine |
| `await` | Pausa la coroutine y devuelve el control al event loop hasta que la tarea termine |
| Event loop | Programa las tasks y alterna entre ellas |
| Coroutine | Debe ceder el control voluntariamente con `await` — no hay preempción |

> Las coroutines **no corren solas**: hay que ejecutarlas con `asyncio.run()` o desde otra coroutine con `await`.

---

## Cuándo usar asyncio

**Ideal para:**
- Fetching de múltiples APIs en paralelo.
- Conexiones concurrentes a bases de datos o sockets.
- Web services o bots de alto throughput.

**No recomendado para:**
- Tareas CPU-intensivas (cálculos numéricos, procesamiento de imágenes).
- Cómputos de larga duración (encoding de video, cálculos grandes).
- Aplicaciones con requisitos de latencia estricta.
- Codebases que no son async-friendly.

---

## Asyncio vs Threading

| | Threading | Asyncio |
|---|---|---|
| Modelo | Concurrencia preemptiva | Concurrencia cooperativa |
| Recursos | Múltiples hilos del SO | Un único hilo con event loop |
| Complejidad | Más fácil de razonar, pero propenso a errores | Más complejo, pero más seguro y predecible |
| Mejor para | Operaciones de I/O bloqueantes | Operaciones de I/O de alto volumen |

Con `threading`, Python lanza múltiples hilos del sistema operativo.
Con `asyncio`, todo corre en un único hilo del event loop, pero las tasks se turnan en los puntos `await`.
Los threads pueden sentirse más "paralelos" pero tienen overhead extra y riesgo de conflictos.
Asyncio es más liviano y seguro para workloads I/O-bound.

---

## Caso de uso: fetching de múltiples APIs

Escenario: una aplicación necesita obtener datos de múltiples APIs (precios de acciones, clima, noticias, etc.).
Cada request es lento, pero no queremos esperar uno por uno.
Async permite lanzar todos los requests a la vez y manejar los resultados a medida que llegan,
sin necesidad de múltiples threads.

Simulamos los requests con `asyncio.sleep()`.

---

## Código: ejecución serial vs concurrente

```python
import asyncio
import time


async def fetch_data(n):
    print(f"Fetching data from {n}")
    await asyncio.sleep(2)  # Simula el delay de una llamada de red
    print(f"Data fetched from {n}")


# Ejecución serial: espera cada fetch antes de continuar
async def main_serial():
    start = time.perf_counter()
    for i in range(4):
        await fetch_data(i)
    elapsed = time.perf_counter() - start
    print(f"Time taken: {elapsed:.2f} seconds")  # ~8.00 seconds


asyncio.run(main_serial())


# Ejecución concurrente: lanza todos los fetches a la vez
async def main_concurrent():
    start = time.perf_counter()
    tasks = [fetch_data(i) for i in range(4)]
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    print(f"Time taken (concurrent): {elapsed:.2f} seconds")  # ~2.00 seconds


asyncio.run(main_concurrent())
```

**Por qué funciona `asyncio.gather()`:**
- Lanza todas las coroutines y espera a que todas terminen.
- Cada coroutine pausa en `await`, permitiendo que las otras corran.
- El event loop orquesta esto eficientemente: sin threads, sin locks, solo multitasking cooperativo.

---

## Errores comunes

1. **Olvidar el `await`** → la coroutine no corre, solo se crea el objeto coroutine.
2. **Usar `time.sleep()` en lugar de `asyncio.sleep()`** → congela todo el event loop.
3. **Usar `asyncio.run()` dentro de Jupyter** → lanza `RuntimeError` porque ya hay un loop corriendo.
   Solución: usar `await main()` directamente en la celda del notebook.

---

## Resumen

1. `async def` define una coroutine.
2. `await` devuelve el control al event loop.
3. `asyncio.gather()` corre coroutines concurrentemente.
4. En scripts, usar `asyncio.run()`. En notebooks/Quarto, usar `await main()` a nivel top-level.
5. Asyncio es ideal para manejar múltiples operaciones I/O simultáneas: network requests, file I/O, etc.

Este patrón es la base de web servers, chatbots, crawlers y APIs de alto rendimiento.
