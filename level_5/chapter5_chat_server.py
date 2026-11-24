# chat_server.py
import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def broadcaste(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcaste(message)
        except:
            index = clients.index(
                client
            )  # index => raise ValueError if the value is not presente,
            # en los siguientes pasos lo eliminamos y cerramos la conexión y hacemos lo mismo para el nickname asociado
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcaste(f"{nickname} left the chat!".encode("ascii"))
            nicknames.remove(nickname)
            break


def receive():  # This is the main loop
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}!")
        broadcaste(f"{nickname} joined the chat!".encode("ascii"))
        client.send("Connected to the server".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening")
receive()
