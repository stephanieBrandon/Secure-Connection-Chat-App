#objective create a reliable connection for chat application using TCP
import socket
import threading 
import select

HEADER_LENGTH = 10

host = 'localhost' #refers to the loopback interface of the local machine 127.0.0.1 IE listens for connections only on this machine
port = 1077

#TCP socket creation
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Binding the socket to the address and port
server_socket.bind((host, port))
#setting it to listen for up to 5 connections.
# -sb potentially change to a list instead of a set amount of 5
server_socket.listen(5)
sockets_list = [server_socket]
print(f"Server is listening on {host} : {port} for connections.")

def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = recieve_message(client_socket)

#handle client connections
#def handle_client(client_socket, address):
    #print(f"Connection from {address}")

   # while True:
        # -sb change to recieve msg from client
      #  data = client_socket.recv(1024)
       # if not data:
       #     break

      #  print(f"Recieved data from {address}: {data.decode('utf-8')}")

      #  client_socket.send(data)
    #client_socket.close()
  #  print(f"The connection from {address} has been closed.")
#Server config
def main():


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