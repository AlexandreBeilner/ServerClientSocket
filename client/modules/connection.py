import socket


class Connection:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect(self):
        self.client.connect((self.host, self.port))

    def send(self, data):
        self.client.send(data)

    def receive(self):
        return self.client.recv(1024)

    def close(self):
        self.client.close()


if __name__ == '__main__':
    connection = Connection('127.0.0.1', 8080)
