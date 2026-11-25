# Patrones de diseño en Python

*Apuntes de la clase de Dr. Chester Ismay ("Apply Common Design Patterns in Python / Understanding Design Patterns"), revisados y ampliados.*

## Qué es un patrón de diseño

Un patrón de diseño es una **solución reutilizable, con nombre, a un problema que se repite** en el diseño de software. No es código para copiar: es una plantilla de cómo organizar responsabilidades.

El catálogo clásico es el libro *Design Patterns* (Gamma, Helm, Johnson y Vlissides, 1994), conocido como **GoF** (*Gang of Four*). Describe 23 patrones en tres familias ([refactoring.guru – catálogo](https://refactoring.guru/design-patterns/catalog)):

| Familia | Resuelve | Patrones de estos apuntes |
|---|---|---|
| **Creacionales** | Cómo se crean los objetos | Singleton, Factory, Builder |
| **Estructurales** | Cómo se combinan objetos y clases | Decorator, Adapter, Composite, Proxy |
| **De comportamiento** | Cómo se reparten responsabilidades y se comunican | Strategy, Observer, Command, Template Method, Iterator, State |

**Idea clave para Python:** muchos patrones GoF se pensaron para C++/Java. En Python, las funciones son objetos de primera clase, los módulos se importan una sola vez y hay *duck typing*. Por eso varios patrones se reducen a pocas líneas o vienen incorporados al lenguaje. Tu clase sigue ese enfoque: implementaciones "mínimas e idiomáticas".

## Metáfora de la clase: el código como ciudad

| Patrón | Metáfora |
|---|---|
| Singleton | La única central eléctrica (en tus notas dice *"one ad only"*: es *"one and only"*) |
| Factory | La oficina de obras que construye según especificación |
| Strategy | Reglas de tránsito intercambiables |
| Observer | El sistema de alertas que avisa a los vecinos |
| Decorator | Agregarle funciones a un edificio sin demolerlo |

---

## 1. Singleton — una sola central eléctrica

**Qué es:** garantiza que una clase tenga una sola instancia y da un punto de acceso global a ella. ✅ Tu definición es correcta.

```python
class Config:
    _instance = None
    settings: dict[str, str]  # anotación para Pylance: el atributo existirá en la instancia

    def __new__(cls):
        if cls._instance is None:
            obj = super().__new__(cls)
            obj.settings = {"env": "prod"}
            cls._instance = obj
        return cls._instance


a = Config()
b = Config()
print(a is b)              # True
print(a.settings["env"])   # prod
```

**Por qué funciona:** `Config()` llama primero a `__new__`, que **crea** el objeto, y después a `__init__`, que lo **inicializa**. Si `__new__` devuelve siempre el mismo objeto, nunca hay un segundo. ([`object.__new__`](https://docs.python.org/3/reference/datamodel.html#object.__new__))

- `super().__new__(cls)` delega en `object.__new__` la creación real del objeto vacío.
- La inicialización está en `__new__` **a propósito**. Si estuviera en `__init__`, se ejecutaría en cada `Config()` y reiniciaría `settings` en cada llamada. La documentación lo dice: si `__new__` devuelve una instancia de `cls`, se llama a `__init__` igual.

### Correcciones y observaciones

1. **`if not cls._instance` → `if cls._instance is None`.** `not` evalúa la *veracidad* del objeto. Si algún día la clase define `__len__` o `__bool__` y la instancia resulta "falsa", se crearía otra. Para comparar con `None`, PEP 8 recomienda `is None` ([PEP 8 – Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations)).
2. **Subclases:** lo probé, y `class Sub(Config): pass` seguido de `Sub()` devuelve **la instancia de `Config`**, no un `Sub`. Pasa porque `cls._instance` se busca por herencia y encuentra la del padre.
3. **No es thread-safe:** dos hilos pueden pasar el `if` a la vez y crear dos instancias. Se resuelve con un `threading.Lock`.

### La alternativa más pythónica: el módulo

Un módulo se ejecuta una sola vez y queda guardado en `sys.modules`. Cada `import` posterior devuelve el mismo objeto ([The import system](https://docs.python.org/3/reference/import.html#the-module-cache)). Por eso un `config.py` con variables ya funciona como singleton, sin clase.

**Riesgos (los de la clase):** dependencias ocultas y tests difíciles. El consejo de la clase es pasar `Config()` explícitamente a quien lo necesite (*inyección de dependencias*) y agregar un *reset hook* para los tests, por ejemplo un método que haga `Config._instance = None`.

---

## 2. Factory — la oficina de obras

**Qué es:** quien pide un objeto expresa **la intención** ("quiero un reporte PDF") y no los detalles del constructor.

```python
class PDF:
    kind = "pdf"

class HTML:
    kind = "html"

REG = {"pdf": PDF, "html": HTML}

def make_report(fmt: str):
    return REG[fmt.lower()]()

print(type(make_report("pdf")).__name__)   # PDF
```

> Tus notas muestran `REG[fmt.lower()]\()&#x20;`: son restos del copiado. Lo correcto es `REG[fmt.lower()]()`.

**Por qué funciona:** en Python **las clases son objetos**, así que se pueden guardar en un diccionario. `REG["pdf"]` devuelve la clase `PDF` y los `()` la instancian.

### Precisión conceptual

La definición de tus notas ("interfaz para crear objetos sin especificar la clase exacta") es la del **Factory Method** de GoF, que usa herencia: una subclase decide qué crear. El código de la clase es otra cosa, una **Simple Factory con registro**: una función más un diccionario. No es un patrón GoF formal, pero es la forma más común en Python. ([refactoring.guru – Factory Method](https://refactoring.guru/design-patterns/factory-method))

### Mejoras

- Con un formato desconocido, `make_report("csv")` lanza `KeyError: 'csv'`, que no explica mucho. Es mejor atraparlo y lanzar `ValueError(f"Formato no soportado: {fmt}")`.
- El registro se puede llenar solo con `__init_subclass__`, como en [modulo-5-metaclases.md](modulo-5-metaclases.md). Es el mismo patrón.

**Riesgo:** que `REG` crezca sin control. Mantenerlo chico o dividirlo por dominio.

---

## 3. Strategy — reglas de tránsito intercambiables

**Qué es:** una familia de algoritmos intercambiables. Quien los usa no sabe cuál le tocó. ✅ Definición correcta.

```python
def asc(items):
    return sorted(items)

def desc(items):
    return sorted(items, reverse=True)

class Catalog:
    def __init__(self, strategy):
        self.strategy = strategy

    def show(self, items):
        return self.strategy(items)

print(Catalog(asc).show([3, 1, 4, 2]))   # [1, 2, 3, 4]
```

**Por qué funciona:** `Catalog` depende de **algo invocable** (*callable*), no de una clase concreta. En Java harían falta una interfaz y una clase por estrategia; en Python alcanza con una función.

**Ya lo usaste sin saberlo:** el `key=` de [`sorted()`](https://docs.python.org/3/library/functions.html#sorted) es Strategy. Le pasás la regla de comparación como función.

**Para Pylance:** podés tipar la estrategia como `Callable[[list[int]], list[int]]` usando [`collections.abc.Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable).

**Riesgo:** demasiadas micro-estrategias fragmentan la lógica. Hay que nombrarlas bien y documentarlas.

---

## 4. Observer — el sistema de alertas

**Qué es:** cuando un objeto cambia, se notifica automáticamente a todos los interesados. ✅ Definición correcta.

```python
subs = {}  # topic -> lista de callbacks

def subscribe(topic, fn):
    subs.setdefault(topic, []).append(fn)

def publish(topic, msg):
    for fn in subs.get(topic, []):
        fn(msg)

subscribe("roads", lambda msg: print("News:", msg))
subscribe("roads", lambda msg: print("TV:", msg))
publish("roads", "New road construction announced.")
```

### Funciones que conviene entender

- [`dict.setdefault(key, default)`](https://docs.python.org/3/library/stdtypes.html#dict.setdefault): si la clave no existe, la crea con `default` y lo devuelve; si existe, devuelve el valor actual. Por eso `.append(fn)` siempre opera sobre una lista.
- [`dict.get(key, default)`](https://docs.python.org/3/library/stdtypes.html#dict.get): devuelve `default` si la clave no existe y **no** la crea. Publicar en un tema sin suscriptores no hace nada y no falla.

### Correcciones

1. **El código de la clase usa `[fn(msg) for fn in ...]`.** Es una list comprehension usada solo por el efecto secundario: arma una lista de `None` que se descarta. No es idiomático. Para efectos, un `for` común, como en el código de arriba.
2. **Precisión conceptual:** esto es **Publish/Subscribe** (pub/sub), una variante de Observer. En el Observer clásico, el *sujeto* guarda su propia lista de observadores y los conoce. Acá hay un intermediario (el diccionario `subs`) con *topics*, y por eso la clase dice *"publishers don't know the listeners"*.
3. **"idem potent"** en tus notas es **idempotent**: un handler idempotente produce el mismo resultado si se ejecuta una o varias veces con el mismo mensaje. Importa porque en sistemas de eventos un mensaje puede llegar duplicado.

**Riesgo:** cascadas difíciles de rastrear, cuando un handler publica otro evento que dispara otro handler. La clase recomienda topics claros.

---

## 5. Decorator — agregar funciones sin demoler

**Qué es:** agrega comportamiento a algo existente sin modificarlo. ✅ Definición correcta.

### ⚠️ Distinción importante

Hay **dos "decorator"** que comparten nombre:

| | Patrón Decorator (GoF) | Decorador de Python (`@`) |
|---|---|---|
| Qué envuelve | Un **objeto**, con otro objeto de la misma interfaz | Una **función o clase**, al definirla |
| Mecanismo | Composición de objetos | Sintaxis: `@d` sobre `f` equivale a `f = d(f)` |

La sintaxis `@` **implementa la idea** del patrón, pero no son lo mismo. El propio PEP 318 reconoce que el nombre generó quejas por no coincidir con el uso del libro GoF ([PEP 318 – On the name 'Decorator'](https://peps.python.org/pep-0318/#on-the-name-decorator)). La clase usa la versión de Python.

### El ejemplo: `retry` (con las funciones que más dudas suelen generar)

```python
import time
from functools import wraps

def retry(times=3, delay=0.1):          # nivel 1: recibe la configuración
    def decorator(fn):                  # nivel 2: recibe la función a decorar
        @wraps(fn)
        def wrapper(*args, **kwargs):   # nivel 3: reemplaza a la función original
            for _ in range(times - 1):
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    time.sleep(delay)
            return fn(*args, **kwargs)  # último intento, fuera del try
        return wrapper
    return decorator
```

**¿Por qué tres funciones anidadas?** Porque `retry` **recibe parámetros**. `@retry(3, 0.01)` primero **ejecuta** `retry(3, 0.01)`, que devuelve `decorator`; recién ese decora a `flaky`. Es decir:

```python
flaky = retry(3, 0.01)(flaky)
```

Un decorador sin parámetros (`@log`) necesita solo dos niveles.

**`*args, **kwargs`:** hacen que `wrapper` acepte cualquier combinación de argumentos y se los pase intactos a `fn`, así el decorador sirve para cualquier función ([tutorial – argumentos arbitrarios](https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists)).

**El truco del bucle:** son `times - 1` intentos **protegidos** (si fallan, espera y reintenta) y un último intento **sin protección**. Si ese también falla, la excepción llega a quien llamó. Así el error no se traga en silencio. Lo probé: con un contador que nunca llega a 3, `flaky()` lanza `RuntimeError: not yet`.

**`@wraps(fn)`:** sin él, `flaky.__name__` valdría `"wrapper"` y se perderían el docstring y otros metadatos. [`functools.wraps`](https://docs.python.org/3/library/functools.html#functools.wraps) los copia de la original. Lo verifiqué: con `wraps`, `flaky.__name__ == "flaky"`.

**¿Por qué `n = {'x': 0}` y no `n = 0`?** Dentro de `flaky`, `n += 1` con un entero crearía una variable local y fallaría con `UnboundLocalError`; haría falta `global n`. `n['x'] += 1` **modifica** el diccionario sin reasignar el nombre `n`, así que no hace falta `global`. Es un atajo de demo, no un estilo recomendable ([FAQ – reglas de variables locales y globales](https://docs.python.org/3/faq/programming.html#what-are-the-rules-for-local-and-global-variables-in-python)).

### Bugs en tus notas

1. **`from turtle import delay`** sobra: no se usa y además lo **tapa** el parámetro `delay` de `retry`. Encima `turtle` importa `tkinter`, que en algunos entornos no está instalado y haría fallar el script. Ruff lo marca como `F401` (import sin usar). Probablemente lo agregó el autocompletado del IDE.
2. **`except Exception`** reintenta ante *cualquier* error, incluso bugs como `TypeError`, que nunca se van a arreglar solos. En código real conviene reintentar solo los errores transitorios: `except (ConnectionError, TimeoutError)`.

**Riesgo:** apilar muchos decoradores oscurece el flujo. Mejor pocos y bien documentados.

---

## 6. Combinando patrones (Step 7 de la clase)

Escenario: un pipeline de reportes.

| Necesidad | Patrón |
|---|---|
| Elegir formateador (pdf, html, csv) | Factory |
| Configuración compartida | Singleton |
| Ranking distinto para admin y público | Strategy |
| Avisar `report_ready` a email y caché | Observer |
| Reintentar escrituras de red inestables | Decorator |

### Heurística rápida

- ¿Solo debe existir uno? → **Singleton**
- ¿Ocultar una construcción compleja? → **Factory**
- ¿Cambiar reglas o algoritmos en tiempo de ejecución? → **Strategy**
- ¿Avisar a varios interesados de un cambio? → **Observer**
- ¿Agregar comportamiento sin tocar el original? → **Decorator**

---

## 7. Otros patrones (sugeridos por Copilot)

Las definiciones de tus notas son correctas; coinciden con las formulaciones GoF. Acá van ampliadas, con su equivalente en Python. Referencia general: [refactoring.guru – catálogo](https://refactoring.guru/design-patterns/catalog).

| Patrón | Idea | En Python |
|---|---|---|
| **Adapter** | Un "enchufe adaptador" entre interfaces incompatibles | Una clase que envuelve a otra y traduce sus métodos. Ej.: adaptar la API de un proveedor de pagos a la interfaz que espera tu sistema |
| **Composite** | Árbol donde hojas y ramas se tratan igual | Carpetas y archivos con el mismo método `size()`; la carpeta suma el de sus hijos recursivamente |
| **Proxy** | Un representante que controla el acceso al objeto real | Carga diferida, control de permisos o caché. [`functools.cached_property`](https://docs.python.org/3/library/functools.html#functools.cached_property) aplica una idea parecida |
| **Command** | Una acción guardada como objeto | Permite colas, historial y *deshacer*. En Python una función o un [`functools.partial`](https://docs.python.org/3/library/functools.html#functools.partial) ya son un "comando" |
| **Template Method** | La clase base fija los pasos; las subclases completan algunos | Clase base con un método `run()` que llama a `_paso()`, marcado con [`@abstractmethod`](https://docs.python.org/3/library/abc.html#abc.abstractmethod) |
| **Iterator** | Recorrer una colección sin conocer su estructura interna | **Incorporado al lenguaje**: `__iter__`/`__next__` y los generadores con `yield` ([Iterator types](https://docs.python.org/3/library/stdtypes.html#iterator-types)). Cada `for` lo usa |
| **State** | El comportamiento cambia según el estado interno | Un objeto delega en otro objeto-estado y lo reemplaza al cambiar. Ej.: un pedido "pendiente → pagado → enviado". Se parece a Strategy, pero acá el que cambia es el propio objeto, no el cliente |
| **Builder** | Construir un objeto complejo paso a paso | Métodos encadenables (`.with_x().with_y().build()`). En Python, los argumentos con nombre y valores por defecto, o un [`dataclass`](https://docs.python.org/3/library/dataclasses.html), muchas veces lo vuelven innecesario |

---

## Cierre (takeaways de la clase)

- Los patrones son **planos con nombre**: aceleran el desarrollo, mejoran la comunicación ("acá usé un Strategy" se entiende al instante) y reducen bugs.
- Elegí el patrón por el **problema recurrente**, no al revés.
- **Evitá la sobreingeniería:** no todo problema necesita un patrón.
- Implementaciones chicas e idiomáticas; **claridad antes que ingenio**.
- Revisá periódicamente si el patrón todavía encaja.

## Erratas menores en las notas originales

`beween` → between · `Stategy` → Strategy · `shoul` → should · `Overgrowwth` → Overgrowth · `Hiddend` → Hidden · `modifing` → modifying · `raning` → ranking · `bluepints` → blueprints · `Desing pattern` → Design patterns · `implementantion` → implementation · `calllers` → callers.
