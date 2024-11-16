import os
from tkinter import *
from modules.connection import Connection


class UI:
    def __init__(self):
        self.sio = None
        self.name_entry = None
        self.password_entry = None
        self.window = Tk()
        self.input_entry = None
        self.name = None
        self.password = None
        self.connection = Connection('localhost', 3000, self)

    def start(self):
        self.start_registration_screen()

    def start_registration_screen(self):
        self.window.geometry('400x300')
        self.window.title("Conectar ao Chat")

        name_label = Label(self.window, text="Nome:", font=('Helvetica', 14))
        name_label.pack(pady=10)

        self.name_entry = Entry(self.window, font=('Helvetica', 14))
        self.name_entry.pack(pady=5)

        password_label = Label(self.window, text="Senha:", font=('Helvetica', 14))
        password_label.pack(pady=10)

        self.password_entry = Entry(self.window, font=('Helvetica', 14), show="*")
        self.password_entry.pack(pady=5)

        connect_button = Button(self.window, text="Conectar", font=('Helvetica', 14), command=self.on_connect)
        connect_button.pack(pady=20)
        self.window.mainloop()

    def start_chat_screen(self):
        self.window = Tk()
        self.window.geometry('800x800')
        self.window.title("Trabalho Moreto")

        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../assets/images.png'))

        icon = PhotoImage(file=image_path)
        self.window.iconphoto(True, icon)

        self.window.config(background='black')

        self.add_input()

        self.window.mainloop()

    def on_connect(self):
        self.name = self.name_entry.get()
        self.password = self.password_entry.get()

        self.connection.connect(self.password)
        self.sio = self.connection.get_sio()

        self.window.destroy()
        self.start_chat_screen()
        self.connection.start()

    def add_message(self, user, message, color='green'):
        frame = Frame(self.window, bg="black")
        frame.pack(pady=8, fill='x', padx=10)

        text_user = Label(frame, text=user + ': ', font=('Helvetica', 14), fg=color, bg="black", anchor='w')
        text_user.pack(side=LEFT)

        text_message = Label(frame, text=message, font=('Helvetica', 14), fg="white", bg="black", anchor='w')
        text_message.pack(side=LEFT)

    def add_input(self):
        input_frame = Frame(self.window, bg="black")
        input_frame.pack(side=BOTTOM, fill='x', padx=10, pady=10)

        input_label = Label(input_frame, font=('Helvetica', 18), fg="white", bg="black")
        input_label.pack(side=LEFT)

        self.input_entry = Entry(input_frame, font=('Helvetica', 14))
        self.input_entry.pack(side=LEFT, fill='x', expand=True)

        self.input_entry.bind('<Return>', self.on_enter_pressed)

    def on_enter_pressed(self, event):
        input_value = self.input_entry.get()

        if len(input_value) > 0:
            self.add_message(self.name, input_value, 'blue')
            self.send_message(input_value)
            self.input_entry.delete(0, END)

    def send_message(self, message):
        self.sio.emit('message', {'message': message, 'user': self.name})