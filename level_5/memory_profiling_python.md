# Monitor Memory Usage — Memory Profiling in Python

Apuntes de la ruta Python de O’Reilly. Basados en las notas y mediciones de la práctica guiada; las aclaraciones técnicas y ampliaciones se identifican en el texto.

## 1. Objetivo

Analizar el consumo de memoria de un programa, localizar estructuras innecesarias y refactorizar sin alterar el resultado lógico. Aunque la introducción menciona funciones memoizadas, este ejemplo no utiliza memoización: estudia la agrupación de datos y la eliminación de una lista intermedia.

`memory_profiler` es un paquete externo que permite observar la memoria del proceso y asociar mediciones a líneas de funciones decoradas. El backend habitual mide RSS (resident set size), es decir, memoria residente del proceso, no exclusivamente los objetos Python de una línea. El paquete no está en mantenimiento activo; para proyectos nuevos también conviene conocer `tracemalloc`, de la biblioteca estándar.

## 2. Instalación y ejecución

Con el entorno virtual activado en PowerShell:

```powershell
python -m pip show memory-profiler
python -m pip install memory-profiler
```

Para un archivo llamado `ejemplo.py` con `from memory_profiler import profile` y funciones decoradas:

```powershell
python ejemplo.py
python -m memory_profiler ejemplo.py
```

Ambas formas permiten obtener el informe cuando se importa y aplica el decorador. En Jupyter, `!python -m memory_profiler ejemplo.py` ejecuta el comando en una shell; en PowerShell no se utiliza `!`.

### Perfil temporal

```powershell
mprof run python ejemplo.py
mprof plot
```

Para graficar puede ser necesario instalar `matplotlib`. `mprof` registra muestras de memoria a lo largo del tiempo; no es lo mismo que el informe línea por línea. No necesita decorar funciones para medir el proceso. Un muestreo puede perder picos muy breves. Para comparar funciones, ejecutar cada una en un proceso nuevo.

## 3. Escenario de la práctica

Una empresa de viajes necesita agrupar las calificaciones de sus conductores. Se simulan 100.000 viajes, con identificadores entre 1000 y 9999 (9000 posibles conductores) y calificaciones enteras de 1 a 5. El resultado es un diccionario que relaciona cada conductor con una lista de calificaciones. No calcula todavía promedios ni otros indicadores.

## 4. Implementación original del profesor

```python
import random
from memory_profiler import profile


@profile
def generate_report():
    ratings = []
    for _ in range(10**5):
        ratings.append(
            {
                "driver_id": random.randint(1000, 9999),
                "rating": random.choice([1, 2, 3, 4, 5]),
            }
        )
    reports = {}

    for entry in ratings:
        driver = entry["driver_id"]
        reports.setdefault(driver, []).append(entry["rating"])
    return reports
```

### Construcción paso a paso

- `@profile`: envuelve la función para instrumentar su ejecución.
- `ratings = []`: crea una lista vacía que conservará todos los registros.
- `range(10**5)`: produce 100.000 iteraciones sin construir una lista de enteros. `_` indica por convención que no necesitamos el valor de la variable.
- `random.randint(1000, 9999)`: ambos extremos están incluidos.
- `random.choice([1, 2, 3, 4, 5])`: selecciona una calificación; la lista literal se construye en cada iteración.
- `ratings.append({...})`: crea y conserva un diccionario por viaje. Al terminar hay 100.000 diccionarios en la lista.
- `reports = {}`: crea el diccionario de agrupación.
- `for entry in ratings`: recorre los registros ya generados. `entry` referencia cada diccionario, no una copia.
- `entry["driver_id"]`: obtiene la clave de agrupación.
- `reports.setdefault(driver, []).append(entry["rating"])`: obtiene o crea la lista del conductor y agrega la calificación.
- `return reports`: devuelve el resultado agrupado, no la lista original.

### Entender `setdefault()`

