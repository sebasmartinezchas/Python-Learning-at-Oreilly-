# Datos binarios y codificación — `bytes`, `encode`, `decode`

*Apuntes del módulo 5 ("Work with Binary Files and Encoding in Python"), revisados y ampliados.*

## Idea central

En Python, los datos binarios se representan con el tipo `bytes` y el texto con `str`. Para pasar de uno al otro hace falta una **codificación** (por ejemplo UTF-8). **Los bytes no guardan qué codificación se usó**: quien los decodifica tiene que saberlo o averiguarlo.

| Operación | Dirección | Método |
|---|---|---|
| Codificar | `str` → `bytes` (hacia la máquina) | `str.encode()` |
| Decodificar | `bytes` → `str` (hacia el humano) | `bytes.decode()` |

`bytes` **no tiene** `.encode()` y `str` **no tiene** `.decode()`. Llamarlos lanza `AttributeError`.

Docs: [`str.encode`](https://docs.python.org/3/library/stdtypes.html#str.encode) · [`bytes.decode`](https://docs.python.org/3/library/stdtypes.html#bytes.decode) · [Bytes objects](https://docs.python.org/3/library/stdtypes.html#bytes-objects)

## Ejemplos básicos

```python
from urllib.request import urlopen  # imports al principio (PEP 8 / Ruff E402)

text = "hello"
data = b"hello"
print(type(data))            # <class 'bytes'>
print(data)                  # b'hello'
print(type(text))            # <class 'str'>
print(text)                  # hello
print(text.encode("utf-8"))  # b'hello'

print(list(text))  # ['h', 'e', 'l', 'l', 'o']  -> iterar str da caracteres
print(list(data))  # [104, 101, 108, 108, 111]  -> iterar bytes da enteros (0-255)

nums = [0, 65, 97, 255]
print(bytes(nums))  # b'\x00Aa\xff'
```

### Cómo se muestran los bytes

Python muestra un byte como carácter **solo si es ASCII imprimible**. Si no, lo muestra en hexadecimal:

- `0` → `\x00` (no imprimible)
- `65` → `A`, `97` → `a` (ASCII imprimible)
- `255` → `\xff` (fuera de ASCII, que llega hasta 127)

### Indexar vs. rebanar

```python
data[0]    # 104   -> int
data[0:1]  # b'h'  -> bytes
```

## Caracteres ≠ bytes

Con texto ASCII puro coinciden, y eso confunde. Con otros caracteres no:

```python
s = "ñandú"
b = s.encode("utf-8")
print(len(s), len(b))  # 5 7  -> ñ y ú ocupan 2 bytes cada una en UTF-8
print(b)               # b'\xc3\xb1and\xc3\xba'
```

Los literales `b"..."` solo aceptan caracteres ASCII: `b"ñ"` es un `SyntaxError`.

## Decodificar con la codificación equivocada

```python
b.decode("latin-1")  # 'Ã±andÃº'  -> no da error, pero el texto sale mal (mojibake)
b.decode("ascii")    # UnicodeDecodeError
```

El parámetro `errors` controla qué pasa cuando no se puede decodificar:

- `"strict"` (por defecto): lanza excepción.
- `"replace"`: reemplaza por `�`.
- `"ignore"`: descarta el byte.

Docs: [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html) · [Error handlers](https://docs.python.org/3/library/codecs.html#error-handlers)

## Leer bytes de la web

```python
url = "https://www.example.com"
with urlopen(url) as response:  # urlopen también es context manager
    data = response.read()
    charset = response.headers.get_content_charset() or "utf-8"

print(type(data))            # <class 'bytes'>
print(data.decode(charset))  # texto, usando la codificación que declaró el servidor
```

`bytes.decode()` usa `"utf-8"` por defecto, pero en la web conviene usar la codificación que declara el servidor en los headers en lugar de suponerla.

Docs: [`urllib.request.urlopen`](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen)

## Leer archivos binarios

```python
with open("avatar.png", mode="rb") as avatar:  # "rb" = read binary
    avatar_data = avatar.read()
    print(type(avatar_data))  # <class 'bytes'>
    print(len(avatar_data))   # cantidad de bytes del archivo
```

En modo binario (`"b"`), `open()` devuelve `bytes` sin decodificar nada. En modo texto, devuelve `str` y decodifica con el parámetro `encoding`. Docs: [`open()`](https://docs.python.org/3/library/functions.html#open)

## `bytes` vs. `bytearray`

- `bytes` es **inmutable**, como `str`.
- `bytearray` es la versión **mutable**: sirve para modificar datos binarios en el lugar.

Docs: [Bytearray objects](https://docs.python.org/3/library/stdtypes.html#bytearray-objects)
