# Patrones de diseño en Python

**Curso:** Apply Common Design Patterns in Python / Understanding Design Patterns\
**Instructor:** Dr. Chester Ismay --- O'Reilly\
**Propósito:** apuntes personales de estudio, revisados y ampliados.

## 1. ¿Qué es un patrón de diseño?

Un patrón de diseño es una solución conceptual reutilizable a un problema recurrente de diseño de software. No es una receta de código obligatoria ni una biblioteca. Describe responsabilidades, relaciones y decisiones de diseño.

Python permite implementar patrones mediante clases, funciones, módulos y estructuras de datos. No siempre hace falta recurrir a la programación orientada a objetos. Las funciones y clases son objetos de primera clase: pueden almacenarse, pasarse como argumentos y devolverse.

Los patrones clásicos del libro *Design Patterns* (Gamma, Helm, Johnson y Vlissides, 1994), conocido como GoF, se agrupan en tres familias:

-   **Creacionales:** cómo se crean los objetos.
-   **Estructurales:** cómo se componen objetos y clases.
-   **De comportamiento:** cómo se distribuyen responsabilidades y se comunican los objetos.

## 2. La metáfora de la ciudad

  ---------------------------------------------------------------------------------------------------------------------
  Patrón de la clase   Familia             Metáfora                             Problema que resuelve
  -------------------- ------------------- ------------------------------------ ---------------------------------------
  Singleton            Creacional          Una central eléctrica                Compartir una única instancia

  Factory              Creacional          Oficina de construcción              Centralizar la creación de objetos

  Strategy             Comportamiento      Reglas de tránsito intercambiables   Cambiar algoritmos

  Observer             Comportamiento      Sistema de alertas                   Notificar a interesados

  Decorator            Estructural (GoF)   Mejoras en edificios existentes      Añadir comportamiento por composición
  ---------------------------------------------------------------------------------------------------------------------

Factory es un término general: el ejemplo de la clase es una fábrica simple basada en un registro, no necesariamente el patrón GoF Factory Method. El ejemplo de Decorator utiliza decoradores de funciones de Python, relacionados con la intención del patrón estructural GoF, pero no idénticos a él.

## 3. Singleton --- One Power Plant

### Concepto

Restringe la creación a una única instancia de una clase y proporciona un mecanismo para acceder a ella. Puede servir para configuración compartida, servicios de logging o administración de un pool de conexiones. Esto no significa que toda aplicación deba tener un único logger o pool.

### Ejemplo de la clase

``` python
class Config:
    _instance = None
    # Type hint: settings is initialized in __new__
    settings: dict[str, str]

    def __new__(cls):
        if not cls._instance:
            obj = super().__new__(cls)
            obj.settings = {"env": "prod"}
            cls._instance = obj
        return cls._instance


a = Config()
b = Config()
print(a is b)  # True
print(a.settings["env"])  # prod
```

### Cómo funciona

1.  `_instance` es un atributo de clase, inicialmente `None`.
2.  Al ejecutar `Config()`, Python llama a `__new__`, que recibe la clase (`cls`), no una instancia.
3.  En la primera llamada, `super().__new__(cls)` delega la creación del objeto al siguiente método de la jerarquía de resolución (aquí, `object.__new__`).
4.  `obj.settings = ...` crea dinámicamente un atributo de instancia. No requiere una declaración previa.
5.  La referencia al objeto queda almacenada en `cls._instance`.
6.  Las siguientes llamadas devuelven la referencia existente sin crear otro objeto.

Normalmente Python ejecuta `__init__` después de `__new__` cuando este devuelve una instancia de la clase solicitada. Esto ocurre incluso si la instancia ya existía. Por eso el profesor inicializa `settings` dentro de la rama de creación de `__new__`: evita reinicializar el diccionario cada vez.

### Identidad, atributos y Pylance

`is` comprueba identidad; `==` comprueba igualdad según la semántica del tipo. Aquí `a is b` es verdadero porque ambas variables referencian el mismo objeto.

