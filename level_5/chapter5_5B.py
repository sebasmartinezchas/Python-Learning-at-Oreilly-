"""
Step 1: The Use Case
Imagine you're fetching data from multiple URLs. Each call is slow because of network delays, not because
of computation. You don't wanto to wait 8 seconds for 4 calls when most of the time is just waiting on the
"internet traffic jam".
 Threads are perfect here because the GIL is released while are waitomg on I/O.
 Let´s simulate this with time.sleep().

"""
import time
import threading

def fetch_data(n):
    print(f"Fetching data from {n}")
    time.sleep(2) # Simulate I/O delay
    print(f"Finished fetching data from {n}")

start=time.time()

for i in range(4):
    fetch_data(i)

end=time.time()
print(f"Total time (serial) :",end-start) # 8.0000000000000004 seconds

# Ejemplo con threading

start_threading=time.time()
threads = []

for i in range(4):
    thread = threading.Thread(target=fetch_data, args=(i,))
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

end_threading=time.time()
print(f"Total time (threading) :",end_threading-start_threading) # 2.0000000000000004 seconds
