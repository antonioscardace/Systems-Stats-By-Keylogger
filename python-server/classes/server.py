import socket

from threading import Thread
from .client_thread import ClientThread

class Server:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    def binding(self, n):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((self.__host, self.__port))
        self.__sock.listen(n)

    def listen_all(self):
        while True:
            (victim_socket, address) = self.__sock.accept()
            Thread(target=ClientThread, args=(victim_socket,)).start()

    def close(self):
        self.__sock.close()