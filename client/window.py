from PyQt6.QtWidgets import QApplication, QMainWindow
import sys


class Window(QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)

        super().__init__()

        self.create()

    def create(self):
        self.setWindowTitle("Window")
        self.setGeometry(100, 100, 800, 600)

    def show(self):
        super().show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    window = Window()
    window.show()
