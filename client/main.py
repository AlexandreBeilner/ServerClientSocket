from modules.connection import Connection


def main():
    connection = Connection('localhost', 3000)
    connection.connect()
    connection.start()


if __name__ == '__main__':
    main()
