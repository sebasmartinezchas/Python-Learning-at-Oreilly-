"""
# Write Multi- Threaded and Async Code in Python / Introducing Asyncio for Lightweight Concurrency


# In this chapter, we will learn how to write multi-threaded and async code in Python.

# We will also learn about Asyncio, a library for lightweight concurrency.

# Asyncio is a library for writing concurrent code using coroutines, event loops, and tasks.

En asyncio, una task es una coroutine envuelta por el event loop para ejecutarse concurrentemente con otras.
Los threads y procesos son conceptos de otras APIs (threading, multiprocessing), no de asyncio."

# async def creates a coroutine

# await is used to pause the coroutine and wait until the task is completed.

# The event loop schedules tasks. switches between them.

# Coroutines must voluntarily yield (with await)-no preemption.

# Ideal for I/O-heavy tasks like network requests, file operations, etc.

# Great for:

    -Fetching from many APIs.
    - Managing concurrent database or socket connections.
    - High-throughput web services or bots.

# Not great for :

    - CPU-intensive tasks (e.g., number crunching, image processing).
    - Long-running computations (e.g., video encoding, large calculations).
    - Real-time or latency-sensitive applications.
    - Codebases that are not async-friendly.

Comparing Asyncio with Threading:
    - Asyncio is a library for writing concurrent code using coroutines, event loops, and tasks.
    - Threading is a library for writing concurrent code using threads.

# Threads:

- Model => Premptive concurrency
- Resources=> Multiple OS threads
- Complexity => Easier to reason but error prone
- Best for => Blocking I/O operations

# Asyncio:

- Model => Cooperative concurrency
- Resources=> Single event loop thread
- Complexity => More complex but more safe and predictable
- Best for => High-volume I/O operations

"""
