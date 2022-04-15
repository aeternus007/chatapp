from getpass import getpass
from rich import print as rprint
import socket
import threading

from utils import *


def main():
    choice = input("Do you want to login (0) or do you want to register(1)? ")
    if choice == "0":
        username = input("Enter your username: ")
        password = getpass(prompt="Enter your password: ")
        send(server, "LOGIN")
        send(server, username)
        send_password(server, password)
        response = receive(server)
        if response == "LOGIN_SUCCESS":
            rprint("Logged in successfully!")
            threading.Thread(target=send_messages, args=(username,)).start()
            threading.Thread(target=print_messages).start()
        else:
            rprint("Login failed!")
        
    elif choice == "1":
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")
        send(server, "REGISTER")
        send(server, username)
        send_password(server, password)
        response = receive(server)
        if response == "REGISTER_SUCCESS":
            rprint("Registration successful!")
            threading.Thread(target=send_messages, args=(username,)).start()
            threading.Thread(target=print_messages).start()
        else:
            rprint("Registration failed!")


def print_messages():
    while True:
        message = receive(server)
        rprint(message)


def send_messages(username):
    while True:
        message = f"{username}: {input()}"
        send(server, message)


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("", 55555))
    main()