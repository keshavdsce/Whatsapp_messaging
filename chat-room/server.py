import threading
import socket
import argparse
import os

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port
        self.lock = threading.Lock()  # Lock to ensure thread-safe access to connections

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(1)
        print("Listening at", sock.getsockname())

        while True:
            sc, sockname = sock.accept()
            print(f"Accepting a new connection from {sc.getpeername()} to {sc.getsockname()}")

            server_socket = ServerSocket(sc, sockname, self)
            server_socket.start()

            with self.lock:
                self.connections.append(server_socket)

            print("Ready to receive messages from", sc.getpeername())

    def broadcast(self, message, source):
        with self.lock:
            for connection in self.connections:
                if connection.sockname != source:
                    connection.send(message)

    def remove_connection(self, connection):
        with self.lock:
            self.connections.remove(connection)

class ServerSocket(threading.Thread):
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server
    
    def run(self):
        try:
            while True:
                message = self.sc.recv(1024).decode('ascii')
                if message:
                    print(f"[*] Received {message} from {self.sockname}")
                    self.server.broadcast(message, self.sockname)
                else:
                    print(f"Connection to {self.sockname} is closed")
                    self.sc.close()
                    self.server.remove_connection(self)
                    return
        except Exception as e:
            print(f"Error with connection {self.sockname}: {e}")
            self.sc.close()
            self.server.remove_connection(self)

    def send(self, message):
        try:
            self.sc.sendall(message.encode('ascii'))
        except Exception as e:
            print(f"Error sending message to {self.sockname}: {e}")
            self.sc.close()
            self.server.remove_connection(self)

def exit_program(server):
    while True:
        ipt = input('')
        if ipt == 'q':
            print("Closing all connections")
            for connection in server.connections:
                connection.sc.close()
            print("Shutting down the server")
            os._exit(0)  # exit the program

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat Room Server")
    parser.add_argument('host', help="Interface the server listens at")
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help="TCP port (default 1060)")

    args = parser.parse_args()
    server = Server(args.host, args.p)
    server.start()

    exiting = threading.Thread(target=exit_program, args=(server,))
    exiting.start()
