import socketio
from modules.events import Events


class Connection:
    def __init__(self, route, port):
        self.sio = socketio.Client()

        self.url = f'http://{route}:{port}'
        self.password = "password"

        self.events()

    def events(self):
        Events(self.sio)

    def connect(self):
        try:
            self.sio.connect(f'{self.url}?token={self.password}')
        except Exception as error:
            print(f"Error connecting in the server: {error}")

    def disconnect(self):
        self.sio.disconnect()

    def start(self):
        self.sio.wait()


if __name__ == '__main__':
    connection = Connection('localhost', 3000)