``` python
print(a.__dict__)  # {'settings': {'env': 'prod'}}
a.settings["env"] = "dev"
print(b.settings["env"])  # dev
```

La anotación `settings: dict[str, str]` informa a Pylance del atributo esperado. No crea el diccionario ni impone el tipo en tiempo de ejecución. `_instance` pertenece a la clase; `settings` pertenece a la instancia.

### Riesgos y alternativas

-   Es preferible comprobar `cls._instance is None` en vez de `not cls._instance`: expresa exactamente la condición deseada y no depende de la evaluación booleana del objeto.
-   El ejemplo no garantiza una única instancia ante llamadas concurrentes desde varios hilos: la comprobación y creación no forman una operación atómica. Si se necesita esa garantía, hace falta sincronización, por ejemplo con un lock.
-   No garantiza unicidad entre procesos ni contempla correctamente todos los escenarios de herencia.
-   El estado compartido puede ocultar dependencias y complicar pruebas. Un reset para tests requiere cuidado porque pueden quedar referencias anteriores.
-   Una alternativa habitual en Python es un módulo con configuración compartida o crear una instancia explícitamente y pasarla a quienes la necesitan (inyección de dependencias). Los módulos normalmente se reutilizan mediante `sys.modules` dentro de un intérprete.

**Cuándo elegirlo:** cuando la unicidad sea un requisito real, no simplemente porque resulte cómodo acceder a un objeto global.

## 4. Factory --- Construction Office

### Concepto

Centraliza la selección y creación de objetos. El cliente solicita un objeto por su intención o formato sin conocer los detalles de su construcción. Útil para proveedores de pago, formatos de archivos y plugins.

``` python
class PDF:
    kind = "pdf"


class HTML:
    kind = "html"


REG = {
    "pdf": PDF,
    "html": HTML,
}


def make_report(fmt: str):
    return REG[fmt.lower()]()


print(type(make_report("pdf")).__name__)  # PDF
print(type(make_report("html")).__name__)  # HTML
```

### Cómo funciona `REG[fmt.lower()]()`

-   `fmt.lower()` normaliza el texto a minúsculas.
-   `REG[...]` recupera el objeto clase asociado a esa clave.
-   Los paréntesis finales llaman a esa clase y crean una instancia.

La expresión equivale a:

``` python
report_class = REG[fmt.lower()]
report = report_class()
```

`PDF` es la clase; `PDF()` es una instancia. `type(obj).__name__` obtiene el nombre de la clase como string. `kind` es un atributo de clase.

El registro almacena clases, pero también podría almacenar funciones constructoras. A diferencia del Singleton, esta fábrica crea un objeto nuevo en cada llamada en el ejemplo presentado.

### Riesgos y matices

-   Un formato desconocido produce `KeyError`. Una API real puede validar el formato y generar un error más descriptivo.
-   `PDF` y `HTML` son ejemplos mínimos; no generan archivos reales. En una aplicación deberían compartir un contrato útil, por ejemplo un método `render()`.
-   El registro puede crecer demasiado. Separarlo por dominio cuando corresponda.
-   No agregar una fábrica si llamar directamente al constructor resulta suficientemente claro.

**Distinción GoF:** Factory Method delega la elección de producto a subclases mediante un método de creación; Abstract Factory crea familias de objetos relacionados. Este ejemplo es una fábrica simple con registro, perfectamente válida como técnica Python.

## 5. Strategy --- Swap City Plans

### Concepto

Encapsula algoritmos intercambiables para que el cliente pueda elegir cuál utilizar sin modificar la lógica que los consume. Útil para descuentos, rankings, costos y procesamiento de datos.

``` python
def asc(items):
    return sorted(items)


def desc(items):
    return sorted(items, reverse=True)


class Catalog:
    def __init__(self, strategy):
        self.strategy = strategy

    def show(self, items):
        return self.strategy(items)


items = [3, 1, 4, 2]
print(Catalog(asc).show(items))  # [1, 2, 3, 4]
print(Catalog(desc).show(items))  # [4, 3, 2, 1]
```

