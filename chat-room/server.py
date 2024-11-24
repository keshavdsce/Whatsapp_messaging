import threading
import socket
import argparse
import os

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        #self.clients = []
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(1)
        print("Listening at", sock.getsockname())
        while True:
            
    def broadcast(self, message, source):
        for client in self.clients:
            if client.ip != source:
                client.send(message)