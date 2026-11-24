"""
Guided Practice: Writing Async Code with Asyncio

Dr Chester Ismay

We'll next explore how Python's asyncio library works and gives you concurrency without threads.
By the end, you'll be able to:

-Defines coroutines using async def.

-Use awais to pause execution during I/O like delays or network requests.

-Run Multiples coroutines in parallel using asyncio.gather().

-Explain how the event loop enables efficient task switching.

# Step 1: Define the Use Case

Scenario:You're building a web application that needs to fetch data from multiple APIs,

-stock prices, weather, news, etc.-. Each request is slow, but you don't want to wait for them
one by one. You want to fetch all of them at the same time.

Async code lets you fire off all request at once and handle results as they arrive, without spinning up
multiple threads.

We'll simulate this by using asyncio.sleep() to represent slow network calls.

"""

import asyncio
import time


async def fetch_data(n):
    print(f"Fetching data from {n}")
    await asyncio.sleep(2)  # Simulate I/O delay
    print(f"Data fetched from {n}")  # 2.00 seconds per fetch


# Now we'll call it serially inside a main coroutine.
async def main_serial():
    start = time.perf_counter()
    for i in range(4):
        await fetch_data(i)
        elapsed = time.perf_counter() - start
        print(f"Time taken: {elapsed:.2f} seconds")  #200 seconds


asyncio.run(main_serial())


# Step 3 : Run Coroutines concurrently using asyncio.gather()
async def main_concurrent():
    start = time.perf_counter()
    tasks = [fetch_data(i) for i in range(4)]
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    print(f"Time taken (concurrent): {elapsed:.2f} seconds")  # 2.00 seconds


asyncio.run(main_concurrent())

# Explanation:
# The asyncio.gather() function runs the coroutines in parallel and waits for all of them to complete.
# Each coroutines pauses on await ,allowing others to run
# The event loop orchestrates this efficiently : no threads, no locks, just cooperative multitasking.

# Step 4: Compare with Threading
# with threading.Thread, Python spins up multiple operations systems threads.
# wirn asyncio, everything runs on a single event loop thread, but tasks politely take turns at await points.
# Threads can feel more 'parallel' but they carry extra overhead and  the risk of conflicts. Asyncciois
# lighter and safer for I/O -bound workloads.

# Step 5:Commont Pitfalls
# Watch out for these:
# 1. Forgetting to await => the coroutine won't run at all.
# 2. Mixing in blocking code like time.sleep()=> it freezes the whole event loop.Always use asyncio.sleep().
# 3. Using asyncio.run() inside Jupiter =>raises RunTime Error since a loop is already running.- Use await main() in notebook.

# Step 6: Review
# You just wrote and ran real async code!

# Key Points:
# 1. async def defines a coroutine.

# 2. await yields control back to the event loop.

# 3 . asyncio.gather() runs coroutines concurrently.

# 4. In Notebooks/Quarto, use top-level await to run async code, in scripts use asyncio.run().

# 5. Asyncio is perfects for juggling multipleoperations at once, like network requests or file I/O.

# This patterns in the backbone of web servers, chatbots,crawling, and high-performance APIs.
