# Create Iterators with iter and next in Python
numbers = [2, 1, 3, 4]
squares = (n**2 for n in numbers)
print(squares)  # <generator object <genexpr> at 0x000002596A839490>
print(next(squares))  # 4

# print(next(numbers))  # TypeError: 'list' object is not an iterator
"""
¿Que es un iterator?
Sabemos lo que es un iterable, cualquier cosa sobre la que puedas iterar, pero que un iterator?
El iterator es objeto que realiza la ejecución ( iteración --- función iter) sobre el iterable (ej lista)

Desde la perspectiva de Python un iterable es cualquier objeto que puedes pasar
a la función iter.

Iterator Protocol
1 . An iterable can be passed to `iter` function to get an iterator
2 . An ierator can be passed to `next` function to get the next item
3 . When an exhausted iterator is passed to `next`, StopIteration will be raised
4 . Iterators are iterables: they return themselves when passed to `iter`

"""

my_iterator = iter(numbers)
print(my_iterator)  # <list_iterator object at 0x0000018DF9D80C10>
print(next(my_iterator))
print(
    next(my_iterator)
)  # 2 , 1 hasta terminar los elementos, cuando termina, la función next, en el caso de que se ejecute una vez más
# lanzará un error de  StopIteration


def for_loop(iterable):
    for item in iterable:
        print("Do something with", item)


my_iteration = for_loop([2, 1, 3, 4])
print(my_iteration)


# While con Con try and Except
def while_loop(iterable):
    iterator = iter(iterable)
    while True:
        try:
            item = next(iterator)
        except StopIteration:
            break  # iterator exhausted
        else:
            print("Do something with", item)


print(while_loop([50, 60, 30, 80, 90]))


# Los generadores se pueden pasar a Next
numbers_two=[70,89,69,75]
squares_two=(n**2 for n in numbers_two)
print(next(squares_two))

# Es más comun hacer un loop con los generadores, lo que significa que son iterables. Son tanto iteradores como iterables
# Además, cada iterable se le peude pasar a la función iter
for n in squares_two:
    print(n)