### Cómo funciona

`asc` y `desc` son referencias a funciones; no se ejecutan al pasarlas al constructor. `Catalog` almacena el callable y lo ejecuta posteriormente mediante `self.strategy(items)`. No necesita conocer el algoritmo concreto.

`sorted()` devuelve una lista nueva, a diferencia de `list.sort()`, que modifica la lista y devuelve `None`.

El ejemplo crea dos catálogos. También permite cambiar la estrategia en tiempo de ejecución sobre el mismo objeto:

``` python
catalog = Catalog(asc)
print(catalog.show(items))
catalog.strategy = desc
print(catalog.show(items))
```

Esto es una forma de inyección de dependencias: el comportamiento se proporciona desde afuera. En Python no hace falta definir una jerarquía de clases para estrategias sencillas. Si una estrategia necesita estado propio, una clase con `__call__` también puede servir.

### Riesgos

-   Las estrategias deben respetar un contrato compatible de entrada y salida.
-   Demasiadas estrategias pequeñas pueden fragmentar la lógica.
-   Si solo hay una regla estable y sencilla, abstraerla puede resultar innecesario.

**Cuándo elegirlo:** cuando hay variantes de un algoritmo que realmente necesitan intercambiarse.

## 6. Observer --- Monitor City Changes

### Concepto

Permite notificar cambios o eventos a múltiples interesados sin que el emisor dependa directamente de su implementación. Útil en interfaces, eventos y cambios de estado.

### Ejemplo de la clase

``` python
subs = {}  # topic -> callbacks


def subscribe(topic, fn):
    subs.setdefault(topic, []).append(fn)


def publish(topic, msg):
    [fn(msg) for fn in subs.get(topic, [])]


subscribe("roads", lambda msg: print("News:", msg))
subscribe("roads", lambda msg: print("TV:", msg))
publish("roads", "New road construction announced.")
```

Salida:

``` text
News: New road construction announced.
TV: New road construction announced.
```

### Funciones y mecanismos relevantes

`dict.setdefault(key, default)` devuelve el valor existente o, si la clave no existe, inserta el valor por defecto y lo devuelve. Así `subscribe` obtiene la lista de callbacks y agrega una función con `append`.

`dict.get(key, default)` devuelve el valor existente o el valor por defecto, pero no inserta una clave nueva. Publicar en un tema sin suscriptores no produce ningún efecto.

Las expresiones `lambda` crean funciones anónimas. Aquí reciben un mensaje e imprimen una salida. El callback se almacena para ejecutarse cuando se publique el evento.

El ejemplo es más precisamente una variante de **publish/subscribe (pub/sub)** con un registro intermediario por temas. En Observer clásico, el sujeto suele mantener directamente sus observadores. Ambos comparten la idea de notificación desacoplada. Es similar conceptualmente a los eventos de `EventEmitter` de Node.js.

### Mejora idiomática

La list comprehension del profesor funciona, pero crea una lista de resultados que no se utiliza. Para efectos secundarios, es más claro un bucle:

``` python
def publish(topic, msg):
    for fn in subs.get(topic, []):
        fn(msg)
```

### Riesgos y comportamiento real

-   La notificación es síncrona: los callbacks se ejecutan uno después de otro, no en hilos separados.
-   Si un callback lanza una excepción, los siguientes no se ejecutan en esta implementación.
-   No existe un mecanismo para cancelar suscripciones; los callbacks pueden permanecer referenciados indefinidamente.
-   Suscribir dos veces la misma función implica ejecutarla dos veces.
-   Las cascadas de eventos dificultan seguir el flujo. Conviene usar nombres claros y logging cuando corresponda.
-   Un handler idempotente puede procesar repetidamente el mismo evento sin acumular efectos no deseados. Es especialmente útil si existe la posibilidad de entregas duplicadas.

