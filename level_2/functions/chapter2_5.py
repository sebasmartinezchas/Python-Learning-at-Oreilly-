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


# The generator only produces values when we iterate ("Lazy evaluation")
print("First 5 lines from the generator: ")
for i, line in enumerate(lines_gen):
    if i>=5:
        break
    print(line)

# An example working with a for large secuences like fibonacci, posible for the generators and imposible for list
def fibonacci():
    """An infinite generator for the Fibonacci sequence"""
    a,b=0,1
    while True:
        yield a
        a,b=b,a+b

fib_squares=(x**2 for x in fibonacci())
first_10_squares=list(itertools.islice(fib_squares,10))
print(f"The first 10 Fibonacci squares : {first_10_squares}")

# I want to find the squares of even numbers under 1,000,000 but only keep those under 1,000."
# 1. Start with a sequence of numbers
numbers=range(1_000_000)

# 2. Chain a generator to filter for even numbers
evens=(x for x in numbers if x % 2 ==0)

# 3. Chain another generator to square them
squares=(x**2 for x in evens)

# 4. Chain a final generator to filter the results
filtered=(x for x in squares if x < 1000)

# 5. The data is only processed when we iterate!!!!
print(list(filtered))

"""
Common Mistakes to Avoid

1. Trying to iterate over a generator multiple times. It gets "used up"
after the first pass!

2. No realizing generators are consumed. Once you loop over it, it´s empty

3. Using generators for small datasets or when you need random access( e.g., `my_list[10]`). Lists are better for that.

"""



