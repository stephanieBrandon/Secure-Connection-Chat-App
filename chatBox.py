# imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

#base
class ChatApp(App):
    def build(self):
        # layout for chat 
        chatLayout = BoxLayout(orientation='vertical')

        # Message block 
        self.messages_label = Label(text="Chat Application by Stephanie and Yulia")
        chatLayout.add_widget(self.messages_label)

        # text block
        self.text_input = TextInput(hint_text="Start typing")
        chatLayout.add_widget(self.text_input)

        # send button
        send_button = Button(text="Send")
        send_button.bind(on_press=self.send_message)
        chatLayout.add_widget(send_button)

        return chatLayout

    #refelect message 
    def send_message(self, instance):
        message = self.text_input.text
        self.messages_label.text += f"\n{message}"
        self.text_input.text = ""

if __name__ == "__main__":
    ChatApp().run()
