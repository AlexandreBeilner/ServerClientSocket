import socketio
from modules.events import Events

class Connection:
    def __init__(self, route, port, ui):
        self.sio = socketio.Client()
        self.url = f'http://{route}:{port}'
        self.ui = ui
        self.events()

    def events(self):
        Events(self.sio, self.ui)

    def connect(self, user_password):
        try:
            self.sio.connect(f'{self.url}?token={user_password}')
        except Exception as error:
            print(f"Error connecting in the server: {error}")

    def disconnect(self):
        self.sio.disconnect()

    def start(self):
        self.sio.wait()

    def get_sio(self):
        return self.sio