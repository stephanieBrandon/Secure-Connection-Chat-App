from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class ChatApp(App):
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
        self.message_label.text = f"USER A: {message}"
     # clear input box 
        self.text_input.text = '' 


if __name__ == '__main__':
    ChatApp().run()
