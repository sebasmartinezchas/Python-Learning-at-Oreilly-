"""
Use Metaclasses to Customize Class Creation in Python / Defining New Classes with Metaclasses

En Python todo es un objeto, las clases también. Las metaclases son como definimos y personalizamos
esas clases.
Pero: ¿Que pasaría si quisieramos que las clases sigan reglas?
En ese caso deben ser regidas por una clase mayor, como un director de un casting, su metaclase.

- 1 .type: The default metaclass in Python.

 * Normally used like MyClass=type(name,base,dict)
 name => nombre de la clase como string
 base => es una tupla de clases padres
 dict => diccionario de atributos

- 2 . A metaclass is a class whose instances are classes (not objects)
- 3 . If a object is an instance of MyClass, and MyClass is an instance of Meta, then Meta is a metaclass.

- 4 . You customize metaclass behavior by overriding __new__ or __init__
- 5 . Metaclasses let you intercept or modify:
        a _ Approve or deny the class
        b _ Add properties or structure to it
        c _ Modify how it behaves once created

Example 1: Auto-registration plugin system
    * Whenever a new class is defined, ot registers itself in a global list

Example 2: Enforcing class-level attributes
    * All classes in a framework must define author or version
    
Example 3: Logging class creation
    * Automatically log every time a new class is declared, for audit trails.
        
        
"""