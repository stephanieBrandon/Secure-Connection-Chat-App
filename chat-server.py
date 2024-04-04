#objective create a reliable connection for chat application using TCP
import socket
import threading 

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

            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
        server_socket.close()
if __name__ == "__main__":
    main()