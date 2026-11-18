"""
Create and Apply Custom Decorators to Modify Function Behavior

Key Topics:
- Decorator Mechanics: Functions objets and closures.
- Syntax Forms: The '@' symbol vs explicit calls.
-Common Use Cases: When to build vs when to use existing solutions.

Key Terms:
- Higher-order functions: A function that takes abnother functions as an argument or returns one.
- Wrapper functions: The inner function that 'wraps' the original function.
- Closure: A function that remembers the environment in which it was created.
- Cross-cutting concern: Functionality that applies acorss multiple parts of an application (like logging).
- Function metadata: The original function's name (__name__) and docstring (__doc__).

"""

import time
import functools

def timing_decorator(func):
    @functools.wraps(func)
    # Esto es un closure
    def wrapper(*args,**kwargs):
        """The wrapper function that adds the timing logic."""
        start_time=time.perf_counter()
        result=func(*args, **kwargs)
        end_time=time.perf_counter()
        print(f"'{func.__name__}' took {end_time} - {start_time:.4f} seconds to execute" )
        return result
    return wrapper

# Para usar el decorador lo agregamos a la función
# En definitva es azucar sintáctico a decir process_payment=timing_decorator(process_payment) | En Python las funciones son
# ciudadanos de primera clase y se pueden pasar como argumentos a otras funciones.

@timing_decorator
def process_payment(amount,payment_method="credit"):
    """Process payment through an external gateway"""
    time.sleep(0.2)
    return f"Processed ${amount} via {payment_method}"

# En lugar de incluir lógica de procesamiento, tiempos de espera dentro de la función construiremos un decorador como wrapper.


print(process_payment(100))
print()
print(f"Function name: {process_payment.__name__}")
print(f"Docstring: {process_payment.__doc__}")
