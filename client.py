import socket

# -sb this is so that the GUI can get the messages back to display.
class MySocket:
    def __init__(self, host="localhost", port= 1077):
        self.sock = socket.socket()
        self.sock.connect((host, port))

        def get_data(self):
            return self.sock.recv(1024)