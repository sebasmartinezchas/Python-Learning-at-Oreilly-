# Use Inherintance to Extends Python Classes / Reducing Repetitive Code
class Pet:
    def __init__(self, name):
        self.name = name


class Dog(Pet):
    def describe(self):
        return "Mensaje de Dog"


class Cat(Pet):
    def describe(self):
        return "Mensaje de Cat"


fredy = Dog("Fredy")
mycha = Dog("Misha")

print(f"{fredy.name} | {fredy.describe()}")

print(f"{mycha.name} | {mycha.describe()}")


class Quarter:
    value = 25


class QuarterTwo:
    def __init__(self, value):
        self.value = value


"""
¿Cual es la diferencia de esas dos opciones? 
En una clase tan pequeña no tiene demasiada importancia
Pero miremos la siguiente
"""


class PetTwo:
    sound = ""

    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"the pet says: {self.sound}"


class DogTwo(PetTwo):
    sound = "Woof"


class CatTwo(PetTwo):
    sound = "Meow"


class Bird(PetTwo):
    sound = "Chirp"

   


"""
Las subclases pueden sobreescribir un valor de la superclase, específicamente 'sound'.
Entonces definimos un método en la clase base y ajustamos el comportamiento en las subclases, 
esto es realmente muy poderoso.
"""
rover = DogTwo("Rover")
print(rover.describe())
print(isinstance(rover,PetTwo))

misty = CatTwo("Misty")
print(misty.describe())

angel = Bird("Angel")
print(angel.describe())

# The __class__attribute
""""
Python instances all have an attribute called __class__
This is the same class object they were instantiated from.


"""


class Penny:
    value = 1


coin = Penny()
print(coin.__class__)  # <class '__main__.Penny'>

# Can eve instantiate from it!
new_coin = coin.__class__()

print(type(new_coin))  # <class '__main__.Penny'>

# In Python, all class objets hace a __name__attribute - a string:
print(Penny.__name__)  # Penny
print(coin.__class__.__name__)  # Penny

# Even the built-in types have this! They're classes too.
print(int.__name__)
print(dict.__name__)
x = 4.5
y = ["a", "b", "c"]
print(x.__class__.__name__)  # float

print(y.__class__.__name__)  # list

print(type(x.__class__.__name__))  # <class 'str'>

print(type(y.__class__.__name__))  # <class 'str'>'list


# Pet.describe()
class PetThree:
    sound = ""

    def __init__(self, name) -> None:
        self.name = name

    def describe(self):
        kind_of_pet = self.__class__.__name__.lower()
        return f"the {kind_of_pet} says: {self.sound}"


class DogThree(PetThree):
    sound = "Woof"


class CatThree(PetThree):
    sound = "Meow"


luna = DogThree("Luna!")
print(luna.describe())

noah = CatThree("Noah")
print(noah.describe())
