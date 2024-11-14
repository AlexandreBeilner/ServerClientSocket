class Events:
    def __init__(self, sio):
        self.sio = sio
        self.register()

    def register(self):
        @self.sio.event
        def connect():
            self.on_connect()

        @self.sio.event
        def disconnect():
            self.on_disconnect()

    def on_connect(self):
        print("Connected to the server...")

    def on_disconnect(self):
        print("Disconnected from the server...")
