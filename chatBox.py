from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

#imports for connecting to server 
import socket 
from threading import Thread
"""import sys
print(sys.path)"""
from client import MySocket


class ChatApp(App):
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
    def recieved_data(self, instance):
            self.incoming_msg_label.text = self.client_socket.recv(1024).decode()

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # name of our prog
        title_label = Label(text="Stephanies and Yulia's chat app", size_hint_y=None, height=50)
        layout.add_widget(title_label)

        # view messages
        self.incoming_msg_label = Label(text="incoming msg should appear here", size_hint_y=None, height=50)
        layout.add_widget(self.incoming_msg_label)


        #Label to display incoming messages 
        class MyLabel(Label):
            def __init__(self, **kwargs):
                super(MyLabel, self).__init(**kwargs)

                self.sock = MySocket()
                Thread(target=self.get_data).start()

                def get_data(self):
                    while True:
                     recieved_msg = 'test'
                     recieved_msg = self.text = self.sock.get_data()
        
        # space to type
        self.text_input = TextInput(hint_text='Type here', multiline=False)
        layout.add_widget(self.text_input)
        
        # send button
        button = Button(text='Send')
        #connect to function
        button.bind(on_press=self.on_button_click)
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


if __name__ == '__main__':
    ChatApp().run()
