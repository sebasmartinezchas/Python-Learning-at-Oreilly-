# server.py
import socket

HOST = "127.0.0.1"  # Standard loopback interface addess (localhost)
PORT = 65432  # Port to liest on (non-rpivileged ports are > 1023)

with socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
) as s:  # Creamos un objeto socket, con with nos aseguramos que se cierre
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = (
        s.accept()
    )  # Esta es la parte importante: s.accept es una llamada de bloqueo, el programa se detendrá
    # aquí y esperará hasta que un cliente se conecte. Devuelve una tupla conn =>socket  and addr => _RetAddress. Mientras exista la conexión
    # la estaremos iterando en el bucle. La gran limitación de este esquema es que puede gestionar un cliente por vez. PAra hcer algo tipo chat
    # necesitaremos el modulo threading
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)  # Envia la data
