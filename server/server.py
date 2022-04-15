import json
import _thread
import socket


class User:
    def __init__(self, connection, address, name, password, command_token="/"):
        self.connection = connection
        self.address = address
        self.name = name
        self.password = password
        self.command_token = command_token
        # self.color = color
        self.admin = False


    def register(self):
        with open("users.json", "r+") as file:
            users = json.load(file)

        if users[self.name]:
            self.connection.send(str(len("REGISTER_FAILED")).encode("utf-8"))
            self.connection.send("REGISTER_FAILED".encode("utf-8"))
        else:
            users[self.name] = {
                "password": self.password,
                "admin": self.admin
            }
            json.dump(users, file)

            self.connection.send(str(len("REGISTER_SUCCESS")).encode("utf-8"))
            self.connection.send("REGISTER_SUCCESS".encode("utf-8"))


    def login(self):
        with open("users.json", "r+") as file:
            users = json.load(file)

        if users[self.name]["password"] == self.password:
            self.connection.send(str(len("LOGIN_SUCCESS")).encode("utf-8"))
            self.connection.send("LOGIN_SUCCESS".encode("utf-8"))
            self.admin = users[self.name]["admin"]
        else:
            self.connection.send(str(len("LOGIN_FAILED")).encode("utf-8"))
            self.connection.send("LOGIN_FAILED".encode("utf-8"))


def send(client, message):
    client.send(str(len(message)).encode("utf-8"))
    client.send(message.encode("utf-8"))


def broadcast(message):
    for client in clients:
        send(client, message)


def normal_send(client, message):
    for client in clients:
        if client.name != message.split(": ")[0]:
            send(client, message)


def receive_first(client):
    message_length = int(client.recv(1024).decode("utf-8"))
    message = client.recv(message_length).decode("utf-8")
    return message


def receive(client):
    message_length = int(client.connection.recv(1024).decode("utf-8"))
    message = client.connection.recv(message_length).decode("utf-8")
    return message


def receive_password(client):
    message_length = int(client.connection.recv(1024).decode("utf-8"))
    message = client.recv(message_length)
    return message


def handle_client(client):
    clients.append(client)
    print(f"{client} connected")
    while True:
        message = receive(client)
        if message == "DISCONNECT":
            clients.remove(client)
            print(f"{client} disconnected")
            break
        normal_send(message)


def main():
    server.listen()
    while True:
        client, address = server.accept()
        received = receive_first(client)
        client = User(client, address, receive_first(client), receive_password(client))

        if received == "REGISTER":
            client.register()
        elif received == "LOGIN":
            client.login()

        _thread.start_new_thread(handle_client, (client,))


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 55555))

    clients = []

    main()