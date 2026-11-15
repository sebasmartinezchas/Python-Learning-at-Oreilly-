"""
Create Genertator Functions in Python / Writting effient Python Iterators

"""
# Python never reaches the seconnd and third return statements
#  because the first return statement is executed and the function finishes.
def myfunc():
    return 1
    return 2
    return 3

print(myfunc())

def myfunc():
    yield 1
    yield 2
    yield 3

print(myfunc())
# outputs: <generator object myfunc at 0x000001A4540273C0>  
# This is a generator object -- it knows how to behave inside a for loop.
# A generator is an iterator that can be used to iterate over a sequence 
# of values.
# A generator is created using the yield keyword.
# A generator is a function that returns a generator object.
# A generator object is an iterator that can be used to iterate over a sequence of values.
# A generator object is created using the yield keyword.
# A generator object is a function that returns a generator object.
# When we write our function, Python notices that we have a yield keyword insde
# of the function body. As a result, Python treats this function as a generator function. not
# as  regular function,which executes the body when we run it,but rather as a generator function.
#,which returns a generator object when we run it.
# What can we do with a generator object? Put it into a for loop.!!!

g=myfunc()
for one_item in g:
    print(one_item)
# outputs: 1
# 2
# 3
# The generator object is now empty.
"""
Generator Functions
A generator function is a function! It has all of the capabilities of a regular function.
--arguments,function body,return statement,etc.--
The only difference is that a generator function uses the yield keyword instead of the return keyword.
Each time, when we run the generator (iterate over the generator), the function
will return a value at "yield" and then go to sleep.
The next iteration, then picks up right after the previous one.
    """


def myfunc():
    print("line 1")
    yield 1
    print("line 2")
    yield 2
    print("line 3")
    yield 3
    print("line 4")
    yield 4
    print("line 5")
    yield 5
    print("line 6")
    yield 6
    print("line 7")
    yield 7
    print("line 8")
    yield 8
g=myfunc()
next(g) # low level iterator command -- give me your next value
next(g)
next(g)
next(g)
next(g)
next(g)
next(g)
next(g)
next(g)
next(g)
next(g)
next(g)
next(g)
next(g) # StopIteration error -- no more values to iterate over

def fib():
    first=0
    second=1
    while True:
        yield first
        first, second = second, first + second

g=fib()
print(next(g))
print(next(g))
print(next(g))


for one_item in fib():
    if one_item > 100_000_000_000:
        break
    print(one_item,end=" ")

# outputs: 0
# 1
# 1
# 2
# 3
# 5
# 8
# 13
# 21

# Where are generator functions used?
# 1 - Very long sequences that we want to get in small doses.
# 2 - Filtering data.
# 3 - Gerenally speaking, modern Python programs try not to return lists,because they migght
# be very large. We don't lose much always return generators.


# Exercise: char_range
# You're familiar with range, the Python built that allows us to say range(10,15)
# , and then we get all of the numbers from 10 to 14.
# I want to do the same whing with characters. So, char_range("a","f") and
# you''ll get all of the characters, one at a time( in each etaration)
# from 'a' to 'z'.
def char_range(start,stop):
    for one_item in range(ord(start),ord(stop)):
        yield chr(one_item)

for one_item in char_range("a","f"):
    print(one_item)

# outputs: a b c d e 