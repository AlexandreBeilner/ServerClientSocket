class Events:
    def __init__(self, sio, ui):
        self.ui = None
        self.sio = sio
        self.register()
        self.ui = ui

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

    def on_connect(self):
        print("Connected to the server...")

    def on_disconnect(self):
        print("Disconnected from the server...")

    def on_message(self, data):
        self.ui.add_message(data['user'], data['message'])
