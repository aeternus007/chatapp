import hashlib

def send(server, message):
    server.send(str(len(message)).encode("utf-8"))
    server.send(message.encode("utf-8"))


def receive(server):
    try:
        message_length = int(server.recv(1024).decode("utf-8"))
        message = server.recv(message_length).decode("utf-8")
        return message
    except:
        return "Disconnected with the server..."


def send_password(server, password):
    password_hash = hashlib.sha256(password.encode("utf-8")).digest()
    send(server, password_hash)