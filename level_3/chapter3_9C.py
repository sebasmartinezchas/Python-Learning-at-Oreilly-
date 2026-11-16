import time
from collections import defaultdict

class PerformanceTimer:
    _statistics = defaultdict(list)

    def __init__(self, operation_name):
        self.operation_name = operation_name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.start_time is None:
            raise RuntimeError("PerformanceTimer was not started properly.")
        end_time = time.perf_counter()
        elapsed = end_time - self.start_time


        if exc_type is None:
            self._statistics[self.operation_name].append(elapsed)
            print(f"Operation '{self.operation_name}' took {elapsed:.4f} seconds.")
        else:
            print(f"Operation '{self.operation_name}' raised an exception: {exc_value}. Elapsed time: {elapsed:.4f} seconds.")

    @classmethod
    def print_stats(cls):
        print("\nPerformance Statistics:")
        for operation, times in cls._statistics.items():
            avg_time = sum(times) / len(times)
            print(f"Operation '{operation}': Average Time: {avg_time:.4f} seconds over {len(times)} runs.")

    # Simulate a few operations to demonstrate the performance timer
with PerformanceTimer("Operation A"):
     time.sleep(0.5)  # Simulate a time-consuming operation  

with PerformanceTimer("Operation B"):
     time.sleep(0.2)  # Simulate a faster operation

with PerformanceTimer("Operation A"):
     time.sleep(0.3)  # Simulate another run of Operation A

# This one will fail
try:
     with PerformanceTimer("Operation C"):
          time.sleep(0.1)
          raise ConnectionError("Simulated error in Operation C")
except ConnectionError:
    pass


print("\n--- Performance Statistics ---")
PerformanceTimer.print_stats()