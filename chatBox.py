from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

#imports for connecting to server 
import socket 
from threading import Thread
"""import sys
print(sys.path)"""
from client import MySocket

class ChatApp(MDApp):
    def __init__(self, **kwargs):
        # give subclass same parameter signature as parent 
        super().__init__(**kwargs)
        # connect to the server setting set in file chat-server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 1077))
        #threading.Thread(target=self.receive_messages).start()

    """def handle_received_message(self, message):
        # Process the message (e.g., extract sender, timestamp, etc.)
        # For now, let's assume the message format is "<sender>: <message>"
        _, received_message = message.split(":", 1)
        self.update_message(received_message.strip())  # Update the chat label
    """

    #- sb !important
    def recieved_data(self, instance):
            self.incoming_msg_label.text = self.client_socket.recv(1024).decode()

    def build(self):
        layout = MDBoxLayout(orientation='vertical')

        # name of our prog
        title_label = MDLabel(text="Stephanies and Yulia's chat app", size_hint_y=None, height=20, halign="center", valign="middle" )
        layout.add_widget(title_label)

        #- sb !important
        # view messages
        self.incoming_msg_label = MDLabel(text="incoming msg should appear here", size_hint=(1, None), height=500, halign="center", valign="middle" )
        layout.add_widget(self.incoming_msg_label)

        #-sb probably removing ignore ( same with in client.py file)
        #Label to display incoming messages 

        """
        class MyLabel(Label):
            def __init__(self, **kwargs):
                super(MyLabel, self).__init(**kwargs)

                self.sock = MySocket()
                Thread(target=self.get_data).start()

                def get_data(self):
                    while True:
                     recieved_msg = 'test'
                     recieved_msg = self.text = self.sock.get_data()

        """

        button_height = 100 

        # space to type
        self.text_input = MDTextField(hint_text='Type here',  multiline=False, size_hint=(1, None), height=button_height)
        layout.add_widget(self.text_input)
        
        button = MDRaisedButton(text='Send', size_hint=(1, None), height=button_height)

        #connect to function
        button.bind(on_press=self.on_button_click)
        #- sb !important
        button.bind(on_release=self.recieved_data)
        layout.add_widget(button)

        return layout

    #function to reflect typed messages use for testing
    def on_button_click(self, instance):
        message = self.text_input.text
        #send message to server
        self.client_socket.send(message.encode('utf-8'))
        # clear input box 
        self.text_input.text = '' 

    """
    #function to display who the message is from

    -- function passing self, addess of the user, and the message we have 
    def incoming_message(self, address, message):
    
    -- split incoming context 
    ip , port = address.split(':')

    -- display the messsage 
    self.incoming_msg_label.text += f"FROM {port}: {message}\n"
    """

if __name__ == '__main__':
    ChatApp().run()