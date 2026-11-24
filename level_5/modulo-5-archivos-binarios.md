# Módulo 5 — Archivos binarios y bytes en Python

## Lectura de archivos: texto vs binario

```python
# En Python, open() abre archivos en modo texto ('r') por defecto: el contenido se lee como str.
# Para leer bytes hay que especificar mode='rb' explícitamente.
with open("my_file.txt") as f:
    contents = f.read()
    print(f.mode)  # output: 'r'
    print(contents)  # output: contenido del archivo
    print(type(contents))  # output: <class 'str'>


with open("my_file.txt", mode="rb") as f:
    contents = f.read()
    print(f.mode)  # output: 'rb'
    print(contents)  # output: contenido del archivo en bytes
    print(type(contents))  # output: <class 'bytes'>


data = b"Hello there!\xe2\x80\x99s"
print(data)  # output: b'Hello there!\xe2\x80\x99s'
print(type(data))  # output: <class 'bytes'>
print(
    data.decode()
)  # output: Hello there!'s  (usa el encoding del sistema; no portable)
print(data.decode("utf-8"))  # output: Hello there!'s

# Cuando abres un archivo en Python se considera buena práctica especificar el encoding del archivo.
# En diferentes sistemas operativos se usa un encoding diferente.
# En Windows se usa cp1252 y en Linux/MacOS se usa utf-8.
# Los bytes en una diferente codificación pueden ser decodificados a diferentes caracteres.
# with open('my_file.txt', encoding='utf-8') as f:
```

## Archivos ZIP y hashing SHA-256

```python
"""
Los archivos ZIP son binarios. Debemos abrirlos en modo binario (mode='rb')
para poder leerlos correctamente. Si los abriéramos como texto, el contenido
no sería texto válido en ningún encoding y obtendríamos un UnicodeDecodeError.

Típicamente no estarás leyendo archivos en bytes en Python sino que usarás
librerías específicas según sea el objetivo del programa.

Sin embargo, algunas veces uno se puede encontrar con la necesidad de leer
archivos binarios directamente, para lo cual uno debería estar familiarizado
con la lectura de archivos de este tipo.
"""

import hashlib

with open("exercices.zip", mode="rb") as zip_file:
    contents = zip_file.read()

print(type(contents))  # out <class 'bytes'>
print(contents[:20])   # output first 20 bytes of the ZIP file


def get_sha256_hash(filename):
    """Calcula el hash SHA-256 de un archivo dado (carga todo en memoria)."""
    with open(filename, mode="rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# El problema con esta función es que lee todo el archivo en memoria de una sola vez,
# lo cual puede ser ineficiente o incluso inviable para archivos muy grandes.
# En un archivo de texto lo leeríamos línea por línea, pero en un archivo binario
# debemos leerlo en bloques.


def get_sha256_hash_chunk(filename, buffer_size=2**10 * 8):  # buffer_size = 8192 bytes = 8 KB
    """Calcula el hash SHA-256 leyendo el archivo en bloques (eficiente para archivos grandes)."""
    file_hash = hashlib.sha256()
    with open(filename, mode="rb") as f:
        chunk = f.read(buffer_size)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(buffer_size)
    return file_hash.hexdigest()

# Esencialmente estamos haciendo lo mismo que en la función anterior, pero en lugar de leer
# todo el archivo de una vez, lo leemos en bloques de tamaño buffer_size y vamos actualizando
# el hash de manera incremental. Esto permite calcular el hash de archivos muy grandes
# sin cargar todo el contenido en memoria.
```
