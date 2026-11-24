"""
Guided Practice: Building a PLugin Registry with a Metaclass

Dr Chester Ismay:

You'll next hand-on with metaclasses --the 'casting directors' of Python classes
Our Mission is to build a simple plugin registry that automatically track all new plugin subclasses, without any
extra work  from developers.

By the end, you'll be able to:
 * Define a custom metaclass by subclassing type
 * Intercept class creation with __init__
 * Automatically register subclasses in a global registry
 * Recognize why this technique show up in real framework and plugin systems

 Step 1: Introduce the Use Case

 Imagine you're running a studio. Every time a new actor joins, you want them added to the roster automatically.
   No paperwork. No forgetting.

 In software, the same thing happend with plugins. You want every class automatically added to a registry, so your
   app can discover them.

 That's where a metaclass steps in. It's the casting director, making sure every new class signs the contract before
 entering the production.

 Step 2: Define the Metaclass

 Here's the heart of our system:



"""

plugin_registry = {}


class PluginMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if name != "Plugin":  # Skip the base class
            plugin_registry[name] = cls  # key => name / value: the class itself


"""
What's happening?
 * cls is the class being created (not an instance of it).
 * We override __init__ to intercept class creation.
 * We add the new class to plugin_registry
 * The base Plugin itself isn't added - only- its subclasses
 
 Think of this as: every actor role created must be approved by casting and added to the roster.

 Step 3 : Create a Base Class and Subclasses
 Now let's see the metaclass in action
 

 Step 4 : Common Mistakes and Misconceptions
 
 Here a a few traps to avoid:

    * Forgetting to declare the base with metaclass=PluginMeta => no registry magin happens.
    * Mixing up __init__ for instances with the metaclass __init__ for classes.
    * Overriding __new__ when you only need __init__

   Tip:add a debug print to confirm what's happening:
   print(f'Registering Class: {name}')

   This way, you'll see exactly when classes get added.


   Wrap-Up & Takeaways
   
   You just buil a real metaclass!

   Key takeaways:

        * A metaclass is the class of a class. It controls whether a class even exists.
        * Overriding __init__ in a metaclass lets you intercept class creation
        * With this, you can auto-register, enforce rules, or inject shared behaviors.
        * Frameworks like Django, SQLAlchemy, and Flask extensions use this same pattern.

    Remember: actors play roles, but the casting director decides if the role even makes it on stage.
 """


class Plugin(metaclass=PluginMeta):
    pass


class VideoPlugin(Plugin):
    pass


class AudioPlugin(Plugin):
    pass


print(
    plugin_registry
)  # output {'VideoPlugin': <class '__main__.VideoPlugin'>, 'AudioPlugin': <class '__main__.AudioPlugin'>}

# Notice: As soon as each subclass is defined, it shows up in the registry. No extra `register` function call is needed.
# Shis pattern is super useful un plugin systems, serialization frameworks, and ORMs.
