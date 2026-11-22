# Implement Multiple Inheritance in Python / Handling Inheritance Ambiguity with MRO
"""
Method Resolution Order (MRO)
Handling Inheritance Ambiguity

You can have a class implement multiple
parent classes, combining functionality and
traits

Note that when you start extending classes with shared method name, it can get
ambiguous which method will actualy be called.

- When a method signature is shared between a child and a parent, the child will be called-
- When two or more parents share a method and the child does not override it, the 'left
 parent will be called

 class A
    def do_action(self):
    print("In class A")

 class B(A):
    def do_action(self):
    print("In class B)

 class C(A):
    def do_action(self):
    print("In class C")

 class D(B,C):
    pass # don't add any methods

r=D()
d.do_Action() # prints "In class B"

"""


class Flyer:
    def fly(self, speed, altitude):
        if speed < 0 or altitude < 0:
            raise ValueError("Speed and altitude must be positive")
        return f"flying at {speed} mph at {altitude} ft"


class Swimmer:
    def swim(self, speed, depth):
        if depth > 0:
            raise ValueError("Depth must be negative or zero.")
        return f"Swimming at {speed} mph at {depth} ft depth"


class Fish(Swimmer):
    def glub(self):
        return "Glub Glub"


class Duck(Flyer, Swimmer):
    def quack(self):
        return "Quack Quack"

    def swim(self, speed, depth=0):
        if depth != 0:
            raise ValueError("Depth must be zero for a duck!")
        return super().swim(speed, depth)


# print("FISH:")
# fish = Fish()
# print(fish.glub())
# print(fish.swim(7, -10))

# print("DUCK")
# duck = Duck()
# print(duck.quack())
# print(duck.fly(20, 30))
# print(duck.swim(5))


# Cambiamos un poco los ejemplos, usaremos __init__  en los hijos entre otras cosas
class FlyerTwo:
    def __init__(self, max_height):
        self.max_height = max_height

    def make_noise(self):
        return "Whooosh"


class SwimmerTwo:
    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def make_noise(self):
        return "Splash!"


class DuckTwo(FlyerTwo, SwimmerTwo):
    def __init__(self, max_height, depth_limit):
        FlyerTwo.__init__(self, max_height)
        SwimmerTwo.__init__(self, depth_limit)

    def make_noise(self):
        return "Quack"


duck_two=DuckTwo(100,0)

print(f'max_height: {duck_two.max_height}')
print(f'depth_limit: {duck_two.depth_limit}')
print(f'make_noise: {duck_two.make_noise()}')

"""
Si quitamos el método make_moise en DuckTwo, como lo hereda de las dos clases va a tomar el valor que tenga la primera de la izquierda
que pasamos como argumento ( las super clases ), en este caso la de FlyerTWo, esto lo podemos modificar según cual sea nuestra necesidad.
"""
