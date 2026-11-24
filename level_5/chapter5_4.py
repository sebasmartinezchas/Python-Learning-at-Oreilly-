# Work with Binary Files and Encoding in Python / Representing Binary data with bytes
"""
Los datos binarios en Python se representan con el tipo bytes.Los bytes no guardan su codificación:
para convertirlos a texto, hay que indicar cual se usó.

"""

from urllib.request import urlopen

text = "hello"
data = b"hello"
print(type(data))  # <class 'bytes'>
print(data)  # b'hello'
print(type(text))  # <class 'str'>
print(text)  # hello
print(text.encode())  # b'hello'


print(list(text))  # ['h', 'e', 'l', 'l', 'o']
print(list(data))  # [104, 101, 108, 108, 111]
nums = [0, 65, 97, 255]
print(bytes(nums))  # b'\x00Aa\xff'


with urlopen("https://www.example.com") as response:
    data = response.read()
    print(type(data))  # <class 'bytes'>
    print(data)
    # print(data.encode('utf-8'))  #  Mal, no se puede codificar bytes,
    # Decodifica los bytes a texto usando UTF-8 explícitamente (buena práctica)
    print(data.decode("utf-8"))

with open("avatar.png", mode="rb") as avatar:
    avatar_data = avatar.read()
    print(type(avatar_data))  # <class 'bytes'>
    print(len(avatar_data))  # Muestra la longitud de los datos leídos
