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
    #DELETE MAYBE
    host = 'localhost'  
    port = 1077  

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
        layout = MDBoxLayout(orientation='vertical', padding=40, spacing=20) 

        # Title
        title_label = MDLabel(text="Stephanies and Yulia's chat app", size_hint_y=None, height=50, halign="center", valign="middle" )
        layout.add_widget(title_label)

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
        
        button = MDRaisedButton(text='Send', size_hint=(1, None), height=button_height)

        #self.username_input = TextInput(hint_text='Username', multiline=False)
        #layout.add_widget(self.username_input)
        #connect to server button
        #connect_button = Button(text='Connect')
        #connect_button.bind(on_press=self.connect_to_server)
        # User input section
        username_label = MDLabel(text="Name:", size_hint=(None, None), size=(100, 50), halign="center", valign="middle")
        layout.add_widget(username_label)
        self.username_input = MDTextField(hint_text='type name here', size_hint=(None, None), size=(250, 100))
        layout.add_widget(self.username_input)
        # user input Button
        connect_button = MDRaisedButton(text='Connect', size_hint=(None, None), size=(100, 50))
        connect_button.bind(on_press=self.connect_to_server)
        layout.add_widget(connect_button)

        #- sb !important
        # view messages
        self.incoming_msg_label = MDLabel(text="incoming msg should appear here", size_hint=(1, None), height=500, halign="center", valign="middle" )
        layout.add_widget(self.incoming_msg_label)

        # space to type
        self.text_input = MDTextField(hint_text='Type here', multiline=False)
        layout.add_widget(self.text_input)
        
        # send button
        button = MDRaisedButton(text='Send')
        #connect to function
        button.bind(on_press=self.on_button_click)
        #- sb !important
        button.bind(on_release=self.recieved_data)
        layout.add_widget(button)

        return layout
        # -sb -Tues
        # -??? self.client_socket.send('clientA'.encode('utf-8'))
    def connect_to_server(self, instance):

        #disable button after pressed 
        #instance.disabled = True 

        username = self.username_input.text

        #connect method to connect our client to the server.
        self.client_socket.connect((self.host, self.port))
    
        #where 'client' is we want the entry of what user put in as their user name
        print(f'username: {username}')
        self.client_socket.send(username.encode('utf-8'))

        #self.name_label['state'] = "disable"
        #self.username_input['state'] = "disable"
        #self.connect_button['state'] = "disable"
        msg_thread = threading.Thread(target=self.listen_to_server)
        msg_thread.daemon = True # marked as Daemon so that it will close when the main thread closes.
        msg_thread.start()

    
    def listen_to_server(self):
        while (True):
            dataBytes = self.client_socket.recv(1024)
            #yulia replace with text box 
            self.text_input.text = dataBytes.decode()

    def send_to_server(self, instance):
        #send the message from client to the server.
        #yulia -substitute in kivy? -- shows users msgs in blue
       #self.main_textbox.tag_config("self_message", foreground="blue")
        message = self.text_input.text
        #encode to convert the string to array of bytes to send to the server
        self.client_socket.send(message.encode('utf-8'))
        #clearing the input box
        #self.text_input.text = ''
        self.text_input.text = f'\n{self.username_input.text}:\n   {message}' #, "self_message" add back if able to create blue in kivy

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