```python
reports = {}
reports.setdefault(1234, []).append(5)
reports.setdefault(5678, []).append(3)
reports.setdefault(1234, []).append(4)
# {1234: [5, 4], 5678: [3]}
```

`dict.setdefault(key, default)` devuelve el valor existente si la clave está presente. Si no existe, inserta el valor por defecto y lo devuelve. `append()` modifica esa misma lista. El valor por defecto `[]` se evalúa incluso si la clave ya existe, aunque en ese caso no se inserta. `append()` devuelve `None`, no la lista.

Una alternativa idiomática (ampliación) es `collections.defaultdict(list)`, que crea una lista al acceder a una clave ausente. No es necesaria para entender el ejemplo original.

## 5. Interpretación del informe original

Extracto de las mediciones aportadas en los apuntes:

| Línea / operación | Mem usage | Increment | Occurrences |
|---|---:|---:|---:|
| Entrada de función | 28.6 MiB | 28.6 MiB | 1 |
| `ratings = []` | 28.6 MiB | 0.0 MiB | 1 |
| Primer `for` | 51.2 MiB | -960.7 MiB | 100001 |
| `ratings.append(` | 51.2 MiB | -1907.3 MiB | 200000 |
| `reports = {}` | 51.2 MiB | 0.0 MiB | 1 |
| Segundo `for` | 53.2 MiB | 0.0 MiB | 100001 |
| `setdefault(...).append(...)` | 53.2 MiB | 2.0 MiB | 100000 |
| `return reports` | 53.2 MiB | 0.0 MiB | 1 |

- **Line #**: número de línea del archivo.
- **Mem usage**: máximo de memoria observado y atribuido a esa línea en el informe, no el tamaño del objeto creado por ella.
- **Increment**: diferencias acumuladas atribuidas a la línea por el profiler. En bucles y expresiones multilínea pueden aparecer cifras contraintuitivas por la contabilidad de eventos de trazado; no interpretar como una liberación real de gigabytes ni como el tamaño de una asignación. Sin conocer la versión y los eventos exactos no se puede determinar la causa concreta de cada cifra negativa.
- **Occurrences**: cantidad de eventos de ejecución registrados para la línea. El `for` puede aparecer 100001 veces por la comprobación final; una expresión multilínea puede generar varios eventos por iteración.
- **Line Contents**: código fuente correspondiente.

MiB = 1.048.576 bytes; MB = 1.000.000 bytes.

La memoria observada pasa de 28.6 a 51.2 MiB durante la generación y a 53.2 MiB durante la agrupación. No hay evidencia aquí de una fuga de memoria: la lista crece porque el código conserva deliberadamente los registros. Al terminar la función, las referencias locales pueden liberarse, aunque el proceso no necesariamente devuelve inmediatamente toda esa memoria al sistema operativo.

## 6. Implementación optimizada del profesor

```python
@profile
def generate_report_optimized():
    reports = {}
    for _ in range(10**5):
        driver = random.randint(1000, 9999)
        rating = random.choice([1, 2, 3, 4, 5])
        reports.setdefault(driver, []).append(rating)
    return reports


if __name__ == "__main__":
    # generate_report()
    generate_report_optimized()
```

La función crea primero el diccionario final. En cada iteración genera un identificador y una calificación, y los incorpora directamente al grupo correspondiente. No crea un diccionario por viaje ni conserva una lista de registros originales. Las variables locales `driver` y `rating` se reasignan en cada iteración; las calificaciones agrupadas sí permanecen en `reports`.

`if __name__ == "__main__":` permite ejecutar la práctica al lanzar el archivo directamente, sin ejecutar automáticamente las funciones al importarlo como módulo. Para medir la versión original, intercambiar las llamadas y ejecutar nuevamente en otro proceso.

## 7. Comparación de resultados

