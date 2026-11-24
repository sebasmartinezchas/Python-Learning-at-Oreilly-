# Metaclases — Registro de plugins

*Apuntes de la clase de Dr. Chester Ismay, módulo 5, revisados y ampliados.*

## Qué es una metaclase

Una metaclase es **la clase de una clase**. Así como un objeto es instancia de una clase, una clase es instancia de su metaclase. La metaclase por defecto es `type`.

```python
type(VideoPlugin)   # PluginMeta
type(PluginMeta)    # type
type(type)          # type  -> type es su propia metaclase; ahí termina la cadena
```

Analogía de la clase: la metaclase es el *director de casting*. Los actores (instancias) interpretan roles (clases), pero el director decide cómo entra cada rol a la producción.

## Caso de uso: registro automático de plugins

Queremos que toda subclase de `Plugin` quede registrada sola, sin que el desarrollador tenga que llamar a ninguna función `register()`.

```python
plugin_registry = {}


class PluginMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if bases:  # la base se define sin padres explícitos -> bases == ()
            plugin_registry[name] = cls  # clave: nombre / valor: la clase


class Plugin(metaclass=PluginMeta):
    pass


class VideoPlugin(Plugin):
    pass


class AudioPlugin(Plugin):
    pass


print(plugin_registry)
# {'VideoPlugin': <class '__main__.VideoPlugin'>,
#  'AudioPlugin': <class '__main__.AudioPlugin'>}
```

- `cls` es la clase que se está creando, no una instancia de ella.
- Cada subclase aparece en el registro **en el momento en que se define**.
- Las subclases no declaran `metaclass=`: **la metaclase se hereda** de la base. Por eso basta con declararla una vez. ([Determining the appropriate metaclass](https://docs.python.org/3/reference/datamodel.html#determining-the-appropriate-metaclass))

### Correcciones al ejemplo original

1. **Saltear la base por nombre (`if name != "Plugin"`) es frágil**: una subclase llamada `Plugin` en otro módulo no se registraría. Es más robusto mirar `bases`: la base llega con `()` y las subclases con `(Plugin,)`.
2. **Usar `name` como clave pisa entradas sin avisar**: dos plugins con el mismo nombre en módulos distintos se sobrescriben. Para algo serio conviene `f"{cls.__module__}.{cls.__qualname__}"` como clave, o lanzar un error si ya existe.

## `__new__` vs `__init__` en una metaclase

La clase lo resumía como *"`__init__` intercepta la creación de la clase"* y *"la metaclase controla si la clase siquiera existe"*. Es impreciso:

| Método | Cuándo corre | Para qué sirve |
|---|---|---|
| `__new__` | **Antes** de que la clase exista; es el que la crea | Modificar namespace, bases o nombre antes de crearla |
| `__init__` | **Después**: recibe la clase ya creada | Registrar, validar, agregar atributos |

Si `__init__` lanza una excepción, la sentencia `class` falla y el nombre no queda definido, así que puede "vetar" la clase. Pero no la intercepta antes de que se cree.

## Proceso completo de creación de una clase

1. Se determina la metaclase (por defecto `type`).
2. Se prepara el namespace con `__prepare__`.
3. Se ejecuta el cuerpo de la clase dentro de ese namespace.
4. Se llama `metaclase(name, bases, namespace)`, que dispara `__new__` y después `__init__`.

Docs: [Customizing class creation](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation) · [Creating the class object](https://docs.python.org/3/reference/datamodel.html#creating-the-class-object)

## Errores comunes

- Olvidarse de declarar `metaclass=PluginMeta` en la base: no se registra nada.
- Confundir el `__init__` de las instancias con el `__init__` de la metaclase, que inicializa clases.
- Sobrescribir `__new__` cuando alcanza con `__init__`.
- **Conflicto de metaclases**: si una clase hereda de dos bases con metaclases distintas y no relacionadas (por ejemplo `PluginMeta` y `ABCMeta`), Python lanza `TypeError: metaclass conflict`. Es la limitación práctica más grande de este enfoque.

Para depurar, agregá un print en la metaclase: `print(f"Registering class: {name}, bases={bases}")`.

## Alternativa moderna: `__init_subclass__` (Python 3.6+, PEP 487)

Para registrar o validar subclases **no hace falta una metaclase**:

```python
class Plugin:
    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.registry[cls.__name__] = cls
```

- La base no se registra a sí misma: el método se llama solo cuando se define una subclase.
- No hay conflicto de metaclases.
- El código es más simple y explícito.

Docs: [`object.__init_subclass__`](https://docs.python.org/3/reference/datamodel.html#object.__init_subclass__) · [PEP 487](https://peps.python.org/pep-0487/)

## ¿Quién usa este patrón en frameworks reales?

- **Django**: sigue usando una metaclase (`ModelBase`) para los modelos. ([código fuente](https://github.com/django/django/blob/main/django/db/models/base.py))
- **Flask**: `MethodView` usaba la metaclase `MethodViewType`; en las versiones actuales lo hace con `__init_subclass__`.
- **SQLAlchemy 2.0**: `DeclarativeBase` usa `__init_subclass__` y no metaclases. Reemplaza al viejo `declarative_base()`, que se basaba en `DeclarativeMeta`. ([docs SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html))

## Regla práctica

- **Registrar o validar subclases** → `__init_subclass__`.
- **Metaclase** → solo para lo que únicamente ella puede hacer: modificar el namespace antes de crear la clase (`__new__`, `__prepare__`) o cambiar cómo se comporta la clase como objeto.