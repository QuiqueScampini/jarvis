from threading import Thread
from util import Constant
import socket


class MessageServer(Thread):

    message_socket = None
    val = None
    active = False

    def __init__(self, val):
        Thread.__init__(self)
        self.val = val
        self.start_socket()
        self.active = True

    def start_socket(self):
        self.message_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_socket.bind((Constant.MessageServerIP, Constant.MessageServerPort))
        self.message_socket.listen(1)

    def run(self):
        print("Start server receptor")
        connection, client_address = self.message_socket.accept()
        try:
            while self.active:
                message = connection.recv(Constant.MessageServerBufferSize)
                if message:
                    print("received message:", message)
                    connection.send(message)  # echo
                else:
                    break
        finally:
            connection.close()
        print("Stop server receptor")

    def stop(self):
        self.active = False
        self.message_socket.shutdown(socket.SHUT_WR)

