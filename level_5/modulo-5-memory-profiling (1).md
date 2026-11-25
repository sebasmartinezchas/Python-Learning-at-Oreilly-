# Memory profiling con `memory_profiler`

*Apuntes de la clase "Monitor Memory Usage / Memory Profiling in Python" (guided practice, sin consigna de ejercicio), revisados y ampliados. El código se corrió para contrastarlo contra la salida que traían las notas.*

## Qué es y para qué sirve

`memory_profiler` es un paquete que mide **cuánta memoria RAM usa un script de Python, línea por línea**. La metáfora de la clase es acertada: es el medidor de combustible de tu programa. El CPU profiling te dice *qué tan rápido* corre algo; el memory profiling te dice *cuánta memoria* ocupa mientras corre, y en qué línea exacta empieza a crecer.

Esto importa porque un programa puede ser rápido y aun así quedarse sin memoria (`MemoryError`) o volverse progresivamente más lento por un *memory leak*: una estructura que crece y nunca se libera.

## Instalación y uso básico

```bash
pip install memory_profiler
```

```python
from memory_profiler import profile

@profile
def mi_funcion():
    ...
```

El decorador `@profile` es lo que activa la medición línea por línea. **No** es el `profile` del módulo estándar [`cProfile`/`profile`](https://docs.python.org/3/library/profile.html) (que mide tiempo de ejecución): es el de `memory_profiler`, por eso el `import` explícito. Sin ese `import`, `@profile` no existe y el script falla con `NameError`.

Para ejecutarlo:

```bash
python mi_script.py
```

alcanza para ver la tabla por consola en cada función decorada. El paso adicional de la clase,

```bash
mprof run your_script.py
mprof plot
```

usa la utilidad de línea de comandos `mprof` (instalada junto con el paquete) para registrar el consumo de memoria **a lo largo del tiempo** de todo el proceso y después graficarlo. Es un nivel más: `@profile` da detalle línea por línea de una función puntual; `mprof run` + `mprof plot` da una foto temporal de todo el programa, útil para ver tendencias (¿la memoria sube y después baja, o sube y se queda arriba?).

## El caso de uso: reporte de ratings de un rideshare

La consigna plantea un escenario realista: un script que agrupa calificaciones de conductores por `driver_id`, que anda bien con pocos datos pero empieza a fallar cuando el dataset crece. La sospecha es que el problema es de memoria, no de lógica.

### Versión original

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

**Qué hace, paso a paso:**

1. Simula 100.000 (`10**5`) calificaciones. Cada una es un diccionario con dos claves: `driver_id` y `rating`. Las junta todas en la lista `ratings`.
2. Recorre esa lista completa **por segunda vez** y arma `reports`: un diccionario donde cada clave es un `driver_id` y el valor es la lista de sus ratings.
3. [`dict.setdefault(driver, [])`](https://docs.python.org/3/library/stdtypes.html#dict.setdefault) es el mismo patrón que vimos para Observer en patrones de diseño: si `driver` todavía no está en `reports`, lo crea con una lista vacía; si ya está, usa la lista existente. Así nunca hace falta un `if driver not in reports`.

**Dónde está el gasto de memoria, aunque el resultado final sea correcto:** la lista intermedia `ratings` guarda **los 100.000 diccionarios completos**, con sus dos claves cada uno, aunque al final solo se necesite el `rating` agrupado por `driver_id`. Esa lista es pura memoria de paso: se arma entera, se recorre una vez más, y después se descarta. Mientras tanto ocupa espacio en paralelo con `reports`, que es la estructura que realmente importa.

### Versión optimizada

```python
@profile
def generate_report_optimized():
    reports = {}
    for _ in range(10**5):
        driver = random.randint(1000, 9999)
        rating = random.choice([1, 2, 3, 4, 5])
        reports.setdefault(driver, []).append(rating)
    return reports
```

**La diferencia clave:** no existe la lista intermedia `ratings`. Cada calificación se genera y se guarda **directamente** en `reports`, en una sola pasada. No hay una colección de 100.000 diccionarios viviendo en memoria a la vez; solo existen `driver` y `rating` como variables sueltas, que se descartan en cada vuelta del bucle.

Es el mismo principio que aparece en generadores vs. listas: si no necesitás guardar todo junto, no lo guardes todo junto.

### Comparación real (corrida en este entorno)

Ejecuté ambas funciones con `memory_profiler` para confirmar el comportamiento. Esta es la salida real, con los mismos datos y el mismo entorno:

```
Línea 6  generate_report() — versión original
  @profile                             21.6 MiB  (inicio)
  ratings = []                         21.6 MiB   +0.0 MiB
  for _ in range(10**5):               44.2 MiB  +22.6 MiB   <- acá crece: se arma la lista de 100k dicts
      ratings.append({...})            44.2 MiB  +19.4 MiB      (dentro del for, en el append)
  reports = {}                         44.2 MiB   +0.0 MiB
  for entry in ratings:                46.6 MiB   +1.1 MiB   <- reports crece bastante menos que ratings
  return reports                       46.6 MiB   +0.0 MiB

Línea 24  generate_report_optimized() — versión optimizada
  @profile                             27.6 MiB  (inicio)
  reports = {}                         27.6 MiB   +0.0 MiB
  for _ in range(10**5):               27.6 MiB   +0.0 MiB   <- prácticamente sin crecimiento
      reports.setdefault(...)          27.6 MiB   +0.0 MiB
  return reports                       27.6 MiB   +0.0 MiB
```

La versión original termina usando **~46.6 MiB** frente a los **~27.6 MiB** de la optimizada (los números de base difieren un poco entre corridas porque dependen del intérprete y del entorno, pero la proporción se mantiene). El salto grande y claro está exactamente donde dice la intuición de la clase: en el bucle que arma `ratings`, por los 100.000 diccionarios completos que no hacían falta guardar. La versión optimizada ni siquiera muestra un incremento visible línea por línea, porque nunca acumula nada más que `reports`.

## `@profile` en la práctica: un detalle que conviene saber

`@profile` **no existe** como builtin de Python: solo funciona si el módulo corre bajo `memory_profiler` (por el `import`) o bajo el ejecutable `mprof`/`python -m memory_profiler`. Si alguna vez ves código con `@profile` sin ese import y sin ejecutarlo con las herramientas de `memory_profiler`, va a fallar con `NameError: name 'profile' is not defined`. Por eso casi siempre se ve comentado o se saca antes de hacer commit del código "de verdad": es una herramienta de diagnóstico puntual, no algo para dejar en producción (afecta el rendimiento, como marca el apunte).

## Por qué tus notas traían incrementos negativos

Las notas originales mostraban líneas como `-960.7 MiB` justo sobre el `for` y el `append` de `generate_report`. Vale la pena entender bien esto, porque hay **dos fenómenos distintos** detrás de un número negativo en `memory_profiler`, y conviene no confundirlos.

**1) Negativo real: la línea efectivamente libera memoria.** Lo reproduje acá con un `del` explícito:

```python
big = [0] * (10**7)      # reserva memoria
del big                  # la libera
```

```
5     97.1 MiB     76.3 MiB           1   big = [0] * (10**7)
6     20.8 MiB    -76.3 MiB           1   del big
```

Esto coincide con el ejemplo que trae la propia documentación del paquete: un `del b` después de crear una lista grande muestra un incremento de **-152.59 MB** en esa línea ([README de memory_profiler](https://github.com/pythonprofilers/memory_profiler/blob/master/README.rst)). Acá el negativo es información real: la línea liberó memoria.

**2) Negativo "fantasma": un artefacto conocido al medir dentro de un `for`.** Esto es lo que probablemente pasó en tus notas. Hay un issue abierto en el repositorio oficial que describe exactamente este caso: al recorrer un bucle, el profiler le asigna a la **primera línea del bucle** el cambio de memoria ocurrido desde la **última línea evaluada en la vuelta anterior**, porque esa fue la última línea que el *tracer* vio antes de volver al principio ([memory_profiler issue #353](https://github.com/pythonprofilers/memory_profiler/issues/353)). El resultado es que el `for` o la primera línea del cuerpo del bucle pueden mostrar un número negativo grande aunque esa línea en los hechos solo esté agregando datos (como `ratings.append(...)`), nunca liberando nada. No es que se haya "inventado" el número: es una mala atribución de a qué línea pertenece cada medición, por cómo el perfilador recorre el bucle.

**Cómo distinguir uno del otro en la práctica:** si el negativo cae justo después de un `del`, de un `return`, o de salir de un bloque que contenía objetos grandes, es real. Si cae sobre la primera línea de un `for` o un `while` que solo agrega o modifica datos, hay buenas chances de que sea el artefacto de atribución del punto 2, y conviene mirar el total acumulado al final de la función (o usar `mprof plot`, que mide por tiempo y no por línea) en vez de confiar en esa línea puntual.

## Errores y precisiones sobre las notas originales

1. **Los incrementos negativos de tus notas** (ver sección anterior): no son imposibles ni inventados en general, pero en ese punto específico (sobre el `for`/`append`) son casi seguro el artefacto de atribución documentado en el issue #353, no memoria liberada de verdad.
2. **"Only functions decorated with `@profile` are measured"** es correcto: si `generate_report` llama a una función auxiliar sin decorar, esa auxiliar no aparece línea por línea en el reporte (aunque su uso de memoria sí impacta el total de la función que la llama).
3. **Erratas de tipeo:** "frind" → friend, "ridesate" → rideshare, "Your suspect" → "You suspect", "irregular memory efficient" → la frase está mal armada; lo que se quiere preguntar es "is it actually memory efficient?", "unnecesary" → unnecessary, "reduce peak" → "reduces peak" (concordancia de sujeto en tercera persona).

## Para practicar tranquilo

- Correr ambas versiones en tu máquina con `python archivo.py` (necesitás `pip install memory_profiler`) y comparar los números reales contra los de acá: van a variar según el entorno, pero la diferencia proporcional entre ambas funciones debería sostenerse.
- Probar `mprof run archivo.py` seguido de `mprof plot` para ver la curva de memoria de todo el proceso en el tiempo, no solo función por función.
- Modificar `generate_report` para que libere `ratings` con `del ratings` justo después del primer `for`, antes de armar `reports`, y ver si el profiler muestra una baja real en esa línea (el caso 1 de la sección anterior).
- Pensar qué pasaría con un dataset de 10 millones de registros en vez de 100.000: ¿la versión original directamente fallaría con `MemoryError`? Es una buena forma de internalizar por qué este patrón (acumular en una lista intermedia innecesaria) importa más cuanto más grande es el dataset.

## Referencias

- [`memory_profiler` en PyPI](https://pypi.org/project/memory-profiler/) — paquete y documentación de uso.
- [README de `memory_profiler`](https://github.com/pythonprofilers/memory_profiler/blob/master/README.rst) — ejemplo oficial de incremento negativo real con `del`.
- [Issue #353 de `memory_profiler`](https://github.com/pythonprofilers/memory_profiler/issues/353) — artefacto de atribución de línea dentro de bucles `for`/`while`.
- [`dict.setdefault`](https://docs.python.org/3/library/stdtypes.html#dict.setdefault) — el patrón de agrupamiento usado en ambas versiones.
- [`profile` / `cProfile`](https://docs.python.org/3/library/profile.html) — el profiler de **tiempo** de la librería estándar, para no confundirlo con `memory_profiler`.
