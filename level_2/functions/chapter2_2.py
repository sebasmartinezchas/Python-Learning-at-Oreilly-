"""
1. smallest_and_largest -- this function should take any number of integers as positional arguments. It
returns a tuple with 2 elemts, the smallest and largest integers from the input arguments. We can
assume that we received at least one argument.

2. apply_functions -- this functions take one regular argument, and then any number of keyword arguments, which will have functions
as values. Each functions is applied to that value , giving us a new dict back as a return value.
"""


def smallest_and_largest(*args):
    smallest = args[0]
    largest = args[0]
    for number in args:
        if number < smallest:
            smallest = number
        if number > max:
            largest = number

    return smallest, largest

def apply_functions(x, **kwargs):
    results = {}
    for key, value in kwargs.items():
        results[key]=value(x)


    return results