## 7. Decorator --- Enhance City Plans

### Concepto

El patrón GoF Decorator añade responsabilidades a un objeto mediante composición, normalmente manteniendo una interfaz compatible. Los decoradores de Python (`@`) son un mecanismo del lenguaje para transformar o reemplazar funciones y clases. Pueden implementar una intención similar, aunque no todo decorador de Python es el patrón GoF.

Útil para caching, logging, autorización, transacciones y reintentos.

``` python
import time
from functools import wraps


def retry(times=3, delay=0.1):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for _ in range(times - 1):
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    time.sleep(delay)
            return fn(*args, **kwargs)  # last attempt
        return wrapper
    return decorator


n = {"x": 0}


@retry(3, 0.01)
def flaky():
    n["x"] += 1
    if n["x"] < 3:
        raise RuntimeError("not yet")
    return "Success"


print(flaky())  # Success
```

### Los tres niveles de funciones

  -------------------------------------------------------------------------------------------------------------
  Función                             Responsabilidad
  ----------------------------------- -------------------------------------------------------------------------
  `retry(times, delay)`               Configura el decorador y devuelve `decorator`

  `decorator(fn)`                     Recibe la función original y devuelve `wrapper`

  `wrapper(*args, **kwargs)`          Ejecuta la lógica adicional cada vez que se llama a la función decorada
  -------------------------------------------------------------------------------------------------------------

La sintaxis `@retry(3, 0.01)` equivale conceptualmente a `flaky = retry(3, 0.01)(flaky)` después de definir la función original. La configuración y la decoración ocurren al definirla; los intentos ocurren al llamarla.

El wrapper conserva acceso a `fn`, `times` y `delay` gracias a los closures. `*args` y `**kwargs` permiten recibir y reenviar argumentos posicionales y nombrados.

### ¿Por qué `range(times - 1)`?

Con `times=3`, el bucle permite dos intentos protegidos por `try/except`. El último intento queda afuera para que, si falla, su excepción se propague al llamador.

  Intento     Contador `n['x']` Resultado
  --------- ------------------- ------------------------------------
  1                           1 RuntimeError; espera 0,01 segundos
  2                           2 RuntimeError; espera 0,01 segundos
  3                           3 Devuelve `Success`

Si cualquier intento anterior tiene éxito, `return` termina inmediatamente el wrapper. El último intento no tiene una espera posterior. `times` representa intentos totales, no reintentos adicionales.

`_` es una variable normal utilizada convencionalmente cuando no interesa su valor. `time.sleep(delay)` suspende el hilo que ejecuta el código durante aproximadamente ese intervalo (en segundos).

### ¿Qué hace `@wraps(fn)`?

`functools.wraps` conserva metadatos de la función original, como `__name__`, `__doc__` y anotaciones, y establece `__wrapped__` para acceder a la función original. Sin él, el nombre visible de la función decorada normalmente sería `wrapper`. No elimina el wrapper ni cambia su lógica.

### ¿Por qué un diccionario `n`?

`flaky` modifica el contenido de un objeto mutable definido fuera de la función. No reasigna la variable `n`, por lo que no necesita `global n`. El contador simula una operación que falla dos veces antes de tener éxito. Una segunda llamada a `flaky()` tendrá éxito inmediatamente porque el contador conserva su estado.

### Riesgos y límites del ejemplo

-   `except Exception` captura demasiados tipos de error para muchos escenarios reales. Conviene reintentar solo fallos transitorios previstos.
-   No valida `times`: con cero o un número negativo todavía ejecuta el intento final. Un contrato razonable exigiría un entero mayor o igual a uno y un delay no negativo.
-   Reintentar operaciones con efectos secundarios puede duplicar pagos, escrituras o envíos. Evaluar idempotencia antes de aplicar el patrón.
-   En redes suele convenir backoff (aumentar la espera) y jitter (variación aleatoria) para evitar reintentos simultáneos.
-   Este wrapper es síncrono; no es una implementación adecuada para funciones `async def` sin adaptaciones.
-   Muchos decoradores apilados pueden ocultar el flujo. Su orden importa.

