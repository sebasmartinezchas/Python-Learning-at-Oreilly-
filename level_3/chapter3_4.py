# Use @property to Define Read-Only Attributes in Python / Understand Python Attribute Properties
""" Read Only Properties 
    1 . Attributes
    2 . Properties  
    3 . Read Only Properties

Attributes are a storage system.
Each value in Python, each object, has its own attributes-- a miniature
dict on the value.

"""
# We can see what attributes a value has by invoking "dir" built-in function.
s='Hello, World!'
print(dir(s))
# Properties
# A property is a simplified version of something know as a "descriptor" in Python.
"""
The idea is:
* We'll set an attribute on the class.
* This attribute, when we retrieve it, will actually invoke a method.
* This attribute, when we set it, will actually invoke a (separate,different method).

"""
class BadAgeError(Exception):
    pass

class Person:
    def __init__(self,name,age):
        self.name=name
        self._age=age # We use a single underscore to indicate that this attribute is private.
    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self._age} years old.")

    @property
    def age(self):
        return self._age
    @age.setter
    def age(self,new_age):
        if new_age < 0:
            raise BadAgeError("Age must be positive")
        if new_age > 120:
            raise BadAgeError("Age must be less than 120")
        self._age=new_age
   
p=Person("John",30) 
print(p.age) # We're retrieving the age attribute. Because it's a property and get its return value back.

