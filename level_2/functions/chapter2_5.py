# Introducing Generator Expressións

"""
# List Comprehension: Photocopy the whole book at once
[expression for item in iterable]
=> Creates a full list in memory inmediately.

# Generator Expression: Read one page at a time
(expression for item in iterable)
=> Creates a "generator object" that produce items on demand.

"""
# Guided Practice Setup
import sys
import itertools

# Create a large dummy file
with open('large_file.csv','w') as f:
    for i in range(1_000_000):
        f.write(f"line number {i}\n")

# Memory- heavy approach (list comprehension)
lines_list=[line.strip().upper() for line in open('large_file.csv')]
print(f"List comprehension memory usage: {sys.getsizeof(lines_list)} bytes")


# Memory- efficient  approach (generator expression)
lines_gen = (line.strip().upper() for line in open("large_file.csv"))
print(f"Generator expression memory usage: {sys.getsizeof(lines_gen)} bytes")