## 8. Combinación de patrones: reporting pipeline

Ejemplo conceptual de la clase, no una implementación completa:

1.  Singleton: proporciona la configuración compartida.
2.  Factory: selecciona el formateador PDF, HTML o CSV.
3.  Strategy: elige el criterio de ranking para administradores o público general.
4.  Decorator: reintenta escrituras de red cuando corresponde.
5.  Observer: publica `report_ready` para que otros componentes actualicen caché o envíen notificaciones.

El evento debería publicarse cuando el reporte esté realmente listo. Cada patrón resuelve una responsabilidad diferente; no es obligatorio emplearlos todos.

## 9. Otros patrones --- material complementario sugerido por Copilot

Estos patrones no fueron desarrollados en las dos clases compartidas. Se conservan como mapa conceptual para estudiar posteriormente.

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Patrón                  Familia                 Concepto y ejemplo
  ----------------------- ----------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------
  Adapter                 Estructural             Traduce una interfaz a otra esperada. Ej.: adaptar una API externa al contrato interno.

  Composite               Estructural             Trata hojas y grupos de una estructura de árbol mediante una interfaz común. Ej.: archivos y carpetas.

  Proxy                   Estructural             Intermediario que controla el acceso a otro objeto. Ej.: carga diferida o control de permisos.

  Command                 Comportamiento          Encapsula una solicitud para ejecutarla, encolarla o registrarla; puede facilitar deshacer si se diseña para ello.

  Template Method         Comportamiento          Define el esqueleto de un algoritmo en una clase base y permite que subclases personalicen determinados pasos.

  Iterator                Comportamiento          Recorre elementos sin exponer la representación interna. Python lo integra mediante `iter()`, `next()` y generadores.

  State                   Comportamiento          Cambia el comportamiento según el estado interno, sin necesidad de cambiar realmente la clase del objeto. Ej.: pedido pendiente, pagado o enviado.

  Builder                 Creacional              Separa la construcción paso a paso de un objeto complejo de su representación. Ej.: construcción configurable de un reporte.
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 10. Guía rápida para elegir un patrón

  ----------------------------------------------------------------------------------------------------
  Necesidad                                                        Patrón candidato
  ---------------------------------------------------------------- -----------------------------------
  Una sola instancia compartida                                    Singleton

  Ocultar o centralizar la creación                                Factory

  Intercambiar algoritmos                                          Strategy

  Notificar a múltiples interesados                                Observer

  Añadir comportamiento sin modificar la implementación original   Decorator
  ----------------------------------------------------------------------------------------------------

No elegir un patrón por su nombre o por querer aplicarlo: primero identificar el problema. Los patrones aportan vocabulario común y pueden mejorar la mantenibilidad, pero no garantizan menos errores ni mayor eficiencia. Evitar el sobre-diseño y preferir implementaciones pequeñas, claras e idiomáticas.

## 11. Referencias para profundizar

-   [Modelo de datos de Python: `__new__` y `__init__`](https://docs.python.org/3/reference/datamodel.html#object.__new__)
-   [Tipos incorporados: diccionarios](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
-   [Funciones incorporadas: `sorted`, `type`, `super`](https://docs.python.org/3/library/functions.html)
-   [`functools.wraps`](https://docs.python.org/3/library/functools.html#functools.wraps)
-   [Anotaciones de variables --- PEP 526](https://peps.python.org/pep-0526/)
-   [Definición de funciones y decoradores](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)
-   [Threading y locks](https://docs.python.org/3/library/threading.html#lock-objects)

Los ejemplos se basan en el código transcrito de las clases; las explicaciones, matices y alternativas son ampliaciones de estudio. Las referencias se incluyen como material de consulta, no como fuentes verificadas en línea durante esta revisión.
