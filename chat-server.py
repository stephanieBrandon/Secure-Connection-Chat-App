#figure out how to change the data from only displaying in terminal to having that data passed through client.py class MySocket
import kivy
print(kivy.__version__)
#objective create a reliable connection for chat application using TCP
import socket
import threading
from kivy.clock import Clock

class ServerManager:
    #method to set up the chat's server
    def set_up_server(self):
        host = '127.0.0.1'
        port = 1077
        #creating a IPv4, TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #binding this socket to the designated host(IP) and port
        self.server_socket.bind((host, port))
        #when new client connects add it to our connected clients list
        self.clients = []
        #setting the maximum clients this server will accept to connect.
        self.server_socket.listen(5)
        print(f"Server is listening on host {host} and port {port}")
        #a while loop to continually accept new connections 
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection from {address}")
            #-sb need to get the username from the client after it connects here.
            username = client_socket.recv(1024)
            print(f'user: {username.decode()} is connected to the server.')
            self.clients.append(client_socket)
            #-sb now incorportating threads to handle the already connected clients
            # msgs so that our while loop can keep accepting connection while our threads deal with the msgs.
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, username.decode()))
            client_thread.start()
    def handle_client(self, client_socket, username):
        try:
            # this method had a while loop that keeps listening to incoming msgs from the client_socket passed to it that is connected to a specific client
            while True:
                #if we get an empty msg we conclude that the client disconnected.
                data = client_socket.recv(1024) # this recieve method is blocking. 
                if not data:
                    break
                print(f"{username}: {data.decode()}")
                #client_socket.send(f'\n{username}: \n   '.encode('utf-8') + data)
                for sock in self.clients:
                    if sock == client_socket:
                       continue 
                    # Schedule the message sending on the main thread
                    Clock.schedule_once(lambda dt: self.broadcast_message(sock, username, data.decode()), 0)
                    sock.sendall(f'\n{username}: \n   '.encode('utf-8') + data)
        except ConnectionResetError:
            pass
        finally:
            #close socket from the server side
            client_socket.close()
            print(f'{username}\'s socket is closed.')
            self.clients.remove(client_socket)
    def broadcast_message(self, sender_username, message, client_socket):
        # Send the message to all connected clients except the sender
        for sock in self.clients:
            if sock != client_socket:
                sock.sendall(f"\n{sender_username}:\n   {message}".encode("utf-8"))
            
if __name__ == '__main__':
    server_manager = ServerManager()
    server_manager.set_up_server()
