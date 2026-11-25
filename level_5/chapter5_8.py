"""
Monitor Memory Usage / Memory Profiling in Python

    Using memory profiling tools like `memory_profiler` to monitor memory usage of memoized functions.
    * A Python package that tracks line by line memory usage of Python code.
    * Works by decorating functions with `@profile` to track their memory usage line by line.
    * Output memory usage in MB next to each line of code.
    * Can be used via Cli or directly within Python scripts.

    Step 1: Install the memory_profiler package using pip.
        ```bash
        pip install memory_profiler
        ```
    Step 2: Use the `@profile` decorator to monitor memory usage of a function.
        ```python
        from memory_profiler import profile

        @profile
        def my_function():
            # Your code here
        ```
        Step 3: Run your Python script with memory profiling enabled.
        ```bash
        mprof run your_script.py
        mprof plot
        ```

    Tips:
    * Profile memory usage regularly during development to catch memory leaks early.
    * Combine with other profiling tools to get a complete picture of your application's performance.

    Guided Practice:

    Welcome to the guided practice for memory profiling in Python.. We'll get hands-on with memory-profiler: your Python 'fuel gauge' for memory usage.
    Just like keeping an eye on your gas tank during a road trip, monitoring memory usage helps you avoid running out of memory unexpectedly.

    By the end of this guided practice, you'll be able to effectively monitor and analyze the memory usage of your Python functions,
    helping you write more efficient and memory-conscious code.

    * Step 1: Define the Use Case
        Scenario:Your frind work for a rideshate company with a script summarizing driver ratings from daily trip log.
        Everything works fine on small datasets, but memory usage becomes a concern as the dataset grows larger and the program crashes .
        Your suspect memory is the culprit. Let's use memory profiler to track where memory spikes and fix it-

    * Step 2: Review The Simulated Report Function

        Look at the `generate_report` function. It simulates generating driver ratings and aggregates them into a report.

        Notice how memory usage can grow with the size of the `ratings` list and the `reports` dictionary.

        We simulate 100,000 ratings to observe memory usage growth

        We group rating by driver in a dictionary

        It looks fine, but is irregular memory efficient?. Lets find out
"""

import random
from memory_profiler import profile


@profile
def generate_report():
    ratings = []
    for _ in range(10**5):
        ratings.append(
            {
                "driver_id": random.randint(1000, 9999),
                "rating": random.choice([1, 2, 3, 4, 5]),
            }
        )
    reports = {}

    for entry in ratings:
        driver = entry["driver_id"]
        reports.setdefault(driver, []).append(entry["rating"])
    return reports


# Line #    Mem usage    Increment  Occurrences   Line Contents

# =============================================================
#     57     28.6 MiB     28.6 MiB           1   @profile
#     58                                         def generate_report():
#     59     28.6 MiB      0.0 MiB           1       ratings = []
#     60     51.2 MiB   -960.7 MiB      100001       for _ in range(10**5):
#     61     51.2 MiB  -1907.3 MiB      200000           ratings.append(
#     62     51.2 MiB   -954.1 MiB      100000               {
#     63     51.2 MiB   -960.6 MiB      100000                   "driver_id": random.randint(1000, 9999),
#     64     51.2 MiB   -958.1 MiB      100000                   "rating": random.choice([1, 2, 3, 4, 5]),
#     65                                                     }
#     66                                                 )
#     67     51.2 MiB      0.0 MiB           1       reports={}
#     68
#     69     53.2 MiB      0.0 MiB      100001       for entry in ratings:
#     70     53.2 MiB      0.0 MiB      100000           driver=entry["driver_id"]
#     71     53.2 MiB      2.0 MiB      100000           reports.setdefault(driver, []).append(entry["rating"])
#     72     53.2 MiB      0.0 MiB           1       return reports


# Optimize the function
@profile
def generate_report_optimized():
    reports = {}
    for _ in range(10**5):
        driver = random.randint(1000, 9999)
        rating = random.choice([1, 2, 3, 4, 5])
        reports.setdefault(driver, []).append(rating)
    return reports


if __name__ == "__main__":
    #generate_report()
    generate_report_optimized()

    # report optimized memory usage

# Line #    Mem usage    Increment  Occurrences   Line Contents
# =============================================================
#    102     28.7 MiB     28.7 MiB           1   @profile
#    103                                         def generate_report_optimized():
#    104     28.7 MiB      0.0 MiB           1       reports = {}
#    105     31.4 MiB      0.0 MiB      100001       for _ in range(10**5):
#    106     31.4 MiB      0.0 MiB      100000           driver = random.randint(1000, 9999)
#    107     31.4 MiB      0.1 MiB      100000           rating = random.choice([1, 2, 3, 4, 5])
#    108     31.4 MiB      2.5 MiB      100000           reports.setdefault(driver, []).append(rating)
#    109     31.4 MiB      0.0 MiB           1       return reports



# Common Pitfall:
# Only functions decorated with @profile are measured for memory usage.
# Avoid mixing in blocking calls like time.sleep(). They distort measurement results.
# Profiling adds overhead. Use it to diagnose memory use, not to benchmark performance.

# Wrap-Up and Takeaways
#  - Memory-profiler reveals hidden costs, line by line.
#  - You spotted a big spike from an unnecesary list.
#  - Refactoring reduce peak memory usage while keeping result correct.
#  - This technique is essential for data heavy workloads, from batch jobs to ML pipelines.
