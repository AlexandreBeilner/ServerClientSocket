import os
from tkinter import LEFT, BOTTOM, END
from modules.connection import Connection
from modules.window import Window


class UI:
    def __init__(self):
        self.sio = None

        self.name_entry = None
        self.password_entry = None

        self.window = Window()

        self.input_entry = None
        self.name = None
        self.password = None
        self.connection = Connection('localhost', 3000, self)

    def start(self):
        self.start_registration_screen()

    def start_registration_screen(self):
        self.window.setup("Conectar ao Chat", "400x300")

        self.window.label("Nome:", pady=10)
        self.name_entry = self.window.input(pady=5)

        self.window.label("Senha:", pady=10)
        self.password_entry = self.window.input(pady=5)

        self.window.button("Conectar", self.on_connect, pady=10)

        self.window.start()

    def start_chat_screen(self):
        self.window.create()
        self.window.setup("Chat", "800x600", background='black')

        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                  '../../assets/images.png'))
        self.window.set_icon(True, image_path)

        self.add_input()

        self.window.start()

    def on_connect(self):
        self.name = self.name_entry.get()
        self.password = self.password_entry.get()

        self.connection.connect(self.password)
        self.sio = self.connection.get_sio()

        self.window.stop()
        self.start_chat_screen()
        self.connection.start()

    def add_message(self, user, message, color='green'):
        frame = self.window.frame(bg='black', padx=10, pady=10)
        self.window.label(user + ': ',
                          fg=color,
                          bg='black',
                          frame=frame,
                          side=LEFT)
        self.window.label(message,
                          fg='white',
                          bg='black',
                          frame=frame,
                          side=LEFT)

    def add_input(self):
        input_frame = self.window.frame(padx=10,
                                        pady=10,
                                        side=BOTTOM,
                                        bg='black')

        self.window.label('Digite sua mensagem:',
                          frame=input_frame,
                          side=LEFT,
                          fg='white',
                          bg='black')

        self.input_entry = self.window.input(frame=input_frame,
                                             side=LEFT,
                                             expand=True,
                                             bg='black',
                                             fg='white')
        self.input_entry.bind('<Return>', self.on_enter_pressed)

    def on_enter_pressed(self, event):
        input_value = self.input_entry.get()

        if len(input_value) > 0:
            self.add_message(self.name, input_value, 'blue')
            self.send_message(input_value)
            self.input_entry.delete(0, END)

    def send_message(self, message):
        self.sio.emit('message', {'message': message, 'user': self.name})
