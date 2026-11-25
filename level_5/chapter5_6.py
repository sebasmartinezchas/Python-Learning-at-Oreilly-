"""
Dr Chester Ismay

Apply Common Design Patterns in Python / Understanding Design Patterns

¿Qué son los patrones de diseño y cómo se aplican en Python?
Un patrón de diseño es una solución reutilizable a un problema común que ocurre en el diseño de software.
En Python, los patrones de diseño se pueden aplicar utilizando clases, funciones y módulos para estructurar el código de manera eficiente y,
mantenible.

Algunos patrones de diseño comunes en Python incluyen:
- Singleton: Garantiza que una clase tenga solo una instancia y proporciona un punto de acceso global a ella.
 # Use when there must be only one instance of an object.
 * Good for:
 - A central configuration manager
 - A logging service
 - A database connection pool
 * Risks:
 - Can hide dependencies and make the system harder to manage.

- Factory: Proporciona una interfaz para crear objetos sin especificar la clase exacta del objeto que se creará.
 # Use when the details of an object should be hidden.
 * Good for:
 - Choosing beween different payment providers.
 - Loading various file formats
 - Managing plugins
 * Risks:
 - Adding unnecessary complexity and maintenance overhead.

- Observer: Permite que un objeto notifique a otros objetos sobre cambios en su estado.
 # Use when one change needs to be broadcasted to multiple objects.
 * Good for:
 - Event systems
 - Real time UI updates
 - State changes notifications
 * Risks:
 - If not managed with clear naming and good records, broadcasting too many alerts can lead to confusion.

 - Strategy: Define una familia de algoritmos, encapsula cada uno y los hace intercambiables.
 # Use when the rules of algorithms should be swappable.
 * Good for:
 - Swapping out discounts rules
 - Data processing steps
 - Ranking systems
 * Risks:
 - Creating small, individual strategies can make the system harder to maintain.

 - Decorator: Permite agregar comportamiento a un objeto de manera dinámica sin modificar su estructura.
 # Use when you need to add features without rebuilding.
 * Good for:
 - Adding caching, logging, security checks.
 - Adding transaction management to existing code.

 * Risks:
 - Too many decorators can make the code difficult to understand and maintain.

  `` Los de arriba son los mencionados por el Dr Chester Ismay``
  
  Otros patrones de diseño son:

- Adapter: Permite que interfaces incompatibles trabajen juntas al convertir la interfaz de una clase en otra que el cliente espera.

- Composite: Permite componer objetos en estructuras de árbol para representar jerarquías parte-todo, tratando de manera uniforme a los objetos individuales y a las composiciones de objetos.

- Proxy: Proporciona un sustituto o representante de otro objeto para controlar el acceso a él.

- Command: Encapsula una solicitud como un objeto, permitiendo parametrizar clientes con diferentes solicitudes, encolar o registrar solicitudes y soportar operaciones deshacer.

- Template Method: Define el esqueleto de un algoritmo en una operación, dejando algunos pasos a ser implementados por subclases.

- Iterator: Proporciona una forma de acceder secuencialmente a los elementos de un objeto agregado sin exponer su representación subyacente.

- State: Permite a un objeto alterar su comportamiento cuando su estado interno cambia, pareciendo que cambia su clase.

- Builder: Separa la construcción de un objeto complejo de su representación, permitiendo crear diferentes representaciones d
  el objeto utilizando el mismo proceso de construcción.
"""
