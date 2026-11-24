# En Python, open() abre archivos en modo texto ('r') por defecto: el contenido se lee como str.
# Para leer bytes hay que especificar mode='rb' explícitamente..
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
print(data.decode("utf-8"))  # output: Hello there!’s

# Cuando abres un archivo en python se considera buena practica expecificar el encoding del archivo.
# with open('my_file.txt', encoding='utf-8') as f:
# En diferenes sistemas operativos se usa un encoding diferente.
# En Windows se usa cp1252 y en Linux /MacOS se usa utf-8.
# Los bytes en una diferente codificación pueden ser decodificados a diferentes caracteres.
