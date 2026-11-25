"""
Dr Chester Ismay

Apply Common Design Patterns in Python / Understanding Design Patterns

Next you'll turn the city-planning metaphor into practical design patterns into hands-on Python examples.
By the end, you will be able:
- Recognize when to use Singleton, Factory, Observer, and Decorators.
- Implement each pattern in idiomatic , minimal Python code.
- Explain trade-offs and common pitfalls associated with each pattern.
# Steps 1: Warm-up: The City Map
  Think of your code as a city:
  - Singleton=one ad only power grid.
  - Factory= construction office that builds by specs
  - Strategy= traffic rules that can be swapped
  - Observer= city alert system that notifies residents of changes
  - Decorator= adding new features to buildings without rebuilding them

  `` Los de arriba son los mencionados por el Dr Chester Ismay``

   Otros patrones de diseño son:

  - Adapter= making incompatible systems work together
  - Composite= organizing buildings into hierarchical structures
  - Proxy= controlling access to certain buildings
  - Command= encapsulating requests as objects
  - Template Method= defining the skeleton of a process with customizable steps
  - Iterator= accessing elements of a collection sequentially
  - State= changing behavior based on internal state
  - Builder= constructing complex buildings step by step
"""
import time
from functools import wraps
from turtle import delay

# Step 2 - Singleton: One Power Plant
class Config:
    _instance = None
    settings: dict[str, str]   # Informo a pylance que esta propiedad existirá en la instancia y su tipo es dict[str, str]

    def __new__(cls):
        if not cls._instance:
            obj = super().__new__(cls)
            obj.settings = {"env": "prod"}
            cls._instance = obj
        return cls._instance


a = Config()
b = Config()
print(a is b)  # True, only one instance exists
print(a.settings["env"])  # prod

# Why it works: __new__ returns the same object after the first creation.
# Pitfalls
# * Hiddend dependency; prefer passing Config() into modules that need it explicitly.
# * Testing: add a reset hook if needed in test suites

# Step 3 - Factory: Construction Office | Use when calllers ask for an object by intent, not by constructor details.

class PDF:
    kind = "pdf"

class HTML:
    kind = "html"

REG = {
    "pdf": PDF,
    "html": HTML
}
def make_report(fmt:str):
    return REG[fmt.lower()]() 

print(type(make_report("pdf")).__name__)  # PDF
print(type(make_report("html")).__name__)  # HTML

# Why it works: creation rules live in one place;callers don't touch classes.
# Pitfalls
# * Overgrowwth:keep REG small or split by domain.


# Step 4 -- Stategy : Swap City Plans
# Use then an algorithm shoul be swappable at runtime ( discounts, ranking, costs)
def asc(items):
    return sorted(items)

def desc(items):
    return sorted(items, reverse=True)

class Catalog:
    def __init__(self, strategy):
        self.strategy = strategy
        
    def show(self, items):
        return self.strategy(items)

items=[3,1,4,2]
print(Catalog(asc).show(items))  # [1, 2, 3, 4]
print(Catalog(desc).show(items))  # [4, 3, 2, 1]

# Why it works: Catalog depends on a callable, not a concrete class.
# Pitfalls
# * Too many micro-strategies can fragment logic; name clearly and document their purpose.

# Step 5 - Observer: Monitor City Changes
# Use when one subject needs to notify multiple observers about changes(events,UI updates, state changes).
subs={} # topic => callback

def subscribe(topic, fn):
    subs.setdefault(topic, []).append(fn)

def publish(topic, msg):
    [fn(msg) for fn in subs.get(topic, [])]

subscribe("roads", lambda msg: print("News:",msg))
subscribe("roads", lambda msg: print("TV:",msg))

publish("roads", "New road construction announced.")

# Why it works: publishers don't know the listeners, listeners opt in.
# Pitfalls
# * Hard to trace cascades; keep topic clear and handlers idem potent.

# Step 6: Decorator: Enhance City Plans
# Use when you want to add behavior to functions or methods dynamically without modifing the original function(retries, logging, formatting).

def retry(times=3,delay=0.1):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for _ in range(times -1):
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    time.sleep(delay)
            return fn(*args, **kwargs)  # last attempt
        return wrapper
    return decorator

n={'x': 0}

@retry(3,0.01)
def flaky():
    n['x'] += 1
    if n['x'] < 3:
        raise RuntimeError("not yet")
    return "Success"

print(flaky())  # Success
# Why it works: the wrapper adds behavior before / after the call; wraps preserves metadata of the original function.
# Pitfalls
# * Many stacked decorators can obscure flow; prefer a few well-documented ones.

# Step 7 -- Putting Pattern Together
# Mini-scenario: Build a reporting pipeline
# Factory picks a formatter (pdf,html,csv)
# Singleton config holds shared settings.
# Strategy swaps raning for admin vs public
# Observer announces report_ready to email/cache
# Decorator retries flaky network writes.
# These bluepints interlock like city plans: each solves a recurring seam.

# Quick Heuristic:
# * Only one should exist => Singleton
# * Hide Complex construction => Factory
# * Swap rules /algorithms dynamically => Strategy
# * Notify multiple parties about changes => Observer
# * Enhance behavior of functions/methods dynamically => Decorator      
# * Document the intent and trade-offs of each pattern.

# Wrap-Up & Takeaways
# * Desing pattern are named blueprints. They speed development, improve communication , and reduce bugs when used thoughtfully.
# * Choose the pattern that best fits the recurring problem you are trying to solve.
# * Avoid over-engineering; not every problem needs a design pattern.
# * Keep implementantion tiny and idiomatic, and favor clarity over cleverness.
# * Review and refactor patterns periodically to ensure they still fit the problem context.