| Medición | Original | Optimizada |
|---|---:|---:|
| Memoria inicial | 28.6 MiB | 28.7 MiB |
| Máximo observado en el informe | 53.2 MiB | 31.4 MiB |
| Diferencia respecto de la base | 24.6 MiB | 2.7 MiB |

Reducción total observada: `(53.2 - 31.4) / 53.2` = 41.0%. Reducción de memoria adicional: `(24.6 - 2.7) / 24.6` = 89.0%. Son aproximaciones basadas en las mediciones aportadas, no tamaños exactos de objetos ni garantías universales.

Ambas versiones generan y agrupan N calificaciones. La original realiza dos recorridos de N elementos y la optimizada uno; ambas tienen tiempo esperado O(N), suponiendo operaciones de diccionario de coste promedio constante. Ambas conservan O(N) memoria para el resultado, pero la optimizada elimina la lista intermedia de O(N) registros. Reduce factores constantes y memoria auxiliar, no la clase de complejidad espacial total.

## 8. Comprobar la equivalencia funcional

Las funciones producen datos aleatorios, por lo que dos llamadas independientes no tienen por qué devolver el mismo diccionario. Para una prueba reproducible, usar la misma semilla antes de cada llamada (ampliación):

```python
random.seed(42)
original = generate_report()
random.seed(42)
optimized = generate_report_optimized()
assert original == optimized
assert sum(len(ratings) for ratings in optimized.values()) == 100_000
```

La primera prueba comprueba que ambas funciones agrupan los mismos datos bajo las mismas condiciones; la segunda comprueba que no se perdieron calificaciones. Esta prueba es funcional, no una comparación justa de memoria: mantiene ambos resultados vivos. Para medir memoria, usar procesos separados.

## 9. Procesamiento incremental y posibles mejoras

La optimización consiste en procesar cada registro cuando llega, en lugar de materializar todos los registros antes de agruparlos. Es el mismo principio que puede aplicarse a un archivo CSV leído línea por línea o a un generador. Aquí no se necesita `yield` porque la generación y el consumo ocurren en el mismo bucle.

Si el requisito fuera únicamente calcular promedios por conductor, se podrían guardar suma y cantidad por conductor en vez de todas las calificaciones. Eso reduciría el almacenamiento a O(D), donde D es el número de conductores distintos. Sin embargo, cambiaría el resultado y no sería un reemplazo equivalente si necesitamos conservar cada calificación.

## 10. Buenas prácticas y limitaciones

- Medir antes y después de optimizar, con entradas comparables y procesos nuevos.
- El profiling añade overhead: no utilizar sus tiempos como benchmark representativo.
- `@profile` delimita el informe línea por línea, pero el RSS incluye memoria de todo el proceso, incluso llamadas a funciones no decoradas.
- `time.sleep()` no invalida por sí mismo las mediciones de memoria; puede afectar duración y muestreo temporal.
- Un pico de memoria no demuestra una fuga. Investigar crecimiento sostenido y referencias retenidas.
- `tracemalloc` permite rastrear asignaciones de memoria de Python y comparar snapshots; no mide necesariamente toda la memoria nativa del proceso.
- Para estudiar tiempos de ejecución, utilizar herramientas específicas como `timeit` o `cProfile` según el objetivo.

## 11. Referencias para profundizar

- [memory-profiler en PyPI](https://pypi.org/project/memory-profiler/)
- [Repositorio de memory_profiler](https://github.com/pythonprofilers/memory_profiler)
- [Python: dict.setdefault](https://docs.python.org/3/library/stdtypes.html#dict.setdefault)
- [Python: random](https://docs.python.org/3/library/random.html)
- [Python: defaultdict](https://docs.python.org/3/library/collections.html#collections.defaultdict)
- [Python: tracemalloc](https://docs.python.org/3/library/tracemalloc.html)

Referencias sugeridas, no consultadas en línea durante esta revisión. Las cifras proceden de los apuntes del estudiante; no se reprodujo el profiling.
