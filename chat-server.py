#figure out how to change the data from only displaying in terminal to having that data passed through client.py class MySocket
import kivy
print(kivy.__version__)
#objective create a reliable connection for chat application using TCP
import socket
import threading
"""from chatBox import handle_received_message
import sys
print(sys.path)"""

host = 'localhost' #refers to the loopback interface of the local machine 127.0.0.1 IE listens for connections only on this machine

#handle client connections
def handle_client(client_socket, address):
    print(f"Connection from {address}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        print(f"Recieved data from {address}: {data.decode('utf-8')}")

        client_socket.send(data)
    client_socket.close()
    print(f"The connection from {address} has been closed.")

"""def recieve_message(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                handle_received_message(data.decode("utf-8"))
        except ConnectionResetError:
            print("Connection closed by server.")
            break"""
#Server config
def main():
    host
    port = 1077

    #TCP socket creation
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Binding the socket to the address and port
    server_socket.bind((host, port))

    #setting it to listen for up to 5 connections.
    server_socket.listen(5)
    print(f"Server is listening on {host} : {port}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            #create a thread for each new connecting client.
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
            """client_socket.send()"""
    except KeyboardInterrupt:
        print("Server is shutting down.")
        server_socket.close()
if __name__ == "__main__":
    main()