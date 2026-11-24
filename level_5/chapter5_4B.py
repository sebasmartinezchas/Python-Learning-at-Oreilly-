"""
Los archivos ZIP son binarios, si los quisiéramos leer como texto, obtendríamos un error del tipo UnicodeDecodeError.

Debemos abrir los archivos ZIP en modo binario para poder leerlos correctamente. Por ejemplo:
mode='rb'.

Tipicamente no estarás leyendo archivos en bytes en python sino que usaras librerías específicas según sea el objetivo del
programa.

Sin embargo, algunas veces uno se puede tomar con la necesidad de leer archivos binarios directamente, para lo cual
uno debería estar familiarizado con la lectura de archivos de este tipo.

"""


import hashlib

with open("exercices.zip", mode="rb") as zip_file:
    contents = zip_file.read()

print(type(contents))  # out <class 'bytes'>

print(contents[:20])  # output first 20 bytes of the ZIP file


def get_sha256_hash(
    filename,
):  # Esta función calcula el hash SHA-256 de un archivo dado.
    with open(filename, mode="rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# El problema con esta función es que lee todo el archivo en memoria de una sola vez, lo cual puede ser ineficiente
# o incluso inviable para archivos muy grandes. En un archivo de texto lo leeríamos línea por línea, pero en un archivo binario
# debemos leerlo en bloques.


def get_sha256_hash_chunk(filename, buffer_size=2**10 * 8):
    file_hash = hashlib.sha256()
    with open(filename, mode="rb") as f:
        chunk = f.read(buffer_size)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(buffer_size)
    return file_hash.hexdigest()


# Esencialemte estamos haciendo lo mismo que en la función anterior, pero en lugar de leer todo el archivo de una vez,
# lo leemos en bloques de tamaño buffer_size y vamos actualizando el hash de manera incremental. Esto permite calcular
# el hash de archivos muy grandes sin cargar todo el contenido en memoria.
