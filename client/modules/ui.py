import os
from tkinter import LEFT, BOTTOM, END, Label, Scrollbar, Canvas
from modules.connection import Connection
from modules.window import Window
from modules.video import Video


class UI:
    def __init__(self):
        self.video_manager = Video()
        self.has_video = False
        self.all_chats_id = []
        self.id_active_chat = None
        self.all_chats = []
        self.input_frame = None
        self.chat_frame = None
        self.users_frame = None
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
        self.window.setup("Chat", "800x600", background='black')

        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../assets/images.png'))
        self.window.set_icon(True, image_path)

        self.window.grid_columnconfigure(0, weight=3)
        self.window.grid_columnconfigure(1, weight=7)

        self.window.grid_rowconfigure(0, weight=9)
        self.window.grid_rowconfigure(1, weight=1)

        self.users_frame = self.window.frame(bg='#282C34', row=0, column=0, sticky='nsew', rowspan=2)

        chat_container = self.window.frame(bg='#3e495e', row=0, column=1, sticky='nsew')

        canvas = Canvas(chat_container, bg='#3e495e')
        canvas.pack(side='left', fill='both', expand=True)

        scrollbar = Scrollbar(chat_container, command=canvas.yview)
        scrollbar.pack(side='right', fill='y')

        canvas.config(yscrollcommand=scrollbar.set)

        self.chat_frame = self.window.frame(bg='#3e495e', frame=canvas)
        canvas.create_window((0, 0), window=self.chat_frame, anchor='nw')

        self.chat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.add_input()
        self.add_chat('Chat Geral', 'general')
        self.set_active_chat('general')

        self.window.start()

    def on_connect(self):
        self.name = self.name_entry.get()
        self.password = self.password_entry.get()
        self.window.stop()
        self.window.create()

        self.connection.connect(self.password, self.name)
        self.sio = self.connection.get_sio()

        self.start_chat_screen()
        self.connection.start()

    def add_message(self, user, message, color='green', message_color='white'):
        row = len(self.chat_frame.winfo_children())
        frame = self.window.frame(bg='#3e495e', padx=10, pady=10, row=row, column=0, sticky='ew', frame=self.chat_frame)
        self.window.label(user + ': ',
                          fg=color,
                          bg='#3e495e',
                          frame=frame,
                          side=LEFT)
        self.window.label(message,
                          fg=message_color,
                          bg='#3e495e',
                          frame=frame,
                          side=LEFT)

    def add_input(self):
        self.input_frame = self.window.frame(bg='black', row=1, column=1, sticky="ew")

        self.window.label('', frame=self.input_frame, side=LEFT, fg='white', bg='black')

        self.input_entry = self.window.input(frame=self.input_frame, side=LEFT, expand=True, bg='black', fg='white')
        self.input_entry.bind('<Return>', self.on_enter_pressed)

    def on_enter_pressed(self, event):
        input_value = self.input_entry.get()

        if len(input_value) > 0:
            self.add_message(self.name, input_value, color='blue')
            if self.id_active_chat == 'general':
                self.send_message(input_value)
            else:
                self.send_private_message(input_value, self.id_active_chat)
            self.input_entry.delete(0, END)

        # if input value starts with / run a command
        if input_value.startswith('/'):
            if input_value == '/startVideo':
                self.add_message(self.name, input_value, color='blue')
                self.send_video_status('online')
                self.input_entry.delete(0, END)
                self.video_manager.start(self.sio)
                return
            elif input_value == '/stopVideo':
                self.add_message(self.name, input_value, color='blue')
                self.send_video_status('offline')
                self.input_entry.delete(0, END)
                self.video_manager.stop()
                return
            elif input_value == '/connectInCall' and self.has_video:
                self.sio.emit('show_video')
                self.input_entry.delete(0, END)
                self.video_manager.render_video()
                return


            input_value = input_value[1:]
            self.add_message(self.name,
                             input_value,
                             color='blue',
                             message_color='red')
            self.send_command(input_value)
            self.input_entry.delete(0, END)
            return

    def send_message(self, message):
        self.sio.emit('message', {'message': message, 'user': self.name})

    def send_command(self, command):
        self.sio.emit('command', {'message': command, 'user': self.name})

    def send_video_status(self, status):
        self.sio.emit('video_status', {'status': status, 'user': self.name})

    def send_private_message(self, message, send_to):
        self.sio.emit('private_message', {'message': message, 'user': self.name, 'to': send_to})

    def add_chat(self, user_name, id):
        row = len(self.all_chats)

        chat_button = self.window.button(
            text=user_name,
            command=lambda: self.set_active_chat(id),
            bg='#859cd4',
            fg='white',
            font=('Helvetica', 14, 'bold'),
            row=row,
            column=0,
            padx=5,
            pady=2,
            sticky='ew',
            frame=self.users_frame
        )

        chat_button.id = id
        self.all_chats.append(chat_button)
        self.all_chats_id.append(id)

    def on_user_click(self, event, frame):
        chat_id = frame.id
        self.set_active_chat(chat_id)
        self.id_active_chat = chat_id


    def on_mouse_enter(self, event):
        event.widget.config(cursor="hand2")

    def on_mouse_leave(self, event):
        event.widget.config(cursor="")

    def set_active_chat(self, id):
        for chat in self.all_chats:
            if chat.id == id:
                chat.config(background='green', fg='white')
            else:
                chat.config(background='#859cd4', fg='white')

        self.id_active_chat = id