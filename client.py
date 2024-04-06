import socket
import sys
from threading import Thread

HEADER_LENGTH = 10
cleint_socket = None

#method to connect a client to the server
# -sb potentially add username and error callback
def client_connect(ip, port, error_callback):

    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(('localhost', 1077))
        print(f"client succesfully connected.")
    except Exception as e:
        error_callback('There was a connnection error: {}'.format(str(e)))
        return False
    return True

#method to send the message
def send_msg(message):
    message = message.encode('utf-8')
    # -sb add message header?
    client_socket.send(message)

#method to recieve incoming messages
def start_recieve_msg(incoming_msg, error_callback):
    #the below target is targeting the listen method below
    Thread(target=listen, args=(incoming_msg, error_callback),daemon=True ).start()

def listen(incoming_msg, error_callback):
    while True:
        
        try:
            while True:
                username_header = client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    error_callback('Connection closed by the server.')
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')
                incoming_msg(message)
        except Exception as e:
            error_callback('The following error occured: {}'.format(str(e)))

