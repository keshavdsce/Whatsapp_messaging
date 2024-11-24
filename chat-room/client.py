import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root = tk.Tk()
        self.root.title("Chat Client")

        self.messages = scrolledtext.ScrolledText(self.root)
        self.messages.pack()

        self.input_user = tk.StringVar()
        self.input_field = tk.Entry(self.root, text=self.input_user)
        self.input_field.pack(side=tk.BOTTOM, fill=tk.X)
        self.input_field.bind("<Return>", self.enter_pressed)

    def start(self):
        print("Trying to connect to {}:{}...".format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print("Successfully Connected to {}:{}".format(self.host, self.port))

        self.name = input("Your name: ")
        print("Welcome, {}! Getting ready to send and receive messages...".format(self.name))

        receive = Receive(self.sock, self.name, self.messages)
        receive.start()

        self.sock.sendall('Server: {} has joined the chat. Say hello to buddy!'.format(self.name).encode('ascii'))
        print("\rAll set! Leave the chat anytime by typing 'Quit'\n")
        print('{}: '.format(self.name), end='')

        self.root.mainloop()

    def enter_pressed(self, event):
        message = self.input_user.get()
        self.input_field.delete(0, tk.END)
        self.messages.insert(tk.END, '{}: {}\n'.format(self.name, message))

        if message == "Quit":
            self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))
            print('\nQuitting...')
            self.sock.close()
            self.root.quit()
        else:
            self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))

class Receive(threading.Thread):
    def __init__(self, sock, name, messages):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = messages

    def run(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('ascii')
                if message:
                    self.messages.insert(tk.END, message + '\n')
                else:
                    print("\nConnection closed by the server.")
                    self.sock.close()
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.sock.close()
                break

if __name__ == "__main__":
    host = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    client = Client(host, port)
    client.start()