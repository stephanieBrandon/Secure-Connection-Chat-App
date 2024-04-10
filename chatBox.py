from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

#imports for connecting to server 
import socket 
import threading
from client import MySocket


class ChatApp(App):
    def __init__(self, **kwargs):
        # give subclass same parameter signature as parent 
        super().__init__(**kwargs)
        # connect to the server setting set in file chat-server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 1077))
        # -sb -Tues
        # -??? self.client_socket.send('clientA'.encode('utf-8'))
    def connect_to_server(self):
        #connect method to connect our client to the server.
        self.client_socket.connect((self.host, self.port))
        #where 'client' is we want the entry of what user put in as their user name
        # - yulia replace name_text with kivy version
        username = self.username_input.get()
        self.client_socket.send(username.encode('utf-8'))
        #self.name_label['state'] = "disable"
        self.username_input['state'] = "disable"
        self.connect_button['state'] = "disable"
        msg_thread = threading.Thread(target=self.listen_to_server)
        msg_thread.daemon = True # marked as Daemon so that it will close when the main thread closes.
        msg_thread.start()
    
    def listen_to_server(self):
        while (True):
            dataBytes = self.client_socket.recv(1024)
            #yulia replace with text box 
            self.incoming_msg_label.text =  dataBytes.decode()

    def send_to_server(self):
        #send the message from client to the server.
        #yulia -substitute in kivy? -- shows users msgs in blue
       #self.main_textbox.tag_config("self_message", foreground="blue")
        message = self.text_input.get()
        #encode to convert the string to array of bytes to send to the server
        self.client_socket.send(message.encode('utf-8'))
        #clearing the input box
        self.text_input.text = ''
        self.incoming_msg_label.text = f'\n{self.name_text.get()}:\n   {message}' #, "self_message" add back if able to create blue in kivy

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # name of our prog
        title_label = Label(text="Stephanies and Yulia's chat app", size_hint_y=None, height=50)
        layout.add_widget(title_label)
        #- sb !important
        # view messages
        self.incoming_msg_label = Label(text="incoming msg should appear here", size_hint_y=None, height=50)
        layout.add_widget(self.incoming_msg_label)

        #-sb probably removing ignore ( same with in client.py file)
        #Label to display incoming messages 
        class MyLabel(Label):
            def __init__(self, **kwargs):
                super(MyLabel, self).__init(**kwargs)

        # space to type
        self.text_input = TextInput(hint_text='Type here', multiline=False)
        layout.add_widget(self.text_input)
        
        # send button
        button = Button(text='Send')
        #connect to function
        button.bind(on_press=self.on_button_click) #-sb remove?
        button.bind(on_press=self.send_to_server)
        #- sb !important
        #button.bind(on_release=self.recieved_data)
        layout.add_widget(button)

        # space to type
        self.username_input = TextInput(hint_text='Username', multiline=False)
        layout.add_widget(self.username_input)
        #connect to server button
        connect_button = Button(text='Connect')
        connect_button.bind(on_press=self.connect_to_server)

        return layout

    #function to reflect typed messages use for testing
    def on_button_click(self, instance):

       # message = self.text_input.text
        #send message to server
      #  self.client_socket.send(message.encode('utf-8'))
     # clear input box 
        self.text_input.text = '' 


if __name__ == '__main__':
    ChatApp().run()
