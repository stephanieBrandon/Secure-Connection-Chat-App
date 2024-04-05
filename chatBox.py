from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

#imports for connecting to server 
import socket 
import threading 

class ChatApp(App):
    def __init__(self, **kwargs):
        # give subclass same parameter signature as parent 
        super().__init__(**kwargs)
        # connect to the server setting set in file chat-server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 1077))
        #threading.Thread(target=self.receive_messages).start()

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # name of our prog
        title_label = Label(text="Stephanies and Yulia's chat app", size_hint_y=None, height=50)
        layout.add_widget(title_label)

        # view messages
        self.message_label = Label(text="", size_hint_y=None, height=50)
        layout.add_widget(self.message_label)
        
        # space to type
        self.text_input = TextInput(hint_text='Type here', multiline=False)
        layout.add_widget(self.text_input)
        
        # send button
        button = Button(text='Send')
        #connect to function
        button.bind(on_press=self.on_button_click)
